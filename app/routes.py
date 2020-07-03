import os
import json
from flask import render_template, request, jsonify, send_file, send_from_directory
from app import app
from PyPDF2 import PdfFileWriter, PdfFileReader
import requests
from requests_toolbelt import MultipartEncoder


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
        pages= {}


        for i in range(0,pdf_data.numPages,1):
            output.addPage(pdf_data.getPage(i))
            page = i + 1

        
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
                print('Created: {}'.format("document-page%s.pdf" % i))
                outputStream.close()

            with open("document-page%s.pdf" % i,"rb") as doc_page:
                pages.update({'page%s' % i : (doc_page,open("document-page%s.pdf" % i,"rb"),'application/pdf')})
                doc_page.close()

        m=MultipartEncoder(pages)
    

            
            
        os.remove("document-page%s.pdf" % i)
    else:
        return "please upload a file to process" , 403
    
 #   with open("output_INV.pdf", "wb") as outputStream:
 #       path ='/home/smokeythebear/Documents/Python/cimarex/output_INV.pdf'
 #       output.write(outputStream)
        #print('Created: {}'.format("document-page%s.pdf" % i))
 #       outputStream.close()

    return Response(m.to_string(), mimetype=m.content_type)


@app.route('/convert', methods = ['POST'])
def convert():
    uri='https://api.cloudconvert.com/v2/convert'
    h = {"Authorization": "cw3fcEID0Jq9vj11yIE9ck2wQxRE3Qo3BGFwnhIdsZVlwk9tKuf67jjCpd9eyq6M","Content-type": "application/json"}
    
    if 'pdf' in request.files:
        incoming_pdf = request.files['pdf']

        data={
        "input": incoming_pdf,    
        "input_format": "pdf",
        "output_format": "png",
        }
        x= requests.post(uri,headers=h, data=datas)
        print(x.content)
        

    return 'success'