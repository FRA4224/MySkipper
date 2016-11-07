#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : log.py
# Author  : Nicolas ISAERT
# Date    : 18/01/2016
# Version : 1.0 - Created
#
#------------------------------------------------

import time

#------------------------------------------------
def Init():
  
  pass

#------------------------------------------------
def WriteLine(Line):
  fichier = open("log.txt", "a")
  Timelog = time.strftime("%d/%m/%y %H:%M:%S",time.localtime())
  if Line[len(Line)-1] == "\n":
    fichier.write(Timelog + ": " + Line)
  else:
    fichier.write(Timelog + ": " + Line +"\n")
  fichier.close()

#------------------------------------------------
