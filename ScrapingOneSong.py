import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0' }

songname = []
artist = []
year = []
sample = []
genre = []
links = []

for i in tqdm(range(1,24)):
    url = "http://www.whosampled.com/James-Brown/The-Payback/sampled/?cp={}".format(i)
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, "lxml")
    g_data = soup.find_all("div", {"class": "listEntry sampleEntry"})
    for item in g_data:
        songname.append(item.contents[3].find("a", {'class', 'trackName playIcon'}).text) #songname
        artist.append(item.contents[3].find("span", {'class', 'trackArtist'}).text[3:-10]) #artistname
        year.append(item.contents[3].find("span", {'class', 'trackArtist'}).text[-8:-4]) #year
        sample.append(item.contents[3].find("span", {'class', 'topItem'}).text)#what was sampled
        genre.append(item.contents[3].find("span", {'class', 'bottomItem'}).text) #genre
        link = "http://www.whosampled.com/"+ item.contents[1].get('href')
        links.append(link)



jsonfile = "songs.json"


def main():
	# Create the list of dicts
	lotteryData = song_data()

	# JSON EXAMPLE BEGINS HERE

	with open(jsonfile, 'w') as outputFile:
		json.dump(lotteryData, outputFile)

	#
	# Print statement if its done
	print("created lottery numbers for %d months" % (len(lotteryData)))
count = 0
def song_data():
    global count
    songinfo = []
    for song in songname:
        random_dict = {}
    	random_dict['song'] = songname[count]
    	random_dict['artist'] = artist[count]
    	random_dict['year'] = year[count]
        random_dict['sample'] = sample[count]
    	random_dict['genre'] = genre[count]
        random_dict['link'] = links[count]
    	songinfo.append(random_dict)
        count += 1
    return songinfo
# Helper functions to create a series of random numbers

if __name__ == '__main__':
	main()
