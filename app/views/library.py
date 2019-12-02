from ast import dump

import flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, get_flashed_messages

from app.models import channels as model
from app.models.channels import SubscriptionError

library = Blueprint('library', __name__)


@library.route('/')
def display():
    feeds = model.find_all_channels()
    return render_template('library/display.html', channels=feeds)


@library.route('/new')
def new():
    return render_template('library/new.html')


@library.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        url = request.form['url']
        channel = model.subscribe(url)
        flash(f"Added subscription to channel ‘{channel.title}’.")
        return redirect(url_for('library.display'))
    except SubscriptionError as err:
        flash(f"Failed to add subscription: {err}", category='error')
        return redirect(url_for('library.new'))
