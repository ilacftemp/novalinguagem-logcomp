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
        int total = 0;
        int tempo_forno = 0, tempo_resfriar = 0, tempo_decorar = 0;

        for (int k = 0; k < r->num_etapas; k++) {
            EtapaExecucao* etapa = &r->etapas[k];
            switch (etapa->tipo) {
                case ETAPA_FORNO:
                    fprintf(f, "Println(\"%d. Assar a %d°C por %d minutos.\")\n", k+1, etapa->temperatura, etapa->duracao);
                    tempo_forno += etapa->duracao;
                    total += etapa->duracao;
                    break;
                case ETAPA_RESFRIAR:
                    fprintf(f, "Println(\"%d. Resfriar por %d minutos.\")\n", k+1, etapa->duracao);
                    tempo_resfriar += etapa->duracao;
                    total += etapa->duracao;
                    break;
                case ETAPA_DECORAR:
                    fprintf(f, "Println(\"%d. Decorar com %s.\")\n", k+1, etapa->decoracao);
                    tempo_decorar += etapa->duracao;
                    total += etapa->duracao;
                    break;
            }
        }

        fprintf(f, "Println(\"Tempo estimado:\")\n");
        if (tempo_forno > 0)
            fprintf(f, "Println(\"- Forno: %d minutos\")\n", tempo_forno);
        if (tempo_resfriar > 0)
            fprintf(f, "Println(\"- Resfriamento: %d minutos\")\n", tempo_resfriar);
        if (tempo_decorar > 0)
            fprintf(f, "Println(\"- Decoração: %d minutos\")\n", tempo_decorar);

        fprintf(f, "Println(\"Tempo total previsto: %d minutos\")\n", total);
        fprintf(f, "Println(\"Tempo disponível para produção: %d minutos\")\n", p->tempo_total);
        fprintf(f, "Println(\"Status: %s\")\n", (total <= p->tempo_total) ? "Dentro do limite de tempo" : "Fora do limite de tempo");

        fprintf(f, "Println(\"=============================================\")\n");
    }

    fprintf(f, "}");
    fclose(f);
}
