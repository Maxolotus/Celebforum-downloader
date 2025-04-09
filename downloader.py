from mimetypes import guess_extension
from urllib.parse import urlsplit
from time import sleep
import threading
import cloudscraper
import os

# Create a single cloudscraper session (to reuse cookies and headers)
scraper = cloudscraper.create_scraper()

def download_file(url, folder, headers={}, cookies={}, celeb=False, waittime=4):
    try:
        response = scraper.get(url, stream=True, headers=headers, cookies=cookies)
        content_type = response.headers.get('Content-Type')
        extension = guess_extension(content_type) or '.bin'
        celebname = url.replace('https://celebforum.to/attachments/', '').split('-')[0] + extension
        filename = os.path.basename(urlsplit(url).path) or f"file{extension}" if celeb == False else celebname

        file_path = os.path.join(folder, filename)

        if file_path.endswith(".bin"):
            print("RATE-LIMITED or blocked – waiting 20 seconds...")
            sleep(20)
            download_file(url, folder, headers, cookies, celeb)
            return  # return needed to avoid double download

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        sleep(waittime)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    except ConnectionError as e:
        print(f"Connection error downloading {url}: {e}")

def download_files(urls, folder, num_threads, headers={}, cookies={}, celeb=False, waittime=4):
    if not os.path.exists(folder):
        os.makedirs(folder)

    threads = []
    for url in urls:
        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []
        t = threading.Thread(target=download_file, args=(url, folder, headers, cookies, celeb, waittime))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
