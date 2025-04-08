import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """func main() {};"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 300))

    def test_uninitialized_vardecl_1(self):
        input = r"""var x float ;"""
        expect = str(Program([
            VarDecl("x", FloatType(), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 301))
    
    def test_uninitialized_vardecl_2(self):
        input = r"""var __forbidden string;"""
        expect = str(Program([
            VarDecl("__forbidden", StringType(), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 302))
    
    def test_uninitialized_vardecl_3(self):
        input = r"""           var for_fun   boolean;   """
        expect = str(Program([
            VarDecl("for_fun", BoolType(), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 303))
    
    def test_initialized_vardecl_1(self):
        input = r"""var x float = 2.1e3;"""
        expect = str(Program([
            VarDecl("x", FloatType(), FloatLiteral("2.1e3"))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 304))
    
    def test_initialized_vardecl_2(self):
        input = r"""var thing int = 3;  """
        expect = str(Program([
            VarDecl("thing", IntType(), IntLiteral("3"))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 305))
    
    def test_initialized_vardecl_3(self):
        input = r"""var s string = "welcome to PPL"; """
        expect = str(Program([
            VarDecl("s", StringType(), StringLiteral('"welcome to PPL"'))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 306))
    
    def test_constant_decl_1(self):
        input = r"""const Pi = Circumference / Diameter"""
        expect = str(Program([
            ConstDecl("Pi", None, BinaryOp("/", Id("Circumference"), Id("Diameter")))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 307))
    
    def test_constant_decl_2(self):
        input = r"""const DRESSCODE =  "dxd-" ;"""
        expect = str(Program([
            ConstDecl("DRESSCODE", None, StringLiteral('"dxd-"'))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 308))
    
    def test_constant_decl_3(self):
        input = r"""const Euler =  2.718281828 ;"""
        expect = str(Program([
            ConstDecl("Euler", None, FloatLiteral("2.718281828"))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))
    
    def test_array_decl_1(self):
        input = r""" var arr [3][2]int ;"""
        expect = str(Program([
            VarDecl("arr", ArrayType([IntLiteral("3"), IntLiteral("2")], IntType()), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))
    
    def test_array_decl_2(self):
        input = r""" var person_list [10]Person; """
        expect = str(Program([
            VarDecl("person_list", ArrayType([IntLiteral("10")], Id("Person")), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 311))
    
    def test_array_decl_3(self):
        input = r""" var str_mat [3][2][4]string; """
        expect = str(Program([
            VarDecl("str_mat", ArrayType([IntLiteral("3"), IntLiteral("2"), IntLiteral("4")], StringType()), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 312))
    
    def test_expression_1(self):
        input = r""" var expr = (3 + 2) ;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("+",
                IntLiteral("3"),
                IntLiteral("2")
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 313))
    
    def test_expression_2(self):
        input = r""" var expr = 1 + a/(1 - b) ;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("+",
                IntLiteral("1"), BinaryOp("/",
                    Id("a"), BinaryOp("-",
                        IntLiteral("1"), Id("b")
                    )
                )
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 314))
    
    def test_expression_3(self):
        input = r""" var expr = a || b && !c ;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("||",
                Id("a"), BinaryOp("&&",
                    Id("b"), UnaryOp("!", Id("c"))
                )
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 315))
    
    def test_expression_4(self):
        input = r""" var expr = a -b+ c -d ;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("-",
                BinaryOp("+",
                    BinaryOp("-",
                        Id("a"), Id("b")
                    ), Id("c")
                ), Id("d")
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 316))
    
    def test_expression_5(self):
        input = r""" var expr = true == false > a || b;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("||",
                BinaryOp(">",
                    BinaryOp("==",
                        BooleanLiteral(True), BooleanLiteral(False)
                    ), Id("a")
                ), Id("b")
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 317))
    
    def test_expression_6(self):
        input = r""" var expr = 16 % a != -b/2;"""
        expect = str(Program([
            VarDecl("expr", None, BinaryOp("!=",
                BinaryOp("%", IntLiteral("16"), Id("a")),
                BinaryOp("/", UnaryOp("-", Id("b")), IntLiteral("2"))
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))
    
    def test_expression_7(self):
        input = r""" var expr = list[3][2][0];"""
        expect = str(Program([
            VarDecl("expr", None, ArrayCell(Id("list"),
                [IntLiteral("3"), IntLiteral("2"), IntLiteral("0")]
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))
    
    def test_expression_8(self):
        input = r""" var expr = list[3][indices[0]];"""
        expect = str(Program([
            VarDecl("expr", None, ArrayCell(Id("list"),
                [IntLiteral("3"), ArrayCell(Id("indices"), [IntLiteral("0")])]
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))
    
    def test_expression_9(self):
        input = r""" var expr = person.daughter.age;"""
        expect = str(Program([
            VarDecl("expr", None, FieldAccess(
                FieldAccess(Id("person"), "daughter"), "age"
            ))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))
    
    def test_expression_10(self):
        input = r""" var expr = person.heart.stop_beating();"""
        expect = str(Program([
            VarDecl("expr", None,
                MethCall(FieldAccess(Id("person"), "heart"), "stop_beating", [])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))
    
    def test_expression_11(self):
        input = r""" var expr = person.get(drinks[i][j], foods[0]);"""
        expect = str(Program([
            VarDecl("expr", None,
                MethCall(Id("person"), "get", [
                    ArrayCell(Id("drinks"), [Id("i"), Id("j")]),
                    ArrayCell(Id("foods"), [IntLiteral("0")])
                ])
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))
    
    def test_expression_12(self):
        input = r""" var expr = persons[i].daughters.get_tallest().name;"""
        expect = str(Program([
            VarDecl("expr", None,
                FieldAccess(
                    MethCall(
                        FieldAccess(ArrayCell(Id("persons"), [Id("i")]), "daughters"),
                        "get_tallest", []
                    ), "name"
                )
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))
    
    def test_expression_13(self):
        input = r""" var expr = areas[x][y].plant(trees[y + 3 * x]);"""
        expect = str(Program([
            VarDecl("expr", None,
                MethCall(
                    ArrayCell(Id("areas"), [Id("x"), Id("y")]),
                    "plant", [ArrayCell(Id("trees"), [BinaryOp("+", Id("y"), BinaryOp("*", IntLiteral("3"), Id("x")))])]
                )
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))
    
    def test_composite_literal_1(self):
        input = r""" var expr = [3]int{1, c, 3};"""
        dimens = [IntLiteral("3")]
        eltype = IntType()
        values = [IntLiteral("1"), Id("c"), IntLiteral("3")]
        expect = str(Program([VarDecl("expr", None,
            ArrayLiteral(dimens, eltype, values)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))
    
    def test_composite_literal_2(self):
        input = r""" var expr = [a][b]boolean{{true, false}, {false, true}};"""
        dimens = [Id("a"), Id("b")]
        eltype = BoolType()
        values = [[BooleanLiteral(True), BooleanLiteral(False)], [BooleanLiteral(False), BooleanLiteral(True)]]
        expect = str(Program([VarDecl("expr", None,
            ArrayLiteral(dimens, eltype, values)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))
    
    def test_composite_literal_3(self):
        input = r""" var expr = [1][1][1]string{{{"single"}}};"""
        dimens = [IntLiteral("1"), IntLiteral("1"), IntLiteral("1")]
        eltype = StringType()
        values = [[[StringLiteral('"single"')]]]
        expect = str(Program([VarDecl("expr", None,
            ArrayLiteral(dimens, eltype, values)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))
    
    def test_composite_literal_4(self):
        input = r""" var expr = MyStruct{}"""
        name = "MyStruct"
        tuples = []
        expect = str(Program([VarDecl("expr", None,
            StructLiteral(name, tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 329))
    
    def test_composite_literal_5(self):
        input = r""" var expr = MyStruct{name: "hello", age: bank[2]}"""
        name = "MyStruct"
        tuples = [
            ("name", StringLiteral('"hello"')),
            ("age", ArrayCell(Id("bank"), [IntLiteral("2")]))
        ]
        expect = str(Program([VarDecl("expr", None,
            StructLiteral(name, tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))
    
    def test_composite_literal_6(self):
        input = r""" var expr = Person{name: "Joyce", dad: Person{name: "Welt"}, mom: Person{name: "Tesla"}}"""
        tuples = [
            ("name", StringLiteral('"Joyce"')),
            ("dad", StructLiteral("Person", [("name", StringLiteral('"Welt"'))])),
            ("mom", StructLiteral("Person", [("name", StringLiteral('"Tesla"'))]))
        ]
        expect = str(Program([VarDecl("expr", None,
            StructLiteral("Person", tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))
    
    def test_composite_literal_7(self):
        input = r""" var expr = A{b: B{c: C{d: D{}}}}"""
        tuples = [("b", StructLiteral("B", [("c", StructLiteral("C", [("d", StructLiteral("D", []))]))]))]
        expect = str(Program([VarDecl("expr", None,
            StructLiteral("A", tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))
    
    def test_composite_literal_8(self):
        input = r""" var expr = [2]Baby{Baby{age: 0.5}, Baby{age: 0.6}};"""
        dimens = [IntLiteral("2")]
        eltype = Id("Baby")
        values = [
            StructLiteral("Baby", [("age", FloatLiteral("0.5"))]),
            StructLiteral("Baby", [("age", FloatLiteral("0.6"))])
        ]
        expect = str(Program([VarDecl("expr", None,
            ArrayLiteral(dimens, eltype, values)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))
    
    def test_composite_literal_9(self):
        input = r""" var expr = [u][v]A{ {A{}, A{}}, {A{}, A{}} };"""
        dimens = [Id("u"), Id("v")]
        eltype = Id("A")
        elem = StructLiteral("A", [])
        values = [[elem, elem], [elem, elem]]
        expect = str(Program([VarDecl("expr", None,
            ArrayLiteral(dimens, eltype, values)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))
    
    def test_composite_literal_10(self):
        input = r""" var expr = MyStruct{ a: [2]string{s, t} }"""
        tuples = [("a", ArrayLiteral([IntLiteral("2")], StringType(), [Id("s"), Id("t")]))]
        expect = str(Program([VarDecl("expr", None,
            StructLiteral("MyStruct", tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 335))
    
    def test_composite_literal_11(self):
        input = r""" var expr = A{   a: [2][2]A{  { A{}, A{} }, { A{}, A{} }  }   }   ;"""
        e = StructLiteral("A", [])
        tuples = [("a", ArrayLiteral(
            [IntLiteral("2"), IntLiteral("2")],
            Id("A"),
            [[e, e], [e, e]]
        ))]
        expect = str(Program([VarDecl("expr", None,
            StructLiteral("A", tuples)
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))
    
    def test_struct_decl_1(self):
        input = r"""
            type Person struct {
                name string
                age int
            }
            var p = Person{name: "F", age: 0xabFA1}
        """
        expect = str(Program([
            StructType("Person", [("name", StringType()), ("age", IntType())], []),
            VarDecl("p", None, StructLiteral("Person", [("name", StringLiteral('"F"')), ("age", IntLiteral("0xabFA1"))]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))
    
    def test_struct_decl_2(self):
        input = r"""
            type Person struct {
                children [N]Person ;
                pockets [M][K]float
            };
        """
        expect = str(Program([
            StructType("Person", [
                ("children", ArrayType([Id("N")], Id("Person"))),
                ("pockets", ArrayType([Id("M"), Id("K")], FloatType()))    
            ], [])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 338))
    
    def test_struct_decl_3(self):
        input = r"""
            type Person struct {
                disabled boolean;
                weight float;
            };
        """
        expect = str(Program([
            StructType("Person", [
                ("disabled", BoolType()),
                ("weight", FloatType())    
            ], [])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 339))
    
    def test_assignment_1(self):
        input = r""" p := Person{genius: true} """
        expect = str(Program([
            Assign(Id("p"), StructLiteral("Person", [("genius", BooleanLiteral(True))]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))
        
    def test_assignment_2(self):
        input = r""" weights[x][y][z] += h / 2 * Pi """
        lhs = ArrayCell(Id("weights"), [Id("x"), Id("y"), Id("z")])
        rhs = BinaryOp("*", BinaryOp("/", Id("h"), IntLiteral("2")), Id("Pi"))
        rhs = BinaryOp("+", lhs, rhs)
        expect = str(Program([
            Assign(lhs, rhs)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 341))
    
    def test_assignment_3(self):
        input = r""" earth.surface.lake.volume /= constsets[i][3].super_pi """
        lhs = FieldAccess(FieldAccess(FieldAccess(Id("earth"), "surface"), "lake"), "volume")
        rhs = FieldAccess(ArrayCell(Id("constsets"), [Id("i"), IntLiteral("3")]), "super_pi")
        rhs = BinaryOp("/", lhs, rhs)
        expect = str(Program([
            Assign(lhs, rhs)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))
    
    def test_assignment_4(self):
        input = r""" peoples[0].first := "John" + " " + "Kenedy" """
        lhs = FieldAccess(ArrayCell(Id("peoples"), [IntLiteral("0")]), "first")
        rhs = BinaryOp("+", BinaryOp("+", StringLiteral('"John"'), StringLiteral('" "')), StringLiteral('"Kenedy"'))
        # rhs = BinaryOp("/", lhs, rhs)
        expect = str(Program([
            Assign(lhs, rhs)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))
    
    def test_assignment_5(self):
        input = r""" customer.items[i].price %= modifier < TrueRate """
        lhs = FieldAccess(ArrayCell(FieldAccess(Id("customer"), "items"), [Id("i")]), "price")
        rhs = BinaryOp("<", Id("modifier"), Id("TrueRate"))
        rhs = BinaryOp("%", lhs, rhs)
        expect = str(Program([
            Assign(lhs, rhs)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))
    
    def test_loop_control_statement(self):
        input = r"""
            continue;
            break;
            return;
        """
        expect = str(Program([
            Continue(), Break(), Return(None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))
    
    def test_complex_return_1(self):
        input = r"""return f + a[j].attr * me.lst[-i];"""
        term1 = Id("f")
        term2 = FieldAccess(ArrayCell(Id("a"), [Id("j")]), "attr")
        term3 = ArrayCell(FieldAccess(Id("me"), "lst"), [UnaryOp("-", Id("i"))])
        expect = str(Program([Return(
            BinaryOp("+", term1, BinaryOp("*", term2, term3))
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))
    
    def test_complex_return_2(self):
        input = r"""return f + a[j].attr * me.lst[-i];"""
        term1 = Id("f")
        term2 = FieldAccess(ArrayCell(Id("a"), [Id("j")]), "attr")
        term3 = ArrayCell(FieldAccess(Id("me"), "lst"), [UnaryOp("-", Id("i"))])
        expect = str(Program([Return(
            BinaryOp("+", term1, BinaryOp("*", term2, term3))
        )]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))
    
    def test_singular_function_call_1(self):
        input = r""" add_sugar(tables[x][y].plate, 0.43) """
        args = [FieldAccess(ArrayCell(Id("tables"), [Id("x"), Id("y")]), "plate"), FloatLiteral("0.43")]
        expect = str(Program([FuncCall("add_sugar", args)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))
    
    def test_singular_function_call_2(self):
        input = r""" non_arg_func() """
        name = "non_arg_func"
        args = []
        expect = str(Program([FuncCall(name, args)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))
    
    def test_singular_method_call_1(self):
        input = r""" objs[0].do_calc(arg1, a || b - c) ;"""
        receiver = ArrayCell(Id("objs"), [IntLiteral("0")])
        name = "do_calc"
        args = [Id("arg1"), BinaryOp("||", Id("a"), BinaryOp("-", Id("b"), Id("c")))]
        expect = str(Program([MethCall(receiver, name, args)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))
    
    def test_singular_method_call_2(self):
        input = r""" person.get_sons()[0].power_up(person.mom) """
        receiver = ArrayCell(MethCall(Id("person"), "get_sons", []), [IntLiteral("0")])
        name = "power_up"
        args = [FieldAccess(Id("person"), "mom")]
        expect = str(Program([MethCall(receiver, name, args)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))
    
    def test_interface_decl_1(self):
        input = r"""
            type Calculator interface {
                Add(x, y int) int
                Sub(x, y float, z string)
            }
        """
        name = "Calculator"
        mets = [
            Prototype("Add", [IntType(), IntType()], IntType()),
            Prototype("Sub", [FloatType(), FloatType(), StringType()], VoidType())
        ]
        expect = str(Program([InterfaceType(name, mets)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))
    
    def test_interface_decl_2(self):
        input = r"""
            type A interface {
                B(x string, z Person);
                Sub() [3][2]Person;
                Reset();
            };
        """
        name = "A"
        mets = [
            Prototype("B", [StringType(), Id("Person")], VoidType()),
            Prototype("Sub", [], ArrayType([IntLiteral("3"), IntLiteral("2")], Id("Person"))),
            Prototype("Reset", [], VoidType())
        ]
        expect = str(Program([InterfaceType(name, mets)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))
    
    def test_interface_decl_3(self):
        input = r"""
            type ObjectFactory interface {
                MultiInstantiate() [N]Object
                MultiDestroy(objlst [N]Object)
            }
        """
        name = "ObjectFactory"
        mets = [
            Prototype("MultiInstantiate", [], ArrayType([Id("N")], Id("Object"))),
            Prototype("MultiDestroy", [ArrayType([Id("N")], Id("Object"))], VoidType())
        ]
        expect = str(Program([InterfaceType(name, mets)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))
    
    def test_func_decl_1(self):
        input = r"""
            func Average(x, y int) int {
                return (x + y) / 2;
            }
        """
        name = "Average"
        params = [
            ParamDecl("x", IntType()),
            ParamDecl("y", IntType())
        ]
        rettyp = IntType()
        block = Block([Return(
            BinaryOp("/", BinaryOp("+", Id("x"), Id("y")), IntLiteral("2"))
        )])
        expect = str(Program([FuncDecl(name, params, rettyp, block)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))
    
    def test_func_decl_2(self):
        input = r"""
            func Evo(p Person, forward_age int) {
                DestroyAll(p.get_all_aquaintances());
                p.age += forward_age;
            };
        """
        name = "Evo"
        params = [
            ParamDecl("p", Id("Person")),
            ParamDecl("forward_age", IntType())
        ]
        rettyp = VoidType()
        block = Block([
            FuncCall("DestroyAll", [MethCall(Id("p"), "get_all_aquaintances", [])]),
            Assign(FieldAccess(Id("p"), "age"), BinaryOp("+", FieldAccess(Id("p"), "age"), Id("forward_age")))
        ])
        expect = str(Program([FuncDecl(name, params, rettyp, block)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))
    
    def test_func_decl_3(self):
        input = r"""
            func get_random() Object {
                GOD := prayer.summon("Lucifer")
                var obj = GOD.construct_object("truly", "random");
                obj.evilness -= GOD.goodness
                return obj;
            };
        """
        name = "get_random"
        params = []
        rettyp = Id("Object")
        block = Block([
            Assign(Id("GOD"), MethCall(Id("prayer"), "summon", [StringLiteral('"Lucifer"')])),
            VarDecl("obj", None, MethCall(Id("GOD"), "construct_object", [StringLiteral('"truly"'), StringLiteral('"random"')])),
            Assign(FieldAccess(Id("obj"), "evilness"), BinaryOp("-", FieldAccess(Id("obj"), "evilness"), FieldAccess(Id("GOD"), "goodness"))),
            Return(Id("obj"))
        ])
        expect = str(Program([FuncDecl(name, params, rettyp, block)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))
    
    def test_method_decl_1(self):
        input = r"""
            func (p Person) kill(o Object) string {
                p.set_aggressiveness("max")
                o.set_health(0)
                WORLD.disintegrate(o)
                return "successful";
            }
        """
        recname, rectype = "p", Id("Person")
        fname = "kill"
        params = [ParamDecl("o", Id("Object"))]
        rettyp = StringType()
        body = Block([
            MethCall(Id("p"), "set_aggressiveness", [StringLiteral('"max"')]),
            MethCall(Id("o"), "set_health", [IntLiteral("0")]),
            MethCall(Id("WORLD"), "disintegrate", [Id("o")]),
            Return(StringLiteral('"successful"'))
        ])
        funcdecl = FuncDecl(fname, params, rettyp, body)
        expect = str(Program([MethodDecl(recname, rectype, funcdecl)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))
    
    def test_method_decl_2(self):
        input = r"""
            func (calc Calculator) integrate(a, b float, mfunc MathFunc) float {
                var fgraph = mfunc.convert_to("graph").from(a).to(b)
                partitions := fgraph.split_to(1000000)
                values := partitions.to_values("area")
                return Math.sum(values);
            }
        """
        recname, rectype = "calc", Id("Calculator")
        fname = "integrate"
        params = [ParamDecl("a", FloatType()), ParamDecl("b", FloatType()), ParamDecl("mfunc", Id("MathFunc"))]
        rettyp = FloatType()
        body = Block([
            VarDecl("fgraph", None, MethCall(MethCall(MethCall(Id("mfunc"), "convert_to", [StringLiteral('"graph"')]), "from", [Id("a")]), "to", [Id("b")])),
            Assign(Id("partitions"), MethCall(Id("fgraph"), "split_to", [IntLiteral("1000000")])),
            Assign(Id("values"), MethCall(Id("partitions"), "to_values", [StringLiteral('"area"')])),
            Return(MethCall(Id("Math"), "sum", [Id("values")]))
        ])
        funcdecl = FuncDecl(fname, params, rettyp, body)
        expect = str(Program([MethodDecl(recname, rectype, funcdecl)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))
    
    def test_method_decl_3(self):
        input = r"""
            func (a A) b() {
                var x = b()
            }
        """
        recname, rectype = "a", Id("A")
        fname = "b"
        params = []
        rettyp = VoidType()
        body = Block([
            VarDecl("x", None, FuncCall("b", []))
        ])
        funcdecl = FuncDecl(fname, params, rettyp, body)
        expect = str(Program([MethodDecl(recname, rectype, funcdecl)]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))
    
    def test_if_statement_1(self):
        input = r"""
            if (true) {
                a := b
            }
        """
        expect = str(Program([
            If(BooleanLiteral(True), Block([Assign(Id("a"), Id("b"))]), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))
    
    def test_if_statement_2(self):
        input = r"""
            if (persons[0].get_son().name == "Joyce") {
                greet := "Hello, "
                Welt.set_max("hospitality")
                return greet + "Joyce";
            }
        """
        expect = str(Program([
            If(BinaryOp("==", FieldAccess(MethCall(ArrayCell(Id("persons"), [IntLiteral("0")]), "get_son", []), "name"), StringLiteral('"Joyce"')), Block([
                Assign(Id("greet"), StringLiteral('"Hello, "')),
                MethCall(Id("Welt"), "set_max", [StringLiteral('"hospitality"')]),
                Return(BinaryOp("+", Id("greet"), StringLiteral('"Joyce"')))
            ]), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))
    
    def test_if_statement_3(self):
        input = r"""
            if (i < 3) {
                i += 1
                update_counter(i, "warning")
            }
        """
        expect = str(Program([
            If(BinaryOp("<", Id("i"), IntLiteral("3")), Block([
                Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1"))),
                FuncCall("update_counter", [Id("i"), StringLiteral('"warning"')])
            ]), None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))
    
    def test_ifelse_statement_1(self):
        input = r"""
            if (number > 0) {
                print("positive")
            } else {
                print("nonpositive")
            }
        """
        expect = str(Program([
            If(BinaryOp(">", Id("number"), IntLiteral("0")), Block([
                FuncCall("print", [StringLiteral('"positive"')])
            ]), Block([
                FuncCall("print", [StringLiteral('"nonpositive"')])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))
    
    def test_ifelse_statement_2(self):
        input = r"""
            if (wave.collapsed) {
                var electron QuantumState = wave.get_state()
                print(electron.definite_position)
            } else {
                var detector ElectronDetector = Detector{target: wave}
                detector.shoot(NUM_OF_RAYS)
            }
        """
        expect = str(Program([
            If(FieldAccess(Id("wave"), "collapsed"), Block([
                VarDecl("electron", Id("QuantumState"), MethCall(Id("wave"), "get_state", [])),
                FuncCall("print", [FieldAccess(Id("electron"), "definite_position")])
            ]), Block([
                VarDecl("detector", Id("ElectronDetector"), StructLiteral("Detector", [("target", Id("wave"))])),
                MethCall(Id("detector"), "shoot", [Id("NUM_OF_RAYS")])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))
    
    def test_ifelse_statement_3(self):
        input = r"""
            if (false) {
                // this will be skipped
                print("and this won't be printed")
            } else {
                a := Greet{ message: "but this is different" }
                print(a.message + ", because else block's always executed")
            }
        """
        expect = str(Program([
            If(BooleanLiteral(False), Block([
                FuncCall("print", [StringLiteral('"and this won\'t be printed"')])
            ]), Block([
                Assign(Id("a"), StructLiteral("Greet", [("message", StringLiteral('"but this is different"'))])),
                FuncCall("print", [BinaryOp("+", FieldAccess(Id("a"), "message"), StringLiteral('", because else block\'s always executed"'))])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))
    
    def test_elseif_statement_1(self):
        input = r"""
            if (x) {
                return a;
            } else if (y) {
                return b;
            } else {
                return c;
            }
        """
        expect = str(Program([
            If(Id("x"), Block([
                Return(Id("a"))
            ]), If(Id("y"), Block([
                Return(Id("b"))
            ]), Block([
                Return(Id("c"))
            ])))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))
        
    def test_elseif_statement_2(self):
        input = r"""
            if (x) {
                return a;
            } else if (y) {
                return b;
            } else if (z) {
                return c;
            } else if (t) {
                return d;
            }
        """
        expect = str(Program([
            If(Id("x"), Block([
                Return(Id("a"))
            ]), If(Id("y"), Block([
                Return(Id("b"))
            ]), If(Id("z"), Block([
                Return(Id("c"))
            ]), If(Id("t"), Block([
                Return(Id("d"))
            ]), None))))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))
    
    def test_elseif_statement_3(self):
        input = r"""
            if (num == 0.0) {
                print("zero");
            } else if (num < 0.0) {
                print("negative");
            } else {
                print("positive");
            }
        """
        expect = str(Program([
            If(BinaryOp("==", Id("num"), FloatLiteral("0.0")), Block([
                FuncCall("print", [StringLiteral('"zero"')])
            ]), If(BinaryOp("<", Id("num"), FloatLiteral("0.0")), Block([
                FuncCall("print", [StringLiteral('"negative"')])
            ]), Block([
                FuncCall("print", [StringLiteral('"positive"')])
            ])))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))
    
    def test_elseif_statement_4(self):
        input = r"""
            if (mom.arrived) {
                var i int = random(friends.size());
                var hideout = friends[i].find_location("hidden");
                me.hide_at(hideout);
                mom.sight -= 2.7;
            } else if (home.has_friends) {
                me.play_with(friends);
                me.happiness += 2.7;
            }
        """
        expect = str(Program([
            If(FieldAccess(Id("mom"), "arrived"), Block([
                VarDecl("i", IntType(), FuncCall("random", [MethCall(Id("friends"), "size", [])])),
                VarDecl("hideout", None, MethCall(ArrayCell(Id("friends"), [Id("i")]), "find_location", [StringLiteral('"hidden"')])),
                MethCall(Id("me"), "hide_at", [Id("hideout")]),
                Assign(FieldAccess(Id("mom"), "sight"), BinaryOp("-", FieldAccess(Id("mom"), "sight"), FloatLiteral("2.7")))
            ]), If(FieldAccess(Id("home"), "has_friends"), Block([
                MethCall(Id("me"), "play_with", [Id("friends")]),
                Assign(FieldAccess(Id("me"), "happiness"), BinaryOp("+", FieldAccess(Id("me"), "happiness"), FloatLiteral("2.7")))
            ]), None))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))
    
    def test_basic_for_1(self):
        input = r"""
            var i = 0;
            for i < 5 {
                print(i);
                i += 1;
            }
        """
        expect = str(Program([
            VarDecl("i", None, IntLiteral("0")),
            ForBasic(BinaryOp("<", Id("i"), IntLiteral("5")), Block([
                FuncCall("print", [Id("i")]),
                Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1")))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))
    
    def test_basic_for_2(self):
        input = r"""
            for elem != nil {
                if (elem.data == customer.demand) {
                    return elem.data;
                }
                elem := elem.next
            }
        """
        expect = str(Program([
            ForBasic(BinaryOp("!=", Id("elem"), NilLiteral()), Block([
                If(BinaryOp("==", FieldAccess(Id("elem"), "data"), FieldAccess(Id("customer"), "demand")), Block([
                    Return(FieldAccess(Id("elem"), "data"))
                ]), None),
                Assign(Id("elem"), FieldAccess(Id("elem"), "next"))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))
    
    def test_basic_for_3(self):
        input = r"""
            const MAX_POWER = h / 2*PI
            var x int = 3
            var y = 1
            for grid[x][y].power >= MAX_POWER {
                var houses HouseList = GOV.get_house_list()
                var house = houses.get_house_with_policy("lowest power usage")
                power_used := grid[x][y].power_dump(house)
                grid[x][y].power -= power_used
            }
            grid[x][y].owner := nil
        """
        expect = str(Program([
            ConstDecl("MAX_POWER", None, BinaryOp("*", BinaryOp("/", Id("h"), IntLiteral("2")), Id("PI"))),
            VarDecl("x", IntType(), IntLiteral("3")),
            VarDecl("y", None, IntLiteral("1")),
            ForBasic(BinaryOp(">=", FieldAccess(ArrayCell(Id("grid"), [Id("x"), Id("y")]), "power"), Id("MAX_POWER")), Block([
                VarDecl("houses", Id("HouseList"), MethCall(Id("GOV"), "get_house_list", [])),
                VarDecl("house", None, MethCall(Id("houses"), "get_house_with_policy", [StringLiteral('"lowest power usage"')])),
                Assign(Id("power_used"), MethCall(ArrayCell(Id("grid"), [Id("x"), Id("y")]), "power_dump", [Id("house")])),
                Assign(FieldAccess(ArrayCell(Id("grid"), [Id("x"), Id("y")]), "power"), BinaryOp("-", FieldAccess(ArrayCell(Id("grid"), [Id("x"), Id("y")]), "power"), Id("power_used"))),
            ])),
            Assign(FieldAccess(ArrayCell(Id("grid"), [Id("x"), Id("y")]), "owner"), NilLiteral())
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 373))
    
    def test_basic_for_4(self):
        input = r"""
            var i = 0;
            for i < grid.length() {
                var j = 0;
                for j < grid[i].length() {
                    var k = 0;
                    for k < grid[i][j].length() {
                        grid[i][j][k] := MyStruct{name: "string", age: 3};
                    }
                }
            }
        """
        expect = str(Program([
            VarDecl("i", None, IntLiteral("0")),
            ForBasic(BinaryOp("<", Id("i"), MethCall(Id("grid"), "length", [])), Block([
                VarDecl("j", None, IntLiteral("0")),
                ForBasic(BinaryOp("<", Id("j"), MethCall(ArrayCell(Id("grid"), [Id("i")]), "length", [])), Block([
                    VarDecl("k", None, IntLiteral("0")),
                    ForBasic(BinaryOp("<", Id("k"), MethCall(ArrayCell(Id("grid"), [Id("i"), Id("j")]), "length", [])), Block([
                        Assign(ArrayCell(Id("grid"), [Id("i"), Id("j"), Id("k")]), StructLiteral("MyStruct", [("name", StringLiteral('"string"')), ("age", IntLiteral("3"))]))
                    ]))
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 374))
    
    def test_step_for_1(self):
        input = r"""
            for i := 0; i < 100; i += arr[i] {
                j := [3][2]int{{a, 3}, {b, 4}, {c, 5}}
                person.set_list(j)
            }
        """
        expect = str(Program([
            ForStep(Assign(Id("i"), IntLiteral("0")), BinaryOp("<", Id("i"), IntLiteral("100")), Assign(Id("i"), BinaryOp("+", Id("i"), ArrayCell(Id("arr"), [Id("i")]))), Block([
                Assign(Id("j"), ArrayLiteral([IntLiteral("3"), IntLiteral("2")], IntType(), [[Id("a"), IntLiteral("3")], [Id("b"), IntLiteral("4")], [Id("c"), IntLiteral("5")]])),
                MethCall(Id("person"), "set_list", [Id("j")])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 375))
    
    def test_step_for_2(self):
        input = r"""
            for var idx = list.max_size(); idx >= 0; idx -= 1 {
                if (list[idx].name().first() == "John") {
                    print("John " + get_random_name(1), enabled)
                } else if (list[idx] == nil) {
                    print("not exist")
                } else {
                    print("bla")
                }
            }
        """
        expect = str(Program([
            ForStep(VarDecl("idx", None, MethCall(Id("list"), "max_size", [])), BinaryOp(">=", Id("idx"), IntLiteral("0")), Assign(Id("idx"), BinaryOp("-", Id("idx"), IntLiteral("1"))), Block([
                If(BinaryOp("==", MethCall(MethCall(ArrayCell(Id("list"), [Id("idx")]), "name", []), "first", []), StringLiteral('"John"')), Block([
                    FuncCall("print", [BinaryOp("+", StringLiteral('"John "'), FuncCall("get_random_name", [IntLiteral("1")])), Id("enabled")])
                ]), If(BinaryOp("==", ArrayCell(Id("list"), [Id("idx")]), NilLiteral()), Block([
                    FuncCall("print", [StringLiteral('"not exist"')])
                ]),  Block([
                    FuncCall("print", [StringLiteral('"bla"')])
                ])))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))
    
    def test_step_for_3(self):
        input = r"""
            for x := 0; x < 10; x += 1 {
                for y := 0; y < 10; y += 1 {
                    for var z int = 0; z < 10; z += 1 {
                        print(str(Coordinate{x: x, y: y, z: z}));
                        coordinate_list.add([3]float{x, y, z});
                    }
                }
            }
        """
        expect = str(Program([
            ForStep(Assign(Id("x"), IntLiteral("0")), BinaryOp("<", Id("x"), IntLiteral("10")), Assign(Id("x"), BinaryOp("+", Id("x"), IntLiteral("1"))), Block([
                ForStep(Assign(Id("y"), IntLiteral("0")), BinaryOp("<", Id("y"), IntLiteral("10")), Assign(Id("y"), BinaryOp("+", Id("y"), IntLiteral("1"))), Block([
                    ForStep(VarDecl("z", IntType(), IntLiteral("0")), BinaryOp("<", Id("z"), IntLiteral("10")), Assign(Id("z"), BinaryOp("+", Id("z"), IntLiteral("1"))), Block([
                        FuncCall("print", [FuncCall("str", [StructLiteral("Coordinate", [("x", Id("x")), ("y", Id("y")), ("z", Id("z"))])])]),
                        MethCall(Id("coordinate_list"), "add", [ArrayLiteral([IntLiteral("3")], FloatType(), [Id("x"), Id("y"), Id("z")])])
                    ]))
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 377))
    
    def test_step_for_4(self):
        input = r"""
            var root = tree.get_root()
            for var x Node = root; x != nil; x := x.get_next() {
                list := x.get_list().map_to("int")
                load := 0
                for var idx = 0; idx < list.get_size(); idx += 1 {
                    load += list[idx].get_value()
                    Tools.optimize(load)
                }
            }
        """
        expect = str(Program([
            VarDecl("root", None, MethCall(Id("tree"), "get_root", [])),
            ForStep(VarDecl("x", Id("Node"), Id("root")), BinaryOp("!=", Id("x"), NilLiteral()), Assign(Id("x"), MethCall(Id("x"), "get_next", [])), Block([
                Assign(Id("list"), MethCall(MethCall(Id("x"), "get_list", []), "map_to", [StringLiteral('"int"')])),
                Assign(Id("load"), IntLiteral("0")),
                ForStep(VarDecl("idx", None, IntLiteral("0")), BinaryOp("<", Id("idx"), MethCall(Id("list"), "get_size", [])), Assign(Id("idx"), BinaryOp("+", Id("idx"), IntLiteral("1"))), Block([
                    Assign(Id("load"), BinaryOp("+", Id("load"), MethCall(ArrayCell(Id("list"), [Id("idx")]), "get_value", []))),
                    MethCall(Id("Tools"), "optimize", [Id("load")]),
                ])),
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 378))
    
    def test_range_for_1(self):
        input = r"""
            var persons [2]Person = [2]Person{Person{name: "A"}, Person{name: "B"}}
            for i, p := range persons {
                print("No. " + str(i) + ":" + p.get_info() + "\n")
            }
        """
        expect = str(Program([
            VarDecl("persons", ArrayType([IntLiteral("2")], Id("Person")), ArrayLiteral([IntLiteral("2")], Id("Person"), [StructLiteral("Person", [("name", StringLiteral('"A"'))]), StructLiteral("Person", [("name", StringLiteral('"B"'))])])),
            ForEach(Id("i"), Id("p"), Id("persons"), Block([
                FuncCall("print", [BinaryOp("+", BinaryOp("+", BinaryOp("+", BinaryOp("+", StringLiteral('"No. "'), FuncCall("str", [Id("i")])), StringLiteral('":"')), MethCall(Id("p"), "get_info", [])), StringLiteral('"\\n"'))])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 379))
    
    def test_range_for_2(self):
        input = r"""
            for a, b := range c {
                for d, e := range [10]int{1, 2} {
                    if (d != 5) {
                        c[a] := f[d]
                    } else {
                        return c[d[a]];
                    }
                }
            }
        """
        expect = str(Program([
            ForEach(Id("a"), Id("b"), Id("c"), Block([
                ForEach(Id("d"), Id("e"), ArrayLiteral([IntLiteral("10")], IntType(), [IntLiteral("1"), IntLiteral("2")]), Block([
                    If(BinaryOp("!=", Id("d"), IntLiteral("5")), Block([
                        Assign(ArrayCell(Id("c"), [Id("a")]), ArrayCell(Id("f"), [Id("d")]))
                    ]), Block([
                        Return(ArrayCell(Id("c"), [ArrayCell(Id("d"), [Id("a")])]))
                    ]))
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 380))
    
    def test_range_for_3(self):
        input = r"""
            var arr = [2][2]Object{{o11, o12}, {o21, o22}}
            for _, row := range arr {
                for i := 0; i < row.size(); i += 1 {
                    System.notify(row[i])
                    print(System.get_info(row[i], "warning"))
                } 
            }
        """
        expect = str(Program([
            VarDecl("arr", None, ArrayLiteral([IntLiteral("2"), IntLiteral("2")], Id("Object"), [[Id("o11"), Id("o12")], [Id("o21"), Id("o22")]])),
            ForEach(Id("_"), Id("row"), Id("arr"), Block([
                ForStep(Assign(Id("i"), IntLiteral("0")), BinaryOp("<", Id("i"), MethCall(Id("row"), "size", [])), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1"))), Block([
                    MethCall(Id("System"), "notify", [ArrayCell(Id("row"), [Id("i")])]),
                    FuncCall("print", [MethCall(Id("System"), "get_info", [ArrayCell(Id("row"), [Id("i")]), StringLiteral('"warning"')])])
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 381))
    
    def test_range_for_4(self):
        input = r"""
            var A = [3][2]float{{1.3, 2.7}, {3.0, 4.5}, {5.9, 6.2}}
            var B = [2][3]float{{-2.1, 9.9, -0.1}, {7.7, -2.1, 2}}
            var C [3][3]float // C = AB
            for i, rowC := range C {
                for j, colC := range rowC {
                    C[i][j] := 0
                    for k, _ := range A[0] {
                        C[i][j] += A[i][k] * B[k][j]
                    }
                }
            }
        """
        expect = str(Program([
            VarDecl("A", None, ArrayLiteral([IntLiteral("3"), IntLiteral("2")], FloatType(), [[FloatLiteral("1.3"), FloatLiteral("2.7")], [FloatLiteral("3.0"), FloatLiteral("4.5")], [FloatLiteral("5.9"), FloatLiteral("6.2")]])),
            VarDecl("B", None, ArrayLiteral([IntLiteral("2"), IntLiteral("3")], FloatType(), [[UnaryOp("-", FloatLiteral("2.1")), FloatLiteral("9.9"), UnaryOp("-", FloatLiteral("0.1"))], [FloatLiteral("7.7"), UnaryOp("-", FloatLiteral("2.1")), IntLiteral("2")]])),
            VarDecl("C", ArrayType([IntLiteral("3"), IntLiteral("3")], FloatType()), None),
            ForEach(Id("i"), Id("rowC"), Id("C"), Block([
                ForEach(Id("j"), Id("colC"), Id("rowC"), Block([
                    Assign(ArrayCell(Id("C"), [Id("i"), Id("j")]), IntLiteral("0")),
                    ForEach(Id("k"), Id("_"), ArrayCell(Id("A"), [IntLiteral("0")]), Block([
                        Assign(ArrayCell(Id("C"), [Id("i"), Id("j")]), BinaryOp("+", ArrayCell(Id("C"), [Id("i"), Id("j")]), BinaryOp("*", ArrayCell(Id("A"), [Id("i"), Id("k")]), ArrayCell(Id("B"), [Id("k"), Id("j")]))))
                    ]))
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 382))
    
    def test_complex_if_for_1(self):
        input = r"""
            var arr = [2][2]Object{{o11, o12}, {o21, o22}}
            for _, row := range arr {
                for i := 0; i < row.size(); i += 1 {
                    System.notify(row[i])
                    print(System.get_info(row[i], "warning"))
                } 
            }
        """
        expect = str(Program([
            VarDecl("arr", None, ArrayLiteral([IntLiteral("2"), IntLiteral("2")], Id("Object"), [[Id("o11"), Id("o12")], [Id("o21"), Id("o22")]])),
            ForEach(Id("_"), Id("row"), Id("arr"), Block([
                ForStep(Assign(Id("i"), IntLiteral("0")), BinaryOp("<", Id("i"), MethCall(Id("row"), "size", [])), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1"))), Block([
                    MethCall(Id("System"), "notify", [ArrayCell(Id("row"), [Id("i")])]),
                    FuncCall("print", [MethCall(Id("System"), "get_info", [ArrayCell(Id("row"), [Id("i")]), StringLiteral('"warning"')])])
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 383))
    
    def test_complex_if_for_2(self):
        input = r"""
            for i := 1; i <= 10; i += 1 {
                for var j int = 1; j <= 5; j := j + 1 {
                    if ((i * j) % 2 == 0) {
                        print("even product: ", i * j)
                    } else {
                        print ("odd product: ", i * j)
                    }
                }
            }
        """
        expect = str(Program([
            ForStep(Assign(Id("i"), IntLiteral("1")), BinaryOp("<=", Id("i"), IntLiteral("10")), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1"))), Block([
                ForStep(VarDecl("j", IntType(), IntLiteral("1")), BinaryOp("<=", Id("j"), IntLiteral("5")), Assign(Id("j"), BinaryOp("+", Id("j"), IntLiteral("1"))), Block([
                    If(BinaryOp("==", BinaryOp("%", BinaryOp("*", Id("i"), Id("j")), IntLiteral("2")), IntLiteral("0")), Block([
                        FuncCall("print", [StringLiteral('"even product: "'), BinaryOp("*", Id("i"), Id("j"))])
                    ]), Block([
                        FuncCall("print", [StringLiteral('"odd product: "'), BinaryOp("*", Id("i"), Id("j"))])
                    ]))
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 384))
    
    def test_complex_if_for_3(self):
        input = r"""
            for i := 10; i >= 1; i -= 1 {
                if (i % 2 == 0 || i % 3 == 0) {
                    print("condition met for: ", i)
                    break
                } else {
                    print("skipping: ", i)
                }
            }
        """
        expect = str(Program([
            ForStep(Assign(Id("i"), IntLiteral("10")), BinaryOp(">=", Id("i"), IntLiteral("1")), Assign(Id("i"), BinaryOp("-", Id("i"), IntLiteral("1"))), Block([
                If(BinaryOp("||", BinaryOp("==", BinaryOp("%", Id("i"), IntLiteral("2")), IntLiteral("0")), BinaryOp("==", BinaryOp("%", Id("i"), IntLiteral("3")), IntLiteral("0"))), Block([
                    FuncCall("print", [StringLiteral('"condition met for: "'), Id("i")]),
                    Break()
                ]), Block([
                    FuncCall("print", [StringLiteral('"skipping: "'), Id("i")])
                ]))
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))
    
    def test_complex_if_for_4(self):
        input = r"""
            var words = [5]string{"apple", "banana", "cherry", "date", "fig"}
            for _, word := range words {
                if (word == "cherry") {
                    print("Found cherry!")
                    break
                }
                print("Current word: ", word)
            }
        """
        expect = str(Program([
            VarDecl("words", None, ArrayLiteral([IntLiteral("5")], StringType(), [StringLiteral('"apple"'), StringLiteral('"banana"'), StringLiteral('"cherry"'), StringLiteral('"date"'), StringLiteral('"fig"')])),
            ForEach(Id("_"), Id("word"), Id("words"), Block([
                If(BinaryOp("==", Id("word"), StringLiteral('"cherry"')), Block([
                    FuncCall("print", [StringLiteral('"Found cherry!"')]),
                    Break()
                ]), None),
                FuncCall("print", [StringLiteral('"Current word: "'), Id("word")])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 386))
    
    def test_complex_program_1(self):
        input = r"""
            type Student struct {
                name string;
                age int;
            }
            func (s Student) greet() string {
                return "I am " + s.name;
            }
            var students = [3]Student{
                Student{name: "Minh", age: 22},
                Student{name: "Lan", age: 21},
                Student{name: "Tran", age: 18}
            }
            for _, student := range students {
                print(student.name, " is ", student.age, " years old.")
                print(student.greet())
            }
        """
        expect = str(Program([
            StructType("Student", [("name", StringType()), ("age", IntType())], []),
            MethodDecl("s", Id("Student"), FuncDecl("greet", [], StringType(), Block([
                Return(BinaryOp("+", StringLiteral('"I am "'), FieldAccess(Id("s"), "name")))
            ]))),
            VarDecl("students", None, ArrayLiteral([IntLiteral("3")], Id("Student"), [
                StructLiteral("Student", [("name", StringLiteral('"Minh"')), ("age", IntLiteral("22"))]),
                StructLiteral("Student", [("name", StringLiteral('"Lan"')), ("age", IntLiteral("21"))]),
                StructLiteral("Student", [("name", StringLiteral('"Tran"')), ("age", IntLiteral("18"))])
            ])),
            ForEach(Id("_"), Id("student"), Id("students"), Block([
                FuncCall("print", [FieldAccess(Id("student"), "name"), StringLiteral('" is "'), FieldAccess(Id("student"), "age"), StringLiteral('" years old."')]),
                FuncCall("print", [MethCall(Id("student"), "greet", [])])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))
    
    def test_complex_program_2(self):
        input = r"""
            const TEAM_MAX_SIZE = 18
            type Team struct {
                name string
                players [TEAM_MAX_SIZE]Player
            }
            func (t Team) get_player(idx int) Player {
                return t.players[idx];
            }
            func (t Team) kill_all() {
                for _, player := range t.players {
                    player.die(1000)
                }
            }
        """
        expect = str(Program([
            ConstDecl("TEAM_MAX_SIZE", None, IntLiteral("18")),
            StructType("Team", [
                ("name", StringType()),
                ("players", ArrayType([Id("TEAM_MAX_SIZE")], Id("Player")))
            ], []),
            MethodDecl("t", Id("Team"), FuncDecl("get_player", [ParamDecl("idx", IntType())], Id("Player"), Block([
                Return(ArrayCell(FieldAccess(Id("t"), "players"), [Id("idx")]))
            ]))),
            MethodDecl("t", Id("Team"), FuncDecl("kill_all", [], VoidType(), Block([
                ForEach(Id("_"), Id("player"), FieldAccess(Id("t"), "players"), Block([
                    MethCall(Id("player"), "die", [IntLiteral("1000")])
                ]))
            ])))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))
    
    def test_complex_program_3(self):
        input = r"""
            var matrix = [3][3]int{
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
            };
            rows := len(matrix);
            var transposed [3][3]int;
            for var i int = 0; i < rows; i += 1 {
                for j, _ := range matrix[i] {
                    transposed[j][i] := matrix[i][j];
                }
            }
            for _, row := range transposed {
                print(row)
            }
        """
        expect = str(Program([
            VarDecl("matrix", None, ArrayLiteral([IntLiteral("3"), IntLiteral("3")], IntType(), [
                [IntLiteral("1"), IntLiteral("2"), IntLiteral("3")],
                [IntLiteral("4"), IntLiteral("5"), IntLiteral("6")],
                [IntLiteral("7"), IntLiteral("8"), IntLiteral("9")],
            ])),
            Assign(Id("rows"), FuncCall("len", [Id("matrix")])),
            VarDecl("transposed", ArrayType([IntLiteral("3"), IntLiteral("3")], IntType()), None),
            ForStep(VarDecl("i", IntType(), IntLiteral("0")), BinaryOp("<", Id("i"), Id("rows")), Assign(Id("i"), BinaryOp("+", Id("i"), IntLiteral("1"))), Block([
                ForEach(Id("j"), Id("_"), ArrayCell(Id("matrix"), [Id("i")]), Block([
                    Assign(ArrayCell(Id("transposed"), [Id("j"), Id("i")]), ArrayCell(Id("matrix"), [Id("i"), Id("j")])),
                ])),
            ])),
            ForEach(Id("_"), Id("row"), Id("transposed"), Block([
                FuncCall("print", [Id("row")])
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))
    
    def test_complex_program_4(self):
        input = r"""
            type Point3D struct {
                x float; y float; z float;
            };
            func (point Point3D) distance(other Point3D) float {
                var dx = abs(point.x - other.x);
                var dy = abs(point.y - other.y);
                var dz = abs(point.z - other.z);
                return sqrt(dx * dx + dy * dy + dz * dz);
            }
            func (point Point3D) move(dx, dy, dz float) Point3D {
                point.x += dx
                point.y += dy
                point.z += dz
                return point;
            }
            var p = Point3D{x: 2.3, y: -1.0, z: 0.2}
            print(p.move(1, 2, 3).distance(p))
        """
        expect = str(Program([
            StructType("Point3D", [("x", FloatType()), ("y", FloatType()), ("z", FloatType())], []),
            MethodDecl("point", Id("Point3D"), FuncDecl("distance", [ParamDecl("other", Id("Point3D"))], FloatType(), Block([
                VarDecl("dx", None, FuncCall("abs", [BinaryOp("-", FieldAccess(Id("point"), "x"), FieldAccess(Id("other"), "x"))])),
                VarDecl("dy", None, FuncCall("abs", [BinaryOp("-", FieldAccess(Id("point"), "y"), FieldAccess(Id("other"), "y"))])),
                VarDecl("dz", None, FuncCall("abs", [BinaryOp("-", FieldAccess(Id("point"), "z"), FieldAccess(Id("other"), "z"))])),
                Return(FuncCall("sqrt", [BinaryOp("+", BinaryOp("+", BinaryOp("*", Id("dx"), Id("dx")), BinaryOp("*", Id("dy"), Id("dy"))), BinaryOp("*", Id("dz"), Id("dz")))])),
            ]))),
            MethodDecl("point", Id("Point3D"), FuncDecl("move", [ParamDecl("dx", FloatType()), ParamDecl("dy", FloatType()), ParamDecl("dz", FloatType())], Id("Point3D"), Block([
                Assign(FieldAccess(Id("point"), "x"), BinaryOp("+", FieldAccess(Id("point"), "x"), Id("dx"))),
                Assign(FieldAccess(Id("point"), "y"), BinaryOp("+", FieldAccess(Id("point"), "y"), Id("dy"))),
                Assign(FieldAccess(Id("point"), "z"), BinaryOp("+", FieldAccess(Id("point"), "z"), Id("dz"))),
                Return(Id("point")),
            ]))),
            VarDecl("p", None, StructLiteral("Point3D", [("x", FloatLiteral("2.3")), ("y", UnaryOp("-", FloatLiteral("1.0"))), ("z", FloatLiteral("0.2"))])),
            FuncCall("print", [MethCall(MethCall(Id("p"), "move", [IntLiteral("1"), IntLiteral("2"), IntLiteral("3")]), "distance", [Id("p")])])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 390))
    
    def test_complex_program_5(self):
        input = r"""
            func fibo(n int, cache [100]int) int {
                if (n <= 1) {
                    return n;
                }
                if (cache[n] != nil) {
                    return cache[n];
                }
                cache[n] := fibo(n - 1, cache) + fibo(n - 2, cache)
                return cache[n];
            }
            var n = 10
            var cache [100]int
            print(fibo(50, cache))
        """
        expect = str(Program([
            FuncDecl("fibo", [ParamDecl("n", IntType()), ParamDecl("cache", ArrayType([IntLiteral("100")], IntType()))], IntType(), Block([
                If(BinaryOp("<=", Id("n"), IntLiteral("1")), Block([
                    Return(Id("n")),
                ]), None),
                If(BinaryOp("!=", ArrayCell(Id("cache"), [Id("n")]), NilLiteral()), Block([
                    Return(ArrayCell(Id("cache"), [Id("n")])),
                ]), None),
                Assign(ArrayCell(Id("cache"), [Id("n")]), BinaryOp("+", FuncCall("fibo", [BinaryOp("-", Id("n"), IntLiteral("1")), Id("cache")]), FuncCall("fibo", [BinaryOp("-", Id("n"), IntLiteral("2")), Id("cache")]))),
                Return(ArrayCell(Id("cache"), [Id("n")])), 
            ])),
            VarDecl("n", None, IntLiteral("10")),
            VarDecl("cache", ArrayType([IntLiteral("100")], IntType()), None),
            FuncCall("print", [FuncCall("fibo", [IntLiteral("50"), Id("cache")])]),
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 391))
    
    def test_complex_program_6(self):
        input = r"""
            type Shape interface {
                area() float;
                perimeter() float;
            }
            type Circle struct {
                radius float;
                x float;
                y float;
            }
            func create_circle(r, x, y float) Circle {
                var circle = Circle{radius: r, x: x, y: y};
                return circle;
            }
            func (c Circle) area() float {
                var r = c.radius;
                return PI * r * r;
            }
            func (c Circle) perimeter() float {
                var r = c.radius;
                return 2 * PI * r;
            }
            test_circle := create_circle(3, 0, 0);
            print("Area: ", test_circle.area(), " - Perimeter: ", test_circle.perimeter())
         """
        expect = str(Program([
            InterfaceType("Shape", [Prototype("area", [], FloatType()), Prototype("perimeter", [], FloatType())]),
            StructType("Circle", [("radius", FloatType()), ("x", FloatType()), ("y", FloatType())], []),
            FuncDecl("create_circle", [ParamDecl("r", FloatType()), ParamDecl("x", FloatType()), ParamDecl("y", FloatType())], Id("Circle"), Block([
                VarDecl("circle", None, StructLiteral("Circle", [("radius", Id("r")), ("x", Id("x")), ("y", Id("y"))])),
                Return(Id("circle")),
            ])),
            MethodDecl("c", Id("Circle"), FuncDecl("area", [], FloatType(), Block([
                VarDecl("r", None, FieldAccess(Id("c"), "radius")),
                Return(BinaryOp("*", BinaryOp("*", Id("PI"), Id("r")), Id("r"))),
            ]))),
            MethodDecl("c", Id("Circle"), FuncDecl("perimeter", [], FloatType(), Block([
                VarDecl("r", None, FieldAccess(Id("c"), "radius")),
                Return(BinaryOp("*", BinaryOp("*", IntLiteral("2"), Id("PI")), Id("r"))),
            ]))),
            Assign(Id("test_circle"), FuncCall("create_circle", [IntLiteral("3"), IntLiteral("0"), IntLiteral("0")])),
            FuncCall("print", [StringLiteral('"Area: "'), MethCall(Id("test_circle"), "area", []), StringLiteral('" - Perimeter: "'), MethCall(Id("test_circle"), "perimeter", [])])
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 392))
    