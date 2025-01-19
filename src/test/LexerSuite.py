import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
      
    def test_fully_single_line_comment(self):
        input = "var1// abc123!@# \nvar2";
        expect = "var1,var2,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input ,expect, 1));
        
    def test_only_one_single_line_comment(self):
        input = "//\"098?';";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 2));
    
    def test_empty_single_line_comment(self):
        input = "//";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 3));
    
    def test_many_slashes_single_line_comment(self):
        input = "/////// /// ///// // /// /";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 4));
    
    def test_fully_multi_line_comment(self):
        input = "var1 /* &*()*&^ \n ?><Kj \n ASD */ var2";
        expect = "var1,var2,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 5));
    
    def test_only_one_multi_line_comment(self):
        input = "/* random text () */";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 6));
    
    def test_empty_multi_line_comment(self):
        input = "/**/";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 7));
    
    def test_nested_multi_line_comment(self):
        input = "/* out1 /* out2 /* out3 */ out2 */ out3 */"
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 8));
    
    def test_opened_multi_line_comment(self):
        input = "/* out1 ";
        expect = "ErrorToken /";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 9));
    
    def test_opened_nested_multi_line_comment(self):
        # ambiguity: nested comments are necessarily closed?
        input = "/* outer /* inner */";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 10))
    
    def test_mixed_types_of_comment(self):
        input = "// first line \n/* second line: outer /* inner */ \nthird line */// continue third line";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 11));