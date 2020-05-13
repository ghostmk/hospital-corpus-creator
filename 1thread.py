import json
import csv
import requests
import time
import threading

place=str(input('Enter First Location:'))
place_=place
place.replace(" ", "+")

radius=str(input('Enter the Radius:'))


response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key=enter_apikey_here')
resp_json_payload = response.json()
lat1 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
long1 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])


# place=str(input('Enter Second Location:'))
# place.replace(" ", "+")

# response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key=enter_apikey_here')
# resp_json_payload = response.json()
# lat2 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
# long2 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])






url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat1+','+long1+'&radius='+radius+'&type=hospital&key=enter_apikey_here'

headers={'content-type':'application/json',
         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}

def csv_write():
    csvfile =open('hospitals_near_'+place_+'.csv','w')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["name","lat","long"])
    response = requests.get(url=url, headers=headers).json()
    for obj in response['results']:
        writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

    print ('next_page_token' in response)
    while 'next_page_token' in response:
        URL = url + '&pagetoken=' + response['next_page_token']
        time.sleep(5)
        response = requests.get(url=url, headers=headers).json()
        for obj in response['results']:
            writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

def csv_write():
    csvfile =open('hospitals_near_'+place_+'.csv','w')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["name","lat","long"])
    response = requests.get(url=url, headers=headers).json()
    for obj in response['results']:
        writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

    print ('next_page_token' in response)
    while 'next_page_token' in response:
        URL = url + '&pagetoken=' + response['next_page_token']
        time.sleep(5)
        response = requests.get(url=url, headers=headers).json()
        for obj in response['results']:
            writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

if __name__ == '__main__':
    csv_write()
