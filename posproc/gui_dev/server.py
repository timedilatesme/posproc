import PySimpleGUI as sg
from posproc import*


layout = [
    [sg.Text('Select Key')],
    [sg.Text(' Browse From File (.txt) \n (Only sifted keys without spaces)'), sg.Input(), sg.FileBrowse(key = 'key_original_path'),sg.Submit(key = 'submit_key')],
    [sg.Button('Start',key = 'start_listening')],
    [sg.Text('158',key = 'status')]

]

window = sg.Window('QKD Posproc Server', layout=layout, size=(800,600))

alice = QKDServer('Alice')

while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED,'Exit'):
        break
    if event == 'submit_key':
        key_path = value['key_original_path']
        with open(key_path) as fh:
            alice_key_f = Key(key_as_str=fh.read())
        alice._current_key = alice_key_f
    if event == 'start_listening':
        alice.start_listening()
        to_add = window.Element('status').Get() + f'\nListening @ {alice.address}'
        window.Element('status').Update(to_add)
        

window.close()
