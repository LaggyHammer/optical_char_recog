import pytesseract as tesseract
from PIL import Image
import nltk
nltk.download('punkt')
nltk.download('stopwords')

tesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# File
filename = 'do-a-complete-drawing-of-the-general-arrangement-of-your-pressure-vessel.jpg'

# Image to Text
img = Image.open(filename)
text_proc = tesseract.image_to_string(img)
print("Text from Processed Image")
print(text_proc)
#print(type(text))

print("Text from Raw Image")
text_unproc = tesseract.image_to_string(filename)
print(text_unproc)
#print(type(text))

# Program to measure similarity between
# two sentences using cosine similarity.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# X = input("Enter first string: ").lower()
# Y = input("Enter second string: ").lower()
X = text_proc
Y = text_unproc

# tokenization
X_list = word_tokenize(X)
Y_list = word_tokenize(Y)

# sw contains the list of stopwords
sw = stopwords.words('english')
l1 = [];
l2 = []

# remove stop words from string
X_set = {w for w in X_list if not w in sw}
Y_set = {w for w in Y_list if not w in sw}

# form a set containing keywords of both strings
rvector = X_set.union(Y_set)
for w in rvector:
    if w in X_set:
        l1.append(1)  # create a vector
    else:
        l1.append(0)
    if w in Y_set:
        l2.append(1)
    else:
        l2.append(0)
c = 0

# cosine formula
for i in range(len(rvector)):
    c += l1[i] * l2[i]
cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
print("similarity: ", cosine)