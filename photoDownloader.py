import re
import json
import requests
import os
import datetime

api_key = "1079cc75c0dc132799da40256e42011a"
secret = "5bbdc1b5907307d7"

userDatas = dict()
photoDatas = dict()

pids = []
uids = []

for i in range(8):
    os.makedirs('./train_folder' + str(i+1), exist_ok=True)


def loadData():
    f = open('./t1_train_image_link.txt')
    ef = open('./error_list.txt', 'w')
    ef.write('')
    datas = f.readlines()
    size = len(datas)
    print(size)
    for i, li in enumerate(datas):
        print("processing {0} / {1}".format(i+1, size))
        uid = re.search(r'https://www.flickr.com/photos/(\w+@\w+)/\d+', li).group(1)
        pid = re.search(r'https://www.flickr.com/photos/\w+@\w+/(\d+)', li).group(1)
        parameters = {
            'method': 'flickr.photos.getSizes',
            'api_key': api_key,
            'photo_id': pid,
            'format': 'json',
            'nojsoncallback': 1
            }
        try:
            r = requests.post(
                'https://api.flickr.com/services/rest/?',
                data=parameters
                ).content.decode('utf-8')
            jsondata = json.loads(r)
            if jsondata['stat'] == 'ok':
                url = jsondata['sizes']['size'][len(jsondata['sizes']['size'])-1]['source']
                print(url)
                p = open('./train_folder1/{0}.jpg'.format(pid), 'wb')
                pdata = requests.get(url)
                p.write(pdata.content)
                p.close()
            else:
                print('Wrong PhotoID, link = {0}'.format(li))
                ef.writelines(li)

        except:
            print('Connection ERROR')
            ef.writelines(li)

    f.close()
    ef.close()


loadData()

