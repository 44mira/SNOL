import unittest
from lexer import lexer, Error
from evaluator import evaluator
from interfaces import Node, Environment
from unittest.mock import patch
from parser import parser


class TestLexer(unittest.TestCase):
    def test_lexer_with_numbers(self):
        command = "123"
        expected_output = [("NUMBER", "123"), ("EOF", "0")]
        result = lexer(command)
        self.assertEqual(
            result, expected_output, "Lexer can't tokenize numbers correctly"
        )

    def test_lexer_with_keywords(self):
        command = "BEG PRINT EXIT!"
        expected_output = [
            ("KEYWORD", "BEG"),
            ("KEYWORD", "PRINT"),
            ("KEYWORD", "EXIT!"),
            ("EOF", "0"),
        ]
        result = lexer(command)
        self.assertEqual(
            result, expected_output, "Lexer can't tokenize keywords correctly"
        )

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
        self.assertEqual(
            result, expected_output, "Lexer can't tokenize operators correctly"
        )

    def test_lexer_with_invalid_token(self):
        command = "#"
        with self.assertRaises(Error, msg="Lexer can tokenize invalid tokens"):
            lexer(command)


class TestParser(unittest.TestCase):
    def test_parse_assignment(self):
        tokens = [("VARIABLE", "x"), ("KEYWORD", "="), ("NUMBER", "5"), ("EOF", "0")]
        ast = parser(tokens)
        expected_ast = Node("x", "ASSIGNMENT", [Node("5", "FACTOR", [])])
        self.assertEqual(ast, expected_ast, "Parser can't parse assignments correctly")

    def test_parse_output(self):
        tokens = [("KEYWORD", "PRINT"), ("NUMBER", "5"), ("EOF", "0")]
        ast = parser(tokens)
        expected_ast = Node("NUMBER", "OUTPUT", ["5"])

        self.assertEqual(ast, expected_ast, "Parser can't parse output correctly")

    def test_parse_exit(self):
        tokens = [("KEYWORD", "EXIT!"), ("EOF", "0")]
        ast = parser(tokens)
        expected_ast = Node(None, "EXIT", [])
        self.assertEqual(ast, expected_ast, "Parser can't parse exit correctly")

    def test_parse_expression(self):
        tokens = [("NUMBER", "5"), ("PRECEDENCE 1", "+"), ("NUMBER", "3"), ("EOF", "0")]
        ast = parser(tokens)
        expected_ast = Node(
            "+", "EXPRESSION", [Node("5", "FACTOR", []), Node("3", "FACTOR", [])]
        )
        self.assertEqual(ast, expected_ast, "Parser can't parse expressions correctly")

        tokens = [
            ("NUMBER", "5.0"),
            ("PRECEDENCE 1", "-"),
            ("NUMBER", "3"),
            ("EOF", "0"),
        ]
        ast = parser(tokens)
        expected_ast = Node(
            "-", "EXPRESSION", [Node("5.0", "FACTOR", []), Node("3", "FACTOR", [])]
        )
        self.assertEqual(ast, expected_ast, "Parser can't parse expressions correctly")

    def test_parse_complex_expression(self):
        tokens = lexer("5 + 3 * (4 + 2 * 3)")
        ast = parser(tokens)
        expected_ast = Node(
            "+",
            "EXPRESSION",
            [
                Node("5", "FACTOR", []),
                Node(
                    "*",
                    "TERM",
                    [
                        Node("3", "FACTOR", []),
                        Node(
                            None,
                            "FACTOR",
                            [
                                Node(
                                    "+",
                                    "EXPRESSION",
                                    [
                                        Node("4", "FACTOR", []),
                                        Node(
                                            "*",
                                            "TERM",
                                            [
                                                Node("2", "FACTOR", []),
                                                Node("3", "FACTOR", []),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            ast, expected_ast, "Parser can't parse complex expressions correctly"
        )


class TestEvaluator(unittest.TestCase):
    def test_evaluate_expression(self):
        env: Environment = {}
        ast = Node(
            "+", "EXPRESSION", [Node("2", "FACTOR", []), Node("3", "FACTOR", [])]
        )
        result = evaluator(ast, env)
        self.assertEqual(result, 5, "Evaluator can't evaluate expressions correctly")

    def test_evaluate_type_error(self):
        env: Environment = {"x": 5.0}
        ast = Node(
            "+", "EXPRESSION", [Node("2", "FACTOR", []), Node("x", "VARIABLE", [])]
        )
        with self.assertRaises(Error, msg="Evaluator can't handle type errors"):
            evaluator(ast, env)

    def test_evaluate_term(self):
        env: Environment = {}
        ast = Node("*", "TERM", [Node("2", "FACTOR", []), Node("3", "FACTOR", [])])
        result = evaluator(ast, env)
        self.assertEqual(result, 6, "Evaluator can't evaluate terms correctly")

    def test_evaluate_assignment(self):
        env: Environment = {}
        ast = Node("x", "ASSIGNMENT", [Node("5", "FACTOR", [])])
        evaluator(ast, env)
        self.assertEqual(env["x"], 5, "Evaluator can't evaluate assignments correctly")

    def test_evaluate_output(self):
        env: Environment = {"x": 5}
        node = Node("VARIABLE", "OUTPUT", ["x"])
        result = evaluator(node, env)
        self.assertIsNone(result, "Evaluator can't evaluate output correctly")

        env: Environment = {}
        node = Node("NUMBER", "OUTPUT", [5])
        result = evaluator(node, env)
        self.assertIsNone(result, "Evaluator can't evaluate output correctly")

    def test_evaluate_beg(self):
        env: Environment = {}
        ast = Node("x", "BEG", [])
        with patch("builtins.input", return_value="5"):
            evaluator(ast, env)
        self.assertEqual(env["x"], 5)

    def test_evaluate_exit(self):
        env: Environment = {}
        ast = Node(None, "EXIT", [])
        with self.assertRaises(SystemExit):
            evaluator(ast, env)


if __name__ == "__main__":
    unittest.main()
