# X1 Bytecode Interpreter
The X1 Bytecode is bytecode designed for simplicity in programming design and compilation.

## Bytecode Instructions
- `push <integer>`: Push an `<integer>` into the memory stack.
- `drop`: Pop and discard the top element from the stack.
- `dup`: Duplicate the top element of the stack and put it on top.
- `swap`: Swap the top element and swap it with its adjacent element on the stack.
- `add`: Add the `stack[top]` and `stack[top-1]` element and append their result back to the top of the stack.
- `sub`: Sub the `stack[top]` and `stack[top-1]` element and append their result back to the top of the stack.
- `mul`: Mul the `stack[top]` and `stack[top-1]` element and append their result back to the top of the stack.
- `div`: Div the `stack[top]` and `stack[top-1]` element and append their result back to the top of the stack.
- `jmp <address>/<label>`: Uncoditional jump to either the `<address>` or `<label>`.
- `call <label>`: Call a function referenced by the `<label>`.