"""
02_notification_factory.py - 通知系统工厂方法模式

通知系统示例
这个示例展示了工厂方法模式在实际业务场景中的应用。
我们有不同类型的通知方式（邮件、短信、推送），每种通知方式都有对应的工厂。
通过配置可以动态选择通知方式，体现了工厂方法模式的灵活性。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import time
import json


# ==================== 抽象产品 ====================
class Notification(ABC):
    """通知抽象基类"""
    
    def __init__(self):
        self.sent_at: Optional[str] = None
        self.status: str = "未发送"
    
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        """发送通知"""
        pass
    
    @abstractmethod
    def get_delivery_info(self) -> Dict[str, str]:
        """获取投递信息"""
        pass
    
    def mark_as_sent(self):
        """标记为已发送"""
        self.sent_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.status = "已发送"


# ==================== 具体产品 ====================
class EmailNotification(Notification):
    """邮件通知"""
    
    def send(self, message: str, recipient: str) -> bool:
        """发送邮件"""
        print(f"📧 正在发送邮件...")
        print(f"   收件人: {recipient}")
        print(f"   主题: 系统通知")
        print(f"   内容: {message}")
        
        # 模拟邮件发送过程
        time.sleep(0.5)
        
        # 模拟发送成功
        self.mark_as_sent()
        print(f"   ✓ 邮件发送成功")
        return True
    
    def get_delivery_info(self) -> Dict[str, str]:
        return {
            "type": "邮件",
            "protocol": "SMTP",
            "delivery_time": "即时",
            "reliability": "高"
        }


class SMSNotification(Notification):
    """短信通知"""
    
    def send(self, message: str, recipient: str) -> bool:
        """发送短信"""
        print(f"📱 正在发送短信...")
        print(f"   手机号: {recipient}")
        print(f"   内容: {message}")
        
        # 模拟短信发送过程
        time.sleep(0.3)
        
        # 模拟发送成功
        self.mark_as_sent()
        print(f"   ✓ 短信发送成功")
        return True
    
    def get_delivery_info(self) -> Dict[str, str]:
        return {
            "type": "短信",
            "protocol": "SMS",
            "delivery_time": "秒级",
            "reliability": "高"
        }


class PushNotification(Notification):
    """推送通知"""
    
    def send(self, message: str, recipient: str) -> bool:
        """发送推送通知"""
        print(f"🔔 正在发送推送通知...")
        print(f"   设备ID: {recipient}")
        print(f"   标题: 系统消息")
        print(f"   内容: {message}")
        
        # 模拟推送发送过程
        time.sleep(0.2)
        
        # 模拟发送成功
        self.mark_as_sent()
        print(f"   ✓ 推送通知发送成功")
        return True
    
    def get_delivery_info(self) -> Dict[str, str]:
        return {
            "type": "推送",
            "protocol": "FCM/APNs",
            "delivery_time": "实时",
            "reliability": "中"
        }


class WeChatNotification(Notification):
    """微信通知"""
    
    def send(self, message: str, recipient: str) -> bool:
        """发送微信通知"""
        print(f"💬 正在发送微信通知...")
        print(f"   微信号: {recipient}")
        print(f"   消息类型: 模板消息")
        print(f"   内容: {message}")
        
        # 模拟微信发送过程
        time.sleep(0.4)
        
        # 模拟发送成功
        self.mark_as_sent()
        print(f"   ✓ 微信通知发送成功")
        return True
    
    def get_delivery_info(self) -> Dict[str, str]:
        return {
            "type": "微信",
            "protocol": "WeChat API",
            "delivery_time": "即时",
            "reliability": "高"
        }


# ==================== 抽象创建者 ====================
class NotificationFactory(ABC):
    """通知工厂抽象基类"""
    
    @abstractmethod
    def create_notification(self) -> Notification:
        """工厂方法：创建通知对象"""
        pass
    
    def send_notification(self, message: str, recipient: str) -> bool:
        """发送通知的业务逻辑"""
        print(f"🚀 启动通知发送流程...")
        
        # 1. 创建通知对象（使用工厂方法）
        notification = self.create_notification()
        
        # 2. 获取投递信息
        delivery_info = notification.get_delivery_info()
        print(f"📋 通知类型: {delivery_info['type']}")
        print(f"📋 传输协议: {delivery_info['protocol']}")
        
        # 3. 发送通知
        success = notification.send(message, recipient)
        
        # 4. 记录发送结果
        if success:
            print(f"✅ 通知发送成功 - {notification.sent_at}")
        else:
            print(f"❌ 通知发送失败")
        
        return success


# ==================== 具体创建者 ====================
class EmailNotificationFactory(NotificationFactory):
    """邮件通知工厂"""
    
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSNotificationFactory(NotificationFactory):
    """短信通知工厂"""
    
    def create_notification(self) -> Notification:
        return SMSNotification()


class PushNotificationFactory(NotificationFactory):
    """推送通知工厂"""
    
    def create_notification(self) -> Notification:
        return PushNotification()


class WeChatNotificationFactory(NotificationFactory):
    """微信通知工厂"""
    
    def create_notification(self) -> Notification:
        return WeChatNotification()


# ==================== 通知管理器 ====================
class NotificationManager:
    """通知管理器 - 演示配置驱动的工厂选择"""
    
    def __init__(self):
        self.factories = {
            "email": EmailNotificationFactory(),
            "sms": SMSNotificationFactory(),
            "push": PushNotificationFactory(),
            "wechat": WeChatNotificationFactory()
        }
        self.config = {
            "default_channel": "email",
            "fallback_channels": ["sms", "push"],
            "retry_count": 3
        }
    
    def send_notification(self, message: str, recipient: str, 
                         channel: Optional[str] = None) -> bool:
        """发送通知（支持回退机制）"""
        # 确定发送渠道
        target_channel = channel or self.config["default_channel"]
        
        # 尝试发送
        if target_channel in self.factories:
            factory = self.factories[target_channel]
            success = factory.send_notification(message, recipient)
            
            if success:
                return True
        
        # 如果失败，尝试回退渠道
        print(f"⚠️  主渠道 {target_channel} 发送失败，尝试回退渠道...")
        for fallback_channel in self.config["fallback_channels"]:
            if fallback_channel != target_channel and fallback_channel in self.factories:
                print(f"🔄 尝试回退渠道: {fallback_channel}")
                factory = self.factories[fallback_channel]
                success = factory.send_notification(message, recipient)
                if success:
                    return True
        
        print(f"❌ 所有渠道发送失败")
        return False
    
    def batch_send(self, message: str, recipients: List[Dict[str, str]]):
        """批量发送通知"""
        print(f"\n📢 开始批量发送通知...")
        print(f"📝 消息内容: {message}")
        print(f"👥 接收人数: {len(recipients)}")
        
        results = []
        for recipient_info in recipients:
            recipient = recipient_info["contact"]
            channel = recipient_info.get("channel", self.config["default_channel"])
            
            print(f"\n{'='*40}")
            success = self.send_notification(message, recipient, channel)
            results.append({
                "recipient": recipient,
                "channel": channel,
                "success": success
            })
        
        # 统计结果
        success_count = sum(1 for r in results if r["success"])
        print(f"\n📊 发送统计:")
        print(f"   总数: {len(results)}")
        print(f"   成功: {success_count}")
        print(f"   失败: {len(results) - success_count}")


# ==================== 演示函数 ====================
def demo_basic_notification():
    """演示基本通知发送"""
    print("=== 基本通知发送演示 ===\n")
    
    # 创建不同类型的通知工厂
    factories = {
        "邮件": EmailNotificationFactory(),
        "短信": SMSNotificationFactory(),
        "推送": PushNotificationFactory(),
        "微信": WeChatNotificationFactory()
    }
    
    message = "您的订单已发货，预计明天送达。"
    recipients = {
        "邮件": "user@example.com",
        "短信": "13800138000",
        "推送": "device_token_123",
        "微信": "wxid_user123"
    }
    
    for channel_name, factory in factories.items():
        print(f"\n{'='*50}")
        print(f"使用 {channel_name} 发送通知")
        print('='*50)
        
        recipient = recipients[channel_name]
        factory.send_notification(message, recipient)


def demo_notification_manager():
    """演示通知管理器"""
    print("\n" + "="*60)
    print("通知管理器演示")
    print("="*60)
    
    manager = NotificationManager()
    
    # 单个通知发送
    print("\n1. 单个通知发送:")
    manager.send_notification("您的验证码是: 123456", "user@example.com", "email")
    
    # 批量通知发送
    print("\n2. 批量通知发送:")
    recipients = [
        {"contact": "admin@example.com", "channel": "email"},
        {"contact": "13800138001", "channel": "sms"},
        {"contact": "device_token_456", "channel": "push"},
        {"contact": "wxid_admin", "channel": "wechat"}
    ]
    
    manager.batch_send("系统维护通知：今晚22:00-24:00进行系统维护", recipients)


def main():
    """主函数"""
    demo_basic_notification()
    demo_notification_manager()
    
    print("\n" + "="*60)
    print("工厂方法模式在通知系统中的优势:")
    print("1. 易于扩展：可以轻松添加新的通知渠道")
    print("2. 配置驱动：可以通过配置动态选择通知方式")
    print("3. 统一接口：所有通知方式都有相同的调用接口")
    print("4. 业务解耦：通知发送逻辑与具体实现解耦")
    print("="*60)


if __name__ == "__main__":
    main()
