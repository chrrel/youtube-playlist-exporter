import configparser
import csv
import glob
import json
import logging

import requests

from exporter import playlists_to_html, load_json
from exporter import save_to_json


class InvidiousApi:
    base_url = ""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_data_for_video(self, video_id: str) -> dict:
        params = {
            "fields": "videoId,title,published,publishedText,author,authorId,authorUrl,videoThumbnails,lengthSeconds,error",
            "pretty": 1,
        }
        try:
            res = requests.get(f"{self.base_url}/api/v1/videos/{video_id}", params=params)
            logging.info(res.text)
            return json.loads(res.text)
        except Exception as e:
            logging.error(e)
            return {"error": str(e)}

    def get_data_for_playlists(self, playlists: list) -> list:
        for playlist in playlists:
            for video in playlist["videos"]:
                video["metadata"] = self.get_data_for_video(video["id"])
        return playlists


def get_playlist_from_csv(csv_file_name: str) -> dict:
    with open(csv_file_name, encoding="utf-8", newline="") as csvfile:
        data = csvfile.readlines()
        metadata = list(csv.reader(data[1:2], delimiter=","))[0]
        playlist_content_data = list(csv.reader(data[4:], delimiter=","))

        playlist = {
            "id": metadata[0],
            "channel_id": metadata[1],
            "time_updated": metadata[2],
            "time_created": metadata[3],
            "title": metadata[4],
            "description": metadata[5],
            "visibility": metadata[6],
            "videos": [{"id": video[0], "time_added": video[1]} for video in playlist_content_data if len(video) > 1],
        }
        return playlist


def main():
    print("### YouTube Data Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    if config["output"].getboolean("retrieve_data"):
        print("[+] Reading CSV files")

        # Get all playlists from CSV files
        directory_name = config["input"].get("youtube_csv_export_directory")
        playlist_file_paths = glob.glob(f"{directory_name}/*.csv")
        playlists = [get_playlist_from_csv(playlist_path) for playlist_path in playlist_file_paths]

        print("[+] Retrieving additional data using Invidious API")
        invidious = InvidiousApi(config["input"].get("invidious_api_base_url"))
        playlists = invidious.get_data_for_playlists(playlists)

        print("[+] Writing playlist JSON file")
        save_to_json(playlists, config["output"].get("json_output_file"))

    if config["output"].getboolean("export_html"):
        print("[+] Exporting to HTML")
        playlists = load_json(config["output"].get("json_output_file"))
        playlists_to_html(playlists, config["output"].get("html_output_file"))

    print("[+] Finished")


if __name__ == "__main__":
    main()
