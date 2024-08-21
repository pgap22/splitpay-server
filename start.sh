#!/bin/bash

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin'

# Generate Prisma client
prisma generate

# Start the Waitress server
waitress-serve --listen 0.0.0.0:5001 app:app
