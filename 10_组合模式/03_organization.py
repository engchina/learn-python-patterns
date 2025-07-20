"""
组合模式企业应用 - 组织架构管理系统

这个示例展示了组合模式在企业组织架构中的应用，演示如何管理
复杂的组织结构，计算薪资和统计人员信息。

作者: Composite Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class EmployeeLevel(Enum):
    """员工级别枚举"""
    INTERN = "实习生"
    JUNIOR = "初级"
    SENIOR = "高级"
    LEAD = "主管"
    MANAGER = "经理"
    DIRECTOR = "总监"
    VP = "副总裁"
    CEO = "首席执行官"


class OrganizationComponent(ABC):
    """组织架构组件抽象基类"""
    
    def __init__(self, name: str, level: EmployeeLevel):
        self.name = name
        self.level = level
        self.join_date = datetime.now()
    
    @abstractmethod
    def get_salary_total(self) -> float:
        """获取总薪资"""
        pass
    
    @abstractmethod
    def get_employee_count(self) -> int:
        """获取员工总数"""
        pass
    
    @abstractmethod
    def display_structure(self, indent: int = 0) -> str:
        """显示组织结构"""
        pass
    
    def get_level_icon(self) -> str:
        """根据级别获取图标"""
        icons = {
            EmployeeLevel.INTERN: "🎓",
            EmployeeLevel.JUNIOR: "👨‍💻",
            EmployeeLevel.SENIOR: "👨‍💼",
            EmployeeLevel.LEAD: "👨‍🏫",
            EmployeeLevel.MANAGER: "👨‍💼",
            EmployeeLevel.DIRECTOR: "👨‍💼",
            EmployeeLevel.VP: "👔",
            EmployeeLevel.CEO: "👑"
        }
        return icons.get(self.level, "👤")


class Employee(OrganizationComponent):
    """员工类 - 叶子组件"""
    
    def __init__(self, name: str, level: EmployeeLevel, salary: float, 
                 department: str = "", skills: List[str] = None):
        super().__init__(name, level)
        self.salary = salary
        self.department = department
        self.skills = skills or []
        self.performance_rating = 3.0  # 1-5分制
    
    def get_salary_total(self) -> float:
        """获取员工薪资"""
        return self.salary
    
    def get_employee_count(self) -> int:
        """员工数量（自己）"""
        return 1
    
    def display_structure(self, indent: int = 0) -> str:
        """显示员工信息"""
        prefix = "  " * indent
        icon = self.get_level_icon()
        return (f"{prefix}{icon} {self.name} - {self.level.value} "
                f"(薪资: ¥{self.salary:,.0f}, 评分: {self.performance_rating})")
    
    def add_skill(self, skill: str) -> None:
        """添加技能"""
        if skill not in self.skills:
            self.skills.append(skill)
            print(f"✅ 为 {self.name} 添加技能: {skill}")
    
    def set_performance_rating(self, rating: float) -> None:
        """设置绩效评分"""
        if 1.0 <= rating <= 5.0:
            self.performance_rating = rating
            print(f"📊 {self.name} 的绩效评分已更新为: {rating}")
        else:
            print("⚠️  绩效评分必须在1.0-5.0之间")
    
    def get_info(self) -> Dict:
        """获取员工详细信息"""
        return {
            "name": self.name,
            "level": self.level.value,
            "salary": self.salary,
            "department": self.department,
            "skills": self.skills,
            "performance": self.performance_rating,
            "join_date": self.join_date.strftime("%Y-%m-%d")
        }


class Department(OrganizationComponent):
    """部门类 - 组合组件"""
    
    def __init__(self, name: str, manager: Optional[Employee] = None):
        # 部门级别基于经理级别
        level = manager.level if manager else EmployeeLevel.MANAGER
        super().__init__(name, level)
        self.manager = manager
        self._members: List[OrganizationComponent] = []
        self.budget = 0.0
        
        if manager:
            self._members.append(manager)
    
    def get_salary_total(self) -> float:
        """获取部门总薪资"""
        return sum(member.get_salary_total() for member in self._members)
    
    def get_employee_count(self) -> int:
        """获取部门总人数"""
        return sum(member.get_employee_count() for member in self._members)
    
    def display_structure(self, indent: int = 0) -> str:
        """显示部门结构"""
        prefix = "  " * indent
        result = [f"{prefix}🏢 部门: {self.name}"]
        
        if self.manager:
            result.append(f"{prefix}  👨‍💼 部门经理: {self.manager.name}")
        
        result.append(f"{prefix}  📊 统计: {self.get_employee_count()} 人, "
                     f"总薪资: ¥{self.get_salary_total():,.0f}")
        
        # 显示成员
        for member in self._members:
            result.append(member.display_structure(indent + 1))
        
        return "\n".join(result)
    
    def add_member(self, member: OrganizationComponent) -> None:
        """添加部门成员"""
        if member not in self._members:
            self._members.append(member)
            member_type = "员工" if isinstance(member, Employee) else "子部门"
            print(f"✅ {member_type} '{member.name}' 已加入部门 '{self.name}'")
        else:
            print(f"⚠️  '{member.name}' 已在部门 '{self.name}' 中")
    
    def remove_member(self, member: OrganizationComponent) -> None:
        """移除部门成员"""
        if member in self._members and member != self.manager:
            self._members.remove(member)
            member_type = "员工" if isinstance(member, Employee) else "子部门"
            print(f"❌ {member_type} '{member.name}' 已离开部门 '{self.name}'")
        elif member == self.manager:
            print(f"⚠️  不能移除部门经理 '{member.name}'")
        else:
            print(f"⚠️  '{member.name}' 不在部门 '{self.name}' 中")
    
    def find_employee(self, name: str) -> Optional[Employee]:
        """查找员工"""
        for member in self._members:
            if isinstance(member, Employee) and member.name == name:
                return member
            elif isinstance(member, Department):
                found = member.find_employee(name)
                if found:
                    return found
        return None
    
    def get_employees_by_level(self, level: EmployeeLevel) -> List[Employee]:
        """按级别获取员工"""
        employees = []
        for member in self._members:
            if isinstance(member, Employee) and member.level == level:
                employees.append(member)
            elif isinstance(member, Department):
                employees.extend(member.get_employees_by_level(level))
        return employees
    
    def get_department_statistics(self) -> Dict:
        """获取部门统计信息"""
        stats = {
            "total_employees": self.get_employee_count(),
            "total_salary": self.get_salary_total(),
            "average_salary": 0,
            "level_distribution": {},
            "average_performance": 0
        }
        
        # 收集所有员工信息
        all_employees = []
        self._collect_employees(all_employees)
        
        if all_employees:
            stats["average_salary"] = stats["total_salary"] / len(all_employees)
            stats["average_performance"] = sum(emp.performance_rating for emp in all_employees) / len(all_employees)
            
            # 统计级别分布
            for emp in all_employees:
                level_name = emp.level.value
                stats["level_distribution"][level_name] = stats["level_distribution"].get(level_name, 0) + 1
        
        return stats
    
    def _collect_employees(self, employee_list: List[Employee]) -> None:
        """递归收集所有员工"""
        for member in self._members:
            if isinstance(member, Employee):
                employee_list.append(member)
            elif isinstance(member, Department):
                member._collect_employees(employee_list)
    
    def set_budget(self, budget: float) -> None:
        """设置部门预算"""
        self.budget = budget
        print(f"💰 部门 '{self.name}' 预算设置为: ¥{budget:,.0f}")
    
    def check_budget_status(self) -> Dict:
        """检查预算状态"""
        total_salary = self.get_salary_total()
        remaining = self.budget - total_salary
        utilization = (total_salary / self.budget * 100) if self.budget > 0 else 0
        
        return {
            "budget": self.budget,
            "used": total_salary,
            "remaining": remaining,
            "utilization_percent": utilization,
            "over_budget": remaining < 0
        }


def demo_organization():
    """组织架构演示"""
    print("=" * 60)
    print("🏢 企业组织架构管理 - 组合模式演示")
    print("=" * 60)
    
    # 创建高层管理
    ceo = Employee("张总", EmployeeLevel.CEO, 500000, "管理层")
    cto = Employee("李总", EmployeeLevel.VP, 400000, "技术")
    hr_director = Employee("王总监", EmployeeLevel.DIRECTOR, 300000, "人力资源")
    
    # 创建技术部门经理和员工
    dev_manager = Employee("赵经理", EmployeeLevel.MANAGER, 250000, "开发部")
    qa_manager = Employee("钱经理", EmployeeLevel.MANAGER, 220000, "测试部")
    
    # 开发团队
    senior_dev1 = Employee("孙工程师", EmployeeLevel.SENIOR, 180000, "开发部", ["Python", "Django", "React"])
    senior_dev2 = Employee("周工程师", EmployeeLevel.SENIOR, 175000, "开发部", ["Java", "Spring", "MySQL"])
    junior_dev1 = Employee("吴工程师", EmployeeLevel.JUNIOR, 120000, "开发部", ["Python", "Flask"])
    junior_dev2 = Employee("郑工程师", EmployeeLevel.JUNIOR, 115000, "开发部", ["JavaScript", "Vue"])
    
    # 测试团队
    senior_qa = Employee("冯工程师", EmployeeLevel.SENIOR, 160000, "测试部", ["自动化测试", "性能测试"])
    junior_qa = Employee("陈工程师", EmployeeLevel.JUNIOR, 100000, "测试部", ["功能测试", "接口测试"])
    
    # 人力资源团队
    hr_specialist = Employee("褚专员", EmployeeLevel.JUNIOR, 80000, "人力资源", ["招聘", "培训"])
    
    # 创建部门结构
    print("\n🏗️  构建组织架构:")
    
    # 公司
    company = Department("科技有限公司", ceo)
    
    # 技术部
    tech_dept = Department("技术部", cto)
    dev_dept = Department("开发部", dev_manager)
    qa_dept = Department("测试部", qa_manager)
    
    # 人力资源部
    hr_dept = Department("人力资源部", hr_director)
    
    # 构建层次结构
    company.add_member(tech_dept)
    company.add_member(hr_dept)
    
    tech_dept.add_member(dev_dept)
    tech_dept.add_member(qa_dept)
    
    # 添加开发团队成员
    dev_dept.add_member(senior_dev1)
    dev_dept.add_member(senior_dev2)
    dev_dept.add_member(junior_dev1)
    dev_dept.add_member(junior_dev2)
    
    # 添加测试团队成员
    qa_dept.add_member(senior_qa)
    qa_dept.add_member(junior_qa)
    
    # 添加HR团队成员
    hr_dept.add_member(hr_specialist)
    
    # 设置绩效评分
    senior_dev1.set_performance_rating(4.5)
    senior_dev2.set_performance_rating(4.2)
    junior_dev1.set_performance_rating(3.8)
    
    # 显示组织架构
    print(f"\n🏢 组织架构:")
    print(company.display_structure())
    
    # 显示统计信息
    print(f"\n📊 公司统计:")
    stats = company.get_department_statistics()
    print(f"  • 总员工数: {stats['total_employees']} 人")
    print(f"  • 总薪资支出: ¥{stats['total_salary']:,.0f}")
    print(f"  • 平均薪资: ¥{stats['average_salary']:,.0f}")
    print(f"  • 平均绩效: {stats['average_performance']:.2f}")
    
    print(f"\n👥 级别分布:")
    for level, count in stats['level_distribution'].items():
        print(f"  • {level}: {count} 人")


if __name__ == "__main__":
    demo_organization()
