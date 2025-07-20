"""
04_web_elements.py - 网页元素享元

这个示例展示了享元模式在Web开发中的应用。
HTML元素的标签类型、样式类等作为内在状态被共享，
而元素的内容、位置、特定属性等作为外在状态维护。
"""

from typing import Dict, List, Any
from abc import ABC, abstractmethod
from enum import Enum


class ElementType(Enum):
    """HTML元素类型枚举"""
    DIV = "div"
    SPAN = "span"
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    BUTTON = "button"
    INPUT = "input"
    IMG = "img"
    A = "a"


# ==================== HTML元素享元接口 ====================
class HTMLElementFlyweight(ABC):
    """HTML元素享元抽象接口"""
    
    @abstractmethod
    def render(self, extrinsic_state: Dict) -> str:
        """渲染HTML元素"""
        pass
    
    @abstractmethod
    def get_element_info(self) -> str:
        """获取元素信息"""
        pass


# ==================== 具体HTML元素享元 ====================
class HTMLElement(HTMLElementFlyweight):
    """HTML元素享元实现"""
    
    def __init__(self, element_type: ElementType, css_class: str = "", 
                 default_styles: Dict[str, str] = None):
        """
        初始化HTML元素享元
        
        Args:
            element_type: 元素类型（内在状态）
            css_class: CSS类名（内在状态）
            default_styles: 默认样式（内在状态）
        """
        self._element_type = element_type
        self._css_class = css_class
        self._default_styles = default_styles or {}
        print(f"创建HTML元素享元: {element_type.value}.{css_class}")
    
    def render(self, extrinsic_state: Dict) -> str:
        """
        渲染HTML元素
        
        Args:
            extrinsic_state: 外在状态字典
            
        Returns:
            HTML字符串
        """
        content = extrinsic_state.get('content', '')
        attributes = extrinsic_state.get('attributes', {})
        inline_styles = extrinsic_state.get('styles', {})
        
        # 构建属性字符串
        attr_parts = []
        
        # 添加CSS类
        if self._css_class:
            attr_parts.append(f'class="{self._css_class}"')
        
        # 添加其他属性
        for key, value in attributes.items():
            attr_parts.append(f'{key}="{value}"')
        
        # 合并样式
        all_styles = {**self._default_styles, **inline_styles}
        if all_styles:
            style_str = '; '.join([f'{k}: {v}' for k, v in all_styles.items()])
            attr_parts.append(f'style="{style_str}"')
        
        # 构建HTML
        attr_string = ' ' + ' '.join(attr_parts) if attr_parts else ''
        
        # 自闭合标签
        if self._element_type in [ElementType.IMG, ElementType.INPUT]:
            return f'<{self._element_type.value}{attr_string} />'
        else:
            return f'<{self._element_type.value}{attr_string}>{content}</{self._element_type.value}>'
    
    def get_element_info(self) -> str:
        """获取元素信息"""
        return f"{self._element_type.value}.{self._css_class}"
    
    @property
    def element_type(self) -> ElementType:
        """获取元素类型"""
        return self._element_type


# ==================== HTML元素享元工厂 ====================
class HTMLElementFactory:
    """HTML元素享元工厂"""
    
    def __init__(self):
        self._elements: Dict[str, HTMLElement] = {}
        self._creation_count = 0
        self._access_count = 0
        
        # 预定义常用元素样式
        self._predefined_styles = {
            "button-primary": {
                "background-color": "#007bff",
                "color": "white",
                "border": "none",
                "padding": "8px 16px",
                "border-radius": "4px"
            },
            "button-secondary": {
                "background-color": "#6c757d",
                "color": "white",
                "border": "none",
                "padding": "8px 16px",
                "border-radius": "4px"
            },
            "card": {
                "border": "1px solid #dee2e6",
                "border-radius": "8px",
                "padding": "16px",
                "margin": "8px",
                "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
            },
            "title": {
                "font-weight": "bold",
                "margin": "0 0 16px 0",
                "color": "#333"
            },
            "text": {
                "line-height": "1.5",
                "color": "#666"
            }
        }
    
    def get_element(self, element_type: ElementType, css_class: str = "") -> HTMLElement:
        """
        获取HTML元素享元
        
        Args:
            element_type: 元素类型
            css_class: CSS类名
            
        Returns:
            HTML元素享元对象
        """
        key = f"{element_type.value}-{css_class}"
        self._access_count += 1
        
        if key not in self._elements:
            # 获取预定义样式
            default_styles = self._predefined_styles.get(css_class, {})
            
            self._elements[key] = HTMLElement(element_type, css_class, default_styles)
            self._creation_count += 1
            print(f"✓ 创建新HTML元素享元: {key}")
        else:
            print(f"♻️ 复用HTML元素享元: {key}")
        
        return self._elements[key]
    
    def get_element_count(self) -> int:
        """获取元素享元数量"""
        return len(self._elements)
    
    def get_statistics(self) -> Dict[str, any]:
        """获取统计信息"""
        return {
            "flyweight_count": len(self._elements),
            "creation_count": self._creation_count,
            "access_count": self._access_count,
            "reuse_rate": round((self._access_count - self._creation_count) / self._access_count * 100, 1) if self._access_count > 0 else 0
        }


# ==================== DOM元素上下文 ====================
class DOMElement:
    """DOM元素上下文 - 维护外在状态"""
    
    def __init__(self, element: HTMLElement, content: str = "", 
                 attributes: Dict[str, str] = None, styles: Dict[str, str] = None):
        """
        初始化DOM元素
        
        Args:
            element: HTML元素享元
            content: 元素内容（外在状态）
            attributes: 元素属性（外在状态）
            styles: 内联样式（外在状态）
        """
        self.element = element
        self.extrinsic_state = {
            'content': content,
            'attributes': attributes or {},
            'styles': styles or {}
        }
    
    def render(self) -> str:
        """渲染DOM元素"""
        return self.element.render(self.extrinsic_state)
    
    def set_content(self, content: str):
        """设置内容"""
        self.extrinsic_state['content'] = content
    
    def set_attribute(self, key: str, value: str):
        """设置属性"""
        self.extrinsic_state['attributes'][key] = value
    
    def set_style(self, property: str, value: str):
        """设置样式"""
        self.extrinsic_state['styles'][property] = value
    
    def add_class(self, class_name: str):
        """添加CSS类"""
        current_class = self.extrinsic_state['attributes'].get('class', '')
        if current_class:
            self.extrinsic_state['attributes']['class'] = f"{current_class} {class_name}"
        else:
            self.extrinsic_state['attributes']['class'] = class_name


# ==================== 网页构建器 ====================
class WebPageBuilder:
    """网页构建器"""
    
    def __init__(self, title: str):
        self.title = title
        self._factory = HTMLElementFactory()
        self._elements: List[DOMElement] = []
    
    def add_heading(self, text: str, level: int = 1, css_class: str = "title") -> 'WebPageBuilder':
        """添加标题"""
        element_type = {1: ElementType.H1, 2: ElementType.H2, 3: ElementType.H3}.get(level, ElementType.H1)
        element = self._factory.get_element(element_type, css_class)
        dom_element = DOMElement(element, text)
        self._elements.append(dom_element)
        return self
    
    def add_paragraph(self, text: str, css_class: str = "text") -> 'WebPageBuilder':
        """添加段落"""
        element = self._factory.get_element(ElementType.P, css_class)
        dom_element = DOMElement(element, text)
        self._elements.append(dom_element)
        return self
    
    def add_button(self, text: str, button_type: str = "primary", 
                   onclick: str = None) -> 'WebPageBuilder':
        """添加按钮"""
        css_class = f"button-{button_type}"
        element = self._factory.get_element(ElementType.BUTTON, css_class)
        
        attributes = {}
        if onclick:
            attributes['onclick'] = onclick
        
        dom_element = DOMElement(element, text, attributes)
        self._elements.append(dom_element)
        return self
    
    def add_card(self, title: str, content: str) -> 'WebPageBuilder':
        """添加卡片"""
        # 卡片容器
        card_element = self._factory.get_element(ElementType.DIV, "card")
        card_dom = DOMElement(card_element)
        
        # 卡片标题
        title_element = self._factory.get_element(ElementType.H3, "title")
        title_dom = DOMElement(title_element, title)
        
        # 卡片内容
        content_element = self._factory.get_element(ElementType.P, "text")
        content_dom = DOMElement(content_element, content)
        
        # 组合卡片内容
        card_content = title_dom.render() + content_dom.render()
        card_dom.set_content(card_content)
        
        self._elements.append(card_dom)
        return self
    
    def add_input(self, input_type: str = "text", placeholder: str = "", 
                  name: str = "") -> 'WebPageBuilder':
        """添加输入框"""
        element = self._factory.get_element(ElementType.INPUT)
        
        attributes = {
            'type': input_type,
            'placeholder': placeholder,
            'name': name
        }
        
        dom_element = DOMElement(element, "", attributes)
        self._elements.append(dom_element)
        return self
    
    def add_image(self, src: str, alt: str = "", width: str = "", 
                  height: str = "") -> 'WebPageBuilder':
        """添加图片"""
        element = self._factory.get_element(ElementType.IMG)
        
        attributes = {
            'src': src,
            'alt': alt
        }
        
        if width:
            attributes['width'] = width
        if height:
            attributes['height'] = height
        
        dom_element = DOMElement(element, "", attributes)
        self._elements.append(dom_element)
        return self
    
    def render_html(self) -> str:
        """渲染完整HTML"""
        html_parts = [
            f"<!DOCTYPE html>",
            f"<html>",
            f"<head>",
            f"    <title>{self.title}</title>",
            f"    <meta charset='UTF-8'>",
            f"</head>",
            f"<body>",
        ]
        
        for element in self._elements:
            html_parts.append(f"    {element.render()}")
        
        html_parts.extend([
            f"</body>",
            f"</html>"
        ])
        
        return "\n".join(html_parts)
    
    def render_preview(self, max_elements: int = 15):
        """渲染网页预览"""
        print(f"\n🌐 网页预览: {self.title}")
        print("=" * 60)
        
        elements_to_show = min(max_elements, len(self._elements))
        for i in range(elements_to_show):
            element_html = self._elements[i].render()
            print(f"  {i+1:2d}. {element_html}")
        
        if len(self._elements) > max_elements:
            print(f"  ... 还有 {len(self._elements) - max_elements} 个元素")
    
    def get_statistics(self):
        """获取网页统计信息"""
        factory_stats = self._factory.get_statistics()
        
        print(f"\n📊 网页统计信息: {self.title}")
        print(f"  • DOM元素数量: {len(self._elements)}")
        print(f"  • HTML享元数量: {factory_stats['flyweight_count']}")
        print(f"  • 享元创建次数: {factory_stats['creation_count']}")
        print(f"  • 享元访问次数: {factory_stats['access_count']}")
        print(f"  • 享元复用率: {factory_stats['reuse_rate']}%")
        
        if len(self._elements) > 0:
            memory_saved = len(self._elements) - factory_stats['flyweight_count']
            memory_save_rate = (memory_saved / len(self._elements)) * 100
            print(f"  • 节省对象数: {memory_saved}")
            print(f"  • 内存节省率: {memory_save_rate:.1f}%")


# ==================== 使用示例 ====================
def demo_web_elements():
    """网页元素享元模式演示"""
    print("=" * 60)
    print("🌐 网页元素享元模式演示")
    print("=" * 60)
    
    # 创建网页构建器
    page_builder = WebPageBuilder("享元模式演示页面")
    
    # 构建网页内容
    page_builder.add_heading("享元模式在Web开发中的应用", 1) \
                .add_paragraph("这个示例展示了如何在Web开发中使用享元模式优化DOM元素。") \
                .add_card("什么是享元模式", "享元模式通过共享内在状态来减少对象数量，提高性能。") \
                .add_card("Web中的应用", "HTML元素的标签类型和CSS类作为内在状态被共享。") \
                .add_heading("用户操作", 2) \
                .add_input("text", "请输入您的姓名", "username") \
                .add_input("email", "请输入您的邮箱", "email") \
                .add_button("提交", "primary", "submitForm()") \
                .add_button("重置", "secondary", "resetForm()") \
                .add_heading("相关资源", 2) \
                .add_image("https://example.com/flyweight.png", "享元模式图解", "300", "200") \
                .add_paragraph("了解更多设计模式知识，请访问相关文档。")
    
    # 渲染网页预览
    page_builder.render_preview()
    
    # 显示统计信息
    page_builder.get_statistics()


def demo_large_webpage():
    """大型网页演示"""
    print("\n" + "=" * 60)
    print("📄 大型网页享元优化演示")
    print("=" * 60)
    
    # 创建大型网页
    large_page = WebPageBuilder("大型网页测试")
    
    print("\n🏗️ 构建大型网页...")
    
    # 添加大量重复元素
    large_page.add_heading("大型网页测试", 1)
    
    # 添加多个卡片
    for i in range(10):
        large_page.add_card(f"卡片 {i+1}", f"这是第 {i+1} 个卡片的内容。")
    
    # 添加多个按钮
    for i in range(8):
        button_type = "primary" if i % 2 == 0 else "secondary"
        large_page.add_button(f"按钮 {i+1}", button_type, f"action{i+1}()")
    
    # 添加多个段落
    for i in range(12):
        large_page.add_paragraph(f"这是第 {i+1} 个段落的内容。")
    
    # 显示统计信息
    large_page.get_statistics()
    
    print(f"\n💡 享元模式优化效果:")
    print(f"   如果不使用享元模式，每个DOM元素都需要独立的HTML元素对象")
    print(f"   使用享元模式后，相同类型和样式的元素共享同一个享元对象")
    print(f"   在大型网页中，可以显著减少内存使用和提高渲染性能")


def main():
    """主演示函数"""
    demo_web_elements()
    demo_large_webpage()
    
    print("\n" + "=" * 60)
    print("🎉 网页元素享元模式演示完成！")
    print("💡 关键要点:")
    print("   • HTML元素的标签类型、CSS类等作为内在状态被共享")
    print("   • 元素的内容、属性、内联样式等作为外在状态")
    print("   • 大量相同类型的元素可以共享同一个享元对象")
    print("   • 在Web开发中可以优化DOM操作和内存使用")
    print("=" * 60)


if __name__ == "__main__":
    main()
