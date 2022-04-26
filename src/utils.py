import csv
import json


def _load_file_content(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def save_to_json(data, filepath: str):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def _save_to_html_file(playlist_content: str, playlists_list: str, filepath: str):
    # Use template as f-string and populate it with data
    js_code = _load_file_content("res/main.js")
    css_code = _load_file_content("res/styles.css")
    # Avoid SyntaxError: f-string must not include a backslash
    template = _load_file_content("res/template.html").replace("\n", "")
    html_output = f"{template}".format(**locals())

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_output)


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
