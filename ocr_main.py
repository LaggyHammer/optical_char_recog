import pytesseract as tesseract
from pdf2image import convert_from_bytes
import pandas as pd
from pandas import ExcelWriter
from search_functions import *
import os
import time
import PySimpleGUI as sg
import numpy as np

# Tracking Time
start_time = time.time()

# Tesseract OCR File Path
tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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
def image_ocr(image_dict, write_to_file, searchable_pdf):
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
        req_info['Total Mass'] = find_total_mass(text)
        req_info['Static Load'] = find_static_load(text)
        req_info['Spring Constant'] = find_spring_constant(text)
        req_info['Operating Speed'] = find_operating_speed(text)
        req_info['Dynamic Loads'] = find_dynamic_loads(text)

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
                dict_ocr[filename].append(np.nan)

        # Attributes list
        rows = ['Total Mass', 'Static Loads', ' ', 'Spring Constant', 'Operating Speed', 'Dynamic Loads']
        while max_len > len(rows):
            rows.append(' ')

        # Output data frame
        df = pd.DataFrame()

        df['Attributes'] = rows
        for filename in list(dict_ocr.keys()):
            df[filename.split('/')[-1]] = dict_ocr[filename]

        df.to_excel(writer)

    print("\n Output Successful")


# Main Execution Function (Call this!)
def main(input_folder='Input', write_to_file=False, searchable_pdf=False, orientation_threshold=0.5,
         script_threshold=0.5):
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
    info_list = image_ocr(oriented_images_dict, write_to_file, searchable_pdf)
    ocr_time = time.time()
    print("Passed " + str(len(info_list)) + " files through OCR in ""%s seconds" % (ocr_time - orient_time))

    print("\n (Step 5 of 5) Publishing Results to Excel...")
    dict_to_excel(info_list)
    result_time = time.time()
    print("Published results in ""%s seconds" % (result_time - ocr_time))

    sg.Popup("\n Total time to run: ""%s seconds" % (time.time() - start_time), title="OCR Results Published")


if __name__ == "__main__":
    main(write_to_file=False, searchable_pdf=False)
    print("\n Total time to run: ""%s seconds" % (time.time() - start_time))
