import pytesseract as tesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# File
filename = 'Vs-762-R3 - GA.pdf'

images = convert_from_bytes(open(filename, 'rb').read(), grayscale=False)

print(type(images[0]))

# Image to Text
img = images[0]
img.show()
info = tesseract.image_to_osd(img)
info = info.split('\n')
rotation_angle = info[1]
key = 'Orientation in degrees: '
rotation_angle = rotation_angle[rotation_angle.index(key) + len(key):]
rotation_angle = int(rotation_angle)
img = img.rotate(rotation_angle, expand = True)
img.show()


text = tesseract.image_to_string(img, config=r'--psm 6')
print("Text from Image")
print(text.lower())
text_file = open(filename.split('.')[0] + "_ocr.txt", "w")
n = text_file.write(text)
text_file.close()

ocr_list = text.lower().split('\n')
print(ocr_list)
# req_list = ['bridas','acoplamientos','tornilleria externa','presion de diseno interna']
# req_info = {}
# for item in ocr_list:
#     for key in req_list:
#         if key in item:
#             s1 = item
#             s2 = key
#             info = s1[s1.index(s2) + len(s2) + 1:]
#             req_info[key] = info
#
# print(req_info)

# Image to searchable PDF
# pdf = tesseract.image_to_pdf_or_hocr(filename, extension='pdf')
# f = open(filename.split('.')[0] + ".pdf", "w+b")
# f.write(bytearray(pdf))
# f.close()
