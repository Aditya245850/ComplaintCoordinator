import asyncio
import os

from quart import Blueprint, current_app, redirect, request, url_for
from quart_auth import current_user, login_required

from process.Image import process_Image
from process.Text import process_Text
from process.Video import process_Video
from process.Voice import process_Voice

uploads_bp = Blueprint('uploads', __name__)


async def _save_and_process(file_key, process_fn):
    files = await request.files
    if file_key in files:
        f = files[file_key]
        if f.filename != '':
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, f.filename)
            await f.save(file_path)

            username = current_user.auth_id
            api_key = current_app.config['API_KEY']

            async def run():
                await process_fn(file_path, username, api_key)

            asyncio.create_task(run())
    return redirect(url_for('dashboard.index'))


@uploads_bp.route('/Video', methods=['POST'])
@login_required
async def video_action():
    return await _save_and_process('video_file', process_Video)


@uploads_bp.route('/Text', methods=['POST'])
@login_required
async def text_action():
    return await _save_and_process('text_file', process_Text)


@uploads_bp.route('/Voice', methods=['POST'])
@login_required
async def voice_action():
    return await _save_and_process('voice_file', process_Voice)


@uploads_bp.route('/Image', methods=['POST'])
@login_required
async def image_action():
    return await _save_and_process('image_file', process_Image)
