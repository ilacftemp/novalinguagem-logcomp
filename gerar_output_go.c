#include <stdio.h>
#include "estrutura.h"

void gerar_output_go(Encomenda* e) {
    FILE* f = fopen("output.go", "w");
    if (!f) {
        perror("Erro ao criar arquivo output.go");
        return;
    }

    fprintf(f, "{\n");

    fprintf(f, "Println(\"ENCOMENDA\")\n");
    fprintf(f, "Println(\"=============================================\")\n");

    for (int i = 0; i < e->num_pedidos; i++) {
        Pedido* p = &e->pedidos[i];
        Receita* r = &p->receita;

        float fator = (float)p->porcoes_pedido / (float)r->porcoes_receita;
        fprintf(f, "Println(\"Pedido %d: %s\")\n", i + 1, r->nome_receita);
        fprintf(f, "Println(\"---------------------------------------------\")\n");
        fprintf(f, "Println(\"Receita adaptada para %d porções (%.1f %s a receita base)\")\n", p->porcoes_pedido, fator, (fator == 1.0 ? "vez" : "vezes"));
        fprintf(f, "Println(\"Ingredientes:\")\n");

        for (int j = 0; j < r->num_ingredientes; j++) {
            Ingrediente* ing = &r->ingredientes[j];
            fprintf(f, "Println(\"- %s: %d %s\")\n", ing->nome, (int)(ing->quantidade * fator), ing->unidade);
        }

        fprintf(f, "Println(\"Plano de execução:\")\n");
        if (r->forno_duracao > 0)
            fprintf(f, "Println(\"1. Assar a %d°C por %d minutos.\")\n", r->forno_temp, r->forno_duracao);
        if (r->resfriar > 0)
            fprintf(f, "Println(\"2. Resfriar por %d minutos.\")\n", r->resfriar);
        if (r->decoracao)
            fprintf(f, "Println(\"3. Decorar com %s.\")\n", r->decoracao);

        fprintf(f, "Println(\"Tempo estimado:\")\n");
        if (r->forno_duracao > 0)
            fprintf(f, "Println(\"- Forno: %d minutos\")\n", r->forno_duracao);
        if (r->resfriar > 0)
            fprintf(f, "Println(\"- Resfriamento: %d minutos\")\n", r->resfriar);
        if (r->decoracao)
            fprintf(f, "Println(\"- Decoração: 20 minutos\")\n");

        int total = r->forno_duracao + r->resfriar + (r->decoracao ? 20 : 0);
        fprintf(f, "Println(\"Tempo total previsto: %d minutos\")\n", total);
        fprintf(f, "Println(\"Tempo disponível para produção: %d minutos\")\n", p->tempo_total);
        fprintf(f, "Println(\"Status: %s\")\n", (total <= p->tempo_total) ? "Dentro do limite de tempo" : "Fora do limite de tempo");
        fprintf(f, "Println(\"=============================================\")\n");
    }

    fprintf(f, "}");
    fclose(f);
}
