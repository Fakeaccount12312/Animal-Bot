import requests, bs4, re
import csv, os
from datetime import datetime

data = [["animal", "urlstart", "images"]]
row = []
fails = 0

print("Started extracting at " + datetime.now().strftime("the %d.%m.%y at %H:%M:%S"))

for animal in (("bear", "bears"), ("bird", "birds"), ("cat", "cats"), ("chameleon", "chameleons"), ("cheetah", "cheetahs"), ("chicken", "chickens"), ("cow", "cows"), ("deer", "deer", "deers"), ("dog", "dog", "dogs"), ("duck", "ducks"), ("elephant", "elephants"), ("ferret", "ferrets"), ("fish", "fish"), ("fox", "foxes"), ("frog", "frogs"), ("giraffe", "giraffes"), ("guinea pig", "guinea-pigs"), ("hamster", "hamster"), ("hedgehog", "hedgehogs"), ("horse", "horses"), ("kangaroo", "kangaroos"), ("koala", "koalas"), ("leopard", "leopards"), ("lion", "lions"), ("meerkat", "meerkats"), ("mouse", "mice"), ("orangutan", "orangutans"), ("otter", "otters"), ("owl", "owls"), ("panda", "pandas"), ("penguin", "penguins"), ("pig", "pigs"), ("polar bear", "polar-bears"), ("rabbit", "rabbits"), ("red panda", "red-pandas"), ("seal", "seals"), ("sheep", "sheep"), ("sloth", "slothes"), ("squirrel", "squirrels"), ("tiger", "tigers"), ("turtle", "tortoises")):
    row = []
    for tag in animal[1:]:
        website = requests.get("http://www.cutestpaw.com/tag/" + tag + "/").content
        pages = int(re.findall(r"Page 1 of (\d+)", str(website))[0])
        for pageindex in range(pages):
            print("Scraping page " + str(pageindex + 1) + " of " + str(pages) + " for " + tag)
            website = requests.get("http://www.cutestpaw.com/tag/" + tag + "/page/" + str(pageindex + 1) + "/").content
            website = bs4.BeautifulSoup(website, "html5lib")
            images = website.find(id="photos")
            images = images.find_all("img")
            for image in images:
                # ensure that the image url cosists only of ascii to avoid errors
                try:
                    image_src = image["src"][len("http://www.cutestpaw.com/wp-content/uploads/"):]
                    asd = image_src.encode("ascii", "strict")
                    row.append(image_src)
                except:
                    fails += 1
    data.append([animal[0], "http://www.cutestpaw.com/wp-content/uploads/"] + row)

row = []

for page in ("Tiny", "Small", "Medium", "Large"):
    print("Scraping page " + page + " for spiders")
    website = requests.get("http://www.findaspider.org.au/find/spiders/" + page + ".htm").content
    website = bs4.BeautifulSoup(website, "html5lib")
    images = website.find(class_="mainimage")
    images = images.find_all("img")
    for image in images:
        row.append(image.parent["href"][len("./images/"):])

data.append(["spider", "http://www.findaspider.org.au/find/spiders/images/"] + row)

row = []

for page in range(1, 5):
    print("Scraping page " + str(page) + " of 5 for rhinos")
    website = requests.get("https://wall.alphacoders.com/by_sub_category.php?id=174594&name=Rhino+Wallpapers&page=" + str(page)).content
    website = bs4.BeautifulSoup(website, "html5lib")
    images = website.find(class_="thumb-container-big").parent
    images = images.find_all("img")
    for image in images:
        if "user-avatar" not in image["class"]:
            row.append(image["data-src"])

data.append(["rhino", ""] + row)

row = []

print("Scraping page 1 of 1 for sea cucumbers")
website = requests.get("http://www.ryanphotographic.com/holothuroidea.htm").content
website = bs4.BeautifulSoup(website, "html5lib")
images = website.find(height=None)
images = images.find_all("img")
for image in images:
    row.append(image["src"][len("images/"):].replace(" ", "%20"))

data.append(["sea cucumber", "http://www.ryanphotographic.com/images/"] + row)

with open("imageurls.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

print("Images extracted at the " + datetime.now().strftime("the %d.%m.%y at %H:%M:%S. ") + "Failed to resolve urls " + str(fails) + " times.")

if os.name != "nt":
    os.system("update.sh &")
