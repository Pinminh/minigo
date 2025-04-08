import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
      
    def test_fully_single_line_comment(self):
        input = "var1// abc123!@# \nvar2";
        expect = "var1,var2,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 101));
        
    def test_only_one_single_line_comment(self):
        input = "//\"098?';";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 102));
    
    def test_empty_single_line_comment(self):
        input = "//";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 103));
    
    def test_many_slashes_single_line_comment(self):
        input = "/////// /// ///// // /// /";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 104));
    
    def test_fully_multi_line_comment(self):
        input = "var1 /* &*()*&^ \n ?><Kj \n ASD */ var2";
        expect = "var1,var2,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 105));
    
    def test_only_one_multi_line_comment(self):
        input = "/* random text () */";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 106));
    
    def test_empty_multi_line_comment(self):
        input = "/**/";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 107));
    
    def test_nested_multi_line_comment(self):
        input = "/* out1 /* out2 /* out3 */ out2 */ out3 */"
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 108));
    
    def test_opened_multi_line_comment(self):
        input = "/* out1 ";
        expect = "/,*,out1,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 109));
    
    def test_opened_nested_multi_line_comment(self):
        # ambiguity: nested comments are necessarily closed?
        input = "/* outer /* inner */";
        expect = "<EOF>";
        # expect = "Error Token /"; // for the case of unallowed 
        self.assertTrue(TestLexer.checkLexeme(input, expect, 110))
    
    def test_mixed_types_of_comment(self):
        input = "// first line \n/* second line: outer /* inner */ \nthird line */// continue third line";
        expect = "<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 111));
    
    def test_valid_identifier_1(self):
        input = "_ _var_0 A_ fvar11";
        expect = "_,_var_0,A_,fvar11,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 112));
        
    def test_valid_identifier_2(self):
        input = "tothe____moonAndB4ackstillLoveYou"
        expect = "tothe____moonAndB4ackstillLoveYou,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 113));

    def test_valid_identifier_3(self):
        input = "i_tlikeNothingHASchanged123560"
        expect = "i_tlikeNothingHASchanged123560,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 114));

    def test_valid_identifier_4(self):
        input = "s1235__justLIKETHIS"
        expect = "s1235__justLIKETHIS,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 115));

    def test_valid_identifier_5(self):
        input = "aBBBFFWQETYx123_5869"
        expect = "aBBBFFWQETYx123_5869,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input, expect, 116));
        
    def test_valid_identifier_6(self):
        input = "430hello";
        expect = "430,hello,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 117));
        
    def test_valid_identifier_7(self):
        input = "\t__var__\n";
        expect = "__var__,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 118));
    
    def test_invalid_identifier_1(self):
        input = "aa?12abb";
        expect = "aa,ErrorToken ?";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 119));
    
    def test_invalid_identifier_2(self):
        input = "first@@@second";
        expect = "first,ErrorToken @";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 120));
    
    def test_invalid_identifier_3(self):
        input = "!aa?12ab!b";
        expect = "!,aa,ErrorToken ?";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 121));
    
    def test_invalid_identifier_4(self):
        input = "_var_1 `thisfunc";
        expect = "_var_1,ErrorToken `";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 122));
    
    def test_invalid_identifier_5(self):
        input = "/\\jjj_1";
        expect = "/,ErrorToken \\";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 123));
    
    def test_invalid_identifier_6(self):
        input = "mmm_ mbb^";
        expect = "mmm_,mbb,ErrorToken ^";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 124));
    
    def test_invalid_identifier_7(self):
        input = "/\\aaaaa00000";
        expect = "/,ErrorToken \\";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 125));
    
    def test_intlit_decimal_1(self):
        input = "0 1 2 3 4 5 6 7 8 9";
        expect = "0,1,2,3,4,5,6,7,8,9,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 126));
    
    def test_intlit_decimal_2(self):
        input = "000123";
        expect = "000,123,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 127));
    
    def test_intlit_decimal_3(self):
        input = "13002 0 0001";
        expect = "13002,0,000,1,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 128));
    
    def test_intlit_decimal_4(self):
        input = "302 176 293391";
        expect = "302,176,293391,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 129));
    
    def test_intlit_decimal_5(self):
        input = "00100100100";
        expect = "00,100100100,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 130));
    
    def test_intlit_binary_1(self):
        input = "0 1 2 3 4 5 6 7 8 9";
        expect = "0,1,2,3,4,5,6,7,8,9,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 131));
    
    def test_intlit_binary_2(self):
        input = "0 12 0b000";
        expect = "0,12,0b000,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 132));
    
    def test_intlit_binary_3(self):
        input = "0B11110 0b1111";
        expect = "0B11110,0b1111,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 133));
    
    def test_intlit_binary_4(self):
        input = "0001200 0000B0011";
        expect = "000,1200,0000,B0011,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 134));
    
    def test_intlit_binary_5(self):
        input = "0b0B0b 0b33";
        expect = "0b0,B0b,0,b33,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 135));
    
    def test_intlit_octal_1(self):
        input = "113 0o991";
        expect = "113,0,o991,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 136));
    
    def test_intlit_octal_2(self):
        input = "0O1234567";
        expect = "0O1234567,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 137));
    
    def test_intlit_octal_3(self):
        input = "0000120o2130b01";
        expect = "0000,120,o2130b01,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 138));
    
    def test_intlit_octal_4(self):
        input = "0O2781 0o777";
        expect = "0O27,81,0o777,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 139));
    
    def test_intlit_octal_5(self):
        input = "0O0O0o";
        expect = "0O0,O0o,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 140));
    
    def test_intlit_hexa_1(self):
        input = "0x12345679abcdefABCDEF";
        expect = "0x12345679abcdefABCDEF,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 141));
    
    def test_intlit_hexa_2(self):
        input = "0X1Aafe 0xaaFFFEEec1";
        expect = "0X1Aafe,0xaaFFFEEec1,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 142));
    
    def test_intlit_hexa_3(self):
        input = "0xX000XXxxx1Aaff";
        expect = "0,xX000XXxxx1Aaff,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 143));
    
    def test_intlit_hexa_4(self):
        input = "99 0B101 0b1 0o7 0x123AAa 0X99CddD";
        expect = "99,0B101,0b1,0o7,0x123AAa,0X99CddD,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 144));
    
    def test_intlit_hexa_5(self):
        input = "0000000000X1A";
        expect = "0000000000,X1A,<EOF>";
        self.assertTrue(TestLexer.checkLexeme(input, expect, 145));
    
    def test_floatlit_only_int_1(self):
        input = "123."
        expect = "123.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,146))

    def test_floatlit_only_int_2(self):
        input = "000301."
        expect = "000301.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,147))

    def test_floatlit_only_int_3(self):
        input = "044."
        expect = "044.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,148))

    def test_floatlit_only_int_4(self):
        input = "."
        expect = ".,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,149))

    def test_floatlit_only_int_5(self):
        input = "169."
        expect = "169.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,150))
    
    def test_floatlit_only_frac_1(self):
        input = "169.123"
        expect = "169.123,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,151))
    
    def test_floatlit_only_frac_2(self):
        input = ".123"
        expect = ".,123,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,152))
    
    def test_floatlit_only_frac_3(self):
        input = "00.0000"
        expect = "00.0000,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,153))
    
    def test_floatlit_only_frac_4(self):
        input = "0.00001.123"
        expect = "0.00001,.,123,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,154))
    
    def test_floatlit_only_frac_5(self):
        input = "0.00001."
        expect = "0.00001,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,155))
    
    def test_floatlit_full_1(self):
        """float"""
        input = "12E"
        expect = "12,E,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,156))

    def test_floatlit_full_2(self):
        """float"""
        input = "11..111.0e-222"
        expect = "11.,.,111.0e-222,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,157))

    def test_floatlit_full_3(self):
        """float"""
        input = ".11-E11"
        expect = ".,11,-,E11,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,158))

    def test_floatlit_full_4(self):
        """float"""
        input = "123.45F67"
        expect = "123.45,F67,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,159))

    def test_floatlit_full_5(self):
        """float"""
        input = "0000.0000E+0000"
        expect = "0000.0000E+0000,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,160))

    def test_stringlit_1(self):
        """escape string"""
        input = r'''" \\n Hello \\n \\f \\t"'''
        expect = r'''" \\n Hello \\n \\f \\t",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,161))

    def test_stringlit_2(self):
        input='" hello, world "'
        expect = r'''" hello, world ",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,162))

    def test_stringlit_3(self):
        input = r'''""'''
        expect = r'''"",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,163))

    def test_stringlit_4(self):
        input = r'''"""wow"'''
        expect = r'''"","wow",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,164))

    def test_stringlit_5(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,165))

    def test_stringlit_6(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,166))

    def test_stringlit_7(self):
        input = r'''" something just like this \\t huh!!'''
        expect = r'''Unclosed string: " something just like this \\t huh!!'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,167))

    def test_stringlit_8(self):
        input = r'''"""im not completed!""'''
        expect = r'''"","im not completed!",Unclosed string: "'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,168))

    def test_stringlit_9(self):
        input = '" string";'
        expect = '" string",;,<EOF>'
        self.assertTrue(TestLexer.checkLexeme(input,expect,169))

    def test_stringlit_10(self):
        input = r'"Wrong escape: \x";'
        expect = r'''Illegal escape in string: "Wrong escape: \x'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,170))

    def test_stringlit_11(self):
        input = r'"Escapes: \b \t \g \"'
        expect = r'''Illegal escape in string: "Escapes: \b'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,171))

    def test_stringlit_12(self):
        input = r'''"w **x** v"'''
        expect = r'''"w **x** v",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,172))

    def test_stringlit_13(self):
        input = r'''**w "tu" h**'''
        expect = r'''*,*,w,"tu",h,*,*,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,173))

    def test_stringlit_14(self):
        input = r'"Wrong Escape: \"'
        expect = r'''Unclosed string: "Wrong Escape: \"'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,174))

    def test_stringlit_15(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,175))
    
    def test_combination_1(self):
        input = 'me("and") + you("are", not) && 111;'
        expect = 'me,(,"and",),+,you,(,"are",,,not,),&&,111,;,<EOF>'
        self.assertTrue(TestLexer.checkLexeme(input,expect,176))

    def test_combination_2(self):
        input = r'''me = you = someone * 123 - 3.14'''
        expect = r'''me,=,you,=,someone,*,123,-,3.14,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,177))

    def test_combination_3(self):
        """for loop"""
        input = 'For (i=0, i<69,1) Do \n j = j + 1; \n EndFor.'
        expect = 'For,(,i,=,0,,,i,<,69,,,1,),Do,j,=,j,+,1,;,EndFor,.,<EOF>'
        self.assertTrue(TestLexer.checkLexeme(input,expect,178))

    def test_combination_4(self):
        input = r'''a[4[5]] = b[c[6][7][8]];'''
        expect = r'''a,[,4,[,5,],],=,b,[,c,[,6,],[,7,],[,8,],],;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,179))

    def test_combination_5(self):
        input = ''
        expect = '<EOF>'
        self.assertTrue(TestLexer.checkLexeme(input,expect,180))

    def test_combination_6(self):
        input = r'''Var: a, b = 1,2,3,4;'''
        expect = r'''Var,:,a,,,b,=,1,,,2,,,3,,,4,;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,181))

    def test_combination_7(self):
        input = 'abc123\\n;'
        expect = 'abc123,ErrorToken \\'
        self.assertTrue(TestLexer.checkLexeme(input,expect,182))

    def test_combination_8(self):
        input = '  \t  \t'
        expect = '<EOF>'
        self.assertTrue(TestLexer.checkLexeme(input,expect,183))

    def test_combination_9(self):
        input = r'''123123_2591029WEQSD1.45E2'''
        expect = r'''123123,_2591029WEQSD1,.,45,E2,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,184))

    def test_combination_10(self):
        input = r'''5sadqwrE8.1E4GG1392ASdjwoiqjr'''
        expect = r'''5,sadqwrE8,.,1,E4GG1392ASdjwoiqjr,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,185))

    def test_combination_11(self):
        input = r'''1ytr=1234xxx;'''
        expect = r'''1,ytr,=,1234,xxx,;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,186))

    def test_combination_12(self):
        input = r'''2..3467.22'''
        expect = r'''2.,.,3467.22,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,187))

    def test_combination_13(self):
        input = r'''[1][2][3][[4][5]]'''
        expect = r'''[,1,],[,2,],[,3,],[,[,4,],[,5,],],<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,188))

    def test_combination_14(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,189))

    def test_combination_15(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,190))

    def test_combination_16(self):
        input = r'''-1,-1.111'''
        expect = r'''-,1,,,-,1.111,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,191))

    def test_combination_17(self):
        input = r''''''
        expect = r'''<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,192))
    
    def test_combination_18(self):
        input=r'''Var: a_B=0E90, do = 0X90;'''
        expect=r'''Var,:,a_B,=,0,E90,,,do,=,0X90,;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,193))

    def test_combination_19(self):
        input=r'''hh + 0000 >= 12.E00 - True;'''
        expect=r'''hh,+,0000,>=,12.E00,-,True,;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,194))

    def test_combination_20(self):
        input=r'''True False true false TRUE FALSE '''
        expect=r'''True,False,true,false,TRUE,FALSE,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,195))
    
    def test_statement_1(self):
        input=r'''var __name__ string = "hello string"'''
        expect=r'''var,__name__,string,=,"hello string",<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,196))
    
    def test_statement_2(self):
        input=r'''for i := 0, i <= 10, i += 2 { person.eat(breakfast) }'''
        expect=r'''for,i,:=,0,,,i,<=,10,,,i,+=,2,{,person,.,eat,(,breakfast,),},<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,197))
    
    def test_statement_3(self):
        input=r'''var arr [2][2]int = [2][2]int{ {1, 2}, {3, 4} };'''
        expect=r'''var,arr,[,2,],[,2,],int,=,[,2,],[,2,],int,{,{,1,,,2,},,,{,3,,,4,},},;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,198))
    
    def test_statement_4(self):
        input=r'''type Person struct { name string; };'''
        expect=r'''type,Person,struct,{,name,string,;,},;,<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,199))
    
    def test_statement_5(self):
        input=r'''func eval(value int) int { return value; }'''
        expect=r'''func,eval,(,value,int,),int,{,return,value,;,},<EOF>'''
        self.assertTrue(TestLexer.checkLexeme(input,expect,200))