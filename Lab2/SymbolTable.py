from typing import Tuple
from HashTable import HashTable
class SymbolTable:
    def __init__(self, size: int):
        self.size = size
        self.identifiersHashTable = HashTable(size)
        self.intConstantsHashTable = HashTable(size)
        self.stringConstantsHashTable = HashTable(size)

    def add_identifier(self, name: str) -> Tuple[int, int]:
        return self.identifiersHashTable.add(name)

    def add_int_constant(self, constant: int) -> Tuple[int, int]:
        return self.intConstantsHashTable.add(constant)

    def add_string_constant(self, constant: str) -> Tuple[int, int]:
        return self.stringConstantsHashTable.add(constant)

    def has_identifier(self, name: str) -> bool:
        return self.identifiersHashTable.contains(name)

    def has_int_constant(self, constant: int) -> bool:
        return self.intConstantsHashTable.contains(constant)

    def has_string_constant(self, constant: str) -> bool:
        return self.stringConstantsHashTable.contains(constant)

    def get_position_identifier(self, name: str) -> Tuple[int, int]:
        return self.identifiersHashTable.get_position(name)

    def get_position_int_constant(self, constant: int) -> Tuple[int, int]:
        return self.intConstantsHashTable.get_position(constant)

    def get_position_string_constant(self, constant: str) -> Tuple[int, int]:
        return self.stringConstantsHashTable.get_position(constant)

    def __str__(self):
        return f"SymbolTable{{identifiersHashTable={self.identifiersHashTable}\n" \
               f"intConstantsHashTable={self.intConstantsHashTable}\n" \
               f"stringConstantsHashTable={self.stringConstantsHashTable}}}"

# You can use the SymbolTable class as shown in your Java code.
