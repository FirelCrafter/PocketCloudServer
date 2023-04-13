from flask import Blueprint, request, send_from_directory, flash, redirect, url_for, jsonify, make_response, send_file
from werkzeug.utils import secure_filename
from Application.services.file_service import FileService
from Application.config import Config
from Application.models.file_system_model import NodeType

file_blueprint = Blueprint('file_blueprint', __name__, url_prefix='/files')
file_service = FileService()


@file_blueprint.route('/directories', methods=['POST'])
def create_directory():
    parent_id = request.form.get("parentId", 0, type=int)
    name = request.form["name"]
    file_service.create_directory(name, parent_id)
    return make_response(jsonify({"status": "success", "message": "Directory created"}), 200)

@file_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_response(jsonify({"status": "error", "message": "no file provided"}), 400)
    
    file = request.files['file']
    parent_id = request.form.get("parent_id", 0, type=int)
    
    if file.filename == '':
        return make_response(jsonify({"status": "error", "message": "no file provided"}), 400)
    
    filename = secure_filename(file.filename)
    file_service.upload_file(file, parent_id)
    return make_response(jsonify({"status": "success", "message": "file uploaded"}), 200)

@file_blueprint.route('/list', methods=['GET'])
def file_list():
    file_list = file_service.get_file_list()
    return jsonify(file_list)

@file_blueprint.route('/stats', methods=['GET'])
def storage_stats():
    stats = file_service.get_storage_stats()
    return jsonify(stats)

@file_blueprint.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file_node = file_service.get_file_by_id(file_id)
    if not file_node or file_node.node_type != NodeType.FILE:
        return make_response(jsonify({"status": "error", "message": "file not found"}), 400)
    
    return send_file(file_node.file_path, as_attachment=True, download_name=file_node.name)
