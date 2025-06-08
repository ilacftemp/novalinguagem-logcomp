all:
	bison -d parser.y
	flex lexer.l
	gcc -o encomenda main.c parser.tab.c lex.yy.c estrutura.c gerar_output_go.c -lfl
