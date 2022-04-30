import configparser
import glob
import time

from Invidiousapi import InvidiousApi
from exporter import playlists_to_html
from utils import save_to_json, load_json, get_playlist_from_csv


def main():
    print("### YouTube Data Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    retrieve_data = config["output"].getboolean("retrieve_data")
    export_html = config["output"].getboolean("export_html")
    csv_directory_name = config["input"].get("youtube_csv_export_directory")
    json_output_directory = config['output'].get('json_output_directory')
    html_output_file = config["output"].get("html_output_file")
    invidious_api_base_url = config["input"].get("invidious_api_base_url")

    if retrieve_data:
        print("[+] Reading CSV files")
        playlist_file_paths = glob.glob(f"{csv_directory_name}/*.csv")
        playlists = [get_playlist_from_csv(playlist_path) for playlist_path in playlist_file_paths]

        print("[+] Retrieving additional data using Invidious API")
        start_time = time.time()
        invidious = InvidiousApi(invidious_api_base_url)
        playlists = invidious.get_data_for_playlists(playlists)
        print(f"[+] Downloaded data for {len(playlists)} playlists in {time.time() - start_time} seconds")

        print("[+] Writing playlist JSON files")
        for playlist in playlists:
            save_to_json(playlist, f"{json_output_directory}/{playlist['id']}.json")

    if export_html:
        print("[+] Exporting JSON data to HTML")
        playlist_json_file_paths = glob.glob(f"{json_output_directory}/*.json")
        playlists = [load_json(playlist_path) for playlist_path in playlist_json_file_paths]
        playlists_to_html(playlists, html_output_file)

    print("[+] Finished")


if __name__ == "__main__":
    main()
