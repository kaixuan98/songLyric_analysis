import requests
from bs4 import BeautifulSoup
import csv 
import re 


URLROOT = "https://www.mulanci.org/lyric/"
WEBSITE = "https://www.mulanci.org"

# get a list of all the song's id 
songs_with_ids =[]

# Get all the song and the lyrics url from the artist page
def scrape_song_url(artist_id):
    URL = URLROOT + artist_id
    res = requests.get(URL)
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.findAll("div" , {"class":"col-sm-6 col-12 pt-1 pb-1"})
    for songs in table:
        song = {}
        title = "".join(filter(lambda x: not x.isdigit(), (songs.a.text.strip()))) 
        clean_title = re.sub(r'[^\w\s]', '', title) 
        song['song_title'] = clean_title.strip()
        song['song_url'] = WEBSITE + songs.a['href']
        songs_with_ids.append(song)
    return table

# create a csv to hold the song list  
def create_csv():
    filename = '薛之谦歌单.csv'
    with open(filename,'w',newline='') as f : 
        w = csv.DictWriter(f,['song_title','song_url'])
        w.writeheader()
        for song in songs_with_ids:
            w.writerow(song)
    return filename

# get the song_lyrics with the input of the song title and song url
def get_song_lyrics(song_title, song_url):
    res = requests.get(song_url)
    soup = BeautifulSoup(res.content , 'html5lib')
    lyrics_raw = soup.find("div" , {"id" : "lyric-content"})
    lyrics = re.sub('\s{2,}', ' ',lyrics_raw.text)
    lyrics = lyrics.replace("(adsbygoogle = window.adsbygoogle || []).push({});" , " ")
    print(lyrics)
    return lyrics


# One of my testing singer 
singer_id = "s7869/"
scrape_song_url(singer_id)
create_csv()
for song in songs_with_ids:
    song_list = list(song.values())
    get_song_lyrics(song_list[0], song_list[1])



