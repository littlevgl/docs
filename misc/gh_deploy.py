#!/usr/bin/env python
 
import sys
import os
import re

langs = ['en']

  
def cmd(s):
  print("")
  print(s)
  print("----------------------------")
  r = os.system(s)
  if r != 0: 
    print("Exit update due to previous error")
    exit(-1)
    
cmd("git config alias.ci commit")
cmd("git config alias.br branch")
cmd("git restore .")
cmd("git clean -fdX")
cmd("git checkout master")
cmd("git pull origin master")
    
    
for br in [ 'dev', 'latest' ]:
  tmpdir = "_docs_tmp_" + re.sub('/', '_', br)
  urlpath = re.sub('release/', '', br)

  print("")
  print("Update " + br)
  print("========================")


  cmd("git checkout " + br + " --")
  cmd("git clean -fdX")
  cmd("git pull origin " + br)
  cmd("git submodule update")
  cmd("./build.py trans")
  os.system("git commit -am 'Rebuild'")
  cmd("rm -fr ../" + tmpdir)

  for l in langs:
    if os.path.isdir("./" + l):
      cmd("mkdir -p  ../" + tmpdir + "/" + l + "/")
      cmd("cp -r " + l +"/ ../" + tmpdir + "/")
    
  cmd("git checkout master")
  cmd("git clean -fdX")
  
  for l in langs:
    cmd("rm -rf " + urlpath + "/" + l)
  
  cmd("mkdir -p build_output")
  cmd("cp -r ../" + tmpdir + "/. build_output/" + urlpath + "/")
