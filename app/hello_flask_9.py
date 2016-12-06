#!/usr/bin/python
# Filename:hello_flask.py

import hello_flask

if __name__ == '__main__':
    hello_flask.app.run(host="0.0.0.0", port=80, debug=True)
