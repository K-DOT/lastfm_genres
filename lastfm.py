import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def make_request(params):
    url_params = urllib.parse.urlencode(params)
    url = 'http://ws.audioscrobbler.com/2.0/?%s' % url_params
    print(url)
    return urllib.request.urlopen(url).read().decode('utf-8')

def get_track_count(user, limit='50', period='7days'):
    print(user)
    res = []
    xml = make_request({
        'method' : 'user.getTopArtists',
        'user' : user,
        'limit' : limit,
        'period' : period,
        'api_key' : API_KEY
    })
    root = ET.fromstring(xml)
    for i in root.iterfind('./topartists/artist'): 
        #artist = list(list(i)[6])[0].text
        artist = list(i)[0].text
        playcount = list(i)[1].text
        res.append([artist, playcount])
    return res

def get_track_genre(tracks):
    res = {}
    for item in tracks:
        artist, playcount = item
        try:  
            xml = make_request({
                'method' : 'Artist.getTopTags',
                'artist' : artist,
                'api_key' : API_KEY
            }) 
        except:
            continue    
        root = ET.fromstring(xml)
        for i in root.iter('toptags'): 
            try:
                first_tag = list(list(i)[0])[1].text
                print(first_tag)
            except:
                first_tag = 'Unknown'
            if res.get(first_tag):
                res[first_tag] += int(playcount)
            else:
                res[first_tag] = int(playcount)
    return to_json(res)


def to_json(dict_):
    res = []
    for key, val in dict_.items(): 
        res.append({'label' : key, 'y' : val}) 
    return res

if __name__ == '__main__':
    print(get_track_genre(get_track_count('username')))