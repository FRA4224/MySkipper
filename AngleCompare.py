#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : display.py
# Author  : Nicolas ISAERT
# Date    : 10/12/2015
# Version : 1.0 - Created
#
#------------------------------------------------

import math

#------------------------------------------------
def Fonction(AngleRef, Angle):
   """
   HDM Cap magn�tique au format float
   BRG Rel�vement du prochain waypoint au format float
   COG Course On Ground au format float

   La fonction prend en param�tre un angle de r�f�rence (HDM) et l'angle � comparer
   Elle renvoie la diff�rence au format float entre l'angle de r�f�rence et l'angle � comparer
   Elle g�re notamment les valeurs proches de 360 ou 0
   """

   return(math.degrees(math.asin(math.sin(math.radians(Angle))))-math.degrees(math.asin(math.sin(math.radians(AngleRef)))))

#------------------------------------------------

print Fonction(360.0,350.0)
#print (math.degrees(math.asin(math.sin(math.radians(350.0)))))