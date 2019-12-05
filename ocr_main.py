import pytesseract as tesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# File
filename = input("Enter PDF File name: ") + '.pdf'

# Image Conversion
images = convert_from_bytes(open(filename, 'rb').read(), grayscale=False)


# Orientation Handling
def orient_image(image_list, orientation_threshold=0.5, script_threshold=0.5):
    oriented_images = []
    image_counter = 1
    for img in image_list:
        print("Handling Orientation for image " + str(image_counter) + "...")
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

        img.show()
        oriented_images.append(img)
        image_counter += 1
    if oriented_images:
        print("Orientation Handling Successful")
    return oriented_images


# Image to Text
def image_ocr(image_list, req_list=[]):
    req_info_list = []
    for img in image_list:
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
        req_info_list.append(req_info)

    print(req_info_list)
    return req_info_list


oriented_images_list = orient_image(images)
info_list = image_ocr(oriented_images_list,
                      req_list=['TOTAL MASS OF SCREEN & SUBFRAME', 'STATIC LOAD PER SUPPORT POINT',
                                'SPRING CONSTANT OF FOUNDATION BUFFER', 'OPERATING SPEED'])

# Image to searchable PDF
# pdf = tesseract.image_to_pdf_or_hocr(filename, extension='pdf')
# f = open(filename.split('.')[0] + ".pdf", "w+b")
# f.write(bytearray(pdf))
# f.close()
