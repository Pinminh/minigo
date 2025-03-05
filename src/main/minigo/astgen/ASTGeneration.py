from pathlib import Path
from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

def write_test_output(data):
    path = Path("C:/Users/ASUS/Desktop/test.txt").absolute()
    with open(path, "w+") as file:
        file.write(data)

class ASTGeneration(MiniGoVisitor):  

    # Visit a parse tree produced by MiniGoParser#primtyp.
    def visitPrimtyp(self, ctx:MiniGoParser.PrimtypContext):
        # primtyp: INT | FLOAT | BOOLEAN | STRING
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.BOOLEAN():
            return BoolType()
        return StringType()


    # Visit a parse tree produced by MiniGoParser#arrvaltyp.
    def visitArrvaltyp(self, ctx:MiniGoParser.ArrvaltypContext):
        # arrvaltyp: primtyp | ID
        # Id(name:str)
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#arrtyp.
    def visitArrtyp(self, ctx:MiniGoParser.ArrtypContext):
        # arrtyp: dimlist arrvaltyp
        # ArrayType(dimens:List[Expr], eleType:Type)
        dimlist = self.visit(ctx.dimlist())
        eletype = self.visit(ctx.arrvaltyp())
        return dimlist, eletype


    # Visit a parse tree produced by MiniGoParser#dimlist.
    def visitDimlist(self, ctx:MiniGoParser.DimlistContext):
        # dimlist: dim dimlist | dim
        if ctx.dimlist():
            dim = self.visit(ctx.dim())
            dimlist = self.visit(ctx.dimlist())
            return [dim] + dimlist
        return [self.visit(ctx.dim())]


    # Visit a parse tree produced by MiniGoParser#dim.
    def visitDim(self, ctx:MiniGoParser.DimContext):
        # dim: LS (INTLIT | ID) RS
        # IntLiteral(value:int)
        # Id(name:str)
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#bltintyp.
    def visitBltintyp(self, ctx:MiniGoParser.BltintypContext):
        # bltintyp: primtyp | arrtyp
        # ArrayType(dimens:List[Expr], eleType:Type)
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        dimens, etype = self.visit(ctx.arrtyp())
        return ArrayType(dimens, etype)


    # Visit a parse tree produced by MiniGoParser#returntyp.
    def visitReturntyp(self, ctx:MiniGoParser.ReturntypContext):
        # returntyp: availtyp
        return self.visit(ctx.availtyp())
    
    
    # Visit a parse tree produced by MiniGoParser#availtyp.
    def visitAvailtyp(self, ctx:MiniGoParser.AvailtypContext):
        # availtyp: bltintyp | ID
        if ctx.bltintyp():
            return self.visit(ctx.bltintyp())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#primlit.
    def visitPrimlit(self, ctx:MiniGoParser.PrimlitContext):
        # primlit: INTLIT | FLOATLIT | BOOLLIT | STRLIT | NIL
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.BOOLLIT():
            return BooleanLiteral(ctx.BOOLLIT().getText() == 'true')
        if ctx.STRLIT():
            return StringLiteral(ctx.STRLIT().getText()[1:-1])
        return NilLiteral()


    # Visit a parse tree produced by MiniGoParser#complit.
    def visitComplit(self, ctx:MiniGoParser.ComplitContext):
        # complit: arrlit | structlit
        if ctx.arrlit():
            return self.visit(ctx.arrlit())
        return self.visit(ctx.structlit())


    # Visit a parse tree produced by MiniGoParser#bltinlit.
    def visitBltinlit(self, ctx:MiniGoParser.BltinlitContext):
        # bltinlit: primlit | complit
        if ctx.primlit():
            return self.visit(ctx.primlit())
        return self.visit(ctx.complit())


    # Visit a parse tree produced by MiniGoParser#paramtyplistdecl.
    def visitParamtyplistdecl(self, ctx:MiniGoParser.ParamtyplistdeclContext):
        # paramtyplistdecl: LP nullparamtyplist RP
        return self.visit(ctx.nullparamtyplist())


    # Visit a parse tree produced by MiniGoParser#nullparamtyplist.
    def visitNullparamtyplist(self, ctx:MiniGoParser.NullparamtyplistContext):
        # nullparamtyplist: paramtyplist | 
        return self.visit(ctx.paramtyplist()) if ctx.paramtyplist() else []


    # Visit a parse tree produced by MiniGoParser#paramtyplist.
    def visitParamtyplist(self, ctx:MiniGoParser.ParamtyplistContext):
        # paramtyplist: sharedtyplist CM paramtyplist | sharedtyplist
        if ctx.CM():
            sharedtyp = self.visit(ctx.sharedtyplist())
            typlist = self.visit(ctx.paramtyplist())
            return sharedtyp + typlist
        return self.visit(ctx.sharedtyplist())
    

    # Visit a parse tree produced by MiniGoParser#sharedtyplist.
    def visitSharedtyplist(self, ctx:MiniGoParser.SharedtyplistContext):
        # sharedtyplist: paramtyps availtyp
        shared_num = self.visit(ctx.paramtyps())
        paramtyp = self.visit(ctx.availtyp())
        return shared_num * [paramtyp]


    # Visit a parse tree produced by MiniGoParser#paramtyps.
    def visitParamtyps(self, ctx:MiniGoParser.ParamtypsContext):
        # paramtyps: ID CM paramtyps | ID
        if ctx.CM():
            return 1 + self.visit(ctx.paramtyps())
        return 1


    # Visit a parse tree produced by MiniGoParser#arglistdecl.
    def visitArglistdecl(self, ctx:MiniGoParser.ArglistdeclContext):
        # arglistdecl: LP nullarglist RP
        return self.visit(ctx.nullarglist())


    # Visit a parse tree produced by MiniGoParser#nullarglist.
    def visitNullarglist(self, ctx:MiniGoParser.NullarglistContext):
        # nullarglist: arglist | 
        return self.visit(ctx.arglist()) if ctx.arglist() else []


    # Visit a parse tree produced by MiniGoParser#arglist.
    def visitArglist(self, ctx:MiniGoParser.ArglistContext):
        # arglist: expr CM arglist | expr
        if ctx.CM():
            expr = self.visit(ctx.expr())
            arglist = self.visit(ctx.arglist())
            return [expr] + arglist
        return [self.visit(ctx.expr())]


    # Visit a parse tree produced by MiniGoParser#arrlit.
    def visitArrlit(self, ctx:MiniGoParser.ArrlitContext):
        # arrlit: arrtyp elemlistdecl
        dimlist, eletype = self.visit(ctx.arrtyp())
        values = self.visit(ctx.elemlistdecl())
        return ArrayLiteral(dimlist, eletype, values)


    # Visit a parse tree produced by MiniGoParser#elemlistdecl.
    def visitElemlistdecl(self, ctx:MiniGoParser.ElemlistdeclContext):
        # elemlistdecl: LB elemlist RB
        return self.visit(ctx.elemlist())


    # Visit a parse tree produced by MiniGoParser#elemlist.
    def visitElemlist(self, ctx:MiniGoParser.ElemlistContext):
        # elemlist: recurlist | litlist
        if ctx.recurlist():
            return self.visit(ctx.recurlist())
        return self.visit(ctx.litlist())


    # Visit a parse tree produced by MiniGoParser#recurlist.
    def visitRecurlist(self, ctx:MiniGoParser.RecurlistContext):
        # recurlist: elemlistdecl CM recurlist | elemlistdecl
        if ctx.CM():
            elemlist = self.visit(ctx.elemlistdecl())
            recurlist = self.visit(ctx.recurlist())
            return [elemlist] + recurlist
        return [self.visit(ctx.elemlistdecl())]
            


    # Visit a parse tree produced by MiniGoParser#litlist.
    def visitLitlist(self, ctx:MiniGoParser.LitlistContext):
        # litlist: elemlit CM litlist | elemlit
        if ctx.CM():
            lit = self.visit(ctx.elemlit())
            list = self.visit(ctx.litlist())
            return [lit] + list
        return [self.visit(ctx.elemlit())]


    # Visit a parse tree produced by MiniGoParser#elemlit.
    def visitElemlit(self, ctx:MiniGoParser.ElemlitContext):
        # elemlit: expr
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#structdecl.
    def visitStructdecl(self, ctx:MiniGoParser.StructdeclContext):
        # structdecl: TYPE ID STRUCT LB fieldlist RB stmtterm
        # StructType(name:str, elements:List[Tuple(str, Type)], List[MethodDecl])
        name = ctx.ID().getText()
        elements = self.visit(ctx.fieldlist())
        methods = []
        return StructType(name, elements, methods)


    # Visit a parse tree produced by MiniGoParser#fieldlist.
    def visitFieldlist(self, ctx:MiniGoParser.FieldlistContext):
        # fieldlist: field fieldlist | field
        if ctx.fieldlist():
            field = self.visit(ctx.field())
            flist = self.visit(ctx.fieldlist())
            return [field] + flist
        return [self.visit(ctx.field())]


    # Visit a parse tree produced by MiniGoParser#field.
    def visitField(self, ctx:MiniGoParser.FieldContext):
        # field: ID bltintyp stmtterm
        attr_name = ctx.ID().getText()
        attr_type = self.visit(ctx.bltintyp())
        return (attr_name, attr_type)


    # Visit a parse tree produced by MiniGoParser#structlit.
    def visitStructlit(self, ctx:MiniGoParser.StructlitContext):
        # structlit: ID fieldinitdecl
        name = ctx.ID().getText()
        elements = self.visit(ctx.fieldinitdecl())
        return StructLiteral(name, elements)


    # Visit a parse tree produced by MiniGoParser#fieldinitdecl.
    def visitFieldinitdecl(self, ctx:MiniGoParser.FieldinitdeclContext):
        # fieldinitdecl: LB nullstructinitlist RB
        return self.visit(ctx.nullstructinitlist())


    # Visit a parse tree produced by MiniGoParser#nullstructinitlist.
    def visitNullstructinitlist(self, ctx:MiniGoParser.NullstructinitlistContext):
        # nullstructinitlist: structinitlist | 
        return self.visit(ctx.structinitlist()) if ctx.structinitlist() else []


    # Visit a parse tree produced by MiniGoParser#structinitlist.
    def visitStructinitlist(self, ctx:MiniGoParser.StructinitlistContext):
        # structinitlist: fieldval CM structinitlist | fieldval
        if ctx.CM():
            field = self.visit(ctx.fieldval())
            field_list = self.visit(ctx.structinitlist())
            return [field] + field_list
        return [self.visit(ctx.fieldval())]


    # Visit a parse tree produced by MiniGoParser#fieldval.
    def visitFieldval(self, ctx:MiniGoParser.FieldvalContext):
        # fieldval: ID CL expr
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        return (name, value)


    # Visit a parse tree produced by MiniGoParser#interfacedecl.
    def visitInterfacedecl(self, ctx:MiniGoParser.InterfacedeclContext):
        # interfacedecl: TYPE ID INTERFACE LB methodlist RB stmtterm
        name = ctx.ID().getText()
        methods = self.visit(ctx.methodlist())
        return InterfaceType(name, methods)


    # Visit a parse tree produced by MiniGoParser#methodlist.
    def visitMethodlist(self, ctx:MiniGoParser.MethodlistContext):
        # methodlist: method methodlist | method
        if ctx.methodlist():
            method = self.visit(ctx.method())
            methodlist = self.visit(ctx.methodlist())
            return [method] + methodlist
        return [self.visit(ctx.method())]


    # Visit a parse tree produced by MiniGoParser#method.
    def visitMethod(self, ctx:MiniGoParser.MethodContext):
        # method: ID paramtyplistdecl returntyp? stmtterm
        name = ctx.ID().getText()
        params = self.visit(ctx.paramtyplistdecl())
        rettyp = self.visit(ctx.returntyp()) if ctx.returntyp() else VoidType()
        return Prototype(name, params, rettyp)


    # Visit a parse tree produced by MiniGoParser#vardecl.
    def visitVardecl(self, ctx:MiniGoParser.VardeclContext):
        # vardecl: typdecl | untypdecl
        if ctx.typdecl():
            return self.visit(ctx.typdecl())
        return self.visit(ctx.untypdecl())


    # Visit a parse tree produced by MiniGoParser#typdecl.
    def visitTypdecl(self, ctx:MiniGoParser.TypdeclContext):
        # typdecl: VAR ID vartyp varinit?
        # VarDecl(varName:str, varType:Type, varInit:Expr)
        varname = ctx.ID().getText()
        vartype = self.visit(ctx.vartyp())
        varinit = self.visit(ctx.varinit()) if ctx.varinit() else None
        return VarDecl(varname, vartype, varinit)


    # Visit a parse tree produced by MiniGoParser#untypdecl.
    def visitUntypdecl(self, ctx:MiniGoParser.UntypdeclContext):
        # untypdecl: VAR ID varinit
        # VarDecl(varname:str, VarType:Type, varInit:Expr)
        varname = ctx.ID().getText()
        vartype = None
        varinit = self.visit(ctx.varinit())
        return VarDecl(varname, vartype, varinit)


    # Visit a parse tree produced by MiniGoParser#vartyp.
    def visitVartyp(self, ctx:MiniGoParser.VartypContext):
        # vartyp: bltintyp | ID
        # Id(name:str)
        if ctx.bltintyp():
            return self.visit(ctx.bltintyp())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#varinit.
    def visitVarinit(self, ctx:MiniGoParser.VarinitContext):
        # varinit: INIT expr
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#constdecl.
    def visitConstdecl(self, ctx:MiniGoParser.ConstdeclContext):
        # constdecl: CONST ID varinit
        const_name = ctx.ID().getText()
        const_type = None
        const_init = self.visit(ctx.varinit())
        return ConstDecl(const_name, const_type, const_init)


    # Visit a parse tree produced by MiniGoParser#funcdecl.
    def visitFuncdecl(self, ctx:MiniGoParser.FuncdeclContext):
        # funcdecl: FUNC ID paramlistdecl returntyp? block
        name = ctx.ID().getText()
        params = self.visit(ctx.paramlistdecl())
        rettyp = self.visit(ctx.returntyp()) if ctx.returntyp() else VoidType()
        body = self.visit(ctx.block())
        return FuncDecl(name, params, rettyp, body)

    
    # Visit a parse tree produced by MiniGoParser#paramlistdecl.
    def visitParamlistdecl(self, ctx:MiniGoParser.ParamlistdeclContext):
        # paramlistdecl: LP nullparamlist RP
        return self.visit(ctx.nullparamlist())


    # Visit a parse tree produced by MiniGoParser#nullparamlist.
    def visitNullparamlist(self, ctx:MiniGoParser.NullparamlistContext):
        # nullparamlist: paramlist | 
        return self.visit(ctx.paramlist()) if ctx.paramlist() else []


    # Visit a parse tree produced by MiniGoParser#paramlist.
    def visitParamlist(self, ctx:MiniGoParser.ParamlistContext):
        # paramlist: sharedparamlist CM paramlist | sharedparamlist
        if ctx.CM():
            sharedparam = self.visit(ctx.sharedparamlist())
            paramlist = self.visit(ctx.paramlist())
            return sharedparam + paramlist
        return self.visit(ctx.sharedparamlist())


    # Visit a parse tree produced by MiniGoParser#sharedparamlist.
    def visitSharedparamlist(self, ctx:MiniGoParser.SharedparamlistContext):
        # sharedparamlist: params availtyp
        params = self.visit(ctx.params())
        paramtyp = self.visit(ctx.availtyp())
        return [ParamDecl(name, paramtyp) for name in params]


    # Visit a parse tree produced by MiniGoParser#params.
    def visitParams(self, ctx:MiniGoParser.ParamsContext):
        # params: ID CM params | ID
        if ctx.CM():
            param = ctx.ID().getText()
            params = self.visit(ctx.params())
            return [param] + params
        return [ctx.ID().getText()]
    

    # Visit a parse tree produced by MiniGoParser#methoddecl.
    def visitMethoddecl(self, ctx:MiniGoParser.MethoddeclContext):
        # methoddecl: FUNC receiver ID paramlistdecl returntyp? block
        # MethodDecl(receiver:str, recType:Type, fun:FuncDecl)
        recname, rectype = self.visit(ctx.receiver())
        name = ctx.ID().getText()
        params = self.visit(ctx.paramlistdecl())
        rettyp = self.visit(ctx.returntyp()) if ctx.returntyp() else VoidType()
        body = self.visit(ctx.block())
        funcdecl = FuncDecl(name, params, rettyp, body)
        return MethodDecl(recname, rectype, funcdecl)


    # Visit a parse tree produced by MiniGoParser#receiver.
    def visitReceiver(self, ctx:MiniGoParser.ReceiverContext):
        # receiver: LP ID ID RP
        recname = ctx.ID(0).getText()
        rectype = Id(ctx.ID(1).getText())
        return recname, rectype


    # Visit a parse tree produced by MiniGoParser#block.
    def visitBlock(self, ctx:MiniGoParser.BlockContext):
        # block: LB nullstmtlist RB
        # Block(member:List[BlockMember])
        return Block(self.visit(ctx.nullstmtlist()))


    # Visit a parse tree produced by MiniGoParser#nullstmtlist.
    def visitNullstmtlist(self, ctx:MiniGoParser.NullstmtlistContext):
        # nullstmtlist: stmtlist | 
        return self.visit(ctx.stmtlist()) if ctx.stmtlist() else []


    # Visit a parse tree produced by MiniGoParser#stmtlist.
    def visitStmtlist(self, ctx:MiniGoParser.StmtlistContext):
        # stmtlist: stmt stmtlist | stmt
        if ctx.stmtlist():
            stmt = self.visit(ctx.stmt())
            stmtlist = self.visit(ctx.stmtlist())
            return [stmt] + stmtlist
        return [self.visit(ctx.stmt())]


    # Visit a parse tree produced by MiniGoParser#expr.
    def visitExpr(self, ctx:MiniGoParser.ExprContext):
        # expr: expr OR orexpr | orexpr
        # BinaryOp(op:str, left:Expr, right:Expr)
        if ctx.OR():
            op = ctx.OR().getText()
            left = self.visit(ctx.expr())
            right = self.visit(ctx.orexpr())
            return BinaryOp(op, left, right)
        return self.visit(ctx.orexpr())


    # Visit a parse tree produced by MiniGoParser#orexpr.
    def visitOrexpr(self, ctx:MiniGoParser.OrexprContext):
        # orexpr: orexpr AND andexpr | andexpr
        # BinaryOp(op:str, left:Expr, right:Expr)
        if ctx.AND():
            op = ctx.AND().getText()
            left = self.visit(ctx.orexpr())
            right = self.visit(ctx.andexpr())
            return BinaryOp(op, left, right)
        return self.visit(ctx.andexpr())
            


    # Visit a parse tree produced by MiniGoParser#andexpr.
    def visitAndexpr(self, ctx:MiniGoParser.AndexprContext):
        # andexpr: andexpr (EQ | NEQ | LT | LTE | GT | GTE) relexpr | relexpr
        # BinaryOp(op:str, left:Expr, right:Expr)
        if ctx.andexpr():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.andexpr())
            right = self.visit(ctx.relexpr())
            return BinaryOp(op, left, right)
        return self.visit(ctx.relexpr())


    # Visit a parse tree produced by MiniGoParser#relexpr.
    def visitRelexpr(self, ctx:MiniGoParser.RelexprContext):
        # relexpr: relexpr (ADD | SUB) addexpr | addexpr
        # BinaryOp(op:str, left:Expr, right:Expr)
        if ctx.relexpr():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.relexpr())
            right = self.visit(ctx.addexpr())
            return BinaryOp(op, left, right)
        return self.visit(ctx.addexpr())


    # Visit a parse tree produced by MiniGoParser#addexpr.
    def visitAddexpr(self, ctx:MiniGoParser.AddexprContext):
        # addexpr: addexpr (MUL | DIV | MOD) mulexpr | mulexpr
        # BinaryOp(op:str, left:Expr, right:Expr)
        if ctx.addexpr():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.addexpr())
            right = self.visit(ctx.mulexpr())
            return BinaryOp(op, left, right)
        return self.visit(ctx.mulexpr())


    # Visit a parse tree produced by MiniGoParser#mulexpr.
    def visitMulexpr(self, ctx:MiniGoParser.MulexprContext):
        # mulexpr: SUB mulexpr | NOT mulexpr | notexpr
        # UnaryOp(op:str, body:Expr)
        if ctx.mulexpr():
            op = ctx.getChild(0).getText()
            body = self.visit(ctx.mulexpr())
            return UnaryOp(op, body)
        return self.visit(ctx.notexpr())



    # Visit a parse tree produced by MiniGoParser#notexpr.
    def visitNotexpr(self, ctx:MiniGoParser.NotexprContext, arrcell=[]):
        # notexpr: notexpr bracketop | notexpr mcallop | notexpr structop | dotexpr
        # MethCall(receiver:Expr, metName:str, args:List[Expr])
        # FieldAccess(receiver:Expr, field:str)
        # ArrayCell(arr:Expr, idx:List[Expr])
        if ctx.bracketop():
            cell = [self.visit(ctx.bracketop())] + arrcell
            return self.visitNotexpr(ctx.notexpr(), cell)
        if ctx.mcallop():
            receiver = self.visit(ctx.notexpr())
            name, args = self.visit(ctx.mcallop())
            lexpr = MethCall(receiver, name, args)
        if ctx.structop():
            receiver = self.visit(ctx.notexpr())
            field = self.visit(ctx.structop())
            lexpr = FieldAccess(receiver, field)
        if ctx.dotexpr():
            lexpr = self.visit(ctx.dotexpr())
        if arrcell:
            return ArrayCell(lexpr, arrcell)
        return lexpr
                


    # Visit a parse tree produced by MiniGoParser#dotexpr.
    def visitDotexpr(self, ctx:MiniGoParser.DotexprContext):
        # dotexpr: fcallop | callexpr
        if ctx.fcallop():
            return self.visit(ctx.fcallop())
        return self.visit(ctx.callexpr())


    # Visit a parse tree produced by MiniGoParser#callexpr.
    def visitCallexpr(self, ctx:MiniGoParser.CallexprContext):
        # callexpr: LP expr RP | parenexpr
        if ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.parenexpr())


    # Visit a parse tree produced by MiniGoParser#parenexpr.
    def visitParenexpr(self, ctx:MiniGoParser.ParenexprContext):
        # parenexpr: operand
        return self.visit(ctx.operand())


    # Visit a parse tree produced by MiniGoParser#bracketop.
    def visitBracketop(self, ctx:MiniGoParser.BracketopContext):
        # bracketop: LS expr RS
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#mcallop.
    def visitMcallop(self, ctx:MiniGoParser.McallopContext):
        # mcallop: DOT ID arglistdecl
        name = ctx.ID().getText()
        args = self.visit(ctx.arglistdecl())
        return name, args


    # Visit a parse tree produced by MiniGoParser#fcallop.
    def visitFcallop(self, ctx:MiniGoParser.FcallopContext):
        # fcallop: ID arglistdecl
        # FuncCall(funName:str, args:List[Expr])
        name = ctx.ID().getText()
        args = self.visit(ctx.arglistdecl())
        return FuncCall(name, args)


    # Visit a parse tree produced by MiniGoParser#structop.
    def visitStructop(self, ctx:MiniGoParser.StructopContext):
        # structop: DOT ID
        return ctx.ID().getText()


    # Visit a parse tree produced by MiniGoParser#operand.
    def visitOperand(self, ctx:MiniGoParser.OperandContext):
        # operand: bltinlit | ID
        # Id(name:str)
        if ctx.bltinlit():
            return self.visit(ctx.bltinlit())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#stmt.
    def visitStmt(self, ctx:MiniGoParser.StmtContext):
        # stmt: semistmt stmtterm | optsemistmt stmtterm | nosemistmt stmtterm | exstmt stmtterm | returnstmt SC
        return self.visit(ctx.getChild(0))
    
    
    # Visit a parse tree produced by MiniGoParser#semistmt.
    def visitSemistmt(self, ctx:MiniGoParser.SemistmtContext):
        #semistmt: vardecl | constdecl | asgnstmt | breakstmt | continuestmt | callstmt
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#optsemistmt.
    def visitOptsemistmt(self, ctx:MiniGoParser.OptsemistmtContext):
        # optsemistmt: structdecl | interfacedecl
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#nosemistmt.
    def visitNosemistmt(self, ctx:MiniGoParser.NosemistmtContext):
        # nosemistmt: ifstmt | forstmt | funcdecl | methoddecl
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#asgnstmt.
    def visitAsgnstmt(self, ctx:MiniGoParser.AsgnstmtContext):
        # asgnstmt: varexpr (ASGN | ADDEQ | SUBEQ | MULEQ | DIVEQ | MODEQ) expr
        lhs = self.visit(ctx.varexpr())
        rhs = self.visit(ctx.expr())
        eop = ctx.getChild(1).getText()[0]
        if eop != ":":
            rhs = BinaryOp(eop, lhs, rhs)
        return Assign(lhs, rhs)


    # Visit a parse tree produced by MiniGoParser#varexpr.
    def visitVarexpr(self, ctx:MiniGoParser.VarexprContext, arrcell=[]):
        # varexpr: varexpr bracketop | varexpr structop | ID
        if ctx.bracketop():
            cell = [self.visit(ctx.bracketop())] + arrcell
            return self.visitVarexpr(ctx.varexpr(), cell)
        if ctx.structop():
            receiver = self.visit(ctx.varexpr())
            field = self.visit(ctx.structop())
            lexpr = FieldAccess(receiver, field)
        if ctx.ID():
            lexpr = Id(ctx.ID().getText())
        if arrcell:
            return ArrayCell(lexpr, arrcell)
        return lexpr


    # Visit a parse tree produced by MiniGoParser#ifstmt.
    def visitIfstmt(self, ctx:MiniGoParser.IfstmtContext):
        # ifstmt: IF logicexpr block elseportion
        # If(expr:Expr, thenStmt:Stmt, elseStmt:Stmt)
        logic = self.visit(ctx.logicexpr())
        thenstmt = self.visit(ctx.block())
        elsestmt = self.visit(ctx.elseportion())
        return If(logic, thenstmt, elsestmt)


    # Visit a parse tree produced by MiniGoParser#logicexpr.
    def visitLogicexpr(self, ctx:MiniGoParser.LogicexprContext):
        # logicexpr: LP expr RP
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#elseportion.
    def visitElseportion(self, ctx:MiniGoParser.ElseportionContext):
        # elseportion: elseiflist? elseonly?
        elseblock = self.visit(ctx.elseonly()) if ctx.elseonly() else None
        if ctx.elseiflist():
            return self.visitElseiflist(ctx.elseiflist(), elseblock)
        return elseblock
            

    # Visit a parse tree produced by MiniGoParser#elseonly.
    def visitElseonly(self, ctx:MiniGoParser.ElseonlyContext):
        # elseonly: ELSE block
        return self.visit(ctx.block())


    # Visit a parse tree produced by MiniGoParser#elseiflist.
    def visitElseiflist(self, ctx:MiniGoParser.ElseiflistContext, elseblock=None):
        # elseiflist: elseifstmt elseiflist | elseifstmt
        logic, thenstmt = self.visit(ctx.elseifstmt())
        if ctx.elseiflist():
            elsestmt = self.visitElseiflist(ctx.elseiflist(), elseblock)
            return If(logic, thenstmt, elsestmt)
        return If(logic, thenstmt, elseblock)
        


    # Visit a parse tree produced by MiniGoParser#elseifstmt.
    def visitElseifstmt(self, ctx:MiniGoParser.ElseifstmtContext):
        # elseifstmt: ELSE IF logicexpr block
        logic = self.visit(ctx.logicexpr())
        thenstmt = self.visit(ctx.block())
        return logic, thenstmt


    # Visit a parse tree produced by MiniGoParser#forstmt.
    def visitForstmt(self, ctx:MiniGoParser.ForstmtContext):
        # forstmt: basicfor | standfor | rangefor
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#basicfor.
    def visitBasicfor(self, ctx:MiniGoParser.BasicforContext):
        # basicfor: FOR expr block
        cond = self.visit(ctx.expr())
        loop = self.visit(ctx.block())
        return ForBasic(cond, loop)


    # Visit a parse tree produced by MiniGoParser#standfor.
    def visitStandfor(self, ctx:MiniGoParser.StandforContext):
        # standfor: FOR forinit SC forcond SC forupdt block
        init = self.visit(ctx.forinit())
        cond = self.visit(ctx.forcond())
        upda = self.visit(ctx.forupdt())
        loop = self.visit(ctx.block())
        return ForStep(init, cond, upda, loop)


    # Visit a parse tree produced by MiniGoParser#rangefor.
    def visitRangefor(self, ctx:MiniGoParser.RangeforContext):
        # rangefor: FOR ID CM ID ASGN RANGE expr block
        idx = Id(ctx.ID(0).getText())
        val = Id(ctx.ID(1).getText())
        arr = self.visit(ctx.expr())
        loop = self.visit(ctx.block())
        return ForEach(idx, val, arr, loop)


    # Visit a parse tree produced by MiniGoParser#forinit.
    def visitForinit(self, ctx:MiniGoParser.ForinitContext):
        # forinit: forasgn | forvardecl
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#forasgn.
    def visitForasgn(self, ctx:MiniGoParser.ForasgnContext):
        # forasgn: ID ASGN expr
        var = Id(ctx.ID().getText())
        expr = self.visit(ctx.expr())
        return Assign(var, expr)


    # Visit a parse tree produced by MiniGoParser#forvardecl.
    def visitForvardecl(self, ctx:MiniGoParser.ForvardeclContext):
        # forvardecl: VAR ID vartyp? INIT expr
        varname = ctx.ID().getText()
        vartyp = self.visit(ctx.vartyp()) if ctx.vartyp() else None
        expr = self.visit(ctx.expr())
        return VarDecl(varname, vartyp, expr)


    # Visit a parse tree produced by MiniGoParser#forcond.
    def visitForcond(self, ctx:MiniGoParser.ForcondContext):
        # forcond: expr
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#forupdt.
    def visitForupdt(self, ctx:MiniGoParser.ForupdtContext):
        # forupdt: asgnstmt
        return self.visit(ctx.asgnstmt())


    # Visit a parse tree produced by MiniGoParser#breakstmt.
    def visitBreakstmt(self, ctx:MiniGoParser.BreakstmtContext):
        # breakstmt: BREAK
        return Break()


    # Visit a parse tree produced by MiniGoParser#continuestmt.
    def visitContinuestmt(self, ctx:MiniGoParser.ContinuestmtContext):
        # continuestmt: CONTINUE
        return Continue()


    # Visit a parse tree produced by MiniGoParser#callstmt.
    def visitCallstmt(self, ctx:MiniGoParser.CallstmtContext):
        # callstmt: fcallop | varcall mcallop
        if ctx.fcallop():
            return self.visit(ctx.fcallop())
        receiver = self.visit(ctx.varcall())
        name, args = self.visit(ctx.mcallop())
        return MethCall(receiver, name, args)


    # Visit a parse tree produced by MiniGoParser#varcall.
    def visitVarcall(self, ctx:MiniGoParser.VarcallContext, arrcell=[]):
        # varcall: varcall bracketop | varcall structop | varcall mcallop | ID
        if ctx.bracketop():
            cell = [self.visit(ctx.bracketop())] + arrcell
            return self.visitVarcall(ctx.varcall(), cell)
        if ctx.structop():
            receiver = self.visit(ctx.varcall())
            field = self.visit(ctx.structop())
            lexpr = FieldAccess(receiver, field)
        if ctx.mcallop():
            receiver = self.visit(ctx.varcall())
            method, args = self.visit(ctx.mcallop())
            lexpr = MethCall(receiver, method, args)
        if ctx.ID():
            lexpr = Id(ctx.ID().getText())
        if arrcell:
            return ArrayCell(lexpr, arrcell)
        return lexpr


    # Visit a parse tree produced by MiniGoParser#returnstmt.
    def visitReturnstmt(self, ctx:MiniGoParser.ReturnstmtContext):
        # returnstmt: RETURN expr?
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return Return(expr)


    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        # program: stmtlist EOF
        # Program(decl:List[Decl])
        decl_list = self.visit(ctx.stmtlist())
        return Program(decl_list)