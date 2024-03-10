# intended to manage the system that notifies for Printers.
# insert data to Smart home DB
import paho.mqtt.client as mqtt
import time
import random
from mqtt_init import *
from icecream import ic
from datetime import datetime
import data_acq as da

def time_format():
    return f'{datetime.now()}  Manager|> '

ic.configureOutput(prefix = time_format)
ic.configureOutput(includeContext = False)  #use True for including script file context file

# Define callback functions
def on_log(client, userdata, level, buf):
        ic("log: "+buf)
            
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        ic("connected OK")                
    else:
        ic("Bad connection Returned code= ", rc)
        
def on_disconnect(client, userdata, flags, rc=0):
    ic("DisConnected result code "+str(rc))
        
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    ic("message from: " + topic, m_decode)

    pages = float(m_decode.split(' ')[1])
    ink = float(m_decode.split(' ')[3])

    da.add_printer_data(ink, pages)

    if ink < 20 and ink > 0:
        ic("ALERT: Ink is ended! " + m_decode)
        send_msg(client, warning_topic, "ALERT: Ink is about to be end! " + m_decode)
        ink = -1
    elif ink < 100 and ink > 0:
        ic("ALERT: The ink is running dangerously low " + m_decode)
        send_msg(client, warning_topic, "ALERT: The ink is running dangerously low " + m_decode)

    if pages % 1000 > 0 and pages % 1000 < 5:
        ic("ALERT: Many pages have been printed; please ensure the machine is well-maintained and verify that everything is in proper order " + m_decode)
        send_msg(client, warning_topic, "ALERT: Many pages have been printed; please ensure the machine is well-maintained and verify that everything is in proper order " + m_decode)

def send_msg(client, topic, message):
    ic("Sending Message: " + message)
    client.publish(topic, message)

def client_init(cname):
    r = random.randrange(1, 10000000)
    ID = str(cname+str(r+21))

    print(ID)
    client = mqtt.Client(ID, clean_session=True) # create new client instance
    # define callback function       
    client.on_connect=on_connect  # bind callback function
    client.on_disconnect=on_disconnect
    client.on_log = on_log
    client.on_message = on_message
    if username !="":
        client.username_pw_set(username, password)        
    ic("Connecting to broker ",broker_ip, port)
    client.connect(broker_ip,int(port)) # connect to broker
    return client

def main():
    cname = "Manager-"
    client = client_init(cname)
    # main monitoring loop
    client.loop_start()  # Start loop
    client.subscribe(comm_topic+'/5976397/sts')
    
    try:
        while conn_time==0:
            time.sleep(conn_time+manag_time)
            ic(f"Time for sleep {conn_time+manag_time}")
            time.sleep(3)       
        ic("con_time ending") 
    except KeyboardInterrupt:
        client.disconnect() # disconnect from broker
        ic("interrrupted by keyboard")

    # Stop loop
    client.loop_stop()
    # end session
    client.disconnect()
    # disconnect from broker
    ic("End manager run script")

if __name__ == '__main__':
    main()

