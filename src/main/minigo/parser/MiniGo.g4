// 2212059 - Nguyen Hong Minh

grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
    last_tk = None
    rep_list = []

def emit(self):
    self.rep_list = [
        self.ID,
        self.INTLIT,
        self.FLOATLIT,
        self.BOOLLIT,
        self.STRLIT,
        self.INT,
        self.FLOAT,
        self.BOOLEAN,
        self.STRING,
        self.RETURN,
        self.CONTINUE,
        self.BREAK,
        self.RP,
        self.RB,
        self.RS
    ];
    t = super().emit();
    tk = t.type;
    self.last_tk = t;

    if tk == self.UNCLOSE_STRING:
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return t;
}

options{
	language=Python3;
}


/*
    lexer rules
 */

// program comments
// ambiguity: nested comments are necessarily closed?

CMT: (SL_CMT | ML_CMT) -> skip;

fragment SL_CMT: SL_CMT_INIT .*? SL_CMT_END;
fragment SL_CMT_INIT: '//';
fragment SL_CMT_END: '\n' | EOF;

fragment ML_CMT: ML_CMT_INIT (ML_CMT | .)*?  ML_CMT_END;
fragment ML_CMT_INIT: '/*';
fragment ML_CMT_END: '*/';

// keywords

IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';
NIL: 'nil';
fragment TRUE: 'true';
fragment FALSE: 'false';

// arithmetic operators

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

// relational operators

EQ: '==';
NEQ: '!=';
LT: '<';
LTE: '<=';
GT: '>';
GTE: '>=';

// logical operators

AND: '&&';
OR: '||';
NOT: '!';

// assignment operators

ASGN: ':=';
ADDEQ: '+=';
SUBEQ: '-=';
MULEQ: '*=';
DIVEQ: '/=';
MODEQ: '%=';
INIT: '=';

// dot operator

DOT: '.';

// separators

LP: '(';    // parenthesis
RP: ')';
LB: '{';    // brace
RB: '}';
LS: '[';    // squared bracket
RS: ']';
CM: ',';    // comma
SC: ';';    // semicolon
CL: ':';    // colon

// integer literal

INTLIT: DECINT | BININT | OCTINT | HEXINT;
fragment DECINT: [1-9] [0-9]* | [0]+;
fragment BININT: '0' [bB] [01]+;
fragment OCTINT: '0' [oO] [0-7]+;
fragment HEXINT: '0' [xX] [0-9a-fA-F]+;

// floating-point literal

FLOATLIT: FLOATINT DOT FLOATFRAC? FLOATEXP?;
fragment FLOATINT: [0-9]+;
fragment FLOATFRAC: [0-9]+;
fragment FLOATEXP: [eE] [+-]? [0-9]+;

// string literal

STRLIT: DQ CHARS* DQ;
fragment DQ: '"';
fragment CHARS: ~[\\"] | ESCAPED;
fragment ESCAPED: '\\n' | '\\t' | '\\r' | '\\"' | '\\\\';
fragment ILL_ESC: '\\' ~[ntr"\\] | '\\';

// boolean literal

BOOLLIT: TRUE | FALSE;

// identifiers

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// whitespace characters

WS : [ \t\f]+ -> skip;
NL: [\r\n]+ -> skip;

// errors

ILLEGAL_ESCAPE: DQ CHARS* ILL_ESC {
    raise IllegalEscape(self.text)
};
UNCLOSE_STRING: DQ CHARS* {
    raise UncloseString(self.text)
};
ERROR_CHAR: . {
    raise ErrorToken(self.text)
};

/*
    parser rules
 */

// type classification

primtyp: INT | FLOAT | BOOLEAN | STRING;

arrvaltyp: primtyp | ID;

arrtyp: dimlist arrvaltyp;
dimlist: dim dimlist | dim;
dim: LS (INTLIT | ID) RS;   // missing ID constant check

bltintyp: primtyp | arrtyp;
availtyp: bltintyp | ID;

returntyp: availtyp;    // return type can be interface?

// literal classification

primlit: INTLIT | FLOATLIT | BOOLLIT | STRLIT | NIL;
complit: arrlit | structlit;
bltinlit: primlit | complit;

// terminators

stmtterm: SC?;   // temporary terminator

// parameter list declaration

paramlistdecl: LP nullparamlist RP;
nullparamlist: paramlist | ;
paramlist: sharedparamlist CM paramlist | sharedparamlist;

sharedparamlist: params availtyp; // parameter type includes interface?
params: ID CM params | ID;

paramtyplistdecl: LP nullparamtyplist RP;
nullparamtyplist: paramtyplist | ;
paramtyplist: sharedtyplist CM paramtyplist | sharedtyplist;

sharedtyplist: paramtyps availtyp; // parameter type includes interface?
paramtyps: ID CM paramtyps | ID;

// argument list declaration

arglistdecl: LP nullarglist RP;
nullarglist: arglist | ;

arglist: expr CM arglist | expr;

// array declaration

// arrdecl: VAR ID arrtyp;

// array literal (array initialization)

arrlit: arrtyp elemlistdecl;

elemlistdecl: LB elemlist RB;
elemlist: elemlit CM elemlist | elemlit;
elemlit: expr | elemlistdecl;

// struct declaration

structdecl: TYPE ID STRUCT LB fieldlist RB stmtterm;
fieldlist: field fieldlist | field;
field: ID availtyp stmtterm;

// struct literal (struct initialization)

structlit: ID fieldinitdecl;

fieldinitdecl: LB nullstructinitlist RB;
nullstructinitlist: structinitlist | ;
structinitlist: fieldval CM structinitlist | fieldval;

fieldval: ID CL expr;

// struct function declaration
// missing

// interface declaration

interfacedecl: TYPE ID INTERFACE LB methodlist RB stmtterm;
methodlist: method methodlist | method;

method: ID paramtyplistdecl returntyp? stmtterm;    // return type includes interface?

// variable declaration

vardecl: typdecl | untypdecl;

typdecl: VAR ID vartyp varinit?;
untypdecl: VAR ID varinit;

vartyp: bltintyp | ID;
varinit: INIT expr;

// constant declaration

constdecl: CONST ID varinit;   // such expr need evaluable check

// function declaration

funcdecl: FUNC ID paramlistdecl returntyp? block;

// method declaration

methoddecl: FUNC receiver ID paramlistdecl returntyp? block;

// function-method related-declaration

receiver: LP ID ID RP;

block: LB nullstmtlist RB;
nullstmtlist: stmtlist | ;
stmtlist: stmt stmtlist | stmt;

// expression
// note: the name of operator excluded from the expression is included in
//       the name of parse rule, e.g, addexpr is the parse rule that excluded
//       + operator from its expression

expr: expr OR orexpr | orexpr;
orexpr: orexpr AND andexpr | andexpr;
andexpr: andexpr (EQ | NEQ | LT | LTE | GT | GTE) relexpr | relexpr;
relexpr: relexpr (ADD | SUB) addexpr | addexpr;
addexpr: addexpr (MUL | DIV | MOD) mulexpr | mulexpr;
mulexpr: SUB mulexpr | NOT mulexpr | notexpr;
notexpr: notexpr bracketop | notexpr mcallop | notexpr structop | dotexpr;
dotexpr: fcallop | callexpr;
callexpr: LP expr RP | parenexpr;
parenexpr: operand;

bracketop: LS expr RS;
mcallop: DOT ID arglistdecl;
fcallop: ID arglistdecl;
structop: DOT ID;

operand: bltinlit | ID;

// evalexpr: 'evalexpr';   // incomplete, and is it necessary?

// statement declaration

stmt: semistmt stmtterm | optsemistmt stmtterm | nosemistmt stmtterm | returnstmt SC;

semistmt: vardecl | constdecl | asgnstmt | breakstmt | continuestmt | callstmt;
optsemistmt: structdecl | interfacedecl;
nosemistmt: ifstmt | forstmt | funcdecl | methoddecl;

// asignment statement

asgnstmt: varexpr (ASGN | ADDEQ | SUBEQ | MULEQ | DIVEQ | MODEQ) expr;
varexpr: varexpr bracketop | varexpr structop | ID;

// vararr: ID arridxlist;
// arridxlist: bracketop arridxlist | bracketop;

// varstruct: ID fieldacclist;
// fieldacclist: structop fieldacclist | structop;

// if statement

ifstmt: IF logicexpr block elseportion;

logicexpr: LP expr RP;

elseportion: elseiflist? elseonly?;
elseonly: ELSE block;

elseiflist: elseifstmt elseiflist | elseifstmt;
elseifstmt: ELSE IF logicexpr block;

// for statement

forstmt: basicfor | standfor | rangefor;

basicfor: FOR expr block;
standfor: FOR forinit SC forcond SC forupdt block;
rangefor: FOR ID CM ID ASGN RANGE expr block;

forinit: forasgn | forvardecl;
forasgn: ID ASGN expr;
forvardecl: VAR ID vartyp? INIT expr;

forcond: expr;
forupdt: asgnstmt;

// break-continue statement

breakstmt: BREAK;
continuestmt: CONTINUE;

// call statement

callstmt: fcallop | varcall mcallop;
varcall: varcall bracketop | varcall structop | varcall mcallop | ID;

// return statement

returnstmt: RETURN expr?;

// program

program: stmtlist EOF;