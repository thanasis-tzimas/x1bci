import lark
from vm import VirtualMachine
import re

def _isImm(string: str) -> bool:
    return (re.fullmatch(r"@\d+", string or "") is not None) or (re.fullmatch(r"@0x[0-9a-f]+", string or "") is not None) 

def _isInt(string: str) -> bool:
    return (re.fullmatch(r"[+-]?[1-9]\d*", string or "") is not None) or (re.fullmatch(r"0x[0-9a-f]+", string or "") is not None) 

def _isHex(string: str) -> bool:
    return re.fullmatch(r"0x[0-9a-f]+", string or "") is not None

def _hex2Dec(string: str) -> int:
    return int(string, base=16)

def _checkIfNumber(string: str) -> bool:
    return _isInt(string) or _isHex(string)

def eval(VM: VirtualMachine, AST: lark.Tree) -> str:
    """Evaluate a syntax tree and produce a result.

    Args:
        VM (VirtualMachine): The virtual machine that the function can manipulate.
        AST (lark.Tree): The syntax tree that was produced by the parser.

    Returns:
        str: The result in a string format.
    """
    result: str = ""
    # Convert the AST object to an iteratable Token list.
    Tokens = AST.scan_values(lambda v: isinstance(v, lark.Token))
    for token in Tokens:
        match token:
            case "push":
                next_token = next(Tokens)
                if not _checkIfNumber(next_token.value):
                    print('Error @ %d:%d: cannot push %s. Only numbers can be pushed' 
                        % (next_token.line, next_token.column, next_token.value))
                    return
                number = next_token.value
                if _isHex(number):
                    number = _hex2Dec(number)
                    VM.Memory.append(number)
                else:
                    VM.Memory.append(int(number))
            case "drop":
                VM.Memory.pop()
            case "dup":
                x = VM.Memory.pop()
                y = x
                VM.Memory.append(x)
                VM.Memory.append(y)
                pass
            case "swap":
                x = VM.Memory.pop()
                y = VM.Memory.pop()
                VM.Memory.append(y)
                VM.Memory.append(x)
                pass
            case "add":
                x, y = VM.Memory.pop(), VM.Memory.pop()
                res = int(x)+int(y)
                VM.Memory.append(res)
            case "sub":
                x, y = VM.Memory.pop(), VM.Memory.pop()
                res = int(y)-int(x)
                VM.Memory.append(res)
            case "mul":
                x, y = VM.Memory.pop(), VM.Memory.pop()
                res = int(x)*int(y)
                VM.Memory.append(res)
            case "div":
                x, y = VM.Memory.pop(), VM.Memory.pop()
                res = int(x)/int(y)
                VM.Memory.append(res)
            case _:
                print('Error @ %d:%d: %s is not a recognizeable opcode.' % (token.line, token.column, token.value))
                return
        result += str.format("[{}\n{}\n", VM.Flags, VM.Memory)
    return result