import json
import csv
import requests
import time
import threading

apikey=''
place=str(input('Enter First Location:'))
place_1=place
place.replace(" ", "+")

radius1=str(input('Enter the Radius:'))


response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key='+apikey)
resp_json_payload = response.json()
lat1 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
long1 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])


place=str(input('Enter Second Location:'))
place.replace(" ", "+")
place_2 =place
radius2=str(input('Enter the Radius:'))


response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key=AIzaSyByoWKvAT9C_5uwRQJfUlwFF1jkO_kbOoc')
resp_json_payload = response.json()
lat2 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
long2 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])








# def csv_write():
#     csvfile =open('hospitals_near_'+place_+'.csv','w')
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(["name","lat","long"])
#     response = requests.get(url=url, headers=headers).json()
#     for obj in response['results']:
#         writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])

#     print ('next_page_token' in response)
#     while 'next_page_token' in response:
#         URL = url + '&pagetoken=' + response['next_page_token']
#         time.sleep(5)
#         response = requests.get(url=url, headers=headers).json()
#         for obj in response['results']:
#             urlx='https://maps.googleapis.com/maps/api/place/details/json?placeid='+obj['id']+'&fields=name,rating,formatted_phone_number&key=AIzaSyByoWKvAT9C_5uwRQJfUlwFF1jkO_kbOoc'
#             resp_x = requests.get(url=urlx, headers=headers).json()
#             #writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])
#             writer.writerow([resp_x['results']['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng'],resp_x['results']['formatted_address'],resp_x['results']['rating'],resp_x['results']['opening_hours'])

def csv_write(place,radius):
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&key='+apikey)
    resp_json_payload = response.json()
    lat1 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
    long1 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat1+','+long1+'&radius='+radius+'&type=hospital&key='+apikey

    headers={'content-type':'application/json',
         'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}
    csvfile =open('hospitals_near_'+place+'.csv','w')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["name","lat","long","address","rating","phone number","opening hours"])
    response = requests.get(url=url, headers=headers).json()
    for obj in response['results']:
        print(obj['place_id'])
        urlx='https://maps.googleapis.com/maps/api/place/details/json?placeid='+obj['place_id']+'&fields=name,rating,formatted_address,formatted_phone_number,opening_hours&key='+apikey
        resp_x = requests.get(url=urlx, headers=headers).json()
        temp=[]
        try:
            temp.append(resp_x['result']['name'])
        except:
            temp.append("NA")
        
        temp.append(obj['geometry']['location']['lat'])
        temp.append(obj['geometry']['location']['lng'])
        try:
            temp.append(resp_x['result']['formatted_address'])
        except:
            temp.append("NA")
        try:
            temp.append(resp_x['result']['rating'])
        except:
            temp.append("NA")
        try:
            temp.append(resp_x['result']['formatted_phone_number'])
        except:
            temp.append("NA")
        try:
            temp.append(resp_x['result']['opening_hours'])
        except:
            temp.append("NA")
     
        #writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])
        writer.writerow(temp)
    print ('next_page_token' in response)
    while 'next_page_token' in response:
        print(response['next_page_token'])
        URL = url + '&pagetoken=' + response['next_page_token']
        print(url)
        time.sleep(5)
        response = requests.get(url=URL, headers=headers).json()
        for obj in response['results']:
            urlx='https://maps.googleapis.com/maps/api/place/details/json?placeid='+obj['place_id']+'&fields=name,rating,formatted_address,formatted_phone_number,opening_hours&key='+apikey
            resp_x = requests.get(url=urlx, headers=headers).json()
            print(obj['place_id'])
            temp=[]
            temp.append(obj['name'])
        
            temp.append(obj['geometry']['location']['lat'])
            temp.append(obj['geometry']['location']['lng'])
            try:
                temp.append(resp_x['result']['formatted_address'])
            except:
                temp.append("NA")
            try:
                temp.append(resp_x['result']['rating'])
            except:
                temp.append("NA")
            try:
                temp.append(resp_x['result']['formatted_phone_number'])
            except:
                temp.append("NA")
            try:
                temp.append(resp_x['result']['opening_hours'])
            except:
                temp.append("NA")
            
            #writer.writerow ([obj['name'],obj['geometry']['location']['lat'],obj['geometry']['location']['lng']])
            writer.writerow(temp)

if __name__ == '__main__':
    # csv_write()
    x = threading.Thread(target=csv_write, args=(place_1,radius1,))
    y = threading.Thread(target=csv_write, args=(place_2,radius2,))
    x.start()
    y.start()
    x.join()
    y.join()
    with open('hospitals_near_'+place_1+'.csv', 'r') as f:
        reader = csv.reader(f)
        l1 = list(reader)
    with open('hospitals_near_'+place_2+'.csv', 'r') as f:
        reader = csv.reader(f)
        l2 = list(reader)
    intersection = set(tuple(x) for x in l1).intersection(set(tuple(x) for x in l2))
    with open("between_"+place_1+"_and_"+place_2+".csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(intersection)
