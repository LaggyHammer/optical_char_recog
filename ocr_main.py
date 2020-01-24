import pytesseract as tesseract
from pdf2image import convert_from_bytes
import pandas as pd
from pandas import ExcelWriter
from search_functions import *
import os
import time
import PySimpleGUI as sg
import configparser
from ast import literal_eval
import logging

# Logging Setup
logging.basicConfig(filename='ocr_log.log', level=logging.DEBUG, filemode='w+')


# Tesseract OCR File Path
def tess_path(path):
    tesseract.pytesseract.tesseract_cmd = path


# Read File Names from Folder
def read_file_names(folder_name='Input'):
    filename_list = os.listdir(folder_name)
    filename_list = [folder_name + '/' + file for file in filename_list]

    return filename_list


# PDF to Image Function
def pdf_to_image(filename):
    image = convert_from_bytes(open(filename, 'rb').read())

    return image


# Orientation Handling
def orient_image(img, orientation_threshold=0.5, script_threshold=0.5):
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

    return img


# Table Cropping
def crop_table(img, filename):
    # img.show()  # debug
    start_time = time.time()
    position_map = tesseract.image_to_pdf_or_hocr(img, extension='hocr')
    end_time = time.time()
    logging.info("HOCR in ""%s seconds" % (end_time - start_time))
    # print(position_map)

    # write to file
    # f = open(filename + '.html', 'wb')
    # f.write(position_map)
    # f.close()

    position_map = position_map.decode("utf-8")
    # print(position_map)  # debug

    total_position = position_map.find('TOTAL')
    # print('total position')  # debug
    # print(total_position)  # debug
    total_coords = position_map[total_position - 50: total_position]
    # print(total_coords)  # debug
    total_coords = re.search("\d{1,5}\s\d{1,5}\s\d{1,5}\s\d{1,5}", total_coords)
    # print(total_coords)  # debug

    if total_coords is None:
        logging.info("Possible incorrect orientation for " + filename)
        return img

    total_coords = total_coords.group(0).split(' ')
    total_x = int(total_coords[0])
    # print(total_x)  # debug
    total_y = int(total_coords[1])
    # print(total_y)  # debug

    keep_position = position_map.find('KEEP')
    # print('keep position')  # debug
    # print(keep_position)  # debug
    keep_coords = position_map[keep_position - 50: keep_position]
    # print(keep_coords)  # debug
    keep_coords = re.search("\d{1,5}\s\d{1,5}\s\d{1,5}\s\d{1,5}", keep_coords)
    # print(keep_coords)  # debug

    # keep_coords = keep_coords.group(0).split(' ')
    # keep_x = int(keep_coords[0])
    # keep_y = int(keep_coords[3])
    # print(keep_y)

    width, height = img.size
    # print(width, height)  # debug
    # print(total_x - 5, total_y - 5, width, keep_y)
    cropped_img = img.crop((total_x - 5, total_y - 5, width, height))
    # cropped_img.show()  # debug
    # cropped_img.save(filename + '.jpg')

    return cropped_img


# Image to Text (Main OCR)
def image_ocr(img, filename, write_to_file, searchable_pdf, search_dict):
    logging.info("Recognizing Text in " + filename + "...")  # debug
    start_time = time.time()
    text = tesseract.image_to_string(img,
                                     config=r'--psm 6'
                                     )
    end_time = time.time()
    logging.info("String in ""%s seconds" % (end_time - start_time))
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

    # print("Looking for keywords...") # debug
    text = text.lower()

    results_dict = {}
    for keyword in search_dict.keys():
        results_dict[keyword + ' (' + search_dict[keyword]['Unit(s)'] + ')'] = search_function(text, keyword,
                                                                                               search_dict[keyword])
        # print(results_dict)  # debug
        results_dict[keyword + ' (' + search_dict[keyword]['Unit(s)'] + ')'] = formatting(
            results_dict[keyword + ' (' + search_dict[keyword]['Unit(s)'] + ')'])

    # print(req_info_dict) # debug
    logging.info("OCR Successful")

    logging.info(results_dict)
    return results_dict


# Writing Output to Excel
def dict_to_excel(ocr_info_dict, search_dict):
    with ExcelWriter('Output/ocr_output.xlsx') as writer:

        # print(ocr_info_dict) # debug

        # Getting all attribute values in a list
        dict_ocr = {}
        for filename in list(ocr_info_dict.keys()):
            values_list = []
            for value in list(ocr_info_dict[filename].values()):
                values_list = values_list + value
            dict_ocr[filename] = values_list

        # print(dict_ocr)  # debug

        attribute_list = []
        for keyword in search_dict.keys():
            attribute_list.append(keyword + ' (' + search_dict[keyword]['Unit(s)'] + ')')
            length = int(search_dict[keyword]['Occurrence(s)'])
            if length > 1:
                attribute_list = attribute_list + ([' '] * (length - 1))

        # print(attribute_list)  # debug

        # Output data frame
        df = pd.DataFrame()

        df['Attributes'] = attribute_list
        for filename in list(dict_ocr.keys()):
            df[filename.split('/')[-1]] = dict_ocr[filename]

        df.to_excel(writer)

    print("\n Output Successful")


# config file reader
def config_reader(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    settings = config['settings']
    keywords = dict(config['custom keywords'])
    key_dict = {}
    for key in keywords.keys():
        key_dict[key] = literal_eval(keywords[key])

    return settings, key_dict


def launch_odin(input_folder, config_path,
                write_to_file, searchable_pdf,
                ):
    odin_start = time.time()
    start_time = time.time()

    logging.info("Reading Settings")
    settings, key_dict = config_reader(config_path)
    logging.info("Script Threshold: " + (settings['script threshold']))
    logging.info("Orientation Threshold: " + (settings['orientation threshold']))
    end_time = time.time()
    logging.info("Read settings in ""%s seconds" % (end_time - start_time))

    ocr_engine = settings['ocr path']
    tess_path(ocr_engine)

    script_threshold = float(settings['script threshold']) / 100
    orientation_threshold = float(settings['orientation threshold']) / 100

    start_time = time.time()

    logging.info("\n Reading Files...")
    file_list = read_file_names(input_folder)
    end_time = time.time()
    logging.info("Read " + str(len(file_list)) + " files in ""%s seconds" % (end_time - start_time))

    logging.info("\n Processing...")
    req_info_dict = {}
    for file in file_list:
        start_time = time.time()
        logging.info("\nProcessing " + file)

        image = pdf_to_image(file)
        oriented_image = orient_image(image[0],
                                      orientation_threshold=orientation_threshold, script_threshold=script_threshold)
        table_img = crop_table(oriented_image, file)
        req_info_dict[file] = image_ocr(table_img, file,
                                        write_to_file=write_to_file, searchable_pdf=searchable_pdf,
                                        search_dict=key_dict)

        end_time = time.time()
        logging.info("Processed " + file + " in ""%s seconds" % (end_time - start_time))
    # print(req_info_dict)  # debug

    start_time = time.time()

    logging.info("\n Writing to Excel...")
    dict_to_excel(req_info_dict, key_dict)
    end_time = time.time()
    logging.info("Written to Excel in ""%s seconds" % (end_time - start_time))

    odin_end = time.time()
    logging.info("OCR done in ""%s seconds" % (odin_end - odin_start))


if __name__ == "__main__":
    launch_odin(input_folder='Input', config_path='config.ini', write_to_file=False, searchable_pdf=False)
