import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):

    def test_simple_program(self):
        """Simple program: void main() {} """
        input = """func main() {};"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))

    def test_more_complex_program(self):
        """More complex program"""
        input = """func foo () {
        };"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
    
    def test_wrong_miss_close(self):
        """Miss ) void main( {}"""
        input = """func main({};"""
        expect = "Error on line 1 col 11: {"
        self.assertTrue(TestParser.checkParser(input,expect,203))
    
    def test_wrong_variable(self):
        input = """var int;"""
        expect = "Error on line 1 col 5: int"
        self.assertTrue(TestParser.checkParser(input,expect,204))
    
    def test_wrong_index(self):
        input = """var i ;"""
        expect = "Error on line 1 col 7: ;"
        self.assertTrue(TestParser.checkParser(input,expect,205))
    
    def test_var_declaration_1(self):
        input = """var _forbbiden = 3 + 1.23e-2 * 10;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,206))
    
    def test_var_declaration_2(self):
        input = """var i int = 0b00101;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,207))
    
    def test_var_declaration_3(self):
        input = """var i float"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,208))
    
    def test_var_declaration_4(self):
        input = """
            var str string = "welcome";
            var _i boolean = false
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,209))
    
    def test_var_declaration_5(self):
        input = """var i = ("string" + 0xffFa) - 1.2e3;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,210))
    
    def test_var_declaration_6(self):
        input = """
            const Pi = 3.14e0
            const E = 2.71111111
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,211))
    
    def test_var_declaration_7(self):
        input = """
            const GREET = "welcome";
            const size = 10000 - 33;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,212))
    
    def test_var_declaration_8(self):
        input = """
            const e = 2.7;
            var flow float = 3 * (12 / (1 + e)) - e % 3;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,213))
    
    def test_var_declaration_9(self):
        input = """var f boolean = true;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,214))
    
    def test_var_declaration_10(self):
        input = """
            var dummy = 30.22E-5;
            const Construct = dummy * 1.0e5;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,215))
    
    def test_assignment_1(self):
        input = """
            var x int = 0;
            x := 1;
            x += 3;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,216))
    
    def test_assignment_2(self):
        input = """
            person.age += 10;
            person.complex *= calculator.compute(person.config);
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,217))
    
    def test_assignment_3(self):
        input = """
            var arr [2][1]float;
            arr := [2][1]float{ {3.0}, {1.2e-3} };
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,218))
    
    def test_assignment_4(self):
        input = """
            remainder /= int_part * frac_part;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,219))
    
    def test_assignment_5(self):
        input = """
            var a int
            a := 10
            a %= (a + 2) * 3 - (2 / (1 - e))
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,220))
    
    def test_assignment_6(self):
        input = """
            test_array[3 * i] := true_array[2 - i] * 2
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,221))
    
    def test_assignment_7(self):
        input = """
            curve.length += 1
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,222))
    
    def test_assignment_8(self):
        input = """
            curve.length += (4 * (7 - 3) / 2) - 3 * (1 + 2)
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,223))
    
    def test_assignment_9(self):
        input = """
            var x int = 0;
            x := 1;
            x += 3;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,224))
    
    def test_assignment_10(self):
        input = """
            var x int = 0;
            x := 1;
            x += 3;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,225))