from ac_flask.hipchat import room_client, addon_client, sender, context
from ac_flask.hipchat.glance import Glance
from flask import render_template, request, redirect, url_for
import werkzeug.exceptions


from addon import addon

_current_title = "Here will be your ad"
_time = "Set time"


@addon.configure_page()
def configure():
    return "hi"


@addon.webhook(event="room_enter")
def room_entered():
    return '', 204


@addon.webhook(event='room_message', pattern='^/update')
def room_message():
    return '', 204


@addon.glance(key='glance.key', name='Glance', target='webpanel.key', icon='static/img/icon.png')
def glance():
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
        #addon_client.update_global_glance('glance.key', glance_data)
        return "", 200
    except UnicodeEncodeError, werkzeug.exceptions.NotFound:
        return "", 400


if __name__ == '__main__':
    addon.run(host="0.0.0.0", port=5000)

