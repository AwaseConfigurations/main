from fabric.api import *
import socket
import paramiko
from fabric.contrib.console import confirm

env.user='ubuntu'
env.password='ubuntu'
#env.hosts=['webserver', 'fileserver', 'ws1','ws2', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11', 'ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19', 'ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
#env.roledefs={
#'servers' : ['webserver','fileserver'],
#'workstations' : ['ws1','ws2', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11','ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19','ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
#}

env.hosts=['172.28.212.1','172.28.212.2','172.28.212.3','172.28.212.4','172.28.212.5','172.28.212.6','172.28.212.7','172.28.212.8','172.28.212.9','172.28.212.10','172.28.212.11','172.28.212.12','172.28.212.13','172.28.212.14','172.28.212.15','172.28.212.16','172.28.212.17','172.28.212.18','172.28.212.19','172.28.212.20','172.28.212.21','172.28.212.22','172.28.212.23','172.28.212.24','172.28.212.25','172.28.212.26','172.28.212.27','172.28.212.28','172.28.212.29','172.28.212.30']
env.roledefs={
'servers' : ['172.28.212.1','172.28.212.2'],
'workstations' : ['172.28.212.3','172.28.212.4','172.28.212.5','172.28.212.6','172.28.212.7','172.28.212.8','172.28.212.9','172.28.212.10','172.28.212.11','172.28.212.12','172.28.212.13','172.28.212.14','172.28.212.15','172.28.212.16','172.28.212.17','172.28.212.18','172.28.212.19','172.28.212.20','172.28.212.21','172.28.212.22','172.28.212.23','172.28.212.24','172.28.212.25','172.28.212.26','172.28.212.27','172.28.212.28','172.28.212.29','172.28.212.30']
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

@task
def init():
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			#static_ip()
			#add_user(simo)
			#auto_upgrade()
			sshkey()
			change_passwd(ubuntu)
			if env.host=='172.28.212.1':
				webserver_setup()
			add_reposource()
			config(add_unimulti)
			install(gnome)
			bg()

@task
def put_file(path1, path2):
	if _is_host_up(env.host, int(env.port)):
		# check maybe needed here: does the file already exist on remote path
		put(path1,path2)

@task
def get_file(path1, path2):
	if _is_host_up(env.host, int(env.port)):
		get(path1,path2)

@task
def add_user(new_user):
	if _is_host_up(env.host, int(env.port)):
		# check maybe needed here: does user already exist?
		sudo("useradd -m %s" % new_user)

@task
def change_passwd(user):
        if _is_host_up(env.host, int(env.port)):
                sudo("passwd %s" % new_user)

@task
def delete_user(del_user):
	if _is_host_up(env.host, int(env.port)):
		sudo("deluser %s" % del_user)

@task
#@hosts('172.28.212.1')
def config(conff):
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			if conff=='php_enable':
				if env.host=='172.28.212.1':
					install(php-enable-users)
			elif conff=='apache_userdir':
				if env.host=='172.28.212.1':
					install_apache()
			elif conff=='add_unimulti':
				install(add-unimulti)

@task
def status():
	if _is_host_up(env.host, int(env.port)):
		run("uptime")
		run("uname -a")

@task
def shut_down():
	if _is_host_up(env.host, int(env.port)):
		sudo("shutdown -P 0")

@task
def reboot():
	if _is_host_up(env.host, int(env.port)):
		sudo("shutdown -r 0")

@task
def install(package):
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			sudo("apt-get update")
			if sudo("apt-get -y install %s" % package).failed:
				local("echo FAIL "+env.host+" >> ~/fail.log")
				for i in range(1,3):
					sudo("apt-get update")
                        		sudo("apt-get -y install %s" % package)

@task
def uninstall(package):
	if _is_host_up(env.host, int(env.port)):
		sudo("apt-get remove %s" % package)

@task
def update():
	if _is_host_up(env.host, int(env.port)):
		sudo("apt-get update")

@task
def upgrade():
	if _is_host_up(env.host, int(env.port)):
		 with settings(warn_only=True):
                        sudo("apt-get update")
			sudo("apt-get -y upgrade")

@task
def auto_install(package): # this will auto answer "yes" to all and keep old config files
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			sudo("apt-get update")
			sudo('apt-get install -o Dpkg::Options::="--force-confold" --force-yes -y %s' % package)

@task
def auto_upgrade():
        if _is_host_up(env.host, int(env.port)):
                with settings(warn_only=True):
                        sudo("apt-get update")
                        sudo('apt-get upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

@task
def auto_dist_upgrade():
        if _is_host_up(env.host, int(env.port)):
                with settings(warn_only=True):
                        sudo("apt-get update")
                        sudo('apt-get dist-upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

@task
def release_upgrade():
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			sudo("apt-get update")
			sudo("apt-get upgrade")
			sudo("apt-get install update-manager-core")
			sudo("do-release-upgrade")

@task
def add_reposource():
        if _is_host_up(env.host, int(env.port)):
		with cd("/etc/apt/sources.list.d/"):
			sudo("echo deb http://172.28.212.1/~ubuntu/repository awase main >> repository.list")
			# remove duplicates:
			sudo("sort -u repository.list > repository.list.new")
			sudo("cat repository.list.new > repository.list")
			sudo("rm repository.list.new")
		
@task
def static_ip():
	if _is_host_up(env.host, int(env.port)):
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

@task
#@hosts('webserver')
@hosts('172.28.212.1')
def install_apache():
	if _is_host_up(env.host, int(env.port)):
			sudo("apt-get update")
			sudo("apt-get install apache2")
			sudo("a2enmod userdir")
			sudo("/etc/init.d/apache2 restart")

@task	
#@hosts('webserver')
@hosts('172.28.212.1')
def webserver_setup():
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			install_apache()
			install(php5)
			reprepro_setup()
			gitclone()
			add_reposource()
			add_to_repo('main/packages/php/php-enable-users/php-enable-users_0.1_all.deb')
			add_to_repo('main/packages/apt/add-unimulti/add-unimulti_0.1_all.deb')
			config(php_enable)
			sudo("/etc/init.d/apache2 restart")

@task
#@hosts('webserver')
@hosts('172.28.212.1')
def reprepro_setup():
	if _is_host_up(env.host, int(env.port)):
		with settings(hide('warnings','running','stdout','stderr'),warn_only=True):
			if run("reprepro -h").failed:
				with settings(show('warnings','running','stdout','stderr'),warn_only=True):
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

@task(alias='atr')
#@hosts('webserver')
@hosts('172.28.212.1')
def add_to_repo(path):
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			if run("reprepro -Vb repository/ includedeb awase %s" % path).failed:
				reprepro_setup()
				clonegit()
				path='main/packages/php/php-enable-users/php-enable-users_0.1_all.deb'
				run("reprepro -Vb . includedeb awase %s" % path)
	
@task
@hosts('172.28.212.1')
def clonegit():
	if _is_host_up(env.host, int(env.port)):
		with settings(warn_only=True):
			install(git)
			run("git clone https://github.com/AwaseConfigurations/main")

@task
def sshkey():
	if _is_host_up(env.host, int(env.port)):
		if local('ssh-copy-id '+env.user+'@'+env.host).failed:
			local('ssh-keygen -N "" -q -f .ssh/id_rsa -t rsa')
			local('ssh-copy-id '+env.user+'@'+env.host)
		
	
@task
def bg():
	if _is_host_up(env.host, int(env.port)):
		if put("awasebg.jpg","/tmp/").failed
			local("wget http://myy.haaga-helia.fi/~a0900094/awasebg.jpg")
			put("awasebg.jpg","/tmp/")
		sudo("cp /tmp/awasebg.jpg /usr/share/backgrouds/warty-final-ubuntu.png")
