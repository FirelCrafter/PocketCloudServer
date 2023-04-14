import os
from enum import Enum

class NodeType(Enum):
    FILE = "file"
    DIRECTORY = "directory"

class FileSystemNode:
    def __init__(self, name, parent_id=None, node_id=None, path=None):
        self.name = name
        self.parent_id = parent_id
        self.node_id = node_id
        self.path = path
        
    def to_dict(self, node_type):
        return {
            "name": self.name,
            "nodeType": node_type,
            "parentId": self.parent_id,
            "nodeId": self.node_id,
            "path": self.path
        }
        
class File(FileSystemNode):
    node_type = NodeType.FILE.value
    
    def __init__(self, name, extension, parent_id=None, node_id=None, file_path=None):
        super().__init__(name, parent_id, node_id)
        self.extension = extension
        self.file_path = file_path
        
    def to_dict(self):
        file_dict = super().to_dict(self.node_type)
        file_dict["extension"] = self.extension
        return file_dict
    
class Directory(FileSystemNode):
    node_type = NodeType.DIRECTORY.value
    
    def to_dict(self):
        return super().to_dict(self.node_type)
        