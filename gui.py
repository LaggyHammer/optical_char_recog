import PySimpleGUI as sg
from ocr_main import main

sg.ChangeLookAndFeel('Dark Blue 3')

form = sg.FlexForm('Engineering Drawings OCR', default_element_size=(40, 1))

column1 = [[sg.Text('Orientation Threshold: ', text_color='#000000', background_color='#ffffff', justification='left', size=(20, 1))],
           [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
column2 = [[sg.Text('Script Threshold: ', text_color='#000000', background_color='#ffffff', justification='left', size=(20, 1))],
           [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
layout = [
    [sg.Text('Automated OCR for GAs', size=(30, 1), font=("Helvetica", 25))],
    [sg.Text('_' * 80)],
    [sg.Text('Choose Input Folder', size=(35, 1))],
    [sg.Text('Input Folder', size=(15, 1), auto_size_text=False, justification='right'),
     sg.InputText('Default Folder'), sg.FolderBrowse()],
    [sg.Frame(layout=[
        [sg.Checkbox('Create OCR Text File', default=True), sg.Checkbox('Create Searchable PDF', default=False)]
        ],
        title='Additional Files', title_color='white', relief=sg.RELIEF_SUNKEN)],
    [sg.Frame(layout=[
        [sg.Column(column1, background_color='#ffffff'), sg.Column(column2, background_color='#ffffff')]
        ],
        title='Advanced Settings', title_color='white', relief=sg.RELIEF_RIDGE)],
    [sg.Text('_' * 80)],
    [sg.Submit()]
]

button, values = form.layout(layout).Read()
print(values)

if __name__ == "__main__":
    if values[0] is not None:
        input_path = values[0]
        write_to_file = values[1]
        searchable_pdf = values[2]
        orientation_threshold = values[3]/100
        script_threshold = values[4]/100

        main(input_folder=input_path, write_to_file=write_to_file, searchable_pdf=searchable_pdf,
             orientation_threshold=orientation_threshold, script_threshold=script_threshold)
