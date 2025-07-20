"""
03_game_particles.py - 游戏粒子系统享元

这个示例展示了享元模式在游戏粒子系统中的应用。
粒子的类型、纹理、动画等作为内在状态被共享，
而位置、速度、生命周期等作为外在状态由粒子实例维护。
"""

import random
import math
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from enum import Enum


class ParticleType(Enum):
    """粒子类型枚举"""
    FIRE = "火焰"
    SMOKE = "烟雾"
    SPARK = "火花"
    EXPLOSION = "爆炸"
    MAGIC = "魔法"


# ==================== 粒子享元接口 ====================
class ParticleFlyweight(ABC):
    """粒子享元抽象接口"""
    
    @abstractmethod
    def update(self, extrinsic_state: Dict) -> str:
        """更新粒子状态"""
        pass
    
    @abstractmethod
    def render(self, extrinsic_state: Dict) -> str:
        """渲染粒子"""
        pass
    
    @abstractmethod
    def get_type_info(self) -> str:
        """获取粒子类型信息"""
        pass


# ==================== 具体粒子享元 ====================
class Particle(ParticleFlyweight):
    """粒子享元实现"""
    
    def __init__(self, particle_type: ParticleType, texture: str, 
                 base_size: float, base_color: str, animation_frames: int):
        """
        初始化粒子享元
        
        Args:
            particle_type: 粒子类型（内在状态）
            texture: 纹理（内在状态）
            base_size: 基础大小（内在状态）
            base_color: 基础颜色（内在状态）
            animation_frames: 动画帧数（内在状态）
        """
        self._type = particle_type
        self._texture = texture
        self._base_size = base_size
        self._base_color = base_color
        self._animation_frames = animation_frames
        print(f"创建粒子享元: {particle_type.value} ({texture})")
    
    def update(self, extrinsic_state: Dict) -> str:
        """
        更新粒子状态
        
        Args:
            extrinsic_state: 外在状态字典
            
        Returns:
            更新结果描述
        """
        position = extrinsic_state.get('position', (0, 0))
        velocity = extrinsic_state.get('velocity', (0, 0))
        life_time = extrinsic_state.get('life_time', 1.0)
        age = extrinsic_state.get('age', 0.0)
        
        # 模拟物理更新
        new_x = position[0] + velocity[0]
        new_y = position[1] + velocity[1]
        new_age = age + 0.1
        
        # 更新外在状态
        extrinsic_state['position'] = (new_x, new_y)
        extrinsic_state['age'] = new_age
        
        # 根据粒子类型应用不同的物理效果
        if self._type == ParticleType.FIRE:
            # 火焰粒子向上飘动
            extrinsic_state['velocity'] = (velocity[0] * 0.98, velocity[1] - 0.1)
        elif self._type == ParticleType.SMOKE:
            # 烟雾粒子扩散
            extrinsic_state['velocity'] = (velocity[0] * 0.95, velocity[1] - 0.05)
        elif self._type == ParticleType.SPARK:
            # 火花粒子受重力影响
            extrinsic_state['velocity'] = (velocity[0] * 0.99, velocity[1] + 0.2)
        
        return f"{self._type.value}粒子更新: 位置({new_x:.1f},{new_y:.1f}) 年龄{new_age:.1f}"
    
    def render(self, extrinsic_state: Dict) -> str:
        """
        渲染粒子
        
        Args:
            extrinsic_state: 外在状态字典
            
        Returns:
            渲染结果描述
        """
        position = extrinsic_state.get('position', (0, 0))
        life_time = extrinsic_state.get('life_time', 1.0)
        age = extrinsic_state.get('age', 0.0)
        
        # 计算生命周期进度
        life_progress = min(age / life_time, 1.0) if life_time > 0 else 1.0
        
        # 根据生命周期调整大小和透明度
        current_size = self._base_size * (1.0 - life_progress * 0.5)
        alpha = 1.0 - life_progress
        
        # 计算当前动画帧
        current_frame = int(life_progress * self._animation_frames) % self._animation_frames
        
        return (f"渲染{self._type.value} "
                f"位置:({position[0]:.1f},{position[1]:.1f}) "
                f"大小:{current_size:.1f} 透明度:{alpha:.2f} "
                f"帧:{current_frame}/{self._animation_frames} "
                f"纹理:{self._texture}")
    
    def get_type_info(self) -> str:
        """获取粒子类型信息"""
        return f"{self._type.value}-{self._texture}-{self._base_size}-{self._base_color}"
    
    @property
    def particle_type(self) -> ParticleType:
        """获取粒子类型"""
        return self._type


# ==================== 粒子享元工厂 ====================
class ParticleFactory:
    """粒子享元工厂"""
    
    def __init__(self):
        self._particles: Dict[str, Particle] = {}
        self._creation_count = 0
        self._access_count = 0
        
        # 预定义粒子类型配置
        self._particle_configs = {
            ParticleType.FIRE: {
                "texture": "fire_texture.png",
                "base_size": 8.0,
                "base_color": "orange",
                "animation_frames": 16
            },
            ParticleType.SMOKE: {
                "texture": "smoke_texture.png",
                "base_size": 12.0,
                "base_color": "gray",
                "animation_frames": 8
            },
            ParticleType.SPARK: {
                "texture": "spark_texture.png",
                "base_size": 4.0,
                "base_color": "yellow",
                "animation_frames": 4
            },
            ParticleType.EXPLOSION: {
                "texture": "explosion_texture.png",
                "base_size": 20.0,
                "base_color": "red",
                "animation_frames": 24
            },
            ParticleType.MAGIC: {
                "texture": "magic_texture.png",
                "base_size": 10.0,
                "base_color": "purple",
                "animation_frames": 12
            }
        }
    
    def get_particle(self, particle_type: ParticleType, 
                    custom_config: Dict = None) -> Particle:
        """
        获取粒子享元
        
        Args:
            particle_type: 粒子类型
            custom_config: 自定义配置（可选）
            
        Returns:
            粒子享元对象
        """
        # 使用默认配置或自定义配置
        config = custom_config or self._particle_configs.get(particle_type, {})
        
        key = f"{particle_type.value}-{config.get('texture', 'default')}"
        self._access_count += 1
        
        if key not in self._particles:
            self._particles[key] = Particle(
                particle_type,
                config.get('texture', 'default.png'),
                config.get('base_size', 5.0),
                config.get('base_color', 'white'),
                config.get('animation_frames', 8)
            )
            self._creation_count += 1
            print(f"✓ 创建新粒子享元: {key}")
        else:
            print(f"♻️ 复用粒子享元: {key}")
        
        return self._particles[key]
    
    def get_particle_count(self) -> int:
        """获取粒子享元数量"""
        return len(self._particles)
    
    def get_statistics(self) -> Dict[str, any]:
        """获取统计信息"""
        return {
            "flyweight_count": len(self._particles),
            "creation_count": self._creation_count,
            "access_count": self._access_count,
            "reuse_rate": round((self._access_count - self._creation_count) / self._access_count * 100, 1) if self._access_count > 0 else 0
        }


# ==================== 粒子实例 ====================
class ParticleInstance:
    """粒子实例 - 维护外在状态"""
    
    def __init__(self, particle: Particle, position: Tuple[float, float],
                 velocity: Tuple[float, float], life_time: float):
        """
        初始化粒子实例
        
        Args:
            particle: 粒子享元
            position: 初始位置（外在状态）
            velocity: 初始速度（外在状态）
            life_time: 生命周期（外在状态）
        """
        self.particle = particle
        self.extrinsic_state = {
            'position': position,
            'velocity': velocity,
            'life_time': life_time,
            'age': 0.0
        }
        self.is_alive = True
    
    def update(self) -> str:
        """更新粒子实例"""
        if not self.is_alive:
            return "粒子已死亡"
        
        result = self.particle.update(self.extrinsic_state)
        
        # 检查粒子是否死亡
        if self.extrinsic_state['age'] >= self.extrinsic_state['life_time']:
            self.is_alive = False
            result += " [粒子死亡]"
        
        return result
    
    def render(self) -> str:
        """渲染粒子实例"""
        if not self.is_alive:
            return ""
        
        return self.particle.render(self.extrinsic_state)
    
    def get_position(self) -> Tuple[float, float]:
        """获取位置"""
        return self.extrinsic_state['position']
    
    def get_age_progress(self) -> float:
        """获取年龄进度"""
        return self.extrinsic_state['age'] / self.extrinsic_state['life_time']


# ==================== 粒子系统 ====================
class ParticleSystem:
    """粒子系统"""
    
    def __init__(self, name: str):
        self.name = name
        self._factory = ParticleFactory()
        self._particles: List[ParticleInstance] = []
        self._total_created = 0
    
    def emit_particle(self, particle_type: ParticleType, position: Tuple[float, float],
                     velocity: Tuple[float, float] = None, life_time: float = None):
        """
        发射粒子
        
        Args:
            particle_type: 粒子类型
            position: 发射位置
            velocity: 初始速度
            life_time: 生命周期
        """
        # 使用默认值或随机值
        if velocity is None:
            velocity = (random.uniform(-2, 2), random.uniform(-2, 2))
        
        if life_time is None:
            life_time = random.uniform(1.0, 3.0)
        
        # 获取粒子享元
        particle_flyweight = self._factory.get_particle(particle_type)
        
        # 创建粒子实例
        particle_instance = ParticleInstance(particle_flyweight, position, velocity, life_time)
        self._particles.append(particle_instance)
        self._total_created += 1
    
    def emit_burst(self, particle_type: ParticleType, center: Tuple[float, float],
                   count: int, spread: float = 5.0):
        """
        发射粒子爆发
        
        Args:
            particle_type: 粒子类型
            center: 爆发中心
            count: 粒子数量
            spread: 扩散范围
        """
        print(f"💥 发射{particle_type.value}粒子爆发: {count}个粒子")
        
        for _ in range(count):
            # 随机位置和速度
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, spread)
            
            position = (
                center[0] + distance * math.cos(angle),
                center[1] + distance * math.sin(angle)
            )
            
            velocity = (
                random.uniform(-3, 3),
                random.uniform(-3, 3)
            )
            
            self.emit_particle(particle_type, position, velocity)
    
    def update(self):
        """更新粒子系统"""
        alive_particles = []
        
        for particle in self._particles:
            particle.update()
            if particle.is_alive:
                alive_particles.append(particle)
        
        dead_count = len(self._particles) - len(alive_particles)
        self._particles = alive_particles
        
        if dead_count > 0:
            print(f"💀 {dead_count} 个粒子死亡，当前活跃粒子: {len(self._particles)}")
    
    def render_preview(self, max_particles: int = 10):
        """渲染粒子系统预览"""
        print(f"\n🎮 粒子系统渲染: {self.name}")
        print("=" * 60)
        
        particles_to_show = min(max_particles, len(self._particles))
        for i in range(particles_to_show):
            render_result = self._particles[i].render()
            if render_result:
                print(f"  {i+1:2d}. {render_result}")
        
        if len(self._particles) > max_particles:
            print(f"  ... 还有 {len(self._particles) - max_particles} 个粒子")
    
    def get_statistics(self):
        """获取粒子系统统计信息"""
        factory_stats = self._factory.get_statistics()
        
        print(f"\n📊 粒子系统统计: {self.name}")
        print(f"  • 当前活跃粒子: {len(self._particles)}")
        print(f"  • 总创建粒子数: {self._total_created}")
        print(f"  • 粒子享元数: {factory_stats['flyweight_count']}")
        print(f"  • 享元创建次数: {factory_stats['creation_count']}")
        print(f"  • 享元访问次数: {factory_stats['access_count']}")
        print(f"  • 享元复用率: {factory_stats['reuse_rate']}%")
        
        if self._total_created > 0:
            memory_saved = self._total_created - factory_stats['flyweight_count']
            memory_save_rate = (memory_saved / self._total_created) * 100
            print(f"  • 节省对象数: {memory_saved}")
            print(f"  • 内存节省率: {memory_save_rate:.1f}%")


# ==================== 使用示例 ====================
def demo_particle_system():
    """粒子系统享元模式演示"""
    print("=" * 60)
    print("🎮 游戏粒子系统享元模式演示")
    print("=" * 60)
    
    # 创建粒子系统
    particle_system = ParticleSystem("战斗特效系统")
    
    # 发射不同类型的粒子
    print("\n🔥 发射火焰粒子...")
    for i in range(5):
        particle_system.emit_particle(ParticleType.FIRE, (10 + i, 20), (0, -1), 2.0)
    
    print("\n💨 发射烟雾粒子...")
    for i in range(3):
        particle_system.emit_particle(ParticleType.SMOKE, (30 + i, 25), (0.5, -0.5), 3.0)
    
    print("\n✨ 发射火花爆发...")
    particle_system.emit_burst(ParticleType.SPARK, (50, 30), 8, 10.0)
    
    print("\n💥 发射爆炸效果...")
    particle_system.emit_burst(ParticleType.EXPLOSION, (70, 35), 6, 15.0)
    
    print("\n🔮 发射魔法粒子...")
    particle_system.emit_burst(ParticleType.MAGIC, (90, 40), 4, 8.0)
    
    # 渲染初始状态
    particle_system.render_preview(15)
    
    # 模拟几帧更新
    print(f"\n⏱️ 模拟粒子系统更新...")
    for frame in range(3):
        print(f"\n--- 第 {frame + 1} 帧 ---")
        particle_system.update()
    
    # 显示统计信息
    particle_system.get_statistics()


def demo_massive_particles():
    """大量粒子演示"""
    print("\n" + "=" * 60)
    print("🌟 大量粒子享元优化演示")
    print("=" * 60)
    
    # 创建大规模粒子系统
    massive_system = ParticleSystem("大规模特效系统")
    
    print("\n🎆 创建大量粒子...")
    
    # 创建多个爆发效果
    for i in range(5):
        center = (i * 20, i * 10)
        particle_type = list(ParticleType)[i % len(ParticleType)]
        massive_system.emit_burst(particle_type, center, 20)
    
    # 显示统计信息
    massive_system.get_statistics()
    
    print(f"\n💡 享元模式优化效果:")
    print(f"   如果不使用享元模式，每个粒子都需要独立的类型对象")
    print(f"   使用享元模式后，相同类型的粒子共享同一个享元对象")
    print(f"   在大规模粒子系统中，内存节省效果非常显著")


def main():
    """主演示函数"""
    demo_particle_system()
    demo_massive_particles()
    
    print("\n" + "=" * 60)
    print("🎉 游戏粒子系统享元模式演示完成！")
    print("💡 关键要点:")
    print("   • 粒子的类型、纹理、动画等作为内在状态被共享")
    print("   • 粒子的位置、速度、生命周期等作为外在状态")
    print("   • 大量相同类型的粒子可以共享同一个享元对象")
    print("   • 在游戏中可以显著减少内存使用和提高性能")
    print("=" * 60)


if __name__ == "__main__":
    main()
