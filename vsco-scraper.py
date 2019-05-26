import requests, json, urllib, os, errno

# Profile Image:
from PIL import Image
import urllib2

def scrape_vsco(username):

    # List of photos
    pictures = []

    s = requests.session()

    page_number = 1

    # Create the directory:
    directory = username
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            directory = directory+"-"+str(random.randint(0, 5000))
            os.makedirs(directory)
    
    os.chdir(directory)

    # Grab the profile
    profile = s.get("https://vsco.co/"+username+"/images/"+str(page_number))

    # Data from html page
    contents = profile.text

    # Profile picture
    profile_picture_link = contents.split('"profileImage":"')[1]
    profile_picture_link = profile_picture_link[:profile_picture_link.index('"')]
    profile_picture_link = profile_picture_link.split("?")[0]
    
    # Save profile picture
    print "Downloading profile picture..."
    im = Image.open(urllib2.urlopen(profile_picture_link))
    im.save('profile_picture.jpg')

    while True:

        # Grab the full data for this page
        data = contents.split("window.__PRELOADED_STATE__ =")[1]
        data = data[:data.index("</script>")]

        # Convert string to JSON format
        data = json.loads(data)

        if len(data["entities"]["images"]) == 0:
            print "Done."
            break

        print "Downloading page " + str(page_number) + " ..."

        # Grab the images
        for x in data["entities"]["images"]:
            if data["entities"]["images"][x]["isVideo"]:
                urllib.urlretrieve("http://"+data["entities"]["images"][x]["videoUrl"], x+".mp4")
            else:
                urllib.urlretrieve("http://"+data["entities"]["images"][x]["responsiveUrl"], x+".jpg")
            pictures.append(x)

        page_number += 1
        # Grab the profile
        profile = s.get("https://vsco.co/"+username+"/images/"+str(page_number))

        # Data from html page
        contents = profile.text

    os.chdir('../')



username = raw_input('Username: ')
while username.upper() != "EXIT" and username.upper() != "QUIT":
    scrape_vsco(username)
    username = raw_input('Username: ')
    
