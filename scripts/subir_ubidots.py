from logging import error
from ubidots import ApiClient
import dotenv
import os
import requests
import time

def check_variables_entorno():
    dotenv.load_dotenv(dotenv_path='.env')
    try:
        UBIDOTS_API_TOKEN = os.environ['UBIDOTS_API_TOKEN']
        UBIDOTS_DEVICE_ID = os.environ['UBIDOTS_DEVICE_ID']
    except:
        raise error("Variables de ubidots no configuradas en .env")




def get_client_ubidots(token):
    return ApiClient(token='BBFF-mfYqpyZM2LBYAdABfUwrucY4XNOlCw')

def get_variable(api_client: ApiClient, variable):
    return api_client.get_variable('60b44d4f73efc32af6b4e3ac')

def load_data(file_path: str):
    """entrega arreglo con los datos leidos del archivo en csv. En la realidad, leeria los datos del sensor.

    Args:
        file_path (str): Path al archivo .csv
    """
    import csv
    with open(file_path, newline='') as csvfile:
        datos = []
        for fila in csv.reader(csvfile):
            datos.append(int(fila[0]))
    return datos


def post_var(sensor_value, url, device, variable, token):
    """
    Funcion que envia una solicitud POST a la api de ubidots subiendo el valor
    'sensor_value' segun las credenciales y llaves indicadas en 
    url, device y token.
    """
    try:
        url = "http://{}/api/v1.6/devices/{}".format(url, device)
        headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

        attempts = 0
        status_code = 400
        
        payload = {variable: sensor_value}
        
        while status_code >= 400 and attempts < 5:
            print("[INFO] Sending data, attempt number: {}".format(attempts))
            req = requests.post(url=url, headers=headers,
                                json=payload)
            status_code = req.status_code
            attempts += 1
            time.sleep(1)

        print("[INFO] Results:")
        print(req.text)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))

def main():
    check_variables_entorno()

    ENDPOINT = "app.ubidots.com"
    DEVICE_LABEL = "lab2-iot"
    VARIABLE_LABEL = "ph"
    datos = load_data("datos.csv")
    for i, dato in enumerate(datos[:3]):
    # OJO: Ubidots trabaja con milisegundos de timestamp!
        payload = {"value": dato, "timestamp": int(time.time() - 60 * 60 * (len(datos) - i))*1000}
        post_var(payload, url=ENDPOINT, device=DEVICE_LABEL, variable=VARIABLE_LABEL,token=os.environ['UBIDOTS_API_TOKEN'])
    print("subida exitosa!")


if __name__== "main":
    main()