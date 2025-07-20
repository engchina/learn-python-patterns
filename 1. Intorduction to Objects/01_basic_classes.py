"""
01_basic_classes.py - 面向对象编程基础概念

这个示例通过学生管理系统展示面向对象编程的基本概念：
- 类的定义和实例化
- 属性和方法的使用
- 对象状态的管理
- 基本的数据操作
"""

from datetime import datetime
from typing import List, Optional


# ==================== 基础类定义 ====================
class Student:
    """学生类 - 展示基本的类定义和使用"""
    
    # 类属性 - 所有实例共享
    school_name = "Python编程学院"
    total_students = 0
    
    def __init__(self, name: str, age: int, student_id: str):
        """
        构造方法 - 创建学生对象时调用
        
        参数:
            name: 学生姓名
            age: 学生年龄  
            student_id: 学号
        """
        # 实例属性 - 每个对象独有
        self.name = name
        self.age = age
        self.student_id = student_id
        self.grades = []  # 存储成绩的列表
        self.enrollment_date = datetime.now()
        
        # 更新类属性
        Student.total_students += 1
        
        print(f"✅ 学生 {name} 已注册，学号: {student_id}")
    
    def add_grade(self, subject: str, score: float):
        """
        添加成绩
        
        参数:
            subject: 科目名称
            score: 分数
        """
        if 0 <= score <= 100:
            grade_record = {
                "subject": subject,
                "score": score,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.grades.append(grade_record)
            print(f"📝 {self.name} 的 {subject} 成绩已录入: {score}分")
        else:
            print(f"❌ 分数必须在0-100之间，当前输入: {score}")
    
    def get_average_grade(self) -> float:
        """
        计算平均成绩
        
        返回:
            平均分，如果没有成绩则返回0
        """
        if not self.grades:
            return 0.0
        
        total_score = sum(grade["score"] for grade in self.grades)
        average = total_score / len(self.grades)
        return round(average, 2)
    
    def get_grade_summary(self) -> str:
        """
        获取成绩摘要
        
        返回:
            成绩摘要字符串
        """
        if not self.grades:
            return "暂无成绩记录"
        
        summary = [f"📊 {self.name} 的成绩摘要:"]
        summary.append(f"   总科目数: {len(self.grades)}")
        summary.append(f"   平均分: {self.get_average_grade()}")
        summary.append("   各科成绩:")
        
        for grade in self.grades:
            summary.append(f"     - {grade['subject']}: {grade['score']}分 ({grade['date']})")
        
        return "\n".join(summary)
    
    def is_excellent_student(self) -> bool:
        """
        判断是否为优秀学生（平均分>=90）
        
        返回:
            True表示优秀学生，False表示普通学生
        """
        return self.get_average_grade() >= 90
    
    def get_info(self) -> str:
        """
        获取学生基本信息
        
        返回:
            学生信息字符串
        """
        enrollment_days = (datetime.now() - self.enrollment_date).days
        status = "优秀学生" if self.is_excellent_student() else "普通学生"
        
        info = [
            f"👤 学生信息:",
            f"   姓名: {self.name}",
            f"   年龄: {self.age}岁",
            f"   学号: {self.student_id}",
            f"   学校: {self.school_name}",
            f"   入学时间: {self.enrollment_date.strftime('%Y-%m-%d %H:%M:%S')}",
            f"   入学天数: {enrollment_days}天",
            f"   平均成绩: {self.get_average_grade()}分",
            f"   学生状态: {status}"
        ]
        
        return "\n".join(info)
    
    def __str__(self) -> str:
        """
        字符串表示方法 - 当使用print()时调用
        
        返回:
            对象的字符串表示
        """
        return f"Student(姓名={self.name}, 学号={self.student_id}, 平均分={self.get_average_grade()})"
    
    def __repr__(self) -> str:
        """
        官方字符串表示方法 - 用于调试
        
        返回:
            对象的官方字符串表示
        """
        return f"Student(name='{self.name}', age={self.age}, student_id='{self.student_id}')"
    
    @classmethod
    def get_school_info(cls) -> str:
        """
        类方法 - 获取学校信息
        
        返回:
            学校信息字符串
        """
        return f"🏫 {cls.school_name} - 当前在校学生: {cls.total_students}人"
    
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """
        静态方法 - 验证学号格式
        
        参数:
            student_id: 学号
            
        返回:
            True表示格式正确，False表示格式错误
        """
        # 简单验证：学号应该是8位数字
        return student_id.isdigit() and len(student_id) == 8


# ==================== 学生管理类 ====================
class StudentManager:
    """学生管理类 - 展示类之间的协作"""
    
    def __init__(self):
        """初始化学生管理器"""
        self.students: List[Student] = []
        print("🏫 学生管理系统已启动")
    
    def add_student(self, name: str, age: int, student_id: str) -> Optional[Student]:
        """
        添加学生
        
        参数:
            name: 学生姓名
            age: 学生年龄
            student_id: 学号
            
        返回:
            成功返回Student对象，失败返回None
        """
        # 验证学号格式
        if not Student.validate_student_id(student_id):
            print(f"❌ 学号格式错误: {student_id}（应为8位数字）")
            return None
        
        # 检查学号是否已存在
        if self.find_student_by_id(student_id):
            print(f"❌ 学号 {student_id} 已存在")
            return None
        
        # 创建学生对象
        student = Student(name, age, student_id)
        self.students.append(student)
        return student
    
    def find_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        根据学号查找学生
        
        参数:
            student_id: 学号
            
        返回:
            找到返回Student对象，未找到返回None
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def find_students_by_name(self, name: str) -> List[Student]:
        """
        根据姓名查找学生（支持模糊查找）
        
        参数:
            name: 学生姓名
            
        返回:
            匹配的学生列表
        """
        return [student for student in self.students if name.lower() in student.name.lower()]
    
    def get_excellent_students(self) -> List[Student]:
        """
        获取优秀学生列表
        
        返回:
            优秀学生列表
        """
        return [student for student in self.students if student.is_excellent_student()]
    
    def get_statistics(self) -> str:
        """
        获取统计信息
        
        返回:
            统计信息字符串
        """
        if not self.students:
            return "📊 暂无学生数据"
        
        total_students = len(self.students)
        excellent_students = len(self.get_excellent_students())
        
        # 计算整体平均分
        all_grades = []
        for student in self.students:
            all_grades.extend([grade["score"] for grade in student.grades])
        
        overall_average = sum(all_grades) / len(all_grades) if all_grades else 0
        
        stats = [
            "📊 学生管理系统统计:",
            f"   总学生数: {total_students}人",
            f"   优秀学生: {excellent_students}人 ({excellent_students/total_students*100:.1f}%)",
            f"   整体平均分: {overall_average:.2f}分",
            f"   总成绩记录: {len(all_grades)}条"
        ]
        
        return "\n".join(stats)
    
    def list_all_students(self):
        """列出所有学生信息"""
        if not self.students:
            print("📝 暂无学生记录")
            return
        
        print(f"\n📋 学生名单 (共{len(self.students)}人):")
        print("-" * 60)
        
        for i, student in enumerate(self.students, 1):
            print(f"{i:2d}. {student}")
        
        print("-" * 60)


# ==================== 演示函数 ====================
def demo_basic_classes():
    """基础类概念演示"""
    print("=" * 70)
    print("🎓 面向对象编程基础概念演示")
    print("=" * 70)
    
    # 显示学校信息（类方法调用）
    print(f"\n{Student.get_school_info()}")
    
    # 创建学生管理器
    manager = StudentManager()
    
    print(f"\n{'='*20} 添加学生 {'='*20}")
    
    # 添加学生
    students_data = [
        ("张三", 20, "20240001"),
        ("李四", 19, "20240002"),
        ("王五", 21, "20240003"),
        ("赵六", 20, "20240004")
    ]
    
    students = []
    for name, age, student_id in students_data:
        student = manager.add_student(name, age, student_id)
        if student:
            students.append(student)
    
    # 测试无效学号
    print(f"\n🧪 测试无效学号:")
    manager.add_student("测试学生", 20, "123")  # 无效学号
    manager.add_student("重复学号", 20, "20240001")  # 重复学号
    
    print(f"\n{'='*20} 录入成绩 {'='*20}")
    
    # 为学生添加成绩
    if len(students) >= 4:
        students[0].add_grade("数学", 95)
        students[0].add_grade("英语", 88)
        students[0].add_grade("物理", 92)
        
        students[1].add_grade("数学", 78)
        students[1].add_grade("英语", 85)
        students[1].add_grade("化学", 80)
        
        students[2].add_grade("数学", 96)
        students[2].add_grade("英语", 94)
        students[2].add_grade("物理", 98)
        students[2].add_grade("化学", 91)
        
        students[3].add_grade("数学", 82)
        students[3].add_grade("英语", 79)
    
    # 测试无效成绩
    print(f"\n🧪 测试无效成绩:")
    if students:
        students[0].add_grade("测试科目", 150)  # 无效分数
    
    print(f"\n{'='*20} 学生信息展示 {'='*20}")
    
    # 显示学生详细信息
    for student in students[:2]:  # 只显示前两个学生的详细信息
        print(f"\n{student.get_info()}")
        print(f"\n{student.get_grade_summary()}")
    
    print(f"\n{'='*20} 学生列表 {'='*20}")
    
    # 列出所有学生
    manager.list_all_students()
    
    print(f"\n{'='*20} 查找功能 {'='*20}")
    
    # 查找功能演示
    print(f"\n🔍 按学号查找:")
    found_student = manager.find_student_by_id("20240001")
    if found_student:
        print(f"   找到学生: {found_student}")
    
    print(f"\n🔍 按姓名查找:")
    found_students = manager.find_students_by_name("张")
    for student in found_students:
        print(f"   找到学生: {student}")
    
    print(f"\n🔍 优秀学生:")
    excellent_students = manager.get_excellent_students()
    if excellent_students:
        for student in excellent_students:
            print(f"   🌟 {student}")
    else:
        print("   暂无优秀学生")
    
    print(f"\n{'='*20} 统计信息 {'='*20}")
    
    # 显示统计信息
    print(f"\n{manager.get_statistics()}")
    print(f"\n{Student.get_school_info()}")
    
    print(f"\n{'='*20} 对象表示 {'='*20}")
    
    # 演示对象的字符串表示
    if students:
        student = students[0]
        print(f"\nstr()表示: {str(student)}")
        print(f"repr()表示: {repr(student)}")
    
    print("\n" + "=" * 70)
    print("🎉 基础类概念演示完成!")
    print("💡 关键点:")
    print("   - 类是对象的模板，对象是类的实例")
    print("   - 实例属性属于每个对象，类属性被所有对象共享")
    print("   - 方法是对象能执行的操作")
    print("   - 封装将数据和操作数据的方法组织在一起")
    print("=" * 70)


if __name__ == "__main__":
    demo_basic_classes()
