from pkg_resources import get_distribution

from .markdowntoc import main

VERSION = get_distribution(__name__).version
