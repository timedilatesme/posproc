import PySimpleGUI as sg

file_type = (
    ('Text Files', '*.txt')
)

layout = [
    [sg.Text('Select Key')],
    [sg.Text(' Browse From File (.txt) \n (Only sifted keys without spaces)'), sg.Input(), sg.FileBrowse()]
]

window = sg.Window('QKD Posproc Server', layout=layout, size=(800,600))

while True:
    event, value = window.read()
    if event in (sg.WIN_CLOSED,'Exit'):
        break

window.close()