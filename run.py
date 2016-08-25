# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
from addon import addon, app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    addon.run(debug=True, host='0.0.0.0', port=port, threaded=True)
