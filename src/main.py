import configparser
import csv
import requests
import json
import os

from exporter import playlists_to_html
from exporter import save_to_json
import exporter


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
    res = requests.get(f"https://invidio.xamh.de/api/v1/videos/{video_id}?fields=videoId,title,published,publishedText,author,authorId,authorUrl,videoThumbnails,lengthSeconds,error&pretty=1")
    return json.loads(res.text)


def get_data_for_playlist(playlist: dict) -> dict:
    for video in playlist["videos"]:
        video['metadata'] = get_data_for_video(video['Video-ID'])
    return playlist


def main():
    print("### YouTube Data Exporter ###")
    playlists = get_all_playlists_from_csv("../data/playlists")
    load_data = False
    if load_data:
        for playlist in playlists:
            playlist = get_data_for_playlist(playlist)
        save_to_json(playlists, "../output/playlists.json")


    playlists = exporter.load_json("../output/playlists.json")

    playlists_to_html(playlists, "../output/youtube.html")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    print("[+] Reading Database")
    if config["input"].getboolean("use_wa_db"):
       pass

    if config["output"].getboolean("export_html"):
        print("[+] Exporting to HTML")

    print("[+] Finished")


if __name__ == "__main__":
    main()
