import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.InputText(default_text='username',size=(31,1)),sg.InputText(default_text='passwordddddddddddddd',size=(30,1),password_char='*'),sg.Button('Log in')],
            [sg.Text('Topic/chat room'), sg.InputText(size=(47,1)),sg.Button('Connect')],
            [sg.Multiline(size=(70, 27), key='textbox',autoscroll=True,disabled=True)],
            [sg.InputText(size=(66,1),key='msg'),sg.Button('Send',bind_return_key=True)],
            [sg.Button('Close Window')]]  

window = sg.Window('Client chat', layout, size=(540,600)).Finalize()
#window.Maximize()
window.Element('textbox').bind("<FocusIn>", '+FOCUS_IN+')
window.Element('textbox').bind("<FocusOut>", '+FOCUS_OUT+')

x = ""

while True:
    event, values = window.read()
    if event in (None, 'Close Window'): 
        break
    x += values['msg'] + "\n"
    
    window['textbox'].Update(x)
    window['msg'].Update('')

window.close()