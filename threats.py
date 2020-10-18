#!/usr/bin/ python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yagmail
import requests
import json
import datetime
import getpass
import smtplib, ssl


array=[]
port = 465 # SSL
smtpServer = "smtp.gmail.com"
senderEmail = "bcs.sec.notification@gmail.com"
receiverEmail = "receiveremail@gmail.com"


def sendEmail2(array):
    body=json.dumps(array)
    yag = yagmail.SMTP(senderEmail)
    yag.send(
        to=receiverEmail,
        subject="Notification",
        contents=array
    )
 

def emailBody(type,array):
    
    if(type == 'text'):
        message = '''\
            You have new threats {}'''.format(array)
        

    elif(type == 'html'):
        message =  '''\
            <html>
                <body>
                    <h2> Blue Cat Security </h2>
                    <a href="https://cybersecurity.telefonica.com/threats/">View Threat</a>
                    <p> {} </p>
                </body>
            </html>
            '''.format(array)
    
    return MIMEText(message,type)
    

#Creo contexto SSL
def sendEmail(array):
    password = getpass.getpass("Ingrese clave: ")
    message = emailBody('html',array)
    body=json.dumps(array)
    msg = MIMEMultipart()
    msg['Subject'] = "Telefónica Cibervigilancia Alert"
    msg.attach(message)
    text = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
        server.login(senderEmail, password)
        server.sendmail(senderEmail,receiverEmail,text)
    
def isNewThreat(threat):
    if(datetime.datetime.fromtimestamp(threat['validated_at']).strftime('%Y/%m/%d') == datetime.datetime.today().strftime('%Y/%m/%d')):
        return True
    else:
        return False


def getRequest():
    r = requests.get('https://cybersecurity.telefonica.com/threats/api/v2/threats?api_key=""')
    # convierto json a diccionario (dict)
    t = json.loads(r.text)
    threats = t['data']['threats']

    for threat in threats:
        if (isNewThreat(threat)):
            array.append({
                'Nombre':threat['name'],
                'Razon':threat['reason'],
                'Fecha_Deteccion': datetime.datetime.fromtimestamp(threat['validated_at']).strftime('%d/%m/%Y --- %H:%M:%S'),
                'Riesgo': threat['risk_value'],
                'Estado': threat['status']
            }) 
        '''print("---------------------------------------------")
        print("Nombre: "+ threat['name'])
        print("Razon: "+ threat['reason'])
        print("Fecha detección: ", datetime.datetime.fromtimestamp(threat['validated_at']).strftime('%d/%m/%Y --- %H:%M:%S'))
        print("Fecha actualización: ", datetime.datetime.fromtimestamp(threat['updated_at']).strftime('%d/%m/%Y --- %H:%M:%S'))
        print("Riesgo: ", threat['risk_value'])
        print("Estado: "+ threat['status'])
        #print("Riesgo:"+ threat['risk_value'])'''
    sendEmail(array)

getRequest()



