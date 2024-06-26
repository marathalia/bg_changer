import requests
from api import API_TOKEN
from datetime import datetime
from tqdm import tqdm  # taqaddum
import sys


def bg_changer(img, bg_color):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(img, "rb")},
        data={"size": "auto", "bg_color": bg_color},
        headers={"X-Api-Key": API_TOKEN},
    )

    # get response
    total_length = int(response.headers.get("content-length", 0))

    # create progress bar
    progress_bar = tqdm(total=total_length, unit="iB")

    # if request = response
    if response.status_code == requests.codes.ok:
        with open(
            "output/the_result_%s.png" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
            "wb",
        ) as out:
            for i in response.iter_content(chunk_size=1024):
                if i:
                    # update progress bar
                    progress_bar.update(len(i))
                    out.write(i)
    else:
        print("Error:", response.status_code, response.text)

    progress_bar.close()


image_path = sys.argv[1]  # python edit_bg.py
color_name = str(input("Enter the color name: "))

bg_changer(image_path, color_name)
