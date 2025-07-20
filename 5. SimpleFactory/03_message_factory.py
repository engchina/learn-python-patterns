"""
03_message_factory.py - 消息处理器工厂简单工厂模式

消息处理器工厂示例
这个示例展示了简单工厂模式在消息处理系统中的应用。
我们有不同类型的消息处理器（文本、HTML、JSON、XML等），通过一个消息工厂来创建这些处理器。
体现了简单工厂模式在实际业务场景中的价值。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import html
import time
from datetime import datetime


# ==================== 抽象产品 ====================
class MessageProcessor(ABC):
    """消息处理器抽象基类"""
    
    def __init__(self, name: str, content_type: str):
        self.name = name
        self.content_type = content_type
        self.processed_count = 0
    
    @abstractmethod
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理消息内容"""
        pass
    
    @abstractmethod
    def validate(self, content: str) -> bool:
        """验证消息内容格式"""
        pass
    
    @abstractmethod
    def get_format_info(self) -> Dict[str, str]:
        """获取格式信息"""
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        return {
            "name": self.name,
            "content_type": self.content_type,
            "processed_count": self.processed_count
        }


# ==================== 具体产品 ====================
class TextMessageProcessor(MessageProcessor):
    """文本消息处理器"""
    
    def __init__(self):
        super().__init__("文本消息处理器", "text/plain")
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理文本消息"""
        if not self.validate(content):
            raise ValueError("无效的文本内容")
        
        # 文本处理逻辑
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.split('\n'))
        
        # 可选的文本清理
        clean_content = content.strip()
        if kwargs.get("remove_extra_spaces", False):
            clean_content = ' '.join(clean_content.split())
        
        self.processed_count += 1
        
        result = {
            "original_content": content,
            "processed_content": clean_content,
            "word_count": word_count,
            "char_count": char_count,
            "line_count": line_count,
            "processing_time": datetime.now().isoformat()
        }
        
        print(f"📝 文本消息处理完成: {word_count} 个单词, {char_count} 个字符")
        return result
    
    def validate(self, content: str) -> bool:
        """验证文本内容"""
        return isinstance(content, str) and len(content.strip()) > 0
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "纯文本",
            "encoding": "UTF-8",
            "description": "处理纯文本消息，提供字数统计和基本清理功能"
        }


class HTMLMessageProcessor(MessageProcessor):
    """HTML消息处理器"""
    
    def __init__(self):
        super().__init__("HTML消息处理器", "text/html")
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理HTML消息"""
        if not self.validate(content):
            raise ValueError("无效的HTML内容")
        
        # HTML处理逻辑
        # 提取纯文本（简单实现）
        import re
        text_content = re.sub(r'<[^>]+>', '', content)
        text_content = html.unescape(text_content).strip()
        
        # 统计HTML标签
        tags = re.findall(r'<(\w+)', content)
        tag_counts = {}
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 可选的HTML清理
        if kwargs.get("escape_html", False):
            processed_content = html.escape(content)
        else:
            processed_content = content
        
        self.processed_count += 1
        
        result = {
            "original_content": content,
            "processed_content": processed_content,
            "text_content": text_content,
            "tag_counts": tag_counts,
            "total_tags": len(tags),
            "processing_time": datetime.now().isoformat()
        }
        
        print(f"🌐 HTML消息处理完成: {len(tags)} 个标签, 提取文本 {len(text_content)} 字符")
        return result
    
    def validate(self, content: str) -> bool:
        """验证HTML内容"""
        if not isinstance(content, str):
            return False
        # 简单的HTML验证：包含HTML标签
        import re
        return bool(re.search(r'<[^>]+>', content))
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "HTML",
            "encoding": "UTF-8",
            "description": "处理HTML消息，提供标签统计和文本提取功能"
        }


class JSONMessageProcessor(MessageProcessor):
    """JSON消息处理器"""
    
    def __init__(self):
        super().__init__("JSON消息处理器", "application/json")
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理JSON消息"""
        if not self.validate(content):
            raise ValueError("无效的JSON内容")
        
        try:
            # 解析JSON
            json_data = json.loads(content)
            
            # JSON分析
            def analyze_json(obj, path="root"):
                """递归分析JSON结构"""
                if isinstance(obj, dict):
                    return {
                        "type": "object",
                        "keys": list(obj.keys()),
                        "key_count": len(obj),
                        "nested": {k: analyze_json(v, f"{path}.{k}") for k, v in obj.items()}
                    }
                elif isinstance(obj, list):
                    return {
                        "type": "array",
                        "length": len(obj),
                        "item_types": [type(item).__name__ for item in obj]
                    }
                else:
                    return {
                        "type": type(obj).__name__,
                        "value": obj
                    }
            
            analysis = analyze_json(json_data)
            
            # 可选的JSON格式化
            if kwargs.get("pretty_format", True):
                formatted_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            else:
                formatted_content = json.dumps(json_data, ensure_ascii=False)
            
            self.processed_count += 1
            
            result = {
                "original_content": content,
                "processed_content": formatted_content,
                "parsed_data": json_data,
                "structure_analysis": analysis,
                "processing_time": datetime.now().isoformat()
            }
            
            print(f"📊 JSON消息处理完成: 解析成功，结构分析完成")
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析失败: {e}")
    
    def validate(self, content: str) -> bool:
        """验证JSON内容"""
        if not isinstance(content, str):
            return False
        try:
            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "JSON",
            "encoding": "UTF-8",
            "description": "处理JSON消息，提供解析、验证和结构分析功能"
        }


class XMLMessageProcessor(MessageProcessor):
    """XML消息处理器"""
    
    def __init__(self):
        super().__init__("XML消息处理器", "application/xml")
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理XML消息"""
        if not self.validate(content):
            raise ValueError("无效的XML内容")
        
        # 简单的XML处理（实际项目中应使用xml.etree.ElementTree）
        import re
        
        # 提取所有标签
        tags = re.findall(r'<(\w+)', content)
        closing_tags = re.findall(r'</(\w+)>', content)
        
        # 统计标签
        tag_counts = {}
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 提取文本内容
        text_content = re.sub(r'<[^>]+>', '', content).strip()
        
        # 基本的XML验证
        is_well_formed = len(tags) == len(closing_tags)
        
        self.processed_count += 1
        
        result = {
            "original_content": content,
            "processed_content": content,  # XML通常不需要额外处理
            "text_content": text_content,
            "tag_counts": tag_counts,
            "total_tags": len(tags),
            "is_well_formed": is_well_formed,
            "processing_time": datetime.now().isoformat()
        }
        
        print(f"📄 XML消息处理完成: {len(tags)} 个标签, 格式{'正确' if is_well_formed else '可能有误'}")
        return result
    
    def validate(self, content: str) -> bool:
        """验证XML内容"""
        if not isinstance(content, str):
            return False
        # 简单的XML验证：包含XML标签
        import re
        return bool(re.search(r'<\w+.*?>', content))
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "XML",
            "encoding": "UTF-8",
            "description": "处理XML消息，提供标签统计和基本验证功能"
        }


class EmailMessageProcessor(MessageProcessor):
    """邮件消息处理器"""
    
    def __init__(self):
        super().__init__("邮件消息处理器", "message/rfc822")
    
    def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """处理邮件消息"""
        if not self.validate(content):
            raise ValueError("无效的邮件内容")
        
        # 简单的邮件解析
        lines = content.split('\n')
        headers = {}
        body_start = 0
        
        # 解析邮件头
        for i, line in enumerate(lines):
            if line.strip() == '':
                body_start = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        # 提取邮件正文
        body = '\n'.join(lines[body_start:]).strip()
        
        # 分析邮件
        word_count = len(body.split()) if body else 0
        has_attachments = 'attachment' in content.lower()
        
        self.processed_count += 1
        
        result = {
            "original_content": content,
            "processed_content": content,
            "headers": headers,
            "body": body,
            "word_count": word_count,
            "has_attachments": has_attachments,
            "processing_time": datetime.now().isoformat()
        }
        
        print(f"📧 邮件消息处理完成: {len(headers)} 个头部字段, 正文 {word_count} 个单词")
        return result
    
    def validate(self, content: str) -> bool:
        """验证邮件内容"""
        if not isinstance(content, str):
            return False
        # 简单验证：包含邮件头格式
        return 'From:' in content or 'To:' in content or 'Subject:' in content
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "Email",
            "encoding": "UTF-8",
            "description": "处理邮件消息，提供头部解析和正文提取功能"
        }


# ==================== 简单工厂 ====================
class MessageProcessorFactory:
    """消息处理器工厂类"""
    
    # 支持的处理器类型
    SUPPORTED_PROCESSORS = {
        "text": ("文本", TextMessageProcessor),
        "html": ("HTML", HTMLMessageProcessor),
        "json": ("JSON", JSONMessageProcessor),
        "xml": ("XML", XMLMessageProcessor),
        "email": ("邮件", EmailMessageProcessor),
        # 别名支持
        "txt": ("文本", TextMessageProcessor),
        "htm": ("HTML", HTMLMessageProcessor),
        "mail": ("邮件", EmailMessageProcessor),
    }
    
    @staticmethod
    def create_processor(message_type: str) -> MessageProcessor:
        """
        创建消息处理器对象
        
        Args:
            message_type: 消息类型
        
        Returns:
            MessageProcessor: 创建的处理器对象
        
        Raises:
            ValueError: 不支持的消息类型
        """
        message_type = message_type.lower().strip()
        
        if message_type in MessageProcessorFactory.SUPPORTED_PROCESSORS:
            proc_name, proc_class = MessageProcessorFactory.SUPPORTED_PROCESSORS[message_type]
            print(f"🏭 消息处理器工厂正在创建 {proc_name} 处理器...")
            processor = proc_class()
            print(f"✅ {processor.name} 创建成功")
            return processor
        else:
            supported = list(set([name for name, _ in MessageProcessorFactory.SUPPORTED_PROCESSORS.values()]))
            raise ValueError(f"不支持的消息类型: {message_type}。支持的类型: {supported}")
    
    @staticmethod
    def auto_detect_type(content: str) -> str:
        """自动检测消息类型"""
        content_lower = content.lower().strip()
        
        # JSON检测
        if content_lower.startswith(('{', '[')):
            try:
                json.loads(content)
                return "json"
            except:
                pass
        
        # XML检测
        if content_lower.startswith('<?xml') or ('<' in content and '>' in content):
            import re
            if re.search(r'<\w+.*?>', content):
                return "xml"
        
        # HTML检测
        if any(tag in content_lower for tag in ['<html', '<body', '<div', '<p>', '<br']):
            return "html"
        
        # 邮件检测
        if any(header in content for header in ['From:', 'To:', 'Subject:']):
            return "email"
        
        # 默认为文本
        return "text"
    
    @staticmethod
    def process_message(message_type: str, content: str, **kwargs) -> Dict[str, Any]:
        """便捷方法：直接处理消息"""
        processor = MessageProcessorFactory.create_processor(message_type)
        return processor.process(content, **kwargs)
    
    @staticmethod
    def auto_process_message(content: str, **kwargs) -> Dict[str, Any]:
        """自动检测类型并处理消息"""
        detected_type = MessageProcessorFactory.auto_detect_type(content)
        print(f"🔍 自动检测到消息类型: {detected_type}")
        return MessageProcessorFactory.process_message(detected_type, content, **kwargs)


# ==================== 消息管理器 ====================
class MessageManager:
    """消息管理器 - 演示工厂的使用"""
    
    def __init__(self):
        self.processed_messages = []
        self.processors = {}  # 缓存处理器实例
    
    def process_message(self, message_type: str, content: str, **kwargs) -> Dict[str, Any]:
        """处理单个消息"""
        try:
            # 获取或创建处理器
            if message_type not in self.processors:
                self.processors[message_type] = MessageProcessorFactory.create_processor(message_type)
            
            processor = self.processors[message_type]
            result = processor.process(content, **kwargs)
            
            # 记录处理结果
            self.processed_messages.append({
                "type": message_type,
                "processor": processor.name,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            return result
            
        except Exception as e:
            print(f"❌ 消息处理失败: {e}")
            self.processed_messages.append({
                "type": message_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "success": False
            })
            raise
    
    def batch_process(self, messages: List[Dict[str, Any]]):
        """批量处理消息"""
        print(f"📦 开始批量处理 {len(messages)} 条消息...")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n--- 处理第 {i} 条消息 ---")
            try:
                msg_type = msg["type"]
                content = msg["content"]
                kwargs = msg.get("options", {})
                
                result = self.process_message(msg_type, content, **kwargs)
                print(f"✅ 消息处理成功")
                
            except Exception as e:
                print(f"❌ 消息处理失败: {e}")
    
    def get_statistics(self):
        """获取处理统计"""
        if not self.processed_messages:
            return {"total": 0}
        
        total = len(self.processed_messages)
        success = sum(1 for msg in self.processed_messages if msg["success"])
        failed = total - success
        
        type_counts = {}
        for msg in self.processed_messages:
            msg_type = msg["type"]
            type_counts[msg_type] = type_counts.get(msg_type, 0) + 1
        
        processor_stats = {}
        for processor in self.processors.values():
            stats = processor.get_statistics()
            processor_stats[stats["name"]] = stats
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": round(success / total * 100, 2) if total > 0 else 0,
            "type_distribution": type_counts,
            "processor_statistics": processor_stats
        }


# ==================== 演示函数 ====================
def demo_message_processing():
    """演示消息处理功能"""
    print("=== 消息处理器工厂演示 ===\n")
    
    manager = MessageManager()
    
    # 测试不同类型的消息
    messages = [
        {
            "type": "text",
            "content": "这是一条测试文本消息。包含多个单词和句子。",
            "options": {"remove_extra_spaces": True}
        },
        {
            "type": "json",
            "content": '{"name": "张三", "age": 25, "skills": ["Python", "Java"]}',
            "options": {"pretty_format": True}
        },
        {
            "type": "html",
            "content": "<html><body><h1>标题</h1><p>这是一个段落</p></body></html>",
            "options": {}
        },
        {
            "type": "xml",
            "content": "<?xml version='1.0'?><root><name>测试</name><value>123</value></root>",
            "options": {}
        }
    ]
    
    manager.batch_process(messages)
    
    # 显示统计信息
    stats = manager.get_statistics()
    print(f"\n📈 处理统计:")
    print(f"   总消息数: {stats['total']}")
    print(f"   成功率: {stats['success_rate']}%")
    print(f"   类型分布: {stats['type_distribution']}")


def demo_auto_detection():
    """演示自动类型检测"""
    print("\n" + "=" * 60)
    print("自动类型检测演示")
    print("=" * 60)
    
    test_contents = [
        '{"message": "这是JSON"}',
        '<html><body>这是HTML</body></html>',
        '<?xml version="1.0"?><root>这是XML</root>',
        'From: sender@example.com\nTo: receiver@example.com\nSubject: 测试邮件\n\n这是邮件正文',
        '这是普通的文本消息'
    ]
    
    for content in test_contents:
        print(f"\n内容预览: {content[:50]}...")
        try:
            result = MessageProcessorFactory.auto_process_message(content)
            print(f"✅ 自动处理成功")
        except Exception as e:
            print(f"❌ 处理失败: {e}")


def main():
    """主函数"""
    demo_message_processing()
    demo_auto_detection()
    
    print("\n" + "=" * 60)
    print("简单工厂模式在消息处理中的优势:")
    print("1. 统一处理接口：所有消息类型都有相同的处理接口")
    print("2. 自动类型检测：可以自动识别消息类型")
    print("3. 格式验证：每个处理器都有相应的验证逻辑")
    print("4. 处理器复用：相同类型的处理器可以复用")
    print("5. 易于扩展：添加新的消息类型很简单")
    print("=" * 60)


if __name__ == "__main__":
    main()
