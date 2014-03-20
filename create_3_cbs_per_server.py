#!/usr/bin/env python
import pyrax

## USER VARIABLES ##
username = ""
API_key = ""

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "ORD")
# authenticate
pyrax.set_credentials(username, API_key)

# create objects
cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage

servers = cs.servers.list()

for server in servers:
	for count in 'h', 'i', 'j':
		#create cbs volume
		name = server.name + str(count)
		vol = cbs.create(name, size=1024, volume_type="SATA")
		print "-Waiting for CBS volume creation. Will take several minutes depending on size."
		pyrax.utils.wait_until(vol,
			att = "status", \
			desired = "available", \
			callback = None, \
			interval = 30, \
			attempts = 25, \
			verbose = True, \
			verbose_atts = None)
		print "-Attaching volume."
		mount = "/dev/xvd" + count
		vol.attach_to_instance(server, mountpoint=mount)
		
		print "-Waiting for CBS volume attaching. Will take several minutes depending on size."
		pyrax.utils.wait_until(vol,
                		        att = "status", \
                        		desired = "in-use", \
                        		callback = None, \
                        		interval = 10, \
                        		attempts = 25, \
                        		verbose = True, \
                        		verbose_atts = None)
		print "Volume Attached to " + server.name
