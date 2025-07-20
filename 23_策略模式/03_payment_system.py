"""
03_payment_system.py - 支付系统策略模式

这个示例展示了策略模式在支付系统中的应用。
演示了多种支付方式的统一处理和动态选择。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime, timedelta
import random
import uuid


# ==================== 枚举定义 ====================

class PaymentStatus(Enum):
    """支付状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Currency(Enum):
    """货币类型"""
    CNY = "CNY"
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"


# ==================== 支付结果类 ====================

class PaymentResult:
    """支付结果"""
    
    def __init__(self, success: bool, transaction_id: str = None, 
                 message: str = "", error_code: str = None):
        self.success = success
        self.transaction_id = transaction_id or str(uuid.uuid4())[:8]
        self.message = message
        self.error_code = error_code
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        status = "成功" if self.success else "失败"
        return f"支付{status}: {self.message} (ID: {self.transaction_id})"


# ==================== 抽象策略接口 ====================

class PaymentStrategy(ABC):
    """支付策略抽象类"""
    
    @abstractmethod
    def pay(self, amount: float, currency: Currency = Currency.CNY, **kwargs) -> PaymentResult:
        """执行支付"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """执行退款"""
        pass
    
    @abstractmethod
    def get_payment_type(self) -> str:
        """获取支付类型名称"""
        pass
    
    @abstractmethod
    def get_supported_currencies(self) -> List[Currency]:
        """获取支持的货币类型"""
        pass
    
    @abstractmethod
    def get_fee_rate(self) -> float:
        """获取手续费率"""
        pass
    
    @abstractmethod
    def get_max_amount(self) -> float:
        """获取最大支付金额"""
        pass
    
    @abstractmethod
    def validate_payment_data(self, **kwargs) -> bool:
        """验证支付数据"""
        pass


# ==================== 具体支付策略 ====================

class CreditCardPayment(PaymentStrategy):
    """信用卡支付策略"""
    
    def __init__(self):
        self._transaction_history: List[Dict[str, Any]] = []
    
    def pay(self, amount: float, currency: Currency = Currency.CNY, **kwargs) -> PaymentResult:
        """信用卡支付"""
        # 验证支付数据
        if not self.validate_payment_data(**kwargs):
            return PaymentResult(False, message="信用卡信息验证失败", error_code="INVALID_CARD")
        
        # 检查金额限制
        if amount > self.get_max_amount():
            return PaymentResult(False, message=f"超过单笔限额 ¥{self.get_max_amount()}", error_code="AMOUNT_EXCEEDED")
        
        # 检查货币支持
        if currency not in self.get_supported_currencies():
            return PaymentResult(False, message=f"不支持货币类型 {currency.value}", error_code="CURRENCY_NOT_SUPPORTED")
        
        # 模拟支付处理
        card_number = kwargs.get('card_number', '')
        holder_name = kwargs.get('holder_name', '')
        
        # 计算手续费
        fee = amount * self.get_fee_rate()
        total_amount = amount + fee
        
        print(f"💳 信用卡支付处理中...")
        print(f"   卡号: ****-****-****-{card_number[-4:] if len(card_number) >= 4 else '****'}")
        print(f"   持卡人: {holder_name}")
        print(f"   金额: {amount} {currency.value}")
        print(f"   手续费: {fee:.2f} {currency.value}")
        print(f"   总计: {total_amount:.2f} {currency.value}")
        
        # 模拟支付成功率（95%）
        if random.random() < 0.95:
            transaction_id = f"CC_{uuid.uuid4().hex[:8].upper()}"
            
            # 记录交易
            self._transaction_history.append({
                'transaction_id': transaction_id,
                'amount': amount,
                'fee': fee,
                'currency': currency.value,
                'timestamp': datetime.now(),
                'type': 'payment'
            })
            
            return PaymentResult(True, transaction_id, f"信用卡支付成功 ¥{total_amount:.2f}")
        else:
            return PaymentResult(False, message="银行拒绝交易", error_code="BANK_DECLINED")
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """信用卡退款"""
        # 查找原交易
        original_transaction = None
        for transaction in self._transaction_history:
            if transaction['transaction_id'] == transaction_id:
                original_transaction = transaction
                break
        
        if not original_transaction:
            return PaymentResult(False, message="未找到原交易记录", error_code="TRANSACTION_NOT_FOUND")
        
        if amount > original_transaction['amount']:
            return PaymentResult(False, message="退款金额超过原交易金额", error_code="REFUND_AMOUNT_EXCEEDED")
        
        print(f"💳 信用卡退款处理中...")
        print(f"   原交易ID: {transaction_id}")
        print(f"   退款金额: {amount} {original_transaction['currency']}")
        
        # 模拟退款成功率（98%）
        if random.random() < 0.98:
            refund_id = f"RF_{uuid.uuid4().hex[:8].upper()}"
            
            # 记录退款
            self._transaction_history.append({
                'transaction_id': refund_id,
                'original_transaction_id': transaction_id,
                'amount': amount,
                'currency': original_transaction['currency'],
                'timestamp': datetime.now(),
                'type': 'refund'
            })
            
            return PaymentResult(True, refund_id, f"信用卡退款成功 ¥{amount:.2f}")
        else:
            return PaymentResult(False, message="退款处理失败", error_code="REFUND_FAILED")
    
    def get_payment_type(self) -> str:
        return "信用卡支付"
    
    def get_supported_currencies(self) -> List[Currency]:
        return [Currency.CNY, Currency.USD, Currency.EUR]
    
    def get_fee_rate(self) -> float:
        return 0.006  # 0.6% 手续费
    
    def get_max_amount(self) -> float:
        return 50000.0  # 单笔最大5万
    
    def validate_payment_data(self, **kwargs) -> bool:
        """验证信用卡数据"""
        required_fields = ['card_number', 'holder_name', 'cvv', 'expiry_date']
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                return False
        
        # 简单的卡号验证（长度检查）
        card_number = kwargs['card_number'].replace(' ', '').replace('-', '')
        if len(card_number) < 13 or len(card_number) > 19:
            return False
        
        return True


class AlipayPayment(PaymentStrategy):
    """支付宝支付策略"""
    
    def __init__(self):
        self._transaction_history: List[Dict[str, Any]] = []
    
    def pay(self, amount: float, currency: Currency = Currency.CNY, **kwargs) -> PaymentResult:
        """支付宝支付"""
        if not self.validate_payment_data(**kwargs):
            return PaymentResult(False, message="支付宝账户验证失败", error_code="INVALID_ACCOUNT")
        
        if amount > self.get_max_amount():
            return PaymentResult(False, message=f"超过单笔限额 ¥{self.get_max_amount()}", error_code="AMOUNT_EXCEEDED")
        
        if currency not in self.get_supported_currencies():
            return PaymentResult(False, message=f"不支持货币类型 {currency.value}", error_code="CURRENCY_NOT_SUPPORTED")
        
        account = kwargs.get('account', '')
        
        print(f"💰 支付宝支付处理中...")
        print(f"   账户: {account}")
        print(f"   金额: {amount} {currency.value}")
        
        # 支付宝手续费较低
        fee = amount * self.get_fee_rate()
        total_amount = amount + fee
        
        # 模拟支付成功率（98%）
        if random.random() < 0.98:
            transaction_id = f"AP_{uuid.uuid4().hex[:8].upper()}"
            
            self._transaction_history.append({
                'transaction_id': transaction_id,
                'amount': amount,
                'fee': fee,
                'currency': currency.value,
                'timestamp': datetime.now(),
                'type': 'payment'
            })
            
            return PaymentResult(True, transaction_id, f"支付宝支付成功 ¥{amount:.2f}")
        else:
            return PaymentResult(False, message="支付宝余额不足", error_code="INSUFFICIENT_BALANCE")
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """支付宝退款"""
        # 查找原交易
        original_transaction = None
        for transaction in self._transaction_history:
            if transaction['transaction_id'] == transaction_id:
                original_transaction = transaction
                break
        
        if not original_transaction:
            return PaymentResult(False, message="未找到原交易记录", error_code="TRANSACTION_NOT_FOUND")
        
        print(f"💰 支付宝退款处理中...")
        print(f"   原交易ID: {transaction_id}")
        print(f"   退款金额: {amount} {original_transaction['currency']}")
        
        # 支付宝退款通常很快
        refund_id = f"RF_{uuid.uuid4().hex[:8].upper()}"
        
        self._transaction_history.append({
            'transaction_id': refund_id,
            'original_transaction_id': transaction_id,
            'amount': amount,
            'currency': original_transaction['currency'],
            'timestamp': datetime.now(),
            'type': 'refund'
        })
        
        return PaymentResult(True, refund_id, f"支付宝退款成功 ¥{amount:.2f}")
    
    def get_payment_type(self) -> str:
        return "支付宝支付"
    
    def get_supported_currencies(self) -> List[Currency]:
        return [Currency.CNY]  # 主要支持人民币
    
    def get_fee_rate(self) -> float:
        return 0.001  # 0.1% 手续费
    
    def get_max_amount(self) -> float:
        return 200000.0  # 单笔最大20万
    
    def validate_payment_data(self, **kwargs) -> bool:
        """验证支付宝数据"""
        account = kwargs.get('account', '')
        return bool(account and ('@' in account or len(account) == 11))


class WechatPayment(PaymentStrategy):
    """微信支付策略"""
    
    def __init__(self):
        self._transaction_history: List[Dict[str, Any]] = []
    
    def pay(self, amount: float, currency: Currency = Currency.CNY, **kwargs) -> PaymentResult:
        """微信支付"""
        if not self.validate_payment_data(**kwargs):
            return PaymentResult(False, message="微信账户验证失败", error_code="INVALID_ACCOUNT")
        
        if amount > self.get_max_amount():
            return PaymentResult(False, message=f"超过单笔限额 ¥{self.get_max_amount()}", error_code="AMOUNT_EXCEEDED")
        
        phone_number = kwargs.get('phone_number', '')
        
        print(f"💚 微信支付处理中...")
        print(f"   手机号: {phone_number}")
        print(f"   金额: {amount} {currency.value}")
        
        # 模拟支付成功率（97%）
        if random.random() < 0.97:
            transaction_id = f"WX_{uuid.uuid4().hex[:8].upper()}"
            
            self._transaction_history.append({
                'transaction_id': transaction_id,
                'amount': amount,
                'fee': 0,  # 微信支付通常不收手续费
                'currency': currency.value,
                'timestamp': datetime.now(),
                'type': 'payment'
            })
            
            return PaymentResult(True, transaction_id, f"微信支付成功 ¥{amount:.2f}")
        else:
            return PaymentResult(False, message="微信支付失败", error_code="PAYMENT_FAILED")
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """微信退款"""
        original_transaction = None
        for transaction in self._transaction_history:
            if transaction['transaction_id'] == transaction_id:
                original_transaction = transaction
                break
        
        if not original_transaction:
            return PaymentResult(False, message="未找到原交易记录", error_code="TRANSACTION_NOT_FOUND")
        
        print(f"💚 微信退款处理中...")
        print(f"   原交易ID: {transaction_id}")
        print(f"   退款金额: {amount} {original_transaction['currency']}")
        
        refund_id = f"RF_{uuid.uuid4().hex[:8].upper()}"
        
        self._transaction_history.append({
            'transaction_id': refund_id,
            'original_transaction_id': transaction_id,
            'amount': amount,
            'currency': original_transaction['currency'],
            'timestamp': datetime.now(),
            'type': 'refund'
        })
        
        return PaymentResult(True, refund_id, f"微信退款成功 ¥{amount:.2f}")
    
    def get_payment_type(self) -> str:
        return "微信支付"
    
    def get_supported_currencies(self) -> List[Currency]:
        return [Currency.CNY]
    
    def get_fee_rate(self) -> float:
        return 0.0  # 微信支付通常不收手续费
    
    def get_max_amount(self) -> float:
        return 50000.0  # 单笔最大5万
    
    def validate_payment_data(self, **kwargs) -> bool:
        """验证微信数据"""
        phone_number = kwargs.get('phone_number', '')
        return bool(phone_number and len(phone_number) == 11 and phone_number.isdigit())


class BankTransferPayment(PaymentStrategy):
    """银行转账支付策略"""
    
    def __init__(self):
        self._transaction_history: List[Dict[str, Any]] = []
    
    def pay(self, amount: float, currency: Currency = Currency.CNY, **kwargs) -> PaymentResult:
        """银行转账支付"""
        if not self.validate_payment_data(**kwargs):
            return PaymentResult(False, message="银行账户信息验证失败", error_code="INVALID_ACCOUNT")
        
        if amount > self.get_max_amount():
            return PaymentResult(False, message=f"超过单笔限额 ¥{self.get_max_amount()}", error_code="AMOUNT_EXCEEDED")
        
        account_number = kwargs.get('account_number', '')
        bank_name = kwargs.get('bank_name', '')
        
        print(f"🏦 银行转账处理中...")
        print(f"   银行: {bank_name}")
        print(f"   账号: ****{account_number[-4:] if len(account_number) >= 4 else '****'}")
        print(f"   金额: {amount} {currency.value}")
        
        # 银行转账通常需要更长时间处理
        print("   ⏳ 银行转账通常需要1-3个工作日到账")
        
        # 模拟转账成功率（99%，但需要时间）
        if random.random() < 0.99:
            transaction_id = f"BT_{uuid.uuid4().hex[:8].upper()}"
            
            self._transaction_history.append({
                'transaction_id': transaction_id,
                'amount': amount,
                'fee': amount * self.get_fee_rate(),
                'currency': currency.value,
                'timestamp': datetime.now(),
                'type': 'payment'
            })
            
            return PaymentResult(True, transaction_id, f"银行转账提交成功 ¥{amount:.2f}")
        else:
            return PaymentResult(False, message="银行转账失败", error_code="TRANSFER_FAILED")
    
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """银行转账退款"""
        print(f"🏦 银行转账退款处理中...")
        print(f"   ⏳ 银行退款通常需要3-7个工作日")
        
        refund_id = f"RF_{uuid.uuid4().hex[:8].upper()}"
        return PaymentResult(True, refund_id, f"银行退款申请已提交 ¥{amount:.2f}")
    
    def get_payment_type(self) -> str:
        return "银行转账"
    
    def get_supported_currencies(self) -> List[Currency]:
        return [Currency.CNY, Currency.USD, Currency.EUR]
    
    def get_fee_rate(self) -> float:
        return 0.002  # 0.2% 手续费
    
    def get_max_amount(self) -> float:
        return 1000000.0  # 单笔最大100万
    
    def validate_payment_data(self, **kwargs) -> bool:
        """验证银行账户数据"""
        required_fields = ['account_number', 'bank_name', 'account_holder']
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                return False
        return True


# ==================== 支付上下文 ====================

class PaymentProcessor:
    """支付处理器 - 上下文类"""
    
    def __init__(self):
        self._strategy: Optional[PaymentStrategy] = None
        self._payment_history: List[Dict[str, Any]] = []
        self._available_strategies: Dict[str, PaymentStrategy] = {
            'credit_card': CreditCardPayment(),
            'alipay': AlipayPayment(),
            'wechat': WechatPayment(),
            'bank_transfer': BankTransferPayment()
        }
    
    def set_payment_strategy(self, strategy_name: str) -> bool:
        """设置支付策略"""
        if strategy_name not in self._available_strategies:
            print(f"❌ 不支持的支付方式: {strategy_name}")
            return False
        
        self._strategy = self._available_strategies[strategy_name]
        print(f"💳 选择支付方式: {self._strategy.get_payment_type()}")
        return True
    
    def process_payment(self, amount: float, currency: Currency = Currency.CNY, **payment_data) -> PaymentResult:
        """处理支付"""
        if not self._strategy:
            return PaymentResult(False, message="未选择支付方式", error_code="NO_PAYMENT_METHOD")
        
        print(f"\n💰 开始处理支付...")
        print(f"   支付方式: {self._strategy.get_payment_type()}")
        print(f"   支付金额: {amount} {currency.value}")
        
        result = self._strategy.pay(amount, currency, **payment_data)
        
        # 记录支付历史
        self._payment_history.append({
            'payment_method': self._strategy.get_payment_type(),
            'amount': amount,
            'currency': currency.value,
            'result': result,
            'timestamp': datetime.now()
        })
        
        return result
    
    def process_refund(self, transaction_id: str, amount: float) -> PaymentResult:
        """处理退款"""
        if not self._strategy:
            return PaymentResult(False, message="未选择支付方式", error_code="NO_PAYMENT_METHOD")
        
        print(f"\n💸 开始处理退款...")
        print(f"   退款方式: {self._strategy.get_payment_type()}")
        
        return self._strategy.refund(transaction_id, amount)
    
    def get_payment_info(self) -> Dict[str, Any]:
        """获取当前支付方式信息"""
        if not self._strategy:
            return {}
        
        return {
            'payment_type': self._strategy.get_payment_type(),
            'supported_currencies': [c.value for c in self._strategy.get_supported_currencies()],
            'fee_rate': self._strategy.get_fee_rate(),
            'max_amount': self._strategy.get_max_amount()
        }
    
    def get_available_payment_methods(self) -> List[str]:
        """获取可用的支付方式"""
        return list(self._available_strategies.keys())
    
    def get_payment_history(self) -> List[Dict[str, Any]]:
        """获取支付历史"""
        return self._payment_history.copy()


# ==================== 演示函数 ====================

def demo_payment_strategies():
    """支付策略演示"""
    print("=" * 60)
    print("💳 支付系统策略模式演示")
    print("=" * 60)
    
    # 创建支付处理器
    processor = PaymentProcessor()
    
    # 显示可用支付方式
    print("📋 可用支付方式:")
    for method in processor.get_available_payment_methods():
        processor.set_payment_strategy(method)
        info = processor.get_payment_info()
        print(f"   • {info['payment_type']}")
        print(f"     手续费率: {info['fee_rate']*100:.1f}%")
        print(f"     最大金额: ¥{info['max_amount']:,.0f}")
        print(f"     支持货币: {', '.join(info['supported_currencies'])}")
        print()
    
    # 模拟购物场景
    order_amount = 1299.99
    print(f"🛒 模拟订单支付: ¥{order_amount}")
    
    # 尝试不同支付方式
    payment_scenarios = [
        {
            'method': 'alipay',
            'data': {'account': 'user@example.com'}
        },
        {
            'method': 'wechat',
            'data': {'phone_number': '13800138000'}
        },
        {
            'method': 'credit_card',
            'data': {
                'card_number': '4111111111111111',
                'holder_name': '张三',
                'cvv': '123',
                'expiry_date': '12/25'
            }
        }
    ]
    
    successful_payments = []
    
    for scenario in payment_scenarios:
        print(f"\n" + "=" * 40)
        processor.set_payment_strategy(scenario['method'])
        result = processor.process_payment(order_amount, Currency.CNY, **scenario['data'])
        
        print(f"🎯 支付结果: {result}")
        
        if result.success:
            successful_payments.append((scenario['method'], result.transaction_id))
    
    # 演示退款
    if successful_payments:
        print(f"\n" + "=" * 40)
        print("💸 演示退款流程:")
        
        method, transaction_id = successful_payments[0]
        processor.set_payment_strategy(method)
        refund_result = processor.process_refund(transaction_id, order_amount)
        print(f"🎯 退款结果: {refund_result}")


if __name__ == "__main__":
    demo_payment_strategies()
    
    print("\n" + "=" * 60)
    print("✅ 支付系统策略演示完成")
    print("💡 学习要点:")
    print("   - 策略模式统一了不同支付方式的处理接口")
    print("   - 可以轻松添加新的支付方式而不影响现有代码")
    print("   - 每种支付方式都有自己的特点和限制")
    print("   - 支付和退款流程可以独立实现和优化")
    print("=" * 60)
