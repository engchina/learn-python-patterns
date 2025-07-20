#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
聊天系统中介者应用

本模块演示了中介者模式在聊天系统中的应用，包括：
1. 多用户聊天室
2. 私聊和群聊功能
3. 用户状态管理
4. 消息路由和过滤

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional
from datetime import datetime
from enum import Enum
import uuid


class UserStatus(Enum):
    """用户状态枚举"""
    ONLINE = "在线"
    AWAY = "离开"
    BUSY = "忙碌"
    OFFLINE = "离线"


class MessageType(Enum):
    """消息类型枚举"""
    TEXT = "文本"
    IMAGE = "图片"
    FILE = "文件"
    SYSTEM = "系统"


class Message:
    """消息类"""
    
    def __init__(self, sender_id: str, content: str, msg_type: MessageType = MessageType.TEXT):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now()
        self.is_read = False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'content': self.content,
            'type': self.msg_type.value,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read
        }


class ChatMediator(ABC):
    """聊天中介者接口"""
    
    @abstractmethod
    def send_message(self, sender_id: str, content: str, target_id: str = None) -> bool:
        """发送消息"""
        pass
    
    @abstractmethod
    def add_user(self, user: 'User') -> bool:
        """添加用户"""
        pass
    
    @abstractmethod
    def remove_user(self, user_id: str) -> bool:
        """移除用户"""
        pass
    
    @abstractmethod
    def join_room(self, user_id: str, room_name: str) -> bool:
        """加入房间"""
        pass
    
    @abstractmethod
    def leave_room(self, user_id: str, room_name: str) -> bool:
        """离开房间"""
        pass


class User:
    """用户类"""
    
    def __init__(self, user_id: str, username: str, mediator: ChatMediator = None):
        self.user_id = user_id
        self.username = username
        self.status = UserStatus.OFFLINE
        self.mediator = mediator
        self.current_rooms: Set[str] = set()
        self.message_history: List[Message] = []
        
        if mediator:
            mediator.add_user(self)
    
    def set_mediator(self, mediator: ChatMediator) -> None:
        """设置中介者"""
        self.mediator = mediator
        mediator.add_user(self)
    
    def set_status(self, status: UserStatus) -> None:
        """设置用户状态"""
        old_status = self.status
        self.status = status
        print(f"👤 {self.username} 状态从 {old_status.value} 变更为 {status.value}")
        
        if self.mediator:
            self.mediator.notify_status_change(self.user_id, status)
    
    def send_message(self, content: str, target_id: str = None, room_name: str = None) -> bool:
        """发送消息"""
        if self.status == UserStatus.OFFLINE:
            print(f"❌ {self.username} 处于离线状态，无法发送消息")
            return False
        
        if not self.mediator:
            print(f"❌ {self.username} 未连接到聊天系统")
            return False
        
        # 显示发送的消息
        timestamp = datetime.now().strftime("%H:%M:%S")
        if target_id:
            print(f"[{timestamp}] 📤 {self.username} 私聊 -> {target_id}: {content}")
        elif room_name:
            print(f"[{timestamp}] 📤 {self.username} 在 {room_name}: {content}")
        else:
            print(f"[{timestamp}] 📤 {self.username} 群发: {content}")
        
        return self.mediator.send_message(self.user_id, content, target_id, room_name)
    
    def receive_message(self, message: Message, sender_name: str = None, room_name: str = None) -> None:
        """接收消息"""
        if self.status == UserStatus.OFFLINE:
            return
        
        self.message_history.append(message)
        timestamp = message.timestamp.strftime("%H:%M:%S")
        
        if room_name:
            print(f"[{timestamp}] 📥 {self.username} 收到来自 {room_name} 的消息 ({sender_name}): {message.content}")
        else:
            print(f"[{timestamp}] 📥 {self.username} 收到私聊消息 ({sender_name}): {message.content}")
    
    def join_room(self, room_name: str) -> bool:
        """加入房间"""
        if not self.mediator:
            return False
        
        success = self.mediator.join_room(self.user_id, room_name)
        if success:
            self.current_rooms.add(room_name)
            print(f"🚪 {self.username} 加入房间: {room_name}")
        return success
    
    def leave_room(self, room_name: str) -> bool:
        """离开房间"""
        if not self.mediator:
            return False
        
        success = self.mediator.leave_room(self.user_id, room_name)
        if success:
            self.current_rooms.discard(room_name)
            print(f"🚪 {self.username} 离开房间: {room_name}")
        return success
    
    def get_status_info(self) -> Dict:
        """获取用户状态信息"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'status': self.status.value,
            'current_rooms': list(self.current_rooms),
            'message_count': len(self.message_history)
        }


class ChatRoom:
    """聊天房间"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.members: Set[str] = set()
        self.message_history: List[Message] = []
        self.created_at = datetime.now()
    
    def add_member(self, user_id: str) -> None:
        """添加成员"""
        self.members.add(user_id)
    
    def remove_member(self, user_id: str) -> None:
        """移除成员"""
        self.members.discard(user_id)
    
    def add_message(self, message: Message) -> None:
        """添加消息到历史记录"""
        self.message_history.append(message)
    
    def get_info(self) -> Dict:
        """获取房间信息"""
        return {
            'name': self.name,
            'description': self.description,
            'member_count': len(self.members),
            'message_count': len(self.message_history),
            'created_at': self.created_at.isoformat()
        }


class ChatSystemMediator(ChatMediator):
    """聊天系统中介者"""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.users: Dict[str, User] = {}
        self.rooms: Dict[str, ChatRoom] = {}
        self.private_messages: Dict[str, List[Message]] = {}  # 私聊消息记录
        self.blocked_users: Dict[str, Set[str]] = {}  # 黑名单
        
        # 创建默认房间
        self._create_default_rooms()
    
    def _create_default_rooms(self) -> None:
        """创建默认房间"""
        default_rooms = [
            ("大厅", "所有用户的公共聊天区域"),
            ("技术讨论", "技术相关话题讨论"),
            ("闲聊", "日常闲聊和娱乐"),
        ]
        
        for name, description in default_rooms:
            self.rooms[name] = ChatRoom(name, description)
    
    def add_user(self, user: User) -> bool:
        """添加用户"""
        if user.user_id in self.users:
            print(f"⚠️ 用户 {user.username} 已存在")
            return False
        
        self.users[user.user_id] = user
        user.set_status(UserStatus.ONLINE)
        
        # 自动加入大厅
        self.join_room(user.user_id, "大厅")
        
        # 通知其他用户
        self._broadcast_system_message(f"用户 {user.username} 加入了聊天系统")
        
        print(f"✅ 用户 {user.username} 已加入 {self.system_name}")
        return True
    
    def remove_user(self, user_id: str) -> bool:
        """移除用户"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        username = user.username
        
        # 从所有房间中移除
        for room_name in list(user.current_rooms):
            self.leave_room(user_id, room_name)
        
        # 设置为离线状态
        user.set_status(UserStatus.OFFLINE)
        
        # 从用户列表中移除
        del self.users[user_id]
        
        # 通知其他用户
        self._broadcast_system_message(f"用户 {username} 离开了聊天系统")
        
        print(f"👋 用户 {username} 已离开 {self.system_name}")
        return True
    
    def send_message(self, sender_id: str, content: str, target_id: str = None, room_name: str = None) -> bool:
        """发送消息"""
        if sender_id not in self.users:
            return False
        
        sender = self.users[sender_id]
        if sender.status == UserStatus.OFFLINE:
            return False
        
        # 创建消息对象
        message = Message(sender_id, content)
        
        if target_id:
            # 私聊消息
            return self._send_private_message(message, target_id)
        elif room_name:
            # 房间消息
            return self._send_room_message(message, room_name)
        else:
            # 广播消息（发送到用户当前所在的所有房间）
            return self._send_broadcast_message(message)
    
    def _send_private_message(self, message: Message, target_id: str) -> bool:
        """发送私聊消息"""
        if target_id not in self.users:
            print(f"❌ 目标用户不存在: {target_id}")
            return False
        
        sender = self.users[message.sender_id]
        target = self.users[target_id]
        
        # 检查是否被屏蔽
        if self._is_blocked(target_id, message.sender_id):
            print(f"❌ 消息被屏蔽: {target.username} 已屏蔽 {sender.username}")
            return False
        
        # 记录私聊消息
        chat_key = self._get_private_chat_key(message.sender_id, target_id)
        if chat_key not in self.private_messages:
            self.private_messages[chat_key] = []
        self.private_messages[chat_key].append(message)
        
        # 发送给目标用户
        target.receive_message(message, sender.username)
        return True
    
    def _send_room_message(self, message: Message, room_name: str) -> bool:
        """发送房间消息"""
        if room_name not in self.rooms:
            print(f"❌ 房间不存在: {room_name}")
            return False
        
        room = self.rooms[room_name]
        sender = self.users[message.sender_id]
        
        # 检查发送者是否在房间中
        if message.sender_id not in room.members:
            print(f"❌ {sender.username} 不在房间 {room_name} 中")
            return False
        
        # 添加到房间消息历史
        room.add_message(message)
        
        # 发送给房间内的所有成员（除了发送者）
        for member_id in room.members:
            if member_id != message.sender_id and member_id in self.users:
                member = self.users[member_id]
                if not self._is_blocked(member_id, message.sender_id):
                    member.receive_message(message, sender.username, room_name)
        
        return True
    
    def _send_broadcast_message(self, message: Message) -> bool:
        """发送广播消息"""
        sender = self.users[message.sender_id]
        success_count = 0
        
        # 发送到发送者所在的所有房间
        for room_name in sender.current_rooms:
            if self._send_room_message(message, room_name):
                success_count += 1
        
        return success_count > 0
    
    def join_room(self, user_id: str, room_name: str) -> bool:
        """用户加入房间"""
        if user_id not in self.users or room_name not in self.rooms:
            return False
        
        user = self.users[user_id]
        room = self.rooms[room_name]
        
        if user_id in room.members:
            print(f"⚠️ {user.username} 已在房间 {room_name} 中")
            return False
        
        room.add_member(user_id)
        
        # 通知房间内其他成员
        join_message = Message("system", f"{user.username} 加入了房间", MessageType.SYSTEM)
        room.add_message(join_message)
        
        for member_id in room.members:
            if member_id != user_id and member_id in self.users:
                member = self.users[member_id]
                member.receive_message(join_message, "系统", room_name)
        
        return True
    
    def leave_room(self, user_id: str, room_name: str) -> bool:
        """用户离开房间"""
        if user_id not in self.users or room_name not in self.rooms:
            return False
        
        user = self.users[user_id]
        room = self.rooms[room_name]
        
        if user_id not in room.members:
            return False
        
        room.remove_member(user_id)
        
        # 通知房间内其他成员
        leave_message = Message("system", f"{user.username} 离开了房间", MessageType.SYSTEM)
        room.add_message(leave_message)
        
        for member_id in room.members:
            if member_id in self.users:
                member = self.users[member_id]
                member.receive_message(leave_message, "系统", room_name)
        
        return True
    
    def notify_status_change(self, user_id: str, new_status: UserStatus) -> None:
        """通知用户状态变化"""
        if user_id not in self.users:
            return
        
        user = self.users[user_id]
        status_message = f"{user.username} 现在{new_status.value}"
        
        # 通知用户所在房间的其他成员
        for room_name in user.current_rooms:
            room = self.rooms[room_name]
            for member_id in room.members:
                if member_id != user_id and member_id in self.users:
                    member = self.users[member_id]
                    if member.status != UserStatus.OFFLINE:
                        print(f"📢 {member.username} 收到状态通知: {status_message}")
    
    def block_user(self, user_id: str, blocked_user_id: str) -> bool:
        """屏蔽用户"""
        if user_id not in self.users or blocked_user_id not in self.users:
            return False
        
        if user_id not in self.blocked_users:
            self.blocked_users[user_id] = set()
        
        self.blocked_users[user_id].add(blocked_user_id)
        
        user = self.users[user_id]
        blocked_user = self.users[blocked_user_id]
        print(f"🚫 {user.username} 已屏蔽 {blocked_user.username}")
        return True
    
    def unblock_user(self, user_id: str, blocked_user_id: str) -> bool:
        """取消屏蔽用户"""
        if user_id not in self.blocked_users:
            return False
        
        self.blocked_users[user_id].discard(blocked_user_id)
        
        user = self.users[user_id]
        unblocked_user = self.users[blocked_user_id]
        print(f"✅ {user.username} 已取消屏蔽 {unblocked_user.username}")
        return True
    
    def _is_blocked(self, user_id: str, sender_id: str) -> bool:
        """检查是否被屏蔽"""
        return (user_id in self.blocked_users and 
                sender_id in self.blocked_users[user_id])
    
    def _get_private_chat_key(self, user1_id: str, user2_id: str) -> str:
        """获取私聊键"""
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
    
    def _broadcast_system_message(self, content: str) -> None:
        """广播系统消息"""
        system_message = Message("system", content, MessageType.SYSTEM)
        
        for user in self.users.values():
            if user.status != UserStatus.OFFLINE:
                user.receive_message(system_message, "系统")
    
    def get_online_users(self) -> List[Dict]:
        """获取在线用户列表"""
        return [user.get_status_info() for user in self.users.values() 
                if user.status != UserStatus.OFFLINE]
    
    def get_room_info(self, room_name: str) -> Optional[Dict]:
        """获取房间信息"""
        if room_name in self.rooms:
            return self.rooms[room_name].get_info()
        return None
    
    def get_available_rooms(self) -> List[str]:
        """获取可用房间列表"""
        return list(self.rooms.keys())


def demo_chat_system():
    """演示聊天系统"""
    print("=" * 50)
    print("💬 聊天系统中介者演示")
    print("=" * 50)
    
    # 创建聊天系统
    chat_system = ChatSystemMediator("技术交流群")
    
    # 创建用户
    alice = User("user_001", "Alice", chat_system)
    bob = User("user_002", "Bob", chat_system)
    charlie = User("user_003", "Charlie", chat_system)
    diana = User("user_004", "Diana", chat_system)
    
    print(f"\n📋 可用房间: {chat_system.get_available_rooms()}")
    
    # 用户加入不同房间
    print("\n🚪 用户加入房间:")
    alice.join_room("技术讨论")
    bob.join_room("技术讨论")
    charlie.join_room("闲聊")
    diana.join_room("技术讨论")
    diana.join_room("闲聊")
    
    # 房间内群聊
    print("\n💬 房间群聊:")
    alice.send_message("大家好！有人在讨论Python吗？", room_name="技术讨论")
    bob.send_message("我在！最近在学习设计模式", room_name="技术讨论")
    diana.send_message("中介者模式很有用呢", room_name="技术讨论")
    
    # 私聊
    print("\n🔒 私聊消息:")
    alice.send_message("Bob，你有好的Python书籍推荐吗？", target_id="user_002")
    bob.send_message("推荐《Effective Python》", target_id="user_001")
    
    # 用户状态变化
    print("\n📱 用户状态变化:")
    charlie.set_status(UserStatus.AWAY)
    diana.set_status(UserStatus.BUSY)
    
    # 屏蔽功能
    print("\n🚫 屏蔽功能演示:")
    chat_system.block_user("user_003", "user_001")  # Charlie屏蔽Alice
    alice.send_message("Charlie，你在吗？", target_id="user_003")  # 这条消息会被屏蔽
    
    # 显示在线用户
    print("\n👥 当前在线用户:")
    for user_info in chat_system.get_online_users():
        print(f"  {user_info}")
    
    # 用户离开
    print("\n👋 用户离开:")
    chat_system.remove_user("user_004")


if __name__ == "__main__":
    print("🎯 聊天系统中介者模式演示")
    
    demo_chat_system()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 中介者模式简化了用户间的复杂通信逻辑")
    print("=" * 50)
