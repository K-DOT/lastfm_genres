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
    res = []
    xml = make_request({
        'method' : 'user.getTopTracks',
        'user' : user,
        'limit' : limit,
        'period' : period,
        'api_key' : API_KEY
    })
    root = ET.fromstring(xml)
    for i in root.iterfind('./toptracks/track'): 
        artist = list(list(i)[6])[0].text
        track = list(i)[0].text
        playcount = list(i)[2].text
        res.append([artist, track, playcount])
    return res

def get_track_genre(tracks):
    res = {}
    for item in tracks:
        artist, track, playcount = item
        try:  
            xml = make_request({
                'method' : 'Track.getInfo',
                'artist' : artist,
                'track' : track,
                'api_key' : API_KEY
            }) 
        except:
            continue    
        root = ET.fromstring(xml)
        for i in root.iter('toptags'): 
            try:
                first_tag = list(list(i)[0])[0].text
                print(first_tag)
            except:
                first_tag = 'Unknown'
            if res.get(first_tag):
                res[first_tag] += int(playcount)
            else:
                res[first_tag] = int(playcount)
    return sorted(res.items(), key=lambda x: x[1], reverse=True)                

if __name__ == '__main__':
    print(get_track_genre(get_track_count()))