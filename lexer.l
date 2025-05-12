%{
#include "parser.tab.h"
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
"receita"        { return RECEITA; }
"porções"        { return PORCOES; }
"medida"         { return MEDIDA; }
"ingrediente"    { return INGREDIENTE; }
"forno"          { return FORNO; }
"resfriar"       { return RESFRIAR; }
"decorar"        { return DECORAR; }

{number}"g"      { yylval.num = atoi(yytext); return QUANTIDADE; }
{number}"C"      { yylval.num = atoi(yytext); return TEMPERATURA; }
{number}"min"    { yylval.num = atoi(yytext); return DURACAO; }
{number}         { yylval.num = atoi(yytext); return NUMERO; }
{id}             { yylval.id = strdup(yytext); return IDENTIFICADOR; }
\"[^"]*\"        { yylval.txt = strdup(yytext); return STRING; }

[ \t\n\r]+       ;
.                { return yytext[0]; }
%%

int yywrap() { return 1; }