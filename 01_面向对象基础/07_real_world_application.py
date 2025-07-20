"""
07_real_world_application.py - 综合实际应用

这个示例通过图书管理系统综合运用所有面向对象编程概念：
- 类的设计和实例化
- 继承和多态
- 封装和数据保护
- 组合关系
- 实际业务逻辑的实现
"""

from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Set
from enum import Enum
import hashlib


# ==================== 枚举类型 ====================
class BookStatus(Enum):
    """图书状态"""
    AVAILABLE = "可借阅"
    BORROWED = "已借出"
    RESERVED = "已预约"
    MAINTENANCE = "维护中"
    LOST = "丢失"


class MemberType(Enum):
    """会员类型"""
    STUDENT = "学生"
    TEACHER = "教师"
    STAFF = "职工"
    VISITOR = "访客"


class TransactionType(Enum):
    """交易类型"""
    BORROW = "借阅"
    RETURN = "归还"
    RESERVE = "预约"
    RENEW = "续借"
    FINE = "罚款"


# ==================== 抽象基类 ====================
class LibraryItem(ABC):
    """图书馆物品抽象基类"""
    
    def __init__(self, item_id: str, title: str, author: str, publisher: str, 
                 publish_year: int, isbn: str = ""):
        """
        初始化图书馆物品
        
        参数:
            item_id: 物品ID
            title: 标题
            author: 作者
            publisher: 出版社
            publish_year: 出版年份
            isbn: ISBN号
        """
        self.item_id = item_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_year = publish_year
        self.isbn = isbn
        self.status = BookStatus.AVAILABLE
        self.location = "未分配"
        self.added_date = date.today()
        
        print(f"📚 {self.get_item_type()} 《{title}》已添加到图书馆")
    
    @abstractmethod
    def get_item_type(self) -> str:
        """获取物品类型"""
        pass
    
    @abstractmethod
    def get_borrow_period(self) -> int:
        """获取借阅期限（天数）"""
        pass
    
    @abstractmethod
    def calculate_fine(self, days_overdue: int) -> float:
        """计算罚款"""
        pass
    
    def is_available(self) -> bool:
        """检查是否可借阅"""
        return self.status == BookStatus.AVAILABLE
    
    def set_status(self, status: BookStatus, reason: str = ""):
        """设置状态"""
        old_status = self.status
        self.status = status
        print(f"📋 《{self.title}》状态: {old_status.value} → {status.value}" + 
              (f" ({reason})" if reason else ""))
    
    def get_basic_info(self) -> str:
        """获取基本信息"""
        return (f"📖 {self.get_item_type()} 信息:\n"
                f"   ID: {self.item_id}\n"
                f"   标题: {self.title}\n"
                f"   作者: {self.author}\n"
                f"   出版社: {self.publisher}\n"
                f"   出版年份: {self.publish_year}\n"
                f"   ISBN: {self.isbn}\n"
                f"   状态: {self.status.value}\n"
                f"   位置: {self.location}\n"
                f"   借阅期限: {self.get_borrow_period()}天")
    
    def __str__(self) -> str:
        return f"《{self.title}》- {self.author} ({self.status.value})"


# ==================== 具体物品类 ====================
class Book(LibraryItem):
    """图书类"""
    
    def __init__(self, item_id: str, title: str, author: str, publisher: str,
                 publish_year: int, isbn: str, pages: int, category: str):
        """
        初始化图书
        
        参数:
            item_id: 图书ID
            title: 书名
            author: 作者
            publisher: 出版社
            publish_year: 出版年份
            isbn: ISBN号
            pages: 页数
            category: 分类
        """
        super().__init__(item_id, title, author, publisher, publish_year, isbn)
        self.pages = pages
        self.category = category
        self.edition = 1
        self.language = "中文"
    
    def get_item_type(self) -> str:
        return "图书"
    
    def get_borrow_period(self) -> int:
        return 30  # 图书借阅期30天
    
    def calculate_fine(self, days_overdue: int) -> float:
        return days_overdue * 0.5  # 每天罚款0.5元


class Magazine(LibraryItem):
    """杂志类"""
    
    def __init__(self, item_id: str, title: str, publisher: str, 
                 publish_year: int, issue_number: str, month: int):
        """
        初始化杂志
        
        参数:
            item_id: 杂志ID
            title: 杂志名
            publisher: 出版社
            publish_year: 出版年份
            issue_number: 期号
            month: 月份
        """
        super().__init__(item_id, title, "编辑部", publisher, publish_year)
        self.issue_number = issue_number
        self.month = month
    
    def get_item_type(self) -> str:
        return "杂志"
    
    def get_borrow_period(self) -> int:
        return 7  # 杂志借阅期7天
    
    def calculate_fine(self, days_overdue: int) -> float:
        return days_overdue * 1.0  # 每天罚款1.0元


class DVD(LibraryItem):
    """DVD类"""
    
    def __init__(self, item_id: str, title: str, director: str, publisher: str,
                 publish_year: int, duration: int, genre: str):
        """
        初始化DVD
        
        参数:
            item_id: DVD ID
            title: 标题
            director: 导演
            publisher: 发行商
            publish_year: 发行年份
            duration: 时长（分钟）
            genre: 类型
        """
        super().__init__(item_id, title, director, publisher, publish_year)
        self.duration = duration
        self.genre = genre
        self.language = "中文"
        self.subtitles = ["中文", "英文"]
    
    def get_item_type(self) -> str:
        return "DVD"
    
    def get_borrow_period(self) -> int:
        return 3  # DVD借阅期3天
    
    def calculate_fine(self, days_overdue: int) -> float:
        return days_overdue * 2.0  # 每天罚款2.0元


# ==================== 会员类 ====================
class LibraryMember:
    """图书馆会员类 - 展示封装和数据保护"""
    
    def __init__(self, member_id: str, name: str, email: str, phone: str, 
                 member_type: MemberType):
        """
        初始化会员
        
        参数:
            member_id: 会员ID
            name: 姓名
            email: 邮箱
            phone: 电话
            member_type: 会员类型
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.member_type = member_type
        self.join_date = date.today()
        self.is_active = True
        
        # 私有属性
        self._password_hash = None
        self._borrowed_items: List[str] = []  # 借阅的物品ID列表
        self._reserved_items: List[str] = []  # 预约的物品ID列表
        self._fine_amount = 0.0
        self._borrow_history: List[Dict] = []
        
        print(f"👤 {member_type.value} 会员 {name} 已注册")
    
    @property
    def borrowed_count(self) -> int:
        """获取当前借阅数量"""
        return len(self._borrowed_items)
    
    @property
    def fine_amount(self) -> float:
        """获取罚款金额"""
        return self._fine_amount
    
    @property
    def max_borrow_limit(self) -> int:
        """获取最大借阅限制"""
        limits = {
            MemberType.STUDENT: 5,
            MemberType.TEACHER: 10,
            MemberType.STAFF: 8,
            MemberType.VISITOR: 2
        }
        return limits.get(self.member_type, 2)
    
    def set_password(self, password: str) -> bool:
        """设置密码"""
        if len(password) < 6:
            print("❌ 密码长度至少6位")
            return False
        
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
        print("✅ 密码设置成功")
        return True
    
    def verify_password(self, password: str) -> bool:
        """验证密码"""
        if not self._password_hash:
            return False
        return hashlib.sha256(password.encode()).hexdigest() == self._password_hash
    
    def can_borrow(self) -> bool:
        """检查是否可以借阅"""
        if not self.is_active:
            return False
        if self.borrowed_count >= self.max_borrow_limit:
            return False
        if self._fine_amount > 50:  # 罚款超过50元不能借阅
            return False
        return True
    
    def borrow_item(self, item_id: str):
        """借阅物品"""
        if item_id not in self._borrowed_items:
            self._borrowed_items.append(item_id)
    
    def return_item(self, item_id: str):
        """归还物品"""
        if item_id in self._borrowed_items:
            self._borrowed_items.remove(item_id)
    
    def add_fine(self, amount: float, reason: str = ""):
        """添加罚款"""
        self._fine_amount += amount
        print(f"💰 会员 {self.name} 产生罚款: ¥{amount:.2f}" + 
              (f" ({reason})" if reason else ""))
    
    def pay_fine(self, amount: float) -> bool:
        """缴纳罚款"""
        if amount <= 0 or amount > self._fine_amount:
            print("❌ 缴费金额无效")
            return False
        
        self._fine_amount -= amount
        print(f"💳 会员 {self.name} 缴纳罚款: ¥{amount:.2f}，余额: ¥{self._fine_amount:.2f}")
        return True
    
    def get_member_info(self) -> str:
        """获取会员信息"""
        return (f"👤 会员信息:\n"
                f"   ID: {self.member_id}\n"
                f"   姓名: {self.name}\n"
                f"   类型: {self.member_type.value}\n"
                f"   邮箱: {self.email}\n"
                f"   电话: {self.phone}\n"
                f"   加入日期: {self.join_date}\n"
                f"   状态: {'活跃' if self.is_active else '停用'}\n"
                f"   当前借阅: {self.borrowed_count}/{self.max_borrow_limit}\n"
                f"   待缴罚款: ¥{self._fine_amount:.2f}")
    
    def __str__(self) -> str:
        return f"{self.member_type.value} {self.name} ({self.member_id})"


# ==================== 借阅记录类 ====================
class BorrowRecord:
    """借阅记录类 - 展示组合关系"""
    
    def __init__(self, record_id: str, member: LibraryMember, item: LibraryItem):
        """
        初始化借阅记录
        
        参数:
            record_id: 记录ID
            member: 会员对象
            item: 物品对象
        """
        self.record_id = record_id
        self.member = member  # 组合关系：记录"有一个"会员
        self.item = item      # 组合关系：记录"有一个"物品
        self.borrow_date = date.today()
        self.due_date = self.borrow_date + timedelta(days=item.get_borrow_period())
        self.return_date: Optional[date] = None
        self.is_returned = False
        self.renewal_count = 0
        self.fine_paid = 0.0
    
    @property
    def days_overdue(self) -> int:
        """计算逾期天数"""
        if self.is_returned:
            if self.return_date > self.due_date:
                return (self.return_date - self.due_date).days
            return 0
        else:
            if date.today() > self.due_date:
                return (date.today() - self.due_date).days
            return 0
    
    @property
    def fine_amount(self) -> float:
        """计算罚款金额"""
        if self.days_overdue > 0:
            return self.item.calculate_fine(self.days_overdue)
        return 0.0
    
    def renew(self) -> bool:
        """续借"""
        if self.is_returned:
            print("❌ 已归还的物品无法续借")
            return False
        
        if self.renewal_count >= 2:
            print("❌ 续借次数已达上限")
            return False
        
        if self.days_overdue > 0:
            print("❌ 逾期物品无法续借")
            return False
        
        self.due_date += timedelta(days=self.item.get_borrow_period())
        self.renewal_count += 1
        print(f"📅 续借成功，新到期日: {self.due_date}")
        return True
    
    def return_item(self) -> float:
        """归还物品"""
        if self.is_returned:
            print("❌ 物品已归还")
            return 0.0
        
        self.return_date = date.today()
        self.is_returned = True
        
        fine = self.fine_amount
        if fine > 0:
            print(f"💰 逾期 {self.days_overdue} 天，产生罚款: ¥{fine:.2f}")
        
        return fine
    
    def get_record_info(self) -> str:
        """获取记录信息"""
        status = "已归还" if self.is_returned else "借阅中"
        overdue_info = f"逾期 {self.days_overdue} 天" if self.days_overdue > 0 else "正常"
        
        info = [
            f"📋 借阅记录:",
            f"   记录ID: {self.record_id}",
            f"   会员: {self.member.name}",
            f"   物品: {self.item.title}",
            f"   借阅日期: {self.borrow_date}",
            f"   到期日期: {self.due_date}",
            f"   状态: {status}",
            f"   续借次数: {self.renewal_count}",
            f"   逾期状态: {overdue_info}"
        ]
        
        if self.is_returned:
            info.append(f"   归还日期: {self.return_date}")
        
        if self.fine_amount > 0:
            info.append(f"   罚款金额: ¥{self.fine_amount:.2f}")
        
        return "\n".join(info)
    
    def __str__(self) -> str:
        status = "已归还" if self.is_returned else "借阅中"
        return f"{self.member.name} - 《{self.item.title}》({status})"


# ==================== 图书馆管理系统 ====================
class LibraryManagementSystem:
    """图书馆管理系统 - 综合应用所有OOP概念"""
    
    def __init__(self, library_name: str):
        """初始化图书馆管理系统"""
        self.library_name = library_name
        self.items: Dict[str, LibraryItem] = {}
        self.members: Dict[str, LibraryMember] = {}
        self.borrow_records: Dict[str, BorrowRecord] = {}
        self.next_record_id = 1
        
        print(f"🏛️  {library_name} 管理系统已启动")
    
    # ==================== 物品管理 ====================
    def add_item(self, item: LibraryItem):
        """添加物品"""
        if item.item_id in self.items:
            print(f"❌ 物品ID {item.item_id} 已存在")
            return False
        
        self.items[item.item_id] = item
        return True
    
    def find_item(self, item_id: str) -> Optional[LibraryItem]:
        """查找物品"""
        return self.items.get(item_id)
    
    def search_items(self, keyword: str) -> List[LibraryItem]:
        """搜索物品"""
        results = []
        keyword = keyword.lower()
        
        for item in self.items.values():
            if (keyword in item.title.lower() or 
                keyword in item.author.lower() or
                keyword in item.publisher.lower()):
                results.append(item)
        
        return results
    
    # ==================== 会员管理 ====================
    def register_member(self, member: LibraryMember) -> bool:
        """注册会员"""
        if member.member_id in self.members:
            print(f"❌ 会员ID {member.member_id} 已存在")
            return False
        
        self.members[member.member_id] = member
        return True
    
    def find_member(self, member_id: str) -> Optional[LibraryMember]:
        """查找会员"""
        return self.members.get(member_id)
    
    # ==================== 借阅管理 ====================
    def borrow_item(self, member_id: str, item_id: str) -> bool:
        """借阅物品"""
        member = self.find_member(member_id)
        item = self.find_item(item_id)
        
        if not member:
            print(f"❌ 会员 {member_id} 不存在")
            return False
        
        if not item:
            print(f"❌ 物品 {item_id} 不存在")
            return False
        
        if not member.can_borrow():
            print(f"❌ 会员 {member.name} 无法借阅（达到限制或有罚款）")
            return False
        
        if not item.is_available():
            print(f"❌ 《{item.title}》当前不可借阅")
            return False
        
        # 创建借阅记录
        record_id = f"BR{self.next_record_id:06d}"
        self.next_record_id += 1
        
        record = BorrowRecord(record_id, member, item)
        self.borrow_records[record_id] = record
        
        # 更新状态
        member.borrow_item(item_id)
        item.set_status(BookStatus.BORROWED, f"借给 {member.name}")
        
        print(f"📚 借阅成功: {member.name} 借阅《{item.title}》")
        print(f"   到期日期: {record.due_date}")
        return True
    
    def return_item(self, member_id: str, item_id: str) -> bool:
        """归还物品"""
        # 查找借阅记录
        record = None
        for r in self.borrow_records.values():
            if (r.member.member_id == member_id and 
                r.item.item_id == item_id and 
                not r.is_returned):
                record = r
                break
        
        if not record:
            print(f"❌ 未找到有效的借阅记录")
            return False
        
        # 归还处理
        fine = record.return_item()
        
        # 更新状态
        record.member.return_item(item_id)
        record.item.set_status(BookStatus.AVAILABLE, "已归还")
        
        # 处理罚款
        if fine > 0:
            record.member.add_fine(fine, "逾期罚款")
        
        print(f"📚 归还成功: {record.member.name} 归还《{record.item.title}》")
        return True
    
    def renew_item(self, member_id: str, item_id: str) -> bool:
        """续借物品"""
        # 查找借阅记录
        record = None
        for r in self.borrow_records.values():
            if (r.member.member_id == member_id and 
                r.item.item_id == item_id and 
                not r.is_returned):
                record = r
                break
        
        if not record:
            print(f"❌ 未找到有效的借阅记录")
            return False
        
        return record.renew()
    
    # ==================== 查询和统计 ====================
    def get_member_borrowed_items(self, member_id: str) -> List[BorrowRecord]:
        """获取会员当前借阅的物品"""
        records = []
        for record in self.borrow_records.values():
            if (record.member.member_id == member_id and 
                not record.is_returned):
                records.append(record)
        return records
    
    def get_overdue_items(self) -> List[BorrowRecord]:
        """获取逾期物品"""
        overdue_records = []
        for record in self.borrow_records.values():
            if not record.is_returned and record.days_overdue > 0:
                overdue_records.append(record)
        return overdue_records
    
    def get_library_statistics(self) -> str:
        """获取图书馆统计信息"""
        total_items = len(self.items)
        total_members = len(self.members)
        total_records = len(self.borrow_records)
        
        # 按状态统计物品
        status_counts = {}
        for item in self.items.values():
            status = item.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # 按类型统计物品
        type_counts = {}
        for item in self.items.values():
            item_type = item.get_item_type()
            type_counts[item_type] = type_counts.get(item_type, 0) + 1
        
        # 按类型统计会员
        member_type_counts = {}
        for member in self.members.values():
            member_type = member.member_type
            member_type_counts[member_type] = member_type_counts.get(member_type, 0) + 1
        
        # 逾期统计
        overdue_count = len(self.get_overdue_items())
        
        stats = [
            f"📊 {self.library_name} 统计信息:",
            f"   总物品数: {total_items}",
            f"   总会员数: {total_members}",
            f"   总借阅记录: {total_records}",
            f"   逾期物品: {overdue_count}",
            "",
            "📚 物品状态分布:"
        ]
        
        for status, count in status_counts.items():
            percentage = count / total_items * 100 if total_items > 0 else 0
            stats.append(f"   {status.value}: {count} ({percentage:.1f}%)")
        
        stats.append("\n📖 物品类型分布:")
        for item_type, count in type_counts.items():
            percentage = count / total_items * 100 if total_items > 0 else 0
            stats.append(f"   {item_type}: {count} ({percentage:.1f}%)")
        
        stats.append("\n👥 会员类型分布:")
        for member_type, count in member_type_counts.items():
            percentage = count / total_members * 100 if total_members > 0 else 0
            stats.append(f"   {member_type.value}: {count} ({percentage:.1f}%)")
        
        return "\n".join(stats)
    
    def generate_overdue_report(self):
        """生成逾期报告"""
        overdue_records = self.get_overdue_items()
        
        if not overdue_records:
            print("✅ 没有逾期物品")
            return
        
        print(f"\n⚠️  逾期物品报告 (共{len(overdue_records)}项):")
        print("-" * 80)
        
        total_fine = 0
        for record in sorted(overdue_records, key=lambda r: r.days_overdue, reverse=True):
            fine = record.fine_amount
            total_fine += fine
            print(f"📋 {record.member.name} - 《{record.item.title}》")
            print(f"   逾期: {record.days_overdue}天, 罚款: ¥{fine:.2f}")
            print(f"   联系方式: {record.member.email}, {record.member.phone}")
            print()
        
        print(f"💰 总罚款金额: ¥{total_fine:.2f}")
        print("-" * 80)


# ==================== 演示函数 ====================
def demo_library_system():
    """图书馆管理系统综合演示"""
    print("=" * 80)
    print("🏛️  图书馆管理系统 - 面向对象综合应用演示")
    print("=" * 80)
    
    # 创建图书馆管理系统
    library = LibraryManagementSystem("Python大学图书馆")
    
    print(f"\n{'='*20} 添加图书馆物品 {'='*20}")
    
    # 添加各种类型的物品
    items = [
        Book("B001", "Python编程从入门到实践", "埃里克·马瑟斯", "人民邮电出版社", 
             2019, "9787115428028", 459, "计算机"),
        Book("B002", "算法导论", "托马斯·科尔曼", "机械工业出版社", 
             2012, "9787111407010", 780, "计算机"),
        Magazine("M001", "程序员", "电子工业出版社", 2024, "2024-03", 3),
        Magazine("M002", "科学美国人", "环球科学杂志社", 2024, "2024-02", 2),
        DVD("D001", "黑客帝国", "沃卓斯基姐妹", "华纳兄弟", 1999, 136, "科幻"),
        DVD("D002", "阿凡达", "詹姆斯·卡梅隆", "二十世纪福克斯", 2009, 162, "科幻")
    ]
    
    for item in items:
        library.add_item(item)
        item.location = f"区域{item.item_id[0]}-{item.item_id[1:]}"
    
    print(f"\n{'='*20} 注册会员 {'='*20}")
    
    # 注册不同类型的会员
    members = [
        LibraryMember("S001", "张三", "zhangsan@student.edu", "13800138001", MemberType.STUDENT),
        LibraryMember("T001", "李老师", "li@teacher.edu", "13800138002", MemberType.TEACHER),
        LibraryMember("F001", "王职工", "wang@staff.edu", "13800138003", MemberType.STAFF),
        LibraryMember("V001", "赵访客", "zhao@visitor.com", "13800138004", MemberType.VISITOR)
    ]
    
    for member in members:
        library.register_member(member)
        member.set_password("123456")
    
    print(f"\n{'='*20} 借阅操作演示 {'='*20}")
    
    # 借阅操作
    borrow_operations = [
        ("S001", "B001"),  # 学生借书
        ("S001", "M001"),  # 学生借杂志
        ("T001", "B002"),  # 老师借书
        ("T001", "D001"),  # 老师借DVD
        ("F001", "M002"),  # 职工借杂志
        ("V001", "D002"),  # 访客借DVD
    ]
    
    for member_id, item_id in borrow_operations:
        print(f"\n📚 {member_id} 借阅 {item_id}:")
        library.borrow_item(member_id, item_id)
    
    # 测试借阅限制
    print(f"\n🧪 测试借阅限制:")
    library.borrow_item("V001", "B001")  # 访客已达借阅上限
    
    print(f"\n{'='*20} 会员信息查询 {'='*20}")
    
    # 查询会员借阅情况
    for member in members[:2]:  # 只显示前两个会员
        print(f"\n{member.get_member_info()}")
        
        borrowed_items = library.get_member_borrowed_items(member.member_id)
        if borrowed_items:
            print(f"\n当前借阅物品:")
            for record in borrowed_items:
                print(f"   - 《{record.item.title}》(到期: {record.due_date})")
    
    print(f"\n{'='*20} 续借和归还演示 {'='*20}")
    
    # 续借演示
    print(f"\n📅 续借演示:")
    library.renew_item("S001", "B001")
    library.renew_item("T001", "D001")
    
    # 归还演示
    print(f"\n📚 归还演示:")
    library.return_item("S001", "M001")
    library.return_item("F001", "M002")
    
    print(f"\n{'='*20} 搜索功能演示 {'='*20}")
    
    # 搜索功能
    print(f"\n🔍 搜索演示:")
    search_results = library.search_items("Python")
    print(f"搜索'Python'的结果:")
    for item in search_results:
        print(f"   - {item}")
    
    search_results = library.search_items("科幻")
    print(f"\n搜索'科幻'的结果:")
    for item in search_results:
        print(f"   - {item}")
    
    print(f"\n{'='*20} 模拟逾期情况 {'='*20}")
    
    # 模拟逾期（修改借阅记录的日期）
    print(f"\n⏰ 模拟逾期情况:")
    for record in library.borrow_records.values():
        if not record.is_returned and record.item.item_id == "D001":
            # 将借阅日期设为10天前
            record.borrow_date = date.today() - timedelta(days=15)
            record.due_date = record.borrow_date + timedelta(days=record.item.get_borrow_period())
            print(f"模拟 {record.member.name} 的《{record.item.title}》逾期")
    
    print(f"\n{'='*20} 逾期处理 {'='*20}")
    
    # 生成逾期报告
    library.generate_overdue_report()
    
    # 归还逾期物品
    print(f"\n📚 归还逾期物品:")
    library.return_item("T001", "D001")
    
    # 缴纳罚款
    teacher = library.find_member("T001")
    if teacher and teacher.fine_amount > 0:
        teacher.pay_fine(teacher.fine_amount)
    
    print(f"\n{'='*20} 系统统计 {'='*20}")
    
    # 系统统计
    print(f"\n{library.get_library_statistics()}")
    
    print(f"\n{'='*20} 物品详细信息 {'='*20}")
    
    # 显示部分物品详细信息
    for item in list(library.items.values())[:2]:
        print(f"\n{item.get_basic_info()}")
    
    print("\n" + "=" * 80)
    print("🎉 图书馆管理系统演示完成!")
    print("💡 本示例综合运用了以下OOP概念:")
    print("   ✅ 抽象基类和继承 (LibraryItem -> Book/Magazine/DVD)")
    print("   ✅ 多态性 (不同物品类型的统一处理)")
    print("   ✅ 封装和数据保护 (会员密码、私有属性)")
    print("   ✅ 组合关系 (BorrowRecord包含Member和Item)")
    print("   ✅ 属性装饰器 (只读属性、计算属性)")
    print("   ✅ 枚举类型 (状态管理)")
    print("   ✅ 实际业务逻辑 (借阅规则、罚款计算)")
    print("=" * 80)


if __name__ == "__main__":
    demo_library_system()
