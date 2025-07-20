"""
05_real_world_examples.py - 工厂方法模式实际应用示例

实际应用场景演示
这个文件展示了工厂方法模式在实际开发中的多种应用场景：
1. 日志记录器工厂 - 不同级别和输出方式的日志
2. 数据解析器工厂 - JSON、XML、CSV等格式解析
3. 支付处理器工厂 - 不同支付方式的处理
4. 缓存系统工厂 - 内存、Redis、文件等缓存方式
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
import json
from datetime import datetime


# ==================== 日志记录器工厂 ====================
class Logger(ABC):
    """日志记录器抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.level = "INFO"
    
    @abstractmethod
    def write_log(self, level: str, message: str) -> bool:
        """写入日志"""
        pass
    
    def format_message(self, level: str, message: str) -> str:
        """格式化日志消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{level}] [{self.name}] {message}"


class FileLogger(Logger):
    """文件日志记录器"""
    
    def __init__(self, name: str, file_path: str = "app.log"):
        super().__init__(name)
        self.file_path = file_path
    
    def write_log(self, level: str, message: str) -> bool:
        formatted_msg = self.format_message(level, message)
        print(f"📁 写入文件日志 ({self.file_path}): {formatted_msg}")
        return True


class ConsoleLogger(Logger):
    """控制台日志记录器"""
    
    def write_log(self, level: str, message: str) -> bool:
        formatted_msg = self.format_message(level, message)
        print(f"🖥️  控制台日志: {formatted_msg}")
        return True


class DatabaseLogger(Logger):
    """数据库日志记录器"""
    
    def __init__(self, name: str, table_name: str = "logs"):
        super().__init__(name)
        self.table_name = table_name
    
    def write_log(self, level: str, message: str) -> bool:
        formatted_msg = self.format_message(level, message)
        print(f"🗄️  数据库日志 ({self.table_name}): {formatted_msg}")
        return True


class LoggerFactory(ABC):
    """日志记录器工厂抽象基类"""
    
    @abstractmethod
    def create_logger(self, name: str) -> Logger:
        """创建日志记录器"""
        pass
    
    def get_logger(self, name: str) -> Logger:
        """获取日志记录器（业务逻辑）"""
        logger = self.create_logger(name)
        print(f"📝 创建 {logger.__class__.__name__}: {name}")
        return logger


class FileLoggerFactory(LoggerFactory):
    def create_logger(self, name: str) -> Logger:
        return FileLogger(name)


class ConsoleLoggerFactory(LoggerFactory):
    def create_logger(self, name: str) -> Logger:
        return ConsoleLogger(name)


class DatabaseLoggerFactory(LoggerFactory):
    def create_logger(self, name: str) -> Logger:
        return DatabaseLogger(name)


# ==================== 数据解析器工厂 ====================
class DataParser(ABC):
    """数据解析器抽象基类"""
    
    @abstractmethod
    def parse(self, data: str) -> Dict[str, Any]:
        """解析数据"""
        pass
    
    @abstractmethod
    def get_format_info(self) -> Dict[str, str]:
        """获取格式信息"""
        pass


class JSONParser(DataParser):
    """JSON解析器"""
    
    def parse(self, data: str) -> Dict[str, Any]:
        print(f"🔍 解析JSON数据...")
        try:
            result = json.loads(data)
            print(f"✓ JSON解析成功，包含 {len(result)} 个字段")
            return result
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {}
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "JSON",
            "mime_type": "application/json",
            "description": "JavaScript Object Notation"
        }


class XMLParser(DataParser):
    """XML解析器"""
    
    def parse(self, data: str) -> Dict[str, Any]:
        print(f"🔍 解析XML数据...")
        # 简化的XML解析模拟
        if "<root>" in data and "</root>" in data:
            print(f"✓ XML解析成功")
            return {"xml_content": "parsed_xml_data"}
        else:
            print(f"❌ XML格式错误")
            return {}
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "XML",
            "mime_type": "application/xml",
            "description": "eXtensible Markup Language"
        }


class CSVParser(DataParser):
    """CSV解析器"""
    
    def parse(self, data: str) -> Dict[str, Any]:
        print(f"🔍 解析CSV数据...")
        lines = data.strip().split('\n')
        if len(lines) >= 2:
            headers = lines[0].split(',')
            rows = [line.split(',') for line in lines[1:]]
            print(f"✓ CSV解析成功，{len(headers)} 列，{len(rows)} 行")
            return {"headers": headers, "rows": rows}
        else:
            print(f"❌ CSV格式错误")
            return {}
    
    def get_format_info(self) -> Dict[str, str]:
        return {
            "format": "CSV",
            "mime_type": "text/csv",
            "description": "Comma-Separated Values"
        }


class ParserFactory(ABC):
    """解析器工厂抽象基类"""
    
    @abstractmethod
    def create_parser(self) -> DataParser:
        """创建解析器"""
        pass
    
    def parse_data(self, data: str) -> Dict[str, Any]:
        """解析数据（业务逻辑）"""
        parser = self.create_parser()
        format_info = parser.get_format_info()
        print(f"📊 使用 {format_info['format']} 解析器")
        return parser.parse(data)


class JSONParserFactory(ParserFactory):
    def create_parser(self) -> DataParser:
        return JSONParser()


class XMLParserFactory(ParserFactory):
    def create_parser(self) -> DataParser:
        return XMLParser()


class CSVParserFactory(ParserFactory):
    def create_parser(self) -> DataParser:
        return CSVParser()


# ==================== 支付处理器工厂 ====================
class PaymentProcessor(ABC):
    """支付处理器抽象基类"""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str = "CNY") -> Dict[str, Any]:
        """处理支付"""
        pass
    
    @abstractmethod
    def get_payment_info(self) -> Dict[str, str]:
        """获取支付方式信息"""
        pass


class AlipayProcessor(PaymentProcessor):
    """支付宝处理器"""
    
    def process_payment(self, amount: float, currency: str = "CNY") -> Dict[str, Any]:
        print(f"💰 支付宝支付处理...")
        print(f"   金额: {amount} {currency}")
        print(f"   手续费: {amount * 0.006:.2f} {currency}")
        
        # 模拟支付处理
        time.sleep(0.5)
        
        return {
            "status": "success",
            "transaction_id": f"alipay_{int(time.time())}",
            "amount": amount,
            "fee": amount * 0.006,
            "currency": currency
        }
    
    def get_payment_info(self) -> Dict[str, str]:
        return {
            "name": "支付宝",
            "provider": "蚂蚁金服",
            "fee_rate": "0.6%"
        }


class WeChatPayProcessor(PaymentProcessor):
    """微信支付处理器"""
    
    def process_payment(self, amount: float, currency: str = "CNY") -> Dict[str, Any]:
        print(f"💰 微信支付处理...")
        print(f"   金额: {amount} {currency}")
        print(f"   手续费: {amount * 0.006:.2f} {currency}")
        
        # 模拟支付处理
        time.sleep(0.4)
        
        return {
            "status": "success",
            "transaction_id": f"wechat_{int(time.time())}",
            "amount": amount,
            "fee": amount * 0.006,
            "currency": currency
        }
    
    def get_payment_info(self) -> Dict[str, str]:
        return {
            "name": "微信支付",
            "provider": "腾讯",
            "fee_rate": "0.6%"
        }


class BankCardProcessor(PaymentProcessor):
    """银行卡处理器"""
    
    def process_payment(self, amount: float, currency: str = "CNY") -> Dict[str, Any]:
        print(f"💰 银行卡支付处理...")
        print(f"   金额: {amount} {currency}")
        print(f"   手续费: {amount * 0.01:.2f} {currency}")
        
        # 模拟支付处理
        time.sleep(0.8)
        
        return {
            "status": "success",
            "transaction_id": f"bank_{int(time.time())}",
            "amount": amount,
            "fee": amount * 0.01,
            "currency": currency
        }
    
    def get_payment_info(self) -> Dict[str, str]:
        return {
            "name": "银行卡",
            "provider": "银联",
            "fee_rate": "1.0%"
        }


class PaymentFactory(ABC):
    """支付工厂抽象基类"""
    
    @abstractmethod
    def create_processor(self) -> PaymentProcessor:
        """创建支付处理器"""
        pass
    
    def process_payment(self, amount: float, currency: str = "CNY") -> Dict[str, Any]:
        """处理支付（业务逻辑）"""
        processor = self.create_processor()
        payment_info = processor.get_payment_info()
        print(f"💳 使用 {payment_info['name']} 处理支付")
        return processor.process_payment(amount, currency)


class AlipayFactory(PaymentFactory):
    def create_processor(self) -> PaymentProcessor:
        return AlipayProcessor()


class WeChatPayFactory(PaymentFactory):
    def create_processor(self) -> PaymentProcessor:
        return WeChatPayProcessor()


class BankCardFactory(PaymentFactory):
    def create_processor(self) -> PaymentProcessor:
        return BankCardProcessor()


# ==================== 演示函数 ====================
def demo_logger_factory():
    """演示日志记录器工厂"""
    print("=== 日志记录器工厂演示 ===\n")
    
    factories = {
        "文件": FileLoggerFactory(),
        "控制台": ConsoleLoggerFactory(),
        "数据库": DatabaseLoggerFactory()
    }
    
    for name, factory in factories.items():
        print(f"\n{'='*40}")
        print(f"{name}日志记录器")
        print('='*40)
        
        logger = factory.get_logger("UserService")
        logger.write_log("INFO", "用户登录成功")
        logger.write_log("ERROR", "数据库连接失败")


def demo_parser_factory():
    """演示数据解析器工厂"""
    print("\n" + "="*60)
    print("数据解析器工厂演示")
    print("="*60)
    
    # 测试数据
    test_data = {
        "JSON": '{"name": "张三", "age": 25, "city": "北京"}',
        "XML": '<root><name>张三</name><age>25</age></root>',
        "CSV": 'name,age,city\n张三,25,北京\n李四,30,上海'
    }
    
    factories = {
        "JSON": JSONParserFactory(),
        "XML": XMLParserFactory(),
        "CSV": CSVParserFactory()
    }
    
    for format_name, factory in factories.items():
        print(f"\n{'='*40}")
        print(f"{format_name} 解析器")
        print('='*40)
        
        data = test_data[format_name]
        result = factory.parse_data(data)
        print(f"解析结果: {result}")


def demo_payment_factory():
    """演示支付处理器工厂"""
    print("\n" + "="*60)
    print("支付处理器工厂演示")
    print("="*60)
    
    factories = {
        "支付宝": AlipayFactory(),
        "微信支付": WeChatPayFactory(),
        "银行卡": BankCardFactory()
    }
    
    amount = 299.00
    
    for name, factory in factories.items():
        print(f"\n{'='*40}")
        print(f"{name}支付")
        print('='*40)
        
        result = factory.process_payment(amount)
        print(f"支付结果: {result}")


def main():
    """主函数"""
    demo_logger_factory()
    demo_parser_factory()
    demo_payment_factory()
    
    print("\n" + "="*60)
    print("工厂方法模式在实际项目中的应用价值:")
    print("1. 插件化架构：支持动态加载不同的实现")
    print("2. 配置驱动：通过配置选择不同的实现方式")
    print("3. 测试友好：可以轻松创建测试用的实现")
    print("4. 代码解耦：业务逻辑与具体实现分离")
    print("5. 易于维护：新增实现不影响现有代码")
    print("="*60)


if __name__ == "__main__":
    main()
