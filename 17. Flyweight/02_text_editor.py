"""
02_text_editor.py - 文本编辑器中的字符享元

这个示例展示了享元模式在文本编辑器中的应用。
字符的字体、大小等属性作为内在状态被共享，
而位置、颜色等作为外在状态由上下文维护。
"""

import random
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod


# ==================== 字符享元接口 ====================
class CharacterFlyweight(ABC):
    """字符享元抽象接口"""
    
    @abstractmethod
    def render(self, extrinsic_state: Tuple) -> str:
        """渲染字符"""
        pass
    
    @abstractmethod
    def get_intrinsic_info(self) -> str:
        """获取内在状态信息"""
        pass


# ==================== 具体字符享元 ====================
class Character(CharacterFlyweight):
    """字符享元实现"""
    
    def __init__(self, char: str, font: str, size: int, style: str = "normal"):
        """
        初始化字符享元
        
        Args:
            char: 字符内容（内在状态）
            font: 字体（内在状态）
            size: 字体大小（内在状态）
            style: 字体样式（内在状态）
        """
        self._char = char
        self._font = font
        self._size = size
        self._style = style
        print(f"创建字符享元: '{char}' {font}-{size}-{style}")
    
    def render(self, extrinsic_state: Tuple) -> str:
        """
        渲染字符
        
        Args:
            extrinsic_state: (position, color, background) 外在状态
            
        Returns:
            渲染结果字符串
        """
        position, color, background = extrinsic_state
        return (f"字符'{self._char}' "
                f"[字体:{self._font} 大小:{self._size} 样式:{self._style}] "
                f"位置:{position} 颜色:{color} 背景:{background}")
    
    def get_intrinsic_info(self) -> str:
        """获取内在状态信息"""
        return f"{self._char}-{self._font}-{self._size}-{self._style}"
    
    @property
    def character(self) -> str:
        """获取字符"""
        return self._char


# ==================== 字符享元工厂 ====================
class CharacterFactory:
    """字符享元工厂"""
    
    def __init__(self):
        self._characters: Dict[str, Character] = {}
        self._creation_count = 0
        self._access_count = 0
    
    def get_character(self, char: str, font: str, size: int, style: str = "normal") -> Character:
        """
        获取字符享元
        
        Args:
            char: 字符
            font: 字体
            size: 字体大小
            style: 字体样式
            
        Returns:
            字符享元对象
        """
        key = f"{char}-{font}-{size}-{style}"
        self._access_count += 1
        
        if key not in self._characters:
            self._characters[key] = Character(char, font, size, style)
            self._creation_count += 1
            print(f"✓ 创建新字符享元: {key}")
        else:
            print(f"♻️ 复用字符享元: {key}")
        
        return self._characters[key]
    
    def get_character_count(self) -> int:
        """获取字符享元数量"""
        return len(self._characters)
    
    def get_statistics(self) -> Dict[str, any]:
        """获取统计信息"""
        return {
            "flyweight_count": len(self._characters),
            "creation_count": self._creation_count,
            "access_count": self._access_count,
            "reuse_rate": round((self._access_count - self._creation_count) / self._access_count * 100, 1) if self._access_count > 0 else 0
        }
    
    def list_characters(self):
        """列出所有字符享元"""
        print(f"\n📋 字符工厂包含 {len(self._characters)} 个字符享元:")
        for key, char in self._characters.items():
            print(f"  • {key}")


# ==================== 文档字符上下文 ====================
class DocumentCharacter:
    """文档中的字符上下文"""
    
    def __init__(self, character: Character, position: Tuple[int, int], 
                 color: str, background: str = "white"):
        """
        初始化文档字符
        
        Args:
            character: 字符享元
            position: 位置（外在状态）
            color: 颜色（外在状态）
            background: 背景色（外在状态）
        """
        self.character = character
        self.position = position
        self.color = color
        self.background = background
    
    def render(self) -> str:
        """渲染字符"""
        extrinsic_state = (self.position, self.color, self.background)
        return self.character.render(extrinsic_state)
    
    def move_to(self, new_position: Tuple[int, int]):
        """移动字符位置"""
        self.position = new_position
    
    def change_color(self, new_color: str):
        """改变字符颜色"""
        self.color = new_color


# ==================== 文档类 ====================
class Document:
    """文档类"""
    
    def __init__(self, title: str):
        self.title = title
        self._characters: List[DocumentCharacter] = []
        self._factory = CharacterFactory()
    
    def add_text(self, text: str, font: str = "Arial", size: int = 12, 
                 style: str = "normal", color: str = "black", 
                 start_position: Tuple[int, int] = (0, 0)):
        """
        添加文本到文档
        
        Args:
            text: 文本内容
            font: 字体
            size: 字体大小
            style: 字体样式
            color: 字体颜色
            start_position: 起始位置
        """
        print(f"\n📝 添加文本: '{text}' ({font}-{size}-{style})")
        
        x, y = start_position
        char_width = size // 2  # 简化的字符宽度计算
        
        for i, char in enumerate(text):
            if char == ' ':
                x += char_width
                continue
            
            # 获取字符享元
            character_flyweight = self._factory.get_character(char, font, size, style)
            
            # 创建文档字符上下文
            position = (x, y)
            doc_char = DocumentCharacter(character_flyweight, position, color)
            self._characters.append(doc_char)
            
            x += char_width
    
    def add_formatted_text(self, text: str, formats: List[Dict]):
        """
        添加格式化文本
        
        Args:
            text: 文本内容
            formats: 格式列表，每个格式包含字体信息和应用范围
        """
        print(f"\n🎨 添加格式化文本: '{text}'")
        
        for fmt in formats:
            start_idx = fmt.get('start', 0)
            end_idx = fmt.get('end', len(text))
            font = fmt.get('font', 'Arial')
            size = fmt.get('size', 12)
            style = fmt.get('style', 'normal')
            color = fmt.get('color', 'black')
            
            segment = text[start_idx:end_idx]
            position = (start_idx * 6, len(self._characters) // 50 * 20)  # 简化的位置计算
            
            self.add_text(segment, font, size, style, color, position)
    
    def render_preview(self, max_chars: int = 20):
        """渲染文档预览"""
        print(f"\n📄 文档预览: {self.title}")
        print("=" * 60)
        
        chars_to_show = min(max_chars, len(self._characters))
        for i in range(chars_to_show):
            char_info = self._characters[i].render()
            print(f"  {i+1:2d}. {char_info}")
        
        if len(self._characters) > max_chars:
            print(f"  ... 还有 {len(self._characters) - max_chars} 个字符")
    
    def get_text_content(self) -> str:
        """获取文档的纯文本内容"""
        return ''.join(char.character.character for char in self._characters)
    
    def get_statistics(self):
        """获取文档统计信息"""
        total_chars = len(self._characters)
        factory_stats = self._factory.get_statistics()
        
        print(f"\n📊 文档统计信息:")
        print(f"  • 文档标题: {self.title}")
        print(f"  • 总字符数: {total_chars}")
        print(f"  • 字符享元数: {factory_stats['flyweight_count']}")
        print(f"  • 享元创建次数: {factory_stats['creation_count']}")
        print(f"  • 享元访问次数: {factory_stats['access_count']}")
        print(f"  • 享元复用率: {factory_stats['reuse_rate']}%")
        
        if total_chars > 0:
            memory_saved = total_chars - factory_stats['flyweight_count']
            memory_save_rate = (memory_saved / total_chars) * 100
            print(f"  • 节省对象数: {memory_saved}")
            print(f"  • 内存节省率: {memory_save_rate:.1f}%")
    
    def search_and_highlight(self, keyword: str, highlight_color: str = "yellow"):
        """搜索并高亮关键词"""
        print(f"\n🔍 搜索关键词: '{keyword}'")
        
        text_content = self.get_text_content()
        found_positions = []
        
        start = 0
        while True:
            pos = text_content.find(keyword, start)
            if pos == -1:
                break
            found_positions.append(pos)
            start = pos + 1
        
        if found_positions:
            print(f"找到 {len(found_positions)} 个匹配项")
            for pos in found_positions:
                for i in range(len(keyword)):
                    if pos + i < len(self._characters):
                        self._characters[pos + i].change_color(highlight_color)
            print(f"已将匹配项高亮为 {highlight_color}")
        else:
            print("未找到匹配项")


# ==================== 使用示例 ====================
def demo_text_editor():
    """文本编辑器享元模式演示"""
    print("=" * 60)
    print("📝 文本编辑器享元模式演示")
    print("=" * 60)
    
    # 创建文档
    document = Document("享元模式演示文档")
    
    # 添加标题
    document.add_text("享元模式演示", "Times", 18, "bold", "blue")
    
    # 添加正文
    document.add_text("这是一个展示享元模式的示例文档。", "Arial", 12, "normal", "black")
    document.add_text("享元模式通过共享内在状态来减少内存使用。", "Arial", 12, "normal", "black")
    
    # 添加格式化文本
    formats = [
        {"start": 0, "end": 4, "font": "Arial", "size": 14, "style": "bold", "color": "red"},
        {"start": 4, "end": 8, "font": "Arial", "size": 12, "style": "italic", "color": "green"},
        {"start": 8, "end": 12, "font": "Courier", "size": 10, "style": "normal", "color": "blue"}
    ]
    document.add_formatted_text("重要提示信息", formats)
    
    # 渲染文档预览
    document.render_preview(15)
    
    # 搜索和高亮
    document.search_and_highlight("享元")
    
    # 显示统计信息
    document.get_statistics()
    
    # 列出字符享元
    document._factory.list_characters()


def demo_large_document():
    """大文档演示"""
    print("\n" + "=" * 60)
    print("📚 大文档享元优化演示")
    print("=" * 60)
    
    # 创建大文档
    large_doc = Document("大文档测试")
    
    # 模拟添加大量文本
    sample_texts = [
        "Python是一种高级编程语言。",
        "享元模式是结构型设计模式。",
        "设计模式提高代码复用性。",
        "面向对象编程的重要概念。",
        "软件工程的最佳实践。"
    ]
    
    fonts = ["Arial", "Times", "Courier"]
    sizes = [10, 12, 14]
    styles = ["normal", "bold", "italic"]
    colors = ["black", "blue", "red", "green"]
    
    print("\n📝 生成大量文本...")
    for i in range(20):  # 添加20段文本
        text = random.choice(sample_texts)
        font = random.choice(fonts)
        size = random.choice(sizes)
        style = random.choice(styles)
        color = random.choice(colors)
        
        large_doc.add_text(text, font, size, style, color)
    
    # 显示统计信息
    large_doc.get_statistics()
    
    print(f"\n💡 享元模式优化效果:")
    print(f"   如果不使用享元模式，需要为每个字符创建独立对象")
    print(f"   使用享元模式后，相同格式的字符共享同一个享元对象")
    print(f"   大大减少了内存使用和对象创建开销")


def main():
    """主演示函数"""
    demo_text_editor()
    demo_large_document()
    
    print("\n" + "=" * 60)
    print("🎉 文本编辑器享元模式演示完成！")
    print("💡 关键要点:")
    print("   • 字符的字体、大小、样式作为内在状态被共享")
    print("   • 字符的位置、颜色作为外在状态由上下文维护")
    print("   • 大量相同格式的字符可以共享同一个享元对象")
    print("   • 显著减少了内存使用，特别是在大文档中")
    print("=" * 60)


if __name__ == "__main__":
    main()
