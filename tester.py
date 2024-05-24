import unittest
from lexer import lexer, Error
from evaluator import evaluator, Environment, Node
from unittest.mock import patch
from parser import parser


class TestLexer(unittest.TestCase):
    def test_lexer_with_numbers(self):
        command = "123"
        expected_output = [("NUMBER", "123"), ("EOF", "0")]
        result = lexer(command)
        self.assertEqual(result, expected_output)
        if result == expected_output:
            print(f"Lexer can tokenize numbers correctly")
        else:
            print(f"Lexer can't tokenize numbers correctly")

    def test_lexer_with_keywords(self):
        command = "BEG PRINT EXIT!"
        expected_output = [
            ("KEYWORD", "BEG"),
            ("KEYWORD", "PRINT"),
            ("KEYWORD", "EXIT!"),
            ("EOF", "0"),
        ]
        result = lexer(command)
        self.assertEqual(result, expected_output)
        if result == expected_output:
            print(f"Lexer can tokenize keywords correctly")
        else:
            print(f"Lexer can't tokenize keywords correctly")

    def test_lexer_with_operators(self):
        command = "+ - * / %"
        expected_output = [
            ("PRECEDENCE 1", "+"),
            ("PRECEDENCE 1", "-"),
            ("PRECEDENCE 2", "*"),
            ("PRECEDENCE 2", "/"),
            ("PRECEDENCE 2", "%"),
            ("EOF", "0"),
        ]
        result = lexer(command)
        self.assertEqual(result, expected_output)
        if result == expected_output:
            print(f"Lexer can tokenize operators correctly")
        else:
            print(f"Lexer can't tokenize operators correctly")

    def test_lexer_with_invalid_token(self):
        command = "#"
        with self.assertRaises(Error):
            lexer(command)
        if Error:
            print(f"Lexer can't tokenize invalid tokens correctly")
        else:
            print(f"Lexer can tokenize invalid tokens correctly")


class TestParser(unittest.TestCase):
    def test_parse_assignment(self):
        tokens = [("VARIABLE", "x"), ("KEYWORD", "="), ("NUMBER", "5"), ("EOF", "0")]
        ast = parser(tokens)
        self.assertEqual(ast.node_type, "ASSIGNMENT")
        self.assertEqual(ast.value, "x")
        self.assertEqual(ast.children[0].node_type, "FACTOR")
        self.assertEqual(ast.children[0].value, "5")
        result = evaluator(ast, {})

        if result == 5:
            print(f"Parser can parse assignments correctly")
        else:
            print(f"Parser can't parse assignments correctly")

    def test_parse_output(self):
        tokens = [("KEYWORD", "PRINT"), ("NUMBER", "5"), ("EOF", "0")]
        ast = parser(tokens)
        self.assertEqual(ast.node_type, "OUTPUT")
        self.assertEqual(ast.value, "NUMBER")
        self.assertEqual(ast.children[0], "5")
        result = evaluator(ast, {})
        if result == 5:
            print(f"Parser can parse outputs correctly")
        else:
            print(f"Parser can't parse outputs correctly")

    def test_parse_exit(self):
        tokens = [("KEYWORD", "EXIT!"), ("EOF", "0")]
        ast = parser(tokens)
        self.assertEqual(ast.node_type, "EXIT")
        result = evaluator(ast, {})
        if result == None:
            print(f"Parser can parse exits correctly")
        else:
            print(f"Parser can't parse exits correctly")

    def test_parse_expression(self):
        tokens = [("NUMBER", "5"), ("PRECEDENCE 1", "+"), ("NUMBER", "3"), ("EOF", "0")]
        ast = parser(tokens)
        self.assertEqual(ast.node_type, "EXPRESSION")
        self.assertEqual(ast.value, "+")
        self.assertEqual(ast.children[0].node_type, "FACTOR")
        self.assertEqual(ast.children[0].value, "5")
        self.assertEqual(ast.children[1].node_type, "FACTOR")
        self.assertEqual(ast.children[1].value, "3")
        result = evaluator(ast, {})
        if result == 8:
            print(f"Parser can parse expressions correctly")
        else:
            print(f"Parser can't parse expressions correctly")


class TestEvaluator(unittest.TestCase):
    def test_evaluator_with_expression(self):
        env = {}
        ast = Node("EXPRESSION", "+", [Node("TERM", "5", []), Node("TERM", "3", [])])
        result = evaluator(ast, env)
        self.assertEqual(result, 8)
        if result == 8:
            print(f"Evaluator can evaluate expressions correctly")
        else:
            print(f"Evaluator can't evaluate expressions correctly")

    def test_evaluator_with_assignment(self):
        env = {}
        ast = Node(
            "ASSIGNMENT", "=", [Node("VARIABLE", "x", []), Node("TERM", "5", [])]
        )
        evaluator(ast, env)
        self.assertEqual(env["x"], 5)
        if env["x"] == 5:
            print(f"Evaluator can evaluate assignments correctly")
        else:
            print(f"Evaluator can't evaluate assignments correctly")

    @patch("builtins.input", return_value="5")
    def test_evaluator_with_beg(self, input):
        env = {}
        ast = Node("BEG", "x", [])
        evaluator(ast, env)
        self.assertEqual(env["x"], 5)
        if env["x"] == 5:
            print(f"Evaluator can evaluate beg correctly")
        else:
            print(f"Evaluator can't evaluate beg correctly")

    def test_evaluator_with_exit(self):
        ast = Node("EXIT", "", [])
        with self.assertRaises(SystemExit):
            evaluator(ast, {})
        if SystemExit:
            print(f"Evaluator can evaluate exits correctly")


if __name__ == "__main__":
    unittest.main()

