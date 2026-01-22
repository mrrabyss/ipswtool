import requests
import json
import os
import sys
import tqdm
import argparse
from simple_term_menu import TerminalMenu
banner = """
 _ ____  ______        _______           _ 
(_)  _ \\/ ___\\ \\      / /_   _|__   ___ | |
| | |_) \\___ \\\\ \\ /\\ / /  | |/ _ \\ / _ \\| |
| |  __/ ___) |\\ V  V /   | | (_) | (_) | |
|_|_|   |____/  \\_/\\_/    |_|\\___/ \\___/|_|
"""

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_all_ipsw_devices() -> list[dict]:
    r = requests.get("https://api.ipsw.me/v4/devices")
    return json.loads(r.text)
def sort_devices(full_devices_list: list[dict]) -> dict[str, list[dict]]:
    sorted_dict = {"iPhone": [], "iPad": [], "Mac": [], "Apple TV": [], "Apple Watch": [], "Vision": [], "HomePod": [], "iPod Touch": []}
    for device in full_devices_list:
        identifier = device.get("identifier", "")
        if identifier.startswith("iPhone"): sorted_dict["iPhone"].append(device)
        elif identifier.startswith("iPad"): sorted_dict["iPad"].append(device)
        elif identifier.startswith("Mac"): sorted_dict["Mac"].append(device)
        elif identifier.startswith("AppleTV"): sorted_dict["Apple TV"].append(device)
        elif identifier.startswith("Watch"): sorted_dict["Apple Watch"].append(device)
        elif identifier.startswith("RealityDevice"): sorted_dict["Vision"].append(device)
        elif identifier.startswith("AudioAccessory"): sorted_dict["HomePod"].append(device)
        elif identifier.startswith("iPod"): sorted_dict["iPod Touch"].append(device)
    return sorted_dict

def get_prettified_models(models_list: list[dict]) -> dict[str, str]:
    pretty = {}
    for model in models_list:
        name = model.get("name")
        identifier = model.get("identifier")
        if not name or not identifier:
            continue
        pretty[name] = identifier
    return pretty
def get_firmwares(deviceid: str) -> list[dict]:
    r = requests.get(f"https://api.ipsw.me/v4/device/{deviceid}?type=ipsw")
    response = json.loads(r.text)
    firmwares = []
    for firmware in response.get("firmwares", []):
        firmwares.append(firmware)
    return firmwares
def download_ipsw(url: str, save_to_folder: str):
    response = requests.get(url, stream=True)
    if response.status_code == 404:
        print(f"The iPSW isn't present on Apple's servers. Check the info you have passed")
        input("Press ENTER to continue....")
        return
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    filename =  url.split("/")[-1]
    print(f"Downloading {filename}........\n")
    with tqdm.tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(save_to_folder,filename), "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    print(f"Download complete! The file is saved in: {os.path.join(save_to_folder,filename)} ")
    input("Press ENTER to continue....")



def menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    options = ["Download iPSW", "Download OTA", "Download iTunes(Windows & macOS before Catalina)", "Help", "Exit"]
    while True:
        tm = TerminalMenu(options, title="Choose an option:")  
        choice = tm.show()
        if choice == 0:
            # get devices
            ipsws = sort_devices(get_all_ipsw_devices())
            device_options = ["<- Back to main menu", *ipsws.keys()]
            devtm = TerminalMenu(device_options, title="Choose a device:")
            device_choice = devtm.show()
            if device_choice == 0:
                continue
            selected_category = device_options[device_choice]
            models = ipsws.get(selected_category, [])
            pretty_models = get_prettified_models(models)
            if not pretty_models:
                print(f"No models found for {selected_category}")
                continue
            # list models and their identifiers
            model_items = list(pretty_models.items())
            model_names = ["<- Back to main menu", *[name for name in pretty_models.keys()]]
            modeltm = TerminalMenu(model_names, title="Choose your model:")
            model_choice = modeltm.show()
            if model_choice == 0:
                continue
            # get firmwares 
            devid = model_items[model_choice - 1][1]
            firmwares = get_firmwares(devid)
            if not firmwares:
                print("No firmwares available.")
                continue
            firmopt = ["<- Back to main menu"]
            for firmware in firmwares:
                version = firmware.get("version", "Unknown")
                build = firmware.get("buildid", "N/A")
                state = "[signed]" if firmware.get("signed", False) else "[unsigned]"
                firmopt.append(f"{version} ({build}) - {state}")
            firmtm = TerminalMenu(firmopt, title="Choose firmware:")
            firmchoice = firmtm.show()
            if firmchoice == 0:
                continue
            selected_firmware = firmwares[firmchoice - 1]
            download_url = selected_firmware.get("url")
            download_ipsw(download_url, BASE_DIR)
        elif choice == 1:
            ident = input("Please enter your device identifier(e.g iPhone14,7): ")
            buildid = input("Please enter your device identifier(e.g iPhone14,7): ")
            get_url = requests.get(f"https://api.ipsw.me/v4/ota/download/{ident}/{buildid}", allow_redirects=True)
            if get_url.status_code == 302:
                downurl = get_url.url
                download_ipsw(downurl, BASE_DIR)
            if get_url.status_code == 404:
                print("Please enter a correct identifier and build id!")
                input("Press ENTER to continue....")
        elif choice == 2:
            platforms = ["<- Back to main menu","Windows", "macOS"]
            platmenu = TerminalMenu(platforms, title="Choose a platform:")
            platform_choice = platmenu.show()
            if platform_choice == 0: menu()
            itunes_platform = platforms[platform_choice]
            ver_response = requests.get(f"https://api.ipsw.me/v4/itunes/{itunes_platform}")
            version_info = json.loads(ver_response.text)
            versions_options = ["<- Back to main menu"]
            urls = [""]
            for itunes_version in version_info:
                versions_options.append(f'{itunes_version.get("version", "0.0.0")} - {itunes_version.get("releasedate")}')
                urls.append(itunes_version.get("url", None))
            verm = TerminalMenu(versions_options, title="Choose the iTunes version")
            version_choice = verm.show()
            if version_choice == 0: menu()
            itunes_url = urls[version_choice]
            if itunes_url:
                download_ipsw(itunes_url, BASE_DIR)
        elif choice == 3: 
            print("Help can be accessed by visiting https://github.com/mrrabyss/iPSW-Tool")
            input("Press ENTER to continue....")
        else: exit()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            menu()
        else:
            parser = argparse.ArgumentParser(description="IPSW/OTA/iTunes Downloader CLI")
            
            # Mode selection
            parser.add_argument("-t", "--type", choices=["ipsw", "ota", "itunes"], default="ipsw", help="Download type (ipsw, ota, or itunes)")
            
            # Device identifiers (Required for IPSW/OTA)
            parser.add_argument("-d", "--device", help="Device Identifier (e.g. iPhone14,7). Required for IPSW/OTA.")
            
            # iTunes platform (Required for iTunes)
            parser.add_argument("-p", "--platform", choices=["Windows", "macOS"], help="Platform (Windows or macOS). Required for iTunes.")
            
            # Version selection (Mutually exclusive)
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument("-b", "--build", help="Build ID (for IPSW/OTA) or Version Number (for iTunes)")
            group.add_argument("-l", "--latest", action="store_true", help="Download latest available version")

            args = parser.parse_args()

            # --- iTunes Logic ---
            if args.type == "itunes":
                if not args.platform:
                    parser.error("--platform is required when type is 'itunes'")
                
                print(f"Fetching iTunes versions for {args.platform}...")
                try:
                    ver_response = requests.get(f"https://api.ipsw.me/v4/itunes/{args.platform}")
                    ver_response.raise_for_status()
                    version_info = json.loads(ver_response.text)
                except Exception as e:
                    print(f"Error fetching iTunes info: {e}")
                    sys.exit(1)

                target = None
                if args.latest:
                    # Assuming the API returns the list sorted or newest first (typical for ipsw.me)
                    if version_info:
                        target = version_info[0]
                else:
                    for v in version_info:
                        if v.get("version") == args.build:
                            target = v
                            break
                
                if target:
                    print(f"Found iTunes {target.get('version')} ({target.get('releasedate')})")
                    url = target.get("url")
                    if url:
                        download_ipsw(url, BASE_DIR)
                    else:
                        print("Download URL not found in API response.")
                else:
                    print(f"iTunes version '{args.build}' not found for {args.platform}.")
                    sys.exit(1)

            # --- IPSW/OTA Logic ---
            elif args.type in ["ipsw", "ota"]:
                if not args.device:
                    parser.error(f"--device is required when type is '{args.type}'")

                if args.type == "ota":
                    if args.latest:
                        print("Error: --latest is not supported for OTA. Please provide a build ID with -b.")
                        sys.exit(1)
                    
                    ota_url = f"https://api.ipsw.me/v4/ota/download/{args.device}/{args.build}"
                    resp = requests.get(ota_url, allow_redirects=True)
                    if resp.ok: 
                        download_ipsw(resp.url, BASE_DIR)
                    else:
                        print(f"OTA not found. Status Code: {resp.status_code}")

                elif args.type == "ipsw":
                    print(f"Fetching firmwares for {args.device}...")
                    firmwares = get_firmwares(args.device)
                    
                    if not firmwares:
                        print(f"No firmwares found for {args.device}. Check the identifier.")
                        sys.exit(1)

                    target_firmware = None

                    if args.latest:
                        for fw in firmwares:
                            if fw.get("signed"):
                                target_firmware = fw
                                break
                        if not target_firmware:
                            print(f"No signed firmware currently available for {args.device}.")
                            sys.exit(1)
                    else:
                        for fw in firmwares:
                            if fw.get("buildid") == args.build:
                                target_firmware = fw
                                break
                        if not target_firmware:
                            print(f"Firmware with build ID {args.build} not found for {args.device}.")
                            sys.exit(1)
                    
                    if target_firmware:
                        download_url = target_firmware.get("url")
                        print(f"Found {target_firmware.get('version')} ({target_firmware.get('buildid')})")
                        download_ipsw(download_url, BASE_DIR)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"ERR: {e}")
        sys.exit(1)