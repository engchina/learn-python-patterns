"""
03_shopping_facade.py - 在线购物系统外观

这个示例展示了如何使用外观模式来简化复杂的电商系统。
电商系统包含用户管理、商品管理、订单处理、支付处理等多个子系统，
外观模式提供了统一的购物接口，简化了复杂的业务流程。
"""

from typing import Dict, List
from datetime import datetime
from enum import Enum
import uuid


class OrderStatus(Enum):
    """订单状态枚举"""
    PENDING = "待处理"
    CONFIRMED = "已确认"
    SHIPPED = "已发货"
    DELIVERED = "已送达"


class PaymentMethod(Enum):
    """支付方式枚举"""
    CREDIT_CARD = "信用卡"
    ALIPAY = "支付宝"
    WECHAT_PAY = "微信支付"


# ==================== 数据模型 ====================
class User:
    """用户模型"""
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.addresses = []


class Product:
    """商品模型"""
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class Order:
    """订单模型"""
    def __init__(self, order_id: str, user: User, items: List[Dict]):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.total_amount = sum(item["subtotal"] for item in items)
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()


# ==================== 子系统：用户管理 ====================
class UserManagementSystem:
    """用户管理子系统"""
    
    def __init__(self):
        self.users = {}
        self.current_user = None
    
    def register_user(self, name: str, email: str, password: str):
        """注册用户"""
        user_id = str(uuid.uuid4())[:8]
        user = User(user_id, name, email)
        self.users[user_id] = user
        return f"用户管理: 用户 '{name}' 注册成功，用户ID: {user_id}"
    
    def login_user(self, email: str, password: str):
        """用户登录"""
        for user in self.users.values():
            if user.email == email:
                self.current_user = user
                return f"用户管理: 用户 '{user.name}' 登录成功"
        return "用户管理: 登录失败，用户名或密码错误"
    
    def get_current_user(self):
        """获取当前用户"""
        return self.current_user


# ==================== 子系统：商品管理 ====================
class ProductManagementSystem:
    """商品管理子系统"""
    
    def __init__(self):
        self.products = {}
        self._init_sample_products()
    
    def _init_sample_products(self):
        """初始化示例商品"""
        sample_products = [
            ("P001", "iPhone 15 Pro", 7999.0, 50),
            ("P002", "MacBook Pro", 12999.0, 30),
            ("P003", "AirPods Pro", 1899.0, 100),
            ("P004", "iPad Air", 4399.0, 80)
        ]
        
        for product_id, name, price, stock in sample_products:
            self.products[product_id] = Product(product_id, name, price, stock)
    
    def search_products(self, keyword: str = ""):
        """搜索商品"""
        results = []
        for product in self.products.values():
            if not keyword or keyword.lower() in product.name.lower():
                results.append(product)
        
        return f"商品管理: 找到 {len(results)} 个商品", results
    
    def get_product(self, product_id: str):
        """获取商品详情"""
        if product_id in self.products:
            product = self.products[product_id]
            return f"商品管理: 获取商品 '{product.name}' 详情", product
        return "商品管理: 商品不存在", None
    
    def check_stock(self, product_id: str, quantity: int):
        """检查库存"""
        if product_id in self.products:
            product = self.products[product_id]
            if product.stock >= quantity:
                return f"商品管理: 商品 '{product.name}' 库存充足", True
            else:
                return f"商品管理: 商品 '{product.name}' 库存不足", False
        return "商品管理: 商品不存在", False


# ==================== 子系统：购物车管理 ====================
class ShoppingCartSystem:
    """购物车管理子系统"""
    
    def __init__(self):
        self.carts = {}  # user_id -> List[Dict]
    
    def add_to_cart(self, user_id: str, product: Product, quantity: int):
        """添加商品到购物车"""
        if user_id not in self.carts:
            self.carts[user_id] = []
        
        # 检查是否已存在该商品
        for item in self.carts[user_id]:
            if item["product"].product_id == product.product_id:
                item["quantity"] += quantity
                item["subtotal"] = item["product"].price * item["quantity"]
                return f"购物车: 已更新商品 '{product.name}' 数量为 {item['quantity']}"
        
        # 添加新商品
        cart_item = {
            "product": product,
            "quantity": quantity,
            "subtotal": product.price * quantity
        }
        self.carts[user_id].append(cart_item)
        return f"购物车: 已添加商品 '{product.name}' 数量: {quantity}"
    
    def get_cart_items(self, user_id: str):
        """获取购物车商品"""
        return self.carts.get(user_id, [])
    
    def get_cart_total(self, user_id: str):
        """获取购物车总金额"""
        items = self.get_cart_items(user_id)
        total = sum(item["subtotal"] for item in items)
        return f"购物车: 总金额 ¥{total:.2f}", total
    
    def clear_cart(self, user_id: str):
        """清空购物车"""
        if user_id in self.carts:
            self.carts[user_id] = []
            return "购物车: 购物车已清空"
        return "购物车: 购物车为空"


# ==================== 子系统：订单处理 ====================
class OrderProcessingSystem:
    """订单处理子系统"""
    
    def __init__(self):
        self.orders = {}
    
    def create_order(self, user: User, cart_items: List[Dict]):
        """创建订单"""
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = Order(order_id, user, cart_items)
        self.orders[order_id] = order
        return f"订单处理: 订单 {order_id} 创建成功，总金额 ¥{order.total_amount:.2f}", order
    
    def confirm_order(self, order_id: str):
        """确认订单"""
        if order_id in self.orders:
            order = self.orders[order_id]
            order.status = OrderStatus.CONFIRMED
            return f"订单处理: 订单 {order_id} 已确认"
        return "订单处理: 订单不存在"
    
    def get_order(self, order_id: str):
        """获取订单详情"""
        return self.orders.get(order_id)


# ==================== 子系统：支付处理 ====================
class PaymentProcessingSystem:
    """支付处理子系统"""
    
    def __init__(self):
        self.payments = {}
    
    def process_payment(self, order_id: str, amount: float, method: PaymentMethod):
        """处理支付"""
        payment_id = f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 模拟支付处理（这里总是成功）
        payment_info = {
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": amount,
            "method": method.value,
            "status": "成功",
            "processed_at": datetime.now()
        }
        
        self.payments[payment_id] = payment_info
        return f"支付处理: 支付成功，支付ID: {payment_id}", payment_info


# ==================== 外观类：在线购物系统 ====================
class OnlineShoppingFacade:
    """在线购物系统外观类
    
    提供简化的接口来处理复杂的电商业务流程，
    将用户管理、商品管理、购物车、订单、支付等子系统整合起来。
    """
    
    def __init__(self):
        # 初始化所有子系统
        self.user_system = UserManagementSystem()
        self.product_system = ProductManagementSystem()
        self.cart_system = ShoppingCartSystem()
        self.order_system = OrderProcessingSystem()
        self.payment_system = PaymentProcessingSystem()
    
    def register_and_login(self, name: str, email: str, password: str):
        """注册并登录用户"""
        print(f"👤 用户注册和登录: {name}")
        
        actions = [
            self.user_system.register_user(name, email, password),
            self.user_system.login_user(email, password)
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
        
        return self.user_system.get_current_user()
    
    def browse_and_add_to_cart(self, search_keyword: str = "", quantity: int = 1):
        """浏览商品并添加到购物车"""
        current_user = self.user_system.get_current_user()
        if not current_user:
            print("⚠️ 请先登录")
            return
        
        print(f"🛍️ 浏览商品: {search_keyword}")
        
        # 搜索商品
        search_msg, products = self.product_system.search_products(search_keyword)
        print(f"  ✓ {search_msg}")
        
        if products:
            # 选择第一个商品添加到购物车
            product = products[0]
            
            # 检查库存
            stock_msg, stock_available = self.product_system.check_stock(
                product.product_id, quantity)
            print(f"  ✓ {stock_msg}")
            
            if stock_available:
                # 添加到购物车
                cart_msg = self.cart_system.add_to_cart(
                    current_user.user_id, product, quantity)
                print(f"  ✓ {cart_msg}")
                return product
        
        return None
    
    def checkout_and_pay(self, shipping_address: str, payment_method: PaymentMethod):
        """结账并支付"""
        current_user = self.user_system.get_current_user()
        if not current_user:
            print("⚠️ 请先登录")
            return None
        
        print("🛒 开始结账流程...")
        
        # 获取购物车商品
        cart_items = self.cart_system.get_cart_items(current_user.user_id)
        if not cart_items:
            print("  ⚠️ 购物车为空")
            return None
        
        # 显示购物车总金额
        total_msg, total_amount = self.cart_system.get_cart_total(current_user.user_id)
        print(f"  ✓ {total_msg}")
        
        # 创建订单
        order_msg, order = self.order_system.create_order(current_user, cart_items)
        print(f"  ✓ {order_msg}")
        
        # 处理支付
        payment_msg, payment_info = self.payment_system.process_payment(
            order.order_id, total_amount, payment_method)
        print(f"  ✓ {payment_msg}")
        
        # 确认订单
        confirm_msg = self.order_system.confirm_order(order.order_id)
        print(f"  ✓ {confirm_msg}")
        
        # 清空购物车
        clear_msg = self.cart_system.clear_cart(current_user.user_id)
        print(f"  ✓ {clear_msg}")
        
        print(f"🎉 购买成功！订单号: {order.order_id}")
        return order
    
    def quick_purchase(self, user_info: Dict, product_keyword: str, quantity: int,
                      shipping_address: str, payment_method: PaymentMethod):
        """快速购买流程"""
        print("🚀 启动快速购买流程")
        print("="*50)
        
        # 1. 注册并登录
        user = self.register_and_login(
            user_info["name"], user_info["email"], user_info["password"]
        )
        
        print("\n" + "-"*30)
        
        # 2. 浏览并添加到购物车
        product = self.browse_and_add_to_cart(product_keyword, quantity)
        
        if product:
            print("\n" + "-"*30)
            
            # 3. 结账
            order = self.checkout_and_pay(shipping_address, payment_method)
            return order
        
        return None


# ==================== 使用示例 ====================
def demo_shopping_facade():
    """在线购物外观模式演示"""
    print("=" * 60)
    print("🛒 在线购物系统演示 - 外观模式应用")
    print("=" * 60)
    
    # 创建购物系统
    shopping_system = OnlineShoppingFacade()
    
    # 用户信息
    user_info = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "password": "password123"
    }
    
    # 执行快速购买流程
    order = shopping_system.quick_purchase(
        user_info=user_info,
        product_keyword="iPhone",
        quantity=1,
        shipping_address="北京市朝阳区某某街道123号",
        payment_method=PaymentMethod.ALIPAY
    )
    
    print("\n" + "="*60)
    if order:
        print("🎯 演示完成！外观模式成功简化了复杂的电商购物流程！")
    else:
        print("❌ 购买流程未完成")
    print("="*60)


if __name__ == "__main__":
    demo_shopping_facade()
