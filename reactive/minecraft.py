import shutil
import urllib.request
import os
import os.path

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install
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
        stop()
    install_workload(config)
    if need_restart:
        start()


@hook("config-changed")
def config_changed():
    config = hookenv.config()
    need_restart = False
    if host.service_running("minecraft"):
        need_restart = True
    if need_restart:
        stop()

    if not os.path.exists("/opt/minecraft"):
        os.makedirs("/opt/minecraft")
    render(source="config",
           target="/opt/minecraft/server.properties",
           owner="root",
           perms=0o644,
           context={"cfg": config, }
           )
    if need_restart:
        start()


@hook('start')
def start():
    config = hookenv.config()
    host.service_start("minecraft")
    hookenv.status_set('active', 'Ready')
    hookenv.open_port(config['port'])


@hook('stop')
def stop():
    host.service_stop("minecraft")
    hookenv.status_set('active', 'Stopped')


def install_workload(config):
    hookenv.status_set('maintenance', 'Installing java')
    apt_update()
    apt_install("openjdk-6-jre")

    hookenv.status_set('maintenance', 'Fetching minecraft')
    server_jar = urllib.request.urlopen("https://s3.amazonaws.com/Minecraft.Download/versions/1.8.8/minecraft_server.1.8.8.jar")
    hookenv.status_set('maintenance', 'Installing minecraft')
    if not os.path.exists("/opt/minecraft"):
        os.makedirs("/opt/minecraft")
    with open("/opt/minecraft/minecraft_server.jar", 'wb') as dest:
        dest.write(server_jar.read())
    render(source="minecraft",
           target="/etc/init/minecraft.conf",
           owner="root",
           perms=0o644,
           context={},
           )
    shutil.copy("opt/eula.txt", "/opt/minecraft/eula.txt")
    hookenv.status_set('maintenance', 'Minecraft installed')
