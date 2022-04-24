import html
import json
import datetime


def playlists_to_html(playlists: list, filepath: str):
    playlists_list = ""
    playlist_content = ""

    for playlist in playlists:
        # Append name to list of playlists
        playlists_list += f"""
        <a href="#{playlist.get("id")}">{playlist.get("title")}</a>
        """

        # Append content
        playlist_content += f"""
        <div class="single-playlist" data-playlistid="{playlist.get("id")}">
            <h2>{playlist.get("title")}</h2>
            <p>{playlist.get("description")}</p>
            {"".join(_video_to_html(video) for video in playlist["videos"])}
        </div>
        """

    _save_to_html_file(playlist_content, playlists_list, filepath)


def _video_to_html(video: dict) -> str:
    data = video["metadata"]
    length = str(datetime.timedelta(seconds=int(data.get("lengthSeconds"))))
    published = datetime.datetime.utcfromtimestamp(data.get("published")).strftime("%d.%m.%Y")
    if data and not data.get("error") and data.get("videoThumbnails"):
        return f"""
        <div class="video">
            <div class="video-thumbnail-container">
                <img width="150" loading="lazy" src="{data.get("videoThumbnails")[4].get("url")}">
                <span class="video-duration">{length}</span>
            </div>
            <div><h3><a href="https://www.youtube.com/watch?v={video.get("id")}">{data.get("title")}</a></h3>
            <h4><a href="https://www.youtube.com{data.get("authorUrl")}">{data.get("author")}</a>, {published}</h4></div>
        </div>
        """
    else:
        return f"""
        <div class="video">
            <img width="150" height="84" style="background-color: #8E8C8C;">
            <div><h3><a href="https://www.youtube.com/watch?v={video.get("id")}">{data.get("error")}</a></h3></div>
        </div>
        """


def _esc(content) -> str:
    return html.escape(str(content))


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
