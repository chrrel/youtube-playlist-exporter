import html
import json


def playlists_to_html(playlists: list, filepath: str):

    playlists_list = ""

    for p in playlists:
        print(p["meta"])
        playlists_list += f"""
            <a href="#{p["meta"]["Playlist-ID"]}">{p["meta"]["Titel"]}</a>
        """

    html_content = ""
    for playlist in playlists:
        html_content += f"<div class='single-playlist' data-playlistid='{playlist['meta']['Playlist-ID']}'><h2>{playlist['meta']['Titel']}</h2>"

        for video in playlist["videos"]:
            data = video['metadata']

            if not data.get('error') and data.get('videoThumbnails'):
                html_content += f"""
                <div class="video">
                <img width="150" loading="lazy" src="{data.get('videoThumbnails')[4].get('url')}">
                <div><h3><a href="https://www.youtube.com/watch?v={video['Video-ID']}">{data.get('title')}</a></h3>
                <h4><a href="https://www.youtube.com{data.get('authorUrl')}">{data.get('author')}</a></h4></div>
                </div>
                """
            else:
                html_content += f"""
                <div class="video">
                <img width="150" height="84" style="background-color: #8E8C8C;">
                <div><h3><a href="https://www.youtube.com/watch?v={video['Video-ID']}">{data.get('error')}</a></h3></div>
                </div>
                """
        html_content += "</div>"
    _save_to_html_file(html_content, playlists_list, filepath)


def _esc(content) -> str:
    return html.escape(str(content))


def _load_file_content(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def save_to_json(data, filepath: str):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_json(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)


def _save_to_html_file(html_content: str, playlists_list: str, filepath: str):
    # Use template as f-string and populate it with data
    js_code = _load_file_content("res/main.js")
    css_code = _load_file_content("res/styles.css")
    # Avoid SyntaxError: f-string must not include a backslash
    template = _load_file_content('res/template.html').replace("\n", "")
    html_output = f"{template}".format(**locals())

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_output)
