from unittest import TestCase

from slimit.parser import Parser

from jsard.core import deobfuscate, scan_obfuscation_array


# noinspection PyPep8Naming
class Test_deobfuscate(TestCase):
    def test_expression(self):
        """Obfuscation with parent node `ExprStatement`."""
        obfuscated = 'var _0x01ff=["foo"];_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            '"foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_var_declaration(self):
        """Obfuscation with parent node `VarDecl`."""
        obfuscated = 'var _0x01ff=["foo"];var a=_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'var a = "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_assignment(self):
        """Obfuscation with parent node `Assign`."""
        obfuscated = 'var _0x01ff=["foo"];var a;a=_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'var a;\n'
            'a = "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_array(self):
        """Obfuscation with parent node `Array`."""
        obfuscated = 'var _0x01ff=["foo"];var a=[9,_0x01ff[0],7];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'var a = [9,"foo",7];')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_array_access(self):
        """Obfuscation with parent node `BracketAccessor`."""
        obfuscated = 'var _0x01ff=["foo", 0, 1];var a=_0x01ff[_0x01ff[_0x01ff[2]]];'
        expected = (
            'var _0x01ff = ["foo",0,1];\n'
            'var a = "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_conditional(self):
        """Obfuscation with parent node `Conditional`."""
        obfuscated = 'var _0x01ff=["foo"];_0x01ff[0]?true:false;'
        expected = (
            'var _0x01ff = ["foo"];\n'
            '"foo" ? true : false;')
        self.assertEqual(expected, deobfuscate(obfuscated))

        obfuscated = 'var _0x01ff=["foo"];true?_0x01ff[0]:false;'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'true ? "foo" : false;')
        self.assertEqual(expected, deobfuscate(obfuscated))

        obfuscated = 'var _0x01ff=["foo"];true?true:_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'true ? true : "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_return(self):
        """Obfuscation with parent node `Return`."""
        obfuscated = 'var _0x01ff=["foo"];function f(){return _0x01ff[0]}'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'function f() {\n'
            '  return "foo";\n'
            '}')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_binary_operation(self):
        """Obfuscation with parent node `BinOp`."""
        obfuscated = 'var _0x01ff=["foo"];_0x01ff[0]+_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            '"foo" + "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_binary_operation_multiple(self):
        """Obfuscation with parent node `BinOp`."""
        obfuscated = 'var _0x01ff=["foo"];_0x01ff[0]+_0x01ff[0]+_0x01ff[0]+_0x01ff[0];'
        expected = (
            'var _0x01ff = ["foo"];\n'
            '"foo" + "foo" + "foo" + "foo";')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_switch(self):
        """Obfuscation with parent node `Switch`."""
        obfuscated = 'var _0x01ff=["foo"];switch(_0x01ff[0]){case 1:1;break;default:3;break;}'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'switch ("foo") {\n'
            '  case 1:\n'
            '    1;\n'
            '    break;\n'
            '  default:\n'
            '    3;\n'
            '    break;\n'
            '}')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_case(self):
        """Obfuscation with parent node `Case`."""
        obfuscated = 'var _0x01ff=["foo"];switch(0){case _0x01ff[0]:1;break;default:3;break;}'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'switch (0) {\n'
            '  case "foo":\n'
            '    1;\n'
            '    break;\n'
            '  default:\n'
            '    3;\n'
            '    break;\n'
            '}')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_function_call(self):
        """Obfuscation with parent node `FunctionCall`."""
        obfuscated = 'var _0x01ff=["foo"];function f(a){return a}f(_0x01ff[0]);'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'function f(a) {\n'
            '  return a;\n'
            '}\n'
            'f("foo");')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_new_expression(self):
        """Obfuscation with parent node `NewExpr`."""
        obfuscated = 'var _0x01ff=["foo"];new C(_0x01ff[0]);'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'new C("foo");')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_list(self):
        """Obfuscation with parent node `list`,e.g., list of parameters."""
        obfuscated = 'var _0x01ff=["foo"];new C(9,8,_0x01ff[0]);'
        expected = (
            'var _0x01ff = ["foo"];\n'
            'new C(9, 8, "foo");')
        self.assertEqual(expected, deobfuscate(obfuscated))

    def test_context_awareness(self):
        """Test for different contexts."""
        obfuscated = 'var _0x01ff=[9,"context aware \\"_0x01ff[0]\\""];var a=_0x01ff[0];a=_0x01ff[1];'
        expected = (
            'var _0x01ff = [9,"context aware \\"_0x01ff[0]\\""];\n' +
            'var a = 9;\n' +
            'a = "context aware \\"_0x01ff[0]\\"";')
        self.assertEqual(expected, deobfuscate(obfuscated))


# noinspection PyPep8Naming
class Test_scan_obfuscation_array(TestCase):
    def test_single_array(self):
        tree = Parser().parse('var _0x01ff=["text"];')
        obfuscation_array_name, obfuscation_array = scan_obfuscation_array(tree)
        self.assertEqual('_0x01ff', obfuscation_array_name)

    def test_multiple_arrays(self):
        tree = Parser().parse('var _a=["text a"];var _b=["text b"];var _c=["text c"];')
        obfuscation_array_name, obfuscation_array = scan_obfuscation_array(tree)
        self.assertEqual('_a', obfuscation_array_name)

    def test_mixed_w_vars(self):
        """Obfuscation array mixed with other global variables."""
        tree = Parser().parse('var x=1;var _y={"z":2};var _a=["text a"];var _b=["text b"];var _c=["text c"];')
        obfuscation_array_name, obfuscation_array = scan_obfuscation_array(tree)
        self.assertEqual('_a', obfuscation_array_name)
