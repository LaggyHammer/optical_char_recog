import pytesseract as tesseract
from pdf2image import convert_from_bytes
import pandas as pd
from pandas import ExcelWriter
import os
import time
import PySimpleGUI as sg
from fuzzysearch import find_near_matches
import itertools
import re
import configparser


# Search Functions

# Static Load Function
def find_static_load(text, key='STATIC LOAD PER SUPPORT POINT'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match.start
        search_string = text[search_start:]
        for m in itertools.islice(
                re.finditer("p.{0,2}s{0,1}\s{0,1}=\s{0,1}\d{1,5}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)",
                            search_string), 2):
            # Regex: 'p + 0-2 characters + s (maybe) + space (maybe) + = + 1-5 digits + . or , (maybe) + 0-3 digits or
            # 'o's + space (maybe) + k + g or o
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    if not bool(results):
        results = [' ', ' ']
    # print(results) # debug
    return results


# Spring Constant Function
def find_spring_constant(text, key='SPRING CONSTANT OF'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match.start
        search_string = text[search_start:]
        for m in itertools.islice(re.finditer("\d{0,3}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)\/mm", search_string), 1):
            # Regex: 0-3 digits + . or , (maybe) + 0-3 digits or 'o's + space (maybe) + k + g or o + /mm
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    if not bool(results):
        results = [' ']
    return results


# Operating Speed Function
def find_operating_speed(text, key='OPERATING SPEED'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match.start
        search_string = text[search_start:]
        for m in itertools.islice(
                re.finditer("\d{1,5}\s{0,1}(r.{0,1}\s{0,1}p.{0,1}\s{0,1}m.{0,1}|r\s{0,1}\/\s{0,1}min){0,1}",
                            search_string),
                1):
            # Regex: 1-5 digits + space (maybe) + (rpm or r.p.m. or r/min)
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    if not bool(results):
        results = [' ']
    return results


# Total Mass Function
def find_total_mass(text, key='TOTAL MASS OF'):
    results = []
    key = key.lower()
    match_list = find_near_matches(key, text, max_l_dist=2)
    for match in match_list:
        search_start = match.start
        search_string = text[search_start:]
        for m in itertools.islice(re.finditer("\d{1,5}\s{0,1}k(g|o|9)", search_string), 1):
            # Regex: 1-5 digits + space (maybe) + k + g or o
            result = m.string[m.start():m.end()]
            # print(result)
            results.append(result)

        if bool(results):
            break

    if not bool(results):
        results = [' ']
    return results


# Dynamic Loads Function
def find_dynamic_loads(text, key='DYNAMIC'):
    # results = []
    # key = key.lower()
    # match_list = find_near_matches(key, text, max_l_dist=2)
    # print(match_list)
    # text = text[match_list[0][0]:]
    # match_list = find_near_matches(key, text, max_l_dist=2)
    # print(match_list)
    # for match in match_list:
    #     search_start = match[0]
    #     search_string = text[search_start:]
    #     next_field_pos = search_string.find('spring')
    #     search_string = search_string[: next_field_pos]
    #     for m in itertools.islice(re.finditer("\d{0,5}(\.|,){0,1}(\d|o){0,3}\s{0,1}k(g|o|9)", search_string), 10):
    #         # Regex: 0-5 digits + . or , (maybe) + 0-3 digits or 'o's + space (maybe) + k + g or o
    #         result = m.string[m.start():m.end()]
    #         # print(result)
    #         results.append(result)
    #
    #     if bool(results):
    #         break
    #
    #     results = [' ']
    # print(results)
    results = [' ']
    return results


# Remove formatting
def formatting(result_list):
    results = []
    for value in result_list:
        if value != ' ':
            for m in itertools.islice(re.finditer("\d{1,7}[^a-np-z\s](\.|,){0,1}(\d|o){0,3}", value), 1):
                # Regex: 1-5 digits with decimal
                result = m.string[m.start():m.end()]
                # print(result)
                results.append(result)
        else:
            results.append(value)

    return results


# OCR Main

# Tesseract OCR File Path
def tess_path(path):
    tesseract.pytesseract.tesseract_cmd = path


# Read File Names from Folder
def read_file_names(folder_name='Input'):
    filename_list = os.listdir(folder_name)
    filename_list = [folder_name + '/' + file for file in filename_list]

    return filename_list


# PDF to Image Function
def pdf_to_image(file_list):
    file_dict = {}

    # Progress Bar Window
    layout = [[sg.Text('Converting PDF to Image')],
              [sg.ProgressBar(len(file_list), orientation='h', size=(20, 2), key='progressbar')],
              [sg.Cancel()]]
    window = sg.Window('Progress', layout)
    progress_bar = window['progressbar']
    i = 1

    for filename in file_list:

        # window interaction
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        if i == 1:
            progress_bar.UpdateBar(0)

        # print("Converting " + filename + " to image..") # debug
        images = convert_from_bytes(open(filename, 'rb').read())  # Image Conversion
        file_dict[filename] = images

        # progress bar increment
        progress_bar.UpdateBar(i)
        i += 1

    window.close()
    print("\n Conversion Successful")

    return file_dict


# Orientation Handling
def orient_image(image_dict, orientation_threshold=0.5, script_threshold=0.5):
    oriented_images = {}

    # Progress Bar Window
    layout = [[sg.Text('Orienting Images')],
              [sg.ProgressBar(len(image_dict), orientation='h', size=(20, 2), key='progressbar')],
              [sg.Cancel()]]
    window = sg.Window('Progress', layout)
    progress_bar = window['progressbar']
    i = 1

    for filename in image_dict.keys():

        # window interaction
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        if i == 1:
            progress_bar.UpdateBar(0)

        for img in image_dict[filename]:
            # print("Handling Orientation for image " + filename + "...") # debug
            # img.show()  # debug

            # Aspect Ratio Check
            (width, height) = img.size
            if height > width:
                img = img.rotate(90, expand=True)
                info = tesseract.image_to_osd(img)  # Orientation Info

            else:
                info = tesseract.image_to_osd(img)  # Orientation Info

            # print(info)  # debug
            info = info.split('\n')
            # img.show()  # debug

            # Rotation Angle (0 or 180)
            rotation_angle = info[1]
            key = 'Orientation in degrees: '
            rotation_angle = rotation_angle[rotation_angle.index(key) + len(key):]
            rotation_angle = int(rotation_angle)  # Angle to rotate by

            if rotation_angle == 180:
                orientation_confidence = info[3]
                key = 'Orientation confidence: '
                orientation_confidence = orientation_confidence[orientation_confidence.index(key) + len(key):]
                orientation_confidence = float(orientation_confidence)

                script_confidence = info[5]
                key = 'Script confidence: '
                script_confidence = script_confidence[script_confidence.index(key) + len(key):]
                script_confidence = float(script_confidence)

                if script_confidence > script_threshold and orientation_confidence > orientation_threshold:
                    img = img.rotate(rotation_angle, expand=True)

            # img.show()  # debug
            oriented_images[filename] = img

        # progress bar increment
        progress_bar.UpdateBar(i)
        i += 1

    window.close()

    if oriented_images:
        print("\n Orientation Handling Successful")

    return oriented_images


# Image to Text (Main OCR)
def image_ocr(image_dict, write_to_file, searchable_pdf, search_list):
    req_info_dict = {}

    layout = [[sg.Text('Recognizing Text')],
              [sg.ProgressBar(len(image_dict), orientation='h', size=(20, 2), key='progressbar')],
              [sg.Cancel()]]
    window = sg.Window('Progress', layout)
    progress_bar = window['progressbar']
    i = 1

    for filename in image_dict.keys():

        # window interaction
        event, values = window.read(timeout=10)
        if event == 'Cancel' or event is None:
            break
        if i == 1:
            progress_bar.UpdateBar(0)

        img = image_dict[filename]
        # print("Recognizing Text in " + filename + "...") # debug
        text = tesseract.image_to_string(img, config=r'--psm 6')
        # print("Text from Image") # debug
        # print(text.lower()) # debug

        if write_to_file:
            # print("Writing Text to file...") # debug
            output_folder = 'Output'
            text_file = open(output_folder + '/' + filename.split('.')[0].split('/')[-1] + "_ocr.txt", "w")
            n = text_file.write(text)
            text_file.close()

        # Image to searchable PDF
        if searchable_pdf:
            # print("Writing Searchable PDF...") # debug
            output_folder = 'Output'
            pdf = tesseract.image_to_pdf_or_hocr(img, extension='pdf')
            f = open(output_folder + '/' + filename.split('.')[0].split('/')[-1] + ".pdf", "w+b")
            f.write(bytearray(pdf))
            f.close()

        req_info = {}
        # print("Looking for keywords...") # debug
        text = text.lower()
        if search_list[0]:
            req_info['Total Mass (kg)'] = find_total_mass(text)
            req_info['Total Mass (kg)'] = formatting(req_info['Total Mass (kg)'])

        if search_list[1]:
            req_info['Static Load (kg)'] = find_static_load(text)
            req_info['Static Load (kg)'] = formatting(req_info['Static Load (kg)'])

        if search_list[2]:
            req_info['Spring Constant (kg/mm)'] = find_spring_constant(text)
            req_info['Spring Constant (kg/mm)'] = formatting(req_info['Spring Constant (kg/mm)'])

        if search_list[3]:
            req_info['Operating Speed (rpm)'] = find_operating_speed(text)
            req_info['Operating Speed (rpm)'] = formatting(req_info['Operating Speed (rpm)'])

        if search_list[4]:
            req_info['Dynamic Loads (kg)'] = find_dynamic_loads(text)
            req_info['Dynamic Loads (kg)'] = formatting(req_info['Dynamic Loads (kg)'])

        req_info_dict[filename] = req_info
        # print("Done") # debug

        # progress bar increment
        progress_bar.UpdateBar(i)
        i += 1

    window.close()

    # print(req_info_dict) # debug
    print("\n OCR Successful")

    return req_info_dict


# Writing Output to Excel
def dict_to_excel(ocr_info_dict):
    with ExcelWriter('Output/ocr_output.xlsx') as writer:

        # print(ocr_info_dict) # debug

        # Getting all attribute values in a list
        dict_ocr = {}
        for filename in list(ocr_info_dict.keys()):
            values_list = []
            for value in list(ocr_info_dict[filename].values()):
                values_list = values_list + value
            dict_ocr[filename] = values_list

        # Finding out the max length of output columns
        max_len = 7
        for filename in list(dict_ocr.keys()):
            if max_len < len(dict_ocr[filename]):
                max_len = len(dict_ocr[filename])
                # print(filename) # debug
                # print(max_len) # debug

        # Making every list the same length
        for filename in list(dict_ocr.keys()):
            while max_len > len(dict_ocr[filename]):
                dict_ocr[filename].append(' ')

        # Attributes list
        attribute_list = list(list(ocr_info_dict.values())[0].keys())
        if 'Static Load (kg)' in attribute_list:
            attribute_list.insert(attribute_list.index('Static Load (kg)') + 1, ' ')

        # rows = ['Total Mass', 'Static Loads', ' ', 'Spring Constant', 'Operating Speed', 'Dynamic Loads']
        while max_len > len(attribute_list):
            attribute_list.append(' ')

        # Output data frame
        df = pd.DataFrame()

        df['Attributes'] = attribute_list
        for filename in list(dict_ocr.keys()):
            df[filename.split('/')[-1]] = dict_ocr[filename]

        df.to_excel(writer)

    print("\n Output Successful")


# Main Execution Function (Call this!)
def main(input_folder='Input', write_to_file=False, searchable_pdf=False, orientation_threshold=0.5,
         script_threshold=0.5, ocr_engine=r"C:\Program Files\Tesseract-OCR\tesseract.exe", search_list=[True] * 5):
    tess_path(ocr_engine)
    # Tracking Time
    start_time = time.time()

    print("\n (Step 1 of 5) Reading Files...")
    file_list = read_file_names(input_folder)
    read_time = time.time()
    print("Read " + str(len(file_list)) + " files in ""%s seconds" % (read_time - start_time))

    print("\n (Step 2 of 5) Converting to Image...")
    converted_images_dict = pdf_to_image(file_list)
    convert_time = time.time()
    print("Converted " + str(len(converted_images_dict)) + " files in ""%s seconds" % (convert_time - read_time))

    print("\n (Step 3 of 5) Orienting Images...")
    oriented_images_dict = orient_image(converted_images_dict, orientation_threshold, script_threshold)
    orient_time = time.time()
    print("Oriented " + str(len(oriented_images_dict)) + " images in ""%s seconds" % (orient_time - convert_time))

    print("\n (Step 4 of 5) Commencing OCR...")
    info_list = image_ocr(oriented_images_dict, write_to_file, searchable_pdf, search_list)
    ocr_time = time.time()
    print("Passed " + str(len(info_list)) + " files through OCR in ""%s seconds" % (ocr_time - orient_time))

    print("\n (Step 5 of 5) Publishing Results to Excel...")
    dict_to_excel(info_list)
    result_time = time.time()
    print("Published results in ""%s seconds" % (result_time - ocr_time))

    sg.Popup("\n Total time to run: ""%s seconds" % (time.time() - start_time), title="OCR Results Published")


# GUI

# application version: release.improvement.bug_fix
app_version = '1.0.0 (Early Access)'


def ocr_gui():
    sg.ChangeLookAndFeel('Reddit')

    form = sg.FlexForm('Engineering Drawings OCR', default_element_size=(40, 1))

    column1 = [[sg.Text('Orientation Threshold: ', text_color='#000000', background_color='#ffffff',
                        justification='left', size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
    column2 = [[sg.Text('Script Threshold: ', text_color='#000000', background_color='#ffffff', justification='left',
                        size=(20, 1))],
               [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=50)]]
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
            [sg.Column(column1, background_color='#ffffff'), sg.Column(column2, background_color='#ffffff')],
            [sg.Text('Configuration :', size=(35, 1))],
            [sg.Text('Config File', size=(15, 1), auto_size_text=False, justification='right'),
             sg.InputText('config.ini'), sg.FileBrowse()]
        ],
            title='Advanced Settings', title_color='black', relief=sg.RELIEF_RIDGE)],
        [sg.Text('_' * 80)],
        [sg.Submit()],
        [sg.Text('App Version ' + app_version, font=("Helvetica", 10)),
         sg.Text('\N{COPYRIGHT SIGN} Weir EnSci')],
        [sg.Text('Created & Maintained by Ankit Saxena')]

    ]

    button, values = form.layout(layout).Read()
    # print(values) # debug
    return values


# config file reader
def config_reader(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    ocr_path = config['settings']['ocr path']

    return ocr_path


def launch_ocr(input_values):
    if input_values[0] is not None:
        input_path = input_values[0]
        search_list = [input_values[1], input_values[2], input_values[3], input_values[4], input_values[5]]
        write_to_file = input_values[6]
        searchable_pdf = input_values[7]
        orientation_threshold = input_values[8] / 100
        script_threshold = input_values[9] / 100

        # reading config file
        ocr_engine = config_reader(input_values[10])
        print(ocr_engine)

        main(input_folder=input_path, write_to_file=write_to_file, searchable_pdf=searchable_pdf,
             orientation_threshold=orientation_threshold, script_threshold=script_threshold, ocr_engine=ocr_engine,
             search_list=search_list)


if __name__ == "__main__":
    form_input_values = ocr_gui()
    print(form_input_values)
    launch_ocr(form_input_values)
