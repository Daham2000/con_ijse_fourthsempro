from flask import Flask

import os
from flask import Flask, request, jsonify


app = Flask(__name__)

from application import routes