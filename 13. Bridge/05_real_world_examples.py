"""
桥接模式实际应用案例集合

这个文件包含了多个实际项目中桥接模式的应用案例，展示了
不同场景下桥接模式的变体和最佳实践。

作者: Bridge Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
from datetime import datetime
from enum import Enum


# ==================== 案例1: 日志系统 ====================

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogHandler(ABC):
    """日志处理器接口 - 实现层"""
    
    @abstractmethod
    def write_log(self, level: LogLevel, message: str, timestamp: datetime) -> None:
        """写入日志"""
        pass
    
    @abstractmethod
    def get_handler_info(self) -> str:
        """获取处理器信息"""
        pass


class FileLogHandler(LogHandler):
    """文件日志处理器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.log_count = 0
    
    def write_log(self, level: LogLevel, message: str, timestamp: datetime) -> None:
        """写入文件日志"""
        log_entry = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {level.value}: {message}"
        print(f"📁 写入文件日志 ({self.file_path}): {log_entry}")
        self.log_count += 1
    
    def get_handler_info(self) -> str:
        return f"文件日志处理器 (文件: {self.file_path}, 已写入: {self.log_count} 条)"


class DatabaseLogHandler(LogHandler):
    """数据库日志处理器"""
    
    def __init__(self, table_name: str = "logs"):
        self.table_name = table_name
        self.log_count = 0
    
    def write_log(self, level: LogLevel, message: str, timestamp: datetime) -> None:
        """写入数据库日志"""
        print(f"🗄️  写入数据库日志 ({self.table_name}): [{level.value}] {message}")
        self.log_count += 1
    
    def get_handler_info(self) -> str:
        return f"数据库日志处理器 (表: {self.table_name}, 已写入: {self.log_count} 条)"


class ConsoleLogHandler(LogHandler):
    """控制台日志处理器"""
    
    def __init__(self, colored: bool = True):
        self.colored = colored
        self.log_count = 0
    
    def write_log(self, level: LogLevel, message: str, timestamp: datetime) -> None:
        """写入控制台日志"""
        color_map = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌",
            LogLevel.CRITICAL: "🚨"
        }
        
        icon = color_map.get(level, "📝")
        log_entry = f"{icon} [{timestamp.strftime('%H:%M:%S')}] {message}"
        print(f"🖥️  控制台日志: {log_entry}")
        self.log_count += 1
    
    def get_handler_info(self) -> str:
        return f"控制台日志处理器 (彩色: {self.colored}, 已输出: {self.log_count} 条)"


class Logger:
    """日志器抽象类 - 抽象层"""
    
    def __init__(self, handler: LogHandler, name: str = "Logger"):
        self.handler = handler
        self.name = name
        self.min_level = LogLevel.INFO
    
    def log(self, level: LogLevel, message: str) -> None:
        """记录日志"""
        if self._should_log(level):
            timestamp = datetime.now()
            formatted_message = f"[{self.name}] {message}"
            self.handler.write_log(level, formatted_message, timestamp)
    
    def debug(self, message: str) -> None:
        """调试日志"""
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str) -> None:
        """信息日志"""
        self.log(LogLevel.INFO, message)
    
    def warning(self, message: str) -> None:
        """警告日志"""
        self.log(LogLevel.WARNING, message)
    
    def error(self, message: str) -> None:
        """错误日志"""
        self.log(LogLevel.ERROR, message)
    
    def critical(self, message: str) -> None:
        """严重错误日志"""
        self.log(LogLevel.CRITICAL, message)
    
    def set_handler(self, handler: LogHandler) -> None:
        """设置日志处理器"""
        self.handler = handler
        print(f"🔄 日志处理器已切换为: {handler.get_handler_info()}")
    
    def set_level(self, level: LogLevel) -> None:
        """设置最小日志级别"""
        self.min_level = level
        print(f"📊 最小日志级别设置为: {level.value}")
    
    def _should_log(self, level: LogLevel) -> bool:
        """判断是否应该记录日志"""
        level_order = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]
        return level_order.index(level) >= level_order.index(self.min_level)


# ==================== 案例2: 通知系统 ====================

class NotificationChannel(ABC):
    """通知渠道接口 - 实现层"""
    
    @abstractmethod
    def send_notification(self, title: str, content: str, recipient: str) -> bool:
        """发送通知"""
        pass
    
    @abstractmethod
    def get_channel_info(self) -> str:
        """获取渠道信息"""
        pass


class EmailNotificationChannel(NotificationChannel):
    """邮件通知渠道"""
    
    def __init__(self, smtp_server: str):
        self.smtp_server = smtp_server
        self.sent_count = 0
    
    def send_notification(self, title: str, content: str, recipient: str) -> bool:
        """发送邮件通知"""
        print(f"📧 发送邮件通知到 {recipient}")
        print(f"   标题: {title}")
        print(f"   内容: {content}")
        print(f"   SMTP: {self.smtp_server}")
        self.sent_count += 1
        return True
    
    def get_channel_info(self) -> str:
        return f"邮件通知渠道 (SMTP: {self.smtp_server}, 已发送: {self.sent_count})"


class SlackNotificationChannel(NotificationChannel):
    """Slack通知渠道"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.sent_count = 0
    
    def send_notification(self, title: str, content: str, recipient: str) -> bool:
        """发送Slack通知"""
        print(f"💬 发送Slack通知到 {recipient}")
        print(f"   标题: {title}")
        print(f"   内容: {content}")
        print(f"   Webhook: {self.webhook_url}")
        self.sent_count += 1
        return True
    
    def get_channel_info(self) -> str:
        return f"Slack通知渠道 (Webhook: {self.webhook_url}, 已发送: {self.sent_count})"


class NotificationService:
    """通知服务 - 抽象层"""
    
    def __init__(self, channel: NotificationChannel):
        self.channel = channel
        self.notification_history: List[Dict] = []
    
    def send(self, title: str, content: str, recipient: str) -> bool:
        """发送通知"""
        success = self.channel.send_notification(title, content, recipient)
        
        # 记录历史
        self.notification_history.append({
            "title": title,
            "content": content,
            "recipient": recipient,
            "timestamp": datetime.now(),
            "success": success,
            "channel": self.channel.get_channel_info()
        })
        
        return success
    
    def set_channel(self, channel: NotificationChannel) -> None:
        """切换通知渠道"""
        self.channel = channel
        print(f"🔄 通知渠道已切换为: {channel.get_channel_info()}")
    
    def get_history(self) -> List[Dict]:
        """获取通知历史"""
        return self.notification_history


# ==================== 案例3: 支付系统 ====================

class PaymentGateway(ABC):
    """支付网关接口 - 实现层"""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict[str, Any]:
        """处理支付"""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款"""
        pass
    
    @abstractmethod
    def get_gateway_info(self) -> str:
        """获取网关信息"""
        pass


class StripeGateway(PaymentGateway):
    """Stripe支付网关"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.transaction_count = 0
    
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict[str, Any]:
        """处理Stripe支付"""
        print(f"💳 Stripe处理支付: {amount} {currency}")
        print(f"   卡号: ****{card_info.get('number', '')[-4:]}")
        
        # 模拟支付处理
        time.sleep(0.1)
        self.transaction_count += 1
        
        return {
            "success": True,
            "transaction_id": f"stripe_{self.transaction_count}",
            "amount": amount,
            "currency": currency,
            "gateway": "Stripe"
        }
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Stripe退款"""
        print(f"💰 Stripe处理退款: {transaction_id}, 金额: {amount}")
        return {
            "success": True,
            "refund_id": f"refund_{transaction_id}",
            "amount": amount
        }
    
    def get_gateway_info(self) -> str:
        return f"Stripe支付网关 (API密钥: {self.api_key[:8]}..., 交易数: {self.transaction_count})"


class PayPalGateway(PaymentGateway):
    """PayPal支付网关"""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.transaction_count = 0
    
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict[str, Any]:
        """处理PayPal支付"""
        print(f"🅿️  PayPal处理支付: {amount} {currency}")
        print(f"   PayPal账户: {card_info.get('email', 'N/A')}")
        
        time.sleep(0.15)
        self.transaction_count += 1
        
        return {
            "success": True,
            "transaction_id": f"paypal_{self.transaction_count}",
            "amount": amount,
            "currency": currency,
            "gateway": "PayPal"
        }
    
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """PayPal退款"""
        print(f"💰 PayPal处理退款: {transaction_id}, 金额: {amount}")
        return {
            "success": True,
            "refund_id": f"refund_{transaction_id}",
            "amount": amount
        }
    
    def get_gateway_info(self) -> str:
        return f"PayPal支付网关 (客户端ID: {self.client_id[:8]}..., 交易数: {self.transaction_count})"


class PaymentProcessor:
    """支付处理器 - 抽象层"""
    
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
        self.transaction_history: List[Dict] = []
    
    def charge(self, amount: float, currency: str = "USD", **payment_info) -> Dict[str, Any]:
        """收费"""
        print(f"\n💳 处理支付请求: {amount} {currency}")
        
        result = self.gateway.process_payment(amount, currency, payment_info)
        
        # 记录交易历史
        transaction = {
            "type": "charge",
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.now(),
            "result": result,
            "gateway": self.gateway.get_gateway_info()
        }
        self.transaction_history.append(transaction)
        
        if result["success"]:
            print(f"   ✅ 支付成功，交易ID: {result['transaction_id']}")
        else:
            print(f"   ❌ 支付失败")
        
        return result
    
    def refund(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款"""
        print(f"\n💰 处理退款请求: {transaction_id}")
        
        result = self.gateway.refund_payment(transaction_id, amount)
        
        # 记录退款历史
        refund_record = {
            "type": "refund",
            "transaction_id": transaction_id,
            "amount": amount,
            "timestamp": datetime.now(),
            "result": result,
            "gateway": self.gateway.get_gateway_info()
        }
        self.transaction_history.append(refund_record)
        
        return result
    
    def set_gateway(self, gateway: PaymentGateway) -> None:
        """切换支付网关"""
        self.gateway = gateway
        print(f"🔄 支付网关已切换为: {gateway.get_gateway_info()}")


def demo_logging_system():
    """日志系统演示"""
    print("=" * 60)
    print("📝 日志系统 - 桥接模式演示")
    print("=" * 60)
    
    # 创建不同的日志处理器
    file_handler = FileLogHandler("app.log")
    db_handler = DatabaseLogHandler("application_logs")
    console_handler = ConsoleLogHandler(colored=True)
    
    # 创建日志器
    logger = Logger(console_handler, "WebApp")
    
    print("\n🔹 使用控制台处理器:")
    logger.info("应用程序启动")
    logger.warning("内存使用率较高")
    logger.error("数据库连接失败")
    
    print(f"\n🔄 切换到文件处理器:")
    logger.set_handler(file_handler)
    logger.info("切换到文件日志")
    logger.debug("调试信息")  # 不会输出，因为级别不够
    
    print(f"\n📊 设置日志级别为DEBUG:")
    logger.set_level(LogLevel.DEBUG)
    logger.debug("现在可以看到调试信息了")


def demo_notification_system():
    """通知系统演示"""
    print("\n" + "=" * 60)
    print("📢 通知系统演示")
    print("=" * 60)
    
    # 创建通知渠道
    email_channel = EmailNotificationChannel("smtp.gmail.com")
    slack_channel = SlackNotificationChannel("https://hooks.slack.com/webhook")
    
    # 创建通知服务
    notification_service = NotificationService(email_channel)
    
    print("\n📧 使用邮件渠道:")
    notification_service.send("系统维护通知", "系统将在今晚22:00进行维护", "admin@example.com")
    
    print(f"\n💬 切换到Slack渠道:")
    notification_service.set_channel(slack_channel)
    notification_service.send("部署完成", "新版本已成功部署到生产环境", "#dev-team")


def demo_payment_system():
    """支付系统演示"""
    print("\n" + "=" * 60)
    print("💳 支付系统演示")
    print("=" * 60)
    
    # 创建支付网关
    stripe_gateway = StripeGateway("sk_test_123456789")
    paypal_gateway = PayPalGateway("client_987654321")
    
    # 创建支付处理器
    payment_processor = PaymentProcessor(stripe_gateway)
    
    print("\n💳 使用Stripe网关:")
    result1 = payment_processor.charge(99.99, "USD", number="4242424242424242", cvv="123")
    
    print(f"\n🔄 切换到PayPal网关:")
    payment_processor.set_gateway(paypal_gateway)
    result2 = payment_processor.charge(149.99, "USD", email="user@example.com")
    
    # 处理退款
    if result2["success"]:
        payment_processor.refund(result2["transaction_id"], 50.0)


if __name__ == "__main__":
    demo_logging_system()
    demo_notification_system()
    demo_payment_system()
