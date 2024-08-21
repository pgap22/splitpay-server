#!/bin/bash

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin'

# Generate Prisma client
prisma generate

# Start the Waitress server
waitress-serve --host=0.0.0.0 app:app

# Pause the script for 100 seconds
sleep 100