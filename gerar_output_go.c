#include <stdio.h>
#include "estrutura.h"

void gerar_output_go(Encomenda* e) {
    FILE* f = fopen("output.go", "w");
    if (!f) {
        perror("Erro ao criar arquivo output.go");
        return;
    }

    fprintf(f, "package main\n\nimport \"fmt\"\n\nfunc main() {\n");
    fprintf(f, "fmt.Println(\"ENCOMENDA\")\n");
    fprintf(f, "fmt.Println(\"\\n=============================================\")\n");

    for (int i = 0; i < e->num_pedidos; i++) {
        Pedido* p = &e->pedidos[i];
        Receita* r = &p->receita;

        float fator = (float)p->porcoes_pedido / (float)r->porcoes_receita;
        fprintf(f, "fmt.Println(\"Pedido %d: %s\")\n", i + 1, r->nome_receita);
        fprintf(f, "fmt.Println(\"---------------------------------------------\")\n");
        fprintf(f, "fmt.Println(\"Receita adaptada para %d porções:\")\n", p->porcoes_pedido);
        fprintf(f, "fmt.Println(\"\\nIngredientes:\")\n");

        for (int j = 0; j < r->num_ingredientes; j++) {
            Ingrediente* ing = &r->ingredientes[j];
            fprintf(f, "fmt.Println(\"- %s: %dg\")\n", ing->nome, (int)(ing->quantidade * fator));
        }

        fprintf(f, "fmt.Println(\"\\nPlano de execução:\")\n");
        if (r->forno_duracao > 0)
            fprintf(f, "fmt.Println(\"1. Assar a %d°C por %d minutos.\")\n", r->forno_temp, r->forno_duracao);
        if (r->resfriar > 0)
            fprintf(f, "fmt.Println(\"2. Resfriar por %d minutos.\")\n", r->resfriar);
        if (r->decoracao)
            fprintf(f, "fmt.Println(\"3. Decorar com %s.\")\n", r->decoracao);

        fprintf(f, "fmt.Println(\"\\nTempo estimado:\")\n");
        if (r->forno_duracao > 0)
            fprintf(f, "fmt.Println(\"- Forno: %d minutos\")\n", r->forno_duracao);
        if (r->resfriar > 0)
            fprintf(f, "fmt.Println(\"- Resfriamento: %d minutos\")\n", r->resfriar);
        if (r->decoracao)
            fprintf(f, "fmt.Println(\"- Decoração: 20 minutos\")\n");

        int total = r->forno_duracao + r->resfriar + 20;
        fprintf(f, "fmt.Println(\"\\nTempo total previsto: %d minutos\")\n", total);
        fprintf(f, "fmt.Println(\"Limite do pedido: %d minutos\")\n", p->tempo_total);
        fprintf(f, "fmt.Println(\"Status: %s\")\n", (total <= p->tempo_total) ? "Dentro do limite" : "Fora do limite");
        fprintf(f, "fmt.Println(\"\\n=============================================\")\n");
    }

    fprintf(f, "}\n");
    fclose(f);
}
