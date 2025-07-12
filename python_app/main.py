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
            # Install MAX SDK for Python interop
            "cd /mojo_app && /root/.pixi/bin/pixi run pip install max",
            # Build the Mojo shared library for the container architecture
            "cd /mojo_app && /root/.pixi/bin/pixi run mojo build mojo_module.mojo --emit shared-lib",
            # Also build a standalone executable for fallback
            "cd /mojo_app && /root/.pixi/bin/pixi run mojo build factorial_standalone.mojo -o mojo_factorial",
            # Verify the builds and check file types
            "ls -la /mojo_app/mojo_module.so /mojo_app/mojo_factorial",
            "file /mojo_app/mojo_module.so",
            "file /mojo_app/mojo_factorial",
            # Test that MAX SDK is available
            "cd /mojo_app && /root/.pixi/bin/pixi run python -c 'import max.mojo.importer; print(\"MAX SDK available\")'",
        ]
    )
)

app = modal.App(name="hello-mojal", image=image)


@app.function()
def hello_world():
    import sys
    import os


    # Check if the pre-built shared library exists
    if not os.path.exists("/mojo_app/mojo_module.so"):
        raise Exception('Pre-built Mojo shared library not found!')

    # Add mojo_app directory to Python path
    sys.path.insert(0, "/mojo_app")

    try:
        # Import MAX SDK for Mojo interop
        import max.mojo.importer  # type: ignore

        print("MAX SDK imported successfully!")

        # Import the compiled mojo module
        import mojo_module  # type: ignore

        print("Mojo module imported successfully!")

        print("Calling factorial(5)...")
        result = mojo_module.factorial(5)
        print(f"factorial(5) = {result}")

        return result
    except Exception as e:
        print(f"Failed to import or use Mojo module: {e}")
        print("Falling back to binary execution...")

        # Fallback: try to execute the precompiled binary
        import subprocess

        try:
            # Check if the binary exists
            if os.path.exists("/mojo_app/mojo_factorial"):
                print("Found precompiled Mojo binary, executing...")
                result = subprocess.run(
                    ["/mojo_app/mojo_factorial"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print("Mojo binary output:", result.stdout)
                return result.stdout.strip()
            else:
                print("No precompiled binary found, trying to run source...")
                # Try to run the source file directly
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        "cd /mojo_app && /root/.pixi/bin/pixi run mojo mojo_module.mojo",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                print("Mojo source output:", result.stdout)
                return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Binary execution failed: {e}")
            print("stderr:", e.stderr)
            return None


# python -m modal run python_app/main.py
@app.local_entrypoint()
def main():
    hello_world.remote()
