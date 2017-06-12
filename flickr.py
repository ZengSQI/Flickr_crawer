import requests
import untangle
import re
from pyquery import PyQuery as pq

api_key = "1079cc75c0dc132799da40256e42011a"
secret = "5bbdc1b5907307d7"

for i in range(8):
    os.makedirs('./train_folder' + str(i+1), exist_ok=True)


def getPhotoInfo(id):
    data = {'method': 'flickr.photos.getInfo',
            'api_key': api_key,
            'photo_id': id,
            'format': 'json'}
    r = requests.post('https://api.flickr.com/services/rest/?', data=data)
    xml = r.content.decode('utf-8')
    obj = untangle.parse(xml)
    photo = obj.rsp.photo
    return photo


def getUserInfo(id):
    data = {'method': 'flickr.people.getInfo', 'api_key': api_key, 'user_id': id}
    r = requests.post('https://api.flickr.com/services/rest/?', data=data)
    xml = r.content.decode('utf-8')
    obj = untangle.parse(xml)
    person = obj.rsp.person
    return person


def getFaves(id):
    data = {'method': 'flickr.photos.getFavorites', 'api_key': api_key, 'photo_id': id}
    r = requests.post('https://api.flickr.com/services/rest/?', data=data)
    xml = r.content.decode('utf-8')
    obj = untangle.parse(xml)
    faves = obj.rsp.photo['total']
    return faves


def getSubTags(tag):
    data = {'method': 'flickr.tags.getClusters', 'api_key': api_key, 'tag': tag}
    r = requests.post('https://api.flickr.com/services/rest/?', data=data)
    xml = r.content.decode('utf-8')
    obj = untangle.parse(xml)
    clusters = obj.rsp.clusters
    return clusters


def crewData(id):
    r = requests.get('https://www.flickr.com/photos/' + id)
    x = re.search('href="/account/upgrade/pro"', r.content.decode('utf-8'))
    f = re.search(r'<p class="followers truncate">(\d+\.*\d*\w.) Followers', r.content.decode('utf-8'))
    followers = f.group(1)
    if x:
        return ["Yes", followers]
    return ["No", followers]

test = 'https://www.flickr.com/photos/7130511@N02/404831301'


r = re.match(r'https://www.flickr.com/photos/(\d+@N\d+)/(\d+)', test)

author_id = r.group(1)
photo_id = r.group(2)

photo = getPhotoInfo(photo_id)
person = getUserInfo(author_id)
crew = crewData(author_id)


taglist = [tag.cdata for tag in photo.tags.tag]
tagdict = dict()
for tagname in taglist:
    data = getSubTags(tagname)
    tagdict[tagname] = list()
    for clusters in data:
        for cluster in clusters.cluster:
            for tag in cluster.tag:
                tagdict[tagname].append(tag.cdata)
print("photo id :", photo_id)
print("author_id :", author_id)
print("Owner :", photo.owner['username'])
print("Tags :", [tag.cdata for tag in photo.tags.tag])
print("Sub tags :", tagdict)
print("Postdate :", photo.dates['taken'])
print("Title :", photo.title.cdata)
print("Description:", photo.description.cdata)
print("Author has PRO :", crew[0])
print("Number of this author followers :", crew[1])
print("Number of this author posts :", person.photos.count.cdata)
print("Number of this photo faves :", getFaves(photo_id))
