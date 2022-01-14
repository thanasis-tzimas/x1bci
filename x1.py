import parse
import eval
from vm import VirtualMachine
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('file')
args = arg_parser.parse_args()

virtual_machine = VirtualMachine()
bytecode_parser = parse.BytecodeParser(r"""
    // Comments
    COMMENT: "#" /[^\n]/
    %ignore COMMENT

    // Whitespace
    %import common.WS

    // Numbers
    NUMBER: /[+-]?[1-9]\d*/
          | /0x[0-9a-f]+/
    IMM_ADDR: /@\d+/ 
            | /@0x[0-9a-f]+/

    // Identifiers
    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/

    start: instruction*

    instruction: operation+

    operation: opcode
             | opcode operand

    opcode: "push"
          | "drop"
          | "dup"
          | "swap"
          | "add"
          | "sub"
          | "mul"
          | "div"
          | "if"
          | "jmp"
          | "call"

    operand: NUMBER
           | IMM_ADDR
           | IDENTIFIER

    %ignore WS
""")

tree = bytecode_parser.parse_file(args.file)
result = eval.eval(virtual_machine, tree)
print(result)