from fabric.api import *
import socket
import paramiko

#webserver='172.28.212.1'
#fileserver='172.28.212.2'
#ws1='172.28.212.3'
#ws2='172.28.212.4'
#ws3='172.28.212.5'

env.user='ubuntu'
env.password='ubuntu'
env.hosts=['webserver', 'fileserver', 'ws1','ws2', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11', 'ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19', 'ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
env.roledefs={
'servers' : ['webserver','fileserver'],
'workstations' : ['ws1','ws2', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11','ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19','ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
}

def _is_host_up(host, port):
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 3
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
        )
    socket.setdefaulttimeout(original_timeout)
    return host_status

def put_file(path1, path2):
	if _is_host_up(env.host, int(env.port)) is True:
		put(path1,path2)

def get_file(path1, path2):
	if _is_host_up(env.host, int(env.port)) is True:
		get(path1,path2)

def add_user(new_user):
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("adduser %s" % new_user)

def delete_user(del_user):
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("deluser %s" % del_user)

#def config(conff):
#	if _is_host_up(env.host, int(env.port)) is True:
#		local('')
#		put('/packages/','')
#		run("")
#		sudo("gdebi -n ")

def status():
	if _is_host_up(env.host, int(env.port)) is True:
		run("uptime")

def shut_down():
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("shutdown -P 0")

def reboot():
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("shutdown -r 0")

def install(package):
	if _is_host_up(env.host, int(env.port)) is True:
		with settings(warn_only=True):
			sudo("apt-get update")
			sudo("apt-get -y install %s" % package)

def uninstall(package):
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("apt-get remove %s" % package)

def update():
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("apt-get update")

def upgrade():
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("apt-get -y upgrade")
