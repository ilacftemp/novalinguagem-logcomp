#ifndef ESTRUTURA_H
#define ESTRUTURA_H

#define MAX_INGREDIENTES 20
#define MAX_PEDIDOS 10
#define MAX_ETAPAS 10

typedef struct {
    char* nome;
    int quantidade;
    char* unidade;
} Ingrediente;

typedef enum { ETAPA_FORNO, ETAPA_RESFRIAR, ETAPA_DECORAR } TipoEtapa;

typedef struct {
    TipoEtapa tipo;
    int duracao;
    int temperatura;
    char decoracao[100];
} EtapaExecucao;


typedef struct {
    char nome_receita[100];
    int porcoes_receita;
    Ingrediente ingredientes[MAX_INGREDIENTES];
    int num_ingredientes;
    EtapaExecucao etapas[MAX_ETAPAS];
    int num_etapas;
} Receita;

typedef struct {
    Receita receita;
    int porcoes_pedido;
    int tempo_total;
} Pedido;

typedef struct {
    Pedido pedidos[MAX_PEDIDOS];
    int num_pedidos;
} Encomenda;

extern Encomenda encomenda;

#endif
