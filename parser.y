%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
int yylex(void);
%}

%union {
    int    num;
    char  *id;
    char  *txt;
}

%token ENCOMENDA TEXTO PLANEJAR PEDIDO RECEITA PORCOES MEDIDA INGREDIENTE FORNO RESFRIAR DECORAR TEMPO_TOTAL
%token <num> NUMERO QUANTIDADE TEMPERATURA DURACAO
%token <id>  IDENTIFICADOR
%token <txt> STRING

%start programa

%%

programa
    : ENCOMENDA ':' bloco_pedidos PLANEJAR
    | ENCOMENDA STRING ':' bloco_pedidos PLANEJAR
    ;

bloco_pedidos
    : /* vazio */
    | bloco_pedidos pedido
    ;

pedido
    : PEDIDO ':' RECEITA IDENTIFICADOR ':' itens_receita itens_pedido
    ;

itens_receita
    : /* vazio */
    | itens_receita item_receita
    ;

item_receita
    : PORCOES        NUMERO
    | MEDIDA         IDENTIFICADOR
    | INGREDIENTE    IDENTIFICADOR QUANTIDADE
    | INGREDIENTE    IDENTIFICADOR NUMERO
    | FORNO          TEMPERATURA DURACAO
    | RESFRIAR       DURACAO
    | DECORAR        STRING
    ;

itens_pedido
    : /* vazio */
    | itens_pedido item_pedido
    ;

item_pedido
    : PORCOES        NUMERO
    | TEMPO_TOTAL    DURACAO
    ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
    exit(EXIT_FAILURE);
}
