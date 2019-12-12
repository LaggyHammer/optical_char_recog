# import pytesseract as tesseract
# from PIL import Image
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
#
# tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#
# # File
# filename = 'do-a-complete-drawing-of-the-general-arrangement-of-your-pressure-vessel.jpg'
#
# # Image to Text
# img = Image.open(filename)
# text_proc = tesseract.image_to_string(img)
# print("Text from Processed Image")
# print(text_proc)
# #print(type(text))
#
# print("Text from Raw Image")
# text_unproc = tesseract.image_to_string(filename)
# print(text_unproc)
# #print(type(text))
#
# # Program to measure similarity between
# # two sentences using cosine similarity.
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# # X = input("Enter first string: ").lower()
# # Y = input("Enter second string: ").lower()
# X = text_proc
# Y = text_unproc
#
# # tokenization
# X_list = word_tokenize(X)
# Y_list = word_tokenize(Y)
#
# # sw contains the list of stopwords
# sw = stopwords.words('english')
# l1 = [];
# l2 = []
#
# # remove stop words from string
# X_set = {w for w in X_list if not w in sw}
# Y_set = {w for w in Y_list if not w in sw}
#
# # form a set containing keywords of both strings
# rvector = X_set.union(Y_set)
# for w in rvector:
#     if w in X_set:
#         l1.append(1)  # create a vector
#     else:
#         l1.append(0)
#     if w in Y_set:
#         l2.append(1)
#     else:
#         l2.append(0)
# c = 0
#
# # cosine formula
# for i in range(len(rvector)):
#     c += l1[i] * l2[i]
# cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
# print("similarity: ", cosine)

from fuzzysearch import find_near_matches
import itertools
import re

# # Static Load
# text = "| ' SI STATIC LOAD PER SUPPORT POINT Pts = 541 kg. P2s=451 kg.\na yy aA _ So “ol \ STATIC LOAD PER SUPPORT " \
#        "POINT Ps = 315 kg ; P,s = 297 kg\n2 STATIC LOAD PER SUPPORT POINT Pl = 7442 kg. P2 = 7031 kg.\nS55 PS AT Thal " \
#        "SSS ES -— - — 4 - — STATIC LOAD PER SUPPORT POINT Pl = 4327 kg. P2 = 4202 ko.\n[EA Sa Ne] Wan ot -STATIC LOAD " \
#        "PER SUPPORT POINT Pils = 472 kg; P2s = 410 kg.\nSTATIC LOAD PER SUPPORT POINT DISCHARGE END / FEED END | IZA] " \
#        "“7 oo a> a : oh ep\nP1 = 848 kg P2 = 940 kg a i I . ,' "
# text = text.lower()
# print(text)
#
#
# def find_static_load(text, key='STATIC LOAD PER SUPPORT POINT'):
#     results = []
#     key = key.lower()
#     match_list = find_near_matches(key, text, max_l_dist=2)
#     search_start = match_list[0][0]
#     search_string = text[search_start:]
#     equal_sign_pos = search_string.find('=')
#     search_string = search_string[equal_sign_pos - 5: equal_sign_pos + 100]
#     for m in itertools.islice(re.finditer("p.{0,2}s{0,1}\s{0,1}=\s{0,1}\d{1,5}\sk(g|o)", search_string), 2):
#         result = m.string[m.start():m.end()]
#         print(result)
#         results.append(result)
#
#     return results

# # Spring Constant
# text = "' | 2 SPRING CONSTANT OF FOUNDATION BUFFER ¢ = 20 kg/mm.\n/ KN | \ f \ <P / SPRING CONSTANT (BUFFER / SPRING) " \
#        "C = 20 kg/mm\nPIPE STI FFENERS 8,34m = 12,1 kg (6mm THK) SPRING CONSTANT OF FOUNDATION SPRING CDIL SPRINGS c " \
#        "= 13.5 kg/mm RUBBER BUFFERS c = 70 kg/mm\n| SS (ee 6-HOLES 918. =) 550_CRS 550_CRS 2 «9 SPRING CONSTANT OF " \
#        "FOUNDATION SPRING c= 16.8 kg/mm\n| | | I | -SPRING CONSTANT (RUBBER BUFFER) c¢ = 20 kg/mm\nSPRING CONSTANT OF " \
#        "FOUNDATION SPRING c=5Okg/mm j 1 é aise = I a SPB 2530 I \. WN "
#
# text = text.lower()
# print(text)
# req_list=['SPRING CONSTANT OF']
#
# import itertools
# import re
#
# for key in req_list:
#     key = key.lower()
#     jar = find_near_matches(key, text, max_l_dist=2)
#     print(jar)
#     for match in jar:
#         search_start = match[0]
#         search_string = text[search_start:]
#         equal_index = search_string.find('=')
#         print(equal_index)
#         search_string = search_string[equal_index - 5: equal_index + 100]
#         print("Searching in:")
#         print(search_string)
#         for m in itertools.islice(re.finditer("\d{0,3}\.{0,1}(\d|o){0,3}\s{0,1}k(g|o)/mm", search_string), 1):
#             print(m.string[m.start():m.end()])


# # Operating Speed
# text = "| OPERATING SPEED n = 980 r.p.m.\nOPERATING SPEED n = 900 r/min. (MAX, >\n. EP Eee ee a OPERATING SPEED = 947 " \
#        "r/min, MAX.\na 25 25 | -OPERATING SPEED n = 1440 r.p.m\nDPERATING SPEED n=1000 r. p.m 2 oe L Fas 4 & I | ‘ BX " \
#        "J JE\nes q \ [ @ \ \ ‘ OPERATING SPEED 960 rpm "
#
# text = text.lower()
# print(text)
# req_list=['OPERATING SPEED']
#
# import itertools
# import re
#
# for key in req_list:
#     key = key.lower()
#     jar = find_near_matches(key, text, max_l_dist=2)
#     print(jar)
#     for match in jar:
#         search_start = match[0]
#         search_string = text[search_start:]
#         print("Searching in:")
#         print(search_string)
#         for m in itertools.islice(re.finditer("\d{1,5}\s{0,1}(r.{0,1}\s{0,1}p.{0,1}\s{0,1}m.{0,1}|r\s{0,1}\/\s{0,1}min)", search_string), 1):
#             print(m.string[m.start():m.end()])


# # Total Mass
# text = "2 TOTAL MASS OF SCREEN & SUBFRAME 2P1s + 2P2s = 1985 kg.\n3 ! ! oT _ SQ ° A TOTAL MASS OF SCREEN AND SUBFRAME " \
#        "2P.s + 2P,s = 1224 kg\nSIDE PLATE (B) 9,78m = 142.0kg (10mm THK) TOTAL MASS OF SCREEN AND SUBFRAME 2P1 + 2P2 " \
#        "= 28946 kg.\nSS ! | PANELS Ee SSS] ! UNDERPAN TOTAL MASS OF SCREEN 2P1 + 2P2 = 17058 kg.\n3 1 -TOTAL MASS OF " \
#        "SCREEN 2P1s + 2P2s = 1764 kg.\nTOTAL MASS OF SCREEN 2P14+2P2 = 3576 kg oe WA ©: prs > fh ee uw Wa 7 oO "
#
# text = text.lower()
# print(text)
# req_list=['TOTAL MASS OF']
#
# import itertools
# import re
#
# for key in req_list:
#     key = key.lower()
#     jar = find_near_matches(key, text, max_l_dist=2)
#     print(jar)
#     for match in jar:
#         search_start = match[0]
#         search_string = text[search_start: search_start + 100]
#         # equal_index = search_string.find('=')
#         # print(equal_index)
#         # search_string = search_string[equal_index - 5: equal_index + 100]
#         print("Searching in:")
#         print(search_string)
#         for m in itertools.islice(re.finditer("\d{1,5}\s{0,1}k(g|o)", search_string), 1):
#             print(m.string[m.start():m.end()])
