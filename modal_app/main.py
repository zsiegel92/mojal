import modal

image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install("uv")
    .add_local_file(
        "pyproject.toml",
        remote_path="/root/pyproject.toml",
        copy=True,
    )
    .run_commands("uv pip install --compile-bytecode --system -r /root/pyproject.toml")
    .pip_install("modal-client")
    .add_local_dir(
        "mojo_app",
        remote_path="/mojo_app",
        copy=True,
    )
    .add_local_dir(
        "modal_app",
        remote_path="/modal_app",
        copy=True,
    )
    .run_commands(
        [
            "mkdir -p /mojo_app",
            "touch /mojo_app/testing.txt",
        ]
    )
)

app = modal.App(name="hello-world")


@app.function()
def hello_world():
    import os

    print(os.listdir("/mojo_app"))
    print(os.listdir("/modal_app"))

if __name__ == "__main__":
    app.run()
