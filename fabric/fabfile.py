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
        print('{host} down.'.format(host=host)
        )
    socket.setdefaulttimeout(original_timeout)
    return host_status

def put_file(path1, path2):
	if _is_host_up(env.host, int(env.port)) is True:
		# check maybe needed here: does the file already exist on remote path
		put(path1,path2)

def get_file(path1, path2):
	if _is_host_up(env.host, int(env.port)) is True:
		get(path1,path2)

def add_user(new_user):
	if _is_host_up(env.host, int(env.port)) is True:
		# check maybe needed here: does user already exist?
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
#		put('','')
#		run("")
#		sudo()

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
			if sudo("apt-get -y install %s" % package).failed:
				local("echo FAIL >> ~/fail.log")
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

def release_upgrade():
	if _is_host_up(env.host, int(env.port)) is True:
		with settings(warn_only=True):
			sudo("apt-get update")
			sudo("apt-get upgrade")
			sudo("apt-get install update-manager-core")
			sudo("do-release-upgrade")

def add_reposource():
        if _is_host_up(env.host, int(env.port)) is True:
		with cd("/etc/apt/sources.list.d/"):
			sudo("echo deb http://172.28.212.1/~ubuntu/repository natty main >> repository.list")
			# remove duplicates:
			sudo("sort -u repository.list > repository.list.new")
			sudo("cat repository.list.new > repository.list")
			sudo("rm repository.list.new")
		

def static_ip():
	run("echo auto lo > interfaces.static")
	run("echo iface lo inet loopback >> interfaces.static")
	run("echo   >> interfaces.static")
	run("echo auto eth0 >> interfaces.static")
	run("echo iface eth0 inet static >> interfaces.static")
	run("echo -n -e address\ >> interfaces.static")
	run("hostname -I >> interfaces.static")
	run("echo netmask 255.255.0.0 >> interfaces.static")
	run("echo network 172.28.0.0 >> interfaces.static")
	run("echo broadcast 172.28.255.255 >> interfaces.static")
	run("echo gateway 172.28.1.254 >> interfaces.static")
	sudo("cat /etc/network/interfaces > /etc/network/interfaces.old")
	sudo("cat interfaces.static > /etc/network/interfaces")
	run("rm interfaces.static")
	with settings(warn_only=True):
		sudo("/etc/init.d/networking restart")

@hosts('webserver')
def install_apache():
	sudo("apt-get update")
	sudo("apt-get install apache2")
	sudo("a2enmod userdir")
	sudo("/etc/init.d/apache2 restart")
	
@hosts('webserver')
def webserver_setup():
	install_apache()
	install(php5)
	#install(php-enable-users)
	sudo("/etc/init.d/apache2 restart")

@hosts('webserver')
def reprepro_setup():
	with settings(hide('warnings','running','stdout','stderr')warn_only=True):
		if run("reprepro -h").failed:
			with settings(show('warnings','running','stdout','stderr')warn_only=True):
				sudo("apt-get update")
				sudo("apt-get install reprepro")
				run("mkdir conf")
				run("echo Origin: Awase > conf/distributions")
				run("echo Label: Awase-All >> conf/distributions")
				run("echo Suite: stable >> conf/distributions")
				run("echo Version: 0.1 >> conf/distributions")
				run("echo Architectures: i386 amd64 source >> conf/distributions")
				run("echo Components: main non-free contrib >> conf/distributions")
				run("echo Description: AwaseConfigurations >> conf/distributions")
		else: 
			print("Reprepro is already installed")
