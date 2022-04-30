import json
import logging

import requests


class InvidiousApi:
    base_url = ""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_data_for_video(self, video_id: str) -> dict:
        params = {
            "fields": "videoId,title,published,author,authorId,authorUrl,videoThumbnails,lengthSeconds,error",
            "pretty": 1,
        }
        try:
            res = requests.get(f"{self.base_url}/api/v1/videos/{video_id}", params=params)
            return json.loads(res.text)
        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    def get_data_for_playlists(self, playlists: list) -> list:
        for playlist in playlists:
            for video in playlist["videos"]:
                logging.debug(f"Retrieving data for {video['id']}")
                video["metadata"] = self.get_data_for_video(video["id"])
        return playlists
