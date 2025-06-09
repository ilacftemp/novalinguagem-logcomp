%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
%}

digit      [0-9]
letter     [A-Za-z_]
id         {letter}({letter}|{digit})*
number     {digit}+

%%

"encomenda"        return ENCOMENDA;
"texto"            return TEXTO;
"planejar"         return PLANEJAR;
"pedido"           return PEDIDO;
":"                return ':';
"receita"          return RECEITA;
"porcoes"          return PORCOES;
"medida"           return MEDIDA;
"ingrediente"      return INGREDIENTE;
"forno"            return FORNO;
"resfriar"         return RESFRIAR;
"decorar"          return DECORAR;
"porcoes_total"    return PORCOES_TOTAL;
"tempo_total"      return TEMPO_TOTAL;

{number}"g"        { yylval.num = atoi(yytext); return QUANTIDADE; }
{number}"C"        { yylval.num = atoi(yytext); return TEMPERATURA; }
{number}"min"      { yylval.num = atoi(yytext); return DURACAO; }
{number}           { yylval.num = atoi(yytext); return NUMERO; }

{id}               { yylval.id  = strdup(yytext); return IDENTIFICADOR; }
\"([^\n\"])*\"     {
    char* raw = strndup(yytext + 1, yyleng - 2);
    yylval.txt = raw;
    return STRING;
}

[ \t\r\n]+         /* ignora espaços em branco */
.                  { return yytext[0]; }

%%
