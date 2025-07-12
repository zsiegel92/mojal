curl -fsSL https://pixi.sh/install.sh | sh
cd /root/mojo_app
/root/.pixi/bin/pixi install
mojo build /root/mojo_app/main.mojo -o /root/main_mojo
