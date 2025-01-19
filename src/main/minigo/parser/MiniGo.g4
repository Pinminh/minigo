grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
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
        return super().emit();
}

options{
	language=Python3;
}

program: EOF;

// whitespace characters

LF: '\n' -> skip;

WS : [ \t\f\r]+ -> skip;

// program comments
// ambiguity: nested comments are necessarily closed?

CMT: (SL_CMT | ML_CMT) -> skip;

SL_CMT: SL_CMT_INIT .*? SL_CMT_END;
fragment SL_CMT_INIT: '//';
fragment SL_CMT_END: '\n' | EOF;

ML_CMT: ML_CMT_INIT (ML_CMT | .)*?  ML_CMT_END -> skip;
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
TRUE: 'true';
FALSE: 'false';

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

ASGN: '=';
ADDEQ: '+=';
SUBEQ: '-=';
MULEQ: '*=';
DIVEQ: '/=';
MODEQ: '%=';

// dot operator

DOT: '.';

// identifiers

ID: [a-zA-Z_] [a-zA-Z0-9_]*;

ERROR_CHAR: .;
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;