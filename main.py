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

    user = input("User (linspics.1460)-> ")
    ithreads = input("Threads (default: 2) ->")
    pics = isit(input("Should Pictures be installed? (default: y) y/n ->"))
    bunkr = isit(input("Should Bunkr-videos be installed? (default: y) y/n ->"))
    saints = isit(input("Should Saints-videos be installed? (default: y) y/n ->"))
    threads = 2 if not ithreads.isnumeric() else int(ithreads)

    celebforum.getUser(user, threads, pics=pics, bunk=bunkr, saint=saints)
