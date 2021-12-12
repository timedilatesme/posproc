import subprocess
import PySimpleGUI as sg
from posproc import*
import clipboard
import tempfile

from posproc.utils import gui_console_print


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
QKD_TIME_OUTPUT_EVENT = '-qkd_time_output-'  
TEXT_TIME_OUTPUT_EVENT = '-text_time_output-'
FINAL_KEY_LENGTH_OUTPUT = '-final_key_length-'
QBER_OUTPUT_EVENT = '-qber_output-'
FRACTION_OUTPUT_EVENT = '-fraction_output-'
PA_ALGORITHM_EVENT = '-pa_algorithm-'
RECONCILIATION_ALGORITHM_EVENT = '-reconciliation_algorithm-'
ASK_PARITY_BLOCKS_AND_BITS_EVENT = '-ask_parity_blocks_and_bits-'
REALISTIC_EFFICIENCY_EVENT = '-realistic_efficiency-'
UNREALISTIC_EFFICIENCY_EVENT ='-unrealistic_efficiency-'
START_POST_PROCESSING_EVENT = '-start_post_processing-' 




# final data
final_data = None

# tooltips
INITIAL_KEY_TOOLTIP = "Please Choose the Method for providing the sifted Raw Key"


# RADIO ID
INPUT_KEY_RADIO_ID = '-input_key_radio_id-'

#CONSTANTS
LIST_ERROR_CORECTION_ALGOS = ['CASCADE','BICONF','YANETAL']
LIST_PRIVACY_AMPLIFACTION_ALGOS = ['RANDOM','SHA','BLAKE','MD']
BACKEND_EC_ALGO_NAMES = {'CASCADE':'original','BICONF':'biconf','YANETAL':'yanetal'}

# Default QKD Variables (Layout Defaults)
QBER_THRESHOLD = 0.1
FRACTION_FOR_QBER_ESTM = 0.1
FINAL_KEY_SIZE = 256 #bits
EC_ALGORITHM = LIST_ERROR_CORECTION_ALGOS[0]
PA_ALGORITHM = LIST_PRIVACY_AMPLIFACTION_ALGOS[0]


# layouts
initialization_frame_layout = [ [sg.T('Provide the sifted key in binary format')],
                                [sg.Text('Initial Key Type :',justification='r'),
                                sg.Radio(' Input Key', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_STR_EVENT,enable_events=True),
                                sg.Radio('Browse Key:', INPUT_KEY_RADIO_ID, key=INPUT_KEY_TYPE_FILE_EVENT, enable_events=True)],
                                [sg.Text('Input the Key:',  key=INPUT_KEY_TEXT_EVENT,justification='c'),
                                sg.Input(key=INPUT_KEY_BOX_EVENT, justification='c', disabled=True),
                                sg.FileBrowse(disabled=True, key=INPUT_FILE_EVENT)],
                                [sg.Text("Server Address:",justification='l'),sg.Text('IP',justification='c'), sg.Input(constants.LOCAL_IP,key=INPUT_IP_EVENT,size = (15,1),justification='c'),
                                sg.Text('Port',justification='c'), sg.Input(constants.LOCAL_PORT,key=INPUT_PORT_EVENT,size = (8,1),justification='c')]
                            ]
parameter_frame_layout = [  [sg.T('Initialize the required parameters')],
                            [sg.Text("QBER Threshold:",justification='c'),sg.Input(str(QBER_THRESHOLD),key = INPUT_QBER_THRESHOLD_EVENT,justification='c',size = (5,1)),
                            sg.Text("QBER Fraction:",justification='c'),sg.Input(str(FRACTION_FOR_QBER_ESTM),key=INPUT_QBER_FRACTION_EVENT,justification='c',size = (5,1))],
                            [sg.Text("EC Algorithm:", justification='c'),sg.Combo(LIST_ERROR_CORECTION_ALGOS,default_value=EC_ALGORITHM,key = INPUT_ERROR_CORRECTION_ALGORITHM_EVENT,size = (10,1),readonly=True),
                            sg.Text("PA Algorithm:", justification='c'),sg.Combo(LIST_PRIVACY_AMPLIFACTION_ALGOS,default_value=PA_ALGORITHM,key = INPUT_PRIVACY_AMPLIFICATION_ALGORITHM_EVENT,size =(10,1),readonly=True)],
                            [sg.Text("Final Key Size:",justification='c'),sg.Input(str(FINAL_KEY_SIZE),key=INPUT_FINAL_KEY_SIZE_EVENT,justification='c',size = (10,1))],
                            
                        ]

opening_tab_layout = [  [sg.Text('')],
                        [sg.Frame('Key Initialization',initialization_frame_layout,font= 'Arial', title_color='lightblue',element_justification='c'), 
                        sg.Frame('Parameter Initialization ',parameter_frame_layout, font = 'Arial', title_color='lightblue',element_justification='c')],
                        [sg.Text('')],
                        [sg.Button('Submit',key = SUBMIT_BUTTON_EVENT),
                        # sg.Button('Connect',key = START_CONNECTING_BUTTON_EVENT,disabled=True),
                        sg.Button('Connect and Start Post Processing',key = START_POST_PROCESSING_EVENT,disabled = True),
                        sg.Button('Reset', key = RESET_BUTTON_EVENT), sg.Button('Exit',  key=EXIT_BUTTON_EVENT)]
                    ]

QKD_stats_frame_layout = [
                            [sg.Text("Final Key Length:                         ",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=FINAL_KEY_LENGTH_OUTPUT,text_color='black')],
                            [sg.Text("Time for:"), sg.Radio('Reconciliation',group_id=TIME_OUTPUT_EVENT,key = RECONCILIATION_TIME_OUTPUT_EVENT,enable_events=True),
                            sg.Radio('QKD',group_id=TIME_OUTPUT_EVENT,key = QKD_TIME_OUTPUT_EVENT,enable_events=True),sg.InputText('',readonly=True,size=(5,1),justification='r',key=TEXT_TIME_OUTPUT_EVENT,text_color='black')],
                            [sg.Text("QBER:",justification='l'), sg.InputText('',readonly=True,size=(5,1),key= QBER_OUTPUT_EVENT,text_color='black'),sg.Text('         ') ,sg.Text("Fraction Used"), sg.InputText('',readonly=True,size=(5,1),key=FRACTION_OUTPUT_EVENT,text_color='black')],
                            [sg.Text("Algorithm for Privacy Amplification:",justification='l'),sg.InputText('',readonly=True,size=(10,1),key=PA_ALGORITHM_EVENT,text_color='black')],
                        ]

reconciliation_stats_frame_layout = [

                            [sg.Text("Reconciliation Algorithm:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=RECONCILIATION_ALGORITHM_EVENT,text_color='black')],
                            [sg.Text("Parity Blocks Messages & Bits:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key=ASK_PARITY_BLOCKS_AND_BITS_EVENT,text_color='black')],
                            [sg.Text("Unrealistic Efficiency:",justification='l'), sg.InputText('',readonly=True,size=(10,1),justification='r',key = UNREALISTIC_EFFICIENCY_EVENT,text_color='black')],
                            [sg.Text("Realistic Efficiency:",justification='l'),sg.InputText('',readonly=True,size=(10,1),justification='r',key=REALISTIC_EFFICIENCY_EVENT,text_color='black')],
                            ]
                
result_tab_layout = [
                [sg.Text('')],   
                [sg.Frame('QKD Stats',QKD_stats_frame_layout, font= 'Arial', title_color='lightblue',element_justification='r'), 
                 sg.Frame('Reconciliation Stats',reconciliation_stats_frame_layout, font = 'Arial', title_color='lightblue',element_justification='r')],
                [sg.Text('',size=(1,2))],                 
                [sg.Text('Save the Final Key:', justification='c'),
                sg.InputText(key=OUTPUT_KEY_BOX_EVENT, justification='c'),sg.FileSaveAs(),
                sg.Button('Save / Copy to Clipboard', key = COPY_CLIPBOARD_EVENT)],
                [sg.Text('')]

                ]

tabs = [
    [sg.Tab('Parameters', opening_tab_layout, element_justification='c'),
     sg.Tab('Results', result_tab_layout,element_justification='c')],
]

tabgrp = [[sg.TabGroup(tabs,)],
          [sg.Multiline("Welcome to QKD Client!", key=CONSOLE_EVENT, enable_events=True,
                        size=(128, 10), background_color=CONSOLE_BACKGROUND_COLOR,
                        text_color=CONSOLE_TEXT_COLOR, no_scrollbar=True)],
          ]
window = sg.Window("QKD Client",tabgrp)

# TEMPORARY FILE TO STORE PARAMETERS DATA
with tempfile.TemporaryFile(mode='wb',suffix='.txt') as tmpfile:
    parameters_data_path = tmpfile.name

# EVENT HANDLING METHODS
def handle_submit_button(event, values):
    if event == SUBMIT_BUTTON_EVENT:
        final_data_to_pickle = {}
        error = False
        either_radio_selected = window.Element(INPUT_KEY_TYPE_STR_EVENT).Get() or window.Element(
            INPUT_KEY_TYPE_FILE_EVENT).Get()  # or window.Element(INPUT_KEY_TYPE_RANDOM_EVENT).Get()
        if either_radio_selected:
            if window.Element(INPUT_KEY_TYPE_STR_EVENT).get():
                bob_key_str = values[INPUT_KEY_BOX_EVENT]
                if not check_valid_key_box_input(bob_key_str):
                    sg.popup('Please Enter Key in Binary Format')
                    error = True
            elif window.Element(INPUT_KEY_TYPE_FILE_EVENT).get():
                key_path = values[INPUT_KEY_BOX_EVENT]
                if key_path == '':
                    sg.Popup('Please Select a File')
                    error = True
                else:
                    with open(key_path) as fh:
                        bob_key_str = fh.read()
        else:
            sg.Popup('Please Select Key Type')
            error = True
            
        if not error:
            address = (values[INPUT_IP_EVENT],
                           int(values[INPUT_PORT_EVENT]))
        
            qber_threshold = float(values[INPUT_QBER_THRESHOLD_EVENT])
            fraction_for_qber_estm = float(values[INPUT_QBER_FRACTION_EVENT])
            ec_algorithm = values[INPUT_ERROR_CORRECTION_ALGORITHM_EVENT]
            pa_algorithm = values[INPUT_PRIVACY_AMPLIFICATION_ALGORITHM_EVENT]
            final_key_size = int(values[INPUT_FINAL_KEY_SIZE_EVENT])
            
            final_data_to_pickle = {"key_str":bob_key_str, 
                                    "address":address, "qber_threshold":qber_threshold,
                                    "fraction_for_qber_estm":fraction_for_qber_estm,
                                    "ec_algorithm":ec_algorithm,"pa_algorithm":pa_algorithm,
                                    "final_key_size":final_key_size}
            #TODO: make this using temporary files
            utils.dump(final_data_to_pickle, parameters_data_path)
            window.Element(START_POST_PROCESSING_EVENT).Update(disabled=False)
                       
def handle_key_inputs(event):
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

def handle_copy_final_key_to_clipboard(event, values):
    if event == COPY_CLIPBOARD_EVENT:
        clipboard.copy(final_data['final_key'])
        if values[OUTPUT_KEY_BOX_EVENT] != '':
            with open(values[OUTPUT_KEY_BOX_EVENT], 'w') as fh:
                fh.write(final_data['final_key'])


def handle_reset_button(event):
    if event == RESET_BUTTON_EVENT:
        window.Element(CONSOLE_EVENT).Update("Welcome to QKD Client!")
        window.Element(START_POST_PROCESSING_EVENT).Update(disabled=True)
        with open(parameters_data_path,'r+') as fh:
            fh.seek(0)
            fh.truncate()

def handle_post_processing_button(event):
    if event == START_POST_PROCESSING_EVENT:
        client_backend = subprocess.Popen('python client_backend.py ' + parameters_data_path,
                                          stdout=subprocess.PIPE, 
                                          universal_newlines=True, text=True, shell = True)
    
        while True:
            output = client_backend.stdout.readline()
            if output == '' and client_backend.poll() is not None:
                break
            if output.strip():
                utils.gui_console_print(output.strip(), window)
        
        client_backend.wait()
        
        global final_data
        final_data = utils.load(parameters_data_path)
        window.Element(FINAL_KEY_LENGTH_OUTPUT).Update(final_data['final_key_length'])
        #TODO:Radio Button for key type
        #if(RECONCILIATION_TIME_OUTPUT_EVENT):
        #    window.Element(RECONCILIATION_TIME_OUTPUT_EVENT).Update(final_data['time_reconciliation'])
        #elif(QKD_TIME_OUPUT_EVENT):
        #    window.Element(QKD_TIME_OUPUT_EVENT).Update(final_data['time_qkd'])
        window.Element(QBER_OUTPUT_EVENT).Update(final_data['qber'])
        window.Element(FRACTION_OUTPUT_EVENT).Update(final_data['fraction_for_qber'])
        window.Element(PA_ALGORITHM_EVENT).Update(final_data['algorithm_pa'])
        window.Element(RECONCILIATION_ALGORITHM_EVENT).Update(final_data['recon_algo'])
        window.Element(ASK_PARITY_BLOCKS_AND_BITS_EVENT).Update(str(final_data['parity_msgs_bits'][0])+' & '+str(final_data['parity_msgs_bits'][1]))
        window.Element(UNREALISTIC_EFFICIENCY_EVENT).Update("{:.2f}".format(final_data['unrealistic_efficiency']))
        window.Element(REALISTIC_EFFICIENCY_EVENT).Update("{:.2f}".format(final_data['realistic_efficiency']))

        


while True:
    event, values = window.read()
    
    #Event Conditioning
    if event in (sg.WIN_CLOSED, 'Exit'):
        os.remove(parameters_data_path)
        break    
    
    handle_submit_button(event, values)
    handle_key_inputs(event)
    handle_copy_final_key_to_clipboard(event, values)
    handle_post_processing_button(event)
    handle_reset_button(event)
    
    # Update Time for reconciliation and QBER
    if final_data:
        if event == RECONCILIATION_TIME_OUTPUT_EVENT:
            window.Element(TEXT_TIME_OUTPUT_EVENT).Update(final_data['time_reconciliation'])
        if event == QKD_TIME_OUTPUT_EVENT:
            window.Element(TEXT_TIME_OUTPUT_EVENT).Update(final_data['time_qkd'])

window.close()
