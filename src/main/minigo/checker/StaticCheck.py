"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"


class Symbol:
    def __init__(self, name, mtype, value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"


class StaticChecker(BaseVisitor, Utils):
    
    def __init__(self, ast):
        self.ast = ast
        self.global_env = [
            Symbol("getInt", MType([], IntType())),
            Symbol("putInt",MType([IntType()], VoidType())),
            Symbol("putIntLn",MType([IntType()], VoidType())),
            Symbol("getFloat", MType([], FloatType())),
            Symbol("putFloat",MType([FloatType()], VoidType())),
            Symbol("putFloatLn",MType([FloatType()], VoidType())),
            Symbol("getBool", MType([], BoolType())),
            Symbol("putBool",MType([BoolType()], VoidType())),
            Symbol("putBoolLn",MType([BoolType()], VoidType())),
            Symbol("getString", MType([], StringType())),
            Symbol("putString",MType([StringType()], VoidType())),
            Symbol("putStringLn",MType([StringType()], VoidType())),
            Symbol("putLn", MType([], VoidType())),
        ]
 
    
    def check(self):
        return self.visit(self.ast, self.global_env)

    
    def visitProgram(self, ast, env):
        # decl : List[Decl]
        env = [env]
        for decl in ast.decl:
            self.visit(decl, env)
        return None
    
    
    def visitVarDecl(self, ast, env):
        # varName : str
        # varType : Type # None if there is no type
        # varInit : Expr # None if there is no initialization
        if ast.varName in (symbol.name for scope in env for symbol in scope):
            raise Redeclared(Variable(), ast.varName)
        env[0].append(Symbol(ast.varName, ast., ast.varType))
        return None

    
    def visitConstDecl(self, ast, env):
        
        return None
    
    
    def visitFuncDecl(self, ast, env):
        return None
    
    
    def visitMethodDecl(self, ast, env):
        return None
    

    def visitPrototype(self, ast, env):
        return None
    
    
    def visitIntType(self, ast, env):
        return None
    
    
    def visitFloatType(self, ast, env):
        return None
    
    
    def visitBoolType(self, ast, env):
        return None
    
    
    def visitStringType(self, ast, env):
        return None
    
    
    def visitVoidType(self, ast, env):
        return None
    
    
    def visitArrayType(self, ast, env):
        return None
    
    
    def visitStructType(self, ast, env):
        return None
    

    def visitInterfaceType(self, ast, env):
        return None
    
    
    def visitBlock(self, ast, env):
        return None
    
 
    def visitAssign(self, ast, env):
        return None
    
   
    def visitIf(self, ast, env):
        return None
    
    
    def visitForBasic(self, ast, env):
        return None
    
 
    def visitForStep(self, ast, env):
        return None
    

    def visitForEach(self, ast, env):
        return None
    

    def visitContinue(self, ast, env):
        return None
    
    
    def visitBreak(self, ast, env):
        return None
    
    
    def visitReturn(self, ast, env):
        return None
    

    def visitBinaryOp(self, ast, env):
        return None
    
    
    def visitUnaryOp(self, ast, env):
        return None
    
    
    def visitFuncCall(self, ast, env):
        return None
    

    def visitMethCall(self, ast, env):
        return None
    
    
    def visitId(self, ast, env):
        return None
    
    
    def visitArrayCell(self, ast, env):
        return None
    
    
    def visitFieldAccess(self, ast, env):
        return None
    
    
    def visitIntLiteral(self, ast, env):
        return IntType()
    
    
    def visitFloatLiteral(self, ast, env):
        return FloatType()
    
    
    def visitBooleanLiteral(self, ast, env):
        return BoolType()
    
    
    def visitStringLiteral(self, ast, env):
        return StringType()
    

    def visitArrayLiteral(self, ast, env):
        return None
    

    def visitStructLiteral(self, ast, env):
        return None
    

    def visitNilLiteral(self, ast, env):
        return NilLiteral()
    
    
    # def visitProgram(self,ast, c):
    #     reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.decl, c)
    #     return c


    # def visitVarDecl(self, ast, env):
    #     res = self.lookup(ast.varName, c, lambda x: x.name)
    #     if not res is None:
    #         raise Redeclared(Variable(), ast.varName) 
    #     if ast.varInit:
    #         initType = self.visit(ast.varInit, c)
    #         if ast.varType is None:
    #             ast.varType = initType
    #         if not type(ast.varType) is type(initType):
    #             raise TypeMismatch(ast)
    #     return Symbol(ast.varName, ast.varType,None)
        

    # def visitFuncDecl(self, ast, env):
    #     res = self.lookup(ast.name, c, lambda x: x.name)
    #     if not res is None:
    #         raise Redeclared(Function(), ast.name)
    #     return Symbol(ast.name, MType([], ast.retType))


    # def visitIntLiteral(self, ast, env):
    #     return IntType()

    
    # def visitFloatLiteral(self, ast, env):
    #     return FloatType()

    
    # def visitId(self,ast,c):
    #     res = self.lookup(ast.name, c, lambda x: x.name)
    #     if res is None:
    #         raise Undeclared(Identifier(), ast.name)
    #     return res.mtype
