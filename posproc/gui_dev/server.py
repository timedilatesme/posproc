import PySimpleGUI as sg
from posproc import*

# EVENTS
SIFTED_KEY_EVENT = '-sifted_key-'
INPUT_KEY_TYPE_STR_EVENT = '-input_key_type_1-'
INPUT_KEY_TYPE_RANDOM_EVENT = '-input_key_type_2-'
INPUT_KEY_TYPE_FILE_EVENT = '-input_key_type_3-'
INPUT_KEY_TEXT_EVENT = '-input_key_text-'
INPUT_KEY_BOX_EVENT = '-input_key_box-'
INPUT_FILE_EVENT = '-input_file-'
INPUT_IP_EVENT = '-input_ip-'
INPUT_PORT_EVENT = '-input_port-'
SUBMIT_BUTTON_EVENT = '-submit_button'
START_LISTENING_BUTTON_EVENT = '-start_listening_button-'
RESET_BUTTON_EVENT = '-reset_button-'
EXIT_BUTTON_EVENT = 'Exit'

# tooltips
INITIAL_KEY_TOOLTIP = "Please Choose the Method for providing the sifted Raw Key"


# RADIO ID
INPUT_KEY_RADIO_ID = '-input_key_radio_id-'

# layouts

parameter_tab_layout = [
    [sg.Text('Initial Key Type :',justification='r'),
     sg.Radio(' Input Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_STR_EVENT,enable_events=True),
     sg.Radio(' Random Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_RANDOM_EVENT,enable_events=True),
     sg.Radio(' Browse Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_FILE_EVENT, enable_events=True)],
    [sg.Text('Input the Key',  key=INPUT_KEY_TEXT_EVENT,justification='c'),
     sg.Input(key=INPUT_KEY_BOX_EVENT, justification='c'),
     sg.FileBrowse(disabled=True, key=INPUT_FILE_EVENT)],
    [sg.Text('IP',justification='c'), sg.Input(constants.LOCAL_IP,key=INPUT_IP_EVENT,size = (15,1),justification='c'),
     sg.Text('Port',justification='c'), sg.Input(constants.LOCAL_PORT,key=INPUT_PORT_EVENT,size = (8,1),justification='c')],
    [sg.Text('')],
    [sg.Button('Submit',key = SUBMIT_BUTTON_EVENT),
     sg.Button('Start Listening',key = START_LISTENING_BUTTON_EVENT,disabled=True)],
    [sg.Button('Reset', key = RESET_BUTTON_EVENT), sg.Button('Exit',  key=EXIT_BUTTON_EVENT)]
]

# result_tab_layout = [
#     [sg.Text('Initial Sifted Key'), 
#      sg.Text('111', background_color='#F0F0F0', key=)],
#     [sg.Text('')],
# ]


# tabgrp = [
#     [sg.TabGroup('Parameters', parameter_tab_layout),
#      sg.TabGroup('Results', result_tab_layout)],
# ]

window = sg.Window("QKD Server",parameter_tab_layout,element_justification= 'c')

alice = QKDServer('Alice')

while True:
    event, values = window.read()
    
    #Event Conditioning
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    if event == INPUT_KEY_TYPE_STR_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=True)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Input the Key')
    
    if event == INPUT_KEY_TYPE_RANDOM_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=True)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Enter Key Length')
    
    if event == INPUT_KEY_TYPE_FILE_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=False)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Browse Key')
    
    if event == SUBMIT_BUTTON_EVENT:
        if window.Element(INPUT_KEY_TYPE_STR_EVENT).get():
            alice.set_key(values[INPUT_KEY_BOX_EVENT])
        elif window.Element(INPUT_KEY_TYPE_RANDOM_EVENT).get():
            pass
        elif window.Element(INPUT_KEY_TYPE_FILE_EVENT).get():
            key_path = values[INPUT_KEY_BOX_EVENT]
            with open(key_path) as fh:
                alice_key_f = Key(key_as_str=fh.read())
            alice.set_key(alice_key_f)
        
        alice.address = (values[INPUT_IP_EVENT], int(values[INPUT_PORT_EVENT]))
        window.Element(START_LISTENING_BUTTON_EVENT).Update(disabled=False)
    if event == START_LISTENING_BUTTON_EVENT:
        alice.start_listening()
        print(alice.get_key())
    
    if event == RESET_BUTTON_EVENT:
        alice.stopServer()
        window.Element(START_LISTENING_BUTTON_EVENT).Update(disabled=True)

window.close()