import configparser
import csv
import json
import os

import requests

from exporter import playlists_to_html, load_json
from exporter import save_to_json


def get_playlist_from_csv(csv_file_name: str) -> dict:
    with open(csv_file_name, newline='') as csvfile:
        data = csvfile.readlines()
        playlist_meta_data = data[:2]
        playlist_content_data = data[3:]

        playlist = {
            "meta":  list(csv.DictReader(playlist_meta_data, delimiter=','))[0],
            "videos": list(csv.DictReader(playlist_content_data, delimiter=',')),
        }
        return playlist


def get_all_playlists_from_csv(directory_name: str):
    playlists = []
    for file in os.listdir(directory_name):
        if file.endswith(".csv"):
            playlist_path = os.path.join(directory_name, file)
            playlists.append(get_playlist_from_csv(playlist_path))
    return playlists


def get_data_for_video(video_id: str) -> dict:
    params = {
        "fields": "videoId,title,published,publishedText,author,authorId,authorUrl,videoThumbnails,lengthSeconds,error",
        "pretty": 1,
    }
    res = requests.get(f"https://invidio.xamh.de/api/v1/videos/{video_id}", params=params)
    return json.loads(res.text)


def get_data_for_playlists(playlists: list) -> list:
    for playlist in playlists:
        for video in playlist["videos"]:
            video['metadata'] = get_data_for_video(video['Video-ID'])
    return playlists


def main():
    print("### YouTube Data Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    if config["output"].getboolean("retrieve_data"):
        print("[+] Reading CSV files")
        playlists = get_all_playlists_from_csv(config["input"].get("youtube_csv_export_directory"))

        print("[+] Retrieving additional data using Web API")
        playlists = get_data_for_playlists(playlists)

        print("[+] Writing playlist JSON file")
        save_to_json(playlists, config["output"].get("json_output_file"))

    if config["output"].getboolean("export_html"):
        print("[+] Exporting to HTML")
        playlists = load_json(config["output"].get("json_output_file"))
        playlists_to_html(playlists, config["output"].get("html_output_file"))

    print("[+] Finished")


if __name__ == "__main__":
    main()
