import os
import json
from flask import render_template, request, jsonify, send_file, Response
from app import app
from PyPDF2 import PdfFileWriter, PdfFileReader
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



@app.route('/')
def start():
    return "holi world"


@app.route('/upload', methods = ['POST'])
def upload():
    pdf_data = None 

    if 'pdf' in request.files:
        incoming_pdf = request.files['pdf']
        pdf_data = PdfFileReader(incoming_pdf, 'rb')
        fields={}
     #   'field2': ('filename', open('document-page%s.pdf'% i, 'rb'), 'Application/pdf')
        #output = PdfFileWriter()
       # output.addPage(pdf_data.getPage(0))


        for i in range(0,pdf_data.numPages,1):
            output = PdfFileWriter()
            output.addPage(pdf_data.getPage(i))
            page = i + 1

        
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
                #docs.append(output.write(outputStream))
                print('Created: {}'.format("document-page%s.pdf" % i))
                #fields.update({'document-page%s'% i: ('filename', open('document-page%s.pdf'% i, 'rb'), 'Application/pdf')})
                #print(fields)
                outputStream.close()

            with open("document-page%s.pdf" % i, "rb") as response_File:
                fields.update({'document-page%s'% i: ('filename', open('document-page%s.pdf'% i, 'rb'), 'Application/pdf')})
                print(fields)
 


            


        os.remove("document-page%s.pdf" % i)

        m = MultipartEncoder(fields)


    else:
        return "please upload a file to process" , 403
    

    return Response(m.to_string(), mimetype=m.content_type)



