import PySimpleGUI as sg

layout = [[
    sg.InputText(key='File to Save', default_text='filename',
                 enable_events=True),
    sg.InputText(key='Save As', do_not_clear=False,
                 enable_events=True, visible=False),
    sg.FileSaveAs(initial_folder='/tmp')
]]
window = sg.Window('', layout)

while True:
    event, values = window.Read()
    print("event:", event, "values: ", values)
    if event is None or event == 'Exit':
        break
    elif event == 'Save As':
        filename = values['Save As']
        if filename:
            window['File to Save'].update(value=filename)

window.close()
