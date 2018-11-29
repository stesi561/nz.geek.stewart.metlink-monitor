#! /bin/bash



cd /home/luke/wc/nz.geek.stewart.metlink-monitor
source .env
src/read.py >> log/read.log 2>> log/read.err

