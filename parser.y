%{
#include <stdio.h>
#include <stdlib.h>
char* strdup(const char*);
int yylex(void);
void yyerror(const char *);
%}

%union {
    int num;
    char* id;
    char* txt;
}

%token ENCOMENDA TEXTO PLANEJAR PEDIDO RECEITA PORCOES MEDIDA INGREDIENTE FORNO RESFRIAR DECORAR TEMPO_TOTAL
%token <num> NUMERO QUANTIDADE TEMPERATURA DURACAO
%token <id> IDENTIFICADOR
%token <txt> STRING

%start programa

%%

programa:
      ENCOMENDA STRING ':' bloco_pedidos PLANEJAR
    | ENCOMENDA ':' bloco_pedidos PLANEJAR ;

bloco_pedidos: pedido bloco_pedidos | /* vazio */ ;

pedido: PEDIDO ':' RECEITA IDENTIFICADOR ':' itens_receita itens_pedido ;

itens_receita: item_receita itens_receita | /* vazio */ ;

item_receita: PORCOES NUMERO
            | MEDIDA IDENTIFICADOR
            | INGREDIENTE IDENTIFICADOR QUANTIDADE
            | FORNO TEMPERATURA DURACAO
            | RESFRIAR DURACAO
            | DECORAR STRING ;

itens_pedido: item_pedido itens_pedido | /* vazio */ ;

item_pedido: PORCOES NUMERO
           | TEMPO_TOTAL NUMERO ;

%%

int main() {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
}