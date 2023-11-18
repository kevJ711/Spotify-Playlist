import json
import requests
from secrets import user_name, token, createplaylist
from datetime import date
from refresh import Refresh


class GetSongs:
    def __init__(self):
        self.user_name = user_name
        self.token = token
        self.createplaylist = createplaylist
        self.tracks = ""
        self.updated_playlist = ""
        
    def get_song(self):
            
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            createplaylist)

        response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.token)})

        response_json = response.json()

        print(response)
        
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]
        
        self.add_to_playlist()

        

    def create_playlist(self):
  
            # Create a new playlist
        print("Trying to create playlist...")
        today = date.today()

        todayFormatted = today.strftime("%m/%d/%Y")
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
        user_name)

        request_body = json.dumps({
            "name": " My recommendation playlist for the week of: " + todayFormatted, "description": "Playlist made for: " + user_name, "public": True
        })

        response = requests.post(query, data=request_body, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.token)
        })

        response_json = response.json()

        return response_json["id"]
        
    def add_to_playlist(self):
        # add all songs to new playlist
        print("Adding songs...")

        self.updated_playlist = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.updated_playlist, self.tracks)

        response = requests.post(query, headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.token)})
        print(response.json)
        
    def call_refresh(self):

        print("Refreshing token")

        refreshCaller = Refresh()

        self.token = refreshCaller.refresh()

        self.get_song()

a = GetSongs()
a.call_refresh()

