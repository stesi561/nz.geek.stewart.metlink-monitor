#! /bin/bash



cd /home/luke/wc/nz.geek.stewart.metlink-monitor
pipenv run src/read.py >> log/read.log 2>> log/read.err

