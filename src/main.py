import configparser
import glob
import time
import logging

from Invidiousapi import InvidiousApi
from HtmlExporter import HtmlExporter
from utils import save_to_json, load_json, get_playlist_from_csv


def main():
    print("### YouTube Data Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    retrieve_data = config["output"].getboolean("retrieve_data")
    export_html = config["output"].getboolean("export_html")
    invidious_api_base_url = config["input"].get("invidious_api_base_url")
    csv_directory_name = config["input"].get("youtube_csv_export_directory")
    json_output_file = config['output'].get('json_output_file')
    html_output_file = config["output"].get("html_output_file")
    video_link_base_url = config["output"].get("video_link_base_url")

    if retrieve_data:
        print("[+] Reading CSV files")
        playlist_file_paths = glob.glob(f"{csv_directory_name}/*.csv")
        playlists = [get_playlist_from_csv(playlist_path) for playlist_path in playlist_file_paths]

        print("[+] Retrieving additional data using Invidious API")
        start_time = time.time()
        invidious = InvidiousApi(invidious_api_base_url)
        playlists = invidious.get_data_for_playlists(playlists)
        print(f"[+] Downloaded data for {len(playlists)} playlists in {time.time() - start_time} seconds")

        print("[+] Writing playlist JSON file")
        save_to_json(playlists, json_output_file)
    if export_html:
        print("[+] Exporting JSON data to HTML")
        playlists = load_json(json_output_file)
        exporter = HtmlExporter(video_link_base_url)
        exporter.playlists_to_html(playlists, html_output_file)

    print("[+] Finished")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
