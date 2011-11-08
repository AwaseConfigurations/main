from fabric.api import *
import socket
import paramiko
from fabric.contrib.console import confirm

env.user='ubuntu'
env.password='ubuntu'
env.hosts=['host1.local','host2.local', 'host3.local','host4.local','host5.local','host6.local','host7.local','host8.local','host9.local', 'host10.local','host11.local', 'host12.local','host13.local','host14.local','host15.local','host16.local','host17.local','host18.local','host19.local', 'host20.local','host21.local','host23.local','host24.local','host25.local','host26.local','host27.local','host28.local','host29.local','host30.local']
env.roledefs={
'servers' : ['host1.local','host2.local'],
'workstations' : ['host3.local','host4.local','host5.local','host6.local','host7.local','host8.local','host9.local', 'host10.local','host11.local', 'host12.local','host13.local','host14.local','host15.local','host16.local','host17.local','host18.local','host19.local', 'host20.local','host21.local','host23.local','host24.local','host25.local','host26.local','host27.local','host28.local','host29.local','host30.local']
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

@task(alias='init')
@with_settings(warn_only=True)
def init():
	if not _is_host_up(env.host, int(env.port)):
		return
	sshkey()
	#change_passwd('ubuntu','')

@task(alias='main')
@with_settings(warn_only=True)
def main():
	if not _is_host_up(env.host, int(env.port)):
                return
	#add_user(simo)
	auto_upgrade()
	if env.host=='host1.local':
		webserver_setup()
	add_reposource()
	config('add_unimulti')
	if env.host!='host1.local':
		install('ubuntu-desktop')
		bg()
		reboot()

@task(alias='put_file')
@with_settings(warn_only=True)
def put_file(path1, path2):
	if not _is_host_up(env.host, int(env.port)):
                return
	put(path1,path2)

@task(alias='get_file')
@with_settings(warn_only=True)
def get_file(path1, path2):
	if not _is_host_up(env.host, int(env.port)):
		return	
	get(path1,path2)

@task(alias='remove_file')
@with_settings(warn_only=True)
def remove_file(path):
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("rm -r %s" % path)

@task(alias='add_user')
@with_settings(warn_only=True)
def add_user(new_user):
	if not _is_host_up(env.host, int(env.port)):
		return	
	if sudo("useradd -m %s" % new_user).failed:
		print("User %s already exists!" % new_user)
		return
	sudo("mkdir /home/%s/public_html" % new_user)
	sudo("chown %s:%s /home/%s/public_html/" % (new_user,new_user,new_user))

@task(alias='change_passwd')
@with_settings(warn_only=True)
def change_passwd(user,passwod):
        if not _is_host_up(env.host, int(env.port)):
		return	
	sudo("echo -e '%s\n%s' | passwd %s" % (passwod,passwod,user))

@task(alias='del_user')
@with_settings(warn_only=True)
def delete_user(del_user):
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("deluser %s" % del_user)

@task(alias='config')
@with_settings(warn_only=True)
def config(conff):
	if not _is_host_up(env.host, int(env.port)):
		return
	if conff=='php_enable':
		if env.host=='host1.local':
			auto_install('php-enable-users')
	elif conff=='apache_userdir':
		if env.host=='host1.local':
			install_apache()
	elif conff=='add_unimulti':
		auto_install('add-unimulti')

@task
def status():
	if not _is_host_up(env.host, int(env.port)):
		return
	run("uptime")
	run("uname -a")

@task(alias='shutdown')
def shut_down():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("shutdown -P 0")

@task
def reboot():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("shutdown -r 0")

@task(alias='install')
@with_settings(warn_only=True)
def install(package):
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
	if sudo("apt-get -y install %s" % package).failed:
		local("echo FAIL "+env.host+": failed to install %s $(date) >> ~/fail.log" % package)
		for i in range(1,3):
			sudo("apt-get update")
                    	sudo("apt-get -y install %s" % package)

@task
def uninstall(package):
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get remove %s" % package)

@task
def update():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")

@task(alias='upgrade')
@with_settings(warn_only=True)
def upgrade():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
	sudo("apt-get -y upgrade")

@task(alias='auto_install')
@with_settings(warn_only=True)
def auto_install(package): # this will auto answer "yes" to all and keep old config files
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
	sudo('apt-get install -o Dpkg::Options::="--force-confold" --force-yes -y %s' % package)

@task(alias='auto_upgrade')
@with_settings(warn_only=True)
def auto_upgrade():
        if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
        sudo('apt-get upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

@task(alias='auto_dist_upgrade')
@with_settings(warn_only=True)
def auto_dist_upgrade():
        if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
        sudo('apt-get dist-upgrade -o Dpkg::Options::="--force-confold" --force-yes -y')

@task(alias='release_upgrade')
@with_settings(warn_only=True)
def release_upgrade():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
	sudo("apt-get upgrade")
	sudo("apt-get install update-manager-core")
	sudo("do-release-upgrade")

@task
def add_reposource():
        if not _is_host_up(env.host, int(env.port)):
		return
	with cd("/etc/apt/sources.list.d/"):
		sudo("echo deb http://host1.local/~ubuntu/ natty main >> repository.list")
		# remove duplicates:
		sudo("sort -u repository.list > repository.list.new")
		sudo("cat repository.list.new > repository.list")
		sudo("rm repository.list.new")
		
@task
@hosts('host1.local')
def install_apache():
	if not _is_host_up(env.host, int(env.port)):
		return
	sudo("apt-get update")
	sudo("apt-get -y install apache2")
	sudo("a2enmod userdir")
	sudo("/etc/init.d/apache2 restart")

@task(alias='webserver_setup')
@hosts('host1.local')
@with_settings(warn_only=True)
def webserver_setup():
	if not _is_host_up(env.host, int(env.port)):
		return
	install_apache()
	install('php5')
	reprepro_setup()
	clonegit()
	add_reposource()
	add_to_repo()
	config('php_enable')
	sudo("/etc/init.d/apache2 restart")

@task
@hosts('host1.local')
def reprepro_setup_old():
	if not _is_host_up(env.host, int(env.port)):
		return
	with settings(hide('warnings','running','stdout','stderr'),warn_only=True):
		if run("reprepro -h").failed:
			with settings(show('warnings','running','stdout','stderr'),warn_only=True):
				sudo("apt-get update")
				sudo("apt-get -y install reprepro")
				run("mkdir -p public_html/conf")
				run("echo Origin: Awase > public_html/conf/distributions")
				run("echo Codename: natty > public_html/conf/distributions")
				run("echo Label: Awase-All >> public_html/conf/distributions")
				run("echo Suite: stable >> public_html/conf/distributions")
				run("echo Version: 0.1 >> public_html/conf/distributions")
				run("echo Architectures: i386 amd64 source >> public_html/conf/distributions")
				run("echo Components: main non-free contrib >> public_html/conf/distributions")
				run("echo Description: AwaseConfigurations >> public_html/conf/distributions")
		else: 
			print("Reprepro is already installed")

@task(alias='reprepro_setup')
@hosts('host1.local')
@with_settings(warn_only=True)
def reprepro_setup():
	if not _is_host_up(env.host, int(env.port)):
                return
        sudo("apt-get update")
        sudo("apt-get -y install reprepro")	
	run("wget https://raw.github.com/AwaseConfigurations/main/master/scripts/reprepro_setup.sh")
	run("chmod +x reprepro_setup.sh")
	run("./reprepro_setup.sh")
	run("rm reprepro_setup.sh")
	

@task(alias='add_to_repo')
@hosts('host1.local')
@with_settings(warn_only=True)
def add_to_repo():
	if not _is_host_up(env.host, int(env.port)):
		return
	with cd('~/public_html/'):
		run("cp ~/main/packages/php/php-enable-users/php-enable-users_0.1_all.deb ~/public_html/")
		run("cp ~/main/packages/apt/add-unimulti/add-unimulti_0.1_all.deb ~/public_html/")
		run("reprepro includedeb natty add-unimulti_0.1_all.deb")			
		if run("reprepro includedeb natty php-enable-users_0.1_all.deb").failed:
			reprepro_setup()
			clonegit()
			run("cp ~/main/packages/php/php-enable-users/php-enable-users_0.1_all.deb ~/public_html/")
			run("cp ~/main/packages/apt/add-unimulti/add-unimulti_0.1_all.deb ~/public_html/")
			run("reprepro includedeb natty php-enable-users_0.1_all.deb")					
			run("reprepro includedeb natty add-unimulti_0.1_all.deb")

@task(alias='clonegit')
@hosts('host1.local')
@with_settings(warn_only=True)
def clonegit():
	if not _is_host_up(env.host, int(env.port)):
		return
	install('git')
	with cd('~/'):
		run("git clone https://github.com/AwaseConfigurations/main")

@task(alias='sshkey')
@with_settings(warn_only=True)
def sshkey():
	if not _is_host_up(env.host, int(env.port)):
		return
	if local('ssh-copy-id '+env.user+'@'+env.host).failed:
		local('ssh-keygen -N "" -q -f .ssh/id_rsa -t rsa')
		local('ssh-copy-id '+env.user+'@'+env.host)
		
	
@task(alias='bg')
@with_settings(warn_only=True)
def bg():
	if not _is_host_up(env.host, int(env.port)):
		return
	run("wget http://myy.haaga-helia.fi/~a0900094/awasebg.jpg")
	sudo("mv -b awasebg.jpg /usr/share/backgrounds/warty-final-ubuntu.png")

@with_settings(warn_only=True)
def bg_old():
	if not _is_host_up(env.host, int(env.port)):
                return
	if put("awasebg.jpg","/tmp/").failed:
		local("wget http://myy.haaga-helia.fi/~a0900094/awasebg.jpg")
		put("awasebg.jpg","/tmp/")
	sudo("cp /tmp/awasebg.jpg /usr/share/backgrounds/warty-final-ubuntu.png")

