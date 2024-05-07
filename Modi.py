import requests
import random
import threading

def get_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all"
    response = requests.get(url)
    proxies = response.text.split('\r\n')  # Split the response by line breaks
    return proxies

def is_valid_proxy(proxy):
    # Check if the proxy URL is in the format ip:port
    return ":" in proxy

def check_proxy(proxy, result_list):
    try:
        response = requests.get("https://google.com", proxies={"https": proxy}, timeout=5)
        if response.status_code == 200:
            result_list.append(proxy)
    except Exception as e:
        pass

def find_working_proxy(proxies):
    result_list = []
    threads = []
    for proxy in proxies:
        if is_valid_proxy(proxy):
            thread = threading.Thread(target=check_proxy, args=(proxy, result_list))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    return result_list

def get_session_and_tourist_id(proxy):
    url = "https://aicover-api.topmediai.com/user/tourist_id"
    try:
        response = requests.get(url, proxies={"https": proxy})
        response.raise_for_status()
        data = response.json()
        session_id = data["data"]["session_id"]
        tourist_id = data["data"]["tourist_id"]
        return session_id, tourist_id
    except Exception as e:
        print(f"Error occurred while fetching session_id and tourist_id with proxy {proxy}: {e}")
        return None, None

def get_cover_yt_tourist(youtube_url, session_id, tourist_id, proxy):
    url = "https://aicover-api.topmediai.com/cover_yt_tourist"
    singer_id = 54
    token = ""  # Provide your token here

    data = {
        "token": token,
        "singer_id": singer_id,
        "youtube_url": youtube_url,
        "session_id": session_id,
        "tourist_id": tourist_id
    }

    try:
        response = requests.post(url, data=data, proxies={"https": proxy})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error occurred while making POST request with proxy {proxy}: {e}")
        return None

def main():
    while True:
        proxies = get_proxies()
        random.shuffle(proxies)  # Shuffle the proxies list for randomness
        working_proxies = find_working_proxy(proxies)
        if not working_proxies:
            print("No valid proxies found. Reloading...")
            continue

        proxy = random.choice(working_proxies)
        session_id, tourist_id = get_session_and_tourist_id(proxy)
        if session_id is not None and tourist_id is not None:
            youtube_url = input("Enter the YouTube URL: ")
            response = get_cover_yt_tourist(youtube_url, session_id, tourist_id, proxy)
            if response is not None:
                if response.get("status") == 200:
                    print("Script by @jashgro")
                    print("https://github.com/BlackHatDevX/Modi-Ai-Voice-Generator/")
                    print("File link (combined): ",response["data"]["file"])
                    print("File link (only vocals): ", response["data"]["acabella_file"])
                    print("File link (only instrumental): ", response["data"]["instrumental_file"])
                else:
                    print("Error:", response["message"])
            break

if __name__ == "__main__":
    main()
