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

Output:

```
(mojal) /.../mojal  python -m modal run python_app/main.py
✓ Initialized. View run at 
https://modal.com/apps/zsiegel92/main/ap-dEuUbfbXs4SAOkutnPEIQf
Building image im-oJ87h9pXVYWAz1eF9AjUSj

=> Step 0: FROM base

=> Step 1: COPY . /
Saving image...
Image saved, took 9.64s

Built image im-oJ87h9pXVYWAz1eF9AjUSj in 11.73s


✓ Created objects.
├── 🔨 Created mount 
│   /.../mojal/python_app/main.py
├── 🔨 Created mount /.../mojal/mojo_app
├── 🔨 Created mount /.../mojal/python_app
└── 🔨 Created function hello_world.
MAX SDK imported successfully!
Mojo module imported successfully!
Calling factorial(5) with interop...
factorial(5) = 120
```