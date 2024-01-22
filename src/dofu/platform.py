import sys


class Platform:
    def __hash__(self):
        return hash(self.__class__)

    def __call__(self):
        return False


class Any(Platform):
    def __call__(self):
        return True


class MacOS(Platform):
    def __call__(self):
        return sys.platform == "darwin"


class Linux(Platform):
    def __call__(self):
        return sys.platform.startswith("linux")


class Windows(Platform):
    def __call__(self):
        return sys.platform == "win32"


ANY = Any()
"""
Any platform.
"""

MACOS = MacOS()
"""
MacOS platform.
"""

LINUX = Linux()
"""
Linux platform.
"""

WINDOWS = Windows()
"""
Windows platform.
"""
