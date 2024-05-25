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
        expected_ast = Node("5", "OUTPUT", [])
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


# TODO: Fix the evaluator tests

# class TestEvaluator(unittest.TestCase):
#     def test_evaluator_with_expression(self):
#         env = {}
#         ast = Node("EXPRESSION", "+", [Node("TERM", "5", []), Node("TERM", "3", [])])
#         result = evaluator(ast, env)
#         self.assertEqual(result, 8)
#         if result == 8:
#             print(f"Evaluator can evaluate expressions correctly")
#         else:
#             print(f"Evaluator can't evaluate expressions correctly")
#
#     def test_evaluator_with_assignment(self):
#         env = {}
#         ast = Node(
#             "ASSIGNMENT", "=", [Node("VARIABLE", "x", []), Node("TERM", "5", [])]
#         )
#         evaluator(ast, env)
#         self.assertEqual(env["x"], 5)
#         if env["x"] == 5:
#             print(f"Evaluator can evaluate assignments correctly")
#         else:
#             print(f"Evaluator can't evaluate assignments correctly")
#
#     @patch("builtins.input", return_value="5")
#     def test_evaluator_with_beg(self, input):
#         env = {}
#         ast = Node("BEG", "x", [])
#         evaluator(ast, env)
#         self.assertEqual(env["x"], 5)
#         if env["x"] == 5:
#             print(f"Evaluator can evaluate beg correctly")
#         else:
#             print(f"Evaluator can't evaluate beg correctly")
#
#     def test_evaluator_with_exit(self):
#         ast = Node("EXIT", "", [])
#         with self.assertRaises(SystemExit):
#             evaluator(ast, {})
#         if SystemExit:
#             print(f"Evaluator can evaluate exits correctly")


if __name__ == "__main__":
    unittest.main()
