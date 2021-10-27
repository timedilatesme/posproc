import PySimpleGUI as sg
from posproc import*

layout = [
    [sg.Text('Select Key')],
    [sg.Text(' Browse From File (.txt) \n (Only sifted keys without spaces)'), sg.Input(
    ), sg.FileBrowse(key='key_original_path'), sg.Submit(key='submit_key')],
    [sg.Button('Start', key='start_listening')]

]

window = sg.Window('QKD Posproc Server', layout=layout, size=(800, 600))

bob = QKDClient('Bob')

while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'submit_key':
        key_path = value['key_original_path']
        with open(key_path) as fh:
            bob_key_f = Key(key_as_str=fh.read())
        bob._current_key = bob_key_f
    if event == 'start_listening':
        bob.start_listening()

window.close()
