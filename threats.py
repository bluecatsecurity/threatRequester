#!/usr/bin/ python

import requests
import json
import datetime


def isNewThreat(threat):
    if(datetime.datetime.fromtimestamp(threat['validated_at']).strftime('%Y/%m/%d') == datetime.datetime.today().strftime('%Y/%m/%d')):
        return True
    else:
        return False


r = requests.get('https://cybersecurity.telefonica.com/threats/api/v2/threats?api_key=""')
# convierto json a diccionario (dict)
t = json.loads(r.text)
threats = t['data']['threats']

for threat in threats:
    if (isNewThreat(threat)):
        print("---------------------------------------------")
        print("Nombre: "+ threat['name'])
        print("Razon: "+ threat['reason'])
        print("Fecha detección: ", datetime.datetime.fromtimestamp(threat['validated_at']).strftime('%d/%m/%Y --- %H:%M:%S'))
        print("Fecha actualización: ", datetime.datetime.fromtimestamp(threat['updated_at']).strftime('%d/%m/%Y --- %H:%M:%S'))
        print("Riesgo: ", threat['risk_value'])
        print("Estado: "+ threat['status'])
        #print("Riesgo:"+ threat['risk_value'])


    






