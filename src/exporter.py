import datetime
import html
from string import Template

from utils import save_to_html_file


def playlists_to_html(playlists: list, filepath: str) -> None:
    playlists_list = ""
    playlist_content = ""

    for playlist in playlists:
        # Append name to list of playlists
        t = Template('<a href="#$playlist_id">$playlist_title</a>')
        playlists_list += t.substitute(playlist_id=playlist.get("id"), playlist_title=playlist.get("title"))

        # Append content
        t = Template("""
            <div class="single-playlist" data-playlistid="$id">
                <h2>$title</h2>
                <a class="yt-playlist-link" href="$youtube_link" title="First 50 videos only">Watch on YouTube</a>
                <p class="clear">$videos_count<br>$description</p>
                $videos
            </div>
        """)
        youtube_link = "https://www.youtube.com/watch_videos?video_ids=" + ",".join(v["id"] for v in playlist["videos"])
        playlist_content += t.substitute(
            id=_esc(playlist.get("id")),
            title=_esc(playlist.get("title")),
            description=_esc(playlist.get("description")),
            videos_count=_esc(f"{len(playlist['videos'])} videos"),
            youtube_link=_esc(youtube_link),
            videos="".join(_video_to_html(video) for video in playlist["videos"]),
        )

    save_to_html_file(playlist_content, playlists_list, filepath)


def _video_to_html(video: dict) -> str:
    data = video["metadata"]

    t = Template(f"""
        <div class="video">
            <div class="video-thumbnail-container">
                <a href="$video_url"><img width="150" loading="lazy" src="$thumbnail"></a>
                <span class="video-duration">$length</span>
            </div>
            <div>
                <h3><a href="$video_url">$title</a></h3>
                <h4><a href="$author_url">$author</a>$published</h4>
            </div>
        </div>
        """)
    if data and not data.get("error"):
        return t.substitute(
            thumbnail=_esc(data.get("videoThumbnails")[4].get("url")),
            length=_esc(datetime.timedelta(seconds=int(data.get("lengthSeconds")))),
            video_url="https://www.youtube.com/watch?v=" + _esc(video.get("id")),
            title=_esc(data.get("title")),
            author_url="https://www.youtube.com" + _esc(data.get("authorUrl")),
            author=_esc(data.get("author")),
            published=_esc(", " + datetime.datetime.utcfromtimestamp(data.get("published")).strftime("%d.%m.%Y"))
        )
    else:
        return t.substitute(
            thumbnail="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
            length="0",
            video_url="https://www.youtube.com/watch?v=" + _esc(video.get("id")),
            title=_esc(data.get("error")),
            author_url="",
            author="",
            published=""
        )


def _esc(content) -> str:
    return html.escape(str(content))
