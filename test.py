from pyquery import PyQuery as pq
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

def loadData():
    # f = open('./t1_train_image_link.txt')
    f = open('./test.txt', 'r')
    ef = open('./error_list.txt', 'w')
    ef.write('')
    datas = f.readlines()
    size = len(datas)
    for i, li in enumerate(datas):
        print("processing {0} / {1}".format(i+1, size))
        # https://www.flickr.com/photos/7130511@N02/404893650
        uid = re.search(r'https://www.flickr.com/photos/(\w+@\w+)/\d+', li).group(1)
        pid = re.search(r'https://www.flickr.com/photos/\w+@\w+/(\d+)', li).group(1)
        # print(uid)
        # print(pid)
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
                p = open('./1/{0}.jpg'.format(pid), 'wb')
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



def crewData(id):
    dom = pq('https://www.flickr.com/photos/' + id)
    # print(dom('.pro-badge-inline').html())
    f = dom('.followers').html()
    followers = float(re.search(r'(\d+\.*\d*)(\w?) Followers', f).group(1))
    unit = re.search(r'(\d+\.*\d*)(\w?) Followers', f).group(2)
    if unit == 'K':
        followers = followers * 1000
    followers = int(followers)
    return followers

def getPhotoInfo(id):
    global photoDatas
    parameters = {
        'method': 'flickr.photos.getInfo',
        'api_key': api_key,
        'photo_id': id,
        'format': 'json',
        'nojsoncallback': 1
        }
    r = requests.post(
        'https://api.flickr.com/services/rest/?',
        data=parameters
        ).content.decode('utf-8')
    jsondata = json.loads(r)
    parameters = {
        'method': 'flickr.photos.getExif',
        'api_key': api_key,
        'photo_id': id,
        'format': 'json',
        'nojsoncallback': 1
        }
    r = requests.post(
        'https://api.flickr.com/services/rest/?',
        data=parameters
        ).content.decode('utf-8')
    jsondataEXIF = json.loads(r)
    parameters = {
        'method': 'flickr.photos.getFavorites',
        'api_key': api_key,
        'photo_id': id,
        'format': 'json',
        'nojsoncallback': 1
        }
    r = requests.post(
        'https://api.flickr.com/services/rest/?',
        data=parameters
        ).content.decode('utf-8')
    jsondataFav = json.loads(r)
    data = dict()
    photoDatas[id] = data
    data['postdateDate'] = datetime.datetime.fromtimestamp(1172605434).strftime("%Y-%m-%d")
    data['postdateTime'] = datetime.datetime.fromtimestamp(1172605434).strftime("%H:%M:%S")
    data['numberOfViewsOfThatPhoto'] = jsondata['photo']['views']
    data['hasPeopleTagged'] = jsondata['photo']['people']['haspeople']
    data['cameraType'] = jsondataEXIF['photo']['camera'].replace(' ', '_')
    data['NumberOfThisPhotoFaves'] = jsondataFav['photo']['total']
    data['description'] = jsondata['photo']['description']['_content']
    print(data)


def getUserInfo(id):
    global userDatas
    if userDatas[id]:
        return userDatas[id]
    parameters = {
        'method': 'flickr.people.getInfo',
        'api_key': api_key,
        'user_id': id,
        'format': 'json',
        'nojsoncallback': 1
        }
    r = requests.post(
        'https://api.flickr.com/services/rest/?',
        data=parameters
        ).content.decode('utf-8')
    jsondata = json.loads(r)
    data = dict()
    userDatas[id] = data
    data['NumberOfThisAuthorFollowers'] = crewData(id)
    data['authorHasPRO'] = jsondata['person']['ispro']
    data['username'] = jsondata['person']['username']['_content']
    data['postcount'] = jsondata['person']['photos']['count']['_content']

    print(data)
    return data


def getSubTags(tag):
    parameters = {
        'method': 'flickr.tags.getClusters',
        'api_key': api_key,
        'tag': tag,
        'format': 'json',
        'nojsoncallback': 1
        }
    r = requests.post(
        'https://api.flickr.com/services/rest/?',
        data=parameters
        ).content.decode('utf-8')
    jsondata = json.loads(r)
    data = dict()

# crewData('j0annie')
# crewData('23868213@N03')
# crewData('136296496@N07')

# getPhotoInfo('34401147823')
loadData()

# getUserInfo('23868213@N03')
