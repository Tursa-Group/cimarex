import os
import json
from flask import render_template, request, jsonify, send_file, send_from_directory
from app import app
from PyPDF2 import PdfFileWriter, PdfFileReader
import requests

from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)



@app.route('/')
def start():
    return "holi world"


@app.route('/upload', methods = ['POST'])
def upload():
    parent_file= (request.form.get('parent_pdf_id'))
    workflow_id= (request.form.get('workflow_id'))
    pdf_data = None 
    doc_images = list()
    #return "test", 200
    if 'pdf' in request.files:
        incoming_pdf = request.files['pdf']
        pdf_data = PdfFileReader(incoming_pdf, 'rb')
        output = PdfFileWriter()
        output.addPage(pdf_data.getPage(0))
        for i in range(0,pdf_data.numPages,1):
            output.addPage(pdf_data.getPage(i))
            page = i + 1
            
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
                print('Created: {}'.format("document-page%s.pdf" % i))
                outputStream.close()

           # with open("document-page%s.pdf" % i,"rb") as doc_page:
            #    images = convert_from_bytes(doc_page.read(), fmt='png')
             #   doc_images.append(images)
            

            
            
            os.remove("document-page%s.pdf" % i)
    else:
        return "please upload a file to process" , 403
    
    with open("output_INV.pdf", "wb") as outputStream:
        path ='/home/smokeythebear/Documents/Python/cimarex/output_INV.pdf'
        output.write(outputStream)
        #print('Created: {}'.format("document-page%s.pdf" % i))
        outputStream.close()

        return send_file(path, as_attachment=True, mimetype='application/pdf')



       