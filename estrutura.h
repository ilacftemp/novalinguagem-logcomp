#ifndef ESTRUTURA_H
#define ESTRUTURA_H

#define MAX_INGREDIENTES 20
#define MAX_PEDIDOS 10

typedef struct {
    char* nome;
    int quantidade;
    char* unidade;
} Ingrediente;

typedef struct {
    char* nome_receita;
    int porcoes_receita;
    Ingrediente ingredientes[MAX_INGREDIENTES];
    int num_ingredientes;
    int forno_temp;
    int forno_duracao;
    int resfriar;
    char* decoracao;
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
