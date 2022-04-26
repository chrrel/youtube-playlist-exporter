import html
import datetime

from string import Template

from utils import _save_to_html_file


def playlists_to_html(playlists: list, filepath: str) -> None:
    playlists_list = ""
    playlist_content = ""

    for playlist in playlists:
        # Append name to list of playlists
        t = Template('<a href="#$playlist_id">$playlist_title</a>')
        playlists_list += t.substitute(playlist_id=playlist.get("id"), playlist_title=playlist.get("title"))

        # Append content
        t = Template('<div class="single-playlist" data-playlistid="$id"><h2>$title</h2><p>$description</p>$videos</div>')
        playlist_content += t.substitute(
            id=_esc(playlist.get("id")),
            title=_esc(playlist.get("title")),
            description=_esc(playlist.get("description")),
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

    if data and not data.get("error"):
        return t.substitute(
            thumbnail=_esc(data.get("videoThumbnails")[4].get("url")),
            length=_esc(datetime.timedelta(seconds=int(data.get("lengthSeconds")))),
            video_id=_esc(video.get("id")),
            title=_esc(data.get("title")),
            author_url=_esc(data.get("authorUrl")),
            author=_esc(data.get("author")),
            published=_esc(", " + datetime.datetime.utcfromtimestamp(data.get("published")).strftime("%d.%m.%Y"))
        )
    else:
        return t.substitute(
            thumbnail="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
            length="0",
            video_id=_esc(video.get("id")),
            title=_esc(data.get("error")),
            author_url="",
            author="",
            published=""
        )


def _esc(content) -> str:
    return html.escape(str(content))
