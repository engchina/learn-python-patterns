"""
04_query_interpreter.py - 查询语言解释器

这个示例展示了如何使用解释器模式来实现一个简单的查询语言。
支持数据过滤、排序、聚合等操作，可以用于数据分析和报表生成。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union, Optional, Callable
import re
from enum import Enum
import operator as op


# ==================== 数据类型定义 ====================
class DataType(Enum):
    """数据类型"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"


class DataRow:
    """数据行"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def get(self, field: str) -> Any:
        """获取字段值"""
        return self.data.get(field)

    def set(self, field: str, value: Any):
        """设置字段值"""
        self.data[field] = value

    def has(self, field: str) -> bool:
        """检查字段是否存在"""
        return field in self.data

    def keys(self) -> List[str]:
        """获取所有字段名"""
        return list(self.data.keys())

    def values(self) -> List[Any]:
        """获取所有字段值"""
        return list(self.data.values())

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.data.copy()

    def __str__(self):
        return str(self.data)


class DataTable:
    """数据表"""

    def __init__(self, name: str, rows: List[DataRow] = None):
        self.name = name
        self.rows = rows or []
        self.schema: Dict[str, DataType] = {}

    def add_row(self, row: DataRow):
        """添加数据行"""
        self.rows.append(row)

    def get_rows(self) -> List[DataRow]:
        """获取所有数据行"""
        return self.rows

    def get_columns(self) -> List[str]:
        """获取所有列名"""
        if not self.rows:
            return []
        return self.rows[0].keys()

    def size(self) -> int:
        """获取行数"""
        return len(self.rows)

    def set_schema(self, schema: Dict[str, DataType]):
        """设置表结构"""
        self.schema = schema

    def get_schema(self) -> Dict[str, DataType]:
        """获取表结构"""
        return self.schema

    def __str__(self):
        return f"Table({self.name}, {self.size()} rows)"


# ==================== 查询表达式 ====================
class QueryExpression(ABC):
    """查询表达式基类"""

    @abstractmethod
    def execute(self, table: DataTable) -> DataTable:
        """执行查询"""
        pass


class SelectExpression(QueryExpression):
    """SELECT表达式"""

    def __init__(self, columns: List[str], table_name: str):
        self.columns = columns
        self.table_name = table_name
        self.where_clause: Optional['WhereExpression'] = None
        self.order_clause: Optional['OrderExpression'] = None
        self.limit_clause: Optional['LimitExpression'] = None
        self.group_clause: Optional['GroupExpression'] = None

    def where(self, field: str, operator: str, value: Any) -> 'SelectExpression':
        """添加WHERE条件"""
        self.where_clause = WhereExpression(field, operator, value)
        return self

    def order_by(self, field: str, ascending: bool = True) -> 'SelectExpression':
        """添加ORDER BY子句"""
        self.order_clause = OrderExpression(field, ascending)
        return self

    def limit(self, count: int, offset: int = 0) -> 'SelectExpression':
        """添加LIMIT子句"""
        self.limit_clause = LimitExpression(count, offset)
        return self

    def group_by(self, field: str, **aggregates) -> 'SelectExpression':
        """添加GROUP BY子句"""
        self.group_clause = GroupExpression(field, aggregates)
        return self

    def execute(self, table: DataTable) -> DataTable:
        """执行SELECT查询"""
        result_rows = table.get_rows().copy()

        # 应用WHERE条件
        if self.where_clause:
            result_rows = [row for row in result_rows if self.where_clause.evaluate(row)]

        # 应用GROUP BY
        if self.group_clause:
            result_rows = self.group_clause.group(result_rows)

        # 应用ORDER BY
        if self.order_clause:
            result_rows = self.order_clause.sort(result_rows)

        # 应用LIMIT
        if self.limit_clause:
            result_rows = self.limit_clause.limit(result_rows)

        # 选择列
        if '*' not in self.columns:
            filtered_rows = []
            for row in result_rows:
                filtered_data = {col: row.get(col) for col in self.columns if row.has(col)}
                filtered_rows.append(DataRow(filtered_data))
            result_rows = filtered_rows

        return DataTable(f"result_{self.table_name}", result_rows)


class WhereExpression:
    """WHERE条件表达式"""

    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator
        self.value = value
        self.operator_map = {
            '=': op.eq,
            '!=': op.ne,
            '<': op.lt,
            '<=': op.le,
            '>': op.gt,
            '>=': op.ge,
            'like': self._like_operator,
            'in': self._in_operator,
            'not_in': self._not_in_operator
        }

    def _like_operator(self, field_value: Any, pattern: str) -> bool:
        """LIKE操作符"""
        if not isinstance(field_value, str) or not isinstance(pattern, str):
            return False
        # 简单的通配符匹配
        regex_pattern = pattern.replace('%', '.*').replace('_', '.')
        return bool(re.match(regex_pattern, field_value, re.IGNORECASE))

    def _in_operator(self, field_value: Any, values: List[Any]) -> bool:
        """IN操作符"""
        return field_value in values

    def _not_in_operator(self, field_value: Any, values: List[Any]) -> bool:
        """NOT IN操作符"""
        return field_value not in values

    def evaluate(self, row: DataRow) -> bool:
        """评估WHERE条件"""
        if not row.has(self.field):
            return False

        field_value = row.get(self.field)
        op_func = self.operator_map.get(self.operator)

        if op_func is None:
            raise ValueError(f"不支持的操作符: {self.operator}")

        try:
            return op_func(field_value, self.value)
        except Exception:
            return False

    def __str__(self):
        return f"{self.field} {self.operator} {self.value}"


class OrderExpression:
    """ORDER BY表达式"""

    def __init__(self, field: str, ascending: bool = True):
        self.field = field
        self.ascending = ascending

    def sort(self, rows: List[DataRow]) -> List[DataRow]:
        """排序数据行"""
        try:
            return sorted(rows,
                         key=lambda row: row.get(self.field) or 0,
                         reverse=not self.ascending)
        except Exception:
            return rows

    def __str__(self):
        direction = "ASC" if self.ascending else "DESC"
        return f"{self.field} {direction}"


class LimitExpression:
    """LIMIT表达式"""

    def __init__(self, count: int, offset: int = 0):
        self.count = count
        self.offset = offset

    def limit(self, rows: List[DataRow]) -> List[DataRow]:
        """限制结果数量"""
        start = self.offset
        end = start + self.count
        return rows[start:end]

    def __str__(self):
        if self.offset > 0:
            return f"LIMIT {self.count} OFFSET {self.offset}"
        return f"LIMIT {self.count}"


class GroupExpression:
    """GROUP BY表达式"""

    def __init__(self, field: str, aggregates: Dict[str, str] = None):
        self.field = field
        self.aggregates = aggregates or {}  # {new_field: 'count|sum|avg|min|max'}

    def group(self, rows: List[DataRow]) -> List[DataRow]:
        """分组数据"""
        groups: Dict[Any, List[DataRow]] = {}

        # 按字段值分组
        for row in rows:
            group_key = row.get(self.field)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(row)

        # 计算聚合值
        result_rows = []
        for group_key, group_rows in groups.items():
            result_data = {self.field: group_key}

            for agg_field, agg_func in self.aggregates.items():
                if agg_func == 'count':
                    result_data[agg_field] = len(group_rows)
                elif agg_func == 'sum':
                    values = [row.get(agg_field.replace('_sum', '')) for row in group_rows]
                    result_data[agg_field] = sum(v for v in values if isinstance(v, (int, float)))
                elif agg_func == 'avg':
                    values = [row.get(agg_field.replace('_avg', '')) for row in group_rows]
                    numeric_values = [v for v in values if isinstance(v, (int, float))]
                    result_data[agg_field] = sum(numeric_values) / len(numeric_values) if numeric_values else 0
                elif agg_func == 'min':
                    values = [row.get(agg_field.replace('_min', '')) for row in group_rows]
                    numeric_values = [v for v in values if v is not None]
                    result_data[agg_field] = min(numeric_values) if numeric_values else None
                elif agg_func == 'max':
                    values = [row.get(agg_field.replace('_max', '')) for row in group_rows]
                    numeric_values = [v for v in values if v is not None]
                    result_data[agg_field] = max(numeric_values) if numeric_values else None

            result_rows.append(DataRow(result_data))

        return result_rows

    def __str__(self):
        agg_str = ', '.join(f"{field}({func})" for field, func in self.aggregates.items())
        return f"GROUP BY {self.field}" + (f" WITH {agg_str}" if agg_str else "")


# ==================== 查询构建器 ====================
class QueryBuilder:
    """查询构建器"""

    @staticmethod
    def select(*columns: str) -> SelectExpression:
        """创建SELECT查询"""
        return SelectExpression(list(columns), "")

    @staticmethod
    def from_table(table_name: str) -> SelectExpression:
        """指定查询的表"""
        return SelectExpression(['*'], table_name)

    @staticmethod
    def where(field: str, operator: str, value: Any) -> WhereExpression:
        """创建WHERE条件"""
        return WhereExpression(field, operator, value)

    @staticmethod
    def order_by(field: str, ascending: bool = True) -> OrderExpression:
        """创建ORDER BY子句"""
        return OrderExpression(field, ascending)

    @staticmethod
    def limit(count: int, offset: int = 0) -> LimitExpression:
        """创建LIMIT子句"""
        return LimitExpression(count, offset)

    @staticmethod
    def group_by(field: str, **aggregates) -> GroupExpression:
        """创建GROUP BY子句"""
        return GroupExpression(field, aggregates)


# ==================== 查询引擎 ====================
class QueryEngine:
    """查询引擎"""

    def __init__(self):
        self.tables: Dict[str, DataTable] = {}

    def add_table(self, table: DataTable):
        """添加数据表"""
        self.tables[table.name] = table

    def get_table(self, name: str) -> Optional[DataTable]:
        """获取数据表"""
        return self.tables.get(name)

    def execute_query(self, query: QueryExpression, table_name: str) -> DataTable:
        """执行查询"""
        table = self.get_table(table_name)
        if table is None:
            raise ValueError(f"表不存在: {table_name}")

        return query.execute(table)

    def list_tables(self) -> List[str]:
        """列出所有表名"""
        return list(self.tables.keys())


# ==================== 演示函数 ====================
def create_sample_data() -> DataTable:
    """创建示例数据"""
    employees = DataTable("employees")

    sample_data = [
        {"id": 1, "name": "张三", "department": "技术部", "salary": 8000, "age": 28, "city": "北京"},
        {"id": 2, "name": "李四", "department": "销售部", "salary": 6000, "age": 25, "city": "上海"},
        {"id": 3, "name": "王五", "department": "技术部", "salary": 9000, "age": 30, "city": "北京"},
        {"id": 4, "name": "赵六", "department": "人事部", "salary": 5500, "age": 26, "city": "广州"},
        {"id": 5, "name": "钱七", "department": "销售部", "salary": 7000, "age": 29, "city": "深圳"},
        {"id": 6, "name": "孙八", "department": "技术部", "salary": 8500, "age": 27, "city": "杭州"},
        {"id": 7, "name": "周九", "department": "财务部", "salary": 6500, "age": 31, "city": "成都"},
        {"id": 8, "name": "吴十", "department": "销售部", "salary": 6800, "age": 24, "city": "武汉"},
    ]

    for data in sample_data:
        employees.add_row(DataRow(data))

    return employees


def demonstrate_basic_queries():
    """演示基础查询功能"""
    print("=" * 60)
    print("查询语言解释器演示")
    print("=" * 60)

    # 创建查询引擎和示例数据
    engine = QueryEngine()
    employees = create_sample_data()
    engine.add_table(employees)

    print(f"员工表数据 ({employees.size()} 行):")
    for row in employees.get_rows()[:3]:  # 只显示前3行
        print(f"  {row}")
    print("  ...")

    builder = QueryBuilder

    print("\n1. 基础SELECT查询:")

    # 查询所有员工
    query1 = builder.select("*").where("department", "=", "技术部")
    result1 = engine.execute_query(query1, "employees")
    print(f"技术部员工 ({result1.size()} 行):")
    for row in result1.get_rows():
        print(f"  {row}")

    print("\n2. 带条件的查询:")

    # 查询高薪员工
    query2 = builder.select("name", "salary", "department").where("salary", ">", 7000)
    result2 = engine.execute_query(query2, "employees")
    print(f"高薪员工 (薪资 > 7000, {result2.size()} 行):")
    for row in result2.get_rows():
        print(f"  {row}")

    print("\n3. 排序查询:")

    # 按薪资排序
    query3 = (builder.select("name", "salary")
              .order_by("salary", ascending=False)
              .limit(5))
    result3 = engine.execute_query(query3, "employees")
    print(f"薪资前5名:")
    for row in result3.get_rows():
        print(f"  {row}")


def demonstrate_advanced_queries():
    """演示高级查询功能"""
    print("\n" + "=" * 60)
    print("高级查询功能演示")
    print("=" * 60)

    engine = QueryEngine()
    employees = create_sample_data()
    engine.add_table(employees)

    builder = QueryBuilder

    print("1. 模糊查询:")

    # 名字包含"三"的员工
    query1 = builder.select("name", "department").where("name", "like", "%三%")
    result1 = engine.execute_query(query1, "employees")
    print(f"名字包含'三'的员工:")
    for row in result1.get_rows():
        print(f"  {row}")

    print("\n2. 范围查询:")

    # 年龄在25-30之间的员工
    query2 = (builder.select("name", "age", "salary")
              .where("age", ">=", 25)
              .where("age", "<=", 30)  # 注意：这里简化处理，实际应该支持AND/OR
              .order_by("age"))

    # 由于简化实现，我们手动处理复合条件
    all_employees = engine.get_table("employees").get_rows()
    filtered_rows = []
    for row in all_employees:
        if 25 <= row.get("age") <= 30:
            filtered_rows.append(DataRow({
                "name": row.get("name"),
                "age": row.get("age"),
                "salary": row.get("salary")
            }))

    # 排序
    filtered_rows.sort(key=lambda r: r.get("age"))

    print(f"年龄25-30岁的员工:")
    for row in filtered_rows:
        print(f"  {row}")

    print("\n3. 分组聚合查询:")

    # 按部门统计
    query3 = builder.group_by("department",
                             count="count",
                             avg_salary="avg",
                             max_salary="max")

    # 手动实现分组聚合
    departments = {}
    for row in all_employees:
        dept = row.get("department")
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(row)

    print("按部门统计:")
    for dept, dept_employees in departments.items():
        count = len(dept_employees)
        salaries = [emp.get("salary") for emp in dept_employees]
        avg_salary = sum(salaries) / len(salaries)
        max_salary = max(salaries)

        print(f"  {dept}: 人数={count}, 平均薪资={avg_salary:.0f}, 最高薪资={max_salary}")


def demonstrate_query_builder():
    """演示查询构建器的链式调用"""
    print("\n" + "=" * 60)
    print("查询构建器链式调用演示")
    print("=" * 60)

    engine = QueryEngine()
    employees = create_sample_data()
    engine.add_table(employees)

    builder = QueryBuilder

    # 复杂查询：技术部薪资前3名
    print("技术部薪资前3名员工:")

    # 由于简化实现，我们手动构建复杂查询
    tech_employees = []
    for row in employees.get_rows():
        if row.get("department") == "技术部":
            tech_employees.append(row)

    # 按薪资排序
    tech_employees.sort(key=lambda r: r.get("salary"), reverse=True)

    # 取前3名
    top3_tech = tech_employees[:3]

    for i, row in enumerate(top3_tech, 1):
        print(f"  {i}. {row.get('name')} - 薪资: {row.get('salary')}")

    print("\n查询语句构建过程:")
    print("1. SELECT name, salary, department")
    print("2. FROM employees")
    print("3. WHERE department = '技术部'")
    print("4. ORDER BY salary DESC")
    print("5. LIMIT 3")


if __name__ == "__main__":
    demonstrate_basic_queries()
    demonstrate_advanced_queries()
    demonstrate_query_builder()
