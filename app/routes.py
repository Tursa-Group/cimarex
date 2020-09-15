import os
import json
import zipfile
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
        zipf = zipfile.ZipFile('Name.zip','w', zipfile.ZIP_DEFLATED)
        fields={}

        for i in range(0,pdf_data.numPages,1):
            output = PdfFileWriter()
            output.addPage(pdf_data.getPage(i))
            page = i + 1

        
            with open("document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
                print('Created: {}'.format("document-page%s.pdf" % i))
                outputStream.close()

            with open("document-page%s.pdf" % i, "rb") as response_File:
                fields.update({'document-page%s'% i: ('filename', open('document-page%s.pdf'% i, 'rb'), 'Application/pdf')})
                zipf.write("document-page%s.pdf" % i)
                print(fields)

            os.remove("document-page%s.pdf" % i)

        zipf.close()

        m = MultipartEncoder(fields)
        print(m)


    else:
        return "please upload a file to process" , 403

    return send_file('../Name.zip',
            mimetype = 'zip',
            attachment_filename= 'Name.zip',
            as_attachment = True)


@app.route('/addrates', methods = ['POST'])
def addrates():

    incoming_data = request.json
    service_ticket = None
    rate_group = None
    labour_trades = []
    equipment_trades = []

    if 'id' in incoming_data[0]:
        service_ticket = incoming_data[0]['id']
        rate_group = incoming_data[0]['field_242_raw'][0]['id']
        labour_rates_url = 'https://api.knack.com/v1/objects/object_15/records?filters=%5B%7B%22field%22%3A%22field_225%22%2C%22operator%22%3A%22is%22%2C%22value%22%3A%22{}%22%7D%5D'.format(rate_group)
        equipment_rates_url = 'https://api.knack.com/v1/objects/object_33/records?filters=%5B%7B%22field%22%3A%22field_225%22%2C%22operator%22%3A%22is%22%2C%22value%22%3A%22{}%22%7D%5D'.format(rate_group)
        service_ticket_url = 'https://api.knack.com/v1/objects/object_2/records/{}'.format(service_ticket)
        auth_upload = {
        'X-Knack-Application-Id':'5ebb23057aae080017afe379',
        'X-Knack-REST-API-KEY':'2fd90c50-94b0-11ea-b236-b17621236c3e'
        }
        r=requests.get(url=labour_rates_url,headers=auth_upload)
        response = json.loads(r.text)
        labour_records = response['records']
        print(labour_records)

        for record in labour_records:
            labour_trades.append(record['id'])

        equipment_records = requests.get(url=equipment_rates_url,headers=auth_upload)
        e_response = json.loads(equipment_records.text)
        equipment_records = e_response['records']

        for record in equipment_records:
            equipment_trades.append(record['id'])

        update_data = {
            'field_244': labour_trades,
            'field_252': equipment_trades
        }
        update_record = requests.put(url=service_ticket_url,headers=auth_upload, json=update_data)
        update_response = json.loads(update_record.text)
        print(update_response)
        return str(update_response)

    else:
        print('data not reaching processing')
        return 'please include the records data'