from .datetime import *
from .math import *
from .qoi import *
from .statistics import *
from .tests import *
from .vtcodes import *
from .collections import *

def relative_path(prefix: str, suffix: str) -> str:
    BACKSLASH = "\\"
    return prefix.replace(BACKSLASH, "/").rsplit("/", 1)[0] + suffix
