import logging
from typing import TextIO, Tuple, Any, Sequence

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit.visitors.nodevisitor import ASTVisitor

LOGGER = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class JsardError(Exception):
    pass


class InvalidInputFormat(JsardError):
    pass


class ReplacingVisitor(ASTVisitor):
    """
    AST visitor which can find and replace `selected` nodes based on provided `obfuscation_array`.
    """
    def __init__(self, selected: Sequence, obfuscation_array: Sequence):
        self.selected = selected
        self.obfuscation_array = obfuscation_array

    def replace(self, node, child: ast.BracketAccessor):
        """Replace `child` node of `node` based on configured `self.obfuscation_array`."""
        replacement = self.obfuscation_array[int(child.expr.value)]
        if isinstance(node, ast.FunctionCall):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child in node.args:
                node.args[:] = [replacement if child is a else a for a in node.args]
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Array):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child in node.items:
                node.items[:] = [replacement if child is a else a for a in node.items]
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Switch):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.expr:
                node.expr = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Case):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.expr:
                node.expr = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.BracketAccessor):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.node:
                node.node = replacement
            elif child is node.expr:
                node.expr = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.VarDecl):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.initializer:
                node.initializer = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Assign):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.right:
                node.right = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.BinOp):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.right:
                node.right = replacement
            elif child is node.left:
                node.left = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Conditional):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.predicate:
                node.predicate = replacement
            elif child is node.consequent:
                node.consequent = replacement
            elif child is node.alternative:
                node.alternative = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.Return):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.expr:
                node.expr = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.ExprStatement):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.expr:
                node.expr = replacement
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, ast.NewExpr):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child is node.args:
                node.args[:] = [replacement if child is a else a for a in node.args]
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        elif isinstance(node, list):
            # TODO: Extend `slimit` package with `replace` method to all nodes instead of these conditions with `isinstance`.
            if child in node:
                node[:] = [replacement if child is a else a for a in node]
            else:
                LOGGER.error('Unexpected structure of node\'s child nodes. Replacement skipped. node={}'.format(node))
        else:
            LOGGER.error('Unsupported type of node. node={}'.format(node))

    def generic_visit(self, node):
        for child in node:
            if child in self.selected:
                self.replace(node, child)
        for child in node:
            self.visit(child)


def dereference(tree, obfuscation_array_name, obfuscation_array) -> int:
    """
    Search provided `tree` and dereference all literal-access to obfuscation array.
    :param tree: Tree for processing.
    :param obfuscation_array_name: Name of JavaScript variable with obfuscation array.
    :param obfuscation_array: Content of obfuscation array for dereferencing.
    :return: Number of references processed.
    """
    selected = []
    for node in nodevisitor.visit(tree):
        if isinstance(node, ast.BracketAccessor) \
                and isinstance(node.expr, ast.Number) \
                and isinstance(node.node, ast.Identifier) \
                and node.node.value == obfuscation_array_name:
            LOGGER.debug('dereference: BracketAccessor=`{}`'.format(node.to_ecma()))
            selected.append(node)
    replacer = ReplacingVisitor(selected, obfuscation_array)
    replacer.visit(tree)
    return len(selected)


def deobfuscate(obfuscated: str) -> str:
    """
    Deobfuscate JavaScript code in Array Ref obfuscation format.
    :param obfuscated: obfuscated code in Array Ref obfuscation format.
    :return: deobfuscated code.

    :raises InvalidInputFormat: Obfuscation array not found in input source code.
    """
    obfuscation_array_name: str
    tree = Parser().parse(obfuscated)

    # detect and store obfuscation_array
    # :raises InvalidInputFormat
    obfuscation_array_name, obfuscation_array = scan_obfuscation_array(tree)
    LOGGER.debug('Obfuscation array name: {}'.format(obfuscation_array_name))

    hits = dereference(tree, obfuscation_array_name, obfuscation_array)
    while hits:
        hits = dereference(tree, obfuscation_array_name, obfuscation_array)

    return tree.to_ecma()


def deobfuscate_files(input_: TextIO, output: TextIO) -> None:
    """
    Deobfuscate JavaScript code in Array Ref obfuscation format from input to output files.
    :param input_: Input text file with obfuscated code.
    :param output: Output text file with deobfuscated code.

    :raises InvalidInputFormat: Obfuscation array not found in input source code.
    """
    output.write(deobfuscate(input_.read()))


def scan_obfuscation_array(tree) -> Tuple[str, Any]:
    """
    Detect obfuscation array in parsed tree, return its name and content.
    :param tree: parsed tree of JavaScript source code
    :return: tuple with 1) name of obfuscation array variable 2) array's content
    :raises InvalidInputFormat: Obfuscation array not found in input source code.
    """
    for node in nodevisitor.visit(tree):
        if isinstance(node, ast.VarStatement) and len(node.children()) == 1:
            child = node.children()[0]
            if isinstance(child, ast.VarDecl) and isinstance(child.identifier, ast.Identifier) \
                    and isinstance(child.initializer, ast.Array):
                obfuscation_array_name = child.identifier.value
                obfuscation_array = child.initializer.items
                break
    else:
        msg = 'Obfuscation array not found in input source code.'
        LOGGER.error(msg)
        raise InvalidInputFormat(msg)
    return obfuscation_array_name, obfuscation_array
