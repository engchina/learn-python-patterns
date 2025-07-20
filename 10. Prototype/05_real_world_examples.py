"""
05_real_world_examples.py - 原型模式实际应用示例

这个文件包含了原型模式在实际项目中的应用示例，
展示了如何在真实场景中使用原型模式解决实际问题。
"""

import copy
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


# ==================== 电商系统：商品原型 ====================
class ProductCategory(Enum):
    """商品分类"""
    ELECTRONICS = "电子产品"
    CLOTHING = "服装"
    BOOKS = "图书"
    HOME = "家居用品"
    SPORTS = "体育用品"


class Product(ABC):
    """商品原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆商品"""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """获取商品信息"""
        pass


class ElectronicsProduct(Product):
    """电子产品类"""

    def __init__(self, name: str = "电子产品"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.category = ProductCategory.ELECTRONICS
        self.price = 0.0
        self.brand = ""
        self.model = ""
        self.warranty_months = 12
        self.specifications = {}
        self.images = []
        self.stock_quantity = 0
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # 电子产品特有属性
        self.power_consumption = ""
        self.dimensions = {"width": 0, "height": 0, "depth": 0}
        self.weight = 0.0
        self.certifications = []

    def clone(self):
        """克隆电子产品"""
        new_product = copy.copy(self)
        # 生成新的ID和时间戳
        new_product.id = str(uuid.uuid4())
        new_product.created_at = datetime.now()
        new_product.updated_at = datetime.now()
        # 深拷贝复杂对象
        new_product.specifications = self.specifications.copy()
        new_product.images = self.images.copy()
        new_product.dimensions = self.dimensions.copy()
        new_product.certifications = self.certifications.copy()
        return new_product

    def set_specifications(self, specs: Dict[str, str]):
        """设置产品规格"""
        self.specifications.update(specs)
        self.updated_at = datetime.now()

    def add_certification(self, cert: str):
        """添加认证"""
        if cert not in self.certifications:
            self.certifications.append(cert)
            self.updated_at = datetime.now()

    def get_info(self) -> Dict[str, Any]:
        """获取商品信息"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "price": self.price,
            "brand": self.brand,
            "model": self.model,
            "warranty_months": self.warranty_months,
            "specifications": self.specifications,
            "stock_quantity": self.stock_quantity,
            "power_consumption": self.power_consumption,
            "dimensions": self.dimensions,
            "weight": self.weight,
            "certifications": self.certifications,
            "is_active": self.is_active
        }


class ClothingProduct(Product):
    """服装产品类"""

    def __init__(self, name: str = "服装"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.category = ProductCategory.CLOTHING
        self.price = 0.0
        self.brand = ""
        self.material = ""
        self.colors = []
        self.sizes = []
        self.gender = "unisex"  # male, female, unisex
        self.season = "all"  # spring, summer, autumn, winter, all
        self.care_instructions = []
        self.images = []
        self.stock_by_variant = {}  # {(color, size): quantity}
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def clone(self):
        """克隆服装产品"""
        new_product = copy.copy(self)
        new_product.id = str(uuid.uuid4())
        new_product.created_at = datetime.now()
        new_product.updated_at = datetime.now()
        # 深拷贝复杂对象
        new_product.colors = self.colors.copy()
        new_product.sizes = self.sizes.copy()
        new_product.care_instructions = self.care_instructions.copy()
        new_product.images = self.images.copy()
        new_product.stock_by_variant = self.stock_by_variant.copy()
        return new_product

    def add_variant(self, color: str, size: str, quantity: int):
        """添加商品变体"""
        variant_key = (color, size)
        self.stock_by_variant[variant_key] = quantity

        if color not in self.colors:
            self.colors.append(color)
        if size not in self.sizes:
            self.sizes.append(size)

        self.updated_at = datetime.now()

    def get_info(self) -> Dict[str, Any]:
        """获取商品信息"""
        total_stock = sum(self.stock_by_variant.values())
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "price": self.price,
            "brand": self.brand,
            "material": self.material,
            "colors": self.colors,
            "sizes": self.sizes,
            "gender": self.gender,
            "season": self.season,
            "total_stock": total_stock,
            "variants": len(self.stock_by_variant),
            "care_instructions": self.care_instructions,
            "is_active": self.is_active
        }


# ==================== 游戏开发：技能系统 ====================
class SkillType(Enum):
    """技能类型"""
    ACTIVE = "主动技能"
    PASSIVE = "被动技能"
    ULTIMATE = "终极技能"


class Skill(ABC):
    """技能原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆技能"""
        pass

    @abstractmethod
    def execute(self, caster, target=None) -> str:
        """执行技能"""
        pass


class ActiveSkill(Skill):
    """主动技能类"""

    def __init__(self, name: str = "主动技能"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.skill_type = SkillType.ACTIVE
        self.description = ""
        self.level = 1
        self.max_level = 10
        self.mana_cost = 10
        self.cooldown = 5.0  # 冷却时间（秒）
        self.cast_time = 1.0  # 施法时间（秒）
        self.range = 5.0  # 技能范围
        self.damage = 50
        self.effects = []  # 技能效果列表
        self.requirements = {}  # 学习要求
        self.icon = ""
        self.animation = ""
        self.sound_effect = ""
        self.created_at = datetime.now()

    def clone(self):
        """克隆主动技能"""
        new_skill = copy.copy(self)
        new_skill.id = str(uuid.uuid4())
        new_skill.created_at = datetime.now()
        # 深拷贝复杂对象
        new_skill.effects = copy.deepcopy(self.effects)
        new_skill.requirements = self.requirements.copy()
        return new_skill

    def add_effect(self, effect_type: str, value: float, duration: float = 0):
        """添加技能效果"""
        effect = {
            "type": effect_type,
            "value": value,
            "duration": duration
        }
        self.effects.append(effect)

    def level_up(self):
        """技能升级"""
        if self.level < self.max_level:
            self.level += 1
            # 升级时提升技能属性
            self.damage = int(self.damage * 1.1)
            self.mana_cost = int(self.mana_cost * 1.05)
            return True
        return False

    def execute(self, caster, target=None) -> str:
        """执行技能"""
        if target:
            return f"{caster} 对 {target} 使用了 {self.name}，造成 {self.damage} 点伤害！"
        else:
            return f"{caster} 使用了 {self.name}！"


class PassiveSkill(Skill):
    """被动技能类"""

    def __init__(self, name: str = "被动技能"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.skill_type = SkillType.PASSIVE
        self.description = ""
        self.level = 1
        self.max_level = 5
        self.stat_bonuses = {}  # 属性加成
        self.trigger_conditions = []  # 触发条件
        self.effects = []
        self.requirements = {}
        self.icon = ""
        self.created_at = datetime.now()

    def clone(self):
        """克隆被动技能"""
        new_skill = copy.copy(self)
        new_skill.id = str(uuid.uuid4())
        new_skill.created_at = datetime.now()
        # 深拷贝复杂对象
        new_skill.stat_bonuses = self.stat_bonuses.copy()
        new_skill.trigger_conditions = self.trigger_conditions.copy()
        new_skill.effects = copy.deepcopy(self.effects)
        new_skill.requirements = self.requirements.copy()
        return new_skill

    def add_stat_bonus(self, stat: str, bonus: float):
        """添加属性加成"""
        self.stat_bonuses[stat] = bonus

    def execute(self, caster, target=None) -> str:
        """执行技能（被动技能通常不主动执行）"""
        return f"{caster} 的被动技能 {self.name} 生效！"


# ==================== 产品工厂管理器 ====================
class ProductTemplateManager:
    """商品模板管理器"""

    def __init__(self):
        self._templates: Dict[str, Product] = {}
        self._initialize_templates()

    def _initialize_templates(self):
        """初始化商品模板"""
        # 电子产品模板
        smartphone_template = ElectronicsProduct("智能手机模板")
        smartphone_template.brand = "通用品牌"
        smartphone_template.warranty_months = 24
        smartphone_template.set_specifications({
            "屏幕尺寸": "6.1英寸",
            "存储容量": "128GB",
            "内存": "6GB",
            "摄像头": "双摄"
        })
        smartphone_template.add_certification("3C认证")
        smartphone_template.add_certification("入网许可")

        laptop_template = ElectronicsProduct("笔记本电脑模板")
        laptop_template.brand = "通用品牌"
        laptop_template.warranty_months = 36
        laptop_template.set_specifications({
            "屏幕尺寸": "14英寸",
            "处理器": "Intel i5",
            "内存": "8GB",
            "存储": "512GB SSD"
        })

        # 服装模板
        tshirt_template = ClothingProduct("T恤模板")
        tshirt_template.material = "100%棉"
        tshirt_template.season = "summer"
        tshirt_template.care_instructions = ["机洗", "低温烘干", "不可漂白"]
        tshirt_template.add_variant("白色", "M", 50)
        tshirt_template.add_variant("黑色", "L", 30)

        jeans_template = ClothingProduct("牛仔裤模板")
        jeans_template.material = "98%棉 2%弹性纤维"
        jeans_template.season = "all"
        jeans_template.care_instructions = ["机洗", "反面晾干", "不可漂白"]

        # 注册模板
        self.register_template("smartphone", smartphone_template)
        self.register_template("laptop", laptop_template)
        self.register_template("tshirt", tshirt_template)
        self.register_template("jeans", jeans_template)

    def register_template(self, name: str, template: Product):
        """注册商品模板"""
        self._templates[name] = template
        print(f"商品模板管理器: 已注册模板 '{name}'")

    def create_product(self, template_name: str, customizations: Dict[str, Any] = None) -> Product:
        """基于模板创建商品"""
        if template_name not in self._templates:
            raise ValueError(f"未找到模板 '{template_name}'")

        product = self._templates[template_name].clone()

        # 应用自定义设置
        if customizations:
            for key, value in customizations.items():
                if hasattr(product, key):
                    setattr(product, key, value)

        print(f"商品模板管理器: 基于 '{template_name}' 创建了商品 '{product.name}'")
        return product

    def list_templates(self) -> List[str]:
        """列出所有模板"""
        return list(self._templates.keys())


class SkillTemplateManager:
    """技能模板管理器"""

    def __init__(self):
        self._templates: Dict[str, Skill] = {}
        self._initialize_templates()

    def _initialize_templates(self):
        """初始化技能模板"""
        # 主动技能模板
        fireball_template = ActiveSkill("火球术模板")
        fireball_template.description = "发射一个火球攻击敌人"
        fireball_template.mana_cost = 15
        fireball_template.cooldown = 3.0
        fireball_template.damage = 80
        fireball_template.add_effect("火焰伤害", 10, 3.0)

        heal_template = ActiveSkill("治疗术模板")
        heal_template.description = "恢复目标的生命值"
        heal_template.mana_cost = 20
        heal_template.cooldown = 2.0
        heal_template.damage = -50  # 负数表示治疗
        heal_template.add_effect("治疗", 50, 0)

        # 被动技能模板
        strength_template = PassiveSkill("力量强化模板")
        strength_template.description = "永久增加攻击力"
        strength_template.add_stat_bonus("attack", 10)

        defense_template = PassiveSkill("防御强化模板")
        defense_template.description = "永久增加防御力"
        defense_template.add_stat_bonus("defense", 8)

        # 注册模板
        self.register_template("fireball", fireball_template)
        self.register_template("heal", heal_template)
        self.register_template("strength_boost", strength_template)
        self.register_template("defense_boost", defense_template)

    def register_template(self, name: str, template: Skill):
        """注册技能模板"""
        self._templates[name] = template
        print(f"技能模板管理器: 已注册模板 '{name}'")

    def create_skill(self, template_name: str, customizations: Dict[str, Any] = None) -> Skill:
        """基于模板创建技能"""
        if template_name not in self._templates:
            raise ValueError(f"未找到模板 '{template_name}'")

        skill = self._templates[template_name].clone()

        # 应用自定义设置
        if customizations:
            for key, value in customizations.items():
                if hasattr(skill, key):
                    setattr(skill, key, value)

        print(f"技能模板管理器: 基于 '{template_name}' 创建了技能 '{skill.name}'")
        return skill

    def list_templates(self) -> List[str]:
        """列出所有模板"""
        return list(self._templates.keys())


# ==================== 演示函数 ====================
def demonstrate_ecommerce_products():
    """演示电商商品系统"""
    print("=" * 50)
    print("电商商品系统演示")
    print("=" * 50)

    manager = ProductTemplateManager()

    print("可用的商品模板:")
    for template in manager.list_templates():
        print(f"- {template}")
    print()

    # 创建具体商品
    print("创建具体商品:")

    # 创建iPhone
    iphone = manager.create_product("smartphone", {
        "name": "iPhone 15 Pro",
        "brand": "Apple",
        "price": 7999.0,
        "stock_quantity": 100
    })

    # 创建MacBook
    macbook = manager.create_product("laptop", {
        "name": "MacBook Air M2",
        "brand": "Apple",
        "price": 8999.0,
        "stock_quantity": 50
    })

    # 创建T恤
    nike_tshirt = manager.create_product("tshirt", {
        "name": "Nike运动T恤",
        "brand": "Nike",
        "price": 199.0
    })

    products = [iphone, macbook, nike_tshirt]
    for product in products:
        print(f"\n商品: {product.name}")
        info = product.get_info()
        print(f"  ID: {info['id']}")
        print(f"  分类: {info['category']}")
        print(f"  品牌: {info.get('brand', 'N/A')}")
        print(f"  价格: ¥{info.get('price', 0)}")


def demonstrate_game_skills():
    """演示游戏技能系统"""
    print("\n" + "=" * 50)
    print("游戏技能系统演示")
    print("=" * 50)

    manager = SkillTemplateManager()

    print("可用的技能模板:")
    for template in manager.list_templates():
        print(f"- {template}")
    print()

    # 创建具体技能
    print("创建具体技能:")

    # 创建法师技能
    mage_fireball = manager.create_skill("fireball", {
        "name": "法师火球术",
        "damage": 120,
        "mana_cost": 25
    })

    # 创建牧师技能
    priest_heal = manager.create_skill("heal", {
        "name": "牧师治疗术",
        "damage": -80,  # 治疗80点
        "mana_cost": 30
    })

    # 创建战士被动技能
    warrior_strength = manager.create_skill("strength_boost", {
        "name": "战士力量",
        "level": 3
    })

    skills = [mage_fireball, priest_heal, warrior_strength]

    print("\n技能演示:")
    for skill in skills:
        print(f"\n技能: {skill.name}")
        print(f"  类型: {skill.skill_type.value}")
        print(f"  等级: {skill.level}")
        if hasattr(skill, 'damage'):
            print(f"  伤害/治疗: {skill.damage}")
        if hasattr(skill, 'mana_cost'):
            print(f"  法力消耗: {skill.mana_cost}")
        if hasattr(skill, 'stat_bonuses'):
            print(f"  属性加成: {skill.stat_bonuses}")

        # 演示技能执行
        if hasattr(skill, 'damage'):
            # 主动技能
            result = skill.execute("玩家", "敌人" if skill.damage > 0 else "队友")
        else:
            # 被动技能
            result = skill.execute("玩家")
        print(f"  执行结果: {result}")


def main():
    """主函数"""
    print("原型模式实际应用示例")

    demonstrate_ecommerce_products()
    demonstrate_game_skills()

    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
