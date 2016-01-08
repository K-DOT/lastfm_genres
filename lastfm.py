import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

class LastFMError(Exception):
    pass
        
def errors(xml):
    root = ET.fromstring(xml)
    for i in root.iter('error'):
        return i.text
    return None    

def make_request(params):
    url_params = urllib.parse.urlencode(params)
    url = 'http://ws.audioscrobbler.com/2.0/?%s' % url_params
    try:
        return urllib.request.urlopen(url).read().decode('utf-8')
    except urllib.request.HTTPError as error:
        return error.read()

def get_track_count(user, limit='500', period='7days'):
    res = []
    xml = make_request({
        'method' : 'user.getTopArtists',
        'user' : user,
        'limit' : limit,
        'period' : period,
        'api_key' : API_KEY
    })
    error = errors(xml)
    if not error:
        root = ET.fromstring(xml)
        for i in root.iterfind('./topartists/artist'): 
            artist = list(i)[0].text
            playcount = list(i)[1].text
            res.append([artist, playcount])
        return res
    raise LastFMError(error)    

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
    try:
        count = get_track_count('username')
    except LastFMError as e:
        print(e)
    else:
        print(get_track_genre(count))  