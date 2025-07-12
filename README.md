

# Setup locally

1. Install `pixi`: `curl -fsSL https://pixi.sh/install.sh | sh`
2. Init mojo project:
```
pixi init mojo_app \
  -c https://conda.modular.com/max-nightly/ -c conda-forge \
  && cd mojo_app
pixi add modular
# add `main.mojo`
mojo main.mojo
```