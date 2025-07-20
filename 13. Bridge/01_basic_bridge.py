"""
桥接模式基础实现 - 消息发送系统

这个示例展示了桥接模式的基本概念，通过一个消息发送系统来演示
如何将抽象部分（消息类型）与实现部分（发送方式）分离。

作者: Bridge Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List
import time
from datetime import datetime


# ==================== 实现层接口 ====================

class MessageSender(ABC):
    """消息发送器接口 - 实现层"""
    
    @abstractmethod
    def send_message(self, recipient: str, content: str) -> bool:
        """发送消息的具体实现"""
        pass
    
    @abstractmethod
    def get_sender_info(self) -> str:
        """获取发送器信息"""
        pass


# ==================== 具体实现 ====================

class EmailSender(MessageSender):
    """邮件发送器 - 具体实现A"""
    
    def __init__(self, smtp_server: str = "smtp.example.com"):
        self.smtp_server = smtp_server
        self.sent_count = 0
    
    def send_message(self, recipient: str, content: str) -> bool:
        """发送邮件"""
        print(f"📧 通过邮件发送到 {recipient}")
        print(f"   SMTP服务器: {self.smtp_server}")
        print(f"   内容: {content}")
        
        # 模拟发送延迟
        time.sleep(0.1)
        self.sent_count += 1
        
        print(f"   ✅ 邮件发送成功")
        return True
    
    def get_sender_info(self) -> str:
        return f"邮件发送器 (服务器: {self.smtp_server}, 已发送: {self.sent_count})"


class SMSSender(MessageSender):
    """短信发送器 - 具体实现B"""
    
    def __init__(self, provider: str = "移动"):
        self.provider = provider
        self.sent_count = 0
    
    def send_message(self, recipient: str, content: str) -> bool:
        """发送短信"""
        print(f"📱 通过短信发送到 {recipient}")
        print(f"   运营商: {self.provider}")
        print(f"   内容: {content}")
        
        # 模拟发送延迟
        time.sleep(0.05)
        self.sent_count += 1
        
        print(f"   ✅ 短信发送成功")
        return True
    
    def get_sender_info(self) -> str:
        return f"短信发送器 (运营商: {self.provider}, 已发送: {self.sent_count})"


class PushNotificationSender(MessageSender):
    """推送通知发送器 - 具体实现C"""
    
    def __init__(self, platform: str = "Android"):
        self.platform = platform
        self.sent_count = 0
    
    def send_message(self, recipient: str, content: str) -> bool:
        """发送推送通知"""
        print(f"🔔 通过推送通知发送到 {recipient}")
        print(f"   平台: {self.platform}")
        print(f"   内容: {content}")
        
        # 模拟发送延迟
        time.sleep(0.02)
        self.sent_count += 1
        
        print(f"   ✅ 推送通知发送成功")
        return True
    
    def get_sender_info(self) -> str:
        return f"推送通知发送器 (平台: {self.platform}, 已发送: {self.sent_count})"


# ==================== 抽象层 ====================

class Message:
    """消息抽象类 - 抽象层"""
    
    def __init__(self, sender: MessageSender):
        self.sender = sender
        self.timestamp = datetime.now()
    
    def send(self, recipient: str, content: str) -> bool:
        """发送消息 - 委托给实现层"""
        print(f"\n📨 准备发送消息 ({self.timestamp.strftime('%H:%M:%S')})")
        return self.sender.send_message(recipient, content)
    
    def get_info(self) -> str:
        """获取消息信息"""
        return f"消息 - {self.sender.get_sender_info()}"
    
    def set_sender(self, sender: MessageSender) -> None:
        """动态切换发送器"""
        self.sender = sender
        print(f"🔄 已切换发送器: {sender.get_sender_info()}")


# ==================== 扩展抽象层 ====================

class UrgentMessage(Message):
    """紧急消息 - 扩展抽象层"""
    
    def __init__(self, sender: MessageSender, priority: int = 1):
        super().__init__(sender)
        self.priority = priority
    
    def send(self, recipient: str, content: str) -> bool:
        """发送紧急消息 - 增加优先级标识"""
        urgent_content = f"🚨 [紧急-P{self.priority}] {content}"
        print(f"\n🚨 准备发送紧急消息 (优先级: {self.priority})")
        return self.sender.send_message(recipient, urgent_content)
    
    def send_multiple_channels(self, recipient: str, content: str, 
                             backup_senders: List[MessageSender]) -> bool:
        """通过多个渠道发送紧急消息"""
        print(f"\n🚨 通过多渠道发送紧急消息")
        
        # 主渠道发送
        success = self.send(recipient, content)
        
        # 备用渠道发送
        for backup_sender in backup_senders:
            print(f"\n📡 备用渠道发送:")
            backup_sender.send_message(recipient, f"[备用渠道] {content}")
        
        return success


class ScheduledMessage(Message):
    """定时消息 - 扩展抽象层"""
    
    def __init__(self, sender: MessageSender, delay_seconds: int = 0):
        super().__init__(sender)
        self.delay_seconds = delay_seconds
        self.scheduled = False
    
    def send(self, recipient: str, content: str) -> bool:
        """发送定时消息"""
        if self.delay_seconds > 0:
            print(f"\n⏰ 定时消息将在 {self.delay_seconds} 秒后发送")
            time.sleep(self.delay_seconds)
        
        scheduled_content = f"⏰ [定时消息] {content}"
        print(f"\n⏰ 发送定时消息")
        return self.sender.send_message(recipient, scheduled_content)
    
    def schedule_send(self, recipient: str, content: str) -> None:
        """安排定时发送（模拟）"""
        self.scheduled = True
        print(f"📅 消息已安排在 {self.delay_seconds} 秒后发送给 {recipient}")


class BroadcastMessage(Message):
    """广播消息 - 扩展抽象层"""
    
    def __init__(self, sender: MessageSender):
        super().__init__(sender)
        self.recipients: List[str] = []
    
    def add_recipient(self, recipient: str) -> None:
        """添加接收者"""
        if recipient not in self.recipients:
            self.recipients.append(recipient)
            print(f"➕ 已添加接收者: {recipient}")
    
    def send_broadcast(self, content: str) -> bool:
        """发送广播消息"""
        if not self.recipients:
            print("⚠️  没有接收者，无法发送广播消息")
            return False
        
        print(f"\n📢 发送广播消息给 {len(self.recipients)} 个接收者")
        broadcast_content = f"📢 [广播] {content}"
        
        success_count = 0
        for recipient in self.recipients:
            if self.sender.send_message(recipient, broadcast_content):
                success_count += 1
        
        print(f"📊 广播结果: {success_count}/{len(self.recipients)} 发送成功")
        return success_count == len(self.recipients)


def demo_basic_bridge():
    """基础桥接模式演示"""
    print("=" * 60)
    print("📨 消息发送系统 - 桥接模式演示")
    print("=" * 60)
    
    # 创建不同的发送器（实现层）
    email_sender = EmailSender("smtp.gmail.com")
    sms_sender = SMSSender("联通")
    push_sender = PushNotificationSender("iOS")
    
    # 创建基本消息（抽象层）
    print("\n🔹 基本消息发送:")
    message = Message(email_sender)
    message.send("user@example.com", "欢迎使用我们的服务！")
    
    # 动态切换发送器
    print(f"\n🔄 动态切换发送器:")
    message.set_sender(sms_sender)
    message.send("13800138000", "您的验证码是: 123456")
    
    # 紧急消息
    print(f"\n🚨 紧急消息发送:")
    urgent_msg = UrgentMessage(push_sender, priority=1)
    urgent_msg.send("user123", "系统将在5分钟后维护")
    
    # 多渠道紧急消息
    print(f"\n📡 多渠道紧急消息:")
    backup_senders = [email_sender, sms_sender]
    urgent_msg.send_multiple_channels("admin", "服务器异常", backup_senders)


def demo_extended_features():
    """扩展功能演示"""
    print("\n" + "=" * 60)
    print("⏰ 扩展功能演示")
    print("=" * 60)
    
    # 定时消息
    print("\n⏰ 定时消息:")
    email_sender = EmailSender()
    scheduled_msg = ScheduledMessage(email_sender, delay_seconds=2)
    scheduled_msg.send("user@example.com", "这是一条定时消息")
    
    # 广播消息
    print(f"\n📢 广播消息:")
    sms_sender = SMSSender()
    broadcast_msg = BroadcastMessage(sms_sender)
    
    # 添加接收者
    broadcast_msg.add_recipient("13800138001")
    broadcast_msg.add_recipient("13800138002")
    broadcast_msg.add_recipient("13800138003")
    
    # 发送广播
    broadcast_msg.send_broadcast("系统升级通知：今晚22:00-24:00进行系统维护")


def demo_runtime_switching():
    """运行时切换演示"""
    print("\n" + "=" * 60)
    print("🔄 运行时切换演示")
    print("=" * 60)
    
    # 创建发送器
    senders = [
        EmailSender("smtp.qq.com"),
        SMSSender("电信"),
        PushNotificationSender("Android")
    ]
    
    # 创建消息并动态切换发送器
    message = Message(senders[0])
    
    for i, sender in enumerate(senders):
        print(f"\n📍 使用发送器 {i+1}:")
        message.set_sender(sender)
        message.send(f"user{i+1}", f"这是通过第{i+1}种方式发送的消息")
        print(f"   发送器信息: {message.get_info()}")


if __name__ == "__main__":
    demo_basic_bridge()
    demo_extended_features()
    demo_runtime_switching()
