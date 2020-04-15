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
        output = PdfFileWriter()
        output.addPage(pdf_data.getPage(0))
        with open("document-page0.pdf", "wb") as outputStream:
            output.write(outputStream)
            print('Created: {}'.format("document-page0.pdf"))
            outputStream.close()

        with open("document-page0.pdf", "rb") as file_to_send:
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

        with open("document-page0.pdf", "rb") as pdf_to_upload:
            knack_headers= {
                'x-knack-rest-api-key': '1c6ec550-7526-11ea-9edc-dd38c98162a1',
                'X-Knack-Application-ID': '5e8632e077f0c200158408ff'
            }
            record_url= 'https://api.knack.com/v1/objects/object_4/records/'+ str(parent_file)
            record_data= {
                'field_41': xtracta_id,
            }
            record_r= requests.put(url=record_url, headers=knack_headers, data=record_data)
            print(record_r.content)
            pdf_to_upload.close() 
            
        os.remove("document-page0.pdf")
    else:
        return "please upload a file to process" , 403

    return "success"