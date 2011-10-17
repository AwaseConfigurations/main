from fabric.api import *

env.hosts=['webserver', 'fileserver', 'ws1', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11', 'ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19', 'ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
env.roledefs={
	'servers'=['webserver','fileserver']
	'workstations'=['ws1', 'ws3','ws4','ws5','ws6','ws7','ws8','ws9', 'ws10','ws11', 'ws12','ws13','ws14','ws15','ws16','ws17','ws18','ws19', 'ws20','ws21','ws23','ws24','ws25','ws26','ws27','ws28','ws29','ws30']
}

def put_file(path1, path2):
	put(path1,path2)

def get_file(path1, path2):
	get(path1,path2)

def add_user(new_user):
	sudo("adduser %s" % new_user)

def delete_user(del_user):
	sudo("deluser %s" % del_user)

def config(conff):
	local('')
	put('/packages/','')
	run("")
	sudo("gdebi -n ")	

def status():
	run("")

def shut_down():
	sudo("shutdown -P 0")

def reboot():
	sudo("shutdown -r 0")

def install(package):
	sudo("apt-get install %s" % package)

def uninstall(package):
	sudo("apt-get remove %s" % package)

def update():
	sudo("apt-get update")

def upgrade():
	sudo("apt-get -y upgrade")

 
