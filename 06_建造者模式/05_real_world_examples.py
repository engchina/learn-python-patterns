"""
05_real_world_examples.py - 建造者模式实际应用示例

这个文件包含了建造者模式在实际项目中的应用示例，
展示了如何在真实场景中使用建造者模式解决复杂的构建问题。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid


# ==================== 电商系统：订单建造者 ====================
class OrderStatus(Enum):
    """订单状态"""
    PENDING = "待支付"
    PAID = "已支付"
    SHIPPED = "已发货"
    DELIVERED = "已送达"
    CANCELLED = "已取消"


class PaymentMethod(Enum):
    """支付方式"""
    CREDIT_CARD = "信用卡"
    DEBIT_CARD = "借记卡"
    ALIPAY = "支付宝"
    WECHAT_PAY = "微信支付"
    BANK_TRANSFER = "银行转账"


class OrderItem:
    """订单项"""
    
    def __init__(self, product_id: str, product_name: str, price: float, quantity: int):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.discount = 0.0
        self.tax_rate = 0.0
    
    def get_subtotal(self) -> float:
        """获取小计"""
        subtotal = self.price * self.quantity
        subtotal -= self.discount
        subtotal += subtotal * self.tax_rate
        return round(subtotal, 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "discount": self.discount,
            "tax_rate": self.tax_rate,
            "subtotal": self.get_subtotal()
        }


class ShippingAddress:
    """收货地址"""
    
    def __init__(self):
        self.recipient_name = ""
        self.phone = ""
        self.country = ""
        self.province = ""
        self.city = ""
        self.district = ""
        self.street_address = ""
        self.postal_code = ""
        self.is_default = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "recipient_name": self.recipient_name,
            "phone": self.phone,
            "country": self.country,
            "province": self.province,
            "city": self.city,
            "district": self.district,
            "street_address": self.street_address,
            "postal_code": self.postal_code,
            "is_default": self.is_default
        }


class Order:
    """订单类"""
    
    def __init__(self):
        self.order_id = str(uuid.uuid4())
        self.customer_id = ""
        self.customer_name = ""
        self.customer_email = ""
        self.items = []
        self.shipping_address = ShippingAddress()
        self.billing_address = ShippingAddress()
        self.payment_method = PaymentMethod.CREDIT_CARD
        self.status = OrderStatus.PENDING
        self.subtotal = 0.0
        self.shipping_fee = 0.0
        self.tax_amount = 0.0
        self.discount_amount = 0.0
        self.total_amount = 0.0
        self.currency = "CNY"
        self.notes = ""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.estimated_delivery = None
        self.tracking_number = ""
        self.coupon_code = ""
        self.loyalty_points_used = 0
        self.metadata = {}
    
    def add_item(self, item: OrderItem):
        """添加订单项"""
        self.items.append(item)
        self.calculate_totals()
    
    def calculate_totals(self):
        """计算总金额"""
        self.subtotal = sum(item.get_subtotal() for item in self.items)
        self.total_amount = self.subtotal + self.shipping_fee + self.tax_amount - self.discount_amount
        self.total_amount = round(self.total_amount, 2)
        self.updated_at = datetime.now()
    
    def apply_coupon(self, coupon_code: str, discount_amount: float):
        """应用优惠券"""
        self.coupon_code = coupon_code
        self.discount_amount = discount_amount
        self.calculate_totals()
    
    def set_estimated_delivery(self, days: int):
        """设置预计送达时间"""
        self.estimated_delivery = self.created_at + timedelta(days=days)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "items": [item.to_dict() for item in self.items],
            "shipping_address": self.shipping_address.to_dict(),
            "billing_address": self.billing_address.to_dict(),
            "payment_method": self.payment_method.value,
            "status": self.status.value,
            "subtotal": self.subtotal,
            "shipping_fee": self.shipping_fee,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "estimated_delivery": self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            "tracking_number": self.tracking_number,
            "coupon_code": self.coupon_code,
            "loyalty_points_used": self.loyalty_points_used,
            "metadata": self.metadata
        }


class OrderBuilder:
    """订单建造者"""
    
    def __init__(self):
        self.order = Order()
    
    def set_customer(self, customer_id: str, name: str, email: str) -> 'OrderBuilder':
        """设置客户信息"""
        self.order.customer_id = customer_id
        self.order.customer_name = name
        self.order.customer_email = email
        return self
    
    def add_item(self, product_id: str, product_name: str, price: float, quantity: int) -> 'OrderBuilder':
        """添加商品"""
        item = OrderItem(product_id, product_name, price, quantity)
        self.order.add_item(item)
        return self
    
    def set_shipping_address(self, name: str, phone: str, address: str, city: str, province: str, postal_code: str) -> 'OrderBuilder':
        """设置收货地址"""
        self.order.shipping_address.recipient_name = name
        self.order.shipping_address.phone = phone
        self.order.shipping_address.street_address = address
        self.order.shipping_address.city = city
        self.order.shipping_address.province = province
        self.order.shipping_address.postal_code = postal_code
        self.order.shipping_address.country = "中国"
        return self
    
    def set_payment_method(self, method: PaymentMethod) -> 'OrderBuilder':
        """设置支付方式"""
        self.order.payment_method = method
        return self
    
    def set_shipping_fee(self, fee: float) -> 'OrderBuilder':
        """设置运费"""
        self.order.shipping_fee = fee
        self.order.calculate_totals()
        return self
    
    def apply_coupon(self, coupon_code: str, discount_amount: float) -> 'OrderBuilder':
        """应用优惠券"""
        self.order.apply_coupon(coupon_code, discount_amount)
        return self
    
    def use_loyalty_points(self, points: int, value: float) -> 'OrderBuilder':
        """使用积分"""
        self.order.loyalty_points_used = points
        self.order.discount_amount += value
        self.order.calculate_totals()
        return self
    
    def set_notes(self, notes: str) -> 'OrderBuilder':
        """设置备注"""
        self.order.notes = notes
        return self
    
    def set_delivery_days(self, days: int) -> 'OrderBuilder':
        """设置预计送达天数"""
        self.order.set_estimated_delivery(days)
        return self
    
    def build(self) -> Order:
        """构建订单"""
        return self.order


# ==================== 游戏开发：角色建造者 ====================
class CharacterClass(Enum):
    """角色职业"""
    WARRIOR = "战士"
    MAGE = "法师"
    ARCHER = "弓箭手"
    ROGUE = "盗贼"
    PRIEST = "牧师"


class Attribute:
    """属性"""
    
    def __init__(self, base_value: int = 10):
        self.base_value = base_value
        self.bonus_value = 0
        self.equipment_bonus = 0
        self.temporary_bonus = 0
    
    def get_total(self) -> int:
        """获取总属性值"""
        return self.base_value + self.bonus_value + self.equipment_bonus + self.temporary_bonus


class Skill:
    """技能"""
    
    def __init__(self, name: str, level: int = 1, max_level: int = 10):
        self.name = name
        self.level = level
        self.max_level = max_level
        self.experience = 0
        self.description = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "level": self.level,
            "max_level": self.max_level,
            "experience": self.experience,
            "description": self.description
        }


class Equipment:
    """装备"""
    
    def __init__(self, name: str, equipment_type: str, level: int = 1):
        self.name = name
        self.equipment_type = equipment_type
        self.level = level
        self.attributes = {}
        self.special_effects = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.equipment_type,
            "level": self.level,
            "attributes": self.attributes,
            "special_effects": self.special_effects
        }


class GameCharacter:
    """游戏角色"""
    
    def __init__(self):
        self.character_id = str(uuid.uuid4())
        self.name = ""
        self.character_class = CharacterClass.WARRIOR
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # 基础属性
        self.strength = Attribute(10)
        self.agility = Attribute(10)
        self.intelligence = Attribute(10)
        self.vitality = Attribute(10)
        self.luck = Attribute(10)
        
        # 衍生属性
        self.health = 100
        self.mana = 50
        self.stamina = 100
        
        # 技能和装备
        self.skills = []
        self.equipment = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "boots": None,
            "accessory": None
        }
        
        # 背包和金币
        self.inventory = []
        self.gold = 0
        
        # 其他信息
        self.created_at = datetime.now()
        self.last_login = datetime.now()
        self.play_time = 0  # 游戏时间（分钟）
        self.achievements = []
        self.guild_id = ""
        self.pvp_rating = 1000
    
    def add_skill(self, skill: Skill):
        """添加技能"""
        self.skills.append(skill)
    
    def equip_item(self, equipment: Equipment):
        """装备物品"""
        self.equipment[equipment.equipment_type] = equipment
    
    def calculate_combat_power(self) -> int:
        """计算战斗力"""
        base_power = (self.strength.get_total() * 2 + 
                     self.agility.get_total() + 
                     self.intelligence.get_total() + 
                     self.vitality.get_total()) * self.level
        
        # 装备加成
        equipment_bonus = 0
        for item in self.equipment.values():
            if item:
                equipment_bonus += item.level * 10
        
        # 技能加成
        skill_bonus = sum(skill.level * 5 for skill in self.skills)
        
        return base_power + equipment_bonus + skill_bonus
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "character_id": self.character_id,
            "name": self.name,
            "class": self.character_class.value,
            "level": self.level,
            "experience": self.experience,
            "attributes": {
                "strength": self.strength.get_total(),
                "agility": self.agility.get_total(),
                "intelligence": self.intelligence.get_total(),
                "vitality": self.vitality.get_total(),
                "luck": self.luck.get_total()
            },
            "health": self.health,
            "mana": self.mana,
            "stamina": self.stamina,
            "skills": [skill.to_dict() for skill in self.skills],
            "equipment": {k: v.to_dict() if v else None for k, v in self.equipment.items()},
            "inventory_count": len(self.inventory),
            "gold": self.gold,
            "combat_power": self.calculate_combat_power(),
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat(),
            "play_time": self.play_time,
            "achievements_count": len(self.achievements),
            "guild_id": self.guild_id,
            "pvp_rating": self.pvp_rating
        }


class CharacterBuilder:
    """角色建造者"""
    
    def __init__(self):
        self.character = GameCharacter()
    
    def set_basic_info(self, name: str, character_class: CharacterClass) -> 'CharacterBuilder':
        """设置基本信息"""
        self.character.name = name
        self.character.character_class = character_class
        return self
    
    def set_level(self, level: int) -> 'CharacterBuilder':
        """设置等级"""
        self.character.level = level
        self.character.experience_to_next_level = level * 100
        return self
    
    def set_attributes(self, strength: int = None, agility: int = None, 
                      intelligence: int = None, vitality: int = None, luck: int = None) -> 'CharacterBuilder':
        """设置属性"""
        if strength is not None:
            self.character.strength.base_value = strength
        if agility is not None:
            self.character.agility.base_value = agility
        if intelligence is not None:
            self.character.intelligence.base_value = intelligence
        if vitality is not None:
            self.character.vitality.base_value = vitality
        if luck is not None:
            self.character.luck.base_value = luck
        
        # 重新计算衍生属性
        self.character.health = self.character.vitality.get_total() * 10
        self.character.mana = self.character.intelligence.get_total() * 5
        self.character.stamina = (self.character.strength.get_total() + self.character.agility.get_total()) * 5
        
        return self
    
    def add_skill(self, name: str, level: int = 1, description: str = "") -> 'CharacterBuilder':
        """添加技能"""
        skill = Skill(name, level)
        skill.description = description
        self.character.add_skill(skill)
        return self
    
    def equip_weapon(self, name: str, level: int = 1, attributes: Dict[str, int] = None) -> 'CharacterBuilder':
        """装备武器"""
        weapon = Equipment(name, "weapon", level)
        if attributes:
            weapon.attributes = attributes
        self.character.equip_item(weapon)
        return self
    
    def equip_armor(self, name: str, level: int = 1, attributes: Dict[str, int] = None) -> 'CharacterBuilder':
        """装备护甲"""
        armor = Equipment(name, "armor", level)
        if attributes:
            armor.attributes = attributes
        self.character.equip_item(armor)
        return self
    
    def set_gold(self, amount: int) -> 'CharacterBuilder':
        """设置金币"""
        self.character.gold = amount
        return self
    
    def join_guild(self, guild_id: str) -> 'CharacterBuilder':
        """加入公会"""
        self.character.guild_id = guild_id
        return self
    
    def set_pvp_rating(self, rating: int) -> 'CharacterBuilder':
        """设置PVP评级"""
        self.character.pvp_rating = rating
        return self
    
    def build(self) -> GameCharacter:
        """构建角色"""
        return self.character


# ==================== 演示函数 ====================
def demonstrate_order_builder():
    """演示订单建造者"""
    print("=" * 60)
    print("电商订单建造者演示")
    print("=" * 60)
    
    # 构建一个复杂订单
    order = (OrderBuilder()
             .set_customer("CUST001", "张三", "zhangsan@example.com")
             .add_item("PROD001", "iPhone 15 Pro", 7999.0, 1)
             .add_item("PROD002", "AirPods Pro", 1999.0, 1)
             .add_item("PROD003", "手机壳", 99.0, 2)
             .set_shipping_address("张三", "13800138000", "中关村大街1号", "北京市", "北京市", "100000")
             .set_payment_method(PaymentMethod.ALIPAY)
             .set_shipping_fee(15.0)
             .apply_coupon("SAVE100", 100.0)
             .use_loyalty_points(500, 50.0)
             .set_notes("请在工作日送货")
             .set_delivery_days(3)
             .build())
    
    print(f"订单ID: {order.order_id}")
    print(f"客户: {order.customer_name}")
    print(f"商品数量: {len(order.items)}")
    print(f"小计: ¥{order.subtotal}")
    print(f"运费: ¥{order.shipping_fee}")
    print(f"优惠: ¥{order.discount_amount}")
    print(f"总金额: ¥{order.total_amount}")
    print(f"支付方式: {order.payment_method.value}")
    print(f"预计送达: {order.estimated_delivery.strftime('%Y-%m-%d') if order.estimated_delivery else '未设置'}")


def demonstrate_character_builder():
    """演示角色建造者"""
    print("\n" + "=" * 60)
    print("游戏角色建造者演示")
    print("=" * 60)
    
    # 构建一个战士角色
    warrior = (CharacterBuilder()
               .set_basic_info("钢铁战士", CharacterClass.WARRIOR)
               .set_level(25)
               .set_attributes(strength=30, agility=15, intelligence=10, vitality=25, luck=12)
               .add_skill("重击", 5, "造成额外伤害的强力攻击")
               .add_skill("格挡", 3, "减少受到的伤害")
               .add_skill("战吼", 2, "提升队友士气")
               .equip_weapon("传说之剑", 10, {"attack": 50, "critical": 10})
               .equip_armor("龙鳞甲", 8, {"defense": 40, "health": 100})
               .set_gold(50000)
               .join_guild("GUILD001")
               .set_pvp_rating(1500)
               .build())
    
    print(f"角色名称: {warrior.name}")
    print(f"职业: {warrior.character_class.value}")
    print(f"等级: {warrior.level}")
    print(f"战斗力: {warrior.calculate_combat_power()}")
    print(f"生命值: {warrior.health}")
    print(f"法力值: {warrior.mana}")
    print(f"技能数量: {len(warrior.skills)}")
    print(f"金币: {warrior.gold}")
    print(f"PVP评级: {warrior.pvp_rating}")
    
    # 构建一个法师角色
    print("\n" + "-" * 40)
    
    mage = (CharacterBuilder()
            .set_basic_info("智慧法师", CharacterClass.MAGE)
            .set_level(20)
            .set_attributes(strength=8, agility=12, intelligence=35, vitality=15, luck=15)
            .add_skill("火球术", 8, "发射火球攻击敌人")
            .add_skill("冰冻术", 6, "冻结敌人")
            .add_skill("传送术", 4, "瞬间移动")
            .equip_weapon("智慧法杖", 12, {"magic_power": 60, "mana": 50})
            .equip_armor("法师长袍", 6, {"magic_defense": 30, "mana": 30})
            .set_gold(35000)
            .set_pvp_rating(1200)
            .build())
    
    print(f"角色名称: {mage.name}")
    print(f"职业: {mage.character_class.value}")
    print(f"等级: {mage.level}")
    print(f"战斗力: {mage.calculate_combat_power()}")
    print(f"生命值: {mage.health}")
    print(f"法力值: {mage.mana}")
    print(f"技能数量: {len(mage.skills)}")
    print(f"金币: {mage.gold}")


def main():
    """主函数"""
    print("建造者模式实际应用示例")
    
    demonstrate_order_builder()
    demonstrate_character_builder()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
