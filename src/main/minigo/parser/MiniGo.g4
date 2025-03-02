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

STRLIT: DQ (~[\\"] | ESCAPED)* DQ;
fragment DQ: '"';
fragment ESCAPED: '\\n' | '\\t' | '\\r' | '\\"' | '\\\\';

// boolean literal

BOOLLIT: TRUE | FALSE;

// identifiers

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// whitespace characters

WS : [ \t\f]+ -> skip;
NL: [\r\n]+ -> skip;

ERROR_CHAR: .;
ILLEGAL_ESCAPE: .;
UNCLOSE_STRING: .;

/*
    parser rules
 */

// type classification

primtyp: INT | FLOAT | BOOLEAN | STRING;
comptyp: STRUCT | INTERFACE;

arrvaltyp: primtyp | STRUCT;

arrtyp: dimlist arrvaltyp;
dimlist: dim dimlist | dim;
dim: LS (INTLIT | ID) RS;   // missing ID constant check

bltintyp: primtyp | comptyp | arrtyp;

returntyp: bltintyp;    // return type can be interface?

// literal classification

primlit: INTLIT | FLOATLIT | BOOLLIT | STRLIT;
complit: arrlit | structlit;
bltinlit: primlit | complit;

// terminators

stmtterm: SC?;   // temporary terminator

// parameter list declaration

paramlistdecl: LP nullparamlist RP;
nullparamlist: paramlist | ;

paramlist: sharedtyplist CM paramlist | sharedtyplist;
sharedtyplist: params bltintyp; // parameter type includes interface?
params: ID CM params | ID;

// argument list declaration

arglistdecl: LP nullarglist RP;
nullarglist: arglist | ;

arglist: expr CM arglist | expr;

// array declaration

arrdecl: VAR ID arrtyp;

// array literal (array initialization)

arrlit: arrtyp elemlistdecl;

elemlistdecl: LB nullelemlist RB;

nullelemlist: elemlist | ;
elemlist: recurlist | litlist;

recurlist: elemlistdecl CM recurlist | elemlistdecl;
litlist: elemlit CM litlist | elemlit;

elemlit: primlit | structlit;

// struct declaration

structdecl: TYPE ID STRUCT structfielddecl SC?;

structfielddecl: LB nullfieldlist RB;

nullfieldlist: fieldlist | ;
fieldlist: field fieldlist | field;
field: ID bltintyp stmtterm;

// struct literal (struct initialization)

structlit: ID fieldinitdecl;

fieldinitdecl: LB nullstructinitlist RB;
nullstructinitlist: structinitlist | ;
structinitlist: fieldval CM structinitlist | fieldval;

fieldval: ID CL expr;

// struct function declaration
// missing

// interface declaration

interfacedecl: TYPE ID INTERFACE methodlistdecl;

methodlistdecl: LB nullmethodlist RB;
nullmethodlist: methodlist | ;
methodlist: method methodlist | method;

method: ID paramlistdecl returntyp? stmtterm;    // return type includes interface?

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
mcallop: DOT fcallop;
fcallop: ID arglistdecl;
structop: DOT ID;

operand: bltinlit | ID;

evalexpr: 'evalexpr';   // incomplete, and is it necessary?

// statement declaration

stmt: semistmt stmtterm | optsemistmt stmtterm | nosemistmt stmtterm;

semistmt: vardecl | constdecl | asgnstmt | breakstmt | continuestmt | callstmt | returnstmt;
optsemistmt: structdecl | interfacedecl;
nosemistmt: ifstmt | forstmt | funcdecl | methoddecl;

// asignment statement

asgnstmt: varexpr asgnop expr;
varexpr: varexpr bracketop | varexpr structop | ID;

vararr: ID arridxlist;
arridxlist: bracketop arridxlist | bracketop;

varstruct: ID fieldacclist;
fieldacclist: structop fieldacclist | structop;

asgnop: ASGN | ADDEQ | SUBEQ | MULEQ | DIVEQ | MODEQ;

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
standfor: FOR asgnstmt SC expr SC asgnstmt block;
rangefor: FOR ID CM ID ASGN RANGE (ID | arrlit) block;

// break-continue statement

breakstmt: BREAK;
continuestmt: CONTINUE;

// call statement

callstmt: fcallop | ID mcallop;

// return statement

returnstmt: RETURN expr?;

// program

program: nullstmtlist EOF;