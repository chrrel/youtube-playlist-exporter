import configparser
import glob

from exporter import playlists_to_html
from utils import save_to_json, load_json, get_playlist_from_csv
from Invidiousapi import InvidiousApi


def main():
    print("### YouTube Data Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    if config["output"].getboolean("retrieve_data"):
        print("[+] Reading CSV files")
        directory_name = config["input"].get("youtube_csv_export_directory")
        playlist_file_paths = glob.glob(f"{directory_name}/*.csv")
        playlists = [get_playlist_from_csv(playlist_path) for playlist_path in playlist_file_paths]

        print("[+] Retrieving additional data using Invidious API")
        invidious = InvidiousApi(config["input"].get("invidious_api_base_url"))
        playlists = invidious.get_data_for_playlists(playlists)

        print("[+] Writing playlist JSON file")
        save_to_json(playlists, config["output"].get("json_output_file"))

    if config["output"].getboolean("export_html"):
        print("[+] Exporting JSON data to HTML")
        playlists = load_json(config["output"].get("json_output_file"))
        playlists_to_html(playlists, config["output"].get("html_output_file"))

    print("[+] Finished")


if __name__ == "__main__":
    main()
