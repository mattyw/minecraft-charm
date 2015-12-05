import shutil
import os
import os.path

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install, install_remote
from charms.reactive import hook


@hook('install')
def install():
    config = hookenv.config()
    install_workload(config)


@hook('upgrade-charm')
def upgrade():
    service = "minecraft"
    need_restart = False
    if host.service_running(service):
        need_restart = True
    if need_restart:
        host.service_stop(service)
    install_workload(config)
    if need_restart:
        host.service_start(service)


@hook('start')
def start():
    host.service_start("minecraft")
    hookenv.status_set('active', 'Ready')
    hookenv.open_port(25565)


@hook('stop')
def stop():
    host.service_stop("minecraft")
    hookenv.status_set('active', 'Stopped')


def install_workload(config):
    hookenv.status_set('active', 'Installing java')
    apt_update()
    apt_install("openjdk-6-jre")

    hookenv.status_set('active', 'Fetching minecraft')
    install_remote("https://s3.amazonaws.com/Minecraft.Download/versions/1.8.8/minecraft_server.1.8.8.jar")
    hookenv.status_set('active', 'Installing minecraft')
    render(source="minecraft",
        target="/etc/init/minecraft.conf",
        owner="root",
        perms=0o644,
        context={},
        )
    if not os.path.exists("/opt/minecraft"):
        os.makedirs("/opt/minecraft")
    shutil.copy("opt/eula.txt", "/opt/minecraft/eula.txt")
    shutil.copy("fetched/minecraft_server.1.8.8.jar", "/opt/minecraft/minecraft_server.jar")
