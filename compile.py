import subprocess
import lark
import eval

def compile(output_name: str, output_dir: str, AST: lark.Tree) -> None:
    try:
        output_file = open(output_name, 'w')
    except FileExistsError:
        print('Error: %s already exist' % output_name)
        exit(1)
    
    # x86 Bootstrapping
    output_file.write("segment .text\n")
    output_file.write("global _start\n")
    output_file.write("_start:\n")
    # x86 Bootstrapping
    
    Tokens = AST.scan_values(lambda v: isinstance(v, lark.Token))
    for token in Tokens:
        match token:
            case 'push':
                next_token = next(Tokens)
                if not eval._checkIfNumber(next_token.value):
                    print('Error @ %d:%d: cannot push %s. Only numbers can be pushed' 
                        % (next_token.line, next_token.column, next_token.value))
                    return
                number = next_token.value
                if eval._isHex(number):
                    number = eval._hex2Dec(number)
                    output_file.write("\tpush {}\n".format(number))
                else:
                    output_file.write("\tpush {}\n".format(int(number)))
            case 'drop':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, 0\n")
            case 'dup':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
            case 'swap':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
                output_file.write("\tpush rbx\n")
                output_file.write("\tpush rax\n")
            case 'add':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
                output_file.write("\tadd rbx, rax\n")
                output_file.write("\tmov rbx, rax\n")
                output_file.write("\tpush rax\n")
            case 'sub':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
                output_file.write("\tsub rbx, rax\n")
                output_file.write("\tmov rbx, rax\n")
                output_file.write("\tpush rax\n")
            case 'mul':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
                output_file.write("\timul rbx\n")
                output_file.write("\tpush rax\n")
            case 'div':
                output_file.write("\tpop rax\n")
                output_file.write("\tmov rax, rbx\n")
                output_file.write("\tpop rax\n")
                output_file.write("\tidiv rbx\n")
                output_file.write("\tpush rax\n")
            case _:
                print('Error @ %d:%d: %s is not a recognizeable opcode.' % (token.line, token.column, token.value))
                print('Compilation terminated')
                exit(1)
    # x86 Bootstrapping
    output_file.write("\tmov rax, 60\n")
    output_file.write("\tmov rdi, 0\n")
    output_file.write("\tsyscall\n")
    output_file.close()
    # x86 Bootstrapping

    # Assemble and link
    subprocess.run(["nasm","-felf64", output_name, "-o", "a.o"])
    subprocess.run(["ld", "a.o"])
    subprocess.run(["rm", "-rf", output_name, "a.o"])