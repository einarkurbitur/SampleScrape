import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}


url = "http://www.whosampled.com/James-Brown/The-Payback/sampled/"



def childlink(songname, artistname):
    songname = songname.replace(' ', '-')
    artistname = artistname.replace(' ', '-')
    if "feat" in artistname:
        artistname = artistname.rpartition('-feat')[0]

    child_link = "http://www.whosampled.com/" + \
        songname + "/" + artistname + "/sampled"
    return child_link


def scrape(website):
    children = []
    links = []
    shouldBreak = False

    for i in tqdm(range(1, 50)):  # the number of pages for that song
        url = website + "?cp={}".format(i)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            # the div with all the sampled songs
            g_data = soup.find_all("div", {"class": "listEntry sampleEntry"})
            for item in g_data:
                link = "http://www.whosampled.com/" + item.contents[1].get('href') #links
                if any(link in l for l in links):
                    shouldBreak = True
                    break
                links.append(link)

                song = item.contents[3].find(
                    "a", {'class', 'trackName playIcon'}).text

                artistname = item.contents[3].find(
                    "span", {'class', 'trackArtist'}).text[3:-10]

                yearnumber = item.contents[3].find(
                    "span", {'class', 'trackArtist'}).text[-8:-4]

                sampletype = item.contents[3].find(
                    "span", {'class', 'topItem'}).text

                genretype = item.contents[3].find(
                    "span", {'class', 'bottomItem'}).text



                random_dict = {}
                random_dict['song'] = song
                random_dict['artist'] = artistname
                random_dict['year'] = yearnumber
                random_dict['sample'] = sampletype
                random_dict['genre'] = genretype
                random_dict['link'] = childlink(song, artistname)
                children.append(random_dict)
        if shouldBreak:
            break
    return children

def scrape_rec(url):
    childlist = scrape(url)
    newlist = []
    for c in childlist:
        c['children'] = scrape_rec(c['link'])
        newlist.append(c)
    return newlist


def main():
    jsonfile = "songschildren.json"
    data = scrape_rec("http://www.whosampled.com/James-Brown/The-Payback/sampled/")
    print data
    with open(jsonfile, 'w') as outputFile:
        json.dump(data, outputFile)




if __name__ == '__main__':
    main()
