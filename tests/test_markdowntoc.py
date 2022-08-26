import pkg_resources
import pytest

from markdowntoc import get_headers, sequentialize_header_priorities


@pytest.fixture
def get_data():
    file = pkg_resources.resource_filename("tests", "data/before.md")
    with open(file) as fp:
        return fp.read()


def test_sequentialize_header_priorities():
    data = [("Header 1", 1), ("Header 3", 3), ("Header 4", 4)]
    result = sequentialize_header_priorities(data)
    assert result == [("Header 1", 1), ("Header 3", 2), ("Header 4", 3)]

    data = [("Header 1", 1), ("Header 2", 2), ("Header 3", 3)]
    result = sequentialize_header_priorities(data)
    assert result == [("Header 1", 1), ("Header 2", 2), ("Header 3", 3)]


def test_get_headers(get_data):
    headers = get_headers(get_data)
    assert headers == [
        ("The Data Commons Model Source Generator Project (Plaster)", 1),
        ("Purpose", 1),
        ("Goal", 1),
        ("Data Commons Models", 1),
        ("Problems:", 2),
        ("Project Details", 1),
        ("Requirements", 2),
        ("Features", 2),
        ("Dictionary selection and loading", 2),
        ("Template Management", 2),
        ("How to use", 1),
        ("Install plaster", 2),
        ("Generate gdcdictionary", 2),
        ("Generate biodictionary", 2),
        ("Associated Projects", 1),
        ("Repo Visualizer", 1),
    ]
