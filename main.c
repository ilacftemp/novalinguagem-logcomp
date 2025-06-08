#include <stdio.h>
#include <stdlib.h>
#include "estrutura.h"

extern int yyparse();
extern FILE* yyin;

void gerar_output_go(Encomenda* encomenda);

int main(int argc, char** argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }

    if (yyparse() == 0) {
        gerar_output_go(&encomenda);
        liberar_memoria();
    } else {
        fprintf(stderr, "Erro ao interpretar o arquivo.\n");
        return 1;
    }

    return 0;
}
