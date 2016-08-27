# -*- coding: utf-8 -*-
from ac_flask.hipchat import room_client, addon_client, sender, context, tenant
from ac_flask.hipchat.glance import Glance
from flask import render_template, request, redirect, url_for
import werkzeug.exceptions, json

from addon import addon, app

_BASE_URl = "*********"
_current_title = "Here will be your ad"
_time = "Set time"
_token_massage = None
_token = None
_room_id = None

# "2979867"

@addon.configure_page()
def configure():
    return "++++++++"


@addon.glance(key='glance.key', name='Glance', target='webpanel.key', icon='static/img/icon.png')
def glance():
    global _token, _token_massage, _room_id
    _token = room_client.get_token_o()
    _token_massage = room_client.get_token_m()
    _room_id = context['room_id']
    return Glance().with_label(_current_title).with_lozenge(_time, "current").data


@addon.webpanel(key='webpanel.key', name='Panel')
def web_panel():
    return render_template("index.html")


@addon.route(rule="/change_title", methods=['post'])
def change_title():
    global _current_title, _time
    try:
        title = request.form["text_title"].encode('utf-8')
        time = request.form["text_time"].encode('utf-8')
        message = request.form["cb_message"].encode('utf-8')
        if time != "":
            if title != "":
                glance_data = Glance().with_label(title).with_lozenge(time, 'current').data
            else:
                glance_data = Glance().with_label(_current_title).with_lozenge(time, 'current').data
            _time = time
        else:
            glance_data = Glance().with_label(title).data

        if message == "true":
            message = title
            room_client.send_notification(message, notify=True)

        _current_title = title
        addon_client.update_room_glance('glance.key', glance_data, context['room_id'])

        print context["room_id"]

        return "", 200
    except UnicodeEncodeError, werkzeug.exceptions.NotFound:
        return "", 400


@app.route(rule="/index", methods=['get'])
def index():
    rooms = json.loads(room_client.get_rooms(token="vLcofdJjVA4RPymzd0Z6mjNgaEjlYFgnCr3EdQPY").text)["items"]
    return render_template("web.html", rooms=rooms)


@app.route(rule="/get_rooms", methods=['get'])
def rooms():
    print room_client.send_notification_custom("FROM WEB", notify=True, color="green",
                                               room_id=_room_id, token="vLcofdJjVA4RPymzd0Z6mjNgaEjlYFgnCr3EdQPY").text
    print room_client.create_glance(token=_token, room_id="2970960").text
    return room_client.get_rooms(token="vLcofdJjVA4RPymzd0Z6mjNgaEjlYFgnCr3EdQPY").text


@app.route(rule="/ch_web", methods=['post'])
def _change():
    global _current_title, _time, _token, _token_massage
    try:
        title = request.form["text_title"].encode('utf-8')
        time = request.form["text_time"].encode('utf-8')
        message = request.form["cb_message"].encode('utf-8')
        if time != "":
            if title != "":
                glance_data = Glance().with_label(title).with_lozenge(time, 'current').data
                _current_title = title
            else:
                glance_data = Glance().with_label(_current_title).with_lozenge(time, 'current').data
            _time = time
        else:
            glance_data = Glance().with_label(title).data

        if message == "true":
            message = title
            room_client.send_notification_custom(message, notify=True, room_id=_room_id, token=_token_massage)

        print(addon_client.update_room_glance_custom('glance.key', glance_data, _room_id, _token).text)
        return "", 200
    except UnicodeEncodeError, werkzeug.exceptions.NotFound:
        return "", 400


@app.route(rule="/get_details", methods=['post'])
def get_details():
    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.get_room_glance(token=_token, room_id=room_id, glance_key="key{0}".format(room_id))

    if response.status_code == 200:
        response = response.text
    else:
        print(response.text)
        response = str(response.status_code)

    return response


@app.route(rule="/change_glance", methods=['post'])
def change_glance():
    room_id = request.form["room_id"].encode('utf-8')
    title = request.form["title"].encode('utf-8')
    room_client.delete_glance(token=_token, room_id=room_id, glance_key="key{0}".format(room_id))
    response = room_client.create_glance(token=_token, room_id=room_id,
                                         glance_key="key{0}".format(room_id),
                                         advertisement=title,
                                         base_url=_BASE_URl).status_code
    return str(response)


@app.route(rule="/delete_glance", methods=['post'])
def delete_glance():
    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.delete_glance(token=_token, room_id=room_id, glance_key="key{0}".format(room_id))

    return str(response)


@app.route(rule="/create_glance", methods=['post'])
def create_glance():
    room_id = request.form["room_id"].encode('utf-8')
    response = room_client.create_glance(token=_token, room_id=room_id,
                                         glance_key="key{0}".format(room_id),
                                         advertisement="This is your advertisement",
                                         base_url=_BASE_URl)
    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4444)
    addon.run(host="0.0.0.0", port=5000)
