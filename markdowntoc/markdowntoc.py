# encoding=utf-8
# python3.6

import os
from os import path
import re
import argparse
from urllib.parse import quote

HOME = os.getenv("HOME", "")

parser = argparse.ArgumentParser(
    description="Markdown Table of Contents Generator for Bear or Github",
    add_help=False,
)

parser.add_argument("--help", action="help", help="Show this help message and exit")

parser.add_argument(
    "name",
    nargs="+",
    type=str,
    help="Bear Note UUID, Bear Note Title, Bear Note Tag, or Markdown file",
)

parser.add_argument(
    "-h",
    "--header-priority",
    type=int,
    dest="header_priority",
    default=3,
    help="(Default: 3) Maximum Header Priority/Strength to consider as Table of Contents",
)

parser.add_argument(
    "-t",
    "--type",
    type=str.lower,
    dest="type",
    choices=["github", "bear"],
    default="github",
    help="(Default: github) Github Anchors or Bear Anchors",
)

parser.add_argument(
    "--no-write",
    dest="write",
    action="store_false",
    help="Whether or not write Table of Contents to file or note automatically or output to the console.\
                          Add this flag to TURN OFF the automatic writing.",
)

parser.add_argument(
    "-toc",
    "--table-of-contents-style",
    dest="toc",
    default="# Table of Contents",
    help="(Default: '# Table of Contents') Table of Contents Style",
)

parser.set_defaults(write=True)

args = parser.parse_args()
params = vars(args)


def has_table_of_contents(md_text):
    """
    Return True or False whether or not a Table of Contents header already exists in the given Markdown text.
    """
    return (
        re.search(r"^#+\sTable\sof\sContents", md_text, re.IGNORECASE | re.MULTILINE)
        is not None
    )


def get_headers(md_text, max_priority):
    """
    Retrieves a list of header, priority pairs in a given Markdown text.

    Format: (Header Title, Priority)
    """
    lines_iter = iter(md_text.splitlines())

    # Skip the first line because it's the Title
    next(lines_iter)

    # List of Tuples: (Header Title, Number of #)
    header_priority_pairs = []
    in_code_block = False
    for line in lines_iter:
        if line.startswith("```"):
            in_code_block = not in_code_block

        elif not in_code_block and line.startswith("#") and " " in line:
            md_header, header_title = line.split(" ", 1)

            # Check if md_header has all '#'
            if md_header != md_header[0] * len(md_header):
                continue

            # Check if md_header is of lower priority than listed
            if len(md_header) > max_priority:
                continue

            if header_title.lower() != "table of contents" and len(header_title) > 1:
                header_priority_pairs.append((header_title, len(md_header)))

    return sequentialize_header_priorities(header_priority_pairs)


def sequentialize_header_priorities(header_priority_pairs):
    """
    In a case where a H3 or H4 succeeds a H1, due to the nature of the Table of Contents generator\
    which adds the number of tabs corresponding to the header priority/strength, this will sequentialize\
    the headers such that all headers have a priority of atmost 1 more than their preceeding header.

    [('Header 1', 1), ('Header 3', 3), ('Header 4', 4)] -> [('Header 1', 1), ('Header 2', 2), ('Header 3', 3)]
    """
    # Go through each header and and if we see a pair where the difference in priority is > 1, make them sequential
    # Ex: (H1, H3) -> (H1, H2)
    for i in range(len(header_priority_pairs) - 1):
        header, priority = header_priority_pairs[i]
        next_header, next_priority = header_priority_pairs[i + 1]

        if next_priority - priority > 1:
            header_priority_pairs[i + 1] = (next_header, priority + 1)

    return header_priority_pairs


def create_bear_header_anchor(header_title, note_uuid):
    """
    Returns a markdown anchor of a Bear x-callback-url to the header.
    """
    header_title_url_safe = quote(header_title)
    return "[{}](bear://x-callback-url/open-note?id={}&header={})".format(
        header_title, note_uuid, header_title_url_safe
    )


def create_github_header_anchor(header_title):
    """
    Returns a Github Markdown anchor to the header.
    """
    return "[{}](#{})".format(header_title, header_title.strip().replace(" ", "-"))


def create_table_of_contents(header_priority_pairs, note_uuid=None):
    """
    Returns a list of strings containing the Table of Contents.
    """
    if len(header_priority_pairs) == 0:
        return None

    bullet_list = [params["toc"]]
    bullet_list.append("")

    highest_priority = min(header_priority_pairs, key=lambda pair: pair[1])[1]
    for header, priority in header_priority_pairs:
        md_anchor = (
            create_bear_header_anchor(header, note_uuid)
            if params["type"] == "bear"
            else create_github_header_anchor(header)
        )
        bullet_list.append("  " * (priority - highest_priority) + "- " + md_anchor)

    # Specifically for Bear add separator
    if params["type"] == "bear":
        bullet_list.append("---")

    return bullet_list


def create_table_of_contents_github():
    """
    Read from file and returns list of (Original Text, Table of Contents List).
    """
    md_text_toc_pairs = []
    valid_filepaths = []

    for filepath in params["name"]:
        name, ext = path.splitext(filepath)

        if ext.lower() != ".md":
            print("[WARNING]: {} is not a Markdown File, Ignoring...".format(filepath))
            continue

        try:
            with open(filepath, "r") as file:
                md_text = file.read()

                header_list = get_headers(md_text, params["header_priority"])
                table_of_contents_lines = create_table_of_contents(header_list[1:])

                if table_of_contents_lines is None:
                    print(
                        "[WARNING]: {} has no headers to create a Table of Contents, Ignoring...".format(
                            filepath
                        )
                    )
                    continue

                if params["write"]:
                    print("Creating a Table of Contents for '{}'".format(filepath))

                md_text_toc_pairs.append((md_text, table_of_contents_lines))
                valid_filepaths.append(filepath)

        except OSError:
            print(
                "[ERROR]: {} doesn't exist or cannot be read, Ignoring...".format(
                    filepath
                )
            )

    return md_text_toc_pairs, valid_filepaths


def find_toc_start(md_text_lines):
    """
    Some notes in Bear contain #tags near the title. This returns the index in the list that\
    isn't the title or contains tags. If no index found, return len(md_text_lines)
    """
    # Start at 1 to skip the title
    # Look for regex matches of tags and if lines from the top contain tags, then skip
    for i, line in enumerate(md_text_lines):
        if "<!-- toc -->" in line:
            return i + 1

    return len(md_text_lines)


def find_toc_end(md_text_lines):
    for i, line in enumerate(md_text_lines):
        if "<!-- tocstop -->" in line:
            return i

    return len(md_text_lines)


def main():
    md_text_toc_pairs = None
    identifiers = None  # Either Bear Note UUIDs or File Paths

    md_text_toc_pairs, identifiers = create_table_of_contents_github()

    for i, (md_text, toc_lines) in enumerate(md_text_toc_pairs):
        if params["write"]:
            # Inject Table of Contents (Title, \n, Table of Contents, \n, Content)
            text_list = md_text.splitlines()
            toc_start = find_toc_start(text_list)
            toc_end = find_toc_end(text_list)

            updated_text_list = [
                *text_list[:toc_start],
                "",
                *toc_lines,
                "",
                *text_list[toc_end:],
            ]
            # Regex extracts anchor text from ancho
            # NOTE: There are edge cases with code blocks, bold, strikethroughs, etc...
            subtitle_text = re.sub(
                r"\[([^\[\]]+)\]\([^\(\)]+\)", r"\1", " ".join(updated_text_list[1:])
            )
            updated_md_text = "\n".join(updated_text_list) + "\n"

            # Update File
            with open(identifiers[i], "w") as file:
                file.write(updated_md_text)

        else:
            print("\n".join(toc_lines) + "\n")


if __name__ == "__main__":
    main()

    if params["type"] == "bear" and params["write"]:
        print("==================== [DONE] ====================")
        print(
            "[WARNING]: There still might be syncing issues with iCloud, for a precautionary measure, edit the note again."
        )
        print("To see your changes, please restart Bear!")
