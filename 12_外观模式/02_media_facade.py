"""
02_media_facade.py - 媒体播放器外观示例

这个示例展示了如何使用外观模式来简化复杂的媒体播放系统。
媒体播放器包含音频处理、视频处理、字幕处理等多个子系统，
外观模式提供了统一的播放接口，隐藏了底层的复杂性。
"""

from typing import Optional
import time
from enum import Enum


class MediaType(Enum):
    """媒体类型枚举"""
    AUDIO = "音频"
    VIDEO = "视频"


class AudioFormat(Enum):
    """音频格式枚举"""
    MP3 = "MP3"
    WAV = "WAV"
    FLAC = "FLAC"


class VideoFormat(Enum):
    """视频格式枚举"""
    MP4 = "MP4"
    AVI = "AVI"
    MKV = "MKV"


# ==================== 子系统：音频处理 ====================
class AudioProcessor:
    """音频处理子系统"""
    
    def __init__(self):
        self.current_audio = None
        self.volume = 50
        self.is_muted = False
        self.equalizer_settings = {"低音": 0, "中音": 0, "高音": 0}
    
    def load_audio(self, file_path: str, format: AudioFormat):
        """加载音频文件"""
        self.current_audio = {
            "path": file_path,
            "format": format.value,
            "duration": "3:45",
            "bitrate": "320kbps"
        }
        return f"音频处理器: 已加载{format.value}格式音频文件 '{file_path}'"
    
    def start_playback(self):
        """开始播放音频"""
        if self.current_audio:
            return f"音频处理器: 开始播放音频，音量{self.volume}%"
        return "音频处理器: 没有加载音频文件"
    
    def stop_playback(self):
        """停止播放音频"""
        return "音频处理器: 音频播放已停止"
    
    def set_volume(self, volume: int):
        """设置音量"""
        self.volume = max(0, min(100, volume))
        return f"音频处理器: 音量已设置为{self.volume}%"
    
    def set_equalizer(self, low: int, mid: int, high: int):
        """设置均衡器"""
        self.equalizer_settings = {"低音": low, "中音": mid, "高音": high}
        return f"音频处理器: 均衡器已设置 - 低音:{low}, 中音:{mid}, 高音:{high}"


# ==================== 子系统：视频处理 ====================
class VideoProcessor:
    """视频处理子系统"""
    
    def __init__(self):
        self.current_video = None
        self.brightness = 50
        self.contrast = 50
        self.resolution = "1920x1080"
        self.frame_rate = 30
    
    def load_video(self, file_path: str, format: VideoFormat):
        """加载视频文件"""
        self.current_video = {
            "path": file_path,
            "format": format.value,
            "duration": "1:32:45",
            "resolution": self.resolution,
            "frame_rate": f"{self.frame_rate}fps"
        }
        return f"视频处理器: 已加载{format.value}格式视频文件 '{file_path}'"
    
    def start_playback(self):
        """开始播放视频"""
        if self.current_video:
            return f"视频处理器: 开始播放视频，分辨率{self.resolution}@{self.frame_rate}fps"
        return "视频处理器: 没有加载视频文件"
    
    def stop_playback(self):
        """停止播放视频"""
        return "视频处理器: 视频播放已停止"
    
    def set_brightness(self, brightness: int):
        """设置亮度"""
        self.brightness = max(0, min(100, brightness))
        return f"视频处理器: 亮度已设置为{self.brightness}%"
    
    def set_contrast(self, contrast: int):
        """设置对比度"""
        self.contrast = max(0, min(100, contrast))
        return f"视频处理器: 对比度已设置为{self.contrast}%"


# ==================== 子系统：字幕处理 ====================
class SubtitleProcessor:
    """字幕处理子系统"""
    
    def __init__(self):
        self.current_subtitle = None
        self.is_enabled = False
        self.font_size = 16
        self.font_color = "白色"
    
    def load_subtitle(self, file_path: str):
        """加载字幕文件"""
        self.current_subtitle = {
            "path": file_path,
            "encoding": "UTF-8",
            "lines": 1250
        }
        return f"字幕处理器: 已加载字幕文件 '{file_path}'"
    
    def enable_subtitle(self):
        """启用字幕"""
        if self.current_subtitle:
            self.is_enabled = True
            return "字幕处理器: 字幕已启用"
        return "字幕处理器: 没有加载字幕文件"
    
    def disable_subtitle(self):
        """禁用字幕"""
        self.is_enabled = False
        return "字幕处理器: 字幕已禁用"
    
    def set_font_size(self, size: int):
        """设置字体大小"""
        self.font_size = max(8, min(72, size))
        return f"字幕处理器: 字体大小已设置为{self.font_size}px"


# ==================== 子系统：播放控制 ====================
class PlaybackController:
    """播放控制子系统"""
    
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.playback_speed = 1.0
    
    def play(self):
        """播放"""
        self.is_playing = True
        self.is_paused = False
        return "播放控制器: 开始播放"
    
    def pause(self):
        """暂停"""
        if self.is_playing:
            self.is_paused = True
            return "播放控制器: 播放已暂停"
        return "播放控制器: 当前没有播放内容"
    
    def stop(self):
        """停止"""
        self.is_playing = False
        self.is_paused = False
        return "播放控制器: 播放已停止"
    
    def set_speed(self, speed: float):
        """设置播放速度"""
        self.playback_speed = max(0.25, min(4.0, speed))
        return f"播放控制器: 播放速度已设置为{self.playback_speed}x"


# ==================== 外观类：媒体播放器 ====================
class MediaPlayerFacade:
    """媒体播放器外观类
    
    提供简化的接口来控制复杂的媒体播放系统，
    将音频、视频、字幕等子系统的操作封装成简单易用的方法。
    """
    
    def __init__(self):
        # 初始化所有子系统
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
        self.subtitle_processor = SubtitleProcessor()
        self.playback_controller = PlaybackController()
        self.current_media_type = None
    
    def play_audio(self, file_path: str, format: AudioFormat = AudioFormat.MP3):
        """播放音频文件"""
        print(f"🎵 准备播放音频文件: {file_path}")
        
        actions = [
            self.audio_processor.load_audio(file_path, format),
            self.audio_processor.start_playback(),
            self.playback_controller.play()
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
        
        self.current_media_type = MediaType.AUDIO
        print("🎶 音频播放已开始！")
    
    def play_video(self, file_path: str, format: VideoFormat = VideoFormat.MP4, 
                   subtitle_path: Optional[str] = None):
        """播放视频文件（可选字幕）"""
        print(f"🎬 准备播放视频文件: {file_path}")
        
        actions = [
            self.video_processor.load_video(file_path, format),
            self.audio_processor.load_audio(file_path, AudioFormat.MP3),
            self.video_processor.start_playback(),
            self.audio_processor.start_playback(),
            self.playback_controller.play()
        ]
        
        # 如果有字幕文件，加载并启用字幕
        if subtitle_path:
            actions.extend([
                self.subtitle_processor.load_subtitle(subtitle_path),
                self.subtitle_processor.enable_subtitle()
            ])
        
        for action in actions:
            print(f"  ✓ {action}")
        
        self.current_media_type = MediaType.VIDEO
        print("🎥 视频播放已开始！")
    
    def pause_playback(self):
        """暂停播放"""
        print("⏸️ 暂停播放...")
        result = self.playback_controller.pause()
        print(f"  ✓ {result}")
    
    def stop_playback(self):
        """停止播放"""
        print("⏹️ 停止播放...")
        
        actions = [
            self.playback_controller.stop(),
            self.audio_processor.stop_playback()
        ]
        
        if self.current_media_type == MediaType.VIDEO:
            actions.append(self.video_processor.stop_playback())
        
        for action in actions:
            print(f"  ✓ {action}")
        
        self.current_media_type = None
        print("🛑 播放已完全停止！")
    
    def create_cinema_mode(self):
        """影院模式：优化视频和音频设置"""
        if self.current_media_type != MediaType.VIDEO:
            print("⚠️ 影院模式仅适用于视频播放")
            return
        
        print("🎭 启动影院模式...")
        
        actions = [
            self.video_processor.set_brightness(45),
            self.video_processor.set_contrast(60),
            self.audio_processor.set_volume(75),
            self.audio_processor.set_equalizer(5, 0, 3),
            self.subtitle_processor.set_font_size(18)
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
        
        print("🍿 影院模式已启动！享受观影体验！")
    
    def create_music_mode(self):
        """音乐模式：优化音频设置"""
        print("🎼 启动音乐模式...")
        
        actions = [
            self.audio_processor.set_volume(60),
            self.audio_processor.set_equalizer(3, 2, 4),
            self.playback_controller.set_speed(1.0)
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
        
        print("🎵 音乐模式已启动！享受音乐时光！")


# ==================== 使用示例 ====================
def demo_media_facade():
    """媒体播放器外观模式演示"""
    print("=" * 60)
    print("🎬 媒体播放器系统演示 - 外观模式应用")
    print("=" * 60)
    
    # 创建媒体播放器
    player = MediaPlayerFacade()
    
    # 演示音频播放
    print("\n" + "="*20 + " 音频播放演示 " + "="*20)
    player.play_audio("我的音乐.mp3", AudioFormat.MP3)
    time.sleep(1)
    
    player.create_music_mode()
    time.sleep(1)
    
    player.pause_playback()
    time.sleep(1)
    
    player.stop_playback()
    time.sleep(1)
    
    # 演示视频播放
    print("\n" + "="*20 + " 视频播放演示 " + "="*20)
    player.play_video("电影.mp4", VideoFormat.MP4, "电影字幕.srt")
    time.sleep(1)
    
    player.create_cinema_mode()
    time.sleep(1)
    
    player.stop_playback()
    
    print("\n" + "="*60)
    print("🎯 演示完成！外观模式成功简化了复杂的媒体播放系统！")
    print("="*60)


if __name__ == "__main__":
    demo_media_facade()
