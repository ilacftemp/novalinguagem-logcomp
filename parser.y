%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "estrutura.h"

extern Encomenda encomenda;
int pedido_atual = -1;

void liberar_memoria();
int yylex(void);
int yyerror(const char* s);
%}

%union {
    int    num;
    char  *id;
    char  *txt;
}

%token ENCOMENDA TEXTO PLANEJAR PEDIDO RECEITA PORCOES MEDIDA INGREDIENTE FORNO RESFRIAR DECORAR PORCOES_TOTAL TEMPO_TOTAL
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
    : PEDIDO ':' RECEITA IDENTIFICADOR ':' {
        pedido_atual = encomenda.num_pedidos++;
        Pedido* p = &encomenda.pedidos[pedido_atual];
        Receita* r = &p->receita;

        strncpy(r->nome_receita, $<id>4, sizeof(r->nome_receita));
        r->num_ingredientes = 0;
        r->num_etapas = 0;

        p->porcoes_pedido = 0;
        p->tempo_total = 0;

    } itens_receita itens_pedido


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
            int i = r->num_etapas++;
            r->etapas[i].tipo = ETAPA_FORNO;
            r->etapas[i].temperatura = $2;
            r->etapas[i].duracao = $3;
        }
    }
    | RESFRIAR DURACAO {
        if (pedido_atual >= 0) {
            Receita* r = &encomenda.pedidos[pedido_atual].receita;
            int i = r->num_etapas++;
            r->etapas[i].tipo = ETAPA_RESFRIAR;
            r->etapas[i].duracao = $2;
        }
    }
    | DECORAR STRING {
        if (pedido_atual >= 0) {
            Receita* r = &encomenda.pedidos[pedido_atual].receita;
            int i = r->num_etapas++;
            r->etapas[i].tipo = ETAPA_DECORAR;
            r->etapas[i].duracao = 20; // fixo, como no gerar_output
            strncpy(r->etapas[i].decoracao, $2, sizeof(r->etapas[i].decoracao));
        }
    }
    ;

itens_pedido
    : /* vazio */
    | itens_pedido item_pedido
    ;

item_pedido
    : PORCOES_TOTAL NUMERO {
        if (pedido_atual >= 0) {
            encomenda.pedidos[pedido_atual].porcoes_pedido = $2;
        }
    }
    | TEMPO_TOTAL DURACAO {
        if (pedido_atual >= 0) {
            encomenda.pedidos[pedido_atual].tempo_total = $2;
        }
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

        for (int j = 0; j < r->num_ingredientes; j++) {
            if (r->ingredientes[j].nome) free(r->ingredientes[j].nome);
        }
    }
}
