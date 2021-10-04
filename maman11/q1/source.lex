%{
%}


%%
[0-9][0-9]+	 {printf("%s", yytext);}
1 {printf("I");}
2 {printf("II");}
3 {printf("III");}
4 {printf("IV");}
5 {printf("V");}
6 {printf("VI");}
7 {printf("VII");}
8 {printf("VIII");}
9 {printf("IX");}
.	 {printf("%s", yytext);}
%%

int yywrap(){}
int main(int argc, char *argv[]){
FILE *fp;
// todo handle also standard
fp = fopen(argv[1],"r");
yyin = fp;

yylex();

return 0;
}

