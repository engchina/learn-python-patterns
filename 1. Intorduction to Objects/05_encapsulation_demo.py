"""
05_encapsulation_demo.py - 封装和数据保护

这个示例通过银行账户系统展示封装的核心概念：
- 私有属性和方法的使用
- 属性装饰器的应用
- 数据验证和保护
- 访问控制的实现
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from enum import Enum
import hashlib


# ==================== 枚举类型 ====================
class TransactionType(Enum):
    """交易类型枚举"""
    DEPOSIT = "存款"
    WITHDRAWAL = "取款"
    TRANSFER = "转账"
    INTEREST = "利息"
    FEE = "手续费"


class AccountStatus(Enum):
    """账户状态枚举"""
    ACTIVE = "活跃"
    FROZEN = "冻结"
    CLOSED = "关闭"
    SUSPENDED = "暂停"


# ==================== 银行账户类 ====================
class BankAccount:
    """银行账户类 - 展示封装的核心概念"""
    
    # 类属性
    _bank_name = "Python银行"
    _interest_rate = 0.03  # 年利率3%
    _min_balance = 0.0     # 最低余额
    _max_daily_withdrawal = 50000.0  # 每日最大取款额
    
    def __init__(self, account_holder: str, initial_deposit: float = 0.0):
        """
        初始化银行账户
        
        参数:
            account_holder: 账户持有人
            initial_deposit: 初始存款
        """
        # 公共属性
        self.account_holder = account_holder
        self.created_date = date.today()
        self.status = AccountStatus.ACTIVE
        
        # 私有属性（使用单下划线表示内部使用）
        self._account_number = self._generate_account_number()
        self._balance = 0.0
        self._pin = None
        self._daily_withdrawal_amount = 0.0
        self._last_withdrawal_date = None
        
        # 非常私有的属性（使用双下划线）
        self.__transaction_history: List[Dict] = []
        self.__failed_login_attempts = 0
        self.__last_login_time = None
        
        # 初始存款
        if initial_deposit > 0:
            self._deposit(initial_deposit, "开户存款")
        
        print(f"✅ 账户创建成功: {self.account_holder} - {self._account_number}")
    
    # ==================== 私有方法 ====================
    def _generate_account_number(self) -> str:
        """生成账户号码（私有方法）"""
        import random
        return f"ACC{random.randint(100000, 999999)}"
    
    def _hash_pin(self, pin: str) -> str:
        """加密PIN码（私有方法）"""
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def _validate_pin(self, pin: str) -> bool:
        """验证PIN码（私有方法）"""
        if self._pin is None:
            return False
        return self._hash_pin(pin) == self._pin
    
    def _record_transaction(self, transaction_type: TransactionType, 
                          amount: float, description: str = ""):
        """记录交易（私有方法）"""
        transaction = {
            "timestamp": datetime.now(),
            "type": transaction_type,
            "amount": amount,
            "balance_after": self._balance,
            "description": description
        }
        self.__transaction_history.append(transaction)
    
    def _deposit(self, amount: float, description: str = ""):
        """内部存款方法（私有方法）"""
        self._balance += amount
        self._record_transaction(TransactionType.DEPOSIT, amount, description)
    
    def _withdraw(self, amount: float, description: str = ""):
        """内部取款方法（私有方法）"""
        self._balance -= amount
        self._record_transaction(TransactionType.WITHDRAWAL, amount, description)
    
    def _check_daily_withdrawal_limit(self, amount: float) -> bool:
        """检查每日取款限额（私有方法）"""
        today = date.today()
        
        # 如果是新的一天，重置每日取款额
        if self._last_withdrawal_date != today:
            self._daily_withdrawal_amount = 0.0
            self._last_withdrawal_date = today
        
        return (self._daily_withdrawal_amount + amount) <= self._max_daily_withdrawal
    
    # ==================== 属性装饰器 ====================
    @property
    def balance(self) -> float:
        """获取余额（只读属性）"""
        return self._balance
    
    @property
    def account_number(self) -> str:
        """获取账户号码（只读属性）"""
        return self._account_number
    
    @property
    def bank_name(self) -> str:
        """获取银行名称（只读属性）"""
        return self._bank_name
    
    @property
    def has_pin(self) -> bool:
        """检查是否设置了PIN码"""
        return self._pin is not None
    
    @property
    def is_active(self) -> bool:
        """检查账户是否活跃"""
        return self.status == AccountStatus.ACTIVE
    
    @property
    def daily_withdrawal_remaining(self) -> float:
        """获取今日剩余取款额度"""
        today = date.today()
        if self._last_withdrawal_date != today:
            return self._max_daily_withdrawal
        return self._max_daily_withdrawal - self._daily_withdrawal_amount
    
    # ==================== PIN码管理 ====================
    def set_pin(self, new_pin: str) -> bool:
        """
        设置PIN码
        
        参数:
            new_pin: 新PIN码
            
        返回:
            设置是否成功
        """
        # 验证PIN码格式
        if not new_pin.isdigit() or len(new_pin) != 4:
            print("❌ PIN码必须是4位数字")
            return False
        
        self._pin = self._hash_pin(new_pin)
        print("✅ PIN码设置成功")
        return True
    
    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """
        修改PIN码
        
        参数:
            old_pin: 旧PIN码
            new_pin: 新PIN码
            
        返回:
            修改是否成功
        """
        if not self._validate_pin(old_pin):
            self.__failed_login_attempts += 1
            print(f"❌ 旧PIN码错误，失败次数: {self.__failed_login_attempts}")
            
            if self.__failed_login_attempts >= 3:
                self.status = AccountStatus.FROZEN
                print("🔒 账户已被冻结（PIN码错误次数过多）")
            return False
        
        return self.set_pin(new_pin)
    
    def verify_pin(self, pin: str) -> bool:
        """
        验证PIN码
        
        参数:
            pin: PIN码
            
        返回:
            验证是否成功
        """
        if self.status == AccountStatus.FROZEN:
            print("❌ 账户已冻结，无法验证PIN码")
            return False
        
        if self._validate_pin(pin):
            self.__failed_login_attempts = 0
            self.__last_login_time = datetime.now()
            print("✅ PIN码验证成功")
            return True
        else:
            self.__failed_login_attempts += 1
            print(f"❌ PIN码错误，失败次数: {self.__failed_login_attempts}")
            
            if self.__failed_login_attempts >= 3:
                self.status = AccountStatus.FROZEN
                print("🔒 账户已被冻结（PIN码错误次数过多）")
            return False
    
    # ==================== 账户操作 ====================
    def deposit(self, amount: float, description: str = "") -> bool:
        """
        存款
        
        参数:
            amount: 存款金额
            description: 描述
            
        返回:
            操作是否成功
        """
        if not self.is_active:
            print(f"❌ 账户状态为 {self.status.value}，无法存款")
            return False
        
        if amount <= 0:
            print("❌ 存款金额必须大于0")
            return False
        
        if amount > 1000000:  # 大额存款需要特殊处理
            print("⚠️  大额存款，需要额外验证")
        
        self._deposit(amount, description)
        print(f"💰 存款成功: ¥{amount:,.2f}，当前余额: ¥{self._balance:,.2f}")
        return True
    
    def withdraw(self, amount: float, pin: str, description: str = "") -> bool:
        """
        取款
        
        参数:
            amount: 取款金额
            pin: PIN码
            description: 描述
            
        返回:
            操作是否成功
        """
        if not self.is_active:
            print(f"❌ 账户状态为 {self.status.value}，无法取款")
            return False
        
        if not self.verify_pin(pin):
            return False
        
        if amount <= 0:
            print("❌ 取款金额必须大于0")
            return False
        
        if amount > self._balance:
            print(f"❌ 余额不足，当前余额: ¥{self._balance:,.2f}")
            return False
        
        if not self._check_daily_withdrawal_limit(amount):
            print(f"❌ 超过每日取款限额，今日剩余额度: ¥{self.daily_withdrawal_remaining:,.2f}")
            return False
        
        self._withdraw(amount, description)
        self._daily_withdrawal_amount += amount
        print(f"💸 取款成功: ¥{amount:,.2f}，当前余额: ¥{self._balance:,.2f}")
        return True
    
    def transfer(self, target_account: 'BankAccount', amount: float, 
                pin: str, description: str = "") -> bool:
        """
        转账
        
        参数:
            target_account: 目标账户
            amount: 转账金额
            pin: PIN码
            description: 描述
            
        返回:
            操作是否成功
        """
        if not self.is_active or not target_account.is_active:
            print("❌ 源账户或目标账户状态异常")
            return False
        
        if not self.verify_pin(pin):
            return False
        
        if amount <= 0:
            print("❌ 转账金额必须大于0")
            return False
        
        if amount > self._balance:
            print(f"❌ 余额不足，当前余额: ¥{self._balance:,.2f}")
            return False
        
        # 执行转账
        transfer_desc = f"转账给 {target_account.account_holder}"
        receive_desc = f"来自 {self.account_holder} 的转账"
        
        self._withdraw(amount, transfer_desc)
        target_account._deposit(amount, receive_desc)
        
        # 记录转账交易
        self._record_transaction(TransactionType.TRANSFER, -amount, transfer_desc)
        target_account._record_transaction(TransactionType.TRANSFER, amount, receive_desc)
        
        print(f"💸 转账成功: ¥{amount:,.2f} 转给 {target_account.account_holder}")
        print(f"   当前余额: ¥{self._balance:,.2f}")
        return True
    
    def calculate_interest(self) -> float:
        """
        计算利息
        
        返回:
            利息金额
        """
        if self._balance <= 0:
            return 0.0
        
        # 简单的年利息计算（实际应该按日计算）
        interest = self._balance * self._interest_rate
        return round(interest, 2)
    
    def add_interest(self) -> bool:
        """
        添加利息
        
        返回:
            操作是否成功
        """
        if not self.is_active:
            return False
        
        interest = self.calculate_interest()
        if interest > 0:
            self._deposit(interest, "年度利息")
            print(f"💰 利息已添加: ¥{interest:,.2f}")
            return True
        return False
    
    # ==================== 信息查询 ====================
    def get_account_info(self) -> str:
        """获取账户信息"""
        info = [
            f"🏦 {self._bank_name} 账户信息:",
            f"   账户持有人: {self.account_holder}",
            f"   账户号码: {self._account_number}",
            f"   当前余额: ¥{self._balance:,.2f}",
            f"   账户状态: {self.status.value}",
            f"   开户日期: {self.created_date}",
            f"   PIN码状态: {'已设置' if self.has_pin else '未设置'}",
            f"   今日剩余取款额度: ¥{self.daily_withdrawal_remaining:,.2f}",
            f"   预计年利息: ¥{self.calculate_interest():,.2f}"
        ]
        return "\n".join(info)
    
    def get_transaction_history(self, pin: str, limit: int = 10) -> List[Dict]:
        """
        获取交易历史（需要PIN码验证）
        
        参数:
            pin: PIN码
            limit: 返回记录数量限制
            
        返回:
            交易历史列表
        """
        if not self.verify_pin(pin):
            return []
        
        return self.__transaction_history[-limit:]
    
    def print_transaction_history(self, pin: str, limit: int = 10):
        """打印交易历史"""
        transactions = self.get_transaction_history(pin, limit)
        
        if not transactions:
            print("📝 无交易记录或PIN码验证失败")
            return
        
        print(f"\n📝 最近 {len(transactions)} 笔交易记录:")
        print("-" * 70)
        
        for i, trans in enumerate(reversed(transactions), 1):
            timestamp = trans['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            trans_type = trans['type'].value
            amount = trans['amount']
            balance = trans['balance_after']
            desc = trans['description']
            
            amount_str = f"+¥{amount:,.2f}" if amount > 0 else f"-¥{abs(amount):,.2f}"
            print(f"{i:2d}. {timestamp} | {trans_type:4s} | {amount_str:>12s} | "
                  f"余额: ¥{balance:,.2f} | {desc}")
        
        print("-" * 70)
    
    # ==================== 账户管理 ====================
    def freeze_account(self, reason: str = ""):
        """冻结账户"""
        self.status = AccountStatus.FROZEN
        print(f"🔒 账户已冻结" + (f": {reason}" if reason else ""))
    
    def unfreeze_account(self, admin_code: str):
        """解冻账户（需要管理员代码）"""
        if admin_code == "ADMIN123":  # 简单的管理员验证
            self.status = AccountStatus.ACTIVE
            self.__failed_login_attempts = 0
            print("🔓 账户已解冻")
            return True
        else:
            print("❌ 管理员代码错误")
            return False
    
    def close_account(self, pin: str) -> bool:
        """
        关闭账户
        
        参数:
            pin: PIN码
            
        返回:
            操作是否成功
        """
        if not self.verify_pin(pin):
            return False
        
        if self._balance > 0:
            print(f"❌ 账户余额不为零，无法关闭。当前余额: ¥{self._balance:,.2f}")
            return False
        
        self.status = AccountStatus.CLOSED
        print("🔒 账户已关闭")
        return True
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"BankAccount({self.account_holder}, {self._account_number}, ¥{self._balance:,.2f})"
    
    def __repr__(self) -> str:
        """官方字符串表示"""
        return (f"BankAccount(account_holder='{self.account_holder}', "
                f"account_number='{self._account_number}', balance={self._balance})")


# ==================== 银行系统 ====================
class Bank:
    """银行系统类 - 管理多个账户"""
    
    def __init__(self, name: str):
        """初始化银行系统"""
        self.name = name
        self._accounts: Dict[str, BankAccount] = {}
        self._total_deposits = 0.0
        
        print(f"🏦 {name} 银行系统已启动")
    
    def create_account(self, account_holder: str, initial_deposit: float = 0.0) -> BankAccount:
        """创建新账户"""
        account = BankAccount(account_holder, initial_deposit)
        self._accounts[account.account_number] = account
        self._total_deposits += initial_deposit
        return account
    
    def find_account(self, account_number: str) -> Optional[BankAccount]:
        """查找账户"""
        return self._accounts.get(account_number)
    
    def get_bank_statistics(self) -> str:
        """获取银行统计信息"""
        total_accounts = len(self._accounts)
        active_accounts = sum(1 for acc in self._accounts.values() if acc.is_active)
        total_balance = sum(acc.balance for acc in self._accounts.values())
        
        stats = [
            f"🏦 {self.name} 银行统计:",
            f"   总账户数: {total_accounts}",
            f"   活跃账户: {active_accounts}",
            f"   总存款: ¥{total_balance:,.2f}",
            f"   平均余额: ¥{total_balance/total_accounts if total_accounts > 0 else 0:,.2f}"
        ]
        
        return "\n".join(stats)


# ==================== 演示函数 ====================
def demo_encapsulation():
    """封装演示"""
    print("=" * 80)
    print("🏦 面向对象封装和数据保护演示")
    print("=" * 80)
    
    # 创建银行系统
    bank = Bank("Python银行")
    
    print(f"\n{'='*20} 创建账户 {'='*20}")
    
    # 创建账户
    alice_account = bank.create_account("Alice", 10000)
    bob_account = bank.create_account("Bob", 5000)
    charlie_account = bank.create_account("Charlie", 15000)
    
    print(f"\n{'='*20} PIN码设置 {'='*20}")
    
    # 设置PIN码
    alice_account.set_pin("1234")
    bob_account.set_pin("5678")
    charlie_account.set_pin("9999")
    
    # 测试无效PIN码
    alice_account.set_pin("abc")  # 无效格式
    alice_account.set_pin("12345")  # 长度错误
    
    print(f"\n{'='*20} 账户操作 {'='*20}")
    
    # 存款操作
    print(f"\n💰 存款操作:")
    alice_account.deposit(2000, "工资")
    bob_account.deposit(1500, "奖金")
    
    # 取款操作
    print(f"\n💸 取款操作:")
    alice_account.withdraw(500, "1234", "购物")
    bob_account.withdraw(200, "5678", "餐费")
    
    # 测试错误PIN码
    print(f"\n🧪 测试错误PIN码:")
    alice_account.withdraw(100, "0000", "测试")  # 错误PIN
    alice_account.withdraw(100, "1111", "测试")  # 错误PIN
    alice_account.withdraw(100, "2222", "测试")  # 错误PIN（第三次，账户会被冻结）
    
    print(f"\n{'='*20} 转账操作 {'='*20}")
    
    # 转账操作
    print(f"\n💸 转账操作:")
    bob_account.transfer(charlie_account, 1000, "5678", "借款")
    
    print(f"\n{'='*20} 账户信息查询 {'='*20}")
    
    # 查询账户信息
    for account in [alice_account, bob_account, charlie_account]:
        print(f"\n{account.get_account_info()}")
    
    print(f"\n{'='*20} 交易历史 {'='*20}")
    
    # 查看交易历史
    print(f"\nBob的交易历史:")
    bob_account.print_transaction_history("5678", 5)
    
    print(f"\nCharlie的交易历史:")
    charlie_account.print_transaction_history("9999", 5)
    
    print(f"\n{'='*20} 利息计算 {'='*20}")
    
    # 利息计算和添加
    print(f"\n💰 利息计算:")
    for account in [bob_account, charlie_account]:
        if account.is_active:
            interest = account.calculate_interest()
            print(f"   {account.account_holder} 预计年利息: ¥{interest:,.2f}")
            account.add_interest()
    
    print(f"\n{'='*20} 账户管理 {'='*20}")
    
    # 解冻Alice的账户
    print(f"\n🔓 账户解冻:")
    alice_account.unfreeze_account("ADMIN123")
    
    # 修改PIN码
    print(f"\n🔑 修改PIN码:")
    alice_account.change_pin("1234", "4321")
    
    print(f"\n{'='*20} 数据保护演示 {'='*20}")
    
    # 演示封装的数据保护
    print(f"\n🔒 数据保护演示:")
    print(f"   可以访问公共属性: {alice_account.account_holder}")
    print(f"   可以访问只读属性: {alice_account.balance}")
    print(f"   可以访问只读属性: {alice_account.account_number}")
    
    # 尝试直接访问私有属性（不推荐）
    print(f"\n⚠️  尝试访问私有属性:")
    try:
        # 这些操作在实际应用中应该避免
        print(f"   _balance (不推荐): {alice_account._balance}")
        print(f"   无法直接访问 __transaction_history")
    except AttributeError as e:
        print(f"   访问失败: {e}")
    
    print(f"\n{'='*20} 银行统计 {'='*20}")
    
    # 银行统计信息
    print(f"\n{bank.get_bank_statistics()}")
    
    print(f"\n{'='*20} 最终账户状态 {'='*20}")
    
    # 最终账户状态
    for account in [alice_account, bob_account, charlie_account]:
        print(f"   {account}")
    
    print("\n" + "=" * 80)
    print("🎉 封装和数据保护演示完成!")
    print("💡 关键点:")
    print("   - 使用私有属性保护敏感数据")
    print("   - 属性装饰器提供受控的数据访问")
    print("   - 数据验证确保数据的完整性")
    print("   - 封装隐藏了实现细节，提供了清晰的接口")
    print("=" * 80)


if __name__ == "__main__":
    demo_encapsulation()
