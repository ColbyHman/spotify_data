import requests
import os
from dotenv import load_dotenv
import base64

endpoint = "https://api.spotify.com/v1/search/"
load_dotenv()
id = os.environ["id"]
secret = os.environ["secret"]
token = id+":"+secret
token = token.encode("ascii")
token = base64.b64encode(token).decode()
auth = requests.post("https://accounts.spotify.com/api/token", headers={'Content-Type': 'application/x-www-form-urlencoded', "Authorization": "Basic "+token}, params={"grant_type":"client_credentials"})
auth = auth.json()["access_token"]

year = 1930
query = "year:{}".format(year)
type = "artist"
offset = 0
limit = 10

headers = {"Authorization":"Bearer "+auth}
payload = {"q":query, "type":type, "limit":str(limit), "offset":str(offset)}

response = requests.get(endpoint, headers=headers, params=payload)
artists = response.json()["artists"]["items"]

end_of_year = False
# Limit ten per response
while(year <= 2021):
    print("++++++++++++++{}++++++++++++++".format(year))
    end_of_year = False
    while(not end_of_year):
        for i in range(9):
            artist = artists[i]
            if artist:
                name = artist["name"]
                followers = artist["followers"]["total"]
                genres = artist["genres"]
                href = artist["href"]
                popularity = artist["popularity"]
                if artist["images"]:
                    image = artist["images"][0]["url"]
                else:
                    image = None

                print("---------------------")
                print("Name: {}".format(name))
                print("Followers: {}".format(followers))
                print("Genres: {}".format(genres))
                print("URL: {}".format(href))
                print("Popularity: {}".format(popularity))
                if image:
                    print("Image: {}".format(image))
                    with open("images/{0}_{1}.png".format(year,artist["id"]), "wb") as img:
                        image = requests.get(artist["images"][0]["url"])
                        img.write(image.content)
            else:
                end_of_year = True
        offset += 10
        payload = {"q":query, "type":type, "limit":str(limit), "offset":str(offset)}
        artists = requests.get(endpoint, headers=headers, params=payload).json()["artists"]["items"]
print("---------------------")
