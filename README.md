# IranProudCrawler

IranProudCrawler is a Python script designed to detect live TV URLs from IranProud servers and generate an M3U compatible playlist file. This file can be used with various IPTV players, such as IPTV Simple PVR in KODI.

The script automatically creates an `icons` folder and attempts to download channel logos into it.

## Key Features (Post-Refactor)

*   **Python 3:** The script is now written in Python 3.
*   **Uses `requests` library:** For efficient and reliable HTTP requests.
*   **Icon Support:** Downloads channel icons and references them in the M3U file (if your player supports local icons).
*   **Error Handling:** Improved error detection for network issues and file operations.
*   **Automatic Folder Creation:** The `icons` directory is created automatically if it doesn't exist.
*   **M3U Initialization:** The M3U file is properly initialized with `#EXTM3U`.

## Requirements

*   **Python 3:** You must have Python 3 installed. You can check by running `python3 --version`.
*   **`requests` module:** This script depends on the `requests` library.

It is highly recommended to use a Python virtual environment to manage project dependencies. This isolates the project's dependencies from your system-wide Python packages.

**Setting up with a Virtual Environment:**

1.  **Create a virtual environment:**
    Open your terminal in the project directory and run:
    ```bash
    python3 -m venv venv
    ```
    This will create a directory named `venv`.

2.  **Activate the virtual environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    Your terminal prompt should change to indicate that the virtual environment is active.

3.  **Install dependencies:**
    With the virtual environment active, install the `requests` library:
    ```bash
    pip install requests
    ```

4.  **Deactivate (when done):**
    When you're finished working on the project, you can deactivate the virtual environment:
    ```bash
    deactivate
    ```

## How to Run the Script

1.  Ensure you have Python 3 and `requests` installed (preferably in an active virtual environment, see "Requirements").
2.  Navigate to the directory containing `crawler.py`.
3.  Make the script executable (optional, allows running with `./crawler.py`):
    ```bash
    chmod +x crawler.py
    ```
4.  Run the script:
    ```bash
    python3 crawler.py
    ```
    Or, if you made it executable:
    ```bash
    ./crawler.py
    ```
    The script will generate `tvlist.m3u` and populate the `icons` folder.

## Install on OpenElec / KODI

1.  **Install IPTV Simple PVR Add-on:** If not already installed, find and install it from KODI's add-on manager.
2.  **Transfer Files:**
    *   Run the `crawler.py` script on a machine where you can execute Python.
    *   Copy the generated `tvlist.m3u` file and the entire `icons` folder to your OpenElec/KODI device. A common location is the `/storage` directory (e.g., `/storage/tvlist.m3u` and `/storage/icons/`).
3.  **Configure IPTV Simple PVR:**
    *   In KODI, go to Settings -> Add-ons -> My Add-ons -> PVR Clients -> PVR IPTV Simple Client.
    *   Select "Configure".
    *   **General Tab:**
        *   Set "Location" to "Local Path (include Local network)".
        *   Set "M3U Play List Path" to the path where you copied `tvlist.m3u` (e.g., `/storage/tvlist.m3u`).
    *   **Channel Logos Tab:**
        *   Set "Channel Logos" to "Prefer M3U".
        *   *(Alternative, if "Prefer M3U" doesn't work well or for older setups)*: Set "Channel Logos from" to "Local Path" and "Logos Path" to point to your `icons` folder (e.g., `/storage/icons`). The older README mentioned setting "XMLTV Logos Choice" to "Ignore" and configuring a path under TV settings; this might still be relevant for some KODI versions if the IPTV Simple Client logo settings don't behave as expected.
4.  **Enable the Add-on:** If it's not already enabled, enable the IPTV Simple PVR add-on. KODI might prompt you to restart or reload channels.
5.  **Enjoy!**

### Notes on "Whats new in version 1.2" (from original README)

The script has been significantly refactored since v1.2. Here's how those points relate to the current version:

*   **Compatible with OpenElec 6.x:** The script generates a standard M3U file, which should be compatible with any KODI version that supports M3U playlists, including older ones like OpenElec 6.x.
*   **No longer using urllib, we are now using the requests:** This is still true and a core feature.
*   **Support icon! now you can add icons to the channel:** Still true. The script downloads icons.
*   **Fixed a bug in the v1.0 which was not working with IPTV Simple PVR:** The M3U format is standard.
*   **Added the functionality to detect server response timeout:** The `requests` library handles timeouts, and this is configured with `REQUEST_TIMEOUT`.

The "How to add icons" section from the old README provided specific KODI UI steps. These have been integrated into the "Install on OpenElec / KODI" section above, with updates for clarity and modern KODI versions, while also keeping notes for older setups.
The script now automatically creates the `icons` folder, so the manual creation step is no longer needed.
