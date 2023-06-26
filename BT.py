import serial
import time
import Motori
import Led

# apertura della connessione seriale al dispositivo //initializaton of the serial connection with the device
uart_ch_gv = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=1)
 
# funzione per inviare un messaggio al dispositivo //function for sending a message to the device
def send_mess(mess):
    msg=""
    ricevuto = False
    timeout = False
    encode_mess=mess.encode('UTF-8')
    while not ricevuto:
        # invio del messaggio //sends the message
        uart_ch_gv.write(encode_mess)
        t0 = time.time()
        print(mess)
        while not ricevuto and not timeout:
            # lettura della risposta //reading the response
            data = uart_ch_gv.read(1)
            data1 = data.decode('UTF-8', 'ignore')
            if data1 != "":
                if data1 == "$":
                    msg = ""
                elif data1 == '#':
                    # se la risposta è ACK, il messaggio è stato ricevuto correttamente //if the response is ACK, it mean that the message was received correctly
                    print(msg)
                    if msg == "ACK":
                        Led.yellow()
                        print("ho ricevuto ACK")
                        ricevuto = True
                elif data1 >= "A" and data1 <="Z":
                    msg += data1
            uart_ch_gv.flush()
            t1 = time.time()
            # timeout di 5 secondi // 5 seconds timeout
            if not ricevuto and (t1 - t0) > 5:
                timeout = True
                break

# funzione per leggere i dati dal sensore   // function for reading values off the sensor
def sensor_read():
    # apertura della connessione seriale al sensore    //initializaton of the serial connection with the sensor
    uart_channel = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=1)
    data=b''
    t0=time.time()
    distance=150
    while distance > 120 and time.time()-t0 < 1:
        distance_str = ""
        data1 = ""
        while data1 != "!":
            # lettura del dato   //reads the data
            data = uart_channel.read(1)
            data1 = data.decode('UTF-8')
            distance_str += data1
        distance = int(distance_str[:-1])
        print(distance)
        print(time.time()-t0)
    print("Girare")
    # chiusura delle connessioni seriali    //stops the serial communication
    uart_ch_gv.close()
    uart_channel.close()

# funzione per leggere i dati dal sensore e muovere il robot    //function for reading data off the sensor and for moving the robot
def sensor_read_prova():
    # apertura della connessione seriale al sensore     //initializaton of the serial connection with the sensor
    uart_channel = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=1)
    data=b''
    t0=time.time()
    distance=89
    while distance > 70 and time.time()-t0 < 3.6:
        distance_str = ""
        data1 = ""
        while data1 != "!" and time.time()-t0 < 3.6:
            # movimento del robot    //moves the robot
            Motori.straight()
            # lettura del dato      //reads the data
            data = uart_channel.read(1)
            data1 = data.decode('UTF-8')
            distance_str += data1
        distance = int(distance_str[:-1])
        print(distance)
        print(time.time()-t0)

    # il robot si ferma   //the robot stops
    Motori.stop()
   
    print("Girare")
    # chiusura delle connessioni seriali    //stop the serial communciation
    uart_ch_gv.close()
    uart_channel.close()
