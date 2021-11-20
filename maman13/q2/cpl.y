%{
%}
%token NUM
%token ID
%token BREAK
%token CASE
%token DEFAULT
%token ELSE
%token FLOAT
%token IF
%token INPUT
%token INT
%token OUTPUT
%token SWITCH
%token WHILE
%token RELOP
%token ADDOP
%token MULOP
%token OR
%token AND
%token NOT
%token CAST
%%
program : declarations stmt_block
declarations:declarations declaration
 | /*epsilon*/
declaration : idlist ':' type ';'

type : INT
 | FLOAT
idlist : idlist ',' ID
 | ID
stmt : assignment_stmt
| input_stmt
| output_stmt
| if_stmt
| while_stmt
| switch_stmt
| break_stmt
| stmt_block
assignment_stmt : ID '=' expression ';'
input_stmt : INPUT '(' ID ')' ';'
output_stmt : OUTPUT '(' expression ')' ';'
if_stmt : IF ')' boolexpr '(' stmt ELSE stmt
while_stmt : WHILE ')' boolexpr '(' stmt
switch_stmt : SWITCH '(' expression ')' '{' caselist
 DEFAULT ':' stmtlist '}'
caselist : caselist CASE NUM ':' stmtlist
 | /*epsilon*/
break_stmt : BREAK ';'
stmt_block : '{' stmtlist '}'
stmtlist: stmtlist stmt
 | /*epsilon*/
boolexpr : boolexpr OR boolterm
 | boolterm
boolterm : boolterm AND boolfactor
 | boolfactor
boolfactor : NOT '(' boolexpr ')'
| expression RELOP expression
expression : expression ADDOP term
| term
term : term MULOP factor
 | factor
factor : '(' expression ')'
 | CAST '(' expression ')'
 | ID
 | NUM
