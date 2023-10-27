from SymbolTable import SymbolTable


def main():
    symbolTable = SymbolTable(100)
    p1 = (-1, -1)
    p2 = (-1, -1)
    p3 = (-1, -1)

    try:
        p1 = symbolTable.add_identifier("abc")
        print(f"abc -> {p1}")
        print(f"c -> {symbolTable.add_identifier('c')}")
        print(f"a -> {symbolTable.add_identifier('a')}")
        print(f"3 -> {symbolTable.add_int_constant(3)}")
        p2 = symbolTable.add_int_constant(100)
        print(f"100 -> {p2}")
        print(f"20 -> {symbolTable.add_int_constant(20)}")
        print(f"131 -> {symbolTable.add_int_constant(131)}")

        print(f"lab -> {symbolTable.add_string_constant('lab')}")
        print(f"hello -> {symbolTable.add_string_constant('hello')}")
        p3 = symbolTable.add_string_constant('world')
        print(f"world -> {p3}")

        print(f"abc -> {symbolTable.add_identifier('abc')}")
    except Exception as e:
        print(e)

    print(symbolTable)

    try:
        assert symbolTable.get_position_identifier('abc') == p1, f"abc does not have position {p1}"
        assert symbolTable.get_position_int_constant(100) == p2, f"100 does not have position {p2}"
        assert symbolTable.get_position_string_constant('world') == p3, f"world does not have position {p3}"
    except AssertionError as e:
        print(e)

    try:
        print(f"49 -> {symbolTable.get_position_int_constant(49)}")
        assert symbolTable.get_position_int_constant(49) == (2, 2), "49 does not have position (2, 2)"
    except AssertionError as e:
        print(e)

    try:
        print(f"word -> {symbolTable.get_position_string_constant('word')}")
        assert symbolTable.get_position_string_constant('word') == p3, f"word does not have position {p3}"
    except AssertionError as e:
        print(e)


if __name__ == "__main__":
    main()
