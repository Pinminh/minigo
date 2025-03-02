from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

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
        # Id(name: str)
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#arrtyp.
    def visitArrtyp(self, ctx:MiniGoParser.ArrtypContext):
        # arrtyp: dimlist arrvaltyp
        # ArrayType(dimens: List[Expr], eleType: Type)
        dimlist = self.visit(ctx.dimlist())
        eletype = self.visit(ctx.arrvaltyp())
        return ArrayType(dimlist, eletype)


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
        # IntLiteral(value: int)
        # Id(name: str)
        if ctx.INITLIT():
            return IntLiteral(int(ctx.INTLIT()))
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#bltintyp.
    def visitBltintyp(self, ctx:MiniGoParser.BltintypContext):
        # bltintyp: primtyp | arrtyp
        if ctx.primtyp():
            return self.visit(ctx.primtyp())
        return self.visit(ctx.arrtyp())


    # Visit a parse tree produced by MiniGoParser#returntyp.
    def visitReturntyp(self, ctx:MiniGoParser.ReturntypContext):
        # returntyp: bltintyp
        return self.visit(ctx.bltintyp())


    # Visit a parse tree produced by MiniGoParser#primlit.
    def visitPrimlit(self, ctx:MiniGoParser.PrimlitContext):
        # primlit: INTLIT | FLOATLIT | BOOLLIT | STRLIT
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT()))
        if ctx.BOOLLIT():
            return BooleanLiteral(ctx.BOOLLIT().getText() == 'true')
        return StringLiteral(ctx.STRLIT().getText())


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
        return ctx.complit()


    # Visit a parse tree produced by MiniGoParser#stmtterm.
    def visitStmtterm(self, ctx:MiniGoParser.StmttermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#paramlistdecl.
    def visitParamlistdecl(self, ctx:MiniGoParser.ParamlistdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nullparamlist.
    def visitNullparamlist(self, ctx:MiniGoParser.NullparamlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#sharedtyplist.
    def visitSharedtyplist(self, ctx:MiniGoParser.SharedtyplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#params.
    def visitParams(self, ctx:MiniGoParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#pairtyplist.
    def visitPairtyplist(self, ctx:MiniGoParser.PairtyplistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#parampairs.
    def visitParampairs(self, ctx:MiniGoParser.ParampairsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#parampair.
    def visitParampair(self, ctx:MiniGoParser.ParampairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arglistdecl.
    def visitArglistdecl(self, ctx:MiniGoParser.ArglistdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nullarglist.
    def visitNullarglist(self, ctx:MiniGoParser.NullarglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arglist.
    def visitArglist(self, ctx:MiniGoParser.ArglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrdecl.
    def visitArrdecl(self, ctx:MiniGoParser.ArrdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arrlit.
    def visitArrlit(self, ctx:MiniGoParser.ArrlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elemlistdecl.
    def visitElemlistdecl(self, ctx:MiniGoParser.ElemlistdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nullelemlist.
    def visitNullelemlist(self, ctx:MiniGoParser.NullelemlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elemlist.
    def visitElemlist(self, ctx:MiniGoParser.ElemlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#recurlist.
    def visitRecurlist(self, ctx:MiniGoParser.RecurlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#litlist.
    def visitLitlist(self, ctx:MiniGoParser.LitlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elemlit.
    def visitElemlit(self, ctx:MiniGoParser.ElemlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structdecl.
    def visitStructdecl(self, ctx:MiniGoParser.StructdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fieldlist.
    def visitFieldlist(self, ctx:MiniGoParser.FieldlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#field.
    def visitField(self, ctx:MiniGoParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structlit.
    def visitStructlit(self, ctx:MiniGoParser.StructlitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fieldinitdecl.
    def visitFieldinitdecl(self, ctx:MiniGoParser.FieldinitdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nullstructinitlist.
    def visitNullstructinitlist(self, ctx:MiniGoParser.NullstructinitlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structinitlist.
    def visitStructinitlist(self, ctx:MiniGoParser.StructinitlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fieldval.
    def visitFieldval(self, ctx:MiniGoParser.FieldvalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#interfacedecl.
    def visitInterfacedecl(self, ctx:MiniGoParser.InterfacedeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#methodlist.
    def visitMethodlist(self, ctx:MiniGoParser.MethodlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#method.
    def visitMethod(self, ctx:MiniGoParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#vardecl.
    def visitVardecl(self, ctx:MiniGoParser.VardeclContext):
        # vardecl: typdecl | untypdecl
        if ctx.typdecl():
            return self.visit(ctx.typdecl())
        return self.visit(ctx.untypdecl())


    # Visit a parse tree produced by MiniGoParser#typdecl.
    def visitTypdecl(self, ctx:MiniGoParser.TypdeclContext):
        # typdecl: VAR ID vartyp varinit?
        # VarDecl(varName: str, varType: Type, varInit: Expr)
        varname = ctx.ID().getText()
        vartype = self.visit(ctx.vartyp())
        varinit = self.visit(ctx.varinit()) if ctx.varinit() else None
        return VarDecl(varname, vartype, varinit)


    # Visit a parse tree produced by MiniGoParser#untypdecl.
    def visitUntypdecl(self, ctx:MiniGoParser.UntypdeclContext):
        # untypdecl: VAR ID varinit
        # VarDecl(varname: str, VarType: Type, varInit: Expr)
        varname = ctx.ID().getText()
        vartype = None
        varinit = self.visit(ctx.varinit())
        return VarDecl(varname, vartype, varinit)


    # Visit a parse tree produced by MiniGoParser#vartyp.
    def visitVartyp(self, ctx:MiniGoParser.VartypContext):
        # vartyp: bltintyp | ID
        # Id(name: str)
        if ctx.bltintyp():
            return self.visit(ctx.bltintyp())
        return Id(ctx.ID().getText())


    # Visit a parse tree produced by MiniGoParser#varinit.
    def visitVarinit(self, ctx:MiniGoParser.VarinitContext):
        # varinit: INIT expr
        return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#constdecl.
    def visitConstdecl(self, ctx:MiniGoParser.ConstdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#funcdecl.
    def visitFuncdecl(self, ctx:MiniGoParser.FuncdeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#methoddecl.
    def visitMethoddecl(self, ctx:MiniGoParser.MethoddeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#receiver.
    def visitReceiver(self, ctx:MiniGoParser.ReceiverContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#block.
    def visitBlock(self, ctx:MiniGoParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#nullstmtlist.
    def visitNullstmtlist(self, ctx:MiniGoParser.NullstmtlistContext):
        return self.visitChildren(ctx)


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
        return Expr()


    # Visit a parse tree produced by MiniGoParser#orexpr.
    def visitOrexpr(self, ctx:MiniGoParser.OrexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#andexpr.
    def visitAndexpr(self, ctx:MiniGoParser.AndexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#relexpr.
    def visitRelexpr(self, ctx:MiniGoParser.RelexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#addexpr.
    def visitAddexpr(self, ctx:MiniGoParser.AddexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#mulexpr.
    def visitMulexpr(self, ctx:MiniGoParser.MulexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#notexpr.
    def visitNotexpr(self, ctx:MiniGoParser.NotexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#dotexpr.
    def visitDotexpr(self, ctx:MiniGoParser.DotexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#callexpr.
    def visitCallexpr(self, ctx:MiniGoParser.CallexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#parenexpr.
    def visitParenexpr(self, ctx:MiniGoParser.ParenexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#bracketop.
    def visitBracketop(self, ctx:MiniGoParser.BracketopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#mcallop.
    def visitMcallop(self, ctx:MiniGoParser.McallopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fcallop.
    def visitFcallop(self, ctx:MiniGoParser.FcallopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#structop.
    def visitStructop(self, ctx:MiniGoParser.StructopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#operand.
    def visitOperand(self, ctx:MiniGoParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#evalexpr.
    def visitEvalexpr(self, ctx:MiniGoParser.EvalexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#stmt.
    def visitStmt(self, ctx:MiniGoParser.StmtContext):
        # stmt: semistmt stmtterm | optsemistmt stmtterm | nosemistmt stmtterm
        if ctx.semistmt():
            return self.visit(ctx.semistmt())
        if ctx.optsemistmt():
            return self.visit(ctx.optsemistmt())
        return self.visit(ctx.nosemistmt())


    # Visit a parse tree produced by MiniGoParser#semistmt.
    def visitSemistmt(self, ctx:MiniGoParser.SemistmtContext):
        # semistmt: vardecl | constdecl | asgnstmt | breakstmt | continuestmt | callstmt | returnstmt
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        if ctx.constdecl():
            return self.visit(ctx.constdecl())
        if ctx.asgnstmt():
            return self.visit(ctx.asgnstmt())
        if ctx.breakstmt():
            return self.visit(ctx.breakstmt())
        if ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        if ctx.callstmt():
            return self.visit(ctx.callstmt())
        return self.visit(ctx.returnstmt())


    # Visit a parse tree produced by MiniGoParser#optsemistmt.
    def visitOptsemistmt(self, ctx:MiniGoParser.OptsemistmtContext):
        # optsemistmt: structdecl | interfacedecl
        if ctx.structdecl():
            return self.visit(ctx.structdecl())
        return self.visit(ctx.interfacedecl())


    # Visit a parse tree produced by MiniGoParser#nosemistmt.
    def visitNosemistmt(self, ctx:MiniGoParser.NosemistmtContext):
        # nosemistmt: ifstmt | forstmt | funcdecl | methoddecl
        if ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        if ctx.forstmt():
            return self.visit(ctx.forstmt())
        if ctx.funcdecl():
            return self.visit(ctx.funcdecl())
        return self.visit(ctx.methoddecl())


    # Visit a parse tree produced by MiniGoParser#asgnstmt.
    def visitAsgnstmt(self, ctx:MiniGoParser.AsgnstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#varexpr.
    def visitVarexpr(self, ctx:MiniGoParser.VarexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#vararr.
    def visitVararr(self, ctx:MiniGoParser.VararrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arridxlist.
    def visitArridxlist(self, ctx:MiniGoParser.ArridxlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#varstruct.
    def visitVarstruct(self, ctx:MiniGoParser.VarstructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#fieldacclist.
    def visitFieldacclist(self, ctx:MiniGoParser.FieldacclistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#asgnop.
    def visitAsgnop(self, ctx:MiniGoParser.AsgnopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#ifstmt.
    def visitIfstmt(self, ctx:MiniGoParser.IfstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#logicexpr.
    def visitLogicexpr(self, ctx:MiniGoParser.LogicexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elseportion.
    def visitElseportion(self, ctx:MiniGoParser.ElseportionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elseonly.
    def visitElseonly(self, ctx:MiniGoParser.ElseonlyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elseiflist.
    def visitElseiflist(self, ctx:MiniGoParser.ElseiflistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#elseifstmt.
    def visitElseifstmt(self, ctx:MiniGoParser.ElseifstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forstmt.
    def visitForstmt(self, ctx:MiniGoParser.ForstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#basicfor.
    def visitBasicfor(self, ctx:MiniGoParser.BasicforContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#standfor.
    def visitStandfor(self, ctx:MiniGoParser.StandforContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#rangefor.
    def visitRangefor(self, ctx:MiniGoParser.RangeforContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forinit.
    def visitForinit(self, ctx:MiniGoParser.ForinitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forasgn.
    def visitForasgn(self, ctx:MiniGoParser.ForasgnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forvardecl.
    def visitForvardecl(self, ctx:MiniGoParser.ForvardeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forcond.
    def visitForcond(self, ctx:MiniGoParser.ForcondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#forupdt.
    def visitForupdt(self, ctx:MiniGoParser.ForupdtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#breakstmt.
    def visitBreakstmt(self, ctx:MiniGoParser.BreakstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#continuestmt.
    def visitContinuestmt(self, ctx:MiniGoParser.ContinuestmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#callstmt.
    def visitCallstmt(self, ctx:MiniGoParser.CallstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#returnstmt.
    def visitReturnstmt(self, ctx:MiniGoParser.ReturnstmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        # program: stmtlist EOF
        # Program(decl: List[Decl])
        decl_list = self.visit(ctx.stmtlist())
        return Program(decl_list)