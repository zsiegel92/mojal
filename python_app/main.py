import modal

image = (
    modal.Image.from_registry(
        "ubuntu:22.04",
        add_python="3.12",
    )
    .apt_install(
        "build-essential",
        "curl",
        "file",
    )
    .pip_install("uv")
    .run_commands("uv pip install --compile-bytecode --system modal")
    .run_commands("curl -fsSL https://pixi.sh/install.sh | sh")
    .env({"PATH": "/root/.pixi/bin:$PATH"})  # Add pixi to PATH
    .add_local_dir(
        "mojo_app",
        remote_path="/mojo_app",
        copy=True,
        ignore=["**/.pixi/*"],
    )
    .run_commands(
        [
            "cd /mojo_app && /root/.pixi/bin/pixi install",
            "cd /mojo_app && /root/.pixi/bin/pixi run pip install max",
            "cd /mojo_app && /root/.pixi/bin/pixi run mojo build mojo_module.mojo --emit shared-lib",  # not necessary, but pre-building should be faster than compiling on demand
            "file /mojo_app/mojo_module.so", # shared library exists!
            # "cd /mojo_app && /root/.pixi/bin/pixi run mojo build factorial_standalone.mojo -o mojo_factorial",  # can also build a binary during image setup
            # "file /mojo_app/mojo_factorial",  # binary exists!
        ]
    )
    .add_local_dir(
        "python_app",
        remote_path="/python_app",
        copy=True,
    )
)

app = modal.App(name="hello-mojal", image=image)

@app.function()
def hello_world():
    import sys
    import os  # noqa: F401

    sys.path.insert(0, "/mojo_app")
    import max.mojo.importer  # type: ignore # noqa: F401

    print("MAX SDK imported successfully!")
    import mojo_module  # type: ignore

    print("Mojo module imported successfully!")
    print("Calling factorial(5) with interop...")
    result = mojo_module.factorial(5)
    print(f"factorial(5) = {result}")




# python -m modal run python_app/main.py
@app.local_entrypoint()
def main():
    hello_world.remote()
