# Running Mojo from Modal

Mojo is interesting but it's hard to be creative with it without a good app deployment story. Deploying Python apps on Modal is easy and Mojo provides Python interop means we can run Mojo programs from a Modal app.

What would you run in Mojo? That's kind of like asking "when should I use a numpy matrix instead of a `list` of `list`s?" - any custom matrix arithmetic would be a good candidate, or an optimization algorithm.

# Install

```sh
cd python_app
uv venv
source .venv/bin/activate
uv sync
```

# Run

```sh
python -m modal run python_app/main.py
```
