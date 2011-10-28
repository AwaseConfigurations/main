from fabric.api import *
import socket
import paramiko
from fabric.contrib.console import confirm

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
    new_timeout = 1
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('{host} down.'.format(
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
		sudo("useradd -m %s" % new_user)

def change_passwd(user):
        if _is_host_up(env.host, int(env.port)) is True:
                sudo("passwd %s" % new_user)

def delete_user(del_user):
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("deluser %s" % del_user)

#def config(conff):
#       Some function needed here that will first check if the config package
#       has already been installed and maybe then instead of install just
#       update to the latest version.Or maybe apt will take care of it  
#       as we will use it to install config packages?

#	if _is_host_up(env.host, int(env.port)) is True:
#		local('')
#		put('/packages/','')
#		run("")
#		sudo("gdebi -n ")

def status():
	if _is_host_up(env.host, int(env.port)) is True:
		run("uptime")
		run("uname -a")

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
			#sudo("apt-get -y install %s" % package)
			if sudo("apt-get -y install %s" % package).failed:
				for i in range(1,3):
					sudo("apt-get update")
                        		sudo("apt-get -y install %s" % package)
			# result = sudo("apt-get -y install %s" % package, capture=True)
			# if result.failed and not confirm("Install failed. Continue anyway?"):
			# abort("Aborting!")

def uninstall(package):
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("apt-get remove %s" % package)

def update():
	if _is_host_up(env.host, int(env.port)) is True:
		sudo("apt-get update")

def upgrade():
	if _is_host_up(env.host, int(env.port)) is True:
		 with settings(warn_only=True):
                        sudo("apt-get update")
			sudo("apt-get -y upgrade")

def auto_install(package): # this will auto answer "yes" to all and keep old config files
	if _is_host_up(env.host, int(env.port)) is True:
		with settings(warn_only=True):
			sudo("apt-get update")
			sudo('apt-get install -o Dpkg::Options::="--force-confold" --force-yes -y %s' % package)

def auto_upgrade():
        if _is_host_up(env.host, int(env.port)) is True:
                with settings(warn_only=True):
                        sudo("apt-get update")
                        sudo('apt-get upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

def auto_dist_upgrade():
        if _is_host_up(env.host, int(env.port)) is True:
                with settings(warn_only=True):
                        sudo("apt-get update")
                        sudo('apt-get dist-upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

def add_reposource():
        if _is_host_up(env.host, int(env.port)) is True:
                sudo("echo deb http://172.28.212.1/~ubuntu/repository natty main >> /etc/apt/sources.list.d/repository.list")


