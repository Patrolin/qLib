from .colors import *
from .diff import *
from .integration import *
from .iterables import *
from .math import *
from .qoi import *
from .statistics import *
from .testing import *

def relative_path(prefix: str, suffix: str) -> str:
    BACKSLASH = "\\"
    return prefix.replace(BACKSLASH, "/").rsplit("/", 1)[0] + suffix
