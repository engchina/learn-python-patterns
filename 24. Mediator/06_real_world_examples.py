#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中介者模式实际应用场景示例

本模块演示了中介者模式在实际项目中的应用，包括：
1. 游戏对象管理
2. 电商订单处理
3. 物联网设备协调
4. 微服务通信协调

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Any, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import random
import time


# ==================== 游戏对象管理系统 ====================

class GameObjectType(Enum):
    """游戏对象类型"""
    PLAYER = "玩家"
    ENEMY = "敌人"
    ITEM = "道具"
    PROJECTILE = "投射物"
    ENVIRONMENT = "环境"


class GameEvent(Enum):
    """游戏事件类型"""
    COLLISION = "碰撞"
    ATTACK = "攻击"
    PICKUP = "拾取"
    DEATH = "死亡"
    SPAWN = "生成"
    MOVE = "移动"


class GameObject(ABC):
    """游戏对象基类"""
    
    def __init__(self, obj_id: str, obj_type: GameObjectType, x: float, y: float):
        self.obj_id = obj_id
        self.obj_type = obj_type
        self.x = x
        self.y = y
        self.active = True
        self.game_manager: Optional['GameManager'] = None
    
    def set_game_manager(self, manager: 'GameManager') -> None:
        """设置游戏管理器"""
        self.game_manager = manager
    
    def notify_game_manager(self, event: GameEvent, data: Any = None) -> None:
        """通知游戏管理器"""
        if self.game_manager:
            self.game_manager.handle_game_event(self, event, data)
    
    def move_to(self, x: float, y: float) -> None:
        """移动到指定位置"""
        old_pos = (self.x, self.y)
        self.x, self.y = x, y
        self.notify_game_manager(GameEvent.MOVE, {
            'old_position': old_pos,
            'new_position': (x, y)
        })
    
    def get_distance_to(self, other: 'GameObject') -> float:
        """计算到另一个对象的距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """更新对象状态"""
        pass


class Player(GameObject):
    """玩家对象"""
    
    def __init__(self, obj_id: str, x: float, y: float):
        super().__init__(obj_id, GameObjectType.PLAYER, x, y)
        self.health = 100
        self.score = 0
        self.inventory: List[str] = []
    
    def attack(self, target_pos: Tuple[float, float]) -> None:
        """攻击"""
        print(f"🗡️ 玩家 {self.obj_id} 攻击位置 {target_pos}")
        self.notify_game_manager(GameEvent.ATTACK, {
            'attacker': self.obj_id,
            'target_position': target_pos,
            'damage': 25
        })
    
    def take_damage(self, damage: int) -> None:
        """受到伤害"""
        self.health -= damage
        print(f"💔 玩家 {self.obj_id} 受到 {damage} 点伤害，剩余血量: {self.health}")
        
        if self.health <= 0:
            self.active = False
            self.notify_game_manager(GameEvent.DEATH, {'player_id': self.obj_id})
    
    def pickup_item(self, item_id: str) -> None:
        """拾取道具"""
        self.inventory.append(item_id)
        self.score += 10
        print(f"📦 玩家 {self.obj_id} 拾取道具 {item_id}，得分: {self.score}")
    
    def update(self, delta_time: float) -> None:
        """更新玩家状态"""
        # 玩家逻辑更新
        pass


class Enemy(GameObject):
    """敌人对象"""
    
    def __init__(self, obj_id: str, x: float, y: float):
        super().__init__(obj_id, GameObjectType.ENEMY, x, y)
        self.health = 50
        self.attack_range = 30.0
        self.move_speed = 20.0
        self.target_player: Optional[str] = None
    
    def update(self, delta_time: float) -> None:
        """更新敌人状态"""
        if not self.active or not self.game_manager:
            return
        
        # 寻找最近的玩家
        nearest_player = self.game_manager.find_nearest_player(self)
        if nearest_player:
            distance = self.get_distance_to(nearest_player)
            
            if distance <= self.attack_range:
                # 攻击玩家
                self.attack_player(nearest_player)
            else:
                # 向玩家移动
                self.move_towards_player(nearest_player, delta_time)
    
    def attack_player(self, player: Player) -> None:
        """攻击玩家"""
        print(f"👹 敌人 {self.obj_id} 攻击玩家 {player.obj_id}")
        self.notify_game_manager(GameEvent.ATTACK, {
            'attacker': self.obj_id,
            'target': player.obj_id,
            'damage': 15
        })
    
    def move_towards_player(self, player: Player, delta_time: float) -> None:
        """向玩家移动"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance > 0:
            # 标准化方向向量
            dx /= distance
            dy /= distance
            
            # 移动
            new_x = self.x + dx * self.move_speed * delta_time
            new_y = self.y + dy * self.move_speed * delta_time
            self.move_to(new_x, new_y)
    
    def take_damage(self, damage: int) -> None:
        """受到伤害"""
        self.health -= damage
        print(f"💥 敌人 {self.obj_id} 受到 {damage} 点伤害，剩余血量: {self.health}")
        
        if self.health <= 0:
            self.active = False
            self.notify_game_manager(GameEvent.DEATH, {'enemy_id': self.obj_id})


class Item(GameObject):
    """道具对象"""
    
    def __init__(self, obj_id: str, x: float, y: float, item_type: str):
        super().__init__(obj_id, GameObjectType.ITEM, x, y)
        self.item_type = item_type
        self.pickup_range = 15.0
    
    def update(self, delta_time: float) -> None:
        """更新道具状态"""
        if not self.active or not self.game_manager:
            return
        
        # 检查是否有玩家在拾取范围内
        for player in self.game_manager.get_players():
            if self.get_distance_to(player) <= self.pickup_range:
                self.notify_game_manager(GameEvent.PICKUP, {
                    'item_id': self.obj_id,
                    'player_id': player.obj_id,
                    'item_type': self.item_type
                })
                self.active = False
                break


class GameManager:
    """游戏管理器中介者"""
    
    def __init__(self):
        self.game_objects: Dict[str, GameObject] = {}
        self.players: Dict[str, Player] = {}
        self.enemies: Dict[str, Enemy] = {}
        self.items: Dict[str, Item] = {}
        self.game_time = 0.0
        self.is_running = False
    
    def add_game_object(self, obj: GameObject) -> None:
        """添加游戏对象"""
        obj.set_game_manager(self)
        self.game_objects[obj.obj_id] = obj
        
        if isinstance(obj, Player):
            self.players[obj.obj_id] = obj
        elif isinstance(obj, Enemy):
            self.enemies[obj.obj_id] = obj
        elif isinstance(obj, Item):
            self.items[obj.obj_id] = obj
        
        print(f"🎮 添加游戏对象: {obj.obj_type.value} {obj.obj_id}")
    
    def remove_game_object(self, obj_id: str) -> None:
        """移除游戏对象"""
        if obj_id in self.game_objects:
            obj = self.game_objects[obj_id]
            del self.game_objects[obj_id]
            
            # 从特定类型字典中移除
            if obj_id in self.players:
                del self.players[obj_id]
            elif obj_id in self.enemies:
                del self.enemies[obj_id]
            elif obj_id in self.items:
                del self.items[obj_id]
            
            print(f"🗑️ 移除游戏对象: {obj.obj_type.value} {obj_id}")
    
    def handle_game_event(self, sender: GameObject, event: GameEvent, data: Any = None) -> None:
        """处理游戏事件"""
        print(f"🎯 游戏事件: {sender.obj_id} -> {event.value}")
        
        if event == GameEvent.ATTACK:
            self._handle_attack(data)
        elif event == GameEvent.PICKUP:
            self._handle_pickup(data)
        elif event == GameEvent.DEATH:
            self._handle_death(data)
        elif event == GameEvent.COLLISION:
            self._handle_collision(data)
    
    def _handle_attack(self, data: Dict[str, Any]) -> None:
        """处理攻击事件"""
        attacker_id = data['attacker']
        damage = data['damage']
        
        if 'target' in data:
            # 直接攻击目标
            target_id = data['target']
            if target_id in self.players:
                self.players[target_id].take_damage(damage)
            elif target_id in self.enemies:
                self.enemies[target_id].take_damage(damage)
        elif 'target_position' in data:
            # 区域攻击
            target_pos = data['target_position']
            attack_range = 20.0
            
            # 检查范围内的敌人
            for enemy in self.enemies.values():
                if enemy.active:
                    distance = ((enemy.x - target_pos[0]) ** 2 + (enemy.y - target_pos[1]) ** 2) ** 0.5
                    if distance <= attack_range:
                        enemy.take_damage(damage)
    
    def _handle_pickup(self, data: Dict[str, Any]) -> None:
        """处理拾取事件"""
        item_id = data['item_id']
        player_id = data['player_id']
        
        if player_id in self.players and item_id in self.items:
            player = self.players[player_id]
            item = self.items[item_id]
            
            player.pickup_item(item_id)
            self.remove_game_object(item_id)
    
    def _handle_death(self, data: Dict[str, Any]) -> None:
        """处理死亡事件"""
        if 'player_id' in data:
            player_id = data['player_id']
            print(f"💀 玩家 {player_id} 死亡")
            # 可以在这里添加重生逻辑
        elif 'enemy_id' in data:
            enemy_id = data['enemy_id']
            print(f"💀 敌人 {enemy_id} 死亡")
            self.remove_game_object(enemy_id)
            
            # 随机生成道具
            if random.random() < 0.3:  # 30%概率掉落道具
                self._spawn_item_at_position(self.enemies[enemy_id].x, self.enemies[enemy_id].y)
    
    def _handle_collision(self, data: Dict[str, Any]) -> None:
        """处理碰撞事件"""
        # 碰撞处理逻辑
        pass
    
    def _spawn_item_at_position(self, x: float, y: float) -> None:
        """在指定位置生成道具"""
        item_types = ["health_potion", "coin", "power_up"]
        item_type = random.choice(item_types)
        item_id = f"item_{len(self.items) + 1}"
        
        item = Item(item_id, x, y, item_type)
        self.add_game_object(item)
        print(f"✨ 在位置 ({x:.1f}, {y:.1f}) 生成道具: {item_type}")
    
    def find_nearest_player(self, obj: GameObject) -> Optional[Player]:
        """寻找最近的玩家"""
        nearest_player = None
        min_distance = float('inf')
        
        for player in self.players.values():
            if player.active:
                distance = obj.get_distance_to(player)
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player
        
        return nearest_player
    
    def get_players(self) -> List[Player]:
        """获取所有活跃玩家"""
        return [player for player in self.players.values() if player.active]
    
    def update_game(self, delta_time: float) -> None:
        """更新游戏状态"""
        self.game_time += delta_time
        
        # 更新所有游戏对象
        for obj in list(self.game_objects.values()):
            if obj.active:
                obj.update(delta_time)
    
    def get_game_stats(self) -> Dict[str, Any]:
        """获取游戏统计"""
        active_players = len([p for p in self.players.values() if p.active])
        active_enemies = len([e for e in self.enemies.values() if e.active])
        active_items = len([i for i in self.items.values() if i.active])
        
        return {
            'game_time': self.game_time,
            'active_players': active_players,
            'active_enemies': active_enemies,
            'active_items': active_items,
            'total_objects': len(self.game_objects)
        }


def demo_game_system():
    """演示游戏系统"""
    print("=" * 50)
    print("🎮 游戏对象管理系统演示")
    print("=" * 50)
    
    # 创建游戏管理器
    game = GameManager()
    
    # 创建玩家
    player1 = Player("player1", 50.0, 50.0)
    game.add_game_object(player1)
    
    # 创建敌人
    enemy1 = Enemy("enemy1", 100.0, 100.0)
    enemy2 = Enemy("enemy2", 20.0, 80.0)
    game.add_game_object(enemy1)
    game.add_game_object(enemy2)
    
    # 创建道具
    item1 = Item("item1", 30.0, 30.0, "health_potion")
    item2 = Item("item2", 70.0, 70.0, "coin")
    game.add_game_object(item1)
    game.add_game_object(item2)
    
    print(f"\n📊 初始游戏状态: {game.get_game_stats()}")
    
    # 模拟游戏循环
    print("\n🎯 开始游戏模拟:")
    
    for frame in range(5):
        print(f"\n--- 帧 {frame + 1} ---")
        
        # 玩家行动
        if frame == 1:
            # 玩家移动到道具附近
            player1.move_to(25.0, 25.0)
        elif frame == 2:
            # 玩家攻击敌人
            player1.attack((100.0, 100.0))
        elif frame == 3:
            # 玩家移动
            player1.move_to(60.0, 60.0)
        
        # 更新游戏状态
        game.update_game(0.1)  # 模拟0.1秒的时间步长
        
        # 显示当前状态
        stats = game.get_game_stats()
        print(f"📊 当前状态: {stats}")
        
        time.sleep(0.1)  # 模拟帧间隔
    
    print(f"\n🏆 最终玩家状态:")
    print(f"  血量: {player1.health}")
    print(f"  得分: {player1.score}")
    print(f"  背包: {player1.inventory}")


# ==================== 电商订单处理系统 ====================

class OrderStatus(Enum):
    """订单状态"""
    PENDING = "待处理"
    CONFIRMED = "已确认"
    PAID = "已支付"
    SHIPPED = "已发货"
    DELIVERED = "已送达"
    CANCELLED = "已取消"


class OrderEvent(Enum):
    """订单事件"""
    CREATED = "订单创建"
    PAYMENT_RECEIVED = "收到付款"
    INVENTORY_RESERVED = "库存预留"
    SHIPPED = "已发货"
    DELIVERED = "已送达"
    CANCELLED = "订单取消"


class OrderService:
    """订单服务"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.order_coordinator: Optional['OrderCoordinator'] = None
    
    def set_coordinator(self, coordinator: 'OrderCoordinator') -> None:
        """设置协调器"""
        self.order_coordinator = coordinator
    
    def notify_coordinator(self, event: OrderEvent, order_id: str, data: Any = None) -> None:
        """通知协调器"""
        if self.order_coordinator:
            self.order_coordinator.handle_order_event(self.service_name, event, order_id, data)


class PaymentService(OrderService):
    """支付服务"""
    
    def __init__(self):
        super().__init__("PaymentService")
    
    def process_payment(self, order_id: str, amount: float) -> bool:
        """处理支付"""
        print(f"💳 处理订单 {order_id} 的支付，金额: ¥{amount}")
        
        # 模拟支付处理
        success = random.random() > 0.1  # 90%成功率
        
        if success:
            print(f"✅ 订单 {order_id} 支付成功")
            self.notify_coordinator(OrderEvent.PAYMENT_RECEIVED, order_id, {"amount": amount})
        else:
            print(f"❌ 订单 {order_id} 支付失败")
        
        return success


class InventoryService(OrderService):
    """库存服务"""
    
    def __init__(self):
        super().__init__("InventoryService")
        self.inventory = {"product_1": 100, "product_2": 50, "product_3": 200}
    
    def reserve_inventory(self, order_id: str, items: List[Dict[str, Any]]) -> bool:
        """预留库存"""
        print(f"📦 为订单 {order_id} 预留库存")
        
        # 检查库存是否充足
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            
            if self.inventory.get(product_id, 0) < quantity:
                print(f"❌ 产品 {product_id} 库存不足")
                return False
        
        # 预留库存
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            self.inventory[product_id] -= quantity
        
        print(f"✅ 订单 {order_id} 库存预留成功")
        self.notify_coordinator(OrderEvent.INVENTORY_RESERVED, order_id, {"items": items})
        return True


class ShippingService(OrderService):
    """物流服务"""
    
    def __init__(self):
        super().__init__("ShippingService")
    
    def ship_order(self, order_id: str, address: str) -> str:
        """发货"""
        tracking_number = f"TRK_{order_id}_{random.randint(1000, 9999)}"
        print(f"🚚 订单 {order_id} 已发货到 {address}，跟踪号: {tracking_number}")
        
        self.notify_coordinator(OrderEvent.SHIPPED, order_id, {
            "tracking_number": tracking_number,
            "address": address
        })
        
        return tracking_number


class NotificationService(OrderService):
    """通知服务"""
    
    def __init__(self):
        super().__init__("NotificationService")
    
    def send_notification(self, order_id: str, message: str, customer_email: str) -> None:
        """发送通知"""
        print(f"📧 发送通知到 {customer_email}: {message}")


class OrderCoordinator:
    """订单协调器中介者"""
    
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}
        self.payment_service = PaymentService()
        self.inventory_service = InventoryService()
        self.shipping_service = ShippingService()
        self.notification_service = NotificationService()
        
        # 设置协调器
        for service in [self.payment_service, self.inventory_service, 
                       self.shipping_service, self.notification_service]:
            service.set_coordinator(self)
    
    def create_order(self, order_id: str, customer_email: str, items: List[Dict[str, Any]], 
                    total_amount: float, shipping_address: str) -> None:
        """创建订单"""
        order = {
            'order_id': order_id,
            'customer_email': customer_email,
            'items': items,
            'total_amount': total_amount,
            'shipping_address': shipping_address,
            'status': OrderStatus.PENDING,
            'created_at': datetime.now(),
            'events': []
        }
        
        self.orders[order_id] = order
        print(f"📋 创建订单: {order_id}")
        
        # 开始处理流程
        self._process_order(order_id)
    
    def _process_order(self, order_id: str) -> None:
        """处理订单"""
        order = self.orders[order_id]
        
        # 1. 预留库存
        if self.inventory_service.reserve_inventory(order_id, order['items']):
            # 2. 处理支付
            self.payment_service.process_payment(order_id, order['total_amount'])
        else:
            # 库存不足，取消订单
            self._cancel_order(order_id, "库存不足")
    
    def handle_order_event(self, service_name: str, event: OrderEvent, order_id: str, data: Any = None) -> None:
        """处理订单事件"""
        if order_id not in self.orders:
            return
        
        order = self.orders[order_id]
        order['events'].append({
            'service': service_name,
            'event': event.value,
            'timestamp': datetime.now(),
            'data': data
        })
        
        print(f"📨 订单事件: {service_name} -> {event.value} (订单: {order_id})")
        
        if event == OrderEvent.PAYMENT_RECEIVED:
            self._handle_payment_received(order_id, data)
        elif event == OrderEvent.SHIPPED:
            self._handle_order_shipped(order_id, data)
    
    def _handle_payment_received(self, order_id: str, data: Dict[str, Any]) -> None:
        """处理支付成功"""
        order = self.orders[order_id]
        order['status'] = OrderStatus.PAID
        
        # 发送支付确认通知
        self.notification_service.send_notification(
            order_id, 
            f"您的订单 {order_id} 支付成功，金额: ¥{data['amount']}", 
            order['customer_email']
        )
        
        # 安排发货
        self.shipping_service.ship_order(order_id, order['shipping_address'])
    
    def _handle_order_shipped(self, order_id: str, data: Dict[str, Any]) -> None:
        """处理订单发货"""
        order = self.orders[order_id]
        order['status'] = OrderStatus.SHIPPED
        order['tracking_number'] = data['tracking_number']
        
        # 发送发货通知
        self.notification_service.send_notification(
            order_id,
            f"您的订单 {order_id} 已发货，跟踪号: {data['tracking_number']}",
            order['customer_email']
        )
    
    def _cancel_order(self, order_id: str, reason: str) -> None:
        """取消订单"""
        order = self.orders[order_id]
        order['status'] = OrderStatus.CANCELLED
        order['cancel_reason'] = reason
        
        print(f"🚫 订单 {order_id} 已取消: {reason}")
        
        # 发送取消通知
        self.notification_service.send_notification(
            order_id,
            f"很抱歉，您的订单 {order_id} 已取消: {reason}",
            order['customer_email']
        )
    
    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """获取订单状态"""
        if order_id in self.orders:
            order = self.orders[order_id]
            return {
                'order_id': order_id,
                'status': order['status'].value,
                'total_amount': order['total_amount'],
                'created_at': order['created_at'].isoformat(),
                'events_count': len(order['events'])
            }
        return None


def demo_order_system():
    """演示订单处理系统"""
    print("\n" + "=" * 50)
    print("🛒 电商订单处理系统演示")
    print("=" * 50)
    
    # 创建订单协调器
    coordinator = OrderCoordinator()
    
    # 创建测试订单
    order_items = [
        {"product_id": "product_1", "quantity": 2, "price": 99.99},
        {"product_id": "product_2", "quantity": 1, "price": 149.99}
    ]
    
    total_amount = sum(item["quantity"] * item["price"] for item in order_items)
    
    print("📦 创建订单:")
    coordinator.create_order(
        order_id="ORD_001",
        customer_email="customer@example.com",
        items=order_items,
        total_amount=total_amount,
        shipping_address="北京市朝阳区xxx街道xxx号"
    )
    
    # 等待处理完成
    time.sleep(0.5)
    
    # 显示订单状态
    print("\n📊 订单状态:")
    status = coordinator.get_order_status("ORD_001")
    if status:
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    # 显示库存状态
    print(f"\n📦 当前库存: {coordinator.inventory_service.inventory}")


if __name__ == "__main__":
    print("🎯 中介者模式实际应用演示")
    
    # 运行游戏系统演示
    demo_game_system()
    
    # 运行订单系统演示
    demo_order_system()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 中介者模式在复杂系统中发挥着重要的协调作用")
    print("=" * 50)
