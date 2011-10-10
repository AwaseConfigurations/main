from fabric.api import *

def putfile():
	put('/home/hng/testi.txt','/home/hngu/')

def getfile():
	get('/home/hngu/simo.txt','/home/hng/')

def host_name():
	run('hostname')



