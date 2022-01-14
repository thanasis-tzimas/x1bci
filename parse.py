from lark import Lark
from lark import Tree
import os

class BytecodeParser:
    ParserModule: Lark

    def __init__(self, grammar: str ) -> None:
        self.ParserModule = Lark(grammar=grammar, keep_all_tokens=True)
    
    def parse_file(self, file_path: str) -> Tree:
        """Parse a file from the indicated file path and generate an AST.

        Args:
            file_path (str): The file path to the file.

        Returns:
            Tree: The generate AST.
        """
        try:
            file = open(file_path, 'r')
        except IOError:
            print(os.strerror(IOError.errno))
            return
        # Read until EOF.
        # Then convert to lowercase.
        file_contents = file.read().lower()
        # Return the parsed file.
        if not file_contents:
            print('Error: file is empty')
            return
        # Close file
        file.close()
        return self.ParserModule.parse(file_contents)