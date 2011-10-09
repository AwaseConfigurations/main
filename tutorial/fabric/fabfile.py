from fabric.api import *

def putt():
	put('/home/hng/testi.txt','/home/hngu/')

def gett():
	get('/home/hngu/simo.txt','/home/hng/')

def add_user(new_user):
	run("sudo adduser %s" % new_user)

def delete_user(del_user):
	run("sudo deluser %s" % del_user)

