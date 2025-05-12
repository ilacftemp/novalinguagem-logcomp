%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
%}

digit     [0-9]
letter    [a-zA-Z]
id        {letter}({letter}|{digit})*
number    {digit}+

%%

"encomenda"      { return ENCOMENDA; }
"texto"          { return TEXTO; }
"planejar"       { return PLANEJAR; }
"pedido:"        { return PEDIDO; }
":"              { return ':'; }
"receita"        { return RECEITA; }
"porções"        { return PORCOES; }
"medida"         { return MEDIDA; }
"ingrediente"    { return INGREDIENTE; }
"forno"          { return FORNO; }
"resfriar"       { return RESFRIAR; }
"decorar"        { return DECORAR; }
"tempo_total"    { return TEMPO_TOTAL; }

{number}"g"      { yylval.num = atoi(yytext); return QUANTIDADE; }
{number}"C"      { yylval.num = atoi(yytext); return TEMPERATURA; }
{number}"min"    { yylval.num = atoi(yytext); return DURACAO; }
{number}         { yylval.num = atoi(yytext); return NUMERO; }
{id}             { yylval.id = strdup(yytext); return IDENTIFICADOR; }
\"[^"]*\"        { yylval.txt = strdup(yytext); return STRING; }
":"              { return ':'; }

[ \t\n\r]+       ;
.                { return yytext[0]; }

%%

int yywrap() { return 1; }