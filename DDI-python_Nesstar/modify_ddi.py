#!/usr/bin/python
# -*- coding: cp1252 -*-

# modify a DDI xml file 
# usage
# python modify_ddi.py -x <xmlfile> 
#
# needs global_vars.py present
#
# Version history
# V1.0 W. Zenk-Möltgen, 2020-11-12


pname = 'modify_ddi.py'
pdescription = 'Python script to modify a DDI xmlfile'
pversion = '1.0'
pdate = '2020-11-12'
pauthor = 'W. Zenk-Möltgen'

import sys, getopt
import datetime
import os.path
from plumbum import local
from lxml import etree, isoschematron

import global_vars as g
#from schematron import createschematron, getstandardns


        
def checkns(xfile):
    #check if xml file uses a standard namespace: xmlfile_standardns
    # and if xml file has elements with no prefix: xmlfile_noprefix

    #set the g.default_prefix if g.profile_standardns_name found in ns
    
    # load the document to be tested
    xml_doc = etree.parse(local.path(xfile))
    
    root = xml_doc.getroot()
    prefixmap = {}
    for n1 in root.nsmap:
        if n1 is None:
            g.outstatus += 'XML file uses standard namespace ' + root.nsmap[n1] + '\n'
            g.xmlfile_standardns = True
            g.xmlfile_standardns_name = root.nsmap[n1]
        else:
            prefixmap[n1] = root.nsmap[n1]
        if root.nsmap[n1]==g.profile_standardns_name:
            g.default_prefix=n1
    
    nodes = xml_doc.xpath('//*', namespaces=prefixmap)
    for node in nodes:
        if node.prefix == None:
            g.xmlfile_noprefix = True
            g.outstatus += 'XML file uses elements with no prefix \n'
            break 

    

def CLASS(*args): # class is a reserved word in Python
    return {"class":' '.join(args)}

def getfilefrompath(filewithpath):

    filewithoutpath = ''
    if not filewithpath=='':
        elements = filewithpath.split("\\")
        for element in elements:
            if not element == '':
                filewithoutpath = element
                
    return filewithoutpath
                        

    

# validation

def domodification(xfile, tfile, efile):
    
    from xml.etree import ElementTree as ET    
    from xml.etree.ElementTree import ElementTree 
    # load the document 
    xml_doc = etree.parse(local.path(xfile))

    # modify
    if g.xmlfile_noprefix: 
        rt = xml_doc.getroot()
        if rt.tag == "{ddi:instance:3_2}DDIInstance":
            print(rt.tag + " changed to DDIInstance")
            rt.tag = "DDIInstance"
        elif rt.tag == "{ddi:codebook:2_5}codeBook":
            print(rt.tag + " changed to codeBook")
            rt.tag = "codeBook"
    
    #namespace = "{" + g.xmlfile_standardns_name + "}" 
    #print(namespace)
    
    #add agency to IDNo
    idno = rt.xpath('.//*[local-name() = "IDNo"]')
    for i in idno:
        i.set("agency", g.agency)
        g.outstatus += "agency added to IDNo \n"
        break
    
	# write to target file
    if not tfile== '':
        ET.register_namespace('', g.xmlfile_standardns_name) #to remove any namespaces
        tree = ElementTree(rt)
        tree.write(open(tfile,'wb'), xml_declaration=True,encoding='utf-8') # , default_namespace=g.xmlfile_standardns_name)
        #f = open(tfile, "wb") 
        #f.write(rt.tag)
        #f.close()

        
    # validate
    is_valid = True

    g.outstatus += "\n"
    if is_valid:
        g.outstatus += "Result: OK \n"
        g.result="OK"
    else:
        g.outstatus += "Result: Error \n"
        g.result="Error"
        if not efile== '':
            g.outstatus += "(see errorfile for details)\n"
            
    # write to errorfile 
    if not efile== '':
        if not is_valid:
            f = open(efile, "wb") 
            f.write(schematron.validation_report)
            f.close()


# main 

def main(argv):
   
   now = datetime.datetime.now()
   outdatetime = (now.strftime("%Y-%m-%d %H:%M:%S"))

        
   xmlfile = ''
   outputfile = ''
   targetfile = ''
   errorfile = ''
   prefix = ''
   usagenote = 'usage: modify_ddi.py -x <xmlfile>  \n'
   
   usagenote += 'for help use: modify_ddi.py -h \n' 
   
   # check parameters
   try:
      opts, args = getopt.getopt(argv,"hx:o:e:p:a:ri",["xmlfile=","outputfile=","errorfile=","prefix=","agency="])
   except getopt.GetoptError:
      print(usagenote)
      sys.exit(2)

   # show header output
   outheader = '#############################################################\n'
   outheader += '### ' + pname + ' \n'
   outheader += '### ' + pdescription + ' \n'
   outheader += '### Version ' + pversion + ' ' + pdate + ' \n'
   outheader += '### Author: ' + pauthor + ' \n'
   outheader += '###\n'
   outheader += '### ' + outdatetime + '\n'
   outheader += '###\n'
   outheader += '#############################################################\n'
   if not g.resultonly:
       print(outheader)

   
   for opt, arg in opts:
      if opt == '-h':
         print(usagenote)
         print('usage: modify_ddi.py -x <xmlfile> \n')
         print('Options:')
         print(' -x xmlfile (required): path and filename for the xml file to be modified')
         print('\n')
         print(' -a agencyname: agencyname to be added to IDNo element')
         print('\n')
         print(' -h : show this help ')
         print('\n')
         print(' This script modifies a DDI xml file. ')
         print(' Use the -x option for this. ')
         sys.exit()
         
      elif opt in ("-x", "--xmlfile"):
         xmlfile = arg
      elif opt in ("-a", "--agency"):
         g.agency = arg
      

   
   
   #flag for starting the validation
   runthemodification=True
   g.outstatus=''
   
   # show parameter messages and check files
   if xmlfile== '':
       g.outstatus += 'Error: specify xmlfile \n'
       runthemodification=False
   else:
       if not os.path.isfile(xmlfile):
           g.outstatus += 'Error: xmlfile not found \n'
           runthemodification=False
       else:
           g.outstatus += 'XML file is ' + xmlfile + '\n'
   
   if not runthemodification:
       print(g.outstatus)
       print(usagenote)
       sys.exit()

   #if user specifies a prefix for substitution
   if not prefix== '':
       g.profile_standardns_prefix = prefix

   #do this only if at least xmlfile is specified and found:
   f_xmlfile = getfilefrompath(xmlfile)
       
   #set target output file
   if targetfile== '':
       targetfile = f_xmlfile + ".new"
   
   #set standard output 
   if outputfile== '':
       outputfile = f_xmlfile + ".out"
   
   if outputfile== '':
       g.outstatus += 'No output file \n'
   else:
       g.outstatus += 'Output file is '+ outputfile + '\n'

   #set standard error file
   if errorfile== '':
       errorfile = f_xmlfile + ".err"
   
   if errorfile== '':
       g.outstatus += 'No errorfile \n'
   else:
       g.outstatus += 'Errorfile is '+ errorfile + '\n'

   g.outstatus += '\n'
   
   #check for namespace usage
   checkns(f_xmlfile)
   
   #run modification
   g.outstatus += 'Start modification \n'
   domodification(xmlfile, targetfile, errorfile)

   if not g.resultonly:
       print(g.outstatus)
       if not outputfile== '':
            f = open(outputfile, "w")
            f.write(outheader)
            f.write(g.outstatus)
            f.close()
   else:
       print(g.result)

   sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])

