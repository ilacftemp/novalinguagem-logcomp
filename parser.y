%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "estrutura.h"

extern Encomenda encomenda;
int pedido_atual = -1;

void liberar_memoria();
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
    : PEDIDO ':' RECEITA IDENTIFICADOR ':' itens_receita itens_pedido {
        pedido_atual = encomenda.num_pedidos++;
        Pedido* p = &encomenda.pedidos[pedido_atual];
        Receita* r = &p->receita;

        r->nome_receita = strdup($4);
        r->num_ingredientes = 0;
        r->forno_duracao = 0;
        r->forno_temp = 0;
        r->resfriar = 0;
        r->decoracao = NULL;
    }
    ;

itens_receita
    : /* vazio */
    | itens_receita item_receita
    ;

item_receita
    : PORCOES NUMERO {
        if (pedido_atual >= 0)
            encomenda.pedidos[pedido_atual].receita.porcoes_receita = $2;
    }
    | INGREDIENTE IDENTIFICADOR QUANTIDADE {
        if (pedido_atual >= 0) {
            Receita* r = &encomenda.pedidos[pedido_atual].receita;
            Ingrediente* ing = &r->ingredientes[r->num_ingredientes++];
            ing->nome = strdup($2);
            ing->quantidade = $3;
            ing->unidade = "g";
        }
    }
    | INGREDIENTE IDENTIFICADOR NUMERO {
        if (pedido_atual >= 0) {
            Receita* r = &encomenda.pedidos[pedido_atual].receita;
            Ingrediente* ing = &r->ingredientes[r->num_ingredientes++];
            ing->nome = strdup($2);
            ing->quantidade = $3;
            ing->unidade = "unidades";
        }
    }
    | FORNO TEMPERATURA DURACAO {
        if (pedido_atual >= 0) {
            Receita* r = &encomenda.pedidos[pedido_atual].receita;
            r->forno_temp = $2;
            r->forno_duracao = $3;
        }
    }
    | RESFRIAR DURACAO {
        if (pedido_atual >= 0)
            encomenda.pedidos[pedido_atual].receita.resfriar = $2;
    }
    | DECORAR STRING {
        if (pedido_atual >= 0)
            encomenda.pedidos[pedido_atual].receita.decoracao = strdup($2);
    }
    ;

itens_pedido
    : /* vazio */
    | itens_pedido item_pedido
    ;

item_pedido
    : PORCOES NUMERO {
        if (pedido_atual >= 0)
            encomenda.pedidos[pedido_atual].porcoes_pedido = $2;
    }
    | TEMPO_TOTAL DURACAO {
        if (pedido_atual >= 0)
            encomenda.pedidos[pedido_atual].tempo_total = $2;
    }
    ;

%%

int yyerror(const char* s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
    return 1;
}

void liberar_memoria() {
    for (int i = 0; i < encomenda.num_pedidos; i++) {
        Receita* r = &encomenda.pedidos[i].receita;

        if (r->nome_receita) free(r->nome_receita);
        if (r->decoracao) free(r->decoracao);

        for (int j = 0; j < r->num_ingredientes; j++) {
            if (r->ingredientes[j].nome) free(r->ingredientes[j].nome);
        }
    }
}
