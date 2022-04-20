from .iterables import *
from .math import *
from .qoi import *
from .statistics import *
from .string_search import *
from .testing import *
from .vtcodes import *

def relative_path(prefix: str, suffix: str) -> str:
    BACKSLASH = "\\"
    return prefix.replace(BACKSLASH, "/").rsplit("/", 1)[0] + suffix
