#!/usr/bin/python
#
# Creates a CS Server from a snapshot image
# Creates a CBS volume and attaches to new server 
#
# 20130411 - Eric Hernandez
#

import pyrax 
import time

## VALUES TO CHANGE
username = ""
API_key = ""
cs_snap_uuid = ""
cbs_snap_uuid = ""
new_server_name = "newserver"
new_volume_name = "newvolume"
flavorID = 2
cbs_size = 100

# authenticate
pyrax.set_credentials(username, API_key)

# create objects
cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage

# create CBS volumes
vol = cbs.create(new_volume_name, size=cbs_size, volume_type="SATA", snapshot_id = cbs_snap_uuid)
print "-Volume created."
print "  Volume ID: ", vol.id

# create CS server
server = cs.servers.create(new_server_name, cs_snap_uuid, flavorID)
print "-Server created."
print "  Server ID: ", server.id
print "  Admin password: ", server.adminPass

# wait for volume to build
mountpoint = "/dev/xvdb"
print "-Waiting for CBS volume."
pyrax.utils.wait_until(vol, att = "status", desired = "available", callback = None, interval = 30, attempts = 25, verbose = True, verbose_atts = None)

# finally, attach the CBS volume
vol.attach_to_instance(server, mountpoint=mountpoint)
print "-Volume is now attached."
