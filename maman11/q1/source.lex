%{
int lineCounter=1;
int startLine();
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
\n {lineCounter++; printf("\n"); startLine();}
.	 {printf("%s", yytext);}
%%

int yywrap(){}
int main(int argc, char *argv[]){
if (argc>1){
FILE *fp;
fp = fopen(argv[1],"r");
yyin = fp;
startLine();
yylex();
}
return 0;
}
int startLine(){
	if(lineCounter%2==1){
	   printf("%d.\t", lineCounter);
	} else {
	  printf("\t");
	}
	return 0;
}
