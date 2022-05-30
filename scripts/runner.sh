#!/usr/bin/env bash


myDir='/home/michael/lxconfig/scripts/test/'
options=$(cd ${myDir} && /bin/ls -d */ | cut -d " " -f 1)
#arr = ($options)

echo $options