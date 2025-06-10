# APS - Definição de Linguagem de Programação

---

## Objetivo

Criação de uma linguagem voltada para confeiteiros, com o objetivo de organizar pedidos de forma metódica e gerar um plano de execução para as encomendas recebidas. A partir das receitas associadas a cada pedido, a linguagem permite:

- resumir as quantidades de ingredientes necessárias;
- listar os passos de produção, como tempo de forno, resfriamento e decoração;
- ajustar automaticamente as quantidades de ingredientes com base na proporção entre porções que uma receita rende e porções solicitadas;
- estimar o tempo total de produção de cada pedido;
- comparar o tempo total de produção do pedido com o tempo disponível (informado no input).

---

## Tecnologias utilizadas

- C (main, estrutura, geração de output)
- Flex e Bison (análise léxica e sintática)
- Python (compilador de saída Go para NASM)

---

## Como usar

Após clonar o repositório, é necessário abrir um terminal (recomendado o uso de Ubuntu ou terminal WSL) que permita o uso comando `make`. Em seguida, rode o programa da seguinte forma:

```./encomenda < arquivo_input.txt```

Substitua `arquivo_input.txt` pelo nome do arquivo desejado. Exemplo:

```./encomenda < testes/teste1_pedido_unico.txt```

Essa execução gerará o arquivo na linguagem `go`, que pode ser compilado através do uso do `compilador_para_go.py`, desenvolvido ao longo do semestre na disciplina Lógica da Computação. Para compilar o arquivo, utilize o seguinte comando no terminal:

```python compilador_para_go.py output.go```

Em que o arquivo `output.go` é o gerado anteriormente pelo executável `encomenda`. A saída será um arquivo `.asm` que pode ser montado e executado.

LEMBRETE: Use a versão do `python` compatível com o seu sistema para a compilação.

---

## Testes

A pasta de testes contém alguns exemplos de arquivos que podem ser submetidos. Como fica evidente, o sistema permite na entrada uma encomenda com até 10 pedidos que, por sua vez, podem conter até 20 ingredientes e 10 etapas para produção.

A saída envolve os resumos das informações relevantes para o plano de execução, como tempo total, ingredientes e quantidades necessários, entre outros.

### Exemplo completo de execução

Entrada (teste 1):

```
encomenda:
    pedido:
        receita bolo:
            porcoes 4
            ingrediente farinha 200g
            ingrediente ovos 2
            forno 180C 30min
            resfriar 10min
            decorar "açúcar de confeiteiro"

        porcoes_total 4
        tempo_total 60min

planejar
```

Arquivo `.go` intermediário:
```
{
Println("ENCOMENDA")
Println("=============================================")
Println("Pedido 1: bolo")
Println("---------------------------------------------")
Println("Receita adaptada para 4 porções (1.0 vez a receita base)")
Println("Ingredientes:")
Println("- farinha: 200 g")
Println("- ovos: 2 unidades")
Println("Plano de execução:")
Println("1. Assar a 180°C por 30 minutos.")
Println("2. Resfriar por 10 minutos.")
Println("3. Decorar com açúcar de confeiteiro.")
Println("Tempo estimado:")
Println("- Forno: 30 minutos")
Println("- Resfriamento: 10 minutos")
Println("- Decoração: 20 minutos")
Println("Tempo total previsto: 60 minutos")
Println("Tempo disponível para produção: 60 minutos")
Println("Status: Dentro do limite de tempo")
Println("=============================================")
}
```

Saída:
```
section .data
format_in: db "%d", 0
format_out: db "%d", 10, 0
scan_int: dd 0
msg_str_1: db "ENCOMENDA", 10, 0
msg_str_4: db "=============================================", 10, 0
msg_str_7: db "Pedido 1: bolo", 10, 0
msg_str_10: db "---------------------------------------------", 10, 0
msg_str_13: db "Receita adaptada para 4 porções (1.0 vez a receita base)", 10, 0
msg_str_16: db "Ingredientes:", 10, 0
msg_str_19: db "- farinha: 200 g", 10, 0
msg_str_22: db "- ovos: 2 unidades", 10, 0
msg_str_25: db "Plano de execução:", 10, 0
msg_str_28: db "1. Assar a 180°C por 30 minutos.", 10, 0
msg_str_31: db "2. Resfriar por 10 minutos.", 10, 0
msg_str_34: db "3. Decorar com açúcar de confeiteiro.", 10, 0
msg_str_37: db "Tempo estimado:", 10, 0
msg_str_40: db "- Forno: 30 minutos", 10, 0
msg_str_43: db "- Resfriamento: 10 minutos", 10, 0
msg_str_46: db "- Decoração: 20 minutos", 10, 0
msg_str_49: db "Tempo total previsto: 60 minutos", 10, 0
msg_str_52: db "Tempo disponível para produção: 60 minutos", 10, 0
msg_str_55: db "Status: Dentro do limite de tempo", 10, 0
msg_str_58: db "=============================================", 10, 0

section .text
global _start
extern printf
extern scanf

_start:
push ebp
mov ebp, esp
mov eax, msg_str_1
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_4
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_7
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_10
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_13
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_16
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_19
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_22
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_25
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_28
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_31
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_34
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_37
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_40
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_43
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_46
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_49
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_52
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_55
push eax
push format_out
call printf
add esp, 8
mov eax, msg_str_58
push eax
push format_out
call printf
add esp, 8
mov esp, ebp
pop ebp
mov eax, 1
mov ebx, 0
int 0x80
```