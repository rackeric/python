#!/usr/bin/python
#
# List images, including snapshots
#
# 20130411 - Eric Hernandez
#

import pyrax

username = ""
API_key = ""

pyrax.set_credentials(username, API_key)

cs = pyrax.cloudservers

imgs = cs.images.list()
for img in imgs:
    print img.name, "  -- ID:", img.id
