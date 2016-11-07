#!/usr/bin/python
#-*- coding: utf-8 -*

#------------------------------------------------
# File    : Main.py
# Author  : Nicolas ISAERT
# Date    : 29/02/2016
# Version : 1.0 - Created
#
#------------------------------------------------

from Tkinter import *
import threading
import Queue
import time
import ConfigParser
import Log
import GPS
#import serial
import random
#import Lifo
import HMC5883L

DEBUG = True  #if DEBUG == True:print("")
SIMUL = True

Largeur = 480     # Largeur de l'écran (en pixels)
Hauteur = 800    # Hauteur de l'écran (en pixels)

ClText = 'white'
ClFond = 'black'

Canvas1X_Number = 3
Canvas1X_Index = 0
Canvas2X_Number = 2
Canvas2X_Index = 0
Canvas3X_Number = 2
Canvas3X_Index = 0

Pile_SOG = [0,0,0,0,0,0,0,0,0,0]
Last_Val_SOG = Last_Moy_SOG = 0

Pile_COG = [0,0,0,0,0,0,0,0,0,0]

Pile_BRG = [0,0,0,0,0,0,0,0,0,0]

#------------------------------------------------
def Create_RoundRectangle(Cv,pos,rayon,couleur):
    Cv.create_line(pos+rayon,pos,Largeur-(pos+rayon),pos,fill=couleur,width=3)
    Cv.create_line(pos,pos+rayon,pos,int(Hauteur/3)-(pos+rayon),fill=couleur,width=3)
    Cv.create_line(Largeur-pos,pos+rayon,Largeur-pos,int(Hauteur/3)-(pos+rayon),fill=couleur,width=3)
    Cv.create_line(pos+rayon,int(Hauteur/3)-pos,Largeur-(pos+rayon),int(Hauteur/3)-pos,fill=couleur,width=3)
    Cv.create_arc(pos,pos,pos+2*rayon,pos+2*rayon,fill=couleur,outline=couleur,width=3,start=90,extent=90,style='arc')
    Cv.create_arc(Largeur-pos,pos,Largeur-(pos+2*rayon),pos+2*rayon,fill=couleur,outline=couleur,width=3,start=0,extent=90,style='arc')
    Cv.create_arc(pos,int(Hauteur/3)-pos,pos+2*rayon,int(Hauteur/3)-(pos+2*rayon),fill=couleur,outline=couleur,width=3,start=180,extent=90,style='arc')
    Cv.create_arc(Largeur-pos,int(Hauteur/3)-pos,Largeur-(pos+2*rayon),int(Hauteur/3)-(pos+2*rayon),fill=couleur,outline=couleur,width=3,start=270,extent=90,style='arc')
#------------------------------------------------
def onCanvas1XClick(event):
    global Canvas1X_Index

    Canvas1X_Index = Canvas1X_Index + 1
    if Canvas1X_Index == Canvas1X_Number:
       Canvas1X_Index = 0

    print 'Got canvas click', event.x, event.y, event.widget
#------------------------------------------------
def onCanvas2XClick(event):
    global Canvas2X_Index

    Canvas2X_Index = Canvas2X_Index + 1
    if Canvas2X_Index == Canvas2X_Number:
       Canvas2X_Index = 0

    print 'Got canvas click', event.x, event.y, event.widget
#------------------------------------------------
def onCanvas3XClick(event):
    global Canvas3X_Index
    
    Canvas3X_Index = Canvas3X_Index + 1
    if Canvas3X_Index == Canvas3X_Number:
       Canvas3X_Index = 0

    print 'Got canvas click', event.x, event.y, event.widget
    Mafenetre.destroy()
#------------------------------------------------

#------------------------------------------------
def exit():
   Mafenetre.destroy()

#------------------------------------------------
class GuiPart:
   def __init__(self, master, queue, endCommand):
      self.queue = queue

      # Création de la fenêtre principale (main window)

      # Set up the GUI
      #console = Tkinter.Button(master, text='Done', command=endCommand)
      #console.pack()
      # Add more GUI stuff here

#------------------------------------------------
   def processIncoming(self):
      VAL_TMR=VAL_TTL=VAL_BSP=VAL_SOG=VAL_TTG=VAL_BRG=VAL_HDM=VAL_COG=VAL_VMC=VAL_SGA=VAL_CGA=VAL_BGA=""
      VAL_SGG=VAL_SAG=0
      global Canvas1X_Index,Canvas2X_Index,Canvas3X_Index
      global Canvas10_BAR1_pos, Canvas10_BAR1_neg, Canvas10_ARROW1_pos, Canvas10_ARROW1_neg
      global Canvas10_BAR2_pos, Canvas10_BAR2_neg, Canvas10_ARROW2_pos, Canvas10_ARROW2_neg

      """
      Handle all the messages currently in the queue (if any).
      """
      print("Queue size: " + str(self.queue.qsize()))
      while self.queue.qsize():
         try:
            msg = self.queue.get(0)
            self.queue.task_done()
            # Check contents of message and do what it says
            # As a test, we simply print it
            print msg
            # Rafraichit les variables d'affichage
            if   msg[:3] == "SOG": VAL_SOG = msg.split(';')[1]    # Speed Over Ground
            elif msg[:3] == "SGA": VAL_SGA = msg.split(';')[1]    # Speed over Ground Average
            elif msg[:3] == "SGG": VAL_SGG = msg.split(';')[1]    # Speed over Ground Gain
            elif msg[:3] == "SAG": VAL_SAG = msg.split(';')[1]    # Speed over ground Average Gain

            elif msg[:3] == "COG": VAL_COG = msg.split(';')[1]
            elif msg[:3] == "CGA": VAL_CGA = msg.split(';')[1]

            elif msg[:3] == "BRG": VAL_BRG = msg.split(';')[1]
            elif msg[:3] == "BGA": VAL_BGA = msg.split(';')[1]

            elif msg[:3] == "VMC": VAL_TMR = msg.split(';')[1]
            elif msg[:3] == "TMR": VAL_TMR = msg.split(';')[1]
            elif msg[:3] == "TTL": VAL_TTL = msg.split(';')[1]
            elif msg[:3] == "BSP": VAL_BSP = msg.split(';')[1]
            elif msg[:3] == "TTG": VAL_TTG = msg.split(';')[1]
            elif msg[:3] == "HDM": VAL_HDM = msg.split(';')[1]
         except Queue.Empty:
            pass

      # Rafraichit les libelles
      if Canvas1X_Index == 0:
         Canvas10.itemconfigure(Canvas10_LIB1,text="SOG")
         Canvas10.itemconfigure(Canvas10_VAL1,text=VAL_SOG)
         Canvas10.itemconfigure(Canvas10_LIB2,text="SOG~")
         Canvas10.itemconfigure(Canvas10_VAL2,text=VAL_SGA)

         # On efface le bargraph
         Canvas10.delete(Canvas10_BAR1_pos)
         Canvas10.delete(Canvas10_BAR1_neg)
         Canvas10.delete(Canvas10_ARROW1_pos)
         Canvas10.delete(Canvas10_ARROW1_neg)
         Canvas10.delete(Canvas10_BAR2_pos)
         Canvas10.delete(Canvas10_BAR2_neg)
         Canvas10.delete(Canvas10_ARROW2_pos)
         Canvas10.delete(Canvas10_ARROW2_neg)

         VAL_SGG = int(VAL_SGG)
         if VAL_SGG > 0 :
            Canvas10_BAR1_pos = Canvas10.create_rectangle(Largeur-30,65,Largeur-9,65-VAL_SGG/2,fill='#0f0',outline='#0f0',width=0)
            pts = [(Largeur-30,(65-VAL_SGG/2)-2),(Largeur-20,(65-VAL_SGG/2)-2-10),(Largeur-10,(65-VAL_SGG/2)-2)]
            Canvas10_ARROW1_pos = Canvas10.create_polygon(pts, fill='#0f0', outline='#0f0', width=0)
         if VAL_SGG < 0 :
            Canvas10_BAR1_neg = Canvas10.create_rectangle(Largeur-30,65,Largeur-9,65-VAL_SGG/2,fill='red',outline='red',width=0)
            pts = [(Largeur-30,(65-VAL_SGG/2)+2),(Largeur-20,(65-VAL_SGG/2)+2+10),(Largeur-10,(65-VAL_SGG/2)+2)]
            Canvas10_ARROW1_neg = Canvas10.create_polygon(pts, fill='red', outline='red', width=0)

         VAL_SAG = int(VAL_SAG)
         if VAL_SAG > 0 :
            Canvas10_BAR2_pos = Canvas10.create_rectangle(Largeur-30,198,Largeur-9,198-VAL_SAG/2,fill='#0f0',outline='#0f0',width=0)
            pts = [(Largeur-30,(198-VAL_SAG/2)-2),(Largeur-20,(198-VAL_SAG/2)-2-10),(Largeur-10,(198-VAL_SAG/2)-2)]
            Canvas10_ARROW2_pos = Canvas10.create_polygon(pts, fill='#0f0', outline='#0f0', width=0)
         if VAL_SAG < 0 :
            Canvas10_BAR2_neg = Canvas10.create_rectangle(Largeur-30,198,Largeur-9,198-VAL_SAG/2,fill='red',outline='red',width=0)
            pts = [(Largeur-30,(198-VAL_SAG/2)+2),(Largeur-20,(198-VAL_SAG/2)+2+10),(Largeur-10,(198-VAL_SAG/2)+2)]
            Canvas10_ARROW2_neg = Canvas10.create_polygon(pts, fill='red', outline='red', width=0)

         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         Canvas10.place(x=0,y=0)
         Canvas11.place(x=1*Largeur,y=0)
         Canvas12.place(x=2*Largeur,y=0)

      elif Canvas1X_Index == 1:
         Canvas11.itemconfigure(Canvas11_LIB1,text="BSP")
         Canvas11.itemconfigure(Canvas11_VAL1,text=VAL_BSP)
         Canvas11.itemconfigure(Canvas11_LIB2,text="SOG")
         Canvas11.itemconfigure(Canvas11_VAL2,text=VAL_SOG)

         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         Canvas10.place(x=1*Largeur,y=0)
         Canvas11.place(x=0,y=0)
         Canvas12.place(x=2*Largeur,y=0)

      elif Canvas1X_Index == 2:
         Canvas12.itemconfigure(Canvas12_LIB1,text="SOG")
         data = [20, 15, 10, 7, 5, 4, 3, 2, 1, 1, 0, 15, 10, 7, 5, 4, 3, 2, 1, 1]
         c_width = 460
         c_height = 266
         # the variables below size the bar graph
         # experiment with them to fit your needs
         # highest y = max_data_value * y_stretch
         #y_stretch = 15
         y_stretch = 230/max(data)
         # gap between lower canvas edge and x axis
         y_gap = 10
         # stretch enough to get all data items in
         x_stretch = 1
         x_width = 22
         # gap between left canvas edge and y axis
         x_gap = 10
         for x, y in enumerate(data):
            # calculate reactangle coordinates (integers) for each bar
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap - 1
            y1 = c_height - y_gap
            # draw the bar
            Canvas12.create_rectangle(x0, y0, x1, y1, fill="red", outline="red")
            # put the y value above each bar
            #c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         Canvas10.place(x=1*Largeur,y=0)
         Canvas11.place(x=2*Largeur,y=0)
         Canvas12.place(x=0,y=0)

      if Canvas2X_Index == 0:
         Canvas20.itemconfigure(Canvas20_LIB1,text="COG")
         Canvas20.itemconfigure(Canvas20_VAL1,text=VAL_COG)
         Canvas20.itemconfigure(Canvas20_LIB2,text="COG~")
         Canvas20.itemconfigure(Canvas20_VAL2,text=VAL_CGA)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         Canvas20.place(x=0,y=0)
         #Canvas21.place(x=1*Largeur,y=0)

      if Canvas3X_Index == 0:
         Canvas30.itemconfigure(Canvas30_LIB1,text="BRG")
         Canvas30.itemconfigure(Canvas30_VAL1,text=VAL_BRG)
         Canvas30.itemconfigure(Canvas30_LIB2,text="BGA")
         Canvas30.itemconfigure(Canvas30_VAL2,text=VAL_BGA)
         # On déplace les Canvas indésirables dans l'espace non visible de la Frame
         Canvas30.place(x=0,y=0)
         #Canvas31.place(x=1*Largeur,y=0)

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
      self.master.after(250, self.periodicCall)

#------------------------------------------------
   def GPSThread(self):
      self.Last_Val_SOG = 0

      """
      This is where we handle the GPS Communication.
      """
      Log.WriteLine("Première exécution du thread GPS Communication")

      # Initialisation du GPS
      MyGPS = GPS.GPS()

      while self.running:
         # Simulation
         #Val_SOG = round(rand.random()*100,2) # Valeur de 00.00 à 99.99
         #Val_COG = int(rand.random()*360) # Valeur de 0 à 360

         # Acquisitiion des données GPS
         MyGPS.Communicate()
         Val_SOG = float(MyGPS.GPRMC['SOG'])
         Val_COG = int(float(MyGPS.GPRMC['COG']))

         # Moyenne du SOG
         Pile_SOG.pop(0)
         Pile_SOG.append(Val_SOG)
         Somme = 0
         for i in range(len(Pile_SOG)):
            Somme = Somme + Pile_SOG[i]
         Val_SGA = Somme/len(Pile_SOG)

         # Tendance du SOG
         Val_SGG = int((Val_SOG - self.Last_Val_SOG)*100/1)
         if Val_SGG > 100: Val_SGG = 100
         if Val_SGG < -100: Val_SGG = -100
         self.Last_Val_SOG = Val_SGG

         # Tendance de la moyenne du SOG
         Val_SAG = int((Val_SOG - Val_SGA)*100/1)
         if Val_SAG > 100: Val_SAG = 100
         if Val_SAG < -100: Val_SAG = -100

         # Moyenne du COG
         Pile_COG.pop(0)
         Pile_COG.append(Val_COG)
         Somme = 0
         for i in range(len(Pile_COG)):
            Somme = Somme + Pile_COG[i]
         Val_CGA = Somme/len(Pile_COG)

         compass = HMC5883L.hmc5883l(gauss = 4.7, declination = (0,12))
         Val_BRG = compass.degrees(compass.heading())
         Pile_BRG.pop(0)
         Pile_BRG.append(Val_BRG)
         Somme = 0
         for i in range(len(Pile_BRG)):
            Somme = Somme + Pile_BRG[i]
         Val_BGA = Somme/len(Pile_BRG)

         # Ressources envoyées au thread GUI
         self.queue.put("SOG" + ";" + str(round(Val_SOG,2)))         # Speed Over Ground
         self.queue.put("SGA" + ";" + str(round(Val_SGA,2)))         # Speed over Ground Average
         self.queue.put("SGG" + ";" + str(Val_SGG))                  # Speed over Ground Gain
         self.queue.put("SAG" + ";" + str(Val_SAG))                  # Speed over ground Average Gain
         self.queue.put("COG" + ";" + str(Val_COG) + "°".decode('cp1252'))    # Course Over Ground
         self.queue.put("CGA" + ";" + str(Val_CGA) + "°".decode('cp1252'))    # Course over Ground Average
         self.queue.put("BRG" + ";" + str(Val_BRG) + "°".decode('cp1252'))    # Bearing, Cap compas HMC5883L
         self.queue.put("BGA" + ";" + str(Val_BGA) + "°".decode('cp1252'))    # Bearing Average

         #self.queue.put("TMR" + ";" + time.strftime("%H:%M",time.localtime()))
         #self.queue.put("TTL" + ";" + "12:34")
         #self.queue.put("BSP" + ";" + str(round(rand.random(),2)))
         #self.queue.put("VMC" + ";" + str(round(rand.random(),2)))

         #self.queue.put("TTG" + ";" + "11:11")

         # On laisse du temps pour l'exécution des autres threads
         time.sleep(0.100)

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
         time.sleep(0.250)
   
#------------------------------------------------
   def endApplication(self):
      self.running = 0

#------------------------------------------------
rand = random.Random()

Mafenetre = Tk()
Mafenetre.title('')
Mafenetre.overrideredirect(1) # Supprime les bordures de la fenêtre principale
Mafenetre.geometry('480x800+0+0') # Taille et position
Mafenetre['bg']='black' # Couleur de fond

Frame1 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="red")
Frame1.grid(row = 0, columnspan = 1, sticky = W+E+N+S)
Frame2 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="blue")
Frame2.grid(row = 1, columnspan = 1, sticky = W+E+N+S)
Frame3 = Frame(Mafenetre, width = Largeur, height = int(Hauteur/3), bg="green")
Frame3.grid(row = 2, columnspan = 1, sticky = W+E+N+S)

X_LIB1 = 15
Y_LIB1 = 2
X_LIB2 = 15
Y_LIB2 = 135
X_VAL1 = 260
Y_VAL1 = 0
X_VAL2 = 260
Y_VAL2 = 130

# Construction du Canvas 10
Canvas10 = Canvas(Frame1, width = Largeur, height = int(Hauteur/3), bg =ClFond, highlightthickness = 0)
Canvas10.place(x=0,y=0)
Canvas10_LIB1 = Canvas10.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas10_VAL1 = Canvas10.create_text(X_VAL1,Y_VAL1,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Canvas10_LIB2 = Canvas10.create_text(X_LIB2,Y_LIB2,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas10_VAL2 = Canvas10.create_text(X_VAL2,Y_VAL2,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Create_RoundRectangle(Canvas10,2,15,'blue')   # Création de la bordure de canvas
# Création du bargraph supérieur
Canvas10_BAR1_pos = Canvas10.create_rectangle(0,0,0,0,fill='#0f0',outline='green',width=0)
Canvas10_BAR1_neg = Canvas10.create_rectangle(0,0,0,0,fill='red',outline='red',width=0)
Canvas10_BAR2_pos = Canvas10.create_rectangle(0,0,0,0,fill='#0f0',outline='green',width=0)
Canvas10_BAR2_neg = Canvas10.create_rectangle(0,0,0,0,fill='red',outline='red',width=0)
pts = [(0,0),(0,0),(0,0)]
Canvas10_ARROW1_pos = Canvas10.create_polygon(pts, fill='#0f0', outline='black', width=0)
Canvas10_ARROW1_neg = Canvas10.create_polygon(pts, fill='red', outline='black', width=0)
Canvas10_ARROW2_pos = Canvas10.create_polygon(pts, fill='#0f0', outline='black', width=0)
Canvas10_ARROW2_neg = Canvas10.create_polygon(pts, fill='red', outline='black', width=0)

Canvas10.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas

# Construction du Canvas 11
Canvas11 = Canvas(Frame1, width = Largeur, height = int(Hauteur/3), bg =ClFond, highlightthickness = 0)
Canvas11.place(x=0,y=0)
Canvas11_LIB1 = Canvas11.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas11_VAL1 = Canvas11.create_text(X_VAL1,Y_VAL1,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Canvas11_LIB2 = Canvas11.create_text(X_LIB2,Y_LIB2,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas11_VAL2 = Canvas11.create_text(X_VAL2,Y_VAL2,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Create_RoundRectangle(Canvas11,2,15,'blue')   # Création de la bordure de canvas
Canvas11.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas

# Construction du Canvas 12
Canvas12 = Canvas(Frame1, width = Largeur, height = int(Hauteur/3), bg =ClFond, highlightthickness = 0)
Canvas12.place(x=0,y=0)
Canvas12_LIB1 = Canvas12.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Create_RoundRectangle(Canvas12,2,15,'blue')   # Création de la bordure de canvas
Canvas12.bind('<Double-1>',onCanvas1XClick)   # Gestion de l'événement "Double clic" sur le canvas

# Construction du Canvas 20
Canvas20 = Canvas(Frame2, width = Largeur, height = int(Hauteur/3), bg =ClFond, highlightthickness = 0)
Canvas20.place(x=0,y=0)
Canvas20_LIB1 = Canvas20.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas20_VAL1 = Canvas20.create_text(X_VAL1,Y_VAL1,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Canvas20_LIB2 = Canvas20.create_text(X_LIB2,Y_LIB2,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas20_VAL2 = Canvas20.create_text(X_VAL2,Y_VAL2,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Create_RoundRectangle(Canvas20,2,15,'blue')   # Création de la bordure de canvas
Canvas20.bind('<Double-1>',onCanvas2XClick)   # Gestion de l'événement "Double clic" sur le canvas

# Construction du Canvas 30
Canvas30 = Canvas(Frame3, width = Largeur, height = int(Hauteur/3), bg =ClFond, highlightthickness = 0)
Canvas30.place(x=0,y=0)
Canvas30_LIB1 = Canvas30.create_text(X_LIB1,Y_LIB1,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas30_VAL1 = Canvas30.create_text(X_VAL1,Y_VAL1,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Canvas30_LIB2 = Canvas30.create_text(X_LIB2,Y_LIB2,text="---",anchor=NW,font=('Calibri', 14, 'bold'),fill=ClText,justify=LEFT)
Canvas30_VAL2 = Canvas30.create_text(X_VAL2,Y_VAL2,text="---",anchor=N,font=('Calibri', 90, 'bold'),fill=ClText)
Create_RoundRectangle(Canvas30,2,15,'blue')   # Création de la bordure de canvas
Canvas30.bind('<Double-1>',onCanvas3XClick)   # Gestion de l'événement "Double clic" sur le canvas

# ButtonQuit = Button(Canvas10, text='Quit', command=Mafenetre.destroy)
# ButtonQuit.pack()

client = ThreadedClient(Mafenetre)
Mafenetre.mainloop()