#!/usr/bin/python
# -*- coding: cp1252 -*-

# settings for global variables
# for modify_ddi.py script
#
# Version V1.0
# W. Zenk-Möltgen, 2020-11-12
#
 # /*
 # * Copyright ©2021 CESSDA ERIC (support@cessda.eu)
 # *
 # * Licensed under the Apache License, Version 2.0 (the "License");
 # * you may not use this file except in compliance with the License.
 # * You may obtain a copy of the License at
 # *
 # *     http://www.apache.org/licenses/LICENSE-2.0
 # *
 # * Unless required by applicable law or agreed to in writing, software
 # * distributed under the License is distributed on an "AS IS" BASIS,
 # * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # * See the License for the specific language governing permissions and
 # * limitations under the License.
 # */

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

