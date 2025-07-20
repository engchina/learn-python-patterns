"""
适配器模式第三方集成 - 支付系统适配器

这个示例展示了适配器模式在第三方库集成中的应用，演示如何
统一不同支付服务提供商的接口。

作者: Adapter Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
from datetime import datetime
from enum import Enum


class PaymentStatus(Enum):
    """支付状态枚举"""
    PENDING = "待处理"
    SUCCESS = "成功"
    FAILED = "失败"
    CANCELLED = "已取消"


class Currency(Enum):
    """货币类型枚举"""
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"
    JPY = "JPY"


# ==================== 目标接口 ====================

class PaymentProcessor(ABC):
    """支付处理器接口 - 客户端期望的统一接口"""

    @abstractmethod
    def process_payment(self, amount: float, currency: Currency,
                       payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付"""
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款"""
        pass

    @abstractmethod
    def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """获取支付状态"""
        pass

    @abstractmethod
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        pass


# ==================== 被适配者 - 第三方支付服务 ====================

class StripePaymentService:
    """Stripe支付服务 - 被适配者A"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.transactions = {}
        self.transaction_counter = 1000

    def create_charge(self, amount_cents: int, currency_code: str,
                     source: str, description: str = "") -> Dict[str, Any]:
        """创建支付（Stripe原有接口）"""
        print(f"💳 Stripe创建支付: {amount_cents/100} {currency_code}")

        # 模拟Stripe API调用
        time.sleep(0.1)

        transaction_id = f"ch_{self.transaction_counter}"
        self.transaction_counter += 1

        # 模拟支付结果
        success = amount_cents < 100000  # 小于1000元的支付成功

        result = {
            "id": transaction_id,
            "amount": amount_cents,
            "currency": currency_code,
            "status": "succeeded" if success else "failed",
            "source": source,
            "description": description,
            "created": int(time.time())
        }

        self.transactions[transaction_id] = result
        return result

    def create_refund(self, charge_id: str, amount_cents: int = None) -> Dict[str, Any]:
        """创建退款（Stripe原有接口）"""
        print(f"💰 Stripe创建退款: {charge_id}")

        if charge_id not in self.transactions:
            return {"error": "Charge not found"}

        charge = self.transactions[charge_id]
        refund_amount = amount_cents or charge["amount"]

        refund_id = f"re_{self.transaction_counter}"
        self.transaction_counter += 1

        result = {
            "id": refund_id,
            "charge": charge_id,
            "amount": refund_amount,
            "status": "succeeded",
            "created": int(time.time())
        }

        return result

    def retrieve_charge(self, charge_id: str) -> Dict[str, Any]:
        """获取支付信息（Stripe原有接口）"""
        return self.transactions.get(charge_id, {"error": "Charge not found"})


class PayPalPaymentService:
    """PayPal支付服务 - 被适配者B"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.payments = {}
        self.payment_counter = 2000

    def execute_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行支付（PayPal原有接口）"""
        amount = payment_data.get("amount", {})
        total = float(amount.get("total", 0))
        currency = amount.get("currency", "USD")

        print(f"🅿️  PayPal执行支付: {total} {currency}")

        # 模拟PayPal API调用
        time.sleep(0.15)

        payment_id = f"PAY-{self.payment_counter}"
        self.payment_counter += 1

        # 模拟支付结果
        success = total < 500  # 小于500的支付成功

        result = {
            "id": payment_id,
            "state": "approved" if success else "failed",
            "transactions": [{
                "amount": amount,
                "description": payment_data.get("description", "")
            }],
            "create_time": datetime.now().isoformat(),
            "update_time": datetime.now().isoformat()
        }

        self.payments[payment_id] = result
        return result

    def refund_sale(self, sale_id: str, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """退款（PayPal原有接口）"""
        print(f"💰 PayPal处理退款: {sale_id}")

        if sale_id not in self.payments:
            return {"error": "Payment not found"}

        refund_id = f"RF-{self.payment_counter}"
        self.payment_counter += 1

        result = {
            "id": refund_id,
            "sale_id": sale_id,
            "state": "completed",
            "amount": refund_data.get("amount", {}),
            "create_time": datetime.now().isoformat()
        }

        return result

    def get_payment_details(self, payment_id: str) -> Dict[str, Any]:
        """获取支付详情（PayPal原有接口）"""
        return self.payments.get(payment_id, {"error": "Payment not found"})


class AlipayService:
    """支付宝服务 - 被适配者C"""

    def __init__(self, app_id: str, private_key: str):
        self.app_id = app_id
        self.private_key = private_key
        self.orders = {}
        self.order_counter = 3000

    def trade_create(self, out_trade_no: str, total_amount: str,
                    subject: str, body: str = "") -> Dict[str, Any]:
        """创建交易（支付宝原有接口）"""
        print(f"🟡 支付宝创建交易: {total_amount} CNY")

        # 模拟支付宝API调用
        time.sleep(0.08)

        trade_no = f"2024{self.order_counter}"
        self.order_counter += 1

        # 模拟支付结果
        amount = float(total_amount)
        success = amount < 1000  # 小于1000元的支付成功

        result = {
            "trade_no": trade_no,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "trade_status": "TRADE_SUCCESS" if success else "TRADE_CLOSED",
            "subject": subject,
            "body": body,
            "gmt_create": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gmt_payment": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if success else None
        }

        self.orders[trade_no] = result
        return result

    def trade_refund(self, trade_no: str, refund_amount: str,
                    refund_reason: str = "") -> Dict[str, Any]:
        """交易退款（支付宝原有接口）"""
        print(f"💰 支付宝处理退款: {trade_no}")

        if trade_no not in self.orders:
            return {"code": "40004", "msg": "交易不存在"}

        result = {
            "trade_no": trade_no,
            "refund_fee": refund_amount,
            "gmt_refund_pay": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "refund_detail_item_list": [{
                "fund_channel": "ALIPAYACCOUNT",
                "amount": refund_amount
            }]
        }

        return result

    def trade_query(self, trade_no: str) -> Dict[str, Any]:
        """查询交易（支付宝原有接口）"""
        return self.orders.get(trade_no, {"code": "40004", "msg": "交易不存在"})


# ==================== 适配器实现 ====================

class StripeAdapter(PaymentProcessor):
    """Stripe适配器"""

    def __init__(self, stripe_service: StripePaymentService):
        self.stripe_service = stripe_service

    def process_payment(self, amount: float, currency: Currency,
                       payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付 - 适配Stripe接口"""
        print(f"🔄 Stripe适配器处理支付")

        # 转换参数格式
        amount_cents = int(amount * 100)  # Stripe使用分为单位
        currency_code = currency.value.lower()
        source = payment_method.get("card_token", "tok_visa")
        description = payment_method.get("description", "Payment via Stripe Adapter")

        # 调用Stripe服务
        stripe_result = self.stripe_service.create_charge(
            amount_cents, currency_code, source, description
        )

        # 转换返回格式
        if "error" in stripe_result:
            return {
                "success": False,
                "transaction_id": None,
                "status": PaymentStatus.FAILED,
                "error": stripe_result["error"],
                "provider": "Stripe"
            }

        return {
            "success": stripe_result["status"] == "succeeded",
            "transaction_id": stripe_result["id"],
            "status": PaymentStatus.SUCCESS if stripe_result["status"] == "succeeded" else PaymentStatus.FAILED,
            "amount": amount,
            "currency": currency,
            "provider": "Stripe",
            "raw_response": stripe_result
        }

    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款 - 适配Stripe接口"""
        print(f"🔄 Stripe适配器处理退款")

        amount_cents = int(amount * 100)
        stripe_result = self.stripe_service.create_refund(transaction_id, amount_cents)

        if "error" in stripe_result:
            return {
                "success": False,
                "refund_id": None,
                "error": stripe_result["error"]
            }

        return {
            "success": stripe_result["status"] == "succeeded",
            "refund_id": stripe_result["id"],
            "amount": amount,
            "provider": "Stripe"
        }

    def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """获取支付状态 - 适配Stripe接口"""
        stripe_result = self.stripe_service.retrieve_charge(transaction_id)

        if "error" in stripe_result:
            return {
                "found": False,
                "error": stripe_result["error"]
            }

        return {
            "found": True,
            "transaction_id": transaction_id,
            "status": PaymentStatus.SUCCESS if stripe_result["status"] == "succeeded" else PaymentStatus.FAILED,
            "amount": stripe_result["amount"] / 100,
            "currency": stripe_result["currency"].upper(),
            "provider": "Stripe"
        }

    def get_processor_info(self) -> str:
        return f"Stripe适配器 (API密钥: {self.stripe_service.api_key[:8]}...)"


class PayPalAdapter(PaymentProcessor):
    """PayPal适配器"""

    def __init__(self, paypal_service: PayPalPaymentService):
        self.paypal_service = paypal_service

    def process_payment(self, amount: float, currency: Currency,
                       payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付 - 适配PayPal接口"""
        print(f"🔄 PayPal适配器处理支付")

        # 转换参数格式
        payment_data = {
            "amount": {
                "total": str(amount),
                "currency": currency.value
            },
            "description": payment_method.get("description", "Payment via PayPal Adapter")
        }

        # 调用PayPal服务
        paypal_result = self.paypal_service.execute_payment(payment_data)

        # 转换返回格式
        if "error" in paypal_result:
            return {
                "success": False,
                "transaction_id": None,
                "status": PaymentStatus.FAILED,
                "error": paypal_result["error"],
                "provider": "PayPal"
            }

        return {
            "success": paypal_result["state"] == "approved",
            "transaction_id": paypal_result["id"],
            "status": PaymentStatus.SUCCESS if paypal_result["state"] == "approved" else PaymentStatus.FAILED,
            "amount": amount,
            "currency": currency,
            "provider": "PayPal",
            "raw_response": paypal_result
        }

    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款 - 适配PayPal接口"""
        print(f"🔄 PayPal适配器处理退款")

        refund_data = {
            "amount": {
                "total": str(amount),
                "currency": "USD"  # 简化示例
            }
        }

        paypal_result = self.paypal_service.refund_sale(transaction_id, refund_data)

        if "error" in paypal_result:
            return {
                "success": False,
                "refund_id": None,
                "error": paypal_result["error"]
            }

        return {
            "success": paypal_result["state"] == "completed",
            "refund_id": paypal_result["id"],
            "amount": amount,
            "provider": "PayPal"
        }

    def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """获取支付状态 - 适配PayPal接口"""
        paypal_result = self.paypal_service.get_payment_details(transaction_id)

        if "error" in paypal_result:
            return {
                "found": False,
                "error": paypal_result["error"]
            }

        return {
            "found": True,
            "transaction_id": transaction_id,
            "status": PaymentStatus.SUCCESS if paypal_result["state"] == "approved" else PaymentStatus.FAILED,
            "provider": "PayPal"
        }

    def get_processor_info(self) -> str:
        return f"PayPal适配器 (客户端ID: {self.paypal_service.client_id[:8]}...)"


class AlipayAdapter(PaymentProcessor):
    """支付宝适配器"""

    def __init__(self, alipay_service: AlipayService):
        self.alipay_service = alipay_service
        self.order_counter = 1

    def process_payment(self, amount: float, currency: Currency,
                       payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付 - 适配支付宝接口"""
        print(f"🔄 支付宝适配器处理支付")

        # 生成订单号
        out_trade_no = f"ORDER_{self.order_counter}_{int(time.time())}"
        self.order_counter += 1

        # 转换参数格式
        total_amount = str(amount)
        subject = payment_method.get("subject", "商品购买")
        body = payment_method.get("description", "Payment via Alipay Adapter")

        # 调用支付宝服务
        alipay_result = self.alipay_service.trade_create(
            out_trade_no, total_amount, subject, body
        )

        # 转换返回格式
        if "code" in alipay_result:
            return {
                "success": False,
                "transaction_id": None,
                "status": PaymentStatus.FAILED,
                "error": alipay_result["msg"],
                "provider": "Alipay"
            }

        return {
            "success": alipay_result["trade_status"] == "TRADE_SUCCESS",
            "transaction_id": alipay_result["trade_no"],
            "status": PaymentStatus.SUCCESS if alipay_result["trade_status"] == "TRADE_SUCCESS" else PaymentStatus.FAILED,
            "amount": amount,
            "currency": Currency.CNY,  # 支付宝主要使用人民币
            "provider": "Alipay",
            "raw_response": alipay_result
        }

    def refund_payment(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """退款 - 适配支付宝接口"""
        print(f"🔄 支付宝适配器处理退款")

        refund_amount = str(amount)
        alipay_result = self.alipay_service.trade_refund(
            transaction_id, refund_amount, "用户申请退款"
        )

        if "code" in alipay_result:
            return {
                "success": False,
                "refund_id": None,
                "error": alipay_result["msg"]
            }

        return {
            "success": True,
            "refund_id": f"RF_{transaction_id}",
            "amount": amount,
            "provider": "Alipay"
        }

    def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """获取支付状态 - 适配支付宝接口"""
        alipay_result = self.alipay_service.trade_query(transaction_id)

        if "code" in alipay_result:
            return {
                "found": False,
                "error": alipay_result["msg"]
            }

        return {
            "found": True,
            "transaction_id": transaction_id,
            "status": PaymentStatus.SUCCESS if alipay_result["trade_status"] == "TRADE_SUCCESS" else PaymentStatus.FAILED,
            "provider": "Alipay"
        }

    def get_processor_info(self) -> str:
        return f"支付宝适配器 (应用ID: {self.alipay_service.app_id[:8]}...)"


# ==================== 客户端代码 ====================

class PaymentGateway:
    """支付网关 - 客户端"""

    def __init__(self):
        self.processors: Dict[str, PaymentProcessor] = {}
        self.default_processor = None

    def register_processor(self, name: str, processor: PaymentProcessor,
                          is_default: bool = False) -> None:
        """注册支付处理器"""
        self.processors[name] = processor
        if is_default or not self.default_processor:
            self.default_processor = name
        print(f"✅ 已注册支付处理器: {name} -> {processor.get_processor_info()}")

    def process_payment(self, amount: float, currency: Currency = Currency.USD,
                       payment_method: Dict[str, Any] = None,
                       processor_name: str = None) -> Dict[str, Any]:
        """处理支付"""
        processor_name = processor_name or self.default_processor

        if processor_name not in self.processors:
            return {
                "success": False,
                "error": f"未找到支付处理器: {processor_name}"
            }

        processor = self.processors[processor_name]
        print(f"\n💳 使用 {processor_name} 处理支付: {amount} {currency.value}")

        return processor.process_payment(amount, currency, payment_method or {})

    def refund_payment(self, transaction_id: str, amount: float,
                      processor_name: str = None) -> Dict[str, Any]:
        """处理退款"""
        processor_name = processor_name or self.default_processor

        if processor_name not in self.processors:
            return {
                "success": False,
                "error": f"未找到支付处理器: {processor_name}"
            }

        processor = self.processors[processor_name]
        print(f"\n💰 使用 {processor_name} 处理退款: {transaction_id}")

        return processor.refund_payment(transaction_id, amount)

    def get_available_processors(self) -> List[str]:
        """获取可用的支付处理器"""
        return list(self.processors.keys())


def demo_third_party_adapter():
    """第三方支付适配器演示"""
    print("=" * 60)
    print("💳 第三方支付系统 - 适配器模式演示")
    print("=" * 60)

    # 创建第三方支付服务
    stripe_service = StripePaymentService("sk_test_123456789")
    paypal_service = PayPalPaymentService("client_123", "secret_456")
    alipay_service = AlipayService("app_789", "private_key_abc")

    # 创建适配器
    stripe_adapter = StripeAdapter(stripe_service)
    paypal_adapter = PayPalAdapter(paypal_service)
    alipay_adapter = AlipayAdapter(alipay_service)

    # 创建支付网关
    gateway = PaymentGateway()

    # 注册支付处理器
    gateway.register_processor("stripe", stripe_adapter, is_default=True)
    gateway.register_processor("paypal", paypal_adapter)
    gateway.register_processor("alipay", alipay_adapter)

    # 测试支付
    test_payments = [
        (99.99, Currency.USD, {"card_token": "tok_visa", "description": "测试商品"}, "stripe"),
        (299.00, Currency.USD, {"description": "高级服务"}, "paypal"),
        (199.00, Currency.CNY, {"subject": "数码产品", "description": "手机购买"}, "alipay")
    ]

    transaction_ids = []

    print(f"\n🧪 测试不同支付处理器:")
    for amount, currency, payment_method, processor in test_payments:
        result = gateway.process_payment(amount, currency, payment_method, processor)

        if result["success"]:
            transaction_ids.append((result["transaction_id"], processor, amount))
            print(f"   ✅ 支付成功: {result['transaction_id']}")
        else:
            print(f"   ❌ 支付失败: {result.get('error', '未知错误')}")

    # 测试退款
    print(f"\n💰 测试退款功能:")
    for transaction_id, processor, amount in transaction_ids[:2]:  # 只退款前两个
        refund_result = gateway.refund_payment(transaction_id, amount/2, processor)

        if refund_result["success"]:
            print(f"   ✅ 退款成功: {refund_result['refund_id']}")
        else:
            print(f"   ❌ 退款失败: {refund_result.get('error', '未知错误')}")


if __name__ == "__main__":
    demo_third_party_adapter()
