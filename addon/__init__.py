from ac_flask.hipchat import Addon
from flask import Flask
import os

os.environ["AC_BASE_URL"] = "https://d8400839.ngrok.io"  # server's address or tunnel address

app = Flask(__name__)
#app.config.from_object('config')
addon = Addon(app=app,
              key="addon",
              name="__STANDUP",
              allow_global=True,
              scopes=['send_notification', 'view_group', 'view_room'])

from addon import views