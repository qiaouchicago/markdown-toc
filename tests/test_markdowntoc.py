from markdowntoc import sequentialize_header_priorities


def test_sequentialize_header_priorities():
    data = [("Header 1", 1), ("Header 3", 3), ("Header 4", 4)]
    result = sequentialize_header_priorities(data)
    assert result == [("Header 1", 1), ("Header 3", 2), ("Header 4", 3)]

    data = [("Header 1", 1), ("Header 2", 2), ("Header 3", 3)]
    result = sequentialize_header_priorities(data)
    assert result == [("Header 1", 1), ("Header 2", 2), ("Header 3", 3)]
