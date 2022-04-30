import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from requests import adapters


class InvidiousApi:
    base_url = ""
    session = None

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.mount("https://", requests.adapters.HTTPAdapter(pool_maxsize=24, max_retries=3, pool_block=True))

    def get_data_for_video(self, video_id: str) -> dict:
        params = {
            "fields": "videoId,title,published,author,authorId,authorUrl,videoThumbnails,lengthSeconds,error",
            "pretty": 1,
        }
        try:
            logging.info(f"Retrieving data for {video_id}")
            # Make requests using a session in order to reuse connections
            res = self.session.get(f"{self.base_url}/api/v1/videos/{video_id}", params=params)
            if 501 <= res.status_code < 600:
                # Take a break as sever might be overloaded. Start at 501 since the API uses 500 e.g. for private videos
                time.sleep(5)
            data = json.loads(res.text)
            # The response has to contain the videoId, so add it in case it does not exist
            if "videoId" not in data:
                data["videoId"] = video_id
            return data
        except Exception as e:
            logging.error(e)
            return {"videoId": video_id, "error": str(e)}

    def get_data_for_playlists(self, playlists: list) -> list:
        # Get a list of all videos and remove duplicates in order to minimize API requests
        video_ids = [video["id"] for playlist in playlists for video in playlist["videos"]]
        video_ids_unique = list(set(video_ids))
        logging.info(f"Found {len(video_ids)} in total. Of these, {len(video_ids_unique)} are unique.")

        # Create a dictionary containing data retrieved from the API for all videos
        videos_data = {}
        with ThreadPoolExecutor(max_workers=24) as executor:
            # Wrap in a list() to wait for all requests to complete
            for video_data in list(executor.map(self.get_data_for_video, video_ids_unique)):
                videos_data[video_data['videoId']] = video_data

        # Use the retrieved data to augment all playlists with the additional data
        for playlist in playlists:
            for video in playlist["videos"]:
                video["metadata"] = videos_data.get(video["id"])
        return playlists
