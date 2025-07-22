
import sys
from typing import NoReturn


def error(msg) -> NoReturn:
    print(f"Error\n\t{msg}")
    sys.exit(1)


