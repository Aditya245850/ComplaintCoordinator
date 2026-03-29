import os
import threading

from flask import Blueprint, current_app, redirect, request, session, url_for

from process.Image import process_Image
from process.Text import process_Text
from process.Video import process_Video
from process.Voice import process_Voice

uploads_bp = Blueprint('uploads', __name__)


def _save_and_process(file_key, process_fn, async_process=False):
    if file_key in request.files:
        f = request.files[file_key]
        if f.filename != '':
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, f.filename)
            f.save(file_path)

            username = session.get('username')
            api_key = current_app.config['API_KEY']

            def run():
                process_fn(file_path, username, api_key)
                os.remove(file_path)
            threading.Thread(target=run).start()
    return redirect(url_for('dashboard.index'))


@uploads_bp.route('/Video', methods=['POST'])
def video_action():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return _save_and_process('video_file', process_Video)


@uploads_bp.route('/Text', methods=['POST'])
def text_action():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return _save_and_process('text_file', process_Text)


@uploads_bp.route('/Voice', methods=['POST'])
def voice_action():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return _save_and_process('voice_file', process_Voice)


@uploads_bp.route('/Image', methods=['POST'])
def image_action():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return _save_and_process('image_file', process_Image)
