#!/usr/bin/python

import pyrax

username = "utcodemonkey"
API_key = "25136ca5cbe07aa925da1ee2f232aa5a"

pyrax.set_credentials(username, API_key)

cs = pyrax.cloudservers

imgs = cs.images.list()
for img in imgs:
    print img.name, "  -- ID:", img.id
