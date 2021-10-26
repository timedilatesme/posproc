import PySimpleGUI as sg
from posproc import*
import clipboard

# METHODS :
def check_valid_key_box_input(key_str):
    t = set(key_str)
    if t in (set('01'),set('0'),set('1')):
        return True
    else:
        return False
    
def gui_console_print(text:str,window: sg.Window):
    current_text_console = window.Element(CONSOLE_EVENT).Get()
    window.Element(CONSOLE_EVENT).Update(
        current_text_console + text)

# Theming
sg.theme('DarkAmber')
CONSOLE_TEXT_COLOR = '#00ffff'
CONSOLE_BACKGROUND_COLOR = '#000000'


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
INPUT_QBER_THRESHOLD_EVENT ='-input_qber_threshold' 
INPUT_QBER_FRACTION_EVENT = '-input_qber_fraction-'
INPUT_ERROR_CORRECTION_ALGORITHM_EVENT ='-input_error_correction_algorithm-'
INPUT_PRIVACY_AMPLIFICATION_ALGORITHM_EVENT ='-input_privacy_amplification_algorithm-'
INPUT_FINAL_KEY_SIZE_EVENT = "-input_final_key_size-"
SUBMIT_BUTTON_EVENT = '-submit_button'
START_CONNECTING_BUTTON_EVENT = '-start_connecting_button-'
RESET_BUTTON_EVENT = '-reset_button-'
EXIT_BUTTON_EVENT = 'Exit'
CONSOLE_EVENT = '-console-'
COPY_CLIPBOARD_EVENT = '-copy_clipboard-'
OUTPUT_KEY_BOX_EVENT = '-output_key_box-'
TIME_OUTPUT_EVENT = '-time_output_-'
RECONCILIATION_TIME_OUTPUT_EVENT = '-reconciliation_time_output-'
QKD_TIME_OUPUT_EVENT = '-qkd_time_output-'
FINAL_KEY_LENGTH_OUTPUT = '-final_key_length-'
QBER_OUTPUT_EVENT = '-qber_output-'
FRACTION_OUTPUT_EVENT = '-fraction_output-'
PA_ALGORITHM_EVENT = '-pa_algorithm-'
RECONCILIATION_ALGORITHM_EVENT = '-reconciliation_algorithm-'
ASK_PARITY_BLOCKS_AND_BITS_EVENT = '-ask_parity_blocks_and_bits-'
REALISTIC_EFFICIENCY_EVENT = '-realistic_efficiency-'
UNREALISTIC_EFFICIENCY_EVENT ='-unrealistic_efficiency-'


# tooltips
INITIAL_KEY_TOOLTIP = "Please Choose the Method for providing the sifted Raw Key"

#bool
error = False

# RADIO ID
INPUT_KEY_RADIO_ID = '-input_key_radio_id-'


#CONSTANTS
LIST_ERROR_CORECTION_ALGOS = ['CASCADE','BICONF','YANETAL']
LIST_PRIVACY_AMPLIFACTION_ALGOS = ['SHA','BLAKE','MD']

# layouts

'''parameter_tab_layout = [
    [sg.Text('Initial Key Type :',justification='r'),
     sg.Radio(' Input Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_STR_EVENT,enable_events=True),
    #  sg.Radio(' Random Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_RANDOM_EVENT,enable_events=True),
     sg.Radio('Browse Key:', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_FILE_EVENT, enable_events=True)],
    [sg.Text('Input the Key:',  key=INPUT_KEY_TEXT_EVENT,justification='c'),
     sg.Input(key=INPUT_KEY_BOX_EVENT, justification='c', disabled=True),
     sg.FileBrowse(disabled=True, key=INPUT_FILE_EVENT)],
    [sg.Text('IP',justification='c'), sg.Input(constants.LOCAL_IP,key=INPUT_IP_EVENT,size = (15,1),justification='c'),
     sg.Text('Port',justification='c'), sg.Input(constants.LOCAL_PORT,key=INPUT_PORT_EVENT,size = (8,1),justification='c')],
    [sg.Text("QBER Threshold:",justification='c'),sg.Input(key = INPUT_QBER_THRESHOLD_EVENT,justification='c',size = (5,1)),
    sg.Text("QBER Fraction:",justification='c'),sg.Input(key=INPUT_QBER_FRACTION_EVENT,justification='c',size = (5,1))],
    [sg.Text("Error Correction Algorithm:", justification='c'),sg.Combo(LIST_ERROR_CORECTION_ALGOS,key = INPUT_ERROR_CORRECTION_ALGORITHM_EVENT),
    sg.Text("Privacy Amplification Algorithm:", justification='c'),sg.Combo(LIST_PRIVACY_AMPLIFACTION_ALGOS,key = INPUT_PRIVACY_AMPLIFICATION_ALGORITHM_EVENT)],
    [sg.Text("Final Key Size:",justification='c'),sg.Input(key=INPUT_FINAL_KEY_SIZE_EVENT,justification='c',size = (5,1))],
   [sg.Text('')],

    [sg.Button('Submit',key = SUBMIT_BUTTON_EVENT),
     sg.Button('Connect',key = START_CONNECTING_BUTTON_EVENT,disabled=True),
     sg.Button('Reset', key = RESET_BUTTON_EVENT), sg.Button('Exit',  key=EXIT_BUTTON_EVENT)],
]
'''

initialization_frame_layout = [ [sg.T('Provide the sifted key in binary format')],
                                [sg.Text('Initial Key Type :',justification='r'),
                                sg.Radio(' Input Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_STR_EVENT,enable_events=True),
                                sg.Radio('Browse Key:', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_FILE_EVENT, enable_events=True)],
                                [sg.Text('Input the Key:',  key=INPUT_KEY_TEXT_EVENT,justification='c'),
                                sg.Input(key=INPUT_KEY_BOX_EVENT, justification='c', disabled=True),
                                sg.FileBrowse(disabled=True, key=INPUT_FILE_EVENT)],
                                [sg.Text('IP',justification='c'), sg.Input(constants.LOCAL_IP,key=INPUT_IP_EVENT,size = (15,1),justification='c'),
                                sg.Text('Port',justification='c'), sg.Input(constants.LOCAL_PORT,key=INPUT_PORT_EVENT,size = (8,1),justification='c')]
                            ]
parameter_frame_layout = [  [sg.T('Initialize the required parameters')],
                            [sg.Text("QBER Threshold:",justification='c'),sg.Input(key = INPUT_QBER_THRESHOLD_EVENT,justification='c',size = (5,1)),
                            sg.Text("QBER Fraction:",justification='c'),sg.Input(key=INPUT_QBER_FRACTION_EVENT,justification='c',size = (5,1))],
                            [sg.Text("EC Algorithm:", justification='c'),sg.Combo(LIST_ERROR_CORECTION_ALGOS,key = INPUT_ERROR_CORRECTION_ALGORITHM_EVENT),
                            sg.Text("PA Algorithm:", justification='c'),sg.Combo(LIST_PRIVACY_AMPLIFACTION_ALGOS,key = INPUT_PRIVACY_AMPLIFICATION_ALGORITHM_EVENT)],
                            [sg.Text("Final Key Size:",justification='c'),sg.Input(key=INPUT_FINAL_KEY_SIZE_EVENT,justification='c',size = (5,1))]
                        ]

opening_tab_layout = [
                        [sg.Frame('Key Initialization',initialization_frame_layout,font= 'Arial', title_color='lightblue',element_justification='c'), 
                        sg.Frame('Parameter Initialization ',parameter_frame_layout, font = 'Any 12', title_color='lightblue',element_justification='c')],
                        [sg.Button('Submit',key = SUBMIT_BUTTON_EVENT),
                        sg.Button('Connect',key = START_CONNECTING_BUTTON_EVENT,disabled=True),
                        sg.Button('Reset', key = RESET_BUTTON_EVENT), sg.Button('Exit',  key=EXIT_BUTTON_EVENT)]
                    ]

QKD_stats_frame_layout = [
                            [sg.Text("Final Key Length:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=FINAL_KEY_LENGTH_OUTPUT)],
                            [sg.Text("Time for:"), sg.Radio('Reconciliation',group_id=TIME_OUTPUT_EVENT,key = RECONCILIATION_TIME_OUTPUT_EVENT,enable_events=True),
                            sg.Radio('QKD',group_id=TIME_OUTPUT_EVENT,key = QKD_TIME_OUPUT_EVENT,enable_events=True),sg.InputText('',readonly=True,size=(5,1))],
                            [sg.Text("QBER:",justification='l'), sg.InputText('',readonly=True,size=(5,1),key= QBER_OUTPUT_EVENT),sg.Text('         ') ,sg.Text("Fraction Used"), sg.InputText('',readonly=True,size=(5,1),key=FRACTION_OUTPUT_EVENT)],
                            [sg.Text("Algorithm for Privacy Amplification:",justification='l'),sg.InputText('',readonly=True,size=(10,1),key=PA_ALGORITHM_EVENT)]
                        ]

reconciliation_stats_frame_layout = [

                            [sg.Text("Reconciliation Algorithm:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=RECONCILIATION_ALGORITHM_EVENT)],
                            [sg.Text("Parity Blocks Messages & Bits:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=ASK_PARITY_BLOCKS_AND_BITS_EVENT)],
                            [sg.Text("Unrealistic Efficiency:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key = UNREALISTIC_EFFICIENCY_EVENT)],
                            [sg.Text("Realistic Efficiency:",justification='l'),sg.InputText('',readonly=True,size=(10,1),justification='r',key=REALISTIC_EFFICIENCY_EVENT)]
                            ]

                
result_tab_layout = [
                [sg.Text('')],   
                [sg.Frame('QKD Stats',QKD_stats_frame_layout, font= 'Arial', title_color='lightblue',element_justification='l'), sg.Frame('Reconciliation Stats',reconciliation_stats_frame_layout, font = 'Any 12', title_color='lightblue',element_justification='r')],
                 
                [sg.Text('Save the Final Key:', justification='c'),
                sg.InputText(key=OUTPUT_KEY_BOX_EVENT, justification='c'),sg.FileSaveAs(),
                sg.Button('Save / Copy to Clipboard', key = COPY_CLIPBOARD_EVENT)]
                ]




tabs = [
    [sg.Tab('Parameters', opening_tab_layout, element_justification='c'),
     sg.Tab('Results', result_tab_layout,element_justification='c')],
]

tabgrp = [[sg.TabGroup(tabs,)],
          [sg.Multiline("Welcome to QKD Client!", key=CONSOLE_EVENT, enable_events=True,
                        size=(122, 10), background_color=CONSOLE_BACKGROUND_COLOR,
                        text_color=CONSOLE_TEXT_COLOR, no_scrollbar=True)],
          ]

window = sg.Window("QKD Server",tabgrp)

alice = QKDServer('Alice')

# console print
def gui_console_print(text: str, window: sg.Window = window):
    current_text_console = window.Element(CONSOLE_EVENT).Get()
    window.Element(CONSOLE_EVENT).Update(
        current_text_console + '\n' +text)

while True:
    event, values = window.read()
    
    #Event Conditioning
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    if event == INPUT_KEY_TYPE_STR_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=True)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Input the Key')
        window.Element(INPUT_KEY_BOX_EVENT).Update(disabled = False)
    # if event == INPUT_KEY_TYPE_RANDOM_EVENT:
    #     window.Element(INPUT_FILE_EVENT).Update(disabled=True)
    #     window.Element(INPUT_KEY_TEXT_EVENT).Update('Enter Key Length')
    
    if event == INPUT_KEY_TYPE_FILE_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=False)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Browse Key')
        window.Element(INPUT_KEY_BOX_EVENT).Update(disabled=False)
    
    if event == SUBMIT_BUTTON_EVENT:
        error = False
        if window.Element(INPUT_KEY_TYPE_STR_EVENT).get():
            key_str = values[INPUT_KEY_BOX_EVENT]
            if check_valid_key_box_input(key_str):
                alice.set_key(Key(key_as_str=key_str))
            else:
                sg.popup('Please Enter Key in Binary Format')
                error = True
        # elif window.Element(INPUT_KEY_TYPE_RANDOM_EVENT).get():
        #     pass
        elif window.Element(INPUT_KEY_TYPE_FILE_EVENT).get():
            key_path = values[INPUT_KEY_BOX_EVENT]
            with open(key_path) as fh:
                alice_key_f = Key(key_as_str=fh.read())
            alice.set_key(alice_key_f)
            
        if not error:
            alice.address = (values[INPUT_IP_EVENT],
                             int(values[INPUT_PORT_EVENT]))
            window.Element(START_CONNECTING_BUTTON_EVENT).Update(disabled=False)
            gui_console_print('>>> Initial Key Set')
    if event == START_CONNECTING_BUTTON_EVENT:
        alice.start_listening()
        @alice.event
        def onClientConnected(Client):
            if alice.authentication_required:
                Client.send_message('authentication', 'Initialize')
            console_output(f'>>> Client @ {Client.address} is connected!')
            gui_console_print(f'>>> Client @ {Client.address} is connected!')
        gui_console_print('>>> Listening on {}'.format(alice.address))
        
    if event == RESET_BUTTON_EVENT:
        alice.stopServer()
        window.Element(START_CONNECTING_BUTTON_EVENT).Update(disabled=True)
        window.Element(CONSOLE_EVENT).Update("Welcome to QKD Server!")
    
    if event == COPY_CLIPBOARD_EVENT:
        clipboard.copy(alice.get_key().__str__())
        if values[OUTPUT_KEY_BOX_EVENT] != '':    
            with open(values[OUTPUT_KEY_BOX_EVENT], 'w') as fh:
                fh.write(alice.get_key().__str__())

    if event == QKD_TIME_OUPUT_EVENT:
        pass
    if event == RECONCILIATION_TIME_OUTPUT_EVENT:
        pass


window.close()
