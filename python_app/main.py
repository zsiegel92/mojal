import modal

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("build-essential")  # Full build toolchain including g++, make, etc.
    .pip_install("uv")
    .run_commands("uv pip install --compile-bytecode --system modal")
    .run_commands(
        "uv pip install --compile-bytecode --system modular --extra-index-url https://download.pytorch.org/whl/cpu  --index-url https://dl.modular.com/public/nightly/python/simple/  --index-strategy unsafe-best-match --prerelease allow"
    )
    .run_commands(
        [
            "uv pip freeze",
            'python -c "import sys; print(sys.path)"',
            'python -c "import max; print(max.__file__)" || echo "max import failed"',
            'python -c "import max.mojo; print(max.mojo.__file__)" || echo "max.mojo import failed"',
            'which g++ || echo "g++ not found"',
        ]
    )
    .add_local_dir(
        "mojo_app",
        remote_path="/",
        copy=True,
        ignore=["**/.pixi/*"],
    )
    .add_local_dir(
        "python_app",
        remote_path="/",
        copy=True,
    )
    .run_commands(["uv pip freeze"])
)

app = modal.App(name="hello-mojal", image=image)


@app.function()
def hello_world():
    import sys
    import os
    import subprocess

    print("Compiling Mojo module for Linux...")

    # Check if mojo CLI is available
    try:
        result = subprocess.run(["mojo", "--version"], capture_output=True, text=True)
        print("Mojo version:", result.stdout.strip())
    except FileNotFoundError:
        print("Mojo CLI not found!")
        return

    # Compile the Mojo module for Linux
    if os.path.exists("/mojo_module.mojo"):
        print("Compiling mojo_module.mojo...")
        result = subprocess.run(
            [
                "mojo",
                "build",
                "/mojo_module.mojo",
                "--emit",
                "shared-lib",
                "-o",
                "/mojo_module_linux.so",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("Mojo compilation failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return
        else:
            print("Mojo compilation successful!")

    # Add root directory to Python path
    sys.path.insert(0, "/")

    # Import the Linux-compiled mojo module
    import mojo_module_linux as mojo_module  # type: ignore

    print(mojo_module.factorial(5))


# python -m modal run python_app/main.py
@app.local_entrypoint()
def main():
    hello_world.remote()
