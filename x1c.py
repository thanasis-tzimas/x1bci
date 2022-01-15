import argparse
import parse
import compile

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('file')
args = arg_parser.parse_args()

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
          | "jmp"
          | "call"

    operand: NUMBER
           | IMM_ADDR
           | IDENTIFIER

    %ignore WS
""")

tree = bytecode_parser.parse_file(args.file)
compile.compile('./output.s', '', tree)