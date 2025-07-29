import json
from datetime import datetime
import time
import requests
import os


bikeurl = 'https://api.tfl.gov.uk/BikePoint'

response = requests.get(bikeurl)
max_tries = 3
current_try = 0
wait_time = 2
errorvar = ''
now = datetime.now()
while current_try<max_tries:
    try:
        os.makedirs('data', exist_ok=True)
        response.raise_for_status() #method checks if reposne returns an error status. will fail try block if so
        try:
            data = response.json()
        except ValueError:
            errorvar = 'API output is not a JSON'
        if errorvar != '':
            raise Exception("error")
        elif len(data) < 50:
            errorvar = 'API JSON result is too short'
            raise Exception("error")
        timestamps = []
        for item in data:
            for prop in item.get('additionalProperties', []):
                timestamps.append(prop['modified'])
        try:
            max_modified_date = max(datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ') for ts in timestamps)
            datediff = (now-max_modified_date).days
            if int(datediff) > 2:
                errorvar = 'API has not been refreshed in over two days. No output will be provided :('
        except:
            print("Error in parsing dates to check for stale data")
            print("Could not verify if API has the most recent data")
        filename = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        filepath = 'data/'+filename+'.json'
        with open(filepath,'w') as file:
            json.dump(data,file)
        print(f'Data extracted successfully. Filename: {filename}.json' )
        break
    except requests.exceptions.RequestException as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f'Invalid JSON: {e}')
    except:
        if errorvar != '':
            print(errorvar)
        elif response.status_code == 200:
            print('API is calling but the code has failed')
        else:
            print('Unknown error has ocurred')
    
    current_try +=1
    print('waiting.... trying again')
    time.sleep(wait_time)
if current_try == max_tries:
    print('Max attempt number reached. Exiting.')