import Motori
import BT
import vision
import time
import braccino



vision.view("Go")
print("detected")
BT.send_mess("$VAI#")
BT.sensor_read_prova()
Motori.right(2.3)
Motori.stop()
time.sleep(1)
Motori.straightTime(5.5)  
Motori.stop()
braccino.dancing(10) 
vision.view("Scuola")
Motori.right(2.3)
Motori.stop()
Motori.straightTime(4.5)
Motori.stop()


