#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : Display.py
# Author  : Nicolas ISAERT
# Date    : 04/11/2016
# Version : 1.0 - Created
#
#------------------------------------------------

from Tkinter import *
import math

#------------------------------------------------
def MoindresCarres(Data):

   Somme_X = Somme_Y = 0
   for X, Y in enumerate(Data):
      Somme_X += X
      Somme_Y += Y

   Moyenne_X = Somme_X/len(Data)
   Moyenne_Y = Somme_Y/len(Data)

   Somme_XiYi = 0    # Somme du produit des écarts en X et Y
   Somme_Xi2 = 0     # Somme des Ecarts au carré
   for X, Y in enumerate(Data):
      Somme_XiYi = Somme_XiYi + (X-Moyenne_X)*(Y-Moyenne_Y)
      Somme_Xi2 = Somme_Xi2 + (X-Moyenne_X)*(X-Moyenne_X)

   # Calcul des coefficients de la droite y=ax+b
   a = Somme_XiYi / Somme_Xi2
   b = Moyenne_Y - a*Moyenne_X
   if a > 0:
      return True
   else:
      return False

#------------------------------------------------
def MoyenneCap(Data):

   # Data = [355,350,5,10]
   #print (Data)
   
   if max(Data)-min(Data) < 180:
      return int(sum(list(Data))/len(Data))
   else:
      Somme = 0
      for Indice, Valeur in enumerate(Data):
         if Valeur < 180:
            Somme += (Valeur+360)
         else:
            Somme += Valeur

      Moyenne = Somme/len(Data)
      if Moyenne >= 360:
         return int(Moyenne-360)
      else:
         return int(Moyenne)

#------------------------------------------------
def GraphVitesse(Canvas,X_Pos,Y_Pos,C_width,C_height,Gap,Data):

   # The variables below size the bar graph
   # C_width      Canvas Width
   # C_height     Canvas Height
   X_gap = Gap       # Gap between left canvas edge and y axis
   Y_gap = Gap       # Gap between lower canvas edge and x axis
   Y_stretch = (C_height-Y_Pos-Y_gap)/16.0 # -1 à 15 noeuds
   X_width = (C_width-X_Pos-X_gap)/float((len(Data)))

   # Chaque barre du bargraph doit être supprimée
   Canvas.delete(ALL)
   # On crée à nouveau la bordure arrondie
   Bordure = 2
   Rayon = 15
   Couleur = 'blue'
   Largeur = 480
   Hauteur = int(800/3)
   Canvas.create_line(Bordure+Rayon,Bordure,Largeur-(Bordure+Rayon),Bordure,fill=Couleur,width=3)
   Canvas.create_line(Bordure,Bordure+Rayon,Bordure,Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
   Canvas.create_line(Largeur-Bordure,Bordure+Rayon,Largeur-Bordure,Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
   Canvas.create_line(Bordure+Rayon,Hauteur-Bordure,Largeur-(Bordure+Rayon),Hauteur-Bordure,fill=Couleur,width=3)
   Canvas.create_arc(Bordure,Bordure,Bordure+2*Rayon,Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=90,extent=90,style='arc')
   Canvas.create_arc(Largeur-Bordure,Bordure,Largeur-(Bordure+2*Rayon),Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=0,extent=90,style='arc')
   Canvas.create_arc(Bordure,Hauteur-Bordure,Bordure+2*Rayon,Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=180,extent=90,style='arc')
   Canvas.create_arc(Largeur-Bordure,Hauteur-Bordure,Largeur-(Bordure+2*Rayon),Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=270,extent=90,style='arc')

   Canvas.LIB1 = Canvas.create_text(15,2,text="SPEED ON GROUND (1min)",anchor=NW,font=('Calibri', 14, 'bold'),fill="white",justify=LEFT)

   for X, Y in enumerate(Data):
      # calculate rectangle coordinates (integers) for each bar
      X0 = X_Pos + X * X_width
      Y0 = C_height - Y_gap - ((Y+1) * Y_stretch)  # +1 car les vitesses jusqu'à -1 sont affichées
      X1 = X0 + X_width-1
      #X1 = X + X * X_width + X_width + X_gap - 1
      Y1 = C_height - Y_gap
      # draw the bar
      Canvas.create_rectangle(X0, Y0, X1, Y1, fill='#FFC800', outline='#FFC800')

   # Affichage des axes principaux
   Canvas.create_line(X_Pos,C_height-Y_gap-((0+1)*Y_stretch),C_width-X_gap,C_height-Y_gap-((0+1)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((0+1)*Y_stretch),text="0",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)
   Canvas.create_line(X_Pos,C_height-Y_gap-((5+1)*Y_stretch),C_width-X_gap,C_height-Y_gap-((5+1)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((5+1)*Y_stretch),text="5",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)
   Canvas.create_line(X_Pos,C_height-Y_gap-((10+1)*Y_stretch),C_width-X_gap,C_height-Y_gap-((10+1)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((10+1)*Y_stretch),text="10",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)

   # Affichage de la tendance par les méthodes des moindres carrés
   if MoindresCarres(Data) == True:
      pts = [(C_width-Gap-70,Y_Pos+30),(C_width-Gap-40,Y_Pos+0),(C_width-Gap-10,Y_Pos+30)]
      Canvas.create_polygon(pts, fill='#0f0', outline='black', width=0)
   else:
      pts = [(C_width-Gap-70,Y_Pos+0),(C_width-Gap-40,Y_Pos+30),(C_width-Gap-10,Y_Pos+0)]
      Canvas.create_polygon(pts, fill='red', outline='black', width=0)

#------------------------------------------------
def GraphPression(Canvas,X_Pos,Y_Pos,C_width,C_height,Gap,Data):

   # The variables below size the bar graph
   # C_width      Canvas Width
   # C_height     Canvas Height
   X_gap = Gap       # Gap between left canvas edge and y axis
   Y_gap = Gap       # Gap between lower canvas edge and x axis
   Y_stretch = (C_height-Y_Pos-Y_gap)/80.0 # 80 bars, valeur moyenne 1013
   X_width = (C_width-X_Pos-X_gap)/float((len(Data)))

   # Chaque barre du bargraph doit être supprimée
   Canvas.delete(ALL)
   # On crée à nouveau la bordure arrondie
   Bordure = 2
   Rayon = 15
   Couleur = 'blue'
   Largeur = 480
   Hauteur = int(800/3)
   Canvas.create_line(Bordure+Rayon,Bordure,Largeur-(Bordure+Rayon),Bordure,fill=Couleur,width=3)
   Canvas.create_line(Bordure,Bordure+Rayon,Bordure,Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
   Canvas.create_line(Largeur-Bordure,Bordure+Rayon,Largeur-Bordure,Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
   Canvas.create_line(Bordure+Rayon,Hauteur-Bordure,Largeur-(Bordure+Rayon),Hauteur-Bordure,fill=Couleur,width=3)
   Canvas.create_arc(Bordure,Bordure,Bordure+2*Rayon,Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=90,extent=90,style='arc')
   Canvas.create_arc(Largeur-Bordure,Bordure,Largeur-(Bordure+2*Rayon),Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=0,extent=90,style='arc')
   Canvas.create_arc(Bordure,Hauteur-Bordure,Bordure+2*Rayon,Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=180,extent=90,style='arc')
   Canvas.create_arc(Largeur-Bordure,Hauteur-Bordure,Largeur-(Bordure+2*Rayon),Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=270,extent=90,style='arc')

   Canvas.LIB1 = Canvas.create_text(15,2,text="PRESSION (1 jour)",anchor=NW,font=('Calibri', 14, 'bold'),fill="white",justify=LEFT)

   for X, Y in enumerate(Data):
      # calculate rectangle coordinates (integers) for each bar
      X0 = X_Pos + X * X_width
      Y0 = C_height - Y_gap - ((Y-973) * Y_stretch)
      X1 = X0 + X_width-1
      #X1 = X + X * X_width + X_width + X_gap - 1
      Y1 = C_height - Y_gap
      # draw the bar
      Canvas.create_rectangle(X0, Y0, X1, Y1, fill="#FFC800", outline="#FFC800")

   # Affichage des axes principaux
   Canvas.create_line(X_Pos,C_height-Y_gap-((990-973)*Y_stretch),C_width-X_gap,C_height-Y_gap-((990-973)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((990-973)*Y_stretch),text="990",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)
   Canvas.create_line(X_Pos,C_height-Y_gap-((1013-973)*Y_stretch),C_width-X_gap,C_height-Y_gap-((1013-973)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((1013-973)*Y_stretch),text="1013",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)
   Canvas.create_line(X_Pos,C_height-Y_gap-((1030-973)*Y_stretch),C_width-X_gap,C_height-Y_gap-((1030-973)*Y_stretch),fill="red")
   Canvas.create_text(5,C_height-Y_gap-((1030-973)*Y_stretch),text="1030",anchor=W,font=('Calibri', 10, 'bold'),fill="white",justify=LEFT)

   # Affichage de la tendance par les méthodes des moindres carrés
   if MoindresCarres(Data) == True:
      pts = [(C_width-Gap-70,Y_Pos+30),(C_width-Gap-40,Y_Pos+0),(C_width-Gap-10,Y_Pos+30)]
      Canvas.create_polygon(pts, fill='#0f0', outline='black', width=0)
   else:
      pts = [(C_width-Gap-70,Y_Pos+30),(C_width-Gap-40,Y_Pos+60),(C_width-Gap-10,Y_Pos+30)]
      Canvas.create_polygon(pts, fill='red', outline='black', width=0)

#------------------------------------------------
class Ecran:
   def __init__(self,Frame,Largeur,Hauteur,X_Pos,Y_Pos,ClFond,Trend=False,Compass=False):
      self.Largeur = Largeur
      self.Hauteur = Hauteur
      self.ClFond = ClFond
      self.Pos_X = X_Pos
      self.Pos_Y = Y_Pos
      self.Canvas = Canvas(Frame, width = Largeur, height = Hauteur, bg =ClFond, highlightthickness = 0)
      self.Canvas.place(x=self.Pos_X,y=self.Pos_Y)

      ClText = 'white'

      self.create_RoundRectangle(2,15,'blue')   # Création de la bordure de canvas

      # Affichage de type "Gain"
      if Trend == True:
         self.LIB1 = self.Canvas.create_text(15,2,text="",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
         self.VAL1 = self.Canvas.create_text(260,0,text="",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
         self.LIB2 = self.Canvas.create_text(15,135,text="",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
         self.VAL2 = self.Canvas.create_text(260,133,text="",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
         # Création de l'indication de tendance pour les valeurs supérieures et inférieures
         self.BAR1_pos = self.Canvas.create_rectangle(0,0,0,0,fill='#0f0',outline='green',width=0)
         self.BAR1_neg = self.Canvas.create_rectangle(0,0,0,0,fill='red',outline='red',width=0)
         self.BAR2_pos = self.Canvas.create_rectangle(0,0,0,0,fill='#0f0',outline='green',width=0)
         self.BAR2_neg = self.Canvas.create_rectangle(0,0,0,0,fill='red',outline='red',width=0)
         pts = [(0,0),(0,0),(0,0)]
         self.ARROW1_pos = self.Canvas.create_polygon(pts, fill='#0f0', outline='black', width=0)
         self.ARROW1_neg = self.Canvas.create_polygon(pts, fill='red', outline='black', width=0)
         self.ARROW2_pos = self.Canvas.create_polygon(pts, fill='#0f0', outline='black', width=0)
         self.ARROW2_neg = self.Canvas.create_polygon(pts, fill='red', outline='black', width=0)

      # Affichage de type "Compas"
      elif Compass == True:
         self.LIB1 = self.Canvas.create_text(15,2,text="",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
         self.Canvas.create_oval(20,50,460,490,outline='red')
         self.CAP = self.Compass_Arrow(270,20,'#0f0')
      # Affichage de type "classique"
      else:
         self.LIB1 = self.Canvas.create_text(15,2,text="",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
         self.VAL1 = self.Canvas.create_text(260,0,text="",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
         self.LIB2 = self.Canvas.create_text(15,135,text="",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
         self.VAL2 = self.Canvas.create_text(260,133,text="",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)

      self.Canvas.bind('<Double-1>',self.onCanvasClick)   # Gestion de l'événement "Double clic" sur le canvas

#------------------------------------------------
   def place(self,x=0,y=0):
      self.Pos_X = x
      #self.Pos_Y = y
      self.Canvas.place(x=self.Pos_X,y=self.Pos_Y)

#------------------------------------------------
   def onCanvasClick(self,event):
      pass
#       Main.Canvas1X_Index = Main.Canvas1X_Index + 1
#       if Main.Canvas1X_Index == Main.Canvas1X_Number:
#          Main.Canvas1X_Index = 0
#
#       print 'Got canvas click', event.x, event.y, event.widget

#------------------------------------------------
   ''' Cette Fonction permet l'affichage d'une aiguille sur le compas '''
   def Compass_Arrow(self,Angle,Base,Couleur):
      Offset_X=(460-20)/2 + 20
      Offset_Y=(490-50)/2 + 50

      pts = [(Offset_X-math.cos(math.radians(Angle))*Base/2,Offset_Y-math.sin(math.radians(Angle))*Base/2), \
      (Offset_X+math.sin(math.radians(Angle))*(460-20)/2,Offset_Y-math.cos(math.radians(Angle))*(460-20)/2), \
      (Offset_X+math.cos(math.radians(Angle))*Base/2,Offset_Y+math.sin(math.radians(Angle))*Base/2)]
      self.ARROW1_pos = self.Canvas.create_polygon(pts, fill=Couleur, outline=Couleur, width=1)

#------------------------------------------------
   def create_RoundRectangle(self,Bordure,Rayon,Couleur):
      self.Canvas.create_line(Bordure+Rayon,Bordure,self.Largeur-(Bordure+Rayon),Bordure,fill=Couleur,width=3)
      self.Canvas.create_line(Bordure,Bordure+Rayon,Bordure,self.Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
      self.Canvas.create_line(self.Largeur-Bordure,Bordure+Rayon,self.Largeur-Bordure,self.Hauteur-(Bordure+Rayon),fill=Couleur,width=3)
      self.Canvas.create_line(Bordure+Rayon,self.Hauteur-Bordure,self.Largeur-(Bordure+Rayon),self.Hauteur-Bordure,fill=Couleur,width=3)
      self.Canvas.create_arc(Bordure,Bordure,Bordure+2*Rayon,Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=90,extent=90,style='arc')
      self.Canvas.create_arc(self.Largeur-Bordure,Bordure,self.Largeur-(Bordure+2*Rayon),Bordure+2*Rayon,fill=Couleur,outline=Couleur,width=3,start=0,extent=90,style='arc')
      self.Canvas.create_arc(Bordure,self.Hauteur-Bordure,Bordure+2*Rayon,self.Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=180,extent=90,style='arc')
      self.Canvas.create_arc(self.Largeur-Bordure,self.Hauteur-Bordure,self.Largeur-(Bordure+2*Rayon),self.Hauteur-(Bordure+2*Rayon),fill=Couleur,outline=Couleur,width=3,start=270,extent=90,style='arc')

#------------------------------------------------
# def CanvasBuild(CanvasX,Num,Canvas_LIB1,Canvas_VAL1,Canvas_LIB2,Canvas_VAL2):
#    #Largeur = 480     # Largeur de l'écran (en pixels)
#    #Hauteur = 800    # Hauteur de l'écran (en pixels)
# 
#    ClText = 'white'
#    ClFond = 'black'
# 
#    X_LIB1 = 15
#    Y_LIB1 = 2
#    X_LIB2 = 15
#    Y_LIB2 = 135
#    X_VAL1 = 260
#    Y_VAL1 = 0
#    X_VAL2 = 260
#    Y_VAL2 = 130
# 
#    #Canvas[Num] = Canvas(Frame, width = Largeur, height = int(Hauteur/3), bg = ClFond, highlightthickness = 0)
#    CanvasX.place(x=0,y=0)
#    Canvas_LIB1 = CanvasX.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
#    Canvas_VAL1 = CanvasX.create_text(X_VAL1,Y_VAL1,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
#    Canvas_LIB2 = CanvasX.create_text(X_LIB2,Y_LIB2,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
#    Canvas_VAL2 = CanvasX.create_text(X_VAL2,Y_VAL2,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
#    Create_RoundRectangle(CanvasX,2,15,'blue')   # Création de la bordure de canvas
#    CanvasX.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas

#------------------------------------------------
