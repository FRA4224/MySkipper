# MySkipper
Réalisation d'une centrale de navigation à la voile à base de Raspberry

L'objectif de ce projet est de réaliser une centrale de navigation pour voilier à bas coût.
Le programme fonctionne actuellement sur un Raspberry Pi 3 équipé d'un écran 480x800 pixels.
Un module I2C BMP180 permet l'acquisition de la pression atmosphérique et la température.
Un module I2C HMC5883L permet l'acquisition du cap magnétique.
Un GPS USB BU-353S4 permet l'acquisition du SOG (Speed On Ground), COG (Course On Ground) et des coordonnées GPS.

Le but est de placer ce Raspberry et son écran dans un boitier étanche au pied du mât et d'afficher des données pertinentes pour la croisière et surtout la régate...

Les fonctionnalités souhaitées pourraient être:
- Coordonnées GPS
- Affichage BSP/HDG/SOG/COG/TTG/BRG/CMG/XTE
- MOB
- Heures de lever et coucher du soleil
- Mise en veille et sortie automatiques
- Alarme Mouillage
- Alarme route
- Timer
- Temps à la ligne
- Avantage à la ligne
- Optimisation/Contrôle des réglages en navigation
- Temps de course/Heure d'arrivée
- Temps de course concurrents
- Calcul du temps compensé OSIRIS
- Création de waypoints
- Création de routes
- Affichage AIS
- Détermination de la polaire
- Indicateur du jeu de voile optimal
- Indicateurs de performance Temps Réel
- Historisation des données critiques
- Carnet de réglages
- Mesure des pertes au virement
- ...
