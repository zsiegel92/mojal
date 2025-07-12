import modal

image = (
    modal.Image.from_registry("ubuntu:22.04", add_python="3.12")
    .apt_install(
        "build-essential", "curl", "file"
    )  # Full build toolchain including g++, make, etc.
    .pip_install("uv")
    .run_commands("uv pip install --compile-bytecode --system modal")
    .run_commands(
        # Install Pixi
        "curl -fsSL https://pixi.sh/install.sh | sh"
    )
    .env({"PATH": "/root/.pixi/bin:$PATH"})  # Add pixi to PATH
    .add_local_dir(
        "mojo_app",
        remote_path="/mojo_app",
        copy=True,
        ignore=["**/.pixi/*"],
    )
    .add_local_dir(
        "python_app",
        remote_path="/python_app",
        copy=True,
    )
    .run_commands(
        [
            # Set up the Mojo project with Pixi
            "cd /mojo_app && /root/.pixi/bin/pixi install",
            # Build the Mojo shared library
            "cd /mojo_app && /root/.pixi/bin/pixi run mojo build mojo_module.mojo --emit shared-lib",
            # Verify the build and check file type
            "ls -la /mojo_app/mojo_module.so",
            "file /mojo_app/mojo_module.so",
            # "head -c 20 /mojo_app/mojo_module.so | xxd",
        ]
    )
)

app = modal.App(name="hello-mojal", image=image)


@app.function()
def hello_world():
    import sys
    import os

    print("Using pre-built Mojo module...")

    # Check if the pre-built shared library exists
    if os.path.exists("/mojo_app/mojo_module.so"):
        print("Found pre-built Mojo shared library!")
    else:
        print("Pre-built Mojo shared library not found!")
        return

    # Add mojo_app directory to Python path
    sys.path.insert(0, "/mojo_app")

    # Import the compiled mojo module
    import mojo_module  # type: ignore

    print("Calling factorial(5)...")
    result = mojo_module.factorial(5)
    print(f"factorial(5) = {result}")

    return result


# python -m modal run python_app/main.py
@app.local_entrypoint()
def main():
    hello_world.remote()
