#!/usr/bin/env python3
# IranProud Crawler
# Description: This script crawls the IranProud website to detect live TV channel URLs
# and their corresponding logos. It then generates an M3U playlist file compatible
# with IPTV players and saves channel icons to a local directory.
# Original Author: Ali Abbasi
# Refactored: AI Agent for Google VRP
# Version: 2.0 (Post-Refactor)

import requests
import re
import os
import sys

# Constants
BASE_URL = "http://www.iranproud.com"
LIVE_TV_URL = f"{BASE_URL}/livetv"
OUTPUT_M3U_FILE = "tvlist.m3u"
ICONS_DIR = "icons/"
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2015092817 Firefox/3.0.3'
ICON_EXTENSION = ".png"
REQUEST_TIMEOUT = 10  # Default timeout for HTTP requests in seconds
M3U_TEXT_PREFIX = "#EXTINF:-1," # Standard M3U info tag prefix

def fetch_html_content(url, headers, timeout, is_critical=False):
    """
    Fetches HTML content from a given URL.

    Args:
        url (str): The URL to fetch content from.
        headers (dict): HTTP headers to use for the request.
        timeout (int): Request timeout in seconds.
        is_critical (bool): If True and fetching fails, the script will exit.

    Returns:
        str: The HTML content as text if successful, None otherwise.
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.Timeout as e:
        print(f"Timeout error fetching URL {url}: {e}", file=sys.stderr)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching URL {url}: {e}", file=sys.stderr)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching URL {url}: {e} - Status Code: {e.response.status_code}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"Generic error fetching URL {url}: {e}", file=sys.stderr)
    
    if is_critical:
        print(f"Critical error: Could not fetch essential data from {url}. Exiting.", file=sys.stderr)
        sys.exit(1)
    return None

def parse_main_page_channels(html_content):
    """
    Parses the main Live TV page HTML to find channel links and logo URLs.

    Args:
        html_content (str): The HTML content of the main Live TV page.

    Returns:
        list: A list of tuples, where each tuple contains (channel_path, logo_url).
              Returns an empty list if no channels are found or html_content is None.
    """
    if not html_content:
        return []
    # Regex to find list items containing channel links and image sources
    return re.compile('<li><a href="(.+?)" target="_parent".+?src="(.+?)" .+?').findall(html_content)

# The function `parse_channel_page_video_source` was previously commented out as
# the logic was directly embedded in the main loop using `re.compile(...).findall()`.
# This approach is retained as it directly gets all video URLs if a channel page
# were to list multiple. If only one video source is expected or desired,
# using .search() and .group(1) as in a dedicated function would be an alternative.

def download_icon(icon_url, icon_path, headers, timeout):
    """
    Downloads a channel icon from a given URL and saves it to a specified path.

    Args:
        icon_url (str): The URL of the icon to download.
        icon_path (str): The local file path to save the icon.
        headers (dict): HTTP headers for the request.
        timeout (int): Request timeout in seconds.

    Returns:
        bool: True if the icon was successfully downloaded and saved, False otherwise.
    """
    try:
        logo_response = requests.get(icon_url, stream=True, timeout=timeout)
        logo_response.raise_for_status()
        with open(icon_path, 'wb') as icon_file:
            for block in logo_response.iter_content(1024): # Read in chunks
                icon_file.write(block)
        print(f"Saved icon: {icon_path}")
        return True
    except requests.exceptions.Timeout:
        print(f"Timeout downloading icon {icon_url}", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print(f"Connection error downloading icon {icon_url}", file=sys.stderr)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error downloading icon {icon_url}: {e.response.status_code}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading icon {icon_url}: {e}", file=sys.stderr)
    except (IOError, OSError) as e: # Catch file system errors
        print(f"Error saving icon {icon_path}: {e}", file=sys.stderr)
    return False

def append_to_m3u(file_path, channel_name, video_url):
    """
    Appends a channel entry to the M3U playlist file.

    Args:
        file_path (str): The path to the M3U file.
        channel_name (str): The name of the channel.
        video_url (str): The URL of the video stream.

    Returns:
        bool: True if the entry was successfully appended, False otherwise.
    """
    try:
        with open(file_path, "a", encoding='utf-8') as m3u_file:
            m3u_file.write(f"{M3U_TEXT_PREFIX}{channel_name}\n")
            m3u_file.write(f"{video_url}\n")
            m3u_file.write("\n") # Extra newline for readability between entries
        return True
    except (IOError, OSError) as e:
        print(f"Error writing to M3U file {file_path}: {e}", file=sys.stderr)
        return False

def initialize_m3u_file(file_path):
    """
    Initializes the M3U file by writing the #EXTM3U header.
    This will overwrite the file if it already exists.

    Args:
        file_path (str): The path to the M3U file.

    Returns:
        bool: True if the file was successfully initialized, False otherwise.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('#EXTM3U\n') # Standard M3U header
            output_file.write('\n') # Blank line after header
        return True
    except (IOError, OSError) as e:
        print(f"CRITICAL: Error initializing M3U file {file_path}: {e}", file=sys.stderr)
        return False

def main():
    """
    Main function to run the IranProud crawler.
    It fetches channel information, downloads icons, and creates an M3U playlist.
    """
    print("Starting IranProud Crawler...")
    
    try:
        # Create the icons directory if it doesn't already exist.
        # exist_ok=True means it won't raise an error if the directory already exists.
        os.makedirs(ICONS_DIR, exist_ok=True)
    except OSError as e:
        print(f"CRITICAL: Could not create icons directory {ICONS_DIR}: {e}", file=sys.stderr)
        sys.exit(1)

    headers = {'User-Agent': USER_AGENT}

    if not initialize_m3u_file(OUTPUT_M3U_FILE):
        sys.exit(1) # Critical error, cannot proceed without M3U file

    print(f"Fetching main page: {LIVE_TV_URL}")
    # Fetching the main page is critical; script exits if this fails.
    main_page_content = fetch_html_content(LIVE_TV_URL, headers, REQUEST_TIMEOUT, is_critical=True)
    
    # This check is technically redundant if is_critical=True causes sys.exit in fetch_html_content,
    # but kept for clarity in case is_critical behavior changes or for robustness.
    if not main_page_content:
        print("Could not fetch main page content. Exiting.", file=sys.stderr) # Should have already exited
        sys.exit(1)

    channel_entries = parse_main_page_channels(main_page_content)
    channel_count = len(channel_entries)

    if channel_count == 0:
        print("No channels found on the main page. Exiting.")
        return # Normal exit if no channels, not necessarily an error.

    print(f"Detected {channel_count} channel(s) on the main page.")

    processed_channels_count = 0
    for channel_path, logo_url in channel_entries:
        # Default channel name for logging in case parsing fails later
        channel_name_for_print = "Unknown"
        channel_full_url = BASE_URL + channel_path
        print(f"Processing channel: {channel_full_url}")

        channel_page_content = fetch_html_content(channel_full_url, headers, REQUEST_TIMEOUT)
        if not channel_page_content:
            print(f"Skipping channel {channel_path} due to fetch error on its page.", file=sys.stderr)
            continue

        # Regex to find all video source URLs on the channel page.
        # A channel page might theoretically have multiple stream links.
        video_urls = re.compile('.+? videosrc="(.+?)".+?').findall(channel_page_content)

        if not video_urls:
            print(f"No video source found for channel {channel_path}. Skipping.", file=sys.stderr)
            continue
            
        for video_url in video_urls:
            try:
                # Extract channel name from the video URL (last part of path, before extension)
                channel_name = video_url.split("/")[-1].split(".")[0]
                channel_name_for_print = channel_name # Update for logging
            except IndexError:
                # This can happen if the URL format is unexpected.
                print(f"Could not determine channel name from video URL: {video_url}. Skipping this video URL.", file=sys.stderr)
                continue

            print(f"  Channel Name: {channel_name}")
            print(f"  Video URL: {video_url}")
            print(f"  Logo URL: {logo_url}")

            icon_filename = os.path.join(ICONS_DIR, f"{channel_name}{ICON_EXTENSION}")
            # download_icon handles its own errors and returns True/False
            download_icon(logo_url, icon_filename, headers, REQUEST_TIMEOUT) 
            
            # append_to_m3u handles its own errors and returns True/False
            if not append_to_m3u(OUTPUT_M3U_FILE, channel_name, video_url):
                # Log failure but continue processing other video URLs or channels.
                # Depending on requirements, this could be a critical error.
                print(f"Failed to write channel {channel_name} to M3U. Continuing...", file=sys.stderr)
        
        processed_channels_count += 1
        print(f"Processed channel {processed_channels_count}/{channel_count}: {channel_name_for_print}")

    print("Finished processing all channels.")

if __name__ == "__main__":
    main()
