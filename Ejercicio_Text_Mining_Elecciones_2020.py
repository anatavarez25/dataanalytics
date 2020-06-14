# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:44:14 2020

@author: DELL
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import PyPDF2
import pdfminer as pf
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from pdfrw import PdfReader
#objeto de pdf file
pdfFileObj = open('PDI - PROGRAMA DE GOBIERNO 2020 - 2024.pdf', 'rb')

#objeto de pdf reader
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# numero d pags en pdf
print(pdfReader.numPages)

# objeto page
pageObj = pdfReader.getPage(1)
# extraer texto de pagina.
# print de text y puedes guardarlo en string
print(pageObj.extractText())

#pdfminer texto
text = pf.high_level.extract_text('PDI - PROGRAMA DE GOBIERNO 2020 - 2024.pdf')


#otra cosa
output_string = StringIO()
with open('PDI - PROGRAMA DE GOBIERNO 2020 - 2024.pdf', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

print(output_string.getvalue())


#otro mas
x = PdfReader('PDI - PROGRAMA DE GOBIERNO 2020 - 2024.pdf')

#cantidad paginas
len(x.pages)

x.pages[1]