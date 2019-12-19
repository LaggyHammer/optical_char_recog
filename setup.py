from setuptools import setup

setup(
    name='screen_ocr',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Ankit Saxena',
    author_email='ankch24@gmail.com',
    description='Reads keywords from Screen Drawings and writes them to Excel',
    classifiers=['Programming Language::Python::3.7'],
    include_package_data=True,
    install_requires=[
          'fuzzysearch',
        'pytesseract',
        'progress',
        'pdf2image',
        'nltk',
        'pandas'
      ]

    )
