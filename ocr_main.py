import pytesseract as tesseract
from pdf2image import convert_from_bytes
import pandas as pd
from pandas import ExcelWriter

# Tesseract OCR File Path
tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# PDF to Image Function
def pdf_to_image():
    file_dict = {}
    take_filenames = True
    while take_filenames:
        filename = input("Enter PDF File name: ") + '.pdf'  # Filename Input
        images = convert_from_bytes(open(filename, 'rb').read())  # Image Conversion
        file_dict[filename] = images
        cont_input = input("Continue inputting file names? [y/n] :")
        if cont_input.lower() == 'n':
            take_filenames = False
        elif cont_input.lower() == 'y':
            continue
        else:
            print("Non-valid Input")

    return file_dict


# Orientation Handling
def orient_image(image_dict, orientation_threshold=0.5, script_threshold=0.5):
    oriented_images = {}
    for filename in image_dict.keys():
        for img in image_dict[filename]:
            print("Handling Orientation for image " + filename + "...")
            info = tesseract.image_to_osd(img)  # Orientation Info

            # Aspect Ratio Check
            (width, height) = img.size
            if height > width:
                img = img.rotate(90, expand=True)
                info = tesseract.image_to_osd(img)  # Orientation Info
                # print(info)
            info = info.split('\n')

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

            # img.show()  # Enable when debugging
            oriented_images[filename] = img

    if oriented_images:
        print("Orientation Handling Successful")
    return oriented_images


# Image to Text
def image_ocr(image_dict, req_list=None):
    if req_list is None:
        req_list = []
    req_info_dict = {}

    for filename in image_dict.keys():
        img = image_dict[filename]
        text = tesseract.image_to_string(img, config=r'--psm 6')
        # print("Text from Image")
        # print(text.lower())

        text_file = open(filename.split('.')[0] + "_ocr.txt", "w")
        n = text_file.write(text)
        text_file.close()

        ocr_list = text.lower().split('\n')
        # print(ocr_list)
        req_info = {}
        print("Looking for terms in the required list...")
        for item in ocr_list:
            for key in req_list:
                key = key.lower()
                if key in item:
                    s1 = item
                    s2 = key
                    info = s1[s1.index(s2) + len(s2) + 1:]
                    req_info[key] = info
        if bool(req_info):
            print("Term Matches Found: ")
        req_info_dict[filename] = req_info

    print(req_info_dict)
    return req_info_dict


# Writing Output to Excel
def dict_to_excel(ocr_info_dict):
    with ExcelWriter('ocr_output.xlsx') as writer:
        for filename, info in ocr_info_dict.items():
            print("Output for " + filename + ": \n")
            df = pd.DataFrame(data=info, index=[0])
            df = df.T
            print(df)
            print("Writing to Excel...")
            df.to_excel(writer, sheet_name=filename.split('.')[0])


converted_images_dict = pdf_to_image()
oriented_images_dict = orient_image(converted_images_dict)
info_list = image_ocr(oriented_images_dict,
                      req_list=['TOTAL MASS OF SCREEN & SUBFRAME', 'STATIC LOAD PER SUPPORT POINT',
                                'SPRING CONSTANT OF FOUNDATION BUFFER', 'OPERATING SPEED'])
#dict_to_excel(info_list)

# Image to searchable PDF
# pdf = tesseract.image_to_pdf_or_hocr(filename, extension='pdf')
# f = open(filename.split('.')[0] + ".pdf", "w+b")
# f.write(bytearray(pdf))
# f.close()
