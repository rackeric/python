#!/usr/bin/python

import pyrax 
import time

username = "utcodemonkey"
API_key = "25136ca5cbe07aa925da1ee2f232aa5a"

pyrax.set_credentials(username, API_key)

cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage

## VALUES TO CHANGE
cs_snap_uuid = "039a39dc-3000-4751-b79f-f7158772cf51"
cbs_snap_uuid = "7a97fc49-5200-4e7d-8a95-3d3d4cd119e6"
new_server_name = "newserver"
new_volume_name = "newvolume"
flavorID = 2
cbs_size = 100

# create CBS volumes
vol = cbs.create(new_volume_name, size=cbs_size, volume_type="SATA", snapshot_id = cbs_snap_uuid)
print "-Volume created."
print "  Volume ID: ", vol.id

# create CS server
server = cs.servers.create(new_server_name, cs_snap_uuid, flavorID)
print "-Server created."
print "  Server ID: ", server.id
print "  Admin password: ", server.adminPass

# wait for networks to be assigned
#while not (server.networks):
#	server = cs.servers.get(server.id)
#	time.sleep(10)

# wait for volume to build
mountpoint = "/dev/xvdb"
print "-Waiting for CBS volume."
pyrax.utils.wait_until(vol, att = "status", desired = "available", callback = None, interval = 30, attempts = 25, verbose = True, verbose_atts = None)

# finally, attach the CBS volume
vol.attach_to_instance(server, mountpoint=mountpoint)
print "-Volume is now attached."
