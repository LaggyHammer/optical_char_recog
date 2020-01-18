import configparser
import PySimpleGUI as sg


def ocr_gui():
    sg.ChangeLookAndFeel('Reddit')

    form = sg.FlexForm('OCR Configurator', default_element_size=(40, 1))

    column1 = [[sg.Text('Orientation Threshold: ', text_color='#000000', background_color='#ffffff',
                        justification='left', size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
    column2 = [[sg.Text('Script Threshold: ', text_color='#000000', background_color='#ffffff', justification='left',
                        size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
    layout = [
        [sg.Text('Automated GA OCR Configurator', size=(30, 1), font=("Helvetica", 14))],
        [sg.Text('_' * 80)],
        [sg.Text('Choose OCR Engine :', size=(35, 1))],
        [sg.Text('OCR Engine', size=(15, 1), auto_size_text=False, justification='right'),
         sg.InputText(r"C:\Program Files\Tesseract-OCR\tesseract.exe"), sg.FileBrowse()],
        [sg.Text('_' * 80)],
        [sg.Submit()],
        [sg.Text('\N{COPYRIGHT SIGN} Weir EnSci')],
        [sg.Text('Created & Maintained by Ankit Saxena')]

    ]

    button, values = form.layout(layout).Read()
    # print(values) # debug
    return values


def config_writer(input_values):

    if input_values[0] is not None:
        config = configparser.ConfigParser()

        config['DEFAULT'] = {'ocr path': input_values[0]}

        config['settings'] = {}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    form_input_values = ocr_gui()
    config_writer(form_input_values)

