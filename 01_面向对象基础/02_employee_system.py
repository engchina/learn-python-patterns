"""
02_employee_system.py - 实际的员工管理系统

这个示例展示如何将现实世界的业务需求建模为面向对象的系统：
- 实际业务场景的类设计
- 数据封装和验证
- 业务逻辑的实现
- 系统功能的组织
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from enum import Enum


# ==================== 枚举类型定义 ====================
class Department(Enum):
    """部门枚举"""
    ENGINEERING = "工程部"
    MARKETING = "市场部"
    SALES = "销售部"
    HR = "人力资源部"
    FINANCE = "财务部"
    OPERATIONS = "运营部"


class EmployeeStatus(Enum):
    """员工状态枚举"""
    ACTIVE = "在职"
    ON_LEAVE = "请假"
    TERMINATED = "离职"
    SUSPENDED = "停职"


# ==================== 员工类 ====================
class Employee:
    """员工类 - 展示实际业务建模"""
    
    # 类属性
    company_name = "Python科技有限公司"
    next_employee_id = 1001
    
    def __init__(self, first_name: str, last_name: str, email: str, 
                 department: Department, base_salary: float):
        """
        初始化员工对象
        
        参数:
            first_name: 名
            last_name: 姓
            email: 邮箱
            department: 部门
            base_salary: 基本工资
        """
        # 基本信息
        self.employee_id = Employee.next_employee_id
        Employee.next_employee_id += 1
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        
        # 薪资信息（使用私有属性保护敏感数据）
        self._base_salary = base_salary
        self._bonus = 0.0
        self._benefits = 2000.0  # 默认福利
        
        # 工作信息
        self.hire_date = date.today()
        self.status = EmployeeStatus.ACTIVE
        self.manager_id: Optional[int] = None
        
        # 绩效记录
        self.performance_reviews: List[Dict] = []
        self.training_records: List[Dict] = []
        
        print(f"✅ 员工 {self.get_full_name()} 已入职，员工ID: {self.employee_id}")
    
    @property
    def base_salary(self) -> float:
        """获取基本工资（属性装饰器）"""
        return self._base_salary
    
    @base_salary.setter
    def base_salary(self, value: float):
        """设置基本工资（带验证）"""
        if value < 0:
            raise ValueError("工资不能为负数")
        if value > 1000000:
            print("⚠️  工资异常高，请确认是否正确")
        self._base_salary = value
        print(f"💰 {self.get_full_name()} 的基本工资已更新为: ¥{value:,.2f}")
    
    @property
    def bonus(self) -> float:
        """获取奖金"""
        return self._bonus
    
    @bonus.setter
    def bonus(self, value: float):
        """设置奖金"""
        if value < 0:
            raise ValueError("奖金不能为负数")
        self._bonus = value
        print(f"🎁 {self.get_full_name()} 的奖金已设置为: ¥{value:,.2f}")
    
    def get_full_name(self) -> str:
        """获取全名"""
        return f"{self.last_name}{self.first_name}"
    
    def get_total_compensation(self) -> float:
        """计算总薪酬"""
        return self._base_salary + self._bonus + self._benefits
    
    def add_performance_review(self, rating: float, comments: str, reviewer: str):
        """
        添加绩效评估
        
        参数:
            rating: 评分（1-5分）
            comments: 评价
            reviewer: 评估人
        """
        if not 1 <= rating <= 5:
            raise ValueError("评分必须在1-5之间")
        
        review = {
            "date": date.today(),
            "rating": rating,
            "comments": comments,
            "reviewer": reviewer
        }
        self.performance_reviews.append(review)
        print(f"📝 {self.get_full_name()} 的绩效评估已添加，评分: {rating}/5")
    
    def add_training_record(self, course_name: str, completion_date: date, 
                          certificate: bool = False):
        """
        添加培训记录
        
        参数:
            course_name: 课程名称
            completion_date: 完成日期
            certificate: 是否获得证书
        """
        training = {
            "course_name": course_name,
            "completion_date": completion_date,
            "certificate": certificate,
            "added_date": date.today()
        }
        self.training_records.append(training)
        cert_status = "并获得证书" if certificate else ""
        print(f"🎓 {self.get_full_name()} 完成培训: {course_name} {cert_status}")
    
    def get_average_performance(self) -> float:
        """获取平均绩效评分"""
        if not self.performance_reviews:
            return 0.0
        
        total_rating = sum(review["rating"] for review in self.performance_reviews)
        return round(total_rating / len(self.performance_reviews), 2)
    
    def get_years_of_service(self) -> float:
        """获取工作年限"""
        today = date.today()
        days_worked = (today - self.hire_date).days
        return round(days_worked / 365.25, 2)
    
    def is_eligible_for_promotion(self) -> bool:
        """判断是否符合晋升条件"""
        # 简单的晋升条件：工作满1年且平均绩效>=4分
        return (self.get_years_of_service() >= 1.0 and 
                self.get_average_performance() >= 4.0)
    
    def update_status(self, new_status: EmployeeStatus, reason: str = ""):
        """
        更新员工状态
        
        参数:
            new_status: 新状态
            reason: 变更原因
        """
        old_status = self.status
        self.status = new_status
        
        status_msg = f"📋 {self.get_full_name()} 状态变更: {old_status.value} → {new_status.value}"
        if reason:
            status_msg += f" (原因: {reason})"
        print(status_msg)
    
    def get_employee_summary(self) -> str:
        """获取员工摘要信息"""
        summary = [
            f"👤 员工信息摘要:",
            f"   ID: {self.employee_id}",
            f"   姓名: {self.get_full_name()}",
            f"   邮箱: {self.email}",
            f"   部门: {self.department.value}",
            f"   状态: {self.status.value}",
            f"   入职日期: {self.hire_date}",
            f"   工作年限: {self.get_years_of_service()}年",
            f"   基本工资: ¥{self._base_salary:,.2f}",
            f"   奖金: ¥{self._bonus:,.2f}",
            f"   福利: ¥{self._benefits:,.2f}",
            f"   总薪酬: ¥{self.get_total_compensation():,.2f}",
            f"   平均绩效: {self.get_average_performance()}/5",
            f"   培训次数: {len(self.training_records)}次",
            f"   晋升资格: {'符合' if self.is_eligible_for_promotion() else '不符合'}"
        ]
        return "\n".join(summary)
    
    def __str__(self) -> str:
        """字符串表示"""
        return (f"Employee(ID={self.employee_id}, 姓名={self.get_full_name()}, "
                f"部门={self.department.value}, 状态={self.status.value})")
    
    def __repr__(self) -> str:
        """官方字符串表示"""
        return (f"Employee(employee_id={self.employee_id}, "
                f"first_name='{self.first_name}', last_name='{self.last_name}', "
                f"department={self.department}, base_salary={self._base_salary})")


# ==================== 人力资源管理系统 ====================
class HRSystem:
    """人力资源管理系统 - 展示系统级功能"""
    
    def __init__(self, company_name: str = "Python科技有限公司"):
        """初始化HR系统"""
        self.company_name = company_name
        self.employees: Dict[int, Employee] = {}
        self.department_budgets: Dict[Department, float] = {
            Department.ENGINEERING: 500000,
            Department.MARKETING: 300000,
            Department.SALES: 400000,
            Department.HR: 200000,
            Department.FINANCE: 250000,
            Department.OPERATIONS: 350000
        }
        print(f"🏢 {company_name} HR系统已启动")
    
    def hire_employee(self, first_name: str, last_name: str, email: str,
                     department: Department, base_salary: float) -> Employee:
        """
        招聘员工
        
        参数:
            first_name: 名
            last_name: 姓
            email: 邮箱
            department: 部门
            base_salary: 基本工资
            
        返回:
            Employee对象
        """
        # 验证邮箱唯一性
        for emp in self.employees.values():
            if emp.email == email:
                raise ValueError(f"邮箱 {email} 已被使用")
        
        # 检查部门预算
        dept_total_salary = self.get_department_total_salary(department)
        if dept_total_salary + base_salary > self.department_budgets[department]:
            print(f"⚠️  警告: {department.value} 预算可能超支")
        
        # 创建员工
        employee = Employee(first_name, last_name, email, department, base_salary)
        self.employees[employee.employee_id] = employee
        
        return employee
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """根据ID获取员工"""
        return self.employees.get(employee_id)
    
    def find_employees_by_department(self, department: Department) -> List[Employee]:
        """根据部门查找员工"""
        return [emp for emp in self.employees.values() 
                if emp.department == department and emp.status == EmployeeStatus.ACTIVE]
    
    def find_employees_by_name(self, name: str) -> List[Employee]:
        """根据姓名查找员工"""
        return [emp for emp in self.employees.values() 
                if name.lower() in emp.get_full_name().lower()]
    
    def get_department_total_salary(self, department: Department) -> float:
        """获取部门总薪资"""
        dept_employees = self.find_employees_by_department(department)
        return sum(emp.get_total_compensation() for emp in dept_employees)
    
    def get_high_performers(self, min_rating: float = 4.0) -> List[Employee]:
        """获取高绩效员工"""
        return [emp for emp in self.employees.values() 
                if emp.get_average_performance() >= min_rating and 
                emp.status == EmployeeStatus.ACTIVE]
    
    def get_promotion_candidates(self) -> List[Employee]:
        """获取晋升候选人"""
        return [emp for emp in self.employees.values() 
                if emp.is_eligible_for_promotion() and emp.status == EmployeeStatus.ACTIVE]
    
    def generate_company_report(self) -> str:
        """生成公司报告"""
        active_employees = [emp for emp in self.employees.values() 
                          if emp.status == EmployeeStatus.ACTIVE]
        
        if not active_employees:
            return "📊 暂无在职员工数据"
        
        total_employees = len(active_employees)
        total_payroll = sum(emp.get_total_compensation() for emp in active_employees)
        avg_salary = total_payroll / total_employees
        avg_performance = sum(emp.get_average_performance() for emp in active_employees) / total_employees
        
        # 部门分布
        dept_distribution = {}
        for emp in active_employees:
            dept = emp.department
            dept_distribution[dept] = dept_distribution.get(dept, 0) + 1
        
        report = [
            f"📊 {self.company_name} 人力资源报告",
            f"   报告日期: {date.today()}",
            f"   在职员工总数: {total_employees}人",
            f"   总薪资支出: ¥{total_payroll:,.2f}",
            f"   平均薪资: ¥{avg_salary:,.2f}",
            f"   平均绩效: {avg_performance:.2f}/5",
            "",
            "📈 部门分布:",
        ]
        
        for dept, count in dept_distribution.items():
            percentage = count / total_employees * 100
            dept_salary = self.get_department_total_salary(dept)
            budget_usage = dept_salary / self.department_budgets[dept] * 100
            report.append(f"   {dept.value}: {count}人 ({percentage:.1f}%) - "
                         f"预算使用率: {budget_usage:.1f}%")
        
        # 高绩效员工
        high_performers = self.get_high_performers()
        promotion_candidates = self.get_promotion_candidates()
        
        report.extend([
            "",
            f"🌟 高绩效员工: {len(high_performers)}人",
            f"🚀 晋升候选人: {len(promotion_candidates)}人"
        ])
        
        return "\n".join(report)
    
    def list_all_employees(self):
        """列出所有员工"""
        if not self.employees:
            print("📝 暂无员工记录")
            return
        
        print(f"\n📋 员工名单 (共{len(self.employees)}人):")
        print("-" * 80)
        
        for emp in self.employees.values():
            status_icon = "✅" if emp.status == EmployeeStatus.ACTIVE else "❌"
            print(f"{status_icon} {emp}")
        
        print("-" * 80)


# ==================== 演示函数 ====================
def demo_employee_system():
    """员工管理系统演示"""
    print("=" * 80)
    print("🏢 员工管理系统演示")
    print("=" * 80)
    
    # 创建HR系统
    hr_system = HRSystem()
    
    print(f"\n{'='*20} 员工招聘 {'='*20}")
    
    # 招聘员工
    employees_data = [
        ("张", "伟", "zhang.wei@company.com", Department.ENGINEERING, 15000),
        ("李", "娜", "li.na@company.com", Department.MARKETING, 12000),
        ("王", "强", "wang.qiang@company.com", Department.SALES, 13000),
        ("赵", "敏", "zhao.min@company.com", Department.HR, 11000),
        ("刘", "洋", "liu.yang@company.com", Department.FINANCE, 14000),
        ("陈", "静", "chen.jing@company.com", Department.ENGINEERING, 16000)
    ]
    
    employees = []
    for first_name, last_name, email, dept, salary in employees_data:
        try:
            emp = hr_system.hire_employee(first_name, last_name, email, dept, salary)
            employees.append(emp)
        except ValueError as e:
            print(f"❌ 招聘失败: {e}")
    
    print(f"\n{'='*20} 员工发展 {'='*20}")
    
    # 添加绩效评估和培训记录
    if len(employees) >= 3:
        # 张伟的记录
        employees[0].add_performance_review(4.5, "技术能力强，团队合作好", "技术总监")
        employees[0].add_performance_review(4.2, "项目完成质量高", "项目经理")
        employees[0].add_training_record("Python高级编程", date(2024, 1, 15), True)
        employees[0].add_training_record("项目管理", date(2024, 2, 20), False)
        
        # 李娜的记录
        employees[1].add_performance_review(3.8, "市场分析能力不错", "市场总监")
        employees[1].add_training_record("数字营销", date(2024, 1, 10), True)
        employees[1].bonus = 5000  # 设置奖金
        
        # 王强的记录
        employees[2].add_performance_review(4.1, "销售业绩优秀", "销售总监")
        employees[2].add_performance_review(4.3, "客户关系维护好", "销售总监")
        employees[2].bonus = 8000
    
    print(f"\n{'='*20} 薪资调整 {'='*20}")
    
    # 薪资调整演示
    if employees:
        print(f"\n💰 为优秀员工调薪:")
        employees[0].base_salary = 18000  # 张伟加薪
        
        # 测试异常情况
        try:
            employees[1].base_salary = -1000  # 无效工资
        except ValueError as e:
            print(f"❌ 薪资设置失败: {e}")
    
    print(f"\n{'='*20} 员工信息展示 {'='*20}")
    
    # 显示员工详细信息
    for emp in employees[:2]:  # 只显示前两个员工的详细信息
        print(f"\n{emp.get_employee_summary()}")
    
    print(f"\n{'='*20} 查找和筛选 {'='*20}")
    
    # 部门查找
    print(f"\n🔍 工程部员工:")
    eng_employees = hr_system.find_employees_by_department(Department.ENGINEERING)
    for emp in eng_employees:
        print(f"   {emp}")
    
    # 高绩效员工
    print(f"\n🌟 高绩效员工:")
    high_performers = hr_system.get_high_performers()
    for emp in high_performers:
        print(f"   {emp} - 平均绩效: {emp.get_average_performance()}/5")
    
    # 晋升候选人
    print(f"\n🚀 晋升候选人:")
    candidates = hr_system.get_promotion_candidates()
    for emp in candidates:
        print(f"   {emp} - 工作年限: {emp.get_years_of_service()}年, "
              f"平均绩效: {emp.get_average_performance()}/5")
    
    print(f"\n{'='*20} 员工状态管理 {'='*20}")
    
    # 员工状态变更
    if employees:
        employees[-1].update_status(EmployeeStatus.ON_LEAVE, "产假")
    
    print(f"\n{'='*20} 系统报告 {'='*20}")
    
    # 生成公司报告
    print(f"\n{hr_system.generate_company_report()}")
    
    # 列出所有员工
    hr_system.list_all_employees()
    
    print("\n" + "=" * 80)
    print("🎉 员工管理系统演示完成!")
    print("💡 关键点:")
    print("   - 使用枚举类型提高代码可读性和安全性")
    print("   - 属性装饰器保护敏感数据并添加验证")
    print("   - 业务逻辑封装在方法中，便于维护")
    print("   - 系统级功能通过管理类实现")
    print("=" * 80)


if __name__ == "__main__":
    demo_employee_system()
