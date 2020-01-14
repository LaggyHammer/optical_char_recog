import PySimpleGUI as sg
from ocr_main import main
import configparser

# application version: release.improvement.bug_fix
app_version = '1.1.0 (Beta)'


def ocr_gui():
    sg.ChangeLookAndFeel('Reddit')

    form = sg.Window('Engineering Drawings OCR', default_element_size=(40, 1))

    layout = [
        [sg.Text('Automated OCR for GAs', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('_' * 80)],
        [sg.Text('Choose Input Folder :', size=(35, 1))],
        [sg.Text('Input Folder', size=(15, 1), auto_size_text=False, justification='right'),
         sg.InputText('Input'), sg.FolderBrowse()],
        [sg.Frame(layout=[
            [sg.Checkbox('Total Mass', default=True),
             sg.Checkbox('Static Loads', default=True),
             sg.Checkbox('Spring Constant', default=True),
             sg.Checkbox('Operating Speed', default=True),
             sg.Checkbox('Dynamic Loads', default=True)]
        ],
            title='Search Keywords', title_color='black', relief=sg.RELIEF_SUNKEN)],
        [sg.Frame(layout=[
            [sg.Checkbox('Create OCR Text File', default=True), sg.Checkbox('Create Searchable PDF', default=False)]
        ],
            title='Additional Files', title_color='black', relief=sg.RELIEF_SUNKEN)],
        [sg.Frame(layout=[
            [sg.Text('Configuration :', size=(35, 1))],
            [sg.Text('Config File', size=(15, 1), auto_size_text=False, justification='right'),
             sg.InputText('config.ini'), sg.FileBrowse()]
        ],
            title='Advanced Settings', title_color='black', relief=sg.RELIEF_SUNKEN)],
        [sg.Text('_' * 80)],
        [sg.Submit()],
        [sg.Text('App Version ' + app_version, font=("Helvetica", 10)),
         sg.Text('Created & Maintained by Ankit Saxena')]

    ]

    button, values = form.layout(layout).Read()
    # print(values) # debug
    return values


# config file reader
def config_reader(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    settings = config['settings']

    return settings


def launch_ocr(input_values):
    if input_values[0] is not None:
        input_path = input_values[0]
        search_list = [input_values[1], input_values[2], input_values[3], input_values[4], input_values[5]]
        write_to_file = input_values[6]
        searchable_pdf = input_values[7]

        # reading config file
        settings = config_reader(input_values[10])
        print(settings)

        ocr_engine = settings['ocr path']
        orientation_threshold = float(settings['orientation threshold'])/100
        script_threshold = float(settings['script threshold'])/100

        main(input_folder=input_path, write_to_file=write_to_file, searchable_pdf=searchable_pdf,
             orientation_threshold=orientation_threshold, script_threshold=script_threshold, ocr_engine=ocr_engine,
             search_list=search_list)


if __name__ == "__main__":
    form_input_values = ocr_gui()
    print(form_input_values)
    launch_ocr(form_input_values)
