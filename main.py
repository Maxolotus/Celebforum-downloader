import celebforum
import os

banner = """
╔═╗╔═╗╦  ╔═╗╔╗ ╔═╗╔═╗╦═╗╦ ╦╔╦╗
║  ║╣ ║  ║╣ ╠╩╗╠╣ ║ ║╠╦╝║ ║║║║
╚═╝╚═╝╩═╝╚═╝╚═╝╚  ╚═╝╩╚═╚═╝╩ ╩
"""

def isit(value):
    return not (value.lower() == "n" or value.lower() == "no" or value.lower() == "false")

if __name__ == "__main__":
    print(banner)
    print("Celeforum-Downloader is in no way affiliated with by Celebforum. \n\tThis is an independent and unofficial project. \n\t\tUse at your own risk.")
    print("You only have to enter the user and the Rest is optional!")

    print("Also the wait time is not the ratelimit time!!! but you can change that in downloader.py#sleep(20)")

    user = input("User (linspics.1460)-> ")
    ithreads = input("Threads (default: 4) ->")
    itimewait = input("Wait time between download (default 4)->")
    pics = isit(input("Should Pictures be installed? (default: y) y/n ->"))
    bunkr = isit(input("Should Bunkr-videos be installed? (default: y) y/n ->"))
    saints = isit(input("Should Saints-videos be installed? (default: y) y/n ->"))
    threads = 2 if not ithreads.isnumeric() else int(ithreads)
    waittime = 4 if not itimewait.isnumeric() else int(threads)

    celebforum.getUser(user, threads, pics=pics, bunk=bunkr, saint=saints, waittime=waittime)
