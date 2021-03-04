#!/usr/bin/python
# -*- coding: cp1252 -*-

# settings for global variables
# for modify_ddi.py script
#
# Version V1.0
# W. Zenk-Möltgen, 2020-11-12
#

profile_standardns = False
xmlfile_standardns = False
profile_noprefix = False
xmlfile_noprefix = False

xmlfile_standardnsddi = False
xmlfile_standardnsxsi = False

xmlfile_standardns_name = ""
xmlfile_standardns_prefix = ""
profile_standardns_name = ""
profile_standardns_prefix = "xxxx" # used to replace the standard namespace (not declared), if no -p option used to specify this
default_prefix = ""
scenario=0
nsmap={}

agency = "myagency"

outstatus = ''
resultonly=False
result=""

