from flask import Flask, render_template, request, redirect
from vsldata import Database
import cv2
import time
import os
import threading
from imgbeddings import imgbeddings
from PIL import Image
from scipy.spatial.distance import cityblock
from socket import socket
import math
import base64


app = Flask(__name__)
db = Database("db\\db-user.db")
cascade = cv2.CascadeClassifier("static\haarcascade.xml")
bd = imgbeddings()
match_val = 0
user = ""
max_tries = 0
cropped = False
decryptFM = {"0":"gfTE","1":"JKbZ","2":"$RFe","3":"&Uii","4":"QW)(","5":"//We","6":"eeRT","7":"JKMf","8":"oo$$","9":"##Yt",".":"%#@!"}
ON_VPN = True
vpn_port = 4444
IPAddress = "192.168.42.11"
auth_key = ""
n_size = 100
timer = 5
OLD = ""

def photo_write(base64_encoding, path):
    name_tt = 0
    for base in base64_encoding:
        with open(f"db/FR_DB/{path}/{name_tt}.png", "wb") as wph:
            photo = base64.b64decode(base)
            wph.write(photo)
        name_tt += 1

def gen_list(path):
    global n_size

    for image in os.listdir(path):
        # walk through every image to find faces and crop

        img_path = path+"\\"+image
        cv_img = cv2.imread(img_path, 0)
        cv_bw = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

        face = cascade.detectMultiScale(cv_bw, scaleFactor=1.05, minNeighbors=5, minSize=(150, 150))
        # cropping the images
        multiscaler = 0

        for x,y,w,h in face:

            crp_img = cv_img[y+15:(y+h-15), x+25:(x+w-25)]
            o_height , o_width = crp_img.shape
            n_height = o_height - (o_width - n_size)
            crp_img = cv2.resize(crp_img, (n_size, n_height))
            tar_file = path+"\\"+image[:image.find(".") - multiscaler] + ".jpg"
            multiscaler+=1

            # break

            cv2.imwrite(tar_file, crp_img)
            if True:
                print(f"succesfull: {multiscaler}")


def createAuth():
    global auth_key
    global IPAddress
    for i in IPAddress:
        for a, b in decryptFM.items():
            if i == a:
                auth_key+= b
                break

def save_face():
    global match_val
    global cropped

    # cv2.imwrite("db/FR_DB/"+user+"/"+user+str(cap)+".jpg", frame)

    frame = cv2.imread("db/FR_DB/"+user+"/"+user+".png", 0)
    c_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    c_face = cascade.detectMultiScale(c_gray, scaleFactor=1.05,minNeighbors=3, minSize=(100, 100))

    for x, y, w, h in c_face:
        img_diff = 0
        img_total = 0

        c_cropped = c_gray[y+15:(y+h-10), x+25:(x+w-25)]
        o_height , o_width, _ = c_cropped.shape
        n_height = o_height - (o_width - 100)
        c_cropped = cv2.resize(c_cropped, (100, n_height))
        cv2.imwrite("db/FR_DB/"+user+"/"+user+".png", c_cropped)
        cropped = True

        time.sleep(1)
        c_cropped = Image.open("db/FR_DB/"+user+"/"+user+".png")
        c_bd = bd.to_embeddings(c_cropped)
        c_bd = c_bd.flatten()
        for db_images in os.listdir("db/FR_DB/"+user):
            if user not in db_images:
                db_path = os.path.join("db/FR_DB/"+user, db_images)
                db_img = Image.open(db_path)
                db_arr = bd.to_embeddings(db_img)
                db_arr = db_arr.flatten()
                dist = cityblock(db_arr, c_bd)
                img_diff += math.floor(dist)
                img_total += 1

        # print(match_val)
        match_val = math.ceil(((img_diff/img_total)/100) - 0.1)

        time.sleep(1)
        # match_val = (match_val/len(os.listdir("db/FR_DB/"+user)))
        # print(match_val, len(os.listdir("db/FR_DB/"+user)))

def timming():
    while True:
        global timer
        timer -= 1
        time.sleep(1)

@app.route("/")
def index():
    global IPAddress
    # IPAddress = request.remote_addr
    timming()
    createAuth()
    print(IPAddress, auth_key)
    return render_template("index.html")

@app.route("/page")
def admin():
    global ON_VPN
    if user == "leonard" and ON_VPN and timer :
        return render_template("admin.html")
    else:
        return render_template("LAN_index.html")

@app.route("/face_recog", methods=["POST"])
def fralgo():
    global user
    global max_tries
    data = request.get_json()

    fr = base64.b64decode(data["data"])
    
    if os.path.exists("db/FR_DB/"+user):
        with open("db/FR_DB/"+user+"/"+user+".png", "wb") as wb:
            wb.write(fr)

        # for cap in range(0, 3, 1):
        #     vidCap = cv2.VideoCapture(0)
        #     val, frame = vidCap.read()
        #     vidCap.release()
        get_face = threading.Thread(target=save_face)
        get_face.start()
        get_face.join()
        #     if os.path.exists("db/FR_DB/"+user+"/"+user+str(cap)+".jpg"):
        #         os.remove("db/FR_DB/"+user+"/"+user+str(cap)+".jpg")
        #     print(match_val)

        if match_val <= 2 and match_val > 0 and cropped:
            print(f"MATCH : {match_val}")
            return "MATCH"
        elif match_val > 2:
            print(f"NO MATCH : {match_val}")
            max_tries += 1
            return "NO MATCH"

    else:
        return "NO DB"
        

@app.route("/get_pass", methods=["POST"])
def get_post():
    global user
    global max_tries
    data = request.get_json()
    print(data)

    username = data["user"]
    password = data["pass"]

    if db.isindb("name", username) and max_tries < 5:
        if db.findrow(username, password) and max_tries < 5:
            user = username

            return "confirmed"
        else:
            max_tries += 1
            return "password"
    elif max_tries >= 5:
        return redirect("https://www.unknownpath.com")
    else:
        max_tries += 1
        return "unconfirmed"
    
@app.route("/get_auth", methods=["POST"])
def get_auth():
    global auth_key
    return auth_key

    
@app.route("/connect_vpn", methods=["POST"])
def get_conn():
    user_ip = request.remote_addr
    message = request.form.get("message")
    if message == user_ip:
        ON_VPN = True
        print("CONNECTED")
        return vpn_port
    else:
        ON_VPN = False
        return "Server not connected"
    
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    new_id = data["id"]
    new_pass = data["pass"]
    photo_db = data["photos"].split("$$$")

    if db.isindb("name", new_id):
        return "failed"
    else:
        os.mkdir(f"db/FR_DB/{new_id}")
        db.append(new_id, new_pass)
        photo_gen = threading.Thread(target=photo_write, args=(photo_db, new_id))
        face_gen = threading.Thread(target=gen_list, args=(new_id))
        photo_gen.start()
        face_gen.start()
        photo_gen.join()
        face_gen.join()
        return "success"

@app.route("/LAN", methods=["POST"])
def start_LAN():
    area = 0.011
    data = request.get_json()
    with open("locate.coord", "r") as w_location:
        location = w_location.read()
        location = location.split(",")
        lati = location[0]
        longi = location[1]

    latitude = data["latitude"]
    longitude = data["longitude"]

    if user == "leonard":
        with open("locate.coord", "w") as r_location:
            local_data = f"{latitude},{longitude}"
            r_location.write()
    else:
        global timer
        if (latitude <= (lati + area) or longitude <= (longi + area)) and (latitude <= (lati - area) or longitude <= (longi - area)):
            timer = 5


@app.route("/LAN_chat", methods=["POST"])
def chat():
    message = request.get_json()["message"]
    to_add = f"{user}&&{message}\n"
    with open("LAN_chat.coord", "a") as abc:
        abc.write(to_add)
    return "Success"

@app.route("/update", methods=["POST"])
def update():
    global OLD
    while True:
        time.sleep(0.5)
        with open("LAN_chat.coord" , "r") as readLan:
            LANDB = readLan.read()
            LANDB = LANDB.split("\n")
            NEW = LANDB[len(LANDB) - 1]
            if OLD != NEW:
                OLD = NEW
                VALUE = NEW.split("&&")
                if VALUE[0] != user:
                    return NEW
                else:
                    pass

@app.route("/logout")
def logout():
    global match_val
    global user
    global max_tries
    global cropped
    global ON_VPN
    global n_size
    global timer
    global OLD

    match_val = 0
    user = ""
    max_tries = 0
    cropped = False
    ON_VPN = True
    n_size = 100
    timer = 5
    OLD = ""

    return render_template("/")


if __name__ == "__main__":
    timming()
    app.run(#ssl_context=("cert.pem", "key.pem"),
            host="0.0.0.0",
            debug=False)