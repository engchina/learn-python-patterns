#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏存档系统实现

本模块演示了备忘录模式在游戏存档系统中的应用，包括：
1. 游戏状态的完整保存
2. 多个存档槽管理
3. 自动保存机制
4. 存档的持久化存储

作者: Assistant
日期: 2024-01-20
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import os
import pickle
import threading
import time


class GameDifficulty(Enum):
    """游戏难度"""
    EASY = "简单"
    NORMAL = "普通"
    HARD = "困难"
    EXPERT = "专家"


class PlayerClass(Enum):
    """玩家职业"""
    WARRIOR = "战士"
    MAGE = "法师"
    ARCHER = "弓箭手"
    ROGUE = "盗贼"


@dataclass
class PlayerStats:
    """玩家属性"""
    level: int = 1
    experience: int = 0
    health: int = 100
    mana: int = 50
    strength: int = 10
    intelligence: int = 10
    agility: int = 10
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'level': self.level,
            'experience': self.experience,
            'health': self.health,
            'mana': self.mana,
            'strength': self.strength,
            'intelligence': self.intelligence,
            'agility': self.agility
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerStats':
        return cls(**data)


@dataclass
class Item:
    """物品"""
    id: str
    name: str
    type: str
    quantity: int = 1
    value: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'quantity': self.quantity,
            'value': self.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        return cls(**data)


@dataclass
class Quest:
    """任务"""
    id: str
    title: str
    description: str
    completed: bool = False
    progress: int = 0
    max_progress: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'progress': self.progress,
            'max_progress': self.max_progress
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quest':
        return cls(**data)


class GameSaveMemento:
    """游戏存档备忘录"""
    
    def __init__(self, game_state: Dict[str, Any], save_name: str, auto_save: bool = False):
        self._state = game_state.copy()
        self._save_name = save_name
        self._timestamp = datetime.now()
        self._auto_save = auto_save
        self._version = "1.0"
        self._checksum = self._calculate_checksum()
    
    def get_state(self) -> Dict[str, Any]:
        """获取游戏状态"""
        return self._state.copy()
    
    def get_save_name(self) -> str:
        """获取存档名称"""
        return self._save_name
    
    def get_timestamp(self) -> datetime:
        """获取保存时间"""
        return self._timestamp
    
    def is_auto_save(self) -> bool:
        """是否为自动存档"""
        return self._auto_save
    
    def get_version(self) -> str:
        """获取版本"""
        return self._version
    
    def get_checksum(self) -> str:
        """获取校验和"""
        return self._checksum
    
    def _calculate_checksum(self) -> str:
        """计算校验和"""
        # 简单的校验和计算
        state_str = json.dumps(self._state, sort_keys=True, default=str)
        return str(hash(state_str))
    
    def verify_integrity(self) -> bool:
        """验证数据完整性"""
        return self._checksum == self._calculate_checksum()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'state': self._state,
            'save_name': self._save_name,
            'timestamp': self._timestamp.isoformat(),
            'auto_save': self._auto_save,
            'version': self._version,
            'checksum': self._checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameSaveMemento':
        """从字典创建"""
        memento = cls(
            game_state=data['state'],
            save_name=data['save_name'],
            auto_save=data['auto_save']
        )
        memento._timestamp = datetime.fromisoformat(data['timestamp'])
        memento._version = data['version']
        memento._checksum = data['checksum']
        return memento
    
    def __str__(self) -> str:
        save_type = "自动" if self._auto_save else "手动"
        return f"{save_type}存档: {self._save_name} [{self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"


class GameState:
    """游戏状态 - 发起人"""
    
    def __init__(self, player_name: str, player_class: PlayerClass):
        self.player_name = player_name
        self.player_class = player_class
        self.stats = PlayerStats()
        self.inventory: List[Item] = []
        self.quests: List[Quest] = []
        self.current_location = "新手村"
        self.game_time = 0.0  # 游戏时间（小时）
        self.difficulty = GameDifficulty.NORMAL
        self.achievements: List[str] = []
        self.settings = {
            'music_volume': 0.8,
            'sound_volume': 0.9,
            'graphics_quality': 'high'
        }
        self.created_at = datetime.now()
        self.last_played = datetime.now()
    
    def level_up(self) -> None:
        """升级"""
        self.stats.level += 1
        self.stats.health += 20
        self.stats.mana += 10
        self.stats.strength += 2
        self.stats.intelligence += 2
        self.stats.agility += 2
        
        print(f"🎉 {self.player_name} 升级到 {self.stats.level} 级！")
        
        if self.stats.level % 5 == 0:
            self.achievements.append(f"达到{self.stats.level}级")
    
    def gain_experience(self, exp: int) -> None:
        """获得经验"""
        self.stats.experience += exp
        print(f"✨ 获得 {exp} 经验值")
        
        # 检查是否可以升级
        exp_needed = self.stats.level * 100
        while self.stats.experience >= exp_needed:
            self.stats.experience -= exp_needed
            self.level_up()
            exp_needed = self.stats.level * 100
    
    def add_item(self, item: Item) -> None:
        """添加物品"""
        # 检查是否已有相同物品
        for existing_item in self.inventory:
            if existing_item.id == item.id:
                existing_item.quantity += item.quantity
                print(f"📦 获得 {item.name} x{item.quantity}")
                return
        
        self.inventory.append(item)
        print(f"📦 获得新物品: {item.name} x{item.quantity}")
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """移除物品"""
        for item in self.inventory:
            if item.id == item_id:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    print(f"📤 使用 {item.name} x{quantity}")
                    
                    if item.quantity == 0:
                        self.inventory.remove(item)
                    return True
        return False
    
    def start_quest(self, quest: Quest) -> None:
        """开始任务"""
        self.quests.append(quest)
        print(f"📋 接受任务: {quest.title}")
    
    def complete_quest(self, quest_id: str) -> bool:
        """完成任务"""
        for quest in self.quests:
            if quest.id == quest_id and not quest.completed:
                quest.completed = True
                quest.progress = quest.max_progress
                print(f"✅ 完成任务: {quest.title}")
                
                # 奖励经验
                self.gain_experience(quest.max_progress * 50)
                return True
        return False
    
    def travel_to(self, location: str) -> None:
        """前往地点"""
        old_location = self.current_location
        self.current_location = location
        self.game_time += 0.5  # 旅行消耗时间
        print(f"🗺️ 从 {old_location} 前往 {location}")
    
    def play_time(self, hours: float) -> None:
        """游戏时间流逝"""
        self.game_time += hours
        self.last_played = datetime.now()
    
    def create_save_memento(self, save_name: str, auto_save: bool = False) -> GameSaveMemento:
        """创建存档备忘录"""
        state = {
            'player_name': self.player_name,
            'player_class': self.player_class.value,
            'stats': self.stats.to_dict(),
            'inventory': [item.to_dict() for item in self.inventory],
            'quests': [quest.to_dict() for quest in self.quests],
            'current_location': self.current_location,
            'game_time': self.game_time,
            'difficulty': self.difficulty.value,
            'achievements': self.achievements.copy(),
            'settings': self.settings.copy(),
            'created_at': self.created_at.isoformat(),
            'last_played': self.last_played.isoformat()
        }
        
        memento = GameSaveMemento(state, save_name, auto_save)
        save_type = "自动" if auto_save else "手动"
        print(f"💾 创建{save_type}存档: {save_name}")
        return memento
    
    def load_from_memento(self, memento: GameSaveMemento) -> bool:
        """从存档加载"""
        if not memento.verify_integrity():
            print("❌ 存档数据损坏，无法加载")
            return False
        
        try:
            state = memento.get_state()
            
            self.player_name = state['player_name']
            self.player_class = PlayerClass(state['player_class'])
            self.stats = PlayerStats.from_dict(state['stats'])
            self.inventory = [Item.from_dict(item) for item in state['inventory']]
            self.quests = [Quest.from_dict(quest) for quest in state['quests']]
            self.current_location = state['current_location']
            self.game_time = state['game_time']
            self.difficulty = GameDifficulty(state['difficulty'])
            self.achievements = state['achievements'].copy()
            self.settings = state['settings'].copy()
            self.created_at = datetime.fromisoformat(state['created_at'])
            self.last_played = datetime.fromisoformat(state['last_played'])
            
            print(f"🔄 加载存档: {memento.get_save_name()}")
            return True
            
        except Exception as e:
            print(f"❌ 加载存档失败: {e}")
            return False
    
    def get_summary(self) -> str:
        """获取游戏状态摘要"""
        return (f"{self.player_name} ({self.player_class.value}) "
                f"Lv.{self.stats.level} - {self.current_location} "
                f"[{self.game_time:.1f}h]")


class SaveManager:
    """存档管理器 - 管理者"""
    
    def __init__(self, save_directory: str = "saves", max_saves: int = 10):
        self.save_directory = save_directory
        self.max_saves = max_saves
        self.saves: Dict[str, GameSaveMemento] = {}
        self.auto_save_enabled = True
        self.auto_save_interval = 300  # 5分钟
        self.last_auto_save = datetime.now()
        
        # 创建存档目录
        os.makedirs(save_directory, exist_ok=True)
        
        # 加载现有存档
        self._load_existing_saves()
    
    def _load_existing_saves(self) -> None:
        """加载现有存档"""
        try:
            for filename in os.listdir(self.save_directory):
                if filename.endswith('.save'):
                    filepath = os.path.join(self.save_directory, filename)
                    try:
                        with open(filepath, 'rb') as f:
                            data = pickle.load(f)
                            memento = GameSaveMemento.from_dict(data)
                            self.saves[memento.get_save_name()] = memento
                    except Exception as e:
                        print(f"⚠️ 无法加载存档 {filename}: {e}")
        except FileNotFoundError:
            pass
    
    def save_game(self, memento: GameSaveMemento) -> bool:
        """保存游戏"""
        try:
            # 添加到内存中的存档列表
            self.saves[memento.get_save_name()] = memento
            
            # 保存到文件
            filename = f"{memento.get_save_name()}.save"
            filepath = os.path.join(self.save_directory, filename)
            
            with open(filepath, 'wb') as f:
                pickle.dump(memento.to_dict(), f)
            
            print(f"💾 存档已保存: {filepath}")
            
            # 管理存档数量
            self._manage_save_count()
            
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def load_game(self, save_name: str) -> Optional[GameSaveMemento]:
        """加载游戏"""
        if save_name in self.saves:
            memento = self.saves[save_name]
            if memento.verify_integrity():
                print(f"📂 加载存档: {save_name}")
                return memento
            else:
                print(f"❌ 存档损坏: {save_name}")
                return None
        else:
            print(f"❌ 存档不存在: {save_name}")
            return None
    
    def delete_save(self, save_name: str) -> bool:
        """删除存档"""
        if save_name in self.saves:
            # 从内存中删除
            del self.saves[save_name]
            
            # 从文件系统删除
            filename = f"{save_name}.save"
            filepath = os.path.join(self.save_directory, filename)
            
            try:
                os.remove(filepath)
                print(f"🗑️ 删除存档: {save_name}")
                return True
            except FileNotFoundError:
                print(f"⚠️ 存档文件不存在: {filepath}")
                return True
            except Exception as e:
                print(f"❌ 删除存档失败: {e}")
                return False
        else:
            print(f"❌ 存档不存在: {save_name}")
            return False
    
    def _manage_save_count(self) -> None:
        """管理存档数量"""
        if len(self.saves) > self.max_saves:
            # 删除最旧的非自动存档
            manual_saves = [(name, memento) for name, memento in self.saves.items() 
                           if not memento.is_auto_save()]
            
            if manual_saves:
                # 按时间排序，删除最旧的
                manual_saves.sort(key=lambda x: x[1].get_timestamp())
                oldest_save = manual_saves[0][0]
                self.delete_save(oldest_save)
    
    def auto_save(self, game_state: GameState) -> bool:
        """自动保存"""
        if not self.auto_save_enabled:
            return False
        
        now = datetime.now()
        if (now - self.last_auto_save).total_seconds() >= self.auto_save_interval:
            auto_save_name = f"auto_save_{now.strftime('%Y%m%d_%H%M%S')}"
            memento = game_state.create_save_memento(auto_save_name, auto_save=True)
            
            success = self.save_game(memento)
            if success:
                self.last_auto_save = now
                
                # 清理旧的自动存档
                self._cleanup_auto_saves()
            
            return success
        
        return False
    
    def _cleanup_auto_saves(self) -> None:
        """清理旧的自动存档"""
        auto_saves = [(name, memento) for name, memento in self.saves.items() 
                     if memento.is_auto_save()]
        
        # 只保留最新的3个自动存档
        if len(auto_saves) > 3:
            auto_saves.sort(key=lambda x: x[1].get_timestamp())
            for name, _ in auto_saves[:-3]:
                self.delete_save(name)
    
    def get_save_list(self) -> List[Dict[str, Any]]:
        """获取存档列表"""
        save_list = []
        for name, memento in self.saves.items():
            save_info = {
                'name': name,
                'timestamp': memento.get_timestamp(),
                'auto_save': memento.is_auto_save(),
                'version': memento.get_version(),
                'player_info': self._extract_player_info(memento)
            }
            save_list.append(save_info)
        
        # 按时间排序
        save_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return save_list
    
    def _extract_player_info(self, memento: GameSaveMemento) -> str:
        """提取玩家信息"""
        try:
            state = memento.get_state()
            return (f"{state['player_name']} ({state['player_class']}) "
                   f"Lv.{state['stats']['level']} - {state['current_location']}")
        except:
            return "未知"


def demo_game_save_system():
    """演示游戏存档系统"""
    print("=" * 50)
    print("🎮 游戏存档系统演示")
    print("=" * 50)
    
    # 创建游戏状态和存档管理器
    game = GameState("勇者小明", PlayerClass.WARRIOR)
    save_manager = SaveManager(save_directory="demo_saves", max_saves=5)
    
    print(f"\n🎯 开始游戏: {game.get_summary()}")
    
    # 游戏进程模拟
    print("\n📖 游戏进程:")
    
    # 添加初始物品
    game.add_item(Item("sword_001", "新手剑", "武器", 1, 100))
    game.add_item(Item("potion_001", "生命药水", "消耗品", 5, 50))
    
    # 开始任务
    quest1 = Quest("quest_001", "击败史莱姆", "击败10只史莱姆", False, 0, 10)
    game.start_quest(quest1)
    
    # 手动保存
    save1 = game.create_save_memento("新手村开始")
    save_manager.save_game(save1)
    
    # 游戏进展
    game.gain_experience(150)
    game.travel_to("森林")
    game.play_time(1.0)
    
    # 完成任务
    game.complete_quest("quest_001")
    game.add_item(Item("gold", "金币", "货币", 100, 1))
    
    # 自动保存
    save_manager.auto_save(game)
    
    # 继续游戏
    game.gain_experience(200)
    game.travel_to("城镇")
    game.add_item(Item("armor_001", "皮甲", "防具", 1, 200))
    
    # 手动保存
    save2 = game.create_save_memento("到达城镇")
    save_manager.save_game(save2)
    
    print(f"\n📊 当前状态: {game.get_summary()}")
    
    # 显示存档列表
    print("\n💾 存档列表:")
    for save_info in save_manager.get_save_list():
        save_type = "自动" if save_info['auto_save'] else "手动"
        timestamp = save_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {save_type}: {save_info['name']} - {save_info['player_info']} [{timestamp}]")
    
    # 演示加载存档
    print("\n🔄 加载之前的存档:")
    memento = save_manager.load_game("新手村开始")
    if memento:
        game.load_from_memento(memento)
        print(f"📊 加载后状态: {game.get_summary()}")
    
    # 再次加载最新存档
    print("\n🔄 加载最新存档:")
    memento = save_manager.load_game("到达城镇")
    if memento:
        game.load_from_memento(memento)
        print(f"📊 最终状态: {game.get_summary()}")


if __name__ == "__main__":
    print("🎯 游戏存档系统备忘录模式演示")
    
    demo_game_save_system()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 游戏存档系统展示了备忘录模式在复杂状态管理中的应用")
    print("=" * 50)
