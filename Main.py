#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : Main.py
# Author  : Nicolas ISAERT
# Date    : 29/02/2016
# Version : 1.0 - Created
#
#------------------------------------------------

DEBUG = True  #if DEBUG == True:print("")
SIMUL = True

from Tkinter import *
import threading
import Queue
import time
import ConfigParser
import Log
import Display
if SIMUL == False: import GPS
#import serial
import random
#import Lifo
if SIMUL == False: import HMC5883L

Largeur = 480     # Largeur de l'écran (en pixels)
Hauteur = 800    # Hauteur de l'écran (en pixels)

ClText = 'white'
ClFond = 'black'

Canvas1X_Number = 0
Canvas1X_Index = 0
Canvas2X_Number = 0
Canvas2X_Index = 0
Canvas3X_Number = 0
Canvas3X_Index = 0

#Pile_SOG = [0,0,0,0,0,0,0,0,0,0]
#Last_Val_SOG = Last_Moy_SOG = 0

Pile_COG = [0,0,0,0,0,0,0,0,0,0]

Pile_BRG = [0,0,0,0,0,0,0,0,0,0]

NomWaypoint = ""

#------------------------------------------------
def exit():
   Mafenetre.destroy()

#------------------------------------------------
def onCanvas1XClick(event):
    global Canvas1X_Index

    Canvas1X_Index += 1
    if Canvas1X_Index == Canvas1X_Number: Canvas1X_Index = 0
    #print 'Got canvas click', event.x, event.y, event.widget

#------------------------------------------------
def onCanvas2XClick(event):
    global Canvas2X_Index

    Canvas2X_Index += 1
    if Canvas2X_Index == Canvas2X_Number: Canvas2X_Index = 0
    #print 'Got canvas click', event.x, event.y, event.widget
    #exit()

#------------------------------------------------
def onCanvas3XClick(event):
    global Canvas3X_Index

    Canvas3X_Index += 1
    if Canvas3X_Index == Canvas3X_Number: Canvas3X_Index = 0
    #print 'Got canvas click', event.x, event.y, event.widget

#------------------------------------------------
class GuiPart:
   def __init__(self, master, queue, endCommand):
      # Initialisation de la queue
      self.queue = queue

      # Initialisation des variables de navigation dans les canevas
      global Canvas1X_Number,Canvas2X_Number,Canvas3X_Number

      # Initialisation des valeurs affichées
      self.VAL_TMR=""
      self.VAL_TTL=""
      self.VAL_BSP=""
      self.VAL_SOG=""
      self.VAL_TTG=""
      self.VAL_BRG=""
      self.VAL_HDM=""
      self.VAL_COG=""
      self.VAL_VMC=""
      self.VAL_BGA=""
      self.VAL_PRS=""
      self.VAL_LAT=""
      self.VAL_LON=""
      # Initialisation des tableaux de valeurs
      self.SOG_Data = [0] * 120   # 1 valeur toutes les 500ms soit 1min d'enregistrement
      self.COG_Data = [0] * 4     # 1 valeur toutes les 500ms
      self.PRS_Data = [0] * 76#152

      # Création de la fenêtre principale (main window)

      # Création des frames
#       self.Frame1 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="red")
#       self.Frame1.grid(row = 0, columnspan = 1, sticky = W+E+N+S)
#       self.Frame2 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="green")
#       self.Frame2.grid(row = 1, columnspan = 1, sticky = W+E+N+S)
#       self.Frame3 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="blue")
#       self.Frame3.grid(row = 2, columnspan = 1, sticky = W+E+N+S)

      # Construction du Canvas 10
      self.Ecran10 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,0,ClFond,Trend=True)
      self.Ecran10.Canvas.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas1X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 11
      self.Ecran11 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,0,ClFond,Trend=False)
      self.Ecran11.Canvas.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas1X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 12
      self.Ecran12 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,0,ClFond,Trend=False)
      self.Ecran12.Canvas.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas1X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      
      # Construction du Canvas 20
      self.Ecran20 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,int(Hauteur/3),ClFond,Trend=False)
      self.Ecran20.Canvas.bind('<Double-1>',onCanvas2XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas2X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 21
      self.Ecran21 = Display.Ecran(Mafenetre,Largeur,int(Hauteur*2/3),0,int(Hauteur/3),ClFond,Trend=False,Compass=True)
      self.Ecran21.Canvas.bind('<Double-1>',onCanvas2XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas2X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      
      # Construction du Canvas 30
      self.Ecran30 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,int(Hauteur*2/3),ClFond,Trend=False)
      self.Ecran30.Canvas.bind('<Double-1>',onCanvas3XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas3X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 31
      self.Ecran31 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,int(Hauteur*2/3),ClFond,Trend=False)
      self.Ecran31.Canvas.bind('<Double-1>',onCanvas3XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas3X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 32
      self.Ecran32 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,int(Hauteur*2/3),ClFond,Trend=False)
      self.Ecran32.Canvas.bind('<Double-1>',onCanvas3XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas3X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      # Construction du Canvas 33
      self.Ecran33 = Display.Ecran(Mafenetre,Largeur,int(Hauteur/3),0,int(Hauteur*2/3),ClFond,Trend=False)
      self.Ecran33.Canvas.bind('<Double-1>',onCanvas3XClick)   # Gestion de l'événement "Double clic" sur le canvas
      Canvas3X_Number += 1 # On incrémente le nombre d'écran pour la navigation
      ButtonWaypoint = Button(self.Ecran33.Canvas, text=' Waypoint ', command=Mafenetre.destroy)
      ButtonWaypoint.pack(padx=400,pady=230)
      ChampWaypoint = Entry(self.Ecran33.Canvas, textvariable = NomWaypoint, width=30, bg="white")
      self.Ecran33.Canvas.create_window(200,233,window=ChampWaypoint,anchor=NW)
      #ChampWaypoint.pack(padx=200,pady=230)
      # ButtonQuit = Button(Canvas10, text='Quit', command=Mafenetre.destroy)
      # ButtonQuit.pack()

#------------------------------------------------
   def processIncoming(self):

      #VAL_SGG=VAL_SAG=0
      global Canvas1X_Index,Canvas2X_Index,Canvas3X_Index
      #global Canvas10_BAR1_pos, Canvas10_BAR1_neg, Canvas10_ARROW1_pos, Canvas10_ARROW1_neg
      #global Canvas10_BAR2_pos, Canvas10_BAR2_neg, Canvas10_ARROW2_pos, Canvas10_ARROW2_neg

      print("Queue size: " + str(self.queue.qsize()))

      # Si la queue est vide, on ne rafraîchit pas les écrans, on sort pour laisser du temps du cycle au programme
      if self.queue.qsize() == 0:
         return
      # Tant que la queue n'est pas vide, on traite les messages
      while self.queue.qsize():
         try:
            msg = self.queue.get(0)
            self.queue.task_done()
            print msg
            # Rafraichit les variables d'affichage
            if   msg[:3] == "SOG":
               self.VAL_SOG = msg.split(';')[1]    # Speed Over Ground
               self.SOG_Data.pop(0)
               self.SOG_Data.append(float(self.VAL_SOG))

            elif msg[:3] == "COG":
               self.VAL_COG = msg.split(';')[1]    # Course Over Ground
               self.COG_Data.pop(0)
               self.COG_Data.append(float(self.VAL_COG))

            elif msg[:3] == "CGA": self.VAL_CGA = msg.split(';')[1]

            elif msg[:3] == "BRG": self.VAL_BRG = msg.split(';')[1]
            elif msg[:3] == "BGA": self.VAL_BGA = msg.split(';')[1]

            elif msg[:3] == "VMC": self.VAL_TMR = msg.split(';')[1]
            elif msg[:3] == "TMR": self.VAL_TMR = msg.split(';')[1]
            elif msg[:3] == "TTL": self.VAL_TTL = msg.split(';')[1]
            elif msg[:3] == "BSP": self.VAL_BSP = msg.split(';')[1]
            elif msg[:3] == "TTG": self.VAL_TTG = msg.split(';')[1]
            elif msg[:3] == "HDM": self.VAL_HDM = msg.split(';')[1]
            elif msg[:3] == "PRS":
               self.VAL_PRS = msg.split(';')[1]
               self.PRS_Data.pop(0)
               self.PRS_Data.append(float(self.VAL_PRS))
            elif msg[:3] == "LAT": self.VAL_LAT = msg.split(';')[1]
            elif msg[:3] == "LON": self.VAL_LON = msg.split(';')[1]
         except Queue.Empty:
            pass

      # Rafraîchit les libellés
      if Canvas1X_Index == 0:
         self.Ecran10.Canvas.itemconfigure(self.Ecran10.LIB1,text="SOG")
         self.Ecran10.Canvas.itemconfigure(self.Ecran10.VAL1,text=self.VAL_SOG)
         self.Ecran10.Canvas.itemconfigure(self.Ecran10.LIB2,text="SOG Average (1min)")
         self.Ecran10.Canvas.itemconfigure(self.Ecran10.VAL2,text=str(round(sum(list(self.SOG_Data))/len(self.SOG_Data),2)))   # Moyenne sur 1min

         # On efface le bargraph
#          Ecran10.Canvas.delete(Ecran10.BAR1_pos)
#          Ecran10.Canvas.delete(Ecran10.BAR1_neg)
#          Ecran10.Canvas.delete(Ecran10.ARROW1_pos)
#          Ecran10.Canvas.delete(Ecran10.ARROW1_neg)
#          Ecran10.Canvas.delete(Ecran10.BAR2_pos)
#          Ecran10.Canvas.delete(Ecran10.BAR2_neg)
#          Ecran10.Canvas.delete(Ecran10.ARROW2_pos)
#          Ecran10.Canvas.delete(Ecran10.ARROW2_neg)

#          VAL_SGG = int(VAL_SGG)
#          if VAL_SGG > 0 :
#             Ecran10.BAR1_pos = Ecran10.Canvas.create_rectangle(Largeur-30,65,Largeur-9,65-VAL_SGG/2,fill='#0f0',outline='#0f0',width=0)
#             pts = [(Largeur-30,(65-VAL_SGG/2)-2),(Largeur-20,(65-VAL_SGG/2)-2-10),(Largeur-10,(65-VAL_SGG/2)-2)]
#             Ecran10.ARROW1_pos = Ecran10.Canvas.create_polygon(pts, fill='#0f0', outline='#0f0', width=0)
#          if VAL_SGG < 0 :
#             Ecran10.BAR1_neg = Ecran10.Canvas.create_rectangle(Largeur-30,65,Largeur-9,65-VAL_SGG/2,fill='red',outline='red',width=0)
#             pts = [(Largeur-30,(65-VAL_SGG/2)+2),(Largeur-20,(65-VAL_SGG/2)+2+10),(Largeur-10,(65-VAL_SGG/2)+2)]
#             Ecran10.ARROW1_neg = Ecran10.Canvas.create_polygon(pts, fill='red', outline='red', width=0)
# 
#          VAL_SAG = int(VAL_SAG)
#          if VAL_SAG > 0 :
#             Ecran10.BAR2_pos = Ecran10.Canvas.create_rectangle(Largeur-30,198,Largeur-9,198-VAL_SAG/2,fill='#0f0',outline='#0f0',width=0)
#             pts = [(Largeur-30,(198-VAL_SAG/2)-2),(Largeur-20,(198-VAL_SAG/2)-2-10),(Largeur-10,(198-VAL_SAG/2)-2)]
#             Ecran10.ARROW2_pos = Ecran10.Canvas.create_polygon(pts, fill='#0f0', outline='#0f0', width=0)
#          if VAL_SAG < 0 :
#             Ecran10.BAR2_neg = Ecran10.Canvas.create_rectangle(Largeur-30,198,Largeur-9,198-VAL_SAG/2,fill='red',outline='red',width=0)
#             pts = [(Largeur-30,(198-VAL_SAG/2)+2),(Largeur-20,(198-VAL_SAG/2)+2+10),(Largeur-10,(198-VAL_SAG/2)+2)]
#             Ecran10.ARROW2_neg = Ecran10.Canvas.create_polygon(pts, fill='red', outline='red', width=0)

         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran10.place(x=0*Largeur,y=0)
         self.Ecran11.place(x=1*Largeur,y=0)
         self.Ecran12.place(x=2*Largeur,y=0)

      elif Canvas1X_Index == 1:
         self.Ecran11.Canvas.itemconfigure(self.Ecran11.LIB1,text="BSP")
         self.Ecran11.Canvas.itemconfigure(self.Ecran11.VAL1,text=self.VAL_BSP)
         self.Ecran11.Canvas.itemconfigure(self.Ecran11.LIB2,text="SOG")
         self.Ecran11.Canvas.itemconfigure(self.Ecran11.VAL2,text=self.VAL_SOG)

         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran10.place(x=1*Largeur,y=0)
         self.Ecran11.place(x=0*Largeur,y=0)
         self.Ecran12.place(x=2*Largeur,y=0)

      elif Canvas1X_Index == 2:
         #Ecran12.Canvas.itemconfigure(Ecran12.LIB1,text="SPEED ON GROUND")
         #Largeur = 480     # Largeur de l'écran (en pixels)
         #Hauteur = 800    # Hauteur de l'écran (en pixels)
         Display.GraphVitesse(self.Ecran12.Canvas,30,30,Largeur,int(Hauteur/3),10,self.SOG_Data)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran10.place(x=1*Largeur,y=0)
         self.Ecran11.place(x=2*Largeur,y=0)
         self.Ecran12.place(x=0*Largeur,y=0)

      if Canvas2X_Index == 0:
         self.Ecran20.Canvas.itemconfigure(self.Ecran20.LIB1,text="COG")
         self.Ecran20.Canvas.itemconfigure(self.Ecran20.VAL1,text=str(int(float(self.VAL_COG))) + "°".decode('cp1252'))
         self.Ecran20.Canvas.itemconfigure(self.Ecran20.LIB2,text="COG Average (2sec)")
         self.Ecran20.Canvas.itemconfigure(self.Ecran20.VAL2,text=str(Display.MoyenneCap(self.COG_Data)) + "°".decode('cp1252'))
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran20.place(x=0*Largeur,y=0)
         self.Ecran21.place(x=1*Largeur,y=0)

      elif Canvas2X_Index == 1:
         self.Ecran30.place(x=1*Largeur,y=0)
         self.Ecran31.place(x=2*Largeur,y=0)
         self.Ecran32.place(x=3*Largeur,y=0)
         self.Ecran33.place(x=4*Largeur,y=0)

         #Frame2.itemconfigure(height = int(Hauteur*2/3), bg="blue")
#          Frame2 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="blue")
#          Frame2.grid(row = 1, columnspan = 1, sticky = W+E+N+S)
#          Frame3 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="green")
#          Frame3.grid(row = 2, columnspan = 1, sticky = W+E+N+S)

         #self.Frame2.destroy
         #self.Frame3.destroy
         #Frame2 = Frame(Mafenetre, width = Largeur, height = int(Hauteur*2/3), bg="green")
         #self.Frame2.grid(row = 1, columnspan = 2, sticky = W+E+N+S)
#          Frame3 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="green")
#          Frame3.grid(row = 2, columnspan = 1, sticky = W+E+N+S)

         #self.Frame2.destroy
         #self.Frame2 = Frame(Mafenetre, width = Largeur, height = int(Hauteur*2/3), bg="blue")
         #self.Frame3.destroy
         #self.Frame2.grid(row = 1, rowspan = 2, columnspan = 1, sticky = W+E+N+S)
         self.Ecran21.Canvas.itemconfigure(self.Ecran21,height = int(Hauteur*2/3))
         #self.Frame3.forget
         self.Ecran21.Canvas.itemconfigure(self.Ecran21.LIB1,text="COMPASS")
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran20.place(x=1*Largeur,y=0)
         self.Ecran21.place(x=0*Largeur,y=0)

      if Canvas3X_Index == 0 and Canvas2X_Index <> 1:
         self.Ecran30.Canvas.itemconfigure(self.Ecran30.LIB1,text="BRG")
         self.Ecran30.Canvas.itemconfigure(self.Ecran30.VAL1,text=self.VAL_BRG)
         self.Ecran30.Canvas.itemconfigure(self.Ecran30.LIB2,text="BGA")
         self.Ecran30.Canvas.itemconfigure(self.Ecran30.VAL2,text=self.VAL_BGA)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran30.place(x=0*Largeur,y=0)
         self.Ecran31.place(x=1*Largeur,y=0)
         self.Ecran32.place(x=2*Largeur,y=0)
         self.Ecran33.place(x=3*Largeur,y=0)

      elif Canvas3X_Index == 1 and Canvas2X_Index <> 1:
         self.Ecran31.Canvas.itemconfigure(self.Ecran31.LIB1,text="PRESSION")
         Display.GraphPression(self.Ecran31.Canvas,10,30,Largeur,int(Hauteur/3),10,self.PRS_Data)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran30.place(x=1*Largeur,y=0)
         self.Ecran31.place(x=0*Largeur,y=0)
         self.Ecran32.place(x=2*Largeur,y=0)
         self.Ecran33.place(x=3*Largeur,y=0)

      elif Canvas3X_Index == 2 and Canvas2X_Index <> 1:
         self.Ecran32.Canvas.itemconfigure(self.Ecran32.LIB1,text="TEMPERATURE")
         Display.GraphPression(self.Ecran32.Canvas,10,30,Largeur,int(Hauteur/3),10,self.PRS_Data)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran30.place(x=1*Largeur,y=0)
         self.Ecran31.place(x=2*Largeur,y=0)
         self.Ecran32.place(x=0*Largeur,y=0)
         self.Ecran33.place(x=3*Largeur,y=0)

      elif Canvas3X_Index == 3 and Canvas2X_Index <> 1:
         self.Ecran33.Canvas.itemconfigure(self.Ecran33.LIB1,text="LATITUDE")
         self.Ecran33.Canvas.itemconfigure(self.Ecran33.VAL1,text=self.VAL_LAT,font=('Calibri', 60, 'bold'))
         self.Ecran33.Canvas.coords(self.Ecran33.VAL1,240,10)
         self.Ecran33.Canvas.itemconfigure(self.Ecran33.LIB2,text="LONGITUDE")
         self.Ecran33.Canvas.coords(self.Ecran33.LIB2,15,115)
         self.Ecran33.Canvas.itemconfigure(self.Ecran33.VAL2,text=self.VAL_LON,font=('Calibri', 60, 'bold'))
         self.Ecran33.Canvas.coords(self.Ecran33.VAL2,240,123)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         self.Ecran30.place(x=1*Largeur,y=0)
         self.Ecran31.place(x=2*Largeur,y=0)
         self.Ecran32.place(x=3*Largeur,y=0)
         self.Ecran33.place(x=0*Largeur,y=0)

         # Effacement du canvas
         #Canvas2.delete(ALL)

      # Rafraîchit la fenêtre
      Mafenetre.update()

#------------------------------------------------
class ThreadedClient:
   """
   Launch the main part of the GUI and the worker thread. periodicCall and
   endApplication could reside in the GUI part, but putting them here
   means that you have all the thread controls in a single place.
   """
   def __init__(self, master):
      """
      Start the GUI and the asynchronous threads. We are in the main
      (original) thread of the application, which will later be used by
      the GUI. We spawn a new thread for the worker.
      """

      ini = ConfigParser.ConfigParser()
      # Décommenter ce code pour créer le fichier ini
      """
      ini.add_section('GPS')
      ini.set('GPS', 'port', '/dev/ttyUSB0')
      ini.set('GPS', 'baudrate', 4800)
      ini.set('GPS', 'parity', serial.PARITY_NONE)
      ini.set('GPS', 'stopbits', serial.STOPBITS_ONE)
      ini.set('GPS', 'bytesize', serial.EIGHTBITS)
      ini.set('GPS', 'timeout', 1)
      ini.write(open('/home/pi/MySkipper/config.ini','w'))
      """

      # Initialisation des variables
      """
      ini.read('/home/pi/MySkipper/config.ini')
      GPS.port = ini.get('GPS', 'port')
      GPS.baudrate = ini.getint('GPS', 'baudrate')
      GPS.parity = ini.get('GPS', 'parity')
      GPS.stopbits = ini.getint('GPS', 'stopbits')
      GPS.bytesize = ini.getint('GPS', 'bytesize')
      GPS.timeout = ini.getint('GPS', 'timeout')
      """

      # Initialisation du fichier de LOG
      Log.Init()

      self.master = master

      # Create the queue
      self.queue = Queue.Queue()
      
      # Set up the GUI part
      self.gui = GuiPart(master, self.queue, self.endApplication)

      # Set up the thread to do GPS Communication
      self.running = 1
      self.thread1 = threading.Thread(target=self.GPSThread)
      self.thread1.start()

#       # Set up the thread to do Compass Communication
#       self.running = 1
#       self.thread2 = threading.Thread(target=self.CompassThread)
#       self.thread2.start()

      # Set up the thread to do asynchronous I/O
      self.running = 1
      self.thread2 = threading.Thread(target=self.MainThread)
      self.thread2.start()

      # Start the periodic call in the GUI to check if the queue contains anything
      self.periodicCall()

#------------------------------------------------
   def periodicCall(self):
      """
      Check every 250 ms if there is something new in the queue to refresh display.
      """
      self.gui.processIncoming()
      if not self.running:
         # This is the brutal stop of the system. You may want to do some cleanup before actually shutting it down.
         import sys
         # self.thread1.stop() # A tester
         # self.thread2.stop() # A tester
         sys.exit(1)
      self.master.after(400, self.periodicCall)

#------------------------------------------------
   def GPSThread(self):
      self.Last_Val_SOG = 0

      """
      This is where we handle the GPS Communication.
      """
      Log.WriteLine("Première exécution du thread GPS Communication")

      # Initialisation du GPS
      if SIMUL == False : MyGPS = GPS.GPS()

      while self.running:
         # Acquisitiion des données GPS
         if SIMUL == False :
            MyGPS.Communicate()
            Val_SOG = float(MyGPS.GPRMC['SOG'])
            Val_COG = float(MyGPS.GPRMC['COG'])
         else:
            Val_SOG = round(rand.random()*16,2)-1     # Valeur de -01.00 à 14.99
            Val_COG = round(rand.random()*360,2)      # Valeur de 0.00 à 360.00
            Val_PRS = round(rand.random()*80,1)+973   # Valeur de 973.0 à 1052.9
            Val_LAT = "51" + "°".decode('cp1252') + "01'03.7''N"
            Val_LON = "02" + "°".decode('cp1252') + "05'22.4''E"

         # Moyenne du SOG
#          Pile_SOG.pop(0)
#          Pile_SOG.append(Val_SOG)
#          Somme = 0
#          for i in range(len(Pile_SOG)):
#             Somme = Somme + Pile_SOG[i]
#          Val_SGA = Somme/len(Pile_SOG)

         # Tendance du SOG
#          Val_SGG = int((Val_SOG - self.Last_Val_SOG)*100/1)
#          if Val_SGG > 100: Val_SGG = 100
#          if Val_SGG < -100: Val_SGG = -100
#          self.Last_Val_SOG = Val_SGG

         # Tendance de la moyenne du SOG
#          Val_SAG = int((Val_SOG - Val_SGA)*100/1)
#          if Val_SAG > 100: Val_SAG = 100
#          if Val_SAG < -100: Val_SAG = -100

         # Moyenne du COG
#          Pile_COG.pop(0)
#          Pile_COG.append(Val_COG)
#          Somme = 0
#          for i in range(len(Pile_COG)):
#             Somme = Somme + Pile_COG[i]
#          Val_CGA = Somme/len(Pile_COG)

         if SIMUL == False :
            compass = HMC5883L.hmc5883l(gauss = 4.7, declination = (0,12))
            Val_BRG = compass.degrees(compass.heading())
         else:
            Val_BRG = int(rand.random()*360) # Valeur de 0 à 360

         Pile_BRG.pop(0)
         Pile_BRG.append(Val_BRG)
         Somme = 0
         for i in range(len(Pile_BRG)):
            Somme = Somme + Pile_BRG[i]
         Val_BGA = Somme/len(Pile_BRG)

         # Ressources envoyées au thread GUI
         self.queue.put("SOG" + ";" + str(round(Val_SOG,2)))          # Speed Over Ground
         self.queue.put("COG" + ";" + str(round(Val_COG,2)))          # Course Over Ground

         self.queue.put("BRG" + ";" + str(Val_BRG) + "°".decode('cp1252'))    # Bearing, Cap compas HMC5883L
         self.queue.put("BGA" + ";" + str(Val_BGA) + "°".decode('cp1252'))    # Bearing Average
         self.queue.put("PRS" + ";" + str(round(Val_PRS,1)))         # Pressure
         self.queue.put("LAT" + ";" + Val_LAT)                       # Latitude
         self.queue.put("LON" + ";" + Val_LON)                       # Longitude

         #self.queue.put("TMR" + ";" + time.strftime("%H:%M",time.localtime()))
         #self.queue.put("TTL" + ";" + "12:34")
         #self.queue.put("BSP" + ";" + str(round(rand.random(),2)))
         #self.queue.put("VMC" + ";" + str(round(rand.random(),2)))

         #self.queue.put("TTG" + ";" + "11:11")

         # On laisse du temps pour l'exécution des autres threads
         time.sleep(0.500)

#------------------------------------------------
   def MainThread(self):

      """
      This is where we handle the asynchronous I/O. For example, it may be a 'select()'.
      One important thing to remember is that the thread has to yield control.
      """

      Log.WriteLine("Première exécution du thread principal")
      while self.running: # Asynchronous I/O

         # Ressources envoyées au thread GUI
         self.queue.put("TTL" + ";" + "12:34")

         # On laisse du temps pour l'exécution des autres threads
         time.sleep(0.500)
   
#------------------------------------------------
   def endApplication(self):
      self.running = 0

#------------------------------------------------
"""
Programme Principal
"""
rand = random.Random()

Mafenetre = Tk()
Mafenetre.title('')                 # Titre de la fenêtre
Mafenetre.overrideredirect(1)       # Supprime les bordures de la fenêtre principale
Mafenetre.geometry('480x800+0+0')   # Taille et position
Mafenetre['bg']='black'             # Couleur de fond

client = ThreadedClient(Mafenetre)
Mafenetre.mainloop()