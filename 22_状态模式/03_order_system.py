"""
03_order_system.py - 订单系统状态管理

这个示例展示了在业务系统中使用状态模式管理复杂的业务流程。
演示了订单生命周期、状态转换规则、异常处理等实际应用场景。
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid


# ==================== 枚举定义 ====================

class PaymentMethod(Enum):
    """支付方式"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"


class OrderType(Enum):
    """订单类型"""
    REGULAR = "regular"
    EXPRESS = "express"
    BULK = "bulk"
    DIGITAL = "digital"


# ==================== 抽象状态接口 ====================

class OrderState(ABC):
    """订单状态抽象类"""
    
    @abstractmethod
    def get_state_name(self) -> str:
        """获取状态名称"""
        pass
    
    @abstractmethod
    def can_cancel(self) -> bool:
        """是否可以取消"""
        pass
    
    @abstractmethod
    def can_modify(self) -> bool:
        """是否可以修改"""
        pass
    
    @abstractmethod
    def can_pay(self) -> bool:
        """是否可以支付"""
        pass
    
    @abstractmethod
    def get_allowed_actions(self) -> List[str]:
        """获取允许的操作"""
        pass
    
    @abstractmethod
    def handle_action(self, order: 'Order', action: str, **kwargs) -> bool:
        """处理操作"""
        pass


# ==================== 订单实体类 ====================

class OrderItem:
    """订单项"""
    
    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def total_price(self) -> float:
        return self.price * self.quantity
    
    def __str__(self) -> str:
        return f"{self.name} x{self.quantity} @ ¥{self.price:.2f}"


class Order:
    """订单类"""
    
    def __init__(self, customer_id: str, order_type: OrderType = OrderType.REGULAR):
        self.order_id = str(uuid.uuid4())[:8]
        self.customer_id = customer_id
        self.order_type = order_type
        self.items: List[OrderItem] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # 状态相关
        self._state: OrderState = PendingState()
        self._state_history: List[Dict[str, Any]] = []
        
        # 支付相关
        self.payment_method: Optional[PaymentMethod] = None
        self.payment_id: Optional[str] = None
        self.paid_amount: float = 0.0
        
        # 配送相关
        self.shipping_address: Optional[str] = None
        self.tracking_number: Optional[str] = None
        self.estimated_delivery: Optional[datetime] = None
        
        # 其他信息
        self.notes: str = ""
        self.discount_amount: float = 0.0
        
        self._record_state_change("订单创建")
        print(f"📦 订单创建: {self.order_id} (客户: {customer_id})")
    
    def set_state(self, new_state: OrderState, reason: str = "") -> None:
        """设置新状态"""
        old_state = self._state.get_state_name()
        self._state = new_state
        new_state_name = self._state.get_state_name()
        self.updated_at = datetime.now()
        
        self._record_state_change(reason or f"状态转换: {old_state} → {new_state_name}")
        print(f"🔄 订单 {self.order_id}: {old_state} → {new_state_name}")
    
    def _record_state_change(self, reason: str) -> None:
        """记录状态变化"""
        self._state_history.append({
            'state': self._state.get_state_name(),
            'timestamp': datetime.now(),
            'reason': reason
        })
    
    @property
    def current_state(self) -> OrderState:
        return self._state
    
    @property
    def state_name(self) -> str:
        return self._state.get_state_name()
    
    @property
    def total_amount(self) -> float:
        """订单总金额"""
        subtotal = sum(item.total_price for item in self.items)
        return max(0, subtotal - self.discount_amount)
    
    def add_item(self, item: OrderItem) -> bool:
        """添加订单项"""
        if not self._state.can_modify():
            print(f"❌ 订单 {self.order_id} 当前状态不允许修改")
            return False
        
        self.items.append(item)
        self.updated_at = datetime.now()
        print(f"➕ 添加商品: {item}")
        return True
    
    def remove_item(self, product_id: str) -> bool:
        """移除订单项"""
        if not self._state.can_modify():
            print(f"❌ 订单 {self.order_id} 当前状态不允许修改")
            return False
        
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                removed_item = self.items.pop(i)
                self.updated_at = datetime.now()
                print(f"➖ 移除商品: {removed_item}")
                return True
        
        print(f"❌ 未找到商品: {product_id}")
        return False
    
    def execute_action(self, action: str, **kwargs) -> bool:
        """执行操作"""
        if action not in self._state.get_allowed_actions():
            print(f"❌ 当前状态 '{self.state_name}' 不允许操作 '{action}'")
            return False
        
        return self._state.handle_action(self, action, **kwargs)
    
    def get_state_history(self) -> List[Dict[str, Any]]:
        """获取状态历史"""
        return self._state_history.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """获取订单摘要"""
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'state': self.state_name,
            'total_amount': self.total_amount,
            'item_count': len(self.items),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# ==================== 具体状态类 ====================

class PendingState(OrderState):
    """待处理状态"""
    
    def get_state_name(self) -> str:
        return "待处理"
    
    def can_cancel(self) -> bool:
        return True
    
    def can_modify(self) -> bool:
        return True
    
    def can_pay(self) -> bool:
        return True
    
    def get_allowed_actions(self) -> List[str]:
        return ["confirm", "cancel", "add_item", "remove_item", "set_address"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "confirm":
            if not order.items:
                print("❌ 订单为空，无法确认")
                return False
            if not order.shipping_address:
                print("❌ 请先设置配送地址")
                return False
            
            order.set_state(ConfirmedState(), "订单确认")
            return True
        
        elif action == "cancel":
            order.set_state(CancelledState(), "用户取消订单")
            return True
        
        elif action == "set_address":
            address = kwargs.get("address")
            if address:
                order.shipping_address = address
                print(f"📍 设置配送地址: {address}")
                return True
            return False
        
        return False


class ConfirmedState(OrderState):
    """已确认状态"""
    
    def get_state_name(self) -> str:
        return "已确认"
    
    def can_cancel(self) -> bool:
        return True
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return True
    
    def get_allowed_actions(self) -> List[str]:
        return ["pay", "cancel"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "pay":
            payment_method = kwargs.get("payment_method")
            amount = kwargs.get("amount", order.total_amount)
            
            if not payment_method:
                print("❌ 请选择支付方式")
                return False
            
            if amount < order.total_amount:
                print("❌ 支付金额不足")
                return False
            
            order.payment_method = payment_method
            order.paid_amount = amount
            order.payment_id = f"PAY_{uuid.uuid4().hex[:8]}"
            
            print(f"💳 支付成功: ¥{amount:.2f} ({payment_method.value})")
            order.set_state(PaidState(), "支付完成")
            return True
        
        elif action == "cancel":
            order.set_state(CancelledState(), "确认后取消订单")
            return True
        
        return False


class PaidState(OrderState):
    """已支付状态"""
    
    def get_state_name(self) -> str:
        return "已支付"
    
    def can_cancel(self) -> bool:
        return True  # 可以取消但需要退款
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return ["ship", "cancel_with_refund"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "ship":
            tracking_number = kwargs.get("tracking_number", f"TN{uuid.uuid4().hex[:8]}")
            estimated_days = 3 if order.order_type == OrderType.EXPRESS else 7
            
            order.tracking_number = tracking_number
            order.estimated_delivery = datetime.now() + timedelta(days=estimated_days)
            
            print(f"🚚 订单发货: {tracking_number}")
            print(f"📅 预计送达: {order.estimated_delivery.strftime('%Y-%m-%d')}")
            
            order.set_state(ShippedState(), "订单发货")
            return True
        
        elif action == "cancel_with_refund":
            print(f"💰 退款处理: ¥{order.paid_amount:.2f}")
            order.set_state(RefundedState(), "取消订单并退款")
            return True
        
        return False


class ShippedState(OrderState):
    """已发货状态"""
    
    def get_state_name(self) -> str:
        return "已发货"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return ["deliver", "return_request"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "deliver":
            print(f"📦 订单送达: {order.tracking_number}")
            order.set_state(DeliveredState(), "订单送达")
            return True
        
        elif action == "return_request":
            reason = kwargs.get("reason", "客户要求退货")
            print(f"↩️ 退货申请: {reason}")
            order.set_state(ReturningState(), f"退货申请: {reason}")
            return True
        
        return False


class DeliveredState(OrderState):
    """已送达状态"""
    
    def get_state_name(self) -> str:
        return "已送达"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return ["complete", "return_request"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "complete":
            print("✅ 订单完成")
            order.set_state(CompletedState(), "订单完成")
            return True
        
        elif action == "return_request":
            # 送达后7天内可以申请退货
            if datetime.now() - order.updated_at > timedelta(days=7):
                print("❌ 超过退货期限")
                return False
            
            reason = kwargs.get("reason", "客户要求退货")
            print(f"↩️ 退货申请: {reason}")
            order.set_state(ReturningState(), f"退货申请: {reason}")
            return True
        
        return False


class CompletedState(OrderState):
    """已完成状态"""
    
    def get_state_name(self) -> str:
        return "已完成"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return []  # 完成状态不允许任何操作
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        print("❌ 订单已完成，不允许任何操作")
        return False


class CancelledState(OrderState):
    """已取消状态"""
    
    def get_state_name(self) -> str:
        return "已取消"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return []
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        print("❌ 订单已取消，不允许任何操作")
        return False


class RefundedState(OrderState):
    """已退款状态"""
    
    def get_state_name(self) -> str:
        return "已退款"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return []
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        print("❌ 订单已退款，不允许任何操作")
        return False


class ReturningState(OrderState):
    """退货中状态"""
    
    def get_state_name(self) -> str:
        return "退货中"
    
    def can_cancel(self) -> bool:
        return False
    
    def can_modify(self) -> bool:
        return False
    
    def can_pay(self) -> bool:
        return False
    
    def get_allowed_actions(self) -> List[str]:
        return ["approve_return", "reject_return"]
    
    def handle_action(self, order: Order, action: str, **kwargs) -> bool:
        if action == "approve_return":
            print("✅ 退货申请通过")
            order.set_state(RefundedState(), "退货申请通过，处理退款")
            return True
        
        elif action == "reject_return":
            reason = kwargs.get("reason", "不符合退货条件")
            print(f"❌ 退货申请被拒绝: {reason}")
            order.set_state(DeliveredState(), f"退货被拒绝: {reason}")
            return True
        
        return False


# ==================== 演示函数 ====================

def demo_normal_order_flow():
    """正常订单流程演示"""
    print("=" * 60)
    print("📦 订单系统状态管理演示 - 正常流程")
    print("=" * 60)
    
    # 创建订单
    order = Order("customer_001", OrderType.REGULAR)
    
    # 添加商品
    order.add_item(OrderItem("P001", "iPhone 15", 6999.0, 1))
    order.add_item(OrderItem("P002", "保护壳", 99.0, 1))
    
    print(f"\n💰 订单总金额: ¥{order.total_amount:.2f}")
    
    # 设置配送地址
    order.execute_action("set_address", address="北京市朝阳区xxx街道xxx号")
    
    # 确认订单
    order.execute_action("confirm")
    
    # 支付订单
    order.execute_action("pay", 
                        payment_method=PaymentMethod.CREDIT_CARD, 
                        amount=order.total_amount)
    
    # 发货
    order.execute_action("ship", tracking_number="SF1234567890")
    
    # 送达
    order.execute_action("deliver")
    
    # 完成订单
    order.execute_action("complete")
    
    print(f"\n📋 订单摘要: {order.get_summary()}")


if __name__ == "__main__":
    demo_normal_order_flow()
    
    print("\n" + "=" * 60)
    print("✅ 订单系统演示完成")
    print("💡 学习要点:")
    print("   - 复杂业务流程的状态管理")
    print("   - 状态转换的业务规则")
    print("   - 状态对操作权限的控制")
    print("   - 异常情况的处理机制")
    print("=" * 60)
