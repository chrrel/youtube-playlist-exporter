import datetime
import html
from string import Template

from utils import save_to_html_file


class HtmlExporter:
    video_link_base_url = ""

    def __init__(self, video_link_base_url: str):
        self.video_link_base_url = video_link_base_url

    def playlists_to_html(self, playlists: list, filepath: str) -> None:
        playlists_list = ""
        playlist_content = ""

        playlists = sorted(playlists, key=lambda d: d['time_updated'], reverse=True)
        for playlist in playlists:
            # Append name to list of playlists
            t = Template('<a href="#$playlist_id">$playlist_title</a>')
            playlists_list += t.substitute(playlist_id=playlist.get("id"), playlist_title=playlist.get("title"))

            # Append content
            t = Template("""
                <div class="single-playlist" data-playlistid="$id">
                    <h2>$title</h2>
                    <a class="watch-playlist-link" href="$watch_link" title="First 50 videos only">Watch playlist</a>
                    <p class="clear">$videos_count<br>$description</p>
                    $videos
                </div>
            """)
            youtube_link = f"{self.video_link_base_url}/watch_videos?video_ids=" + ",".join(v["id"] for v in playlist["videos"])
            playlist_content += t.substitute(
                id=self._esc(playlist.get("id")),
                title=self._esc(playlist.get("title")),
                description=self._esc(playlist.get("description")),
                videos_count=self._esc(f"{len(playlist['videos'])} videos"),
                watch_link=self._esc(youtube_link),
                videos="".join(self._video_to_html(video) for video in playlist["videos"]),
            )

        save_to_html_file(playlist_content, playlists_list, filepath)

    def _video_to_html(self, video: dict) -> str:
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
        data = video["metadata"]
        if data and not data.get("error"):
            return t.substitute(
                thumbnail=self._esc(data.get("videoThumbnails")[4].get("url")),
                length=self._esc(datetime.timedelta(seconds=int(data.get("lengthSeconds")))),
                video_url=f"{self.video_link_base_url}/watch?v={self._esc(video.get('id'))}",
                title=self._esc(data.get("title")),
                author_url=f"{self.video_link_base_url}{self._esc(video.get('authorUrl'))}",
                author=self._esc(data.get("author")),
                published=self._esc(", " + datetime.datetime.utcfromtimestamp(data.get("published")).strftime("%d.%m.%Y"))
            )
        else:
            return t.substitute(
                thumbnail="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
                length="0",
                video_url=f"{self.video_link_base_url}/watch?v={self._esc(video.get('id'))}",
                title=self._esc(data.get("error")),
                author_url="",
                author="",
                published=""
            )

    @staticmethod
    def _esc(content) -> str:
        return html.escape(str(content))
