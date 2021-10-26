import PySimpleGUI as sg

# sg.preview_all_look_and_feel_themes()
sg.theme('Default')

layout = [
    [sg.Text('Hello World')],
    # [sg.Radio('Radio Num 1', 'RADIO1', default=True),
    #  sg.Radio('Radio Num 2', 'RADIO1')]
    [sg.Text('Select the Location of the file!'),sg.FileBrowse(key = '-IN-'),sg.Button('submit',key='-SUBMIT-')],
    [sg.Checkbox('List 1')],
    [sg.InputText(default_text='Enter Something', do_not_clear=False)]
]

window = sg.Window(title="blahhh", layout=layout, size = (600,400))

# values = {key : value}

while True:
    event, values = window.read()
    if event == '-SUBMIT-':
        print(values["-IN-"])
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    
window.close()