from mimetypes import guess_extension
from urllib.parse import urlsplit
from time import sleep
import threading
import requests
import os

def download_file(url, folder, headers={}, cookies={}, celeb=False):
    try:
        response = requests.get(url, stream=True, headers=headers, cookies=cookies)
        content_type = response.headers.get('Content-Type')
        extension = guess_extension(content_type) or '.bin'
        celebname = url.replace('https://celebforum.to/attachments/', '').split('-')[0] + extension
        filename = os.path.basename(urlsplit(url).path) or f"file{extension}" if celeb == False else celebname

        file_path = os.path.join(folder, filename)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    except ConnectionError as e:
        print(f"Error downloading {url}: {e}")

def download_files(urls, folder, num_threads, headers={}, cookies={}, celeb=False):
    if not os.path.exists(folder):
        os.makedirs(folder)

    threads = []
    for url in urls:
        if len(threads) >= num_threads:
            for t in threads:
                t.join() 
            threads = []  
        t = threading.Thread(target=download_file, args=(url, folder, headers, cookies, celeb))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()