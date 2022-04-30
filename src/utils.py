import csv
import json
from string import Template


def _load_file_content(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def _write_file_content(data: str, filepath: str):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(data)


def save_to_json(data, filepath: str):
    _write_file_content(json.dumps(data), filepath)


def load_json(filepath: str):
    return json.loads(_load_file_content(filepath))


def save_to_html_file(playlist_content: str, playlists_list: str, filepath: str):
    t = Template(_load_file_content("res/template.html"))
    html_output = t.substitute(
        js_code=_load_file_content("res/main.js"),
        css_code=_load_file_content("res/styles.css"),
        playlist_content=playlist_content,
        playlists_list=playlists_list,
    )
    _write_file_content(html_output, filepath)


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
