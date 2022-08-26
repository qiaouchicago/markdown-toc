import pkg_resources
import pytest

from markdowntoc import (
    create_github_header_anchor,
    create_table_of_contents,
    create_table_of_contents_github,
    find_toc_end,
    find_toc_start,
    get_headers,
    get_parser,
    sequentialize_header_priorities,
)
from tests.data import processed


@pytest.fixture
def get_data():
    file = pkg_resources.resource_filename("tests", "data/before.md")
    with open(file) as fp:
        return fp.read()


@pytest.fixture
def get_md_lines(get_data):
    return get_data.splitlines()


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


def test_create_github_header_anchor():
    res = create_github_header_anchor("Purpose")
    assert res == "[Purpose](#Purpose)"


def test_create_table_of_contents():
    pairs = [
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

    res = create_table_of_contents(pairs)
    assert res == [
        "# Table of Contents",
        "",
        "- [The Data Commons Model Source Generator Project (Plaster)](#The-Data-Commons-Model-Source-Generator-Project-(Plaster))",
        "- [Purpose](#Purpose)",
        "- [Goal](#Goal)",
        "- [Data Commons Models](#Data-Commons-Models)",
        "  - [Problems:](#Problems:)",
        "- [Project Details](#Project-Details)",
        "  - [Requirements](#Requirements)",
        "  - [Features](#Features)",
        "  - [Dictionary selection and loading](#Dictionary-selection-and-loading)",
        "  - [Template Management](#Template-Management)",
        "- [How to use](#How-to-use)",
        "  - [Install plaster](#Install-plaster)",
        "  - [Generate gdcdictionary](#Generate-gdcdictionary)",
        "  - [Generate biodictionary](#Generate-biodictionary)",
        "- [Associated Projects](#Associated-Projects)",
        "- [Repo Visualizer](#Repo-Visualizer)",
    ]


def test_find_toc_start(get_md_lines):
    line_number = find_toc_start(get_md_lines)
    assert line_number == 7


def test_find_toc_end(get_md_lines):
    line_number = find_toc_end(get_md_lines)
    assert line_number == 7


def test_create_table_of_contents_github():
    parser = get_parser()
    args = parser.parse_args()
    params = vars(args)
    params["name"] = [pkg_resources.resource_filename("tests", "data/before.md")]

    res = create_table_of_contents_github(params)

    assert res[0] == processed.data
    assert res[1] == params["name"]
