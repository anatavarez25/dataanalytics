# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:13:07 2020

@author: DELL
"""

#import  package
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os 
import pandas as pd
import nltk
#nltk.download()

import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


path = 'FUERZA DEL PUEBLO - FP - PROGRAMA DE GOBIERNO 2020 - 2024.pdf'

#function that converts PDF to text
#optional parameter PAGES can restrict which pages to process
def convert_pdf_to_txt(path, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    
    #Instantiate the PDFminer objects
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    
    infile = open(path, 'rb') #open the file for read in binary mode
    
    for page in PDFPage.get_pages(infile, pagenums):     #iterate with the pdf interpreter through the pdf pages
        interpreter.process_page(page)
    
    #Close the files and converters
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    
    return text   #return the text as str

text = convert_pdf_to_txt(path) #call the function for the file specified here

#This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
if text != "":
   text = text

#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
else:
   text = textract.process(path, method='tesseract', language='spa')


#df = pandas.DataFrame({"text":[text]}) #convert the TEXT str to Panda's DF

#The word_tokenize() function will break our text phrases into individual words.
tokens = word_tokenize(text)
tokens2 = sent_tokenize(text)
#We'll create a new list that contains punctuation we wish to clean.
punctuations = ['(',')',';',':','[',']',',', '?','"','.','!','˜','˚','#','|','-','%','...','','–']
otras = ['344','De','Del','Dr.','Dr. ','así','cada','través','país', 'Y','DE','n','s','l','m','d','p','r','ie','c','i','tos','ágina','La','El','228']
numeros =['0','1','2','3','4','5','6','7','8','9']
pal_int = ['Cambio','cambio','innovación','tecnología','mujer','mujeres','desarrollo','educación','salud','empleo','electricidad','energía','seguro','seguridad','oportunidades','pandemia','coronavirus','COVID-19','salud','finanzas','financiero','economía','recuperar','recuperación']
candidato=['Gonzalo','Castillo','Abinader','Leonel','Fernández','Moreno']
#We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.

stop_words = stopwords.words('spanish')
#We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word in stop_words and not word in punctuations and not word in otras and not word in numeros]
total_words = [word for word in tokens if not word in punctuations and not word in otras]
int_words = [word for word in tokens if word in pal_int]
cands = [word for word in tokens if word in candidato]
#analisis palabras


import matplotlib as plt
#general
counts,values = pd.Series(keywords).value_counts().values, pd.Series(keywords).value_counts().index
df_results = pd.DataFrame(list(zip(values,counts)),columns=["palabra","cant"])

#export excel
df_results.to_excel(r'C:\Users\DELL\Desktop\data science\Text Mining Candidatos RD 2020\FP.xlsx', index = False)

#graficos
freq = nltk.FreqDist(keywords)
freq.plot(25, cumulative=False)

#especifico

counts2,values2 = pd.Series(int_words).value_counts().values, pd.Series(int_words).value_counts().index
df_results2 = pd.DataFrame(list(zip(values2,counts2)),columns=["palabra","cant"])

#excel
df_results2.to_excel(r'C:\Users\DELL\Desktop\data science\Text Mining Candidatos RD 2020\FP.xlsx', sheet_name='2', index = False)

#graficos
freq = nltk.FreqDist(int_words)
freq.plot(25, cumulative=False)
df_results2.plot(kind='bar',x='palabra',y='cant')

#candidato
counts3,values3 = pd.Series(cands).value_counts().values, pd.Series(cands).value_counts().index
df_results3 = pd.DataFrame(list(zip(values3,counts3)),columns=["palabra","cant"])

#para wordcloud
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import urllib
import requests
import matplotlib.pyplot as plt

mask = np.array(Image.open(requests.get('http://www.clker.com/cliparts/O/i/x/Y/q/P/yellow-house-hi.png', stream=True).raw))
words = str(pal_int)
def generate_wordcloud(words, mask):
    word_cloud = WordCloud(width = 512, height = 512, background_color='white', stopwords=STOPWORDS, mask=mask).generate(words)
    plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    
generate_wordcloud(words, mask)

