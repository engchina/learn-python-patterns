"""
05_real_world_examples.py - 单例模式实际应用示例

这个文件包含了单例模式在实际项目中的应用示例，
展示了如何在真实场景中使用单例模式解决实际问题。
"""

import threading
import time
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from collections import defaultdict, deque


# ==================== 游戏开发：游戏管理器 ====================
class GameState(Enum):
    """游戏状态"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LOADING = "loading"


class GameManager:
    """游戏管理器单例"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.game_state = GameState.MENU
            self.current_level = 1
            self.score = 0
            self.lives = 3
            self.player_data = {}
            self.game_settings = {
                "difficulty": "normal",
                "sound_enabled": True,
                "music_volume": 0.8,
                "effects_volume": 0.6
            }
            self.achievements = set()
            self.session_start_time = datetime.now()
            self.total_play_time = timedelta()
            self.event_listeners = defaultdict(list)
            self.save_data = {}
            self.initialized = True
            print("游戏管理器已初始化")
    
    def start_new_game(self):
        """开始新游戏"""
        self.game_state = GameState.PLAYING
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.session_start_time = datetime.now()
        self._emit_event("game_started", {"level": self.current_level})
        print("新游戏已开始")
    
    def pause_game(self):
        """暂停游戏"""
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
            self._emit_event("game_paused", {})
            print("游戏已暂停")
    
    def resume_game(self):
        """恢复游戏"""
        if self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
            self._emit_event("game_resumed", {})
            print("游戏已恢复")
    
    def game_over(self):
        """游戏结束"""
        self.game_state = GameState.GAME_OVER
        session_time = datetime.now() - self.session_start_time
        self.total_play_time += session_time
        self._emit_event("game_over", {
            "final_score": self.score,
            "level_reached": self.current_level,
            "session_time": session_time.total_seconds()
        })
        print(f"游戏结束！最终得分: {self.score}")
    
    def add_score(self, points: int):
        """增加分数"""
        self.score += points
        self._emit_event("score_changed", {"score": self.score, "points_added": points})
        
        # 检查成就
        self._check_score_achievements()
    
    def lose_life(self):
        """失去生命"""
        self.lives -= 1
        self._emit_event("life_lost", {"lives_remaining": self.lives})
        
        if self.lives <= 0:
            self.game_over()
    
    def next_level(self):
        """进入下一关"""
        self.current_level += 1
        self._emit_event("level_completed", {"new_level": self.current_level})
        print(f"进入第 {self.current_level} 关")
    
    def unlock_achievement(self, achievement_id: str, achievement_name: str):
        """解锁成就"""
        if achievement_id not in self.achievements:
            self.achievements.add(achievement_id)
            self._emit_event("achievement_unlocked", {
                "id": achievement_id,
                "name": achievement_name
            })
            print(f"成就解锁: {achievement_name}")
    
    def _check_score_achievements(self):
        """检查分数相关成就"""
        if self.score >= 1000 and "score_1000" not in self.achievements:
            self.unlock_achievement("score_1000", "得分达人")
        if self.score >= 10000 and "score_10000" not in self.achievements:
            self.unlock_achievement("score_10000", "得分大师")
    
    def save_game(self) -> str:
        """保存游戏"""
        save_id = str(uuid.uuid4())
        self.save_data[save_id] = {
            "game_state": self.game_state.value,
            "current_level": self.current_level,
            "score": self.score,
            "lives": self.lives,
            "achievements": list(self.achievements),
            "total_play_time": self.total_play_time.total_seconds(),
            "saved_at": datetime.now().isoformat()
        }
        print(f"游戏已保存，存档ID: {save_id}")
        return save_id
    
    def load_game(self, save_id: str) -> bool:
        """加载游戏"""
        if save_id not in self.save_data:
            print(f"存档不存在: {save_id}")
            return False
        
        save_data = self.save_data[save_id]
        self.game_state = GameState(save_data["game_state"])
        self.current_level = save_data["current_level"]
        self.score = save_data["score"]
        self.lives = save_data["lives"]
        self.achievements = set(save_data["achievements"])
        self.total_play_time = timedelta(seconds=save_data["total_play_time"])
        
        print(f"游戏已加载，存档ID: {save_id}")
        return True
    
    def add_event_listener(self, event_type: str, callback: Callable):
        """添加事件监听器"""
        self.event_listeners[event_type].append(callback)
    
    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """发布事件"""
        for callback in self.event_listeners[event_type]:
            try:
                callback(data)
            except Exception as e:
                print(f"事件处理器执行失败: {e}")
    
    def get_game_stats(self) -> Dict[str, Any]:
        """获取游戏统计"""
        return {
            "current_state": self.game_state.value,
            "current_level": self.current_level,
            "score": self.score,
            "lives": self.lives,
            "achievements_count": len(self.achievements),
            "total_play_time": str(self.total_play_time),
            "saves_count": len(self.save_data)
        }


# ==================== Web应用：会话管理器 ====================
class SessionManager:
    """会话管理器单例"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.sessions = {}
            self.session_timeout = timedelta(minutes=30)
            self.cleanup_interval = 300  # 5分钟清理一次
            self.last_cleanup = datetime.now()
            self.session_stats = {
                "total_created": 0,
                "total_expired": 0,
                "current_active": 0
            }
            self.initialized = True
            print("会话管理器已初始化")
    
    def create_session(self, user_id: str, user_data: Dict[str, Any] = None) -> str:
        """创建会话"""
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "user_data": user_data or {},
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "ip_address": "127.0.0.1",  # 实际应用中从请求获取
            "user_agent": "Mozilla/5.0...",  # 实际应用中从请求获取
            "is_authenticated": True,
            "permissions": [],
            "custom_data": {}
        }
        
        self.sessions[session_id] = session_data
        self.session_stats["total_created"] += 1
        self.session_stats["current_active"] += 1
        
        print(f"会话已创建: {session_id} (用户: {user_id})")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话"""
        self._cleanup_expired_sessions()
        
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # 检查会话是否过期
        if self._is_session_expired(session):
            self.destroy_session(session_id)
            return None
        
        # 更新最后访问时间
        session["last_accessed"] = datetime.now()
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]):
        """更新会话数据"""
        session = self.get_session(session_id)
        if session:
            session["custom_data"].update(data)
            session["last_accessed"] = datetime.now()
            print(f"会话已更新: {session_id}")
    
    def destroy_session(self, session_id: str):
        """销毁会话"""
        if session_id in self.sessions:
            user_id = self.sessions[session_id]["user_id"]
            del self.sessions[session_id]
            self.session_stats["current_active"] -= 1
            print(f"会话已销毁: {session_id} (用户: {user_id})")
    
    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """检查会话是否过期"""
        return datetime.now() - session["last_accessed"] > self.session_timeout
    
    def _cleanup_expired_sessions(self):
        """清理过期会话"""
        now = datetime.now()
        if now - self.last_cleanup < timedelta(seconds=self.cleanup_interval):
            return
        
        expired_sessions = []
        for session_id, session in self.sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)
            self.session_stats["total_expired"] += 1
        
        self.last_cleanup = now
        if expired_sessions:
            print(f"清理了 {len(expired_sessions)} 个过期会话")
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的所有会话"""
        self._cleanup_expired_sessions()
        return [
            session for session in self.sessions.values()
            if session["user_id"] == user_id
        ]
    
    def destroy_user_sessions(self, user_id: str):
        """销毁用户的所有会话"""
        user_sessions = self.get_user_sessions(user_id)
        for session in user_sessions:
            self.destroy_session(session["session_id"])
        print(f"已销毁用户 {user_id} 的所有会话")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计"""
        self._cleanup_expired_sessions()
        return {
            **self.session_stats,
            "current_active": len(self.sessions)
        }
    
    def set_session_timeout(self, minutes: int):
        """设置会话超时时间"""
        self.session_timeout = timedelta(minutes=minutes)
        print(f"会话超时时间已设置为 {minutes} 分钟")


# ==================== 企业应用：审计日志管理器 ====================
class AuditLogManager:
    """审计日志管理器单例"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.logs = deque(maxlen=10000)  # 保留最近10000条日志
            self.log_file = "audit.log"
            self.auto_save = True
            self.save_interval = 60  # 每60秒保存一次
            self.last_save = datetime.now()
            self.log_stats = {
                "total_logs": 0,
                "logs_by_action": defaultdict(int),
                "logs_by_user": defaultdict(int),
                "logs_by_level": defaultdict(int)
            }
            self.initialized = True
            print("审计日志管理器已初始化")
    
    def log_action(self, user_id: str, action: str, resource: str, 
                   details: Dict[str, Any] = None, level: str = "INFO"):
        """记录用户操作"""
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
            "level": level,
            "ip_address": "127.0.0.1",  # 实际应用中从请求获取
            "user_agent": "Mozilla/5.0..."  # 实际应用中从请求获取
        }
        
        self.logs.append(log_entry)
        
        # 更新统计
        self.log_stats["total_logs"] += 1
        self.log_stats["logs_by_action"][action] += 1
        self.log_stats["logs_by_user"][user_id] += 1
        self.log_stats["logs_by_level"][level] += 1
        
        print(f"审计日志: {user_id} {action} {resource}")
        
        # 自动保存
        if self.auto_save:
            self._auto_save()
    
    def log_login(self, user_id: str, success: bool, ip_address: str = "127.0.0.1"):
        """记录登录操作"""
        action = "LOGIN_SUCCESS" if success else "LOGIN_FAILED"
        level = "INFO" if success else "WARNING"
        details = {"ip_address": ip_address, "success": success}
        
        self.log_action(user_id, action, "authentication", details, level)
    
    def log_data_access(self, user_id: str, table: str, operation: str, record_id: str = None):
        """记录数据访问"""
        details = {"table": table, "operation": operation}
        if record_id:
            details["record_id"] = record_id
        
        self.log_action(user_id, f"DATA_{operation.upper()}", f"database.{table}", details)
    
    def log_security_event(self, user_id: str, event_type: str, details: Dict[str, Any]):
        """记录安全事件"""
        self.log_action(user_id, f"SECURITY_{event_type}", "security", details, "WARNING")
    
    def search_logs(self, user_id: str = None, action: str = None, 
                   start_time: datetime = None, end_time: datetime = None,
                   limit: int = 100) -> List[Dict[str, Any]]:
        """搜索日志"""
        results = []
        
        for log in self.logs:
            # 用户过滤
            if user_id and log["user_id"] != user_id:
                continue
            
            # 操作过滤
            if action and log["action"] != action:
                continue
            
            # 时间过滤
            if start_time and log["timestamp"] < start_time:
                continue
            if end_time and log["timestamp"] > end_time:
                continue
            
            results.append(log)
            
            if len(results) >= limit:
                break
        
        return results
    
    def get_user_activity(self, user_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """获取用户活动记录"""
        start_time = datetime.now() - timedelta(days=days)
        return self.search_logs(user_id=user_id, start_time=start_time)
    
    def get_security_events(self, hours: int = 24) -> List[Dict[str, Any]]:
        """获取安全事件"""
        start_time = datetime.now() - timedelta(hours=hours)
        return [
            log for log in self.logs
            if log["action"].startswith("SECURITY_") and log["timestamp"] >= start_time
        ]
    
    def _auto_save(self):
        """自动保存到文件"""
        now = datetime.now()
        if now - self.last_save >= timedelta(seconds=self.save_interval):
            self.save_to_file()
            self.last_save = now
    
    def save_to_file(self):
        """保存日志到文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                for log in self.logs:
                    log_line = json.dumps({
                        **log,
                        "timestamp": log["timestamp"].isoformat()
                    }, ensure_ascii=False)
                    f.write(log_line + '\n')
            print(f"审计日志已保存到 {self.log_file}")
        except Exception as e:
            print(f"保存审计日志失败: {e}")
    
    def get_audit_stats(self) -> Dict[str, Any]:
        """获取审计统计"""
        return {
            "total_logs": len(self.logs),
            "logs_by_action": dict(self.log_stats["logs_by_action"]),
            "logs_by_user": dict(self.log_stats["logs_by_user"]),
            "logs_by_level": dict(self.log_stats["logs_by_level"]),
            "oldest_log": self.logs[0]["timestamp"].isoformat() if self.logs else None,
            "newest_log": self.logs[-1]["timestamp"].isoformat() if self.logs else None
        }


# ==================== 演示函数 ====================
def demonstrate_game_manager():
    """演示游戏管理器"""
    print("=" * 60)
    print("游戏管理器单例演示")
    print("=" * 60)
    
    # 获取游戏管理器实例
    game1 = GameManager()
    game2 = GameManager()
    
    print(f"game1 和 game2 是同一个对象: {game1 is game2}")
    
    # 添加事件监听器
    def on_score_changed(data):
        print(f"分数变化事件: +{data['points_added']} 分，总分: {data['score']}")
    
    def on_achievement_unlocked(data):
        print(f"成就解锁事件: {data['name']}")
    
    game1.add_event_listener("score_changed", on_score_changed)
    game1.add_event_listener("achievement_unlocked", on_achievement_unlocked)
    
    # 开始游戏
    game1.start_new_game()
    
    # 模拟游戏过程
    game1.add_score(500)
    game1.add_score(600)  # 这会触发成就
    game1.next_level()
    game1.add_score(10000)  # 这会触发另一个成就
    
    # 保存游戏
    save_id = game1.save_game()
    
    # 获取游戏统计
    stats = game1.get_game_stats()
    print(f"游戏统计: {stats}")


def demonstrate_session_manager():
    """演示会话管理器"""
    print("\n" + "=" * 60)
    print("会话管理器单例演示")
    print("=" * 60)
    
    # 获取会话管理器实例
    session_mgr1 = SessionManager()
    session_mgr2 = SessionManager()
    
    print(f"session_mgr1 和 session_mgr2 是同一个对象: {session_mgr1 is session_mgr2}")
    
    # 创建会话
    session1 = session_mgr1.create_session("user001", {"name": "张三", "role": "admin"})
    session2 = session_mgr1.create_session("user002", {"name": "李四", "role": "user"})
    
    # 获取会话
    user_session = session_mgr2.get_session(session1)
    print(f"获取会话: {user_session['user_id']} - {user_session['user_data']['name']}")
    
    # 更新会话
    session_mgr1.update_session(session1, {"last_page": "/dashboard", "theme": "dark"})
    
    # 获取用户的所有会话
    user_sessions = session_mgr1.get_user_sessions("user001")
    print(f"用户 user001 的会话数量: {len(user_sessions)}")
    
    # 获取会话统计
    stats = session_mgr1.get_session_stats()
    print(f"会话统计: {stats}")


def demonstrate_audit_log_manager():
    """演示审计日志管理器"""
    print("\n" + "=" * 60)
    print("审计日志管理器单例演示")
    print("=" * 60)
    
    # 获取审计日志管理器实例
    audit1 = AuditLogManager()
    audit2 = AuditLogManager()
    
    print(f"audit1 和 audit2 是同一个对象: {audit1 is audit2}")
    
    # 记录各种操作
    audit1.log_login("user001", True, "192.168.1.100")
    audit1.log_data_access("user001", "users", "SELECT")
    audit1.log_data_access("user001", "orders", "INSERT", "order_12345")
    audit1.log_security_event("user002", "SUSPICIOUS_LOGIN", {
        "reason": "多次失败登录",
        "attempts": 5
    })
    
    # 搜索日志
    user_logs = audit1.search_logs(user_id="user001", limit=10)
    print(f"用户 user001 的操作记录数量: {len(user_logs)}")
    
    # 获取安全事件
    security_events = audit1.get_security_events(24)
    print(f"24小时内的安全事件数量: {len(security_events)}")
    
    # 获取审计统计
    stats = audit1.get_audit_stats()
    print(f"审计统计: {stats}")


def main():
    """主函数"""
    print("单例模式实际应用示例")
    
    demonstrate_game_manager()
    demonstrate_session_manager()
    demonstrate_audit_log_manager()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
