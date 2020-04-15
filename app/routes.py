import os
import json
from flask import render_template, request, jsonify
from app import app
from PyPDF2 import PdfFileWriter, PdfFileReader
import requests

@app.route('/')
def start():
    return "Hello, World!"


@app.route('/upload', methods = ['POST'])
def upload():
    parent_file= (request.form.get('parent_pdf_id'))
    pdf_data = None 
    xtracta_ids = list()
    #return "test", 200
    if 'pdf' in request.files:
        incoming_pdf = request.files['pdf']
        pdf_data = PdfFileReader(incoming_pdf, 'rb')
        for i in range(0,pdf_data.numPages,2):
            output = PdfFileWriter()
            output.addPage(pdf_data.getPage(i))
            page = i + 1
            with open("document-page%s.pdf" % page, "wb") as outputStream:
                output.write(outputStream)
                print('Created: {}'.format("document-page%s.pdf" % i))
                outputStream.close()

            with open("document-page%s.pdf" % page, "rb") as file_to_send:
                print(file_to_send)
                files = {'userfile': file_to_send}
                upload_url ='https://api-app.xtracta.com/v1/documents/upload'
                auth_upload = {
                'api_key':'b65d6427252e69e4aa29728f6ebfbf43ccf2f266',
                'workflow_id':'965372'
                }

                r=requests.post(url=upload_url, files=files,data=auth_upload)
                xtracta_id = r.content[115:124]
                xtracta_ids.append(xtracta_id)
                file_to_send.close()

                
            os.remove("document-page%s.pdf" % page)

        else:
         return "please upload a file to process" , 403

    return "success" 



    return "Hello, World!"