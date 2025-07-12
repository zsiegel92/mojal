# python call_mojo_from_python_locally.py
import max.mojo.importer # noqa: F401
import sys

sys.path.insert(0, "")

import mojo_module # type: ignore

print(mojo_module.factorial(5))