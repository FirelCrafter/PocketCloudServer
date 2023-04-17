import os
import shutil
from Application.models.file_system_model import NodeType, File, Directory
from Application.config import Config
from math import floor

class FileService:
    def __init__(self):
        self.root = Directory("root", node_id=0)
        self.nodes = {0: self.root}
        self.next_node_id = 1
        
    def create_directory(self, name, parent_id, path):
        directory = Directory(name=name, parent_id=parent_id, node_id=self.next_node_id, path=path)
        self.nodes[self.next_node_id] = directory
        self.next_node_id += 1
        
    def upload_file(self, file, parent_id, path, save_to_disk=True):
        file_ext = file.filename.rsplit('.', 1)[-1].lower()
        file_path = os.path.join(Config.UPLOAD_FOLDER, path, str(self.next_node_id)) if save_to_disk else None
        new_file = File(file.filename, file_ext, parent_id=parent_id, node_id=self.next_node_id, file_path=file_path, path=path)
        self.nodes[self.next_node_id] = new_file
        self.next_node_id += 1
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
    def get_file_list(self):
        result = {
            "status": "success",
            "directory": self.root.to_dict(),
            "directories": [],
            "files": []
        }
        self._populate_children(result["directory"], result["directories"], result["files"])
        return result
    
    def _populate_children(self, directory, directories, files):
        directory["directories"] = []
        directory["files"] = []
        for node_id, node in self.nodes.items():
            if node.parent_id == directory["nodeId"]:
                if node.node_type == NodeType.DIRECTORY.value:
                    child_dir = node.to_dict()
                    directory["directories"].append(child_dir)
                    directories.append(child_dir)
                    self._populate_children(child_dir, directories, files)
                elif node.node_type == NodeType.FILE.value:
                    child_file = node.to_dict()
                    directory["files"].append(child_file)
                    files.append(child_file)
                    
    def get_storage_stats(self):
        stats = {
            "directories": 0,
            "files": 0,
            "extensions": {},
            "totalVolume": 0,
            "freeSpace": 0
        }
        
        for node in self.nodes.values():
            if node.node_type == Directory:
                stats["directories"] += 1
            elif node.node_type == File:
                stats["files"] += 1
                if node.extension in stats["extensions"]:
                    stats["extensions"][node.extension] += 1
                else:
                    stats["extensions"][node.extension] = 1
        
        disk_usage = shutil.disk_usage(Config.UPLOAD_FOLDER)
        stats["totalVolume"] = floor(disk_usage.total/1048576)
        stats["freeSpace"] = floor(disk_usage.free/1048576)
        
        return stats
    
    def get_file_by_id(self, file_id):
        return self.nodes.get(file_id)