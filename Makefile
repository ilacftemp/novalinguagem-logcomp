all:
	bison -d parser.y
	flex lexer.l
	gcc -o encomenda parser.tab.c lex.yy.c -lfl