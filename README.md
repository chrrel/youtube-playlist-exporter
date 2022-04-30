# YouTube Playlist Exporter

This is a python tool for exporting playlists from your YouTube account. It allows to import playlist data from CSV 
files and exports all playlists to a simple, browsable HTML web page as well as a JSON file. 

![Screenshot](screenshot.png)

YouTube data exported via Google Takeout does not contain much information on the videos within a playlist. Therefore, 
this tool uses the *[Invidious](https://invidious.io)* REST API to retrieve additional data on each video (e.g. title, 
duration and thumbnail) and saves this locally. This allows to keep an easy-to-use copy of your YouTube playlist even 
if you delete your YouTube account. Note that the videos are not downloaded.

## Usage
1. Download your YouTube data using [Google Takeout](https://takeout.google.com). 
This will yield a zip file containing CSV files, one for each playlist.
2. Supply all configuration values, especially the path to your CSV files, in `config.cfg`.
3. Execute the script by running `python3 main.py`.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0).

*This project is not endorsed or certified by YouTube / Google LLC.*
