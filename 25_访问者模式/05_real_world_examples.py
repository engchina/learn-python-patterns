"""
05_real_world_examples.py - 实际项目中的访问者应用

这个示例展示了访问者模式在实际开发中的常见应用：
- 数据验证系统
- 业务规则引擎
- 配置文件处理
- 系统监控和分析
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import re


class ValidationLevel(Enum):
    """验证级别"""
    INFO = "信息"
    WARNING = "警告"
    ERROR = "错误"
    CRITICAL = "严重错误"


# ==================== 数据验证系统 ====================
class ValidationVisitor(ABC):
    """数据验证访问者抽象类"""
    
    @abstractmethod
    def visit_user_data(self, user_data):
        """验证用户数据"""
        pass
    
    @abstractmethod
    def visit_order_data(self, order_data):
        """验证订单数据"""
        pass
    
    @abstractmethod
    def visit_product_data(self, product_data):
        """验证产品数据"""
        pass
    
    @abstractmethod
    def visit_payment_data(self, payment_data):
        """验证支付数据"""
        pass


class DataElement(ABC):
    """数据元素抽象类"""
    
    def __init__(self, data_id: str, data: Dict[str, Any]):
        self.data_id = data_id
        self.data = data
        self.created_at = datetime.now()
    
    @abstractmethod
    def accept(self, visitor: ValidationVisitor):
        """接受访问者"""
        pass


class UserData(DataElement):
    """用户数据"""
    
    def __init__(self, user_id: str, user_info: Dict[str, Any]):
        super().__init__(user_id, user_info)
        self.username = user_info.get('username', '')
        self.email = user_info.get('email', '')
        self.age = user_info.get('age', 0)
        self.phone = user_info.get('phone', '')
    
    def accept(self, visitor: ValidationVisitor):
        visitor.visit_user_data(self)
    
    def __str__(self):
        return f"用户数据: {self.username} ({self.data_id})"


class OrderData(DataElement):
    """订单数据"""
    
    def __init__(self, order_id: str, order_info: Dict[str, Any]):
        super().__init__(order_id, order_info)
        self.customer_id = order_info.get('customer_id', '')
        self.total_amount = order_info.get('total_amount', 0.0)
        self.items = order_info.get('items', [])
        self.status = order_info.get('status', 'pending')
    
    def accept(self, visitor: ValidationVisitor):
        visitor.visit_order_data(self)
    
    def __str__(self):
        return f"订单数据: {self.data_id} (¥{self.total_amount})"


class ProductData(DataElement):
    """产品数据"""
    
    def __init__(self, product_id: str, product_info: Dict[str, Any]):
        super().__init__(product_id, product_info)
        self.name = product_info.get('name', '')
        self.price = product_info.get('price', 0.0)
        self.stock = product_info.get('stock', 0)
        self.category = product_info.get('category', '')
    
    def accept(self, visitor: ValidationVisitor):
        visitor.visit_product_data(self)
    
    def __str__(self):
        return f"产品数据: {self.name} ({self.data_id})"


class PaymentData(DataElement):
    """支付数据"""
    
    def __init__(self, payment_id: str, payment_info: Dict[str, Any]):
        super().__init__(payment_id, payment_info)
        self.order_id = payment_info.get('order_id', '')
        self.amount = payment_info.get('amount', 0.0)
        self.method = payment_info.get('method', '')
        self.card_number = payment_info.get('card_number', '')
    
    def accept(self, visitor: ValidationVisitor):
        visitor.visit_payment_data(self)
    
    def __str__(self):
        return f"支付数据: {self.data_id} (¥{self.amount})"


# ==================== 具体验证访问者 ====================
class BasicValidationVisitor(ValidationVisitor):
    """基础数据验证访问者"""
    
    def __init__(self):
        self.validation_results: List[Dict[str, Any]] = []
        self.error_count = 0
        self.warning_count = 0
    
    def _add_result(self, level: ValidationLevel, message: str, data_id: str, field: str = ""):
        """添加验证结果"""
        result = {
            "level": level,
            "message": message,
            "data_id": data_id,
            "field": field,
            "timestamp": datetime.now()
        }
        self.validation_results.append(result)
        
        if level == ValidationLevel.ERROR or level == ValidationLevel.CRITICAL:
            self.error_count += 1
        elif level == ValidationLevel.WARNING:
            self.warning_count += 1
        
        print(f"🔍 {level.value}: {message} (ID: {data_id})")
    
    def visit_user_data(self, user_data: UserData):
        """验证用户数据"""
        print(f"👤 验证用户数据: {user_data.username}")
        
        # 验证用户名
        if not user_data.username:
            self._add_result(ValidationLevel.ERROR, "用户名不能为空", user_data.data_id, "username")
        elif len(user_data.username) < 3:
            self._add_result(ValidationLevel.WARNING, "用户名长度建议至少3个字符", user_data.data_id, "username")
        
        # 验证邮箱
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not user_data.email:
            self._add_result(ValidationLevel.ERROR, "邮箱不能为空", user_data.data_id, "email")
        elif not re.match(email_pattern, user_data.email):
            self._add_result(ValidationLevel.ERROR, "邮箱格式不正确", user_data.data_id, "email")
        
        # 验证年龄
        if user_data.age <= 0:
            self._add_result(ValidationLevel.ERROR, "年龄必须大于0", user_data.data_id, "age")
        elif user_data.age > 120:
            self._add_result(ValidationLevel.WARNING, "年龄似乎不合理", user_data.data_id, "age")
        
        # 验证手机号
        phone_pattern = r'^1[3-9]\d{9}$'
        if user_data.phone and not re.match(phone_pattern, user_data.phone):
            self._add_result(ValidationLevel.WARNING, "手机号格式可能不正确", user_data.data_id, "phone")
    
    def visit_order_data(self, order_data: OrderData):
        """验证订单数据"""
        print(f"📦 验证订单数据: {order_data.data_id}")
        
        # 验证客户ID
        if not order_data.customer_id:
            self._add_result(ValidationLevel.ERROR, "客户ID不能为空", order_data.data_id, "customer_id")
        
        # 验证订单金额
        if order_data.total_amount <= 0:
            self._add_result(ValidationLevel.ERROR, "订单金额必须大于0", order_data.data_id, "total_amount")
        elif order_data.total_amount > 100000:
            self._add_result(ValidationLevel.WARNING, "订单金额异常高", order_data.data_id, "total_amount")
        
        # 验证订单项
        if not order_data.items:
            self._add_result(ValidationLevel.ERROR, "订单必须包含商品", order_data.data_id, "items")
        elif len(order_data.items) > 50:
            self._add_result(ValidationLevel.WARNING, "订单商品数量过多", order_data.data_id, "items")
        
        # 验证订单状态
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if order_data.status not in valid_statuses:
            self._add_result(ValidationLevel.ERROR, f"无效的订单状态: {order_data.status}", order_data.data_id, "status")
    
    def visit_product_data(self, product_data: ProductData):
        """验证产品数据"""
        print(f"🛍️  验证产品数据: {product_data.name}")
        
        # 验证产品名称
        if not product_data.name:
            self._add_result(ValidationLevel.ERROR, "产品名称不能为空", product_data.data_id, "name")
        elif len(product_data.name) > 100:
            self._add_result(ValidationLevel.WARNING, "产品名称过长", product_data.data_id, "name")
        
        # 验证价格
        if product_data.price <= 0:
            self._add_result(ValidationLevel.ERROR, "产品价格必须大于0", product_data.data_id, "price")
        elif product_data.price > 50000:
            self._add_result(ValidationLevel.WARNING, "产品价格异常高", product_data.data_id, "price")
        
        # 验证库存
        if product_data.stock < 0:
            self._add_result(ValidationLevel.ERROR, "库存不能为负数", product_data.data_id, "stock")
        elif product_data.stock == 0:
            self._add_result(ValidationLevel.WARNING, "产品库存为0", product_data.data_id, "stock")
        
        # 验证分类
        if not product_data.category:
            self._add_result(ValidationLevel.WARNING, "建议设置产品分类", product_data.data_id, "category")
    
    def visit_payment_data(self, payment_data: PaymentData):
        """验证支付数据"""
        print(f"💳 验证支付数据: {payment_data.data_id}")
        
        # 验证订单ID
        if not payment_data.order_id:
            self._add_result(ValidationLevel.ERROR, "订单ID不能为空", payment_data.data_id, "order_id")
        
        # 验证支付金额
        if payment_data.amount <= 0:
            self._add_result(ValidationLevel.ERROR, "支付金额必须大于0", payment_data.data_id, "amount")
        
        # 验证支付方式
        valid_methods = ['credit_card', 'debit_card', 'paypal', 'alipay', 'wechat_pay']
        if payment_data.method not in valid_methods:
            self._add_result(ValidationLevel.ERROR, f"不支持的支付方式: {payment_data.method}", payment_data.data_id, "method")
        
        # 验证卡号（如果是信用卡支付）
        if payment_data.method in ['credit_card', 'debit_card']:
            if not payment_data.card_number:
                self._add_result(ValidationLevel.ERROR, "卡号不能为空", payment_data.data_id, "card_number")
            elif len(payment_data.card_number) < 13 or len(payment_data.card_number) > 19:
                self._add_result(ValidationLevel.ERROR, "卡号长度不正确", payment_data.data_id, "card_number")
    
    def get_validation_report(self) -> str:
        """获取验证报告"""
        report = [f"数据验证报告 (共验证 {len(self.validation_results)} 项)"]
        report.append(f"错误: {self.error_count} 个")
        report.append(f"警告: {self.warning_count} 个")
        report.append("")
        
        # 按级别分组显示
        for level in [ValidationLevel.CRITICAL, ValidationLevel.ERROR, ValidationLevel.WARNING, ValidationLevel.INFO]:
            level_results = [r for r in self.validation_results if r['level'] == level]
            if level_results:
                report.append(f"{level.value} ({len(level_results)} 个):")
                for result in level_results[:5]:  # 只显示前5个
                    report.append(f"  - {result['message']} (ID: {result['data_id']})")
                if len(level_results) > 5:
                    report.append(f"  ... 还有 {len(level_results) - 5} 个")
                report.append("")
        
        return "\n".join(report)


class SecurityValidationVisitor(ValidationVisitor):
    """安全验证访问者"""
    
    def __init__(self):
        self.security_issues: List[Dict[str, Any]] = []
        self.risk_score = 0
    
    def _add_security_issue(self, severity: str, message: str, data_id: str, risk_points: int = 1):
        """添加安全问题"""
        issue = {
            "severity": severity,
            "message": message,
            "data_id": data_id,
            "risk_points": risk_points,
            "timestamp": datetime.now()
        }
        self.security_issues.append(issue)
        self.risk_score += risk_points
        print(f"🔒 安全检查 - {severity}: {message} (ID: {data_id})")
    
    def visit_user_data(self, user_data: UserData):
        """安全验证用户数据"""
        print(f"🔒 安全检查用户数据: {user_data.username}")
        
        # 检查用户名是否包含敏感词
        sensitive_words = ['admin', 'root', 'system', 'test']
        if any(word in user_data.username.lower() for word in sensitive_words):
            self._add_security_issue("高", f"用户名包含敏感词: {user_data.username}", user_data.data_id, 3)
        
        # 检查邮箱域名
        if user_data.email:
            domain = user_data.email.split('@')[-1] if '@' in user_data.email else ''
            suspicious_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
            if domain in suspicious_domains:
                self._add_security_issue("中", f"使用临时邮箱域名: {domain}", user_data.data_id, 2)
    
    def visit_order_data(self, order_data: OrderData):
        """安全验证订单数据"""
        print(f"🔒 安全检查订单数据: {order_data.data_id}")
        
        # 检查异常大额订单
        if order_data.total_amount > 50000:
            self._add_security_issue("高", f"大额订单需要审核: ¥{order_data.total_amount}", order_data.data_id, 3)
        
        # 检查订单项数量异常
        if len(order_data.items) > 20:
            self._add_security_issue("中", f"订单商品数量异常: {len(order_data.items)} 个", order_data.data_id, 2)
    
    def visit_product_data(self, product_data: ProductData):
        """安全验证产品数据"""
        print(f"🔒 安全检查产品数据: {product_data.name}")
        
        # 检查产品名称是否包含违禁词
        prohibited_words = ['假货', '盗版', '违法', '欺诈']
        if any(word in product_data.name for word in prohibited_words):
            self._add_security_issue("严重", f"产品名称包含违禁词: {product_data.name}", product_data.data_id, 5)
    
    def visit_payment_data(self, payment_data: PaymentData):
        """安全验证支付数据"""
        print(f"🔒 安全检查支付数据: {payment_data.data_id}")
        
        # 检查大额支付
        if payment_data.amount > 10000:
            self._add_security_issue("高", f"大额支付需要额外验证: ¥{payment_data.amount}", payment_data.data_id, 3)
        
        # 检查卡号格式（简单检查）
        if payment_data.card_number and payment_data.method in ['credit_card', 'debit_card']:
            if not payment_data.card_number.replace(' ', '').isdigit():
                self._add_security_issue("高", "卡号格式异常", payment_data.data_id, 3)
    
    def get_security_report(self) -> str:
        """获取安全报告"""
        report = [f"安全验证报告"]
        report.append(f"风险评分: {self.risk_score} 分")
        report.append(f"发现问题: {len(self.security_issues)} 个")
        report.append("")
        
        # 按严重程度分组
        severity_groups = {}
        for issue in self.security_issues:
            severity = issue['severity']
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(issue)
        
        for severity in ['严重', '高', '中', '低']:
            if severity in severity_groups:
                issues = severity_groups[severity]
                report.append(f"{severity}风险 ({len(issues)} 个):")
                for issue in issues[:3]:  # 只显示前3个
                    report.append(f"  - {issue['message']} (ID: {issue['data_id']})")
                if len(issues) > 3:
                    report.append(f"  ... 还有 {len(issues) - 3} 个")
                report.append("")
        
        return "\n".join(report)


# ==================== 演示函数 ====================
def create_sample_data() -> List[DataElement]:
    """创建示例数据"""
    print("🏗️  创建示例数据...")
    
    data_elements = []
    
    # 用户数据
    users = [
        {"username": "john_doe", "email": "john@example.com", "age": 28, "phone": "13812345678"},
        {"username": "admin", "email": "admin@tempmail.com", "age": 0, "phone": "invalid"},  # 有问题的数据
        {"username": "alice", "email": "alice@company.com", "age": 32, "phone": "13987654321"},
        {"username": "test_user", "email": "invalid-email", "age": 150, "phone": ""}  # 有问题的数据
    ]
    
    for i, user_info in enumerate(users, 1):
        data_elements.append(UserData(f"user_{i:03d}", user_info))
    
    # 订单数据
    orders = [
        {"customer_id": "user_001", "total_amount": 299.99, "items": ["item1", "item2"], "status": "confirmed"},
        {"customer_id": "", "total_amount": 0, "items": [], "status": "invalid"},  # 有问题的数据
        {"customer_id": "user_003", "total_amount": 75000, "items": ["expensive_item"], "status": "pending"},  # 大额订单
        {"customer_id": "user_002", "total_amount": 150.50, "items": ["item3", "item4", "item5"], "status": "shipped"}
    ]
    
    for i, order_info in enumerate(orders, 1):
        data_elements.append(OrderData(f"order_{i:03d}", order_info))
    
    # 产品数据
    products = [
        {"name": "笔记本电脑", "price": 5999.00, "stock": 10, "category": "电子产品"},
        {"name": "", "price": 0, "stock": -5, "category": ""},  # 有问题的数据
        {"name": "假货手机", "price": 100000, "stock": 0, "category": "电子产品"},  # 违禁词和异常价格
        {"name": "办公椅", "price": 299.99, "stock": 25, "category": "家具"}
    ]
    
    for i, product_info in enumerate(products, 1):
        data_elements.append(ProductData(f"product_{i:03d}", product_info))
    
    # 支付数据
    payments = [
        {"order_id": "order_001", "amount": 299.99, "method": "credit_card", "card_number": "4111111111111111"},
        {"order_id": "", "amount": 0, "method": "invalid_method", "card_number": ""},  # 有问题的数据
        {"order_id": "order_003", "amount": 75000, "method": "credit_card", "card_number": "4222222222222222"},  # 大额支付
        {"order_id": "order_004", "amount": 150.50, "method": "alipay", "card_number": ""}
    ]
    
    for i, payment_info in enumerate(payments, 1):
        data_elements.append(PaymentData(f"payment_{i:03d}", payment_info))
    
    print(f"✅ 创建了 {len(data_elements)} 个数据元素")
    return data_elements


def demo_validation_system():
    """数据验证系统演示"""
    print("=" * 80)
    print("🔍 数据验证系统访问者演示")
    print("=" * 80)
    
    # 创建示例数据
    data_elements = create_sample_data()
    
    # 创建不同的验证访问者
    validators = [
        ("基础验证器", BasicValidationVisitor()),
        ("安全验证器", SecurityValidationVisitor())
    ]
    
    # 使用不同验证器处理数据
    for name, validator in validators:
        print(f"\n{'='*20} {name} {'='*20}")
        
        for data_element in data_elements:
            data_element.accept(validator)
        
        # 显示验证结果
        if isinstance(validator, BasicValidationVisitor):
            print(f"\n📊 基础验证报告:")
            print("-" * 50)
            print(validator.get_validation_report())
        
        elif isinstance(validator, SecurityValidationVisitor):
            print(f"\n🔒 安全验证报告:")
            print("-" * 50)
            print(validator.get_security_report())
    
    print("\n" + "=" * 80)
    print("🎉 数据验证系统演示完成!")
    print("💡 关键点:")
    print("   - 访问者模式使得验证逻辑与数据结构分离")
    print("   - 可以轻松添加新的验证规则而不修改数据类")
    print("   - 不同类型的验证器可以并行工作")
    print("   - 验证结果可以统一收集和分析")
    print("=" * 80)


if __name__ == "__main__":
    demo_validation_system()
