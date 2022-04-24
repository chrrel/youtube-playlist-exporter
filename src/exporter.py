import html
import json
import datetime

from string import Template


def playlists_to_html(playlists: list, filepath: str):
    playlists_list = ""
    playlist_content = ""

    for playlist in playlists:
        # Append name to list of playlists
        t = Template('<a href="#$playlist_id">$playlist_title</a>')
        playlists_list += t.substitute(playlist_id=playlist.get("id"), playlist_title=playlist.get("title"))

        # Append content
        t = Template('<div class="single-playlist" data-playlistid="$id"><h2>$title</h2><p>$description</p>$videos</div>')
        playlist_content += t.substitute(
            id=playlist.get("id"),
            title=playlist.get("title"),
            description=playlist.get("description"),
            videos="".join(_video_to_html(video) for video in playlist["videos"]),
        )

    _save_to_html_file(playlist_content, playlists_list, filepath)


def _video_to_html(video: dict) -> str:
    data = video["metadata"]

    video_template = f"""
        <div class="video">
            <div class="video-thumbnail-container">
                <img width="150" loading="lazy" src="$thumbnail">
                <span class="video-duration">$length</span>
            </div>
            <div><h3><a href="https://www.youtube.com/watch?v=$video_id">$title</a></h3>
            <h4><a href="https://www.youtube.com$author_url">$author</a> $published</h4></div>
        </div>
        """
    t = Template(video_template)

    if data and not data.get("error") and data.get("videoThumbnails"):
        return t.substitute(
            thumbnail=data.get("videoThumbnails")[4].get("url"),
            length=str(datetime.timedelta(seconds=int(data.get("lengthSeconds")))),
            video_id=video.get("id"),
            title=data.get("title"),
            author_url=data.get("authorUrl"),
            author=data.get("author"),
            published=", " + datetime.datetime.utcfromtimestamp(data.get("published")).strftime("%d.%m.%Y")
        )
    else:
        return t.substitute(
            thumbnail="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
            length="0",
            video_id=video.get("id"),
            title=data.get("error"),
            author_url="",
            author="",
            published=""
        )


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
