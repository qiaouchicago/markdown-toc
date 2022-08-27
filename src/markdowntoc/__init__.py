from pkg_resources import get_distribution

from .markdowntoc import (
    create_github_header_anchor,
    create_table_of_contents,
    create_table_of_contents_github,
    find_toc_end,
    find_toc_start,
    get_headers,
    get_parser,
    main,
    sequentialize_header_priorities,
    write_results,
)

VERSION = get_distribution(__name__).version
