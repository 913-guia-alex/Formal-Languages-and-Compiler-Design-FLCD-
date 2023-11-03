from SymbolTable import SymbolTable
from ScannerException import ScannerException


class Scanner:
    def __init__(self):
        self.program = ""
        self.tokens = set()
        self.reserved_words = set()
        self.symbol_table = SymbolTable(47)
        self.PIF = []
        self.index = 0
        self.current_line = 1

    def set_program(self, program: str):
        self.program = program

    def read_tokens(self, token_file: str):
        with open(token_file) as file:
            self.tokens = {token.strip() for token in file.readlines()}

        reserved = {"for", "break", "elseif", "if", "else", "while", "do", "read", "write", "boolean", "string",
                    "integer", "vector"}
        self.reserved_words = self.tokens.intersection(reserved)
        self.tokens -= self.reserved_words

    def skip_spaces(self):
        while self.index < len(self.program) and self.program[self.index].isspace():
            if self.program[self.index] == '\n':
                self.current_line += 1
            self.index += 1

    def skip_comments(self):
        if self.program.startswith("#", self.index):
            while self.index < len(self.program) and self.program[self.index] != '\n':
                self.index += 1

    def treat_int_constant(self):
        start_index = self.index
        while self.index < len(self.program) and self.program[self.index].isdigit():
            self.index += 1

        if self.index > start_index:
            int_constant = int(self.program[start_index:self.index])
            position = self.symbol_table.add_constant(int_constant)
            self.PIF.append(("const", position))
            return True
        return False

    def treat_string_constant(self):
        if self.program[self.index] == '"':
            start_index = self.index
            self.index += 1
            while self.index < len(self.program) and self.program[self.index] != '"':
                self.index += 1

            if self.index < len(self.program) and self.program[self.index] == '"':
                self.index += 1
                string_constant = self.program[start_index:self.index]
                position = self.symbol_table.add_constant(string_constant)
                self.PIF.append(("const", position))
                return True
            else:
                raise ScannerException(f"Missing closing double quote for string constant at line {self.current_line}")
        return False

    def check_if_valid(self, possible_identifier, program_substring):
        if possible_identifier in self.reserved_words or possible_identifier in self.tokens:
            return True

        if program_substring.startswith(possible_identifier + " (integer") or \
                program_substring.startswith(possible_identifier + " (boolean") or \
                program_substring.startswith(possible_identifier + " (string") or \
                program_substring.startswith(possible_identifier + " (vector"):
            return True

        if (possible_identifier[0].isalpha() or possible_identifier[0] == '_') and all(
                char.isalnum() or char == '_' for char in possible_identifier):
            return True

        return self.symbol_table.has_identifier(possible_identifier)

    def treat_identifier(self):
        start_index = self.index
        while self.index < len(self.program) and (
                self.program[self.index].isalnum() or self.program[self.index] == '_'):
            self.index += 1
        identifier = self.program[start_index:self.index]
        if identifier and not self.check_if_valid(identifier, self.program[start_index:]):
            raise ScannerException(f"Invalid identifier '{identifier}' at line {self.current_line}")
        if identifier:
            if identifier in self.reserved_words:
                self.PIF.append((identifier, (-1, -1)))
            else:
                try:
                    position = self.symbol_table.add_identifier(identifier)
                except Exception:
                    position = self.symbol_table.get_position_identifier(identifier)
                self.PIF.append(("identifier", position))
            return True
        return False

    def treat_from_token_list(self):
        for token in self.tokens:
            if self.program.startswith(token, self.index):
                self.index += len(token)
                self.PIF.append((token, (-1, -1)))
                return True
        return False

    def next_token(self):
        self.skip_spaces()
        self.skip_comments()
        if self.index == len(self.program):
            return
        if self.treat_string_constant():
            return
        if self.treat_int_constant():
            return
        if self.treat_identifier():
            return
        if self.treat_from_token_list():
            return
        raise ScannerException(f"Lexical error: invalid token at line {self.current_line}, index {self.index}")

    def scan(self, program_file_name, token_file_name):
        try:
            self.read_tokens(token_file_name)

            with open(program_file_name) as file:
                self.set_program(file.read())

            self.index = 0
            self.PIF = []
            self.symbol_table = SymbolTable(20)
            self.current_line = 1

            while self.index < len(self.program):
                self.next_token()

            with open("PIF.out", "a") as pif_file:
                pif_file.write(program_file_name + ":\n\n")
                for token, position in self.PIF:
                    pif_file.write(f"{token} -> ({position[0]}, {position[1]})\n")

            # Writing identifiers to ST1.out
            with open("ST1.out", "a") as st1_file:
                st1_file.write("Identifiers:\n")
                identifiers = str(self.symbol_table.identifiers_table)
                st1_file.write(identifiers)

            # Writing constants (integers and strings) to ST2.out
            with open("ST2.out", "a") as st2_file:
                st2_file.write("Constants:\n")
                constants = str(self.symbol_table.constants_table)
                st2_file.write(constants)

            print("Lexically correct")

        except (FileNotFoundError, ScannerException) as e:
            print(e)
