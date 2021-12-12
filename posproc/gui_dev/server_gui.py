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
SUBMIT_BUTTON_EVENT = '-submit_button'
START_LISTENING_BUTTON_EVENT = '-start_listening_button-'
RESET_BUTTON_EVENT = '-reset_button-'
EXIT_BUTTON_EVENT = 'Exit'
CONSOLE_EVENT = '-console-'
COPY_CLIPBOARD_EVENT = '-copy_clipboard-'
OUTPUT_KEY_BOX_EVENT = '-output_key_box-'

RECONCILIATION_TIME_OUTPUT_EVENT = '-reconciliation_time_output-'
QKD_TIME_OUTPUT_EVENT = '-qkd_time_output-'
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
TIME_OUTPUT_EVENT = '-time_output_-'
TEXT_TIME_OUTPUT_EVENT = '-text_time_output-'


# layouts

initialization_frame_layout = [ [sg.T('Provide the sifted key in binary format')],
                                [sg.Text('Initial Key Type :',justification='r'),
                                sg.Radio(' Input Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_STR_EVENT,enable_events=True),
                                #  sg.Radio(' Random Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_RANDOM_EVENT,enable_events=True),
                                sg.Radio(' Browse Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_FILE_EVENT, enable_events=True)],
                                [sg.Text('Input the Key:',  key=INPUT_KEY_TEXT_EVENT,justification='c'),
                                sg.Input(key=INPUT_KEY_BOX_EVENT, justification='c', disabled=True),
                                sg.FileBrowse(disabled=True, key=INPUT_FILE_EVENT)],
                                [sg.Text("Server Address:",justification='l'),sg.Text('IP',justification='c'), sg.Input(constants.LOCAL_IP,key=INPUT_IP_EVENT,size = (15,1),justification='c'),
                                sg.Text('Port',justification='c'), sg.Input(constants.LOCAL_PORT,key=INPUT_PORT_EVENT,size = (8,1),justification='c')]
                                ]

opening_tab_layout = [ [sg.Text('')],
                        [sg.Frame('Key Initialization',initialization_frame_layout,font= 'Arial', title_color='lightblue',element_justification='c')],
                        [sg.Text('',size=(1,3))],
                        [sg.Button('Submit',key = SUBMIT_BUTTON_EVENT),
                        sg.Button('Start Listening',key = START_LISTENING_BUTTON_EVENT,disabled=True),
                        sg.Button('Reset', key = RESET_BUTTON_EVENT), sg.Button('Exit',  key=EXIT_BUTTON_EVENT)],
                        [sg.Text('')]
                    ]

QKD_stats_frame_layout = [
                            [sg.Text("Final Key Length:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=FINAL_KEY_LENGTH_OUTPUT,text_color='black')],
                            [sg.Text("Time for:"), sg.Radio('Reconciliation',group_id=TIME_OUTPUT_EVENT,key = RECONCILIATION_TIME_OUTPUT_EVENT,enable_events=True),
                            sg.Radio('QKD',group_id=TIME_OUTPUT_EVENT,key = QKD_TIME_OUTPUT_EVENT,enable_events=True),sg.InputText('',readonly=True,size=(5,1),text_color='black', key = TEXT_TIME_OUTPUT_EVENT)],
                            [sg.Text("QBER:",justification='l'), sg.InputText('',readonly=True,size=(5,1),key= QBER_OUTPUT_EVENT,text_color='black'),sg.Text('         ') ,sg.Text("Fraction Used"), sg.InputText('',readonly=True,size=(5,1),key=FRACTION_OUTPUT_EVENT,text_color='black')],
                            [sg.Text("Algorithm for Privacy Amplification:",justification='l'),sg.InputText('',readonly=True,size=(10,1),key=PA_ALGORITHM_EVENT,text_color='black')],
                        ]

reconciliation_stats_frame_layout = [
                            [sg.Text("Reconciliation Algorithm:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=RECONCILIATION_ALGORITHM_EVENT,text_color='black')],
                            [sg.Text("Parity Blocks Messages & Bits:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=ASK_PARITY_BLOCKS_AND_BITS_EVENT,text_color='black')],
                            [sg.Text("Unrealistic Efficiency:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key = UNREALISTIC_EFFICIENCY_EVENT,text_color='black')],
                            [sg.Text("Realistic Efficiency:",justification='l'),sg.InputText('',readonly=True,size=(10,1),justification='r',key=REALISTIC_EFFICIENCY_EVENT,text_color='black')],
                            ]

                
result_tab_layout = [ [sg.Text('')],
                [sg.Frame('QKD Stats',QKD_stats_frame_layout, font= 'Arial', title_color='lightblue',element_justification='l'), sg.Frame('Reconciliation Stats',reconciliation_stats_frame_layout, font = 'Arial', title_color='lightblue',element_justification='r')],
                [sg.Text('',size =(1,3))],
                [sg.Text('Save the Final Key:', justification='c'),
                sg.InputText(key=OUTPUT_KEY_BOX_EVENT, justification='c'),sg.FileSaveAs(),
                sg.Button('Save / Copy to Clipboard', key = COPY_CLIPBOARD_EVENT)]
                ]




tabs = [
    [sg.Tab('Parameters', opening_tab_layout, element_justification='c'),
     sg.Tab('Results', result_tab_layout,element_justification='c')],
]

tabgrp = [[sg.TabGroup(tabs,)],
          [sg.Multiline("Welcome to QKD Server!", key=CONSOLE_EVENT, enable_events=True,
                        size=(100, 10), background_color=CONSOLE_BACKGROUND_COLOR,
                        text_color=CONSOLE_TEXT_COLOR, no_scrollbar=True)],
          ]

window = sg.Window("QKD Server",tabgrp)

alice = QKDServer('Alice', gui_window=window)

final_data_to_display = None
@alice.event
def final_data_to_display_on_gui(Client, Content):
    global final_data_to_display
    final_data_to_display = Content
    window.Element(FINAL_KEY_LENGTH_OUTPUT).Update(final_data_to_display['final_key_length'])
    window.Element(QBER_OUTPUT_EVENT).Update(final_data_to_display['qber'])
    window.Element(FRACTION_OUTPUT_EVENT).Update(final_data_to_display['fraction_for_qber'])
    window.Element(PA_ALGORITHM_EVENT).Update(final_data_to_display['algorithm_pa'])
    window.Element(RECONCILIATION_ALGORITHM_EVENT).Update(final_data_to_display['recon_algo'])
    window.Element(ASK_PARITY_BLOCKS_AND_BITS_EVENT).Update(str(final_data_to_display['parity_msgs_bits'][0]) + ' & ' + str(final_data_to_display['parity_msgs_bits'][1]))
    window.Element(UNREALISTIC_EFFICIENCY_EVENT).Update("{:.2f}".format(final_data_to_display['unrealistic_efficiency']))
    window.Element(REALISTIC_EFFICIENCY_EVENT).Update("{:.2f}".format(final_data_to_display['realistic_efficiency']))
    # print(final_data_to_display)

# EVENT HANDLING METHODS
def handle_submit_button(event,values):
    if event == SUBMIT_BUTTON_EVENT:
        error = False
        either_radio_selected = window.Element(INPUT_KEY_TYPE_STR_EVENT).Get() or window.Element(INPUT_KEY_TYPE_FILE_EVENT).Get() #or window.Element(INPUT_KEY_TYPE_RANDOM_EVENT).Get()
        if either_radio_selected:
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
                if key_path == '':
                    sg.Popup('Please Select a File')
                    error = True
                else:    
                    with open(key_path) as fh:
                        alice_key_f = Key(key_as_str=fh.read())
                    alice.set_key(alice_key_f)
        else:
            sg.Popup('Please Select Key Type')
            error = True
        
        if not error:
            alice.address = (values[INPUT_IP_EVENT],
                                int(values[INPUT_PORT_EVENT]))
            window.Element(START_LISTENING_BUTTON_EVENT).Update(disabled=False)
            alice.console_output('Initial Key Set!')

def handle_key_inputs(event, values):
    if event == INPUT_KEY_TYPE_STR_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=True)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Input the Key')
        window.Element(INPUT_KEY_BOX_EVENT).Update(disabled=False)
    # if event == INPUT_KEY_TYPE_RANDOM_EVENT:
    #     window.Element(INPUT_FILE_EVENT).Update(disabled=True)
    #     window.Element(INPUT_KEY_TEXT_EVENT).Update('Enter Key Length')

    if event == INPUT_KEY_TYPE_FILE_EVENT:
        window.Element(INPUT_FILE_EVENT).Update(disabled=False)
        window.Element(INPUT_KEY_TEXT_EVENT).Update('Browse Key')
        window.Element(INPUT_KEY_BOX_EVENT).Update(disabled=False)

def handle_copy_final_key_to_clipboard(event,values):
    if event == COPY_CLIPBOARD_EVENT:
        clipboard.copy(alice.get_key().__str__())
        if values[OUTPUT_KEY_BOX_EVENT] != '':
            with open(values[OUTPUT_KEY_BOX_EVENT], 'w') as fh:
                fh.write(alice.get_key().__str__())

def handle_reset_button(event,values):
    if event == RESET_BUTTON_EVENT:
        if hasattr(alice, 'ursinaServer'):
            alice.stopServer()
        window.Element(START_LISTENING_BUTTON_EVENT).Update(disabled=True)
        window.Element(CONSOLE_EVENT).Update("Welcome to QKD Server!")

def handle_start_listening_button(event, values):
    if event == START_LISTENING_BUTTON_EVENT:
        alice.start_listening()


while True:
    event, values = window.read()
    
    #Event Conditioning
    if event in (sg.WIN_CLOSED, 'Exit'):
        if hasattr(alice, 'ursinaServer'):
            alice.stopServer()
        break
    
    handle_key_inputs(event,values)
    handle_submit_button(event,values)
    handle_copy_final_key_to_clipboard(event,values)
    handle_reset_button(event,values)
    handle_start_listening_button(event,values)
    
    # Update Time for reconciliation and QBER
    if final_data_to_display:
        if event == RECONCILIATION_TIME_OUTPUT_EVENT:
            window.Element(TEXT_TIME_OUTPUT_EVENT).Update(final_data_to_display['time_reconciliation'])
        if event == QKD_TIME_OUTPUT_EVENT:
            window.Element(TEXT_TIME_OUTPUT_EVENT).Update(final_data_to_display['time_qkd'])



window.close()
