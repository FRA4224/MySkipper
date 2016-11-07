#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : Soleil.py
# Author  : Nicolas ISAERT
# Date    : 18/10/2016
# Version : 1.0 - Created
#
#------------------------------------------------

import math

DEBUG = True  #if DEBUG == True:print("")

#------------------------------------------------
def HeuresLCSoleil(Latitude,Longitude):
   # Le code est presque fonctionnel, vérifier par rapport à Google
   # Gravelines 50.987490, 2.124284
   Latitude = 50.9865100
   Longitude = 2.1280700

   D = 18
   M = 10
   A = 2016
   N1 = int((M*275)/9)
   #print("N1:"+str(N1))
   N2 = int((M+9)/12)
   #print("N2:"+str(N2))
   K = 1 + int ( ( A - 4 * int (A / 4) + 2 ) / 3 )
   #print("K:"+str(K))
   N = N1 - N2*K + D -30   #N représente le rang du jour dans l'année (1er janvier = 1)
   if DEBUG == True:print("N:"+str(N))
   #M = 356.8 + 0.9856 * (N - 1)    #M est l'anomalie moyenne en degrés
   M = 357.5291 + 0.98560028 * (N - 1)    #M est l'anomalie moyenne en degrés
   #M = math.degrees(M)
   #C = 1.91378 * math.sin(math.radians(M)) + 0.02 * math.sin(math.radians(2*M))    #C est l'équation du centre (influence de l'ellipticité de l'orbite terrestre) en degrés
   e=0.01671   #excentricité de l'ellipse
   C = (2*e-(math.pow(e,3))/4) * math.sin(math.radians(M)) + 1.25*(math.pow(e,2)) * math.sin(math.radians(2*M))    #C est l'équation du centre (influence de l'ellipticité de l'orbite terrestre) en degrés
   #C = math.degrees(C)
   #L = 280 + C + 0.9856 * N    #L est la longitude vraie du Soleil en degrés
   L = 280.4665 + C + 0.98564736 * N    #L est la longitude vraie du Soleil en degrés
   #L = math.degrees(L)
   #R = -2.46522 * math.sin(math.radians(2*L)) + 0.05303 * math.sin(math.radians(4*L))  #R est la réduction à l'équateur (influence de l'inclinaison de l'axe terrestre) en degrés
   R = -2.4657 * math.sin(math.radians(2*L)) + 0.053 * math.sin(math.radians(4*L))  #R est la réduction à l'équateur (influence de l'inclinaison de l'axe terrestre) en degrés
   #R = math.degrees(R)
   ET = (C+R) * 4
   if DEBUG == True:print("ET(minutes):"+str(int(ET))+"'"+str(int((ET-int(ET))*6/10*100))+"''")
   dec = math.asin(0.39774 * math.sin(math.radians(L)))  #déclinaison du Soleil
   if DEBUG == True:print("Déclinaison("+chr(223)+"):"+str(math.degrees(dec)))

   #Ho = math.acos((-0.01454 - math.sin(dec)*math.sin(math.radians(Latitude)))/(math.cos(dec)*math.cos(math.radians(Latitude))))    #L'angle horaire Ho du Soleil, en degrés, au moment où son bord supérieur est sur l'horizon
   Ho = math.acos((-0.01065 - math.sin(dec)*math.sin(math.radians(Latitude)))/(math.cos(dec)*math.cos(math.radians(Latitude))))    #L'angle horaire Ho du Soleil, en degrés, au moment où son bord supérieur est sur l'horizon
   Ho = math.degrees(Ho)
   if DEBUG == True:print("Ho("+chr(223)+"):"+str(Ho))
   #Ho = math.degrees(Ho)
   Ho = Ho * 4 / 60
   Longitude = Longitude * 4 / 60
   if DEBUG == True:print("Ho(min):"+str(Ho))
   ET = ET / 60
   TL = 12 - Ho + ET + Longitude #Heure UTC du lever du soleil
   if DEBUG == True:print("Heure UTC du lever du soleil:"+str(TL))
   HL = 12 - Ho + ET + Longitude + 1 #Heure légale du lever du soleil
   if DEBUG == True:print("Heure légale du lever du soleil:"+str(HL))
   TC = 12 + Ho + ET + Longitude #Heure UTC du coucher du soleil
   if DEBUG == True:print("Heure UTC du coucher du soleil:"+str(TC))
   HC = 12 + Ho + ET + Longitude + 1 #Heure légale du coucher du soleil
   if DEBUG == True:print("Heure légale du coucher du soleil:"+str(HC))

   return(str(TL),str(HL),str(TC),str(HC))
#------------------------------------------------

HeuresLCSoleil(0,0)