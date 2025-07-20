"""
02_file_system.py - 文件系统的访问者应用

这个示例展示了访问者模式在文件系统中的应用：
- 文件和目录的统一处理
- 不同类型的文件系统操作
- 递归遍历的实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from datetime import datetime
import time


# ==================== 抽象访问者 ====================
class FileSystemVisitor(ABC):
    """文件系统访问者抽象类"""
    
    @abstractmethod
    def visit_file(self, file):
        """访问文件"""
        pass
    
    @abstractmethod
    def visit_directory(self, directory):
        """访问目录"""
        pass


# ==================== 抽象文件系统元素 ====================
class FileSystemElement(ABC):
    """文件系统元素抽象类"""
    
    def __init__(self, name: str, size: int = 0):
        self.name = name
        self.size = size
        self.created_time = datetime.now()
        self.modified_time = datetime.now()
    
    @abstractmethod
    def accept(self, visitor: FileSystemVisitor):
        """接受访问者"""
        pass
    
    def get_age_days(self) -> int:
        """获取文件年龄（天数）"""
        return (datetime.now() - self.created_time).days


# ==================== 具体文件系统元素 ====================
class File(FileSystemElement):
    """文件类"""
    
    def __init__(self, name: str, size: int, file_type: str = "unknown"):
        super().__init__(name, size)
        self.file_type = file_type
        self.extension = self._get_extension()
    
    def _get_extension(self) -> str:
        """获取文件扩展名"""
        return os.path.splitext(self.name)[1].lower() if '.' in self.name else ""
    
    def accept(self, visitor: FileSystemVisitor):
        """接受访问者"""
        visitor.visit_file(self)
    
    def is_image(self) -> bool:
        """判断是否为图片文件"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}
        return self.extension in image_extensions
    
    def is_document(self) -> bool:
        """判断是否为文档文件"""
        doc_extensions = {'.txt', '.doc', '.docx', '.pdf', '.md', '.rtf'}
        return self.extension in doc_extensions
    
    def is_code(self) -> bool:
        """判断是否为代码文件"""
        code_extensions = {'.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.sql'}
        return self.extension in code_extensions
    
    def __str__(self):
        return f"文件: {self.name} ({self.size} bytes)"


class Directory(FileSystemElement):
    """目录类"""
    
    def __init__(self, name: str):
        super().__init__(name, 0)
        self.children: List[FileSystemElement] = []
        self.file_count = 0
        self.directory_count = 0
    
    def add_child(self, child: FileSystemElement):
        """添加子元素"""
        self.children.append(child)
        self.size += child.size
        
        if isinstance(child, File):
            self.file_count += 1
        elif isinstance(child, Directory):
            self.directory_count += 1
            self.file_count += child.file_count
            self.directory_count += child.directory_count
    
    def accept(self, visitor: FileSystemVisitor):
        """接受访问者"""
        visitor.visit_directory(self)
        # 递归访问所有子元素
        for child in self.children:
            child.accept(visitor)
    
    def get_total_files(self) -> int:
        """获取总文件数"""
        return self.file_count
    
    def get_total_directories(self) -> int:
        """获取总目录数"""
        return self.directory_count
    
    def __str__(self):
        return f"目录: {self.name}/ ({self.file_count} 文件, {self.directory_count} 目录)"


# ==================== 具体访问者 ====================
class SizeCalculatorVisitor(FileSystemVisitor):
    """大小统计访问者"""
    
    def __init__(self):
        self.total_size = 0
        self.file_count = 0
        self.directory_count = 0
        self.largest_file = None
        self.largest_file_size = 0
    
    def visit_file(self, file: File):
        """访问文件"""
        self.total_size += file.size
        self.file_count += 1
        
        if file.size > self.largest_file_size:
            self.largest_file = file
            self.largest_file_size = file.size
        
        print(f"📄 文件: {file.name} ({file.size:,} bytes)")
    
    def visit_directory(self, directory: Directory):
        """访问目录"""
        self.directory_count += 1
        print(f"📁 目录: {directory.name}/")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_size": self.total_size,
            "file_count": self.file_count,
            "directory_count": self.directory_count,
            "largest_file": self.largest_file.name if self.largest_file else None,
            "largest_file_size": self.largest_file_size,
            "average_file_size": self.total_size / self.file_count if self.file_count > 0 else 0
        }
    
    def print_summary(self):
        """打印统计摘要"""
        stats = self.get_statistics()
        print(f"\n📊 大小统计摘要:")
        print(f"   总大小: {stats['total_size']:,} bytes ({stats['total_size']/1024/1024:.2f} MB)")
        print(f"   文件数: {stats['file_count']}")
        print(f"   目录数: {stats['directory_count']}")
        print(f"   平均文件大小: {stats['average_file_size']:.0f} bytes")
        if stats['largest_file']:
            print(f"   最大文件: {stats['largest_file']} ({stats['largest_file_size']:,} bytes)")


class SearchVisitor(FileSystemVisitor):
    """搜索访问者"""
    
    def __init__(self, pattern: str, case_sensitive: bool = False):
        self.pattern = pattern if case_sensitive else pattern.lower()
        self.case_sensitive = case_sensitive
        self.found_files: List[File] = []
        self.found_directories: List[Directory] = []
    
    def visit_file(self, file: File):
        """访问文件"""
        name_to_check = file.name if self.case_sensitive else file.name.lower()
        if self.pattern in name_to_check:
            self.found_files.append(file)
            print(f"🔍 找到文件: {file.name}")
    
    def visit_directory(self, directory: Directory):
        """访问目录"""
        name_to_check = directory.name if self.case_sensitive else directory.name.lower()
        if self.pattern in name_to_check:
            self.found_directories.append(directory)
            print(f"🔍 找到目录: {directory.name}/")
    
    def get_results(self) -> Dict[str, List]:
        """获取搜索结果"""
        return {
            "files": self.found_files,
            "directories": self.found_directories,
            "total_found": len(self.found_files) + len(self.found_directories)
        }
    
    def print_summary(self):
        """打印搜索摘要"""
        results = self.get_results()
        print(f"\n🔍 搜索结果 (模式: '{self.pattern}'):")
        print(f"   找到文件: {len(results['files'])} 个")
        print(f"   找到目录: {len(results['directories'])} 个")
        print(f"   总计: {results['total_found']} 项")


class TypeAnalyzerVisitor(FileSystemVisitor):
    """文件类型分析访问者"""
    
    def __init__(self):
        self.type_stats: Dict[str, Dict[str, Any]] = {}
        self.large_files: List[File] = []
        self.old_files: List[File] = []
        self.large_file_threshold = 1000000  # 1MB
        self.old_file_threshold = 30  # 30天
    
    def visit_file(self, file: File):
        """访问文件"""
        # 统计文件类型
        file_type = self._categorize_file(file)
        if file_type not in self.type_stats:
            self.type_stats[file_type] = {
                "count": 0,
                "total_size": 0,
                "extensions": set()
            }
        
        self.type_stats[file_type]["count"] += 1
        self.type_stats[file_type]["total_size"] += file.size
        if file.extension:
            self.type_stats[file_type]["extensions"].add(file.extension)
        
        # 检查大文件
        if file.size > self.large_file_threshold:
            self.large_files.append(file)
        
        # 检查旧文件
        if file.get_age_days() > self.old_file_threshold:
            self.old_files.append(file)
        
        print(f"📊 分析文件: {file.name} -> {file_type}")
    
    def visit_directory(self, directory: Directory):
        """访问目录"""
        print(f"📊 分析目录: {directory.name}/")
    
    def _categorize_file(self, file: File) -> str:
        """文件分类"""
        if file.is_image():
            return "图片"
        elif file.is_document():
            return "文档"
        elif file.is_code():
            return "代码"
        elif file.extension in {'.mp3', '.wav', '.flac', '.aac'}:
            return "音频"
        elif file.extension in {'.mp4', '.avi', '.mkv', '.mov'}:
            return "视频"
        elif file.extension in {'.zip', '.rar', '.7z', '.tar', '.gz'}:
            return "压缩包"
        else:
            return "其他"
    
    def print_analysis(self):
        """打印分析结果"""
        print(f"\n📊 文件类型分析:")
        print("-" * 50)
        
        for file_type, stats in sorted(self.type_stats.items()):
            avg_size = stats["total_size"] / stats["count"]
            extensions = ", ".join(sorted(stats["extensions"])) if stats["extensions"] else "无扩展名"
            
            print(f"📂 {file_type}:")
            print(f"   数量: {stats['count']} 个")
            print(f"   总大小: {stats['total_size']:,} bytes ({stats['total_size']/1024/1024:.2f} MB)")
            print(f"   平均大小: {avg_size:.0f} bytes")
            print(f"   扩展名: {extensions}")
            print()
        
        # 大文件报告
        if self.large_files:
            print(f"🔍 大文件报告 (>{self.large_file_threshold/1024/1024:.1f}MB):")
            for file in sorted(self.large_files, key=lambda f: f.size, reverse=True)[:5]:
                print(f"   {file.name}: {file.size:,} bytes ({file.size/1024/1024:.2f} MB)")
            print()
        
        # 旧文件报告
        if self.old_files:
            print(f"📅 旧文件报告 (>{self.old_file_threshold}天):")
            for file in sorted(self.old_files, key=lambda f: f.get_age_days(), reverse=True)[:5]:
                print(f"   {file.name}: {file.get_age_days()} 天前")


class CleanupVisitor(FileSystemVisitor):
    """清理建议访问者"""
    
    def __init__(self):
        self.duplicate_candidates: Dict[int, List[File]] = {}
        self.empty_directories: List[Directory] = []
        self.cleanup_suggestions: List[str] = []
        self.total_cleanup_size = 0
    
    def visit_file(self, file: File):
        """访问文件"""
        # 按大小分组，寻找可能的重复文件
        if file.size in self.duplicate_candidates:
            self.duplicate_candidates[file.size].append(file)
        else:
            self.duplicate_candidates[file.size] = [file]
        
        # 检查临时文件
        if file.name.startswith('~') or file.name.endswith('.tmp'):
            self.cleanup_suggestions.append(f"删除临时文件: {file.name}")
            self.total_cleanup_size += file.size
        
        print(f"🧹 检查文件: {file.name}")
    
    def visit_directory(self, directory: Directory):
        """访问目录"""
        # 检查空目录
        if not directory.children:
            self.empty_directories.append(directory)
            self.cleanup_suggestions.append(f"删除空目录: {directory.name}/")
        
        print(f"🧹 检查目录: {directory.name}/")
    
    def print_cleanup_suggestions(self):
        """打印清理建议"""
        print(f"\n🧹 清理建议:")
        print("-" * 50)
        
        # 重复文件候选
        duplicates = {size: files for size, files in self.duplicate_candidates.items() if len(files) > 1}
        if duplicates:
            print("🔄 可能的重复文件:")
            for size, files in list(duplicates.items())[:3]:  # 只显示前3组
                print(f"   大小 {size} bytes 的文件:")
                for file in files:
                    print(f"     - {file.name}")
            print()
        
        # 空目录
        if self.empty_directories:
            print("📁 空目录:")
            for directory in self.empty_directories[:5]:  # 只显示前5个
                print(f"   - {directory.name}/")
            print()
        
        # 其他清理建议
        if self.cleanup_suggestions:
            print("💡 清理建议:")
            for suggestion in self.cleanup_suggestions[:5]:  # 只显示前5个
                print(f"   - {suggestion}")
            print()
        
        print(f"💾 预计可释放空间: {self.total_cleanup_size:,} bytes ({self.total_cleanup_size/1024/1024:.2f} MB)")


# ==================== 演示函数 ====================
def create_sample_file_system() -> Directory:
    """创建示例文件系统"""
    print("🏗️  创建示例文件系统...")
    
    # 根目录
    root = Directory("项目根目录")
    
    # 文档目录
    docs = Directory("documents")
    docs.add_child(File("readme.txt", 1500, "text"))
    docs.add_child(File("用户手册.pdf", 2500000, "pdf"))
    docs.add_child(File("设计文档.docx", 850000, "document"))
    docs.add_child(File("~temp.tmp", 100, "temp"))  # 临时文件
    
    # 图片目录
    images = Directory("images")
    images.add_child(File("logo.png", 45000, "image"))
    images.add_child(File("banner.jpg", 120000, "image"))
    images.add_child(File("icon.svg", 8000, "image"))
    images.add_child(File("photo1.jpg", 2800000, "image"))  # 大文件
    
    # 代码目录
    code = Directory("src")
    code.add_child(File("main.py", 3500, "python"))
    code.add_child(File("utils.py", 1200, "python"))
    code.add_child(File("config.json", 800, "json"))
    code.add_child(File("style.css", 2200, "css"))
    
    # 空目录
    empty_dir = Directory("empty_folder")
    
    # 媒体目录
    media = Directory("media")
    media.add_child(File("intro.mp4", 15000000, "video"))  # 大文件
    media.add_child(File("sound.mp3", 3500000, "audio"))
    
    # 构建目录结构
    root.add_child(docs)
    root.add_child(images)
    root.add_child(code)
    root.add_child(empty_dir)
    root.add_child(media)
    root.add_child(File("license.txt", 1200, "text"))
    root.add_child(File("changelog.md", 2800, "markdown"))
    
    print(f"✅ 文件系统创建完成: {root}")
    return root


def demo_file_system_visitor():
    """文件系统访问者演示"""
    print("=" * 80)
    print("📁 文件系统访问者模式演示")
    print("=" * 80)
    
    # 创建示例文件系统
    root = create_sample_file_system()
    
    # 创建不同的访问者
    visitors = [
        ("大小统计器", SizeCalculatorVisitor()),
        ("搜索器", SearchVisitor("py")),
        ("类型分析器", TypeAnalyzerVisitor()),
        ("清理建议器", CleanupVisitor())
    ]
    
    # 使用不同访问者处理文件系统
    for name, visitor in visitors:
        print(f"\n{'='*20} {name} {'='*20}")
        start_time = time.time()
        
        root.accept(visitor)
        
        end_time = time.time()
        print(f"\n⏱️  处理时间: {end_time - start_time:.3f} 秒")
        
        # 显示处理结果
        if isinstance(visitor, SizeCalculatorVisitor):
            visitor.print_summary()
        elif isinstance(visitor, SearchVisitor):
            visitor.print_summary()
        elif isinstance(visitor, TypeAnalyzerVisitor):
            visitor.print_analysis()
        elif isinstance(visitor, CleanupVisitor):
            visitor.print_cleanup_suggestions()
    
    print("\n" + "=" * 80)
    print("🎉 文件系统访问者演示完成!")
    print("💡 关键点:")
    print("   - 访问者可以递归遍历复杂的文件系统结构")
    print("   - 不同访问者实现不同的文件系统操作")
    print("   - 可以轻松添加新的文件系统分析功能")
    print("=" * 80)


if __name__ == "__main__":
    demo_file_system_visitor()
