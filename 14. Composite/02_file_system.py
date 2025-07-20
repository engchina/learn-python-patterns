"""
组合模式实际应用 - 文件系统

这个示例展示了组合模式在文件系统中的应用，演示如何统一处理
文件和目录，实现文件系统的基本操作。

作者: Composite Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
import os


class FileSystemItem(ABC):
    """文件系统项目抽象基类"""
    
    def __init__(self, name: str, parent: Optional['Directory'] = None):
        self.name = name
        self.parent = parent
        self.created_time = datetime.now()
        self.modified_time = datetime.now()
    
    @abstractmethod
    def get_size(self) -> int:
        """获取大小（字节）"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """显示项目信息"""
        pass
    
    def get_path(self) -> str:
        """获取完整路径"""
        if self.parent is None:
            return self.name
        return os.path.join(self.parent.get_path(), self.name)
    
    def get_info(self) -> Dict[str, str]:
        """获取基本信息"""
        return {
            "name": self.name,
            "path": self.get_path(),
            "size": f"{self.get_size()} bytes",
            "created": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "modified": self.modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class File(FileSystemItem):
    """文件类 - 叶子组件"""
    
    def __init__(self, name: str, content: str = "", parent: Optional['Directory'] = None):
        super().__init__(name, parent)
        self._content = content
        self.file_type = self._get_file_type()
    
    def get_size(self) -> int:
        """获取文件大小"""
        return len(self._content.encode('utf-8'))
    
    def display(self, indent: int = 0) -> str:
        """显示文件信息"""
        prefix = "  " * indent
        icon = self._get_file_icon()
        return f"{prefix}{icon} {self.name} ({self.get_size()} bytes)"
    
    def read(self) -> str:
        """读取文件内容"""
        return self._content
    
    def write(self, content: str) -> None:
        """写入文件内容"""
        self._content = content
        self.modified_time = datetime.now()
        print(f"📝 文件 '{self.name}' 已更新")
    
    def append(self, content: str) -> None:
        """追加文件内容"""
        self._content += content
        self.modified_time = datetime.now()
        print(f"➕ 内容已追加到文件 '{self.name}'")
    
    def _get_file_type(self) -> str:
        """获取文件类型"""
        if '.' in self.name:
            return self.name.split('.')[-1].lower()
        return "unknown"
    
    def _get_file_icon(self) -> str:
        """根据文件类型获取图标"""
        icons = {
            "txt": "📄", "md": "📝", "py": "🐍", "js": "📜",
            "html": "🌐", "css": "🎨", "json": "📋", "xml": "📰",
            "jpg": "🖼️", "png": "🖼️", "gif": "🖼️", "pdf": "📕",
            "mp3": "🎵", "mp4": "🎬", "zip": "📦"
        }
        return icons.get(self.file_type, "📄")


class Directory(FileSystemItem):
    """目录类 - 组合组件"""
    
    def __init__(self, name: str, parent: Optional['Directory'] = None):
        super().__init__(name, parent)
        self._children: List[FileSystemItem] = []
    
    def get_size(self) -> int:
        """获取目录总大小"""
        return sum(child.get_size() for child in self._children)
    
    def display(self, indent: int = 0) -> str:
        """显示目录结构"""
        prefix = "  " * indent
        result = [f"{prefix}📁 {self.name}/ ({len(self._children)} items, {self.get_size()} bytes)"]
        
        # 按类型排序：目录在前，文件在后
        sorted_children = sorted(self._children, 
                               key=lambda x: (isinstance(x, File), x.name))
        
        for child in sorted_children:
            result.append(child.display(indent + 1))
        
        return "\n".join(result)
    
    def add_item(self, item: FileSystemItem) -> None:
        """添加文件或子目录"""
        if self.find_item(item.name):
            print(f"⚠️  '{item.name}' 已存在于目录 '{self.name}' 中")
            return
        
        item.parent = self
        self._children.append(item)
        self.modified_time = datetime.now()
        
        item_type = "目录" if isinstance(item, Directory) else "文件"
        print(f"✅ {item_type} '{item.name}' 已添加到 '{self.name}'")
    
    def remove_item(self, name: str) -> bool:
        """移除文件或子目录"""
        item = self.find_item(name)
        if item:
            self._children.remove(item)
            item.parent = None
            self.modified_time = datetime.now()
            
            item_type = "目录" if isinstance(item, Directory) else "文件"
            print(f"❌ {item_type} '{name}' 已从 '{self.name}' 中移除")
            return True
        else:
            print(f"⚠️  '{name}' 不存在于目录 '{self.name}' 中")
            return False
    
    def find_item(self, name: str) -> Optional[FileSystemItem]:
        """在当前目录中查找项目"""
        for child in self._children:
            if child.name == name:
                return child
        return None
    
    def find_item_recursive(self, name: str) -> Optional[FileSystemItem]:
        """递归查找项目"""
        # 先在当前目录查找
        item = self.find_item(name)
        if item:
            return item
        
        # 在子目录中递归查找
        for child in self._children:
            if isinstance(child, Directory):
                found = child.find_item_recursive(name)
                if found:
                    return found
        
        return None
    
    def list_contents(self) -> List[str]:
        """列出目录内容"""
        return [child.name for child in self._children]
    
    def get_files_by_type(self, file_type: str) -> List[File]:
        """按类型获取文件"""
        files = []
        for child in self._children:
            if isinstance(child, File) and child.file_type == file_type:
                files.append(child)
            elif isinstance(child, Directory):
                files.extend(child.get_files_by_type(file_type))
        return files
    
    def get_statistics(self) -> Dict[str, int]:
        """获取目录统计信息"""
        stats = {"files": 0, "directories": 0, "total_size": 0}
        
        for child in self._children:
            if isinstance(child, File):
                stats["files"] += 1
                stats["total_size"] += child.get_size()
            elif isinstance(child, Directory):
                stats["directories"] += 1
                child_stats = child.get_statistics()
                stats["files"] += child_stats["files"]
                stats["directories"] += child_stats["directories"]
                stats["total_size"] += child_stats["total_size"]
        
        return stats


def demo_file_system():
    """文件系统演示"""
    print("=" * 60)
    print("💾 文件系统管理 - 组合模式演示")
    print("=" * 60)
    
    # 创建根目录
    root = Directory("root")
    
    # 创建子目录
    documents = Directory("Documents")
    projects = Directory("Projects")
    pictures = Directory("Pictures")
    
    # 创建文件
    readme = File("README.md", "# 项目说明\n这是一个示例项目，展示组合模式的应用。")
    config = File("config.json", '{"debug": true, "port": 8080}')
    script = File("main.py", "print('Hello, Composite Pattern!')")
    
    # 构建目录结构
    print("\n📁 构建目录结构:")
    root.add_item(documents)
    root.add_item(projects)
    root.add_item(pictures)
    
    documents.add_item(readme)
    documents.add_item(config)
    
    # 创建项目子目录
    python_project = Directory("python-app")
    web_project = Directory("web-app")
    
    projects.add_item(python_project)
    projects.add_item(web_project)
    
    python_project.add_item(script)
    python_project.add_item(File("requirements.txt", "requests==2.25.1\nnumpy==1.21.0"))
    
    web_project.add_item(File("index.html", "<html><body><h1>Hello World</h1></body></html>"))
    web_project.add_item(File("style.css", "body { font-family: Arial; }"))
    
    # 添加图片文件
    pictures.add_item(File("vacation.jpg", "二进制图片数据..." * 100))
    pictures.add_item(File("family.png", "二进制图片数据..." * 80))
    
    # 显示文件系统结构
    print(f"\n🗂️  文件系统结构:")
    print(root.display())
    
    # 显示统计信息
    print(f"\n📊 统计信息:")
    stats = root.get_statistics()
    print(f"  • 文件数量: {stats['files']}")
    print(f"  • 目录数量: {stats['directories']}")
    print(f"  • 总大小: {stats['total_size']} bytes")


if __name__ == "__main__":
    demo_file_system()
