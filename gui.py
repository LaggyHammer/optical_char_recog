import PySimpleGUI as sg
from ocr_main import main

sg.ChangeLookAndFeel('Black')

form = sg.FlexForm('GUI Testing', default_element_size=(40, 1))

column1 = [[sg.Text('Orientation Threshold: ', text_color='#000000', background_color='#ffffff', justification='left', size=(20, 1))],
           [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
column2 = [[sg.Text('Script Threshold: ', text_color='#000000', background_color='#ffffff', justification='left', size=(20, 1))],
           [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
layout = [
    [sg.Text('Screen GA OCR Form', size=(30, 1), font=("Helvetica", 25))],
    [sg.Text('_' * 80)],
    [sg.Text('Choose Input Folder', size=(35, 1))],
    [sg.Text('Input Folder', size=(15, 1), auto_size_text=False, justification='right'),
     sg.InputText('Default Folder'), sg.FolderBrowse()],
    [sg.Text('Additional Files: ')],
    [sg.Checkbox('Create OCR Text File', default=True), sg.Checkbox('Create Searchable PDF', default=False)],
    [sg.Text('_' * 80)],
    [sg.Text('Advanced Settings: ')],
    [sg.Column(column1, background_color='#ffffff'), sg.Column(column2, background_color='#ffffff')],
    [sg.Text('_' * 80)],
    [sg.Submit()]
]

button, values = form.layout(layout).Read()
# sg.Popup(button, values)
print(values)

if values[0] is not None:
    input_path = values[0]
    write_to_file = values[1]
    searchable_pdf = values[2]
    orientation_threshold = values[3]
    script_threshold = values[4]

    main(input_folder=input_path, write_to_file=write_to_file, searchable_pdf=searchable_pdf,
         orientation_threshold=orientation_threshold, script_threshold=script_threshold)
