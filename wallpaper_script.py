import os, time, json, subprocess

TIMER = 60 * 60
DELAY = 24 * 60 * 60


def wallpaper_filter(path):
    return os.path.isfile(wallpaper_dir + "/" + path) and (".jpg" in path or ".png" in path)


def change_wallpaper(path):
    uri = "'file://%s'" % path
    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
    subprocess.Popen(args)
    print("wallpaper changed to", uri)


wallpaper_dir = "/home/amaan/Pictures/wallpapers"
wallpaper_list = list(filter(wallpaper_filter, os.listdir(wallpaper_dir)))
data_file = wallpaper_dir + "/data_file.json"

print(wallpaper_list)

while True:
    CURRENT_TIME = time.time()
    data = {}
    if os.path.exists(data_file):
        with open(data_file, "r") as openfile:
            data = json.load(openfile)
    else:
        data = {"current_index": 0, "last_time": time.time()}
        with open(data_file, "w") as outfile:
            json.dump(data, outfile)

    LAST_TIME = float(data["last_time"])
    current_index = int(data["current_index"])
    new_index = current_index + 1 if current_index + 1 < len(wallpaper_list) else 0
    if CURRENT_TIME - LAST_TIME >= DELAY:
        data = {"current_index": new_index, "last_time": time.time()}
        with open(data_file, "w") as outfile:
            json.dump(data, outfile)
        change_wallpaper(wallpaper_dir + "/" + wallpaper_list[new_index])
    time.sleep(TIMER)
