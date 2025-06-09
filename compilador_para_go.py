import sys
import re
import io
import contextlib

class PrePro:
    def filter(self, source):
        return re.sub(r"//.*", "", source)

class Token:
    def __init__(self, type: str, value: int):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        palavras_reservadas = ['Println', 'if', 'else', 'for', 'Scan', 'var', 'true', 'false', 'int', 'string', 'bool', 'return', 'func']
        if len(self.source) == self.position:
            self.next = Token('EOF', '')
            return
        char = self.source[self.position]
        while char == ' ' or char == '\t':
            self.position += 1
            if len(self.source) == self.position:
                self.next = Token('EOF', '')
                return
            char = self.source[self.position]
        value = 0
        if char.isdigit():
            while char.isdigit():
                value = value * 10 + int(char)
                self.position += 1
                if len(self.source) == self.position:
                    break
                char = self.source[self.position]
            self.next = Token('int', value)
        elif char == '+':
            self.next = Token('plus', char)
            self.position += 1
        elif char == '-':
            self.next = Token('minus', char)
            self.position += 1
        elif char == '*':
            self.next = Token('times', char)
            self.position += 1
        elif char == '/':
            self.next = Token('divided', char)
            self.position += 1
        elif char == '(':
            self.next = Token('open_par', char)
            self.position += 1
        elif char == ')':
            self.next = Token('close_par', char)
            self.position += 1
        elif char == "{":
            self.next = Token('open_chave', char)
            self.position += 1
        elif char == "}":
            self.next = Token('close_chave', char)
            self.position += 1
        elif char == ",":
            self.next = Token('comma', char)
            self.position += 1
        elif char == "\n":
            self.next = Token('enter', char)
            self.position += 1
        elif char == "=":
            if self.source[self.position + 1] == "=":
                self.next = Token('equals', '==')
                self.position += 2
            else:
                self.next = Token('assign', '=')
                self.position += 1
        elif char == '!':
            self.next = Token('not', char)
            self.position += 1
        elif char == "<":
            self.next = Token('less', char)
            self.position += 1
        elif char == ">":
            self.next = Token('greater', char)
            self.position += 1
        elif char == "|" and self.source[self.position + 1] == "|":
            self.next = Token('or', '||')
            self.position += 2
        elif char == "&" and self.source[self.position + 1] == "&":
            self.next = Token('and', '&&')
            self.position += 2
        elif char == "\"":
            self.position += 1
            string = ""
            while self.source[self.position] != "\"":
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token('str', string)
        elif char.isalpha():
            iden = char
            self.position += 1
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                iden += self.source[self.position]
                self.position += 1
            if iden in palavras_reservadas:
                if iden == "true" or iden == "false":
                    self.next = Token('bool', iden)
                elif iden == "var":
                    self.next = Token('var', "")
                elif iden == "int" or iden == "string" or iden == "bool":
                    self.next = Token('type', iden)
                elif iden == "Println" or iden == "if" or iden == "else" or iden == "for" or iden == "Scan" or iden == "return" or iden == "func":
                    self.next = Token('reserved', iden)
            else:
                self.next = Token('iden', iden)
        else:
            raise Exception(f"Tokenizer - Token inválido {char}")

class Node:
    id = 0

    def __init__(self, value: int, children: list):
        self.id = Node.newId()
        self.value = value
        self.children = children

    def evaluate(self):
        pass

    def newId():
        Node.id += 1
        return Node.id
    
class Code():
    pilha = []
    var_table = {}

    def append(instr):
        Code.pilha.append(instr)

    def allocVar(nome):
        offset = -4 * (len(Code.var_table) + 1)
        Code.var_table[nome] = offset

    def getVarOffset(nome):
        return Code.var_table[nome]

    def dump():
        print("section .data")
        print('format_in: db "%d", 0')
        print('format_out: db "%d", 10, 0')
        print("scan_int: dd 0")
        print()
        print("section .text")
        print("global _start")
        print("extern printf")
        print("extern scanf")
        print()
        print("_start:")
        print("push ebp")
        print("mov ebp, esp")
        for instrucao in Code.pilha:
            print(instrucao)
        print("mov esp, ebp")
        print("pop ebp")
        print("mov eax, 1")
        print("mov ebx, 0")
        print("int 0x80")

class Block(Node):
    def evaluate(self, st):
        if self.value != "global":
            new_st = SymbolTable()
            new_st.parent = st
        else:
            new_st = st

        for child in self.children:
            resultado = child.evaluate(new_st)
            if child.value == "return":
                return resultado
            if resultado is not None:
                return resultado
    
    def generate(self, st):
        for child in self.children:
            child.generate(st)

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.parent = None

    def __create__(self, nome, tipo, valor):
        if valor is not None:
            self.table[nome] = (tipo, valor[1])
        else:
            self.table[nome] = (tipo, None)

    def __getitem__(self, nome):
        if nome not in self.table and self.parent is not None:
            return self.parent.__getitem__(nome)
        elif nome in self.table:
            return self.table[nome]
        else:
            raise Exception(f"SymbolTable - Variável {nome} não existe")

    def __setitem__(self, nome, valor):
        if nome not in self.table and self.parent is not None:
            self.parent.__setitem__(nome, valor)
            return
        elif nome in self.table:
            tipo = self.table[nome][0]
            if ((isinstance(valor[1], bool) and tipo == "bool") or (isinstance(valor[1], int) and tipo == "int") or (isinstance(valor[1], str) and tipo == "string")):
                self.table[nome] = (tipo, valor[1])
            else:
                raise Exception("Assignment - Tipo incompatível")
        else:
            raise Exception(f"SymbolTable - Variável {nome} não existe")

class Print(Node):
    def evaluate(self, st):
        val = self.children[0].evaluate(st)[1]
        if isinstance(val, bool):
            print(str(val).lower())
        else:
            print(val)

    def generate(self, st):
        self.children[0].generate(st)
        Code.append("push eax")
        Code.append("push format_out")
        Code.append("call printf")
        Code.append("add esp, 8")


class Iden(Node):
    def evaluate(self, st):
        return st.__getitem__(self.value)
    
    def generate(self, st):
        offset = Code.getVarOffset(self.value)
        Code.append(f"mov eax, [ebp{offset}]")

class IntVal(Node):
    def evaluate(self, st):
        return ("int", self.value)
    
    def generate(self, st):
        Code.append(f"mov eax, {self.value}")

class StrVal(Node):
    def evaluate(self, st):
        return ("str", self.value)

class BoolVal(Node):
    def evaluate(self, st):
        return ("bool", self.value)
    
    def generate(self, st):
        if self.value == "true":
            Code.append("mov eax, 1")
        else:
            Code.append("mov eax, 0")

class FuncDec(Node):
    def evaluate(self, st):
        st.table[self.children[0].value] = (self, self.value, True)

class FuncCall(Node):
    def evaluate(self, st):        
        func_dec, tipo_retorno, flag_eh_func = st.__getitem__(self.value)

        if not flag_eh_func:
            raise Exception(f"FuncCall - {self.value} não é uma função")
        
        args = func_dec.children[1:-1] #exclui o iden e o bloco
        if len(args) != len(self.children):
            raise Exception(f"FuncCall - Número de argumentos inválido para {self.value}")
        
        new_st = SymbolTable()
        new_st.parent = st


        for i in range(len(args)):
            nome_var_local = args[i].children
            tipo_var_local = args[i].value
            valor_var_local = self.children[i].evaluate(st)
            if valor_var_local[0] != tipo_var_local:
                raise Exception(f"FuncCall - Tipo de argumento inválido para {self.value}")
            new_st.__create__(nome_var_local, tipo_var_local, valor_var_local)

        resultado = func_dec.children[-1].evaluate(new_st)

        if tipo_retorno != "void":
            if resultado is None:
                raise Exception(f"FuncCall - Função {self.value} não retornou valor")
            if resultado[0] != tipo_retorno:
                raise Exception(f"FuncCall - Tipo de retorno incorreto para {self.value}")
            return resultado
        else:
            if resultado is not None:
                raise Exception(f"FuncCall - Função {self.value} não deveria retornar valor")
            return None

class Return(Node):
    def evaluate(self, st):
        return self.children[0].evaluate(st)

class VarDec(Node):
    def evaluate(self, st):
        tipo = self.value
        if self.children[0] in st.table:
            raise Exception("VarDec - Variável já existe")
        if len(self.children) == 2:
            if not (self.children[1].evaluate(st)[0] in tipo):
                raise Exception("VarDec - Tipo incompatível")
            st.__create__(self.children[0], tipo, self.children[1].evaluate(st))
        else:
            st.__create__(self.children[0], tipo, None)

    def generate(self, st):
        nome = self.children[0]
        Code.allocVar(nome)
        if len(self.children) == 2:
            self.children[1].generate(st)
            offset = Code.getVarOffset(nome)
            Code.append(f"mov [ebp{offset}], eax")

class BinOp(Node):
    def evaluate(self, st):
        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)
        if self.value == '+':
            if left[0] == "string" or right[0] == "string":
                left_val = str(left[1]).lower() if left[0] == "bool" else str(left[1])
                right_val = str(right[1]).lower() if right[0] == "bool" else str(right[1])
                return ("string", left_val + right_val)
            return ("int", left[1] + right[1])
        elif left[0] == right[0]:
            if self.value == '-':
                return ("int", left[1] - right[1])
            elif self.value == '*':
                return ("int", left[1] * right[1])
            elif self.value == '/':
                return ("int", left[1] // right[1])
            elif self.value == '==':
                return ("bool", left[1] == right[1])
            elif self.value == '<':
                return ("bool", left[1] < right[1])
            elif self.value == '>':
                return ("bool", left[1] > right[1])
            elif self.value == '&&':
                return ("bool", left[1] and right[1])
            elif self.value == '||':
                return ("bool", left[1] or right[1])
            else:
                raise Exception(f"BinOp - Operador inválido {self.value}")
        else:
            raise Exception("BinOp - Tipos incompatíveis")
        
    def generate(self, st):
        self.children[1].generate(st)
        Code.append("push eax")
        self.children[0].generate(st)
        Code.append("pop ecx")

        if self.value == '+':
            Code.append("add eax, ecx")
        elif self.value == '-':
            Code.append("sub eax, ecx")
        elif self.value == '*':
            Code.append("imul eax, ecx")
        elif self.value == '/':
            Code.append("mov edx, 0")
            Code.append("mov ebx, ecx")
            Code.append("div ebx")
        elif self.value == '==':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmove eax, ecx")
        elif self.value == '<':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmovl eax, ecx")
        elif self.value == '>':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmovg eax, ecx")
        elif self.value == '&&':
            Code.append("and eax, ecx")
        elif self.value == '||':
            Code.append("or eax, ecx")
        else:
            raise Exception(f"BinOp.generate - Operador inválido {self.value}")

class UnOp(Node):
    def evaluate(self, st):
        if self.children[0].evaluate(st)[0] == "int":
            if self.value == '+':
                return ("int", +self.children[0].evaluate(st)[1])
            elif self.value == '-':
                return ("int", -self.children[0].evaluate(st)[1])
            else:
                raise Exception("UnOp - Operador inválido")
        elif self.children[0].evaluate(st)[0] == "bool":
            if self.value == '!':
                return ("bool", not self.children[0].evaluate(st)[1])
            else:
                raise Exception("UnOp - Operador inválido")
        else:
            raise Exception("UnOp - Tipo inválido")
        
    def generate(self, st):
        self.children[0].generate(st)
        if self.value == '+':
            pass
        elif self.value == '-':
            Code.append("neg eax")
        elif self.value == '!':
            Code.append("cmp eax, 0")
            Code.append("mov ecx, 1")
            Code.append("mov eax, 0")
            Code.append("cmove eax, ecx")
        else:
            raise Exception("UnOp - Operador inválido")

class Assignment(Node):
    def evaluate(self, st):
        st.__setitem__(self.children[0], self.children[1].evaluate(st))

    def generate(self, st):
        self.children[1].generate(st)
        offset = Code.getVarOffset(self.children[0])
        Code.append(f"mov [ebp{offset}], eax")

class NoOp(Node):
    def evaluate(self, st):
        pass

    def generate(self, st):
        pass

class While(Node):
    def evaluate(self, st):
        while True:
            condicao = self.children[0].evaluate(st)
            if condicao[0] != "bool":
                raise Exception("While - Condição inválida")
            if not condicao[1]:
                break
            self.children[1].evaluate(st)

    def generate(self, st):
        label_start = f"loop_start_{self.id}"
        label_end = f"loop_end_{self.id}"

        Code.append(f"{label_start}:")
        self.children[0].generate(st)
        Code.append("cmp eax, 0")
        Code.append(f"je {label_end}")
        self.children[1].generate(st)
        Code.append(f"jmp {label_start}")
        Code.append(f"{label_end}:")

class If(Node):
    def evaluate(self, st):
        condicao = self.children[0].evaluate(st)
        if condicao[0] != "bool":
            raise Exception("If - Condição inválida")
        if condicao[1]:
            res = self.children[1].evaluate(st)
            return res
        elif len(self.children) == 3:
            res = self.children[2].evaluate(st)
            return res

    def generate(self, st):
        label_else = f"else_{self.id}"
        label_end = f"endif_{self.id}"

        self.children[0].generate(st)
        Code.append("cmp eax, 0")
        Code.append(f"je {label_else}")

        self.children[1].generate(st)

        if len(self.children) == 3:
            Code.append(f"jmp {label_end}")
            Code.append(f"{label_else}:")
            self.children[2].generate(st)
            Code.append(f"{label_end}:")
        else:
            Code.append(f"{label_else}:")

class Read(Node):
    def evaluate(self, st):
        return ("int", int(input()))

    def generate(self, st):
        Code.append("push scan_int")
        Code.append("push format_in")
        Code.append("call scanf")
        Code.append("add esp, 8")
        Code.append("mov eax, [scan_int]")

class Parser:
    def __init__(self):
        self.tokenizer = None

    def parseProgram(self):
        filhos = []

        while self.tokenizer.next.type != "EOF":
            if self.tokenizer.next.type == "reserved" and self.tokenizer.next.value == "func":
                filhos.append(self.parseFuncDec())
            elif self.tokenizer.next.type == "enter":
                self.tokenizer.selectNext()
            else:
                filhos.append(self.parseStatement())

        return Block("global", filhos)
            
    def parseFuncDec(self):
        if self.tokenizer.next.value == "func":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "iden":
                args = []
                no_iden = Iden(self.tokenizer.next.value, [])
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "open_par":
                    self.tokenizer.selectNext()
                    while self.tokenizer.next.type != "close_par":
                        if self.tokenizer.next.type == "iden":
                            nome_arg = self.tokenizer.next.value
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "type":
                                tipo = self.tokenizer.next.value
                                self.tokenizer.selectNext()
                                arg = VarDec(tipo, nome_arg)
                                args.append(arg)
                            else:
                                raise Exception("FuncDec - Deveria ter um type")
                        elif self.tokenizer.next.type == "comma":
                            self.tokenizer.selectNext()
                        else:
                            raise Exception("FuncDec - Esperava ',' ou ')' após argumento")
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "type":
                        return_type = self.tokenizer.next.value
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "open_chave":
                            block = self.parseBlock()
                            filhos = [no_iden]
                            for arg in args:
                                filhos.append(arg)
                            filhos.append(block)
                            return FuncDec(return_type, filhos)
                        else:
                            raise Exception("FuncDec - Deveria ter um open_chave")
                    elif self.tokenizer.next.type == "open_chave":
                        block = self.parseBlock()
                        filhos = [no_iden]
                        for arg in args:
                            filhos.append(arg)
                        filhos.append(block)
                        return FuncDec("void", filhos)
                    else:
                        raise Exception("FuncDec - Deveria ter um type ou open_chave")
                else:
                    raise Exception("FuncDec - Deveria ter um open_par")
            else:
                raise Exception("FuncDec - Deveria ter um iden")
        else:
            raise Exception("FuncDec - Deveria começar com func")

    def parseBlock(self):
        if self.tokenizer.next.type != "open_chave":
            raise Exception("Block - Deveria começar com open_chave")
        
        self.tokenizer.selectNext()

        if self.tokenizer.next.type == "close_chave":
            raise Exception("Block - Não pode ter close_chave depois de open_chave")

        children = []
        while self.tokenizer.next.type != "close_chave":
            if self.tokenizer.next.type == "enter":
                self.tokenizer.selectNext()
            else:
                children.append(self.parseStatement())

        self.tokenizer.selectNext()
        return Block(None, children)

    def parseStatement(self):
        if self.tokenizer.next.type == "iden":
            nome = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "assign":
                self.tokenizer.selectNext()
                return Assignment("=", [nome, self.parseBExpression()])
            elif self.tokenizer.next.type == "open_par":
                self.tokenizer.selectNext()
                args = []
                if self.tokenizer.next.type != "close_par":
                    while True:
                        args.append(self.parseBExpression())
                        if self.tokenizer.next.type == "comma":
                            self.tokenizer.selectNext()
                        elif self.tokenizer.next.type == "close_par":
                            break
                        else:
                            raise Exception("Statement - Esperava ',' ou ')' após argumento")
                self.tokenizer.selectNext()
                return FuncCall(nome, args)
            else:
                raise Exception("Statement - iden deveria ser seguido de um assign")
        elif self.tokenizer.next.value == "Println":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "open_par":
                self.tokenizer.selectNext()
                conteudo = [self.parseBExpression()]
                if self.tokenizer.next.type == "close_par":
                    self.tokenizer.selectNext()
                    return Print("print", conteudo)
                else:
                    raise Exception("Statement - Println deveria ter um close_par")
            else:
                raise Exception("Statement - Println deveria ter um open_par")
        elif self.tokenizer.next.type == "var":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "iden":
                nome = self.tokenizer.next.value
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "type":   
                    tipo = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "assign":
                        self.tokenizer.selectNext()
                        valor = self.parseBExpression()
                        return VarDec(tipo, [nome, valor]) 
                    return VarDec(tipo, [nome])
                else:
                    raise Exception("Statement - var deveria ter um type")
            else:
                raise Exception("Statement - var deveria ter um iden")
        elif self.tokenizer.next.value == "for":
            self.tokenizer.selectNext()
            condicao = self.parseBExpression()
            return While("while", [condicao, self.parseBlock()])
        elif self.tokenizer.next.value == "if":
            self.tokenizer.selectNext()
            condicao = self.parseBExpression()
            subArvoreIf = self.parseBlock()
            if self.tokenizer.next.value == "else":
                self.tokenizer.selectNext()
                return If("if", [condicao, subArvoreIf, self.parseBlock()])
            else:
                return If("if", [condicao, subArvoreIf])
        elif self.tokenizer.next.value == "return":
            self.tokenizer.selectNext()
            return Return("return", [self.parseBExpression()])
        elif self.tokenizer.next.type == "enter":
            self.tokenizer.selectNext()
            return NoOp(None, [])
        elif self.tokenizer.next.type == "open_chave":
            return self.parseBlock()
        else:
            raise Exception("Statement - Deveria começar com iden, print, enter, var, for ou if")
        
    def parseBExpression(self):
        subArvore = self.parseBTerm()
        while self.tokenizer.next.type == 'or':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            subArvore = BinOp(valor, [subArvore, self.parseBTerm()])
        return subArvore

    def parseBTerm(self):
        subArvore = self.parseRelExpression()
        while self.tokenizer.next.type == 'and':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            subArvore = BinOp(valor, [subArvore, self.parseRelExpression()])
        return subArvore
        
    def parseRelExpression(self):
        subArvore = self.parseExpression()
        while self.tokenizer.next.type == 'equals' or self.tokenizer.next.type == 'less' or self.tokenizer.next.type == 'greater':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            subArvore = BinOp(valor, [subArvore, self.parseExpression()])
        return subArvore
    
    def parseExpression(self):
        subArvore = self.parseTerm()
        while self.tokenizer.next.type == 'plus' or self.tokenizer.next.type == 'minus':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            subArvore = BinOp(valor, [subArvore, self.parseTerm()])
        return subArvore
    
    def parseTerm(self):    
        subArvore = self.parseFactor()
        while self.tokenizer.next.type == 'times' or self.tokenizer.next.type == 'divided':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            subArvore = BinOp(valor, [subArvore, self.parseFactor()])
        return subArvore
    
    def parseFactor(self):
        # no factor lidamos com os valores (numero, string, bool ou variavel) para usar na operacao
        if self.tokenizer.next.type == 'int':
            no = IntVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return no
        elif self.tokenizer.next.type == 'iden':
            nome = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'open_par':
                self.tokenizer.selectNext()
                args = []
                while self.tokenizer.next.type != "close_par":
                    args.append(self.parseBExpression())
                    if self.tokenizer.next.type == "comma":
                        self.tokenizer.selectNext()
                    elif self.tokenizer.next.type != "close_par":
                        raise Exception("parseFactor - Esperava ',' ou ')' após argumento")
                self.tokenizer.selectNext()
                return FuncCall(nome, args)
            else:
                return Iden(nome, [])
        elif self.tokenizer.next.type == 'str':
            no = StrVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return no
        elif self.tokenizer.next.type == 'bool':
            no = BoolVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return no
        elif self.tokenizer.next.type == 'plus' or self.tokenizer.next.type == 'minus' or self.tokenizer.next.type == 'not':
            valor = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return UnOp(valor, [self.parseFactor()])
        elif self.tokenizer.next.type == 'open_par':
            self.tokenizer.selectNext()
            result = self.parseBExpression()
            if self.tokenizer.next.type == 'close_par':
                self.tokenizer.selectNext()
                return result
            else:
                raise Exception("parseFactor - Depois de um open_par deveria vir um close_par")
        elif self.tokenizer.next.value == "Scan":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "open_par":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "close_par":
                    self.tokenizer.selectNext()
                    return Read("read", [])
                else:
                    raise Exception("parseFactor - O Scan() deveria ter um close_par")
            else:
                raise Exception("parseFactor - O Scan() deveria ter um open_par")
        else:
            raise Exception("parseFactor - Fator deveria começar com int, plus, minus, not, open_par, iden, str, bool ou Scan")

    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        return self.parseProgram()

def main(expressao):
    prepro = PrePro()
    expressao = prepro.filter(expressao)
    parser = Parser()
    ast = parser.run(expressao)
    global_st = SymbolTable()
    ast.evaluate(global_st)
    FuncCall("main", []).evaluate(global_st)
    # Code.dump()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
        with open(arquivo, 'r') as file:
            expressao = file.read()
        output = io.StringIO()
        # with contextlib.redirect_stdout(output):
        main(expressao)
        codigo_asm = output.getvalue()

        saida = arquivo.rsplit(".", 1)[0] + ".asm"
        with open(saida, 'w') as f:
            f.write(codigo_asm)
    else:
        raise Exception("Expressão vazia")