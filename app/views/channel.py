from flask import Blueprint, render_template, flash, redirect, url_for, request

from app.lib.pagination import paginate
from app.models import channels as model

blueprint = Blueprint('channel', __name__)


@blueprint.route('/<channel_id>')
def display(channel_id):
    page_ordinal = int(request.args.get('page') or 1)
    channel = model.find_channel_by_id(channel_id)
    items = channel.find_all_items()
    page = paginate(items, page_ordinal)
    return render_template('channel/display.html', channel=channel, page=page)


@blueprint.route('/<channel_id>/update', methods=['POST'])
def update(channel_id):
    channel = model.find_channel_by_id(channel_id)
    channel.update_items()
    flash(f"Channel ‘{channel.title}’ was successfully updated.")
    return redirect(url_for('channel.display', channel_id=channel_id))


@blueprint.route('/<channel_id>/unsubscribe', methods=['POST', 'DELETE'])
def unsubscribe(channel_id):
    channel = model.find_channel_by_id(channel_id)
    model.delete_channel_and_its_items(channel_id)
    flash(f"Successfully unsubscribed from channel ‘{channel.title}’.")
    return redirect(url_for('library.display'))
