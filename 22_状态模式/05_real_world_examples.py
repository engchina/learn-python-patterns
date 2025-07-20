"""
05_real_world_examples.py - 实际项目中的状态模式应用

这个示例展示了状态模式在实际项目中的复杂应用场景，
包括媒体播放器、网络连接管理、工作流系统等。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import threading
import time
from datetime import datetime, timedelta
import random


# ==================== 媒体播放器状态机 ====================

class MediaPlayerState(ABC):
    """媒体播放器状态抽象类"""
    
    @abstractmethod
    def play(self, player: 'MediaPlayer') -> bool:
        pass
    
    @abstractmethod
    def pause(self, player: 'MediaPlayer') -> bool:
        pass
    
    @abstractmethod
    def stop(self, player: 'MediaPlayer') -> bool:
        pass
    
    @abstractmethod
    def seek(self, player: 'MediaPlayer', position: float) -> bool:
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        pass


class MediaPlayer:
    """媒体播放器"""
    
    def __init__(self):
        self._state: MediaPlayerState = StoppedState()
        self._current_media: Optional[str] = None
        self._position: float = 0.0
        self._duration: float = 0.0
        self._volume: float = 1.0
        self._is_muted: bool = False
        self._play_thread: Optional[threading.Thread] = None
        self._is_playing: bool = False
        self._observers: List[Callable] = []
        
        print("🎵 媒体播放器初始化")
    
    def add_observer(self, observer: Callable) -> None:
        """添加观察者"""
        self._observers.append(observer)
    
    def _notify_observers(self, event: str, data: Dict[str, Any] = None) -> None:
        """通知观察者"""
        for observer in self._observers:
            observer(event, data or {})
    
    def set_state(self, new_state: MediaPlayerState) -> None:
        """设置新状态"""
        old_state = self._state.get_state_name()
        self._state = new_state
        new_state_name = self._state.get_state_name()
        
        print(f"🔄 播放器状态: {old_state} → {new_state_name}")
        self._notify_observers("state_changed", {
            "old_state": old_state,
            "new_state": new_state_name
        })
    
    def load_media(self, media_path: str, duration: float = 180.0) -> bool:
        """加载媒体文件"""
        if isinstance(self._state, PlayingState):
            self.stop()
        
        self._current_media = media_path
        self._duration = duration
        self._position = 0.0
        
        print(f"📁 加载媒体: {media_path} (时长: {duration:.1f}秒)")
        self._notify_observers("media_loaded", {
            "media": media_path,
            "duration": duration
        })
        
        self.set_state(LoadedState())
        return True
    
    def play(self) -> bool:
        """播放"""
        return self._state.play(self)
    
    def pause(self) -> bool:
        """暂停"""
        return self._state.pause(self)
    
    def stop(self) -> bool:
        """停止"""
        return self._state.stop(self)
    
    def seek(self, position: float) -> bool:
        """跳转到指定位置"""
        return self._state.seek(self, position)
    
    def set_volume(self, volume: float) -> None:
        """设置音量"""
        self._volume = max(0.0, min(1.0, volume))
        print(f"🔊 音量设置为: {self._volume:.1f}")
    
    def mute(self) -> None:
        """静音"""
        self._is_muted = not self._is_muted
        status = "静音" if self._is_muted else "取消静音"
        print(f"🔇 {status}")
    
    def _start_playback(self) -> None:
        """开始播放线程"""
        self._is_playing = True
        self._play_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self._play_thread.start()
    
    def _stop_playback(self) -> None:
        """停止播放线程"""
        self._is_playing = False
        if self._play_thread and self._play_thread.is_alive():
            self._play_thread.join(timeout=1)
    
    def _playback_loop(self) -> None:
        """播放循环"""
        while self._is_playing and self._position < self._duration:
            time.sleep(0.1)
            if self._is_playing:
                self._position += 0.1
                
                # 通知进度更新
                if int(self._position * 10) % 10 == 0:  # 每秒通知一次
                    self._notify_observers("progress_update", {
                        "position": self._position,
                        "duration": self._duration,
                        "percentage": (self._position / self._duration) * 100
                    })
        
        # 播放结束
        if self._position >= self._duration:
            print("🎵 播放完成")
            self.set_state(LoadedState())
            self._notify_observers("playback_finished", {})
    
    def get_status(self) -> Dict[str, Any]:
        """获取播放器状态"""
        return {
            "state": self._state.get_state_name(),
            "media": self._current_media,
            "position": self._position,
            "duration": self._duration,
            "volume": self._volume,
            "is_muted": self._is_muted,
            "progress_percentage": (self._position / self._duration * 100) if self._duration > 0 else 0
        }


# 媒体播放器状态实现
class StoppedState(MediaPlayerState):
    """停止状态"""
    
    def play(self, player: MediaPlayer) -> bool:
        if not player._current_media:
            print("❌ 没有加载媒体文件")
            return False
        
        player._position = 0.0
        player.set_state(PlayingState())
        player._start_playback()
        print("▶️ 开始播放")
        return True
    
    def pause(self, player: MediaPlayer) -> bool:
        print("⚠️ 播放器已停止")
        return False
    
    def stop(self, player: MediaPlayer) -> bool:
        print("⚠️ 播放器已停止")
        return False
    
    def seek(self, player: MediaPlayer, position: float) -> bool:
        print("⚠️ 停止状态无法跳转")
        return False
    
    def get_state_name(self) -> str:
        return "停止"


class LoadedState(MediaPlayerState):
    """已加载状态"""
    
    def play(self, player: MediaPlayer) -> bool:
        player.set_state(PlayingState())
        player._start_playback()
        print("▶️ 开始播放")
        return True
    
    def pause(self, player: MediaPlayer) -> bool:
        print("⚠️ 媒体未播放")
        return False
    
    def stop(self, player: MediaPlayer) -> bool:
        player._position = 0.0
        player.set_state(StoppedState())
        print("⏹️ 停止播放")
        return True
    
    def seek(self, player: MediaPlayer, position: float) -> bool:
        if 0 <= position <= player._duration:
            player._position = position
            print(f"⏭️ 跳转到: {position:.1f}秒")
            return True
        return False
    
    def get_state_name(self) -> str:
        return "已加载"


class PlayingState(MediaPlayerState):
    """播放状态"""
    
    def play(self, player: MediaPlayer) -> bool:
        print("⚠️ 正在播放中")
        return False
    
    def pause(self, player: MediaPlayer) -> bool:
        player._stop_playback()
        player.set_state(PausedState())
        print("⏸️ 暂停播放")
        return True
    
    def stop(self, player: MediaPlayer) -> bool:
        player._stop_playback()
        player._position = 0.0
        player.set_state(StoppedState())
        print("⏹️ 停止播放")
        return True
    
    def seek(self, player: MediaPlayer, position: float) -> bool:
        if 0 <= position <= player._duration:
            player._position = position
            print(f"⏭️ 跳转到: {position:.1f}秒")
            return True
        return False
    
    def get_state_name(self) -> str:
        return "播放中"


class PausedState(MediaPlayerState):
    """暂停状态"""
    
    def play(self, player: MediaPlayer) -> bool:
        player.set_state(PlayingState())
        player._start_playback()
        print("▶️ 继续播放")
        return True
    
    def pause(self, player: MediaPlayer) -> bool:
        print("⚠️ 已经暂停")
        return False
    
    def stop(self, player: MediaPlayer) -> bool:
        player._position = 0.0
        player.set_state(StoppedState())
        print("⏹️ 停止播放")
        return True
    
    def seek(self, player: MediaPlayer, position: float) -> bool:
        if 0 <= position <= player._duration:
            player._position = position
            print(f"⏭️ 跳转到: {position:.1f}秒")
            return True
        return False
    
    def get_state_name(self) -> str:
        return "暂停"


# ==================== 网络连接状态机 ====================

class ConnectionState(ABC):
    """网络连接状态抽象类"""
    
    @abstractmethod
    def connect(self, connection: 'NetworkConnection') -> bool:
        pass
    
    @abstractmethod
    def disconnect(self, connection: 'NetworkConnection') -> bool:
        pass
    
    @abstractmethod
    def send_data(self, connection: 'NetworkConnection', data: str) -> bool:
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        pass


class NetworkConnection:
    """网络连接管理器"""
    
    def __init__(self, server_address: str):
        self.server_address = server_address
        self._state: ConnectionState = DisconnectedState()
        self._retry_count = 0
        self._max_retries = 3
        self._connection_quality = 1.0
        self._last_ping = 0
        self._observers: List[Callable] = []
        
        print(f"🌐 网络连接管理器初始化: {server_address}")
    
    def add_observer(self, observer: Callable) -> None:
        self._observers.append(observer)
    
    def _notify_observers(self, event: str, data: Dict[str, Any] = None) -> None:
        for observer in self._observers:
            observer(event, data or {})
    
    def set_state(self, new_state: ConnectionState) -> None:
        old_state = self._state.get_state_name()
        self._state = new_state
        new_state_name = self._state.get_state_name()
        
        print(f"🔄 连接状态: {old_state} → {new_state_name}")
        self._notify_observers("state_changed", {
            "old_state": old_state,
            "new_state": new_state_name
        })
    
    def connect(self) -> bool:
        return self._state.connect(self)
    
    def disconnect(self) -> bool:
        return self._state.disconnect(self)
    
    def send_data(self, data: str) -> bool:
        return self._state.send_data(self, data)
    
    def _simulate_connection(self) -> bool:
        """模拟连接过程"""
        print("🔌 正在连接服务器...")
        time.sleep(1)  # 模拟连接延迟
        
        # 模拟连接成功/失败
        success_rate = 0.8 - (self._retry_count * 0.2)
        return random.random() < success_rate
    
    def _simulate_network_quality(self) -> None:
        """模拟网络质量变化"""
        self._connection_quality = random.uniform(0.3, 1.0)
        if self._connection_quality < 0.5:
            print("⚠️ 网络质量较差")
            if isinstance(self._state, ConnectedState):
                self.set_state(UnstableState())
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self._state.get_state_name(),
            "server": self.server_address,
            "retry_count": self._retry_count,
            "connection_quality": self._connection_quality,
            "last_ping": self._last_ping
        }


# 网络连接状态实现
class DisconnectedState(ConnectionState):
    def connect(self, connection: NetworkConnection) -> bool:
        connection.set_state(ConnectingState())
        return connection._state.connect(connection)
    
    def disconnect(self, connection: NetworkConnection) -> bool:
        print("⚠️ 已经断开连接")
        return False
    
    def send_data(self, connection: NetworkConnection, data: str) -> bool:
        print("❌ 未连接，无法发送数据")
        return False
    
    def get_state_name(self) -> str:
        return "断开连接"


class ConnectingState(ConnectionState):
    def connect(self, connection: NetworkConnection) -> bool:
        if connection._simulate_connection():
            connection._retry_count = 0
            connection.set_state(ConnectedState())
            print("✅ 连接成功")
            return True
        else:
            connection._retry_count += 1
            if connection._retry_count >= connection._max_retries:
                print("❌ 连接失败，超过最大重试次数")
                connection.set_state(DisconnectedState())
            else:
                print(f"❌ 连接失败，准备重试 ({connection._retry_count}/{connection._max_retries})")
                time.sleep(1)
                return self.connect(connection)
            return False
    
    def disconnect(self, connection: NetworkConnection) -> bool:
        connection.set_state(DisconnectedState())
        print("🔌 取消连接")
        return True
    
    def send_data(self, connection: NetworkConnection, data: str) -> bool:
        print("❌ 正在连接中，无法发送数据")
        return False
    
    def get_state_name(self) -> str:
        return "连接中"


class ConnectedState(ConnectionState):
    def connect(self, connection: NetworkConnection) -> bool:
        print("⚠️ 已经连接")
        return True
    
    def disconnect(self, connection: NetworkConnection) -> bool:
        connection.set_state(DisconnectedState())
        print("🔌 断开连接")
        return True
    
    def send_data(self, connection: NetworkConnection, data: str) -> bool:
        # 模拟网络质量检查
        connection._simulate_network_quality()
        
        if connection._connection_quality > 0.7:
            print(f"📤 发送数据: {data}")
            return True
        else:
            print("❌ 网络质量差，发送失败")
            return False
    
    def get_state_name(self) -> str:
        return "已连接"


class UnstableState(ConnectionState):
    def connect(self, connection: NetworkConnection) -> bool:
        print("⚠️ 连接不稳定")
        return False
    
    def disconnect(self, connection: NetworkConnection) -> bool:
        connection.set_state(DisconnectedState())
        print("🔌 断开不稳定连接")
        return True
    
    def send_data(self, connection: NetworkConnection, data: str) -> bool:
        # 不稳定状态下有概率发送失败
        if random.random() < 0.3:
            print(f"📤 勉强发送数据: {data}")
            return True
        else:
            print("❌ 连接不稳定，发送失败")
            # 可能断开连接
            if random.random() < 0.2:
                connection.set_state(DisconnectedState())
            return False
    
    def get_state_name(self) -> str:
        return "连接不稳定"


# ==================== 演示函数 ====================

def demo_media_player():
    """媒体播放器演示"""
    print("=" * 60)
    print("🎵 媒体播放器状态机演示")
    print("=" * 60)
    
    # 创建播放器
    player = MediaPlayer()
    
    # 添加事件监听
    def on_player_event(event: str, data: Dict[str, Any]):
        if event == "progress_update":
            progress = data.get("percentage", 0)
            if int(progress) % 20 == 0:  # 每20%显示一次
                print(f"📊 播放进度: {progress:.1f}%")
    
    player.add_observer(on_player_event)
    
    # 测试播放器操作
    print("\n📋 播放器操作测试:")
    
    # 尝试播放（没有媒体）
    player.play()
    
    # 加载媒体
    player.load_media("demo_song.mp3", 10.0)
    
    # 播放
    player.play()
    
    # 等待一段时间
    time.sleep(3)
    
    # 暂停
    player.pause()
    
    # 跳转
    player.seek(7.0)
    
    # 继续播放
    player.play()
    
    # 等待播放完成
    time.sleep(4)
    
    print(f"\n📊 最终状态: {player.get_status()}")


def demo_network_connection():
    """网络连接演示"""
    print("\n" + "=" * 60)
    print("🌐 网络连接状态机演示")
    print("=" * 60)
    
    # 创建连接
    connection = NetworkConnection("192.168.1.100:8080")
    
    # 添加事件监听
    def on_connection_event(event: str, data: Dict[str, Any]):
        if event == "state_changed":
            print(f"📡 连接状态变化: {data['old_state']} → {data['new_state']}")
    
    connection.add_observer(on_connection_event)
    
    print("\n📋 网络连接测试:")
    
    # 尝试发送数据（未连接）
    connection.send_data("Hello Server")
    
    # 连接服务器
    connection.connect()
    
    # 发送数据
    if connection._state.get_state_name() == "已连接":
        connection.send_data("Hello Server")
        connection.send_data("How are you?")
    
    # 模拟网络质量变化
    print("\n🌐 模拟网络质量变化:")
    for i in range(3):
        connection.send_data(f"Message {i+1}")
        time.sleep(0.5)
    
    # 断开连接
    connection.disconnect()
    
    print(f"\n📊 最终状态: {connection.get_status()}")


if __name__ == "__main__":
    # 运行媒体播放器演示
    demo_media_player()
    
    # 运行网络连接演示
    demo_network_connection()
    
    print("\n" + "=" * 60)
    print("✅ 实际项目应用演示完成")
    print("💡 学习要点:")
    print("   - 状态模式在复杂系统中的应用")
    print("   - 多线程环境下的状态管理")
    print("   - 状态转换的业务逻辑封装")
    print("   - 观察者模式与状态模式的结合")
    print("=" * 60)
