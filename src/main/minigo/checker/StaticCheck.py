"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
# from Utils import Utils
from StaticError import *
from functools import reduce


class Utils:
    @staticmethod
    def find_duplicate(get_info, lst):
        seen = set()
        for item in lst:
            if get_info(item) in seen:
                return item
            seen.add(get_info(item))
        return None


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return "MType([" + ",".join(str(x) for x in self.partype) + "]," + str(self.rettype) + ")"


class VType:
    def __init__(self, typ):
        self.type = typ
    
    def __str__(self):
        return f"VType({str(self.type)})"


class CType:
    def __init__(self, typ):
        self.type = typ
    
    def __str__(self):
        return f"CType({str(self.type)})"


class SType:
    def __init__(self, elements, methods):
        self.elements = elements
        self.methods = methods
    
    def __str__(self):
        return f"SType({','.join(self.elements)},{','.join(self.methods)})"


class IType:
    def __init__(self, prototypes):
        self.prototypes = prototypes
    
    def __str__(self):
        return f"IType({','.join(str(proto) for proto in self.prototypes)})"


class Symbol:
    def __init__(self, name, typ, value = None):
        self.name = name
        self.symtype = typ
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.symtype) + str(self.value) + ")"


class StaticChecker(BaseVisitor, Utils):
    
    def __init__(self, ast):        
        self.ast = ast
        self.global_env = []
 
    
    def check(self):
        collector = GlobalNameCollector(self.ast)
        collector.collect()
        self.global_env = collector.global_env
        for sym in self.global_env:
            print(sym)
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
        if len(env) <= 1: return None
        if ast.varName in (symbol.name for symbol in env[0]):
            raise Redeclared(Variable(), ast.varName)
        env[0].append(Symbol(ast.varName, VType(ast.varType)))
        return None

    
    def visitConstDecl(self, ast, env):
        # conName : str
        # conType : Type # None if there is no type 
        # iniExpr : Expr
        if len(env) <= 1: return None
        if ast.conName in (symbol.name for symbol in env[0]):
            raise Redeclared(Constant(), ast.conName)
        env[0].append(Symbol(ast.conName, VType(ast.conType, const=True)))
        return None
    
    
    def visitFuncDecl(self, ast, env):
        # name: str
        # params: List[ParamDecl]
        # retType: Type # VoidType if there is no return type
        # body: Block
        if ast.name in (symbol.name for symbol in env[0]):
            raise Redeclared(Function(), ast.name)
        params = reduce(
            lambda acc, param: [self.visit(param, env)] + acc,
            ast.params,
            [],
        )
        # Start of parameter scope
        env = [params] + env
        # Start of body scope
        env = [[]] + env
        self.visit(ast.body, env)
        return None
    
    
    def visitParamDecl(self, ast, env):
        return Symbol(ast.parName, VType(ast.parType))

    
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
        # name: str
        # elements:List[Tuple[str,Type]]
        # methods:List[MethodDecl]
        return None
    

    def visitInterfaceType(self, ast, env):
        return None
    
    
    def visitBlock(self, ast, env):
        # member:List[BlockMember]
        for mem in ast.member:
            self.visit(mem, env)
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


class GlobalNameCollector(BaseVisitor, Utils):
    
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
 
    
    def collect(self):
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
        if ast.varName in (symbol.name for symbol in env[0]):
            raise Redeclared(Variable(), ast.varName)
        env[0].append(Symbol(ast.varName, VType(None)))
        return None

    
    def visitConstDecl(self, ast, env):
        # conName : str
        # conType : Type # None if there is no type 
        # iniExpr : Expr
        if ast.conName in (symbol.name for symbol in env[0]):
            raise Redeclared(Constant(), ast.conName)
        env[0].append(Symbol(ast.conName, CType(None)))
        return None
    
    
    def visitFuncDecl(self, ast, env):
        # name: str
        # params: List[ParamDecl]
        # retType: Type # VoidType if there is no return type
        # body: Block
        if ast.name in (symbol.name for symbol in env[0]):
            raise Redeclared(Function(), ast.name)
        env[0].append(Symbol(
            ast.name,
            MType(None, None),
        ))
        return None

    
    def visitMethodDecl(self, ast, env):
        # receiver: str
        # recType: Type 
        # fun: FuncDecl
        # Cannot resolve receiver type yet in this global name collector
        return None
    

    def visitPrototype(self, ast, env):
        # name: str
        # params:List[Type]
        # retType: Type # VoidType if there is no return type
        return Symbol(ast.name, MType(None, None))
    
    
    def visitStructType(self, ast, env):
        # name: str
        # elements:List[Tuple[str,Type]]
        # methods:List[MethodDecl]
        if ast.name in (symbol.name for symbol in env[0]):
            raise Redeclared(Type(), ast.name)
        elemsyms = list(map(lambda tup: Symbol(tup[0], VType(None)), ast.elements))
        duplicated = Utils.find_duplicate(lambda sym: sym.name, elemsyms)
        if duplicated:
            raise Redeclared(Field(), duplicated.name)
        env[0].append(Symbol(ast.name, SType(elemsyms, methods=[])))
        return None
    

    def visitInterfaceType(self, ast, env):
        # name: str
        # methods:List[Prototype]
        if ast.name in (symbol.name for symbol in env[0]):
            raise Redeclared(Type(), ast.name)
        protos = list(map(lambda proto: self.visit(proto, env), ast.methods))
        duplicated = Utils.find_duplicate(lambda proto: proto.name, protos)
        if duplicated:
            raise Redeclared(Prototype(), duplicated.name)
        env[0].append(Symbol(ast.name, IType(protos)))
        return None
