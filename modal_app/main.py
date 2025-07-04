import modal

image = modal.Image.debian_slim(python_version="3.13").pip_install("modal-client")

app = modal.App(name="hello-world")




@app.function()
def hello_world():
    print("Hello, World!")


if __name__ == "__main__":
    app.run()
