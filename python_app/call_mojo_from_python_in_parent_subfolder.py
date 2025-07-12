# python python_app/call_mojo_from_python_in_parent_subfolder.py
import max.mojo.importer # noqa: F401
import sys

sys.path.insert(0, "mojo_app")

import mojo_module # type: ignore

print(mojo_module.factorial(5))