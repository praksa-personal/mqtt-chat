import PySimpleGUI as sg
import paho.mqtt.client as mqtt
import time
import random

def connect_mqtt(user,pw):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client_id = f'python-mqtt-{random.randint(0, 100)}'
    client = mqtt.Client(client_id,clean_session=True,protocol=mqtt.MQTTv31)
    client.username_pw_set(user, pw)
    client.on_connect = on_connect
    client.connect("localhost", 1883)
    return client

def subscribe(client: mqtt,topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #global mail
        #mail += msg.payload.decode() + "\n"
        global user
        if(msg.payload.decode().startswith(user) == False):
            global window
            global chat_box
            chat_box += msg.payload.decode() + "\n" 
            window['textbox'].Update(chat_box)
            window['msg'].Update('')
    client.subscribe(topic)
    client.on_message = on_message


def publish(client,topic,user,msg):
    fmsg = user + ": " + msg
    result = client.publish(topic, fmsg, qos=1)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    return fmsg

def will_set(client,topic,user):
    client.will_set(topic + "/dc", user +
                            " Gone Offline", qos=1, retain=False) 

                            #last will fix to do
###########################

# def check_mail():
#     global mail
#     flag = 0
#     temp = ""
#     if(mail != ""):
#         #print(mail)
#         temp = mail
#         flag = 1
#         mail = ""
#     return (flag,temp)
    

sg.theme('SystemDefaultForReal')   
layout = [  [sg.InputText(default_text='username',size=(31,1)),sg.InputText(default_text='passwordddddddddddddd',size=(30,1),password_char='*')],
            [sg.Text('Topic/chat room'), sg.InputText(size=(47,1)),sg.Button('Connect')],
            [sg.Multiline(size=(70, 27), key='textbox',autoscroll=True,disabled=True)],
            [sg.InputText(size=(66,1),key='msg'),sg.Button('Send',bind_return_key=True)],
            [sg.Button('Close Window')]]  
window = sg.Window('Client chat', layout, size=(540,600)).Finalize()
window.Element('textbox').bind("<FocusIn>", '+FOCUS_IN+')
window.Element('textbox').bind("<FocusOut>", '+FOCUS_OUT+')

user = ""
pw = ""
topic = ""
chat_box = ""
msg = ""
mail = ""

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
            break
    if event in (None, 'Close Window'): 
        break
    if event == 'Connect':
        user = values[0]
        pw = values[1]
        topic = values[2]
        client = connect_mqtt(user,pw)
        will_set(client,topic,user)
        subscribe(client,topic)
        client.loop_start()

    event, values = window.read(timeout=1)
    chat_box = "Connected to room " + topic +"\n"
    window['textbox'].Update(chat_box)
    event, values = window.read(timeout=1)

    while(True):
        event, values = window.read(timeout=1)# ? timeout treba ili ne 
        if event == sg.WIN_CLOSED:
            client.loop_stop()
            break
        if event == 'Send':
            fmsg = publish(client,topic,user,values['msg'])
            chat_box += fmsg + "\n" 
            window['textbox'].Update(chat_box)
            window['msg'].Update('')

        # flag,rec = check_mail()
        # if(flag):
        #     chat_box += fmsg + "\n" 
        #     window['textbox'].Update(chat_box)
        #     window['msg'].Update('')

window.close()
