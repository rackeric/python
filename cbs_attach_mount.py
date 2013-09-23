##
## cbs_attach_mount.py
##
## Installing pyrax and needed dependencies:
##      http://docs.rackspace.com/sdks/guide/content/python.html
##      http://www.pip-installer.org/en/latest/installing.html
##      https://github.com/rackspace/pyrax/blob/master/docs/installing_pyrax.md
##

import pyrax
import os

# Variables to set
# Soon can use RBAC to set a limited access user
username = ""
API_key = ""
cbs_uuid = ""
cbs_device = "/dev/xvdb"
cbs_device_partition = "/dev/xvdb1"
cbs_mnt_point = "/mnt/cbs"
cs_instance = ""
region = "IAD"

# set identity type and credentials
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(username, API_key)

# Set Region for Cloud Block Storage
cbs = pyrax.connect_to_cloud_blockstorage(region = region)
vol = cbs.get(cbs_uuid)
print "----- Cloud Block Storage -----"
print vol

# Set Region for Cloud Server
cs = pyrax.connect_to_cloudservers(region = region)
instance = cs.servers.get(cs_instance)
print "----- Cloud Server -----"
print instance

# ATTACHE THE VOLUME
vol.attach_to_instance(instance, mountpoint=cbs_device)

print "-Waiting for CBS volume creation. Will take several minutes depending on size."
pyrax.utils.wait_until(vol,
                        att = "status", \
                        desired = "in-use", \
                        callback = None, \
                        interval = 10, \
                        attempts = 25, \
                        verbose = True, \
                        verbose_atts = None)


print "Volume Attached."

# Mount the CBS to the mount point
if (os.system("mount " + cbs_device_partition + " " + cbs_mnt_point)):
  print "Volume Mounted."

# SUCCESS NOTIFICATION
# wanted: email notices
print "SUCCESS!"

