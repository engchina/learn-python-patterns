"""
03_game_level.py - 游戏关卡系统的模板方法实现

这个示例展示了在游戏开发中如何使用模板方法模式：
- 统一的关卡流程框架
- 不同类型关卡的具体实现
- 钩子方法提供的灵活性
- 游戏状态的管理
"""

from abc import ABC, abstractmethod
import random
import time
from typing import List, Dict, Any
from enum import Enum


class GameResult(Enum):
    """游戏结果枚举"""
    VICTORY = "胜利"
    DEFEAT = "失败"
    TIMEOUT = "超时"


# ==================== 抽象游戏关卡 ====================
class GameLevel(ABC):
    """游戏关卡模板类
    
    定义了游戏关卡的标准流程：
    1. 初始化关卡
    2. 显示关卡信息
    3. 生成敌人/挑战
    4. 游戏主循环
    5. 结算奖励
    6. 清理资源
    """
    
    def __init__(self, level_id: int):
        self.level_id = level_id
        self.player_health = 100
        self.player_score = 0
        self.start_time = None
        self.enemies = []
        self.game_result = None
    
    def play_level(self) -> Dict[str, Any]:
        """模板方法 - 定义完整的关卡游戏流程"""
        print(f"🎮 开始关卡: {self.get_level_name()}")
        print("=" * 60)
        
        self.start_time = time.time()
        
        try:
            # 1. 初始化关卡
            print("🔧 步骤1: 初始化关卡")
            self.initialize_level()
            print("✅ 关卡初始化完成")
            
            # 2. 显示关卡信息
            print("\n📋 步骤2: 显示关卡信息")
            self.show_level_info()
            
            # 3. 生成敌人/挑战
            print("\n👹 步骤3: 生成挑战")
            self.enemies = self.spawn_enemies()
            print(f"✅ 生成了 {len(self.enemies)} 个敌人")
            
            # 4. 游戏主循环
            print("\n⚔️  步骤4: 开始战斗")
            self.game_result = self.run_game_loop()
            
            # 5. 结算奖励
            print("\n🏆 步骤5: 结算奖励")
            rewards = self.calculate_rewards()
            
            # 6. 清理资源
            print("\n🧹 步骤6: 清理资源")
            self.cleanup_level()
            
            # 生成关卡报告
            report = self.generate_level_report(rewards)
            
            print("=" * 60)
            print(f"🎯 关卡 {self.get_level_name()} 完成!")
            return report
            
        except Exception as e:
            print(f"❌ 关卡执行失败: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    # 抽象方法 - 子类必须实现
    @abstractmethod
    def get_level_name(self) -> str:
        """获取关卡名称"""
        pass
    
    @abstractmethod
    def spawn_enemies(self) -> List[Dict[str, Any]]:
        """生成敌人"""
        pass
    
    # 具体方法 - 提供默认实现
    def initialize_level(self):
        """初始化关卡 - 默认实现"""
        print("设置关卡环境...")
        print("加载关卡资源...")
        self.player_health = 100
        self.player_score = 0
    
    def show_level_info(self):
        """显示关卡信息 - 默认实现"""
        print(f"关卡名称: {self.get_level_name()}")
        print(f"关卡ID: {self.level_id}")
        print(f"玩家生命值: {self.player_health}")
        print("准备开始挑战...")
    
    def run_game_loop(self) -> GameResult:
        """游戏主循环 - 默认实现"""
        round_count = 0
        max_rounds = self.get_max_rounds()
        
        while self.enemies and self.player_health > 0 and round_count < max_rounds:
            round_count += 1
            print(f"\n--- 第 {round_count} 回合 ---")
            
            # 玩家回合
            if self.should_player_attack():
                self.player_turn()
            
            # 敌人回合
            if self.enemies and self.player_health > 0:
                self.enemy_turn()
            
            # 显示状态
            self.show_battle_status()
            
            # 检查特殊事件
            if self.check_special_events():
                break
            
            time.sleep(0.5)  # 模拟游戏节奏
        
        # 判断游戏结果
        if not self.enemies:
            return GameResult.VICTORY
        elif self.player_health <= 0:
            return GameResult.DEFEAT
        else:
            return GameResult.TIMEOUT
    
    def player_turn(self):
        """玩家回合"""
        if not self.enemies:
            return
            
        damage = self.calculate_player_damage()
        target = self.enemies[0]
        target['health'] -= damage
        
        print(f"🗡️  玩家攻击 {target['name']}，造成 {damage} 点伤害")
        
        if target['health'] <= 0:
            print(f"💀 {target['name']} 被击败！")
            score = target.get('score_value', 10)
            self.player_score += score
            print(f"📈 获得 {score} 分")
            self.enemies.pop(0)
    
    def enemy_turn(self):
        """敌人回合"""
        total_damage = 0
        for enemy in self.enemies:
            if enemy['health'] > 0:
                damage = self.calculate_enemy_damage(enemy)
                total_damage += damage
                print(f"👹 {enemy['name']} 攻击玩家，造成 {damage} 点伤害")
        
        self.player_health -= total_damage
        if self.player_health < 0:
            self.player_health = 0
    
    def show_battle_status(self):
        """显示战斗状态"""
        print(f"❤️  玩家生命值: {self.player_health}")
        print(f"⭐ 当前分数: {self.player_score}")
        alive_enemies = [e for e in self.enemies if e['health'] > 0]
        if alive_enemies:
            print(f"👹 剩余敌人: {len(alive_enemies)}")
    
    def calculate_rewards(self) -> Dict[str, Any]:
        """计算奖励 - 默认实现"""
        base_reward = {"experience": 100, "gold": 50}
        
        if self.game_result == GameResult.VICTORY:
            multiplier = 1.5
            base_reward["bonus"] = "胜利奖励"
        elif self.game_result == GameResult.DEFEAT:
            multiplier = 0.5
            base_reward["bonus"] = "参与奖励"
        else:
            multiplier = 0.8
            base_reward["bonus"] = "时间奖励"
        
        # 根据分数调整奖励
        score_bonus = self.player_score // 10
        base_reward["experience"] = int(base_reward["experience"] * multiplier) + score_bonus
        base_reward["gold"] = int(base_reward["gold"] * multiplier) + score_bonus
        
        return base_reward
    
    def cleanup_level(self):
        """清理关卡资源 - 默认实现"""
        print("清理战斗场地...")
        print("保存游戏进度...")
    
    def generate_level_report(self, rewards: Dict[str, Any]) -> Dict[str, Any]:
        """生成关卡报告"""
        end_time = time.time()
        duration = round(end_time - self.start_time, 2)
        
        report = {
            "level_name": self.get_level_name(),
            "level_id": self.level_id,
            "result": self.game_result.value,
            "final_health": self.player_health,
            "final_score": self.player_score,
            "duration_seconds": duration,
            "rewards": rewards,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"关卡结果: {report['result']}")
        print(f"最终生命值: {report['final_health']}")
        print(f"最终分数: {report['final_score']}")
        print(f"用时: {report['duration_seconds']} 秒")
        print(f"奖励: {report['rewards']}")
        
        return report
    
    # 钩子方法 - 子类可选择重写
    def should_player_attack(self) -> bool:
        """玩家是否攻击"""
        return True
    
    def get_max_rounds(self) -> int:
        """获取最大回合数"""
        return 20
    
    def calculate_player_damage(self) -> int:
        """计算玩家伤害"""
        return random.randint(15, 25)
    
    def calculate_enemy_damage(self, enemy: Dict[str, Any]) -> int:
        """计算敌人伤害"""
        base_damage = enemy.get('attack', 10)
        return random.randint(base_damage - 3, base_damage + 3)
    
    def check_special_events(self) -> bool:
        """检查特殊事件"""
        return False


# ==================== 具体游戏关卡 ====================
class ForestLevel(GameLevel):
    """森林关卡 - 新手关卡"""
    
    def get_level_name(self) -> str:
        return "🌲 神秘森林"
    
    def initialize_level(self):
        """森林关卡初始化"""
        super().initialize_level()
        print("🌿 森林中弥漫着神秘的魔法气息...")
        print("🦋 小动物们在树林中穿梭...")
    
    def spawn_enemies(self) -> List[Dict[str, Any]]:
        """生成森林敌人"""
        return [
            {"name": "野狼", "health": 30, "attack": 8, "score_value": 15},
            {"name": "树精", "health": 40, "attack": 6, "score_value": 20}
        ]
    
    def show_level_info(self):
        """显示森林关卡信息"""
        super().show_level_info()
        print("🌲 你进入了一片神秘的森林...")
        print("⚠️  小心森林中的野生动物!")
    
    def calculate_player_damage(self) -> int:
        """森林中玩家攻击力稍低"""
        return random.randint(12, 20)
    
    def check_special_events(self) -> bool:
        """森林特殊事件：有概率获得治疗"""
        if random.random() < 0.1:  # 10%概率
            heal_amount = random.randint(5, 15)
            self.player_health = min(100, self.player_health + heal_amount)
            print(f"🍃 发现治疗草药，恢复 {heal_amount} 点生命值")
            return False
        return False


class DungeonLevel(GameLevel):
    """地牢关卡 - 中级关卡"""
    
    def get_level_name(self) -> str:
        return "🏰 黑暗地牢"
    
    def initialize_level(self):
        """地牢关卡初始化"""
        super().initialize_level()
        print("🕯️  点燃火把，照亮黑暗的地牢...")
        print("💀 空气中弥漫着死亡的气息...")
    
    def spawn_enemies(self) -> List[Dict[str, Any]]:
        """生成地牢敌人"""
        return [
            {"name": "骷髅战士", "health": 50, "attack": 12, "score_value": 25},
            {"name": "暗影法师", "health": 35, "attack": 15, "score_value": 30},
            {"name": "地牢守卫", "health": 60, "attack": 10, "score_value": 35}
        ]
    
    def show_level_info(self):
        """显示地牢关卡信息"""
        super().show_level_info()
        print("🏰 你踏入了阴森恐怖的地牢...")
        print("⚠️  这里到处都是危险!")
    
    def calculate_enemy_damage(self, enemy: Dict[str, Any]) -> int:
        """地牢敌人攻击力更强"""
        base_damage = enemy.get('attack', 10)
        return random.randint(base_damage - 2, base_damage + 5)
    
    def calculate_rewards(self) -> Dict[str, Any]:
        """地牢奖励更丰富"""
        rewards = super().calculate_rewards()
        rewards["rare_item"] = "神秘宝石"
        rewards["gold"] = int(rewards["gold"] * 1.3)
        return rewards


class BossLevel(GameLevel):
    """Boss关卡 - 高级关卡"""
    
    def get_level_name(self) -> str:
        return "👑 终极Boss战"
    
    def initialize_level(self):
        """Boss关卡初始化"""
        super().initialize_level()
        print("⚔️  准备最终决战...")
        print("🛡️  检查装备和道具...")
        print("💪 调整战斗状态...")
    
    def spawn_enemies(self) -> List[Dict[str, Any]]:
        """生成Boss"""
        return [
            {"name": "暗黑领主", "health": 120, "attack": 18, "score_value": 100}
        ]
    
    def show_level_info(self):
        """显示Boss关卡信息"""
        super().show_level_info()
        print("👑 你面对着最终的敌人——暗黑领主!")
        print("⚔️  这将是一场生死决战!")
        print("🔥 使用你的全部力量!")
    
    def should_player_attack(self) -> bool:
        """Boss战中玩家有策略选择"""
        return random.choice([True, True, True, False])  # 75%概率攻击
    
    def calculate_player_damage(self) -> int:
        """Boss战中玩家攻击力更强"""
        critical = random.random() < 0.25  # 25%暴击率
        base_damage = random.randint(20, 30)
        if critical:
            damage = int(base_damage * 1.8)
            print("💥 暴击!")
            return damage
        return base_damage
    
    def get_max_rounds(self) -> int:
        """Boss战回合数更多"""
        return 30
    
    def calculate_rewards(self) -> Dict[str, Any]:
        """Boss战奖励最丰富"""
        rewards = super().calculate_rewards()
        rewards["legendary_item"] = "传说级武器"
        rewards["experience"] = int(rewards["experience"] * 2)
        rewards["gold"] = int(rewards["gold"] * 2.5)
        rewards["achievement"] = "Boss杀手"
        return rewards
    
    def cleanup_level(self):
        """Boss战清理"""
        super().cleanup_level()
        print("🏆 解锁新内容...")
        print("📊 更新排行榜...")


# ==================== 演示函数 ====================
def demo_game_levels():
    """游戏关卡演示"""
    print("=" * 80)
    print("🎮 游戏关卡系统模板方法演示")
    print("=" * 80)
    
    # 创建不同类型的关卡
    levels = [
        ForestLevel(1),
        DungeonLevel(2),
        BossLevel(3)
    ]
    
    total_score = 0
    level_reports = []
    
    # 依次挑战关卡
    for level in levels:
        print(f"\n{'='*20} 关卡 {level.level_id} {'='*20}")
        report = level.play_level()
        level_reports.append(report)
        total_score += report.get('final_score', 0)
        time.sleep(1)
    
    # 游戏总结
    print("\n" + "="*80)
    print("🏆 游戏总结报告")
    print("="*80)
    
    victories = sum(1 for r in level_reports if r.get('result') == '胜利')
    total_time = sum(r.get('duration_seconds', 0) for r in level_reports)
    
    print(f"挑战关卡数: {len(levels)}")
    print(f"胜利关卡数: {victories}")
    print(f"总分数: {total_score}")
    print(f"总用时: {round(total_time, 2)} 秒")
    print(f"胜率: {round(victories / len(levels) * 100, 1)}%")
    
    # 显示各关卡详情
    print("\n📋 关卡详情:")
    for report in level_reports:
        print(f"  {report['level_name']}: {report['result']} - {report['final_score']}分")


if __name__ == "__main__":
    demo_game_levels()
