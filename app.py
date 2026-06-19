from copy import deepcopy
from os import environ

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
