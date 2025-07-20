"""
桥接模式媒体应用 - 多媒体播放器系统

这个示例展示了桥接模式在媒体播放器中的应用，演示如何将
播放控制（抽象）与播放引擎（实现）分离，支持多种媒体格式。

作者: Bridge Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import time
from enum import Enum


class MediaState(Enum):
    """媒体播放状态"""
    STOPPED = "停止"
    PLAYING = "播放中"
    PAUSED = "暂停"
    LOADING = "加载中"


class MediaType(Enum):
    """媒体类型"""
    AUDIO = "音频"
    VIDEO = "视频"
    STREAM = "流媒体"


# ==================== 实现层接口 ====================

class MediaEngine(ABC):
    """媒体播放引擎接口 - 实现层"""
    
    @abstractmethod
    def load_media(self, file_path: str) -> bool:
        """加载媒体文件"""
        pass
    
    @abstractmethod
    def play(self) -> bool:
        """播放"""
        pass
    
    @abstractmethod
    def pause(self) -> bool:
        """暂停"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """停止"""
        pass
    
    @abstractmethod
    def seek(self, position: float) -> bool:
        """跳转到指定位置（秒）"""
        pass
    
    @abstractmethod
    def set_volume(self, volume: float) -> bool:
        """设置音量（0.0-1.0）"""
        pass
    
    @abstractmethod
    def get_duration(self) -> float:
        """获取媒体总时长（秒）"""
        pass
    
    @abstractmethod
    def get_position(self) -> float:
        """获取当前播放位置（秒）"""
        pass
    
    @abstractmethod
    def get_engine_info(self) -> str:
        """获取引擎信息"""
        pass


# ==================== 具体实现 ====================

class VLCEngine(MediaEngine):
    """VLC播放引擎 - 具体实现A"""
    
    def __init__(self):
        self.current_file = ""
        self.state = MediaState.STOPPED
        self.volume = 0.5
        self.position = 0.0
        self.duration = 0.0
        self.supported_formats = [".mp4", ".avi", ".mkv", ".mp3", ".wav", ".flac"]
    
    def load_media(self, file_path: str) -> bool:
        """加载媒体文件"""
        print(f"🎬 VLC引擎加载媒体: {file_path}")
        
        # 检查格式支持
        file_ext = file_path.lower().split('.')[-1] if '.' in file_path else ""
        if f".{file_ext}" not in self.supported_formats:
            print(f"   ❌ VLC不支持格式: .{file_ext}")
            return False
        
        self.current_file = file_path
        self.state = MediaState.LOADING
        
        # 模拟加载时间
        time.sleep(0.1)
        
        # 模拟获取媒体信息
        if "video" in file_path.lower():
            self.duration = 120.0  # 2分钟视频
        else:
            self.duration = 180.0  # 3分钟音频
        
        self.position = 0.0
        self.state = MediaState.STOPPED
        print(f"   ✅ VLC加载成功，时长: {self.duration:.1f}秒")
        return True
    
    def play(self) -> bool:
        """播放"""
        if not self.current_file:
            print("   ❌ 没有加载媒体文件")
            return False
        
        print(f"▶️  VLC开始播放: {self.current_file}")
        self.state = MediaState.PLAYING
        return True
    
    def pause(self) -> bool:
        """暂停"""
        if self.state == MediaState.PLAYING:
            print(f"⏸️  VLC暂停播放")
            self.state = MediaState.PAUSED
            return True
        return False
    
    def stop(self) -> bool:
        """停止"""
        print(f"⏹️  VLC停止播放")
        self.state = MediaState.STOPPED
        self.position = 0.0
        return True
    
    def seek(self, position: float) -> bool:
        """跳转位置"""
        if 0 <= position <= self.duration:
            self.position = position
            print(f"⏭️  VLC跳转到: {position:.1f}秒")
            return True
        return False
    
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            print(f"🔊 VLC音量设置为: {volume:.1%}")
            return True
        return False
    
    def get_duration(self) -> float:
        return self.duration
    
    def get_position(self) -> float:
        return self.position
    
    def get_engine_info(self) -> str:
        return f"VLC引擎 (状态: {self.state.value}, 音量: {self.volume:.1%})"


class FFmpegEngine(MediaEngine):
    """FFmpeg播放引擎 - 具体实现B"""
    
    def __init__(self):
        self.current_file = ""
        self.state = MediaState.STOPPED
        self.volume = 0.8
        self.position = 0.0
        self.duration = 0.0
        self.codec_info = {}
    
    def load_media(self, file_path: str) -> bool:
        """加载媒体文件"""
        print(f"🎞️  FFmpeg引擎加载媒体: {file_path}")
        
        self.current_file = file_path
        self.state = MediaState.LOADING
        
        # 模拟编解码器检测
        time.sleep(0.15)
        
        if "video" in file_path.lower():
            self.duration = 150.0
            self.codec_info = {"video": "H.264", "audio": "AAC"}
        else:
            self.duration = 200.0
            self.codec_info = {"audio": "MP3"}
        
        self.position = 0.0
        self.state = MediaState.STOPPED
        print(f"   ✅ FFmpeg加载成功，编解码器: {self.codec_info}")
        return True
    
    def play(self) -> bool:
        """播放"""
        if not self.current_file:
            print("   ❌ 没有加载媒体文件")
            return False
        
        print(f"▶️  FFmpeg开始播放: {self.current_file}")
        print(f"   编解码器: {self.codec_info}")
        self.state = MediaState.PLAYING
        return True
    
    def pause(self) -> bool:
        """暂停"""
        if self.state == MediaState.PLAYING:
            print(f"⏸️  FFmpeg暂停播放")
            self.state = MediaState.PAUSED
            return True
        return False
    
    def stop(self) -> bool:
        """停止"""
        print(f"⏹️  FFmpeg停止播放")
        self.state = MediaState.STOPPED
        self.position = 0.0
        return True
    
    def seek(self, position: float) -> bool:
        """跳转位置"""
        if 0 <= position <= self.duration:
            self.position = position
            print(f"⏭️  FFmpeg精确跳转到: {position:.1f}秒")
            return True
        return False
    
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            print(f"🔊 FFmpeg音量设置为: {volume:.1%}")
            return True
        return False
    
    def get_duration(self) -> float:
        return self.duration
    
    def get_position(self) -> float:
        return self.position
    
    def get_engine_info(self) -> str:
        return f"FFmpeg引擎 (状态: {self.state.value}, 编解码器: {self.codec_info})"


class WebAudioEngine(MediaEngine):
    """Web Audio播放引擎 - 具体实现C"""
    
    def __init__(self):
        self.current_file = ""
        self.state = MediaState.STOPPED
        self.volume = 0.7
        self.position = 0.0
        self.duration = 0.0
        self.buffer_size = 0
        self.sample_rate = 44100
    
    def load_media(self, file_path: str) -> bool:
        """加载媒体文件"""
        print(f"🌐 WebAudio引擎加载媒体: {file_path}")
        
        # 只支持音频格式
        if not any(fmt in file_path.lower() for fmt in [".mp3", ".wav", ".ogg", ".m4a"]):
            print(f"   ❌ WebAudio只支持音频格式")
            return False
        
        self.current_file = file_path
        self.state = MediaState.LOADING
        
        # 模拟音频缓冲区加载
        time.sleep(0.2)
        
        self.duration = 240.0
        self.buffer_size = int(self.duration * self.sample_rate)
        self.position = 0.0
        self.state = MediaState.STOPPED
        
        print(f"   ✅ WebAudio加载成功，缓冲区大小: {self.buffer_size} 采样")
        return True
    
    def play(self) -> bool:
        """播放"""
        if not self.current_file:
            print("   ❌ 没有加载媒体文件")
            return False
        
        print(f"▶️  WebAudio开始播放: {self.current_file}")
        print(f"   采样率: {self.sample_rate}Hz")
        self.state = MediaState.PLAYING
        return True
    
    def pause(self) -> bool:
        """暂停"""
        if self.state == MediaState.PLAYING:
            print(f"⏸️  WebAudio暂停播放")
            self.state = MediaState.PAUSED
            return True
        return False
    
    def stop(self) -> bool:
        """停止"""
        print(f"⏹️  WebAudio停止播放")
        self.state = MediaState.STOPPED
        self.position = 0.0
        return True
    
    def seek(self, position: float) -> bool:
        """跳转位置"""
        if 0 <= position <= self.duration:
            self.position = position
            sample_position = int(position * self.sample_rate)
            print(f"⏭️  WebAudio跳转到: {position:.1f}秒 (采样位置: {sample_position})")
            return True
        return False
    
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            print(f"🔊 WebAudio音量设置为: {volume:.1%}")
            return True
        return False
    
    def get_duration(self) -> float:
        return self.duration
    
    def get_position(self) -> float:
        return self.position
    
    def get_engine_info(self) -> str:
        return f"WebAudio引擎 (状态: {self.state.value}, 采样率: {self.sample_rate}Hz)"


# ==================== 抽象层 ====================

class MediaPlayer:
    """媒体播放器抽象类 - 抽象层"""
    
    def __init__(self, engine: MediaEngine):
        self.engine = engine
        self.playlist: List[str] = []
        self.current_index = -1
    
    def load(self, file_path: str) -> bool:
        """加载媒体文件"""
        return self.engine.load_media(file_path)
    
    def play(self) -> bool:
        """播放"""
        return self.engine.play()
    
    def pause(self) -> bool:
        """暂停"""
        return self.engine.pause()
    
    def stop(self) -> bool:
        """停止"""
        return self.engine.stop()
    
    def seek(self, position: float) -> bool:
        """跳转"""
        return self.engine.seek(position)
    
    def set_volume(self, volume: float) -> bool:
        """设置音量"""
        return self.engine.set_volume(volume)
    
    def get_info(self) -> Dict[str, any]:
        """获取播放器信息"""
        return {
            "engine": self.engine.get_engine_info(),
            "duration": self.engine.get_duration(),
            "position": self.engine.get_position(),
            "playlist_size": len(self.playlist)
        }
    
    def set_engine(self, engine: MediaEngine) -> None:
        """切换播放引擎"""
        self.engine = engine
        print(f"🔄 播放引擎已切换为: {engine.get_engine_info()}")


# ==================== 扩展抽象层 ====================

class PlaylistPlayer(MediaPlayer):
    """播放列表播放器 - 扩展抽象层"""
    
    def __init__(self, engine: MediaEngine):
        super().__init__(engine)
        self.repeat_mode = False
        self.shuffle_mode = False
    
    def add_to_playlist(self, file_path: str) -> None:
        """添加到播放列表"""
        self.playlist.append(file_path)
        print(f"➕ 已添加到播放列表: {file_path}")
    
    def play_playlist(self) -> bool:
        """播放播放列表"""
        if not self.playlist:
            print("❌ 播放列表为空")
            return False
        
        self.current_index = 0
        return self.play_current()
    
    def play_current(self) -> bool:
        """播放当前曲目"""
        if 0 <= self.current_index < len(self.playlist):
            current_file = self.playlist[self.current_index]
            print(f"🎵 播放列表 [{self.current_index + 1}/{len(self.playlist)}]: {current_file}")
            
            if self.load(current_file):
                return self.play()
        return False
    
    def next_track(self) -> bool:
        """下一首"""
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            print(f"⏭️  下一首")
            return self.play_current()
        elif self.repeat_mode:
            self.current_index = 0
            print(f"🔁 重复播放，回到第一首")
            return self.play_current()
        else:
            print(f"📋 播放列表结束")
            return False
    
    def previous_track(self) -> bool:
        """上一首"""
        if self.current_index > 0:
            self.current_index -= 1
            print(f"⏮️  上一首")
            return self.play_current()
        return False
    
    def set_repeat_mode(self, repeat: bool) -> None:
        """设置重复模式"""
        self.repeat_mode = repeat
        print(f"🔁 重复模式: {'开启' if repeat else '关闭'}")


class StreamingPlayer(MediaPlayer):
    """流媒体播放器 - 扩展抽象层"""
    
    def __init__(self, engine: MediaEngine):
        super().__init__(engine)
        self.buffer_percentage = 0.0
        self.network_quality = "良好"
    
    def load_stream(self, stream_url: str) -> bool:
        """加载流媒体"""
        print(f"📡 加载流媒体: {stream_url}")
        
        # 模拟缓冲过程
        for i in range(0, 101, 20):
            self.buffer_percentage = i
            print(f"   缓冲进度: {i}%")
            time.sleep(0.1)
        
        return self.load(stream_url)
    
    def get_stream_info(self) -> Dict[str, any]:
        """获取流媒体信息"""
        info = self.get_info()
        info.update({
            "buffer_percentage": self.buffer_percentage,
            "network_quality": self.network_quality,
            "stream_type": "live" if "live" in str(self.playlist) else "vod"
        })
        return info
    
    def adjust_quality(self, quality: str) -> None:
        """调整播放质量"""
        print(f"📺 调整播放质量为: {quality}")
        self.network_quality = quality


def demo_media_bridge():
    """媒体播放器桥接模式演示"""
    print("=" * 60)
    print("🎬 多媒体播放器系统 - 桥接模式演示")
    print("=" * 60)
    
    # 创建不同的播放引擎
    vlc_engine = VLCEngine()
    ffmpeg_engine = FFmpegEngine()
    webaudio_engine = WebAudioEngine()
    
    # 创建基本播放器
    player = MediaPlayer(vlc_engine)
    
    print("\n🔹 使用VLC引擎播放视频:")
    player.load("movie_trailer.mp4")
    player.play()
    player.seek(30.0)
    player.set_volume(0.8)
    
    print(f"\n🔄 切换到FFmpeg引擎:")
    player.set_engine(ffmpeg_engine)
    player.load("documentary.mkv")
    player.play()
    
    print(f"\n🔄 切换到WebAudio引擎:")
    player.set_engine(webaudio_engine)
    player.load("background_music.mp3")
    player.play()


def demo_playlist_player():
    """播放列表播放器演示"""
    print("\n" + "=" * 60)
    print("🎵 播放列表播放器演示")
    print("=" * 60)
    
    # 创建播放列表播放器
    vlc_engine = VLCEngine()
    playlist_player = PlaylistPlayer(vlc_engine)
    
    # 添加歌曲到播放列表
    songs = [
        "song1.mp3",
        "song2.wav",
        "song3.flac",
        "song4.mp3"
    ]
    
    for song in songs:
        playlist_player.add_to_playlist(song)
    
    # 播放播放列表
    print(f"\n🎵 开始播放播放列表:")
    playlist_player.set_repeat_mode(True)
    playlist_player.play_playlist()
    
    # 切换歌曲
    print(f"\n⏭️  切换歌曲:")
    playlist_player.next_track()
    playlist_player.next_track()


def demo_streaming_player():
    """流媒体播放器演示"""
    print("\n" + "=" * 60)
    print("📡 流媒体播放器演示")
    print("=" * 60)
    
    # 创建流媒体播放器
    ffmpeg_engine = FFmpegEngine()
    streaming_player = StreamingPlayer(ffmpeg_engine)
    
    # 加载流媒体
    streaming_player.load_stream("https://stream.example.com/live")
    streaming_player.play()
    
    # 调整质量
    streaming_player.adjust_quality("高清")
    
    # 显示流媒体信息
    info = streaming_player.get_stream_info()
    print(f"\n📊 流媒体信息:")
    for key, value in info.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    demo_media_bridge()
    demo_playlist_player()
    demo_streaming_player()
