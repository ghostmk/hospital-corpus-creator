import json
import csv
import requests
import time
import threading


place=str(input('Enter First Location:'))
place_1=place
place.replace(" ", "+")

radius=str(input('Enter the Radius:'))


response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key=enter_apikey_here')
resp_json_payload = response.json()
lat1 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
long1 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])


place=str(input('Enter Second Location:'))
place.replace(" ", "+")
place_2=place


response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key=enter_apikey_here')
resp_json_payload = response.json()
lat2 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
long2 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])






url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat1+','+long1+'&radius='+radius+'&type=hospital&key=enter_apikey_here'
url2 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat2+','+long2+'&radius='+radius+'&type=hospital&key=enter_apikey_here'

headers={'content-type':'application/json',
         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}

def csv_write():
    csvfile1 =open('hospitals_near_'+place_1+'.csv','w')
    csvfile2 =open('hospitals_near_'+place_2+'.csv','w')
    writer1 = csv.writer(csvfile1, delimiter=',')
    writer2 = csv.writer(csvfile2, delimiter=',')
    writer1.writerow(["name","lat","long"])
    writer2.writerow(["name","lat","long"])
    response1 = requests.get(url=url1, headers=headers).json()
    response2 = requests.get(url=url2, headers=headers).json()
    for obj in response1['results']:
        writer1.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

    print ('next_page_token' in response1)
    while ('next_page_token' in response1) or ('next_page_token' in response2):
        URL = url1 + '&pagetoken=' + response1['next_page_token']
        time.sleep(5)
        response = requests.get(url=url1, headers=headers).json()
        for obj in response['results']:
            writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

if __name__ == '__main__':
    csv_write()
