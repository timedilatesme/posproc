from ctypes import alignment
import PySimpleGUI as sg

layout = [
    [sg.Text('This is a Text Element', )],
]

window = sg.Window('Window Title', layout, size=(400, 400),element_justification = 'down')

event, values = window.read()
