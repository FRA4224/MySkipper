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
   HDM Cap magnétique au format float
   BRG Relèvement du prochain waypoint au format float
   COG Course On Ground au format float

   La fonction prend en paramètre un angle de référence (HDM) et l'angle à comparer
   Elle renvoie la différence au format float entre l'angle de référence et l'angle à comparer
   Elle gère notamment les valeurs proches de 360 ou 0
   """

   return(math.degrees(math.asin(math.sin(math.radians(Angle))))-math.degrees(math.asin(math.sin(math.radians(AngleRef)))))

#------------------------------------------------

print Fonction(360.0,350.0)
#print (math.degrees(math.asin(math.sin(math.radians(350.0)))))