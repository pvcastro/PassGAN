#!/usr/bin/env bash

#for file in $(find /opt/BreachCompilation -type f)
#do

cat /media/discoD/Mestrado/NoLeak/leak00.txt | grep -E -o \"^[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}+[\:\;][A-Za-z0-9!@#$%^&*()+]+$\" | sed \"s/\;\|\:/,/\" | sed \"s/.*,/\L&/\"

#done
