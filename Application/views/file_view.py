import os
from flask import Blueprint, request, send_from_directory, flash, redirect, url_for, jsonify, make_response, send_file, session, abort, current_app
from werkzeug.utils import secure_filename
from Application.services.file_service import FileService
from Application.config import Config
from Application.models.file_system_model import NodeType
from functools import wraps

file_blueprint = Blueprint('file_blueprint', __name__, url_prefix='/files')
file_service = FileService()

def require_pin_verification(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'pin_verified' not in session or not session['pin_verified']:
            abort(400)
        return func(*args, **kwargs)
    return wrapper

@file_blueprint.route('/verifyPin', methods=['POST'])
def verify_pin():
    entered_pin = request.get_json(force=True)["pin"]
    if entered_pin is None or len(entered_pin) != 4:
        return make_response(jsonify({"status": "error", "message": "Invalid PIN format"}), 400)
    
    stored_pin = str(current_app.config['PIN_CODE'])
    if entered_pin == stored_pin:
        session['pin_verified'] = True
        return make_response(jsonify({"status": "success", "message": "PIN verified"}), 200)
    else:
        return make_response(jsonify({"status": "error", "message": "Incorrect PIN"}), 400)
    
@file_blueprint.route('/changePin', methods=["POST"])
@require_pin_verification
def change_pin():
    current_pin = request.get_json(force=True)["currentPin"]
    new_pin = request.get_json(force=True)["newPin"]
    print(f"CURRENT PIN: {current_pin}")
    if current_pin == current_app.config['PIN_CODE']:
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py')
        
        with open(config_file_path, 'r') as config_file:
            config_content = config_file.read()
        
        config_content = config_content.replace(f"PIN_CODE = '{current_app.config['PIN_CODE']}'", f"PIN_CODE ='{new_pin}'")
    
        with open(config_file_path, 'w') as config_file:
            config_file.write(config_content)
        
        current_app.config['PIN_CODE'] = new_pin
        return make_response(jsonify({"status": "success", "message": "PIN changed"}), 200)
    else:
        return make_response(jsonify({"status": "error", "message": "Incorrect current PIN"}), 400)

@file_blueprint.route('/directories', methods=['POST'])
@require_pin_verification
def create_directory():
    parent_id = request.form.get("parentId", 0, type=int)
    name = request.form["name"]
    file_service.create_directory(name, parent_id)
    return make_response(jsonify({"status": "success", "message": "Directory created"}), 200)

@file_blueprint.route('/upload', methods=['POST'])
@require_pin_verification
def upload_file():
    if 'file' not in request.files:
        return make_response(jsonify({"status": "error", "message": "no file provided"}), 400)
    
    file = request.files['file']
    parent_id = request.form.get("parentId", 0, type=int)
    path = request.form.get("path", "", type=str)
    
    if file.filename == '':
        return make_response(jsonify({"status": "error", "message": "no file provided"}), 400)
    
    filename = secure_filename(file.filename)
    file_service.upload_file(file, parent_id, path)
    return make_response(jsonify({"status": "success", "message": "file uploaded"}), 200)

@file_blueprint.route('/list', methods=['GET'])
@require_pin_verification
def file_list():
    file_list = file_service.get_file_list()
    return jsonify(file_list)

@file_blueprint.route('/stats', methods=['GET'])
@require_pin_verification
def storage_stats():
    stats = file_service.get_storage_stats()
    return jsonify(stats)

@file_blueprint.route('/download/<int:file_id>', methods=['GET'])
@require_pin_verification
def download_file(file_id):
    file_node = file_service.get_file_by_id(file_id)
    if not file_node or file_node.node_type != NodeType.FILE:
        return make_response(jsonify({"status": "error", "message": "file not found"}), 400)
    
    return send_file(file_node.file_path, as_attachment=True, download_name=file_node.name, attachment_filename=os.path.join(file_node.path, file_node.name))
