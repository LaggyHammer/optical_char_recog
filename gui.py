import PySimpleGUI as sg
from ocr_main import launch_odin
import time
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


Logo = resource_path("Icon\\odin_icon_inverted.png")

# application version: release.improvement.bug_fix
app_version = '1.6.0 (Early Access)'


def ocr_gui():
    sg.ChangeLookAndFeel('Reddit')

    menu_def = [['File', ['Exit', ]],
                ['Help', 'About'], ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Image(Logo),
         sg.Text('Automated OCR for GAs', size=(30, 1), font=("Helvetica", 20))],
        [sg.Text('_' * 80)],
        [sg.Text('Choose Input Folder :', size=(35, 1))],
        [sg.Text('Input Folder', size=(15, 1), auto_size_text=False, justification='right'),
         sg.InputText('Input', key='-INPUT FOLDER-'), sg.FolderBrowse()],

        [sg.Frame(layout=[
            [sg.Checkbox('Create OCR Text File', default=True, key='-TEXT FILE-'),
             sg.Checkbox('Create Searchable PDF', default=False, key='-PDF')]
        ],
            title='Additional Files', title_color='black', relief=sg.RELIEF_SUNKEN)],

        [sg.Frame(layout=[
            [sg.Checkbox('Table Recognition (for Enduron screens only)', default=False, key='-TABLE RECOG-')],
            [sg.Text('Configuration :', size=(35, 1))],
            [sg.Text('Config File', size=(15, 1), auto_size_text=False, justification='right'),
             sg.InputText('config.ini', key='-CONFIG PATH-'), sg.FileBrowse()]
        ],
            title='Advanced Settings', title_color='black', relief=sg.RELIEF_SUNKEN)],

        [sg.Text('_' * 80)],
        [sg.Submit()]

    ]

    form = sg.Window('ODIN ' + app_version, default_element_size=(40, 1), layout=layout,
                     # icon='Icon/odin_icon.ico'
                     )

    while True:
        event, values = form.read()
        # print(event)  # debug

        if event in (None, 'Exit'):
            break

        if event == 'About':
            sg.Popup(
                'ODIN ' + app_version,
                '\N{COPYRIGHT SIGN} Weir EnSci',
                'ODIN extracts data from Engineering Drawings',
                'Visit cloudweir.sharepoint.com/sites/AutomatedOCRReleases for more info',
                'Created & Maintained by Ankit Saxena (Ankit.Saxena@mail.weir)',
                title='About ODIN')

        if event == 'Submit':
            return values


if __name__ == "__main__":
    form_values = ocr_gui()
    # print(form_values)  # debug
    if form_values is not None:
        process_start_time = time.time()

        launch_odin(input_folder=form_values['-INPUT FOLDER-'], config_path=form_values['-CONFIG PATH-'],
                    searchable_pdf=form_values['-PDF'], write_to_file=form_values['-TEXT FILE-'],
                    table_recognition=form_values['-TABLE RECOG-'])

        sg.Popup("\n Total time to run: ""%s seconds" % (time.time() - process_start_time),
                 title="OCR Results Published")
