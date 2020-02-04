import configparser
import PySimpleGUI as sg
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


Logo = resource_path("odin_icon_inverted.png")


def config_gui():
    sg.ChangeLookAndFeel('Reddit')

    column1 = [[sg.Text('Orientation Threshold: ', text_color='#000000', background_color='#ffffff',
                        justification='left', size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
    column2 = [[sg.Text('Script Threshold: ', text_color='#000000', background_color='#ffffff', justification='left',
                        size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
    layout = [
        [sg.Image(Logo),
         sg.Text('Automated GA OCR Configurator', size=(30, 1), font=("Helvetica", 14))],
        [sg.Text('_' * 80)],
        [sg.Text('Choose OCR Engine :', size=(35, 1))],
        [sg.Text('OCR Engine', size=(15, 1), auto_size_text=False, justification='right'),
         sg.InputText(r"C:\Program Files\Tesseract-OCR\tesseract.exe"), sg.FileBrowse()],
        [sg.Frame(layout=[
            [sg.Column(column1, background_color='#ffffff'), sg.Column(column2, background_color='#ffffff')],
        ],
            title='Advanced Settings', title_color='black', relief=sg.RELIEF_RIDGE)],
        [sg.Button('Add Custom Keyword(s)', key='Add Keyword')],
        [sg.Text('Keywords Added:'), sg.Text(size=(60, 5), key='KEY-LIST')],
        [sg.Text(size=(15, 1), key='-OUTPUT-')],
        [sg.Text('_' * 80)],
        [sg.Submit()],
        [sg.Text('Created & Maintained by Ankit Saxena')]

    ]

    window = sg.Window('OCR Configurator', layout
                       # , icon='Icon/odin_icon.ico'
                       )

    # keyword_dict = {'OPERATING SPEED': {'Alternate(s)': [], 'Unit(s)': 'rpm or equivalent', 'Occurrence(s)': '1'},
    #                 'TOTAL MASS OF': {'Alternate(s)': ['TOTAL LOAD OF'], 'Unit(s)': 'kg', 'Occurrence(s)': '1'},
    #                 'SPRING CONSTANT': {'Alternate(s)': ['BUFFER CONSTANT'], 'Unit(s)': 'kg/mm', 'Occurrence(s)': '1'},
    #                 'STATIC LOAD PER SUPPORT POINT': {'Alternate(s)': [], 'Unit(s)': 'kg', 'Occurrence(s)': '2'}
    #                 }
    keyword_dict = {'example keyword': {'Alternate(s)': ['put alternative', 'keywords', 'in a list', 'like this'],
                                        'Unit(s)': 'kg',
                                        'Occurrence(s)': '4'}}

    while True:
        event, values = window.read()
        # print(event, values)
        if event in (None, 'Submit'):
            break
        if event == 'Add Keyword':
            add_layout = [
                [sg.Text('Add Keyword (Equivalent keywords separated by commas)')],
                [sg.Text('Keyword', size=(15, 1)), sg.InputText(key='KEYWORD')],
                [sg.Text('Unit(s)', size=(15, 1)),
                 sg.InputOptionMenu(('kg', 'kg/mm', 'rpm or equivalent'), size=(20, 1), key='UNIT')],
                [sg.Text('No. of Occurrences up to'),
                 sg.InputOptionMenu(list(range(1, 11)), size=(20, 1), key='NUMBER')],
                [sg.Button('Add', key='ADD'), sg.Button('Done', key='DONE')],
                [sg.Text('Keywords Added:'), sg.Text(size=(60, 1), key='ADDED-KEY-LIST')]
            ]

            add_window = sg.Window('Add Keyword', add_layout)

            while True:
                add_event, add_values = add_window.read()
                if add_event in (None, 'DONE'):
                    break
                if add_event == 'ADD':
                    if bool(add_values['KEYWORD'].strip()):
                        key_break = [x.strip() for x in add_values['KEYWORD'].split(',')]
                        keyword_dict[key_break[0]] = {'Alternate(s)': key_break[1:],
                                                      'Unit(s)': add_values['UNIT'],
                                                      'Occurrence(s)': add_values['NUMBER']}
                    add_window['KEYWORD'].update('')
                    add_window['UNIT'].update('')
                    add_window['NUMBER'].update('')
                    add_window['ADDED-KEY-LIST'].update(list(keyword_dict.keys()))
            add_window.close()

        window['KEY-LIST'].update(list(keyword_dict.keys()))

    window.close()

    # print(keyword_dict)

    return values, keyword_dict


def config_writer(input_values, custom_keywords):
    if input_values is not None:
        if input_values[1] is not None:
            config = configparser.ConfigParser(allow_no_value=True)

            config.add_section('INSTRUCTIONS')
            config.set('INSTRUCTIONS', '# This is a dummy config file\n'
                                       '# Add Keywords by running config.exe or by entering manually\n'
                                       '# A dummy format is given below\n'
                                       '# Choose from Available Units only (given below):\n'
                                       '# 1. kg 2. kg/mm 3. rpm or equivalent\n'
                                       '# Delete the dummy format after adding keywords\n'

                       )

            config['settings'] = {'ocr path': input_values[1],
                                  'orientation threshold': input_values[2],
                                  'script threshold': input_values[3]}

            config['custom keywords'] = custom_keywords

            with open('config.ini', 'w') as configfile:
                config.write(configfile)


if __name__ == "__main__":
    form_input_values, custom_keywords = config_gui()
    config_writer(form_input_values, custom_keywords)
