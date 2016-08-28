# -*- coding: utf-8 -*-
from ac_flask.hipchat import room_client, addon_client, sender, context, tenant
from flask import render_template, request, redirect, url_for
from ac_flask.hipchat.glance import Glance
import werkzeug.exceptions, json

from addon import addon, app

BASE_URl = "https://b8959256.ngrok.io"
GLOBAL_TOKEN = None


@addon.configure_page()
def configure():
    user_id, user_secret = addon_client.get_info()
    with open("info.txt", "w") as f:
        f.write(user_id + "\n" + user_secret)
    return "+"


@app.route(rule="/index", methods=['get'])
def index():
    resp = room_client.get_rooms(token=GLOBAL_TOKEN)
    if resp.status_code == 200:
        rooms = json.loads(resp.text)["items"]
        return render_template("web.html", rooms=rooms)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['post', 'get'])
def login():
    global GLOBAL_TOKEN
    try:
        GLOBAL_TOKEN = request.form.get('txglobaltoken')
    except werkzeug.exceptions.BadRequest:
        pass
    resp = room_client.get_rooms(token=GLOBAL_TOKEN)
    if resp.status_code == 200:
        return redirect(url_for("index"))
    else:
        return render_template("web_auth.html")


@app.route(rule="/get_details", methods=['post'])
def get_details():
    with open("info.txt", "r") as f:
        info = f.read()
    token = addon_client.gen_token(info.split("\n")[0], info.split("\n")[1])

    print "***" * 50
    print token
    print "***" * 50

    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.get_room_glance(token=token, room_id=room_id, glance_key="key{0}".format(room_id))

    if response.status_code == 200:
        response = response.text
    else:
        print(response.text)
        response = str(response.status_code)

    return response


@app.route(rule="/change_glance", methods=['post'])
def change_glance():
    with open("info.txt", "r") as f:
        info = f.read()

    token = addon_client.gen_token(info.split("\n")[0], info.split("\n")[1])

    room_id = request.form["room_id"].encode('utf-8')
    title = request.form["title"].encode('utf-8')
    notify = request.form["notify"].encode('utf-8')
    time = request.form["time"].encode('utf-8')

    if time == "":
        glance_data = Glance().with_label(title).with_lozenge("!", 'current').data
    else:
        glance_data = Glance().with_label(title).with_lozenge(str(time), 'current').data
    addon_client.update_room_glance_custom(token=token, glance_key="key{0}".format(room_id),
                                           glance_data=glance_data, room_id=room_id)

    room_client.delete_glance(token=token, room_id=room_id, glance_key="key{0}".format(room_id))
    response = room_client.create_glance(token=token, room_id=room_id,
                                         glance_key="key{0}".format(room_id),
                                         advertisement=title,
                                         base_url=BASE_URl).status_code
    if notify == "true":
        room_client.send_notification_custom(message=title,
                                             token=token,
                                             room_id=room_id,
                                             notify=True)

    return str(response)


@app.route(rule="/delete_glance", methods=['post'])
def delete_glance():
    with open("info.txt", "r") as f:
        info = f.read()
    token = addon_client.gen_token(info.split("\n")[0], info.split("\n")[1])
    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.delete_glance(token=token, room_id=room_id, glance_key="key{0}".format(room_id))

    return str(response)


@app.route(rule="/create_glance", methods=['post'])
def create_glance():
    with open("info.txt", "r") as f:
        info = f.read()
    token = addon_client.gen_token(info.split("\n")[0], info.split("\n")[1])
    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.create_glance(token=token, room_id=room_id,
                                         glance_key="key{0}".format(room_id),
                                         advertisement="This is your advertisement",
                                         base_url=BASE_URl)
    return str(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4444)
    addon.run(host="0.0.0.0", port=5000)
