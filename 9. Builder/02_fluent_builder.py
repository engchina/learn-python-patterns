"""
02_fluent_builder.py - 流式建造者模式

SQL查询构建器示例
这个示例展示了如何使用流式建造者模式来构建复杂的SQL查询。
流式建造者模式通过方法链的方式，让代码更加简洁和易读，
特别适合构建具有多个可选参数的复杂对象。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from enum import Enum


# ==================== 枚举类型 ====================
class JoinType(Enum):
    """连接类型"""
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"


class OrderDirection(Enum):
    """排序方向"""
    ASC = "ASC"
    DESC = "DESC"


# ==================== SQL查询产品类 ====================
class SQLQuery:
    """SQL查询产品类"""
    
    def __init__(self):
        self.select_fields = []
        self.from_table = ""
        self.joins = []
        self.where_conditions = []
        self.group_by_fields = []
        self.having_conditions = []
        self.order_by_fields = []
        self.limit_count = None
        self.offset_count = None
        self.parameters = {}
    
    def to_sql(self) -> str:
        """生成SQL语句"""
        sql_parts = []
        
        # SELECT 子句
        if self.select_fields:
            sql_parts.append(f"SELECT {', '.join(self.select_fields)}")
        else:
            sql_parts.append("SELECT *")
        
        # FROM 子句
        if self.from_table:
            sql_parts.append(f"FROM {self.from_table}")
        
        # JOIN 子句
        for join in self.joins:
            sql_parts.append(f"{join['type']} {join['table']} ON {join['condition']}")
        
        # WHERE 子句
        if self.where_conditions:
            sql_parts.append(f"WHERE {' AND '.join(self.where_conditions)}")
        
        # GROUP BY 子句
        if self.group_by_fields:
            sql_parts.append(f"GROUP BY {', '.join(self.group_by_fields)}")
        
        # HAVING 子句
        if self.having_conditions:
            sql_parts.append(f"HAVING {' AND '.join(self.having_conditions)}")
        
        # ORDER BY 子句
        if self.order_by_fields:
            order_clauses = []
            for field_info in self.order_by_fields:
                if isinstance(field_info, dict):
                    field = field_info['field']
                    direction = field_info['direction']
                    order_clauses.append(f"{field} {direction}")
                else:
                    order_clauses.append(str(field_info))
            sql_parts.append(f"ORDER BY {', '.join(order_clauses)}")
        
        # LIMIT 子句
        if self.limit_count is not None:
            if self.offset_count is not None:
                sql_parts.append(f"LIMIT {self.offset_count}, {self.limit_count}")
            else:
                sql_parts.append(f"LIMIT {self.limit_count}")
        
        return "\n".join(sql_parts)
    
    def get_parameters(self) -> Dict[str, Any]:
        """获取查询参数"""
        return self.parameters.copy()
    
    def __str__(self):
        return self.to_sql()


# ==================== 流式SQL建造者 ====================
class SQLQueryBuilder:
    """流式SQL查询建造者"""
    
    def __init__(self):
        self.query = SQLQuery()
    
    def select(self, *fields: str) -> 'SQLQueryBuilder':
        """选择字段"""
        if fields:
            self.query.select_fields.extend(fields)
        return self
    
    def select_distinct(self, *fields: str) -> 'SQLQueryBuilder':
        """选择不重复字段"""
        if fields:
            distinct_fields = [f"DISTINCT {field}" if i == 0 else field 
                             for i, field in enumerate(fields)]
            self.query.select_fields.extend(distinct_fields)
        return self
    
    def select_count(self, field: str = "*", alias: str = None) -> 'SQLQueryBuilder':
        """选择计数"""
        count_expr = f"COUNT({field})"
        if alias:
            count_expr += f" AS {alias}"
        self.query.select_fields.append(count_expr)
        return self
    
    def select_sum(self, field: str, alias: str = None) -> 'SQLQueryBuilder':
        """选择求和"""
        sum_expr = f"SUM({field})"
        if alias:
            sum_expr += f" AS {alias}"
        self.query.select_fields.append(sum_expr)
        return self
    
    def select_avg(self, field: str, alias: str = None) -> 'SQLQueryBuilder':
        """选择平均值"""
        avg_expr = f"AVG({field})"
        if alias:
            avg_expr += f" AS {alias}"
        self.query.select_fields.append(avg_expr)
        return self
    
    def from_table(self, table: str, alias: str = None) -> 'SQLQueryBuilder':
        """指定表名"""
        if alias:
            self.query.from_table = f"{table} AS {alias}"
        else:
            self.query.from_table = table
        return self
    
    def join(self, table: str, condition: str, join_type: JoinType = JoinType.INNER) -> 'SQLQueryBuilder':
        """添加连接"""
        self.query.joins.append({
            'type': join_type.value,
            'table': table,
            'condition': condition
        })
        return self
    
    def inner_join(self, table: str, condition: str) -> 'SQLQueryBuilder':
        """内连接"""
        return self.join(table, condition, JoinType.INNER)
    
    def left_join(self, table: str, condition: str) -> 'SQLQueryBuilder':
        """左连接"""
        return self.join(table, condition, JoinType.LEFT)
    
    def right_join(self, table: str, condition: str) -> 'SQLQueryBuilder':
        """右连接"""
        return self.join(table, condition, JoinType.RIGHT)
    
    def where(self, condition: str) -> 'SQLQueryBuilder':
        """添加WHERE条件"""
        self.query.where_conditions.append(condition)
        return self
    
    def where_equals(self, field: str, value: Any, param_name: str = None) -> 'SQLQueryBuilder':
        """添加等于条件"""
        if param_name is None:
            param_name = f"param_{len(self.query.parameters)}"
        
        self.query.where_conditions.append(f"{field} = :{param_name}")
        self.query.parameters[param_name] = value
        return self
    
    def where_in(self, field: str, values: List[Any], param_name: str = None) -> 'SQLQueryBuilder':
        """添加IN条件"""
        if param_name is None:
            param_name = f"param_{len(self.query.parameters)}"
        
        placeholders = [f":{param_name}_{i}" for i in range(len(values))]
        self.query.where_conditions.append(f"{field} IN ({', '.join(placeholders)})")
        
        for i, value in enumerate(values):
            self.query.parameters[f"{param_name}_{i}"] = value
        return self
    
    def where_between(self, field: str, start_value: Any, end_value: Any) -> 'SQLQueryBuilder':
        """添加BETWEEN条件"""
        start_param = f"start_{len(self.query.parameters)}"
        end_param = f"end_{len(self.query.parameters) + 1}"
        
        self.query.where_conditions.append(f"{field} BETWEEN :{start_param} AND :{end_param}")
        self.query.parameters[start_param] = start_value
        self.query.parameters[end_param] = end_value
        return self
    
    def where_like(self, field: str, pattern: str, param_name: str = None) -> 'SQLQueryBuilder':
        """添加LIKE条件"""
        if param_name is None:
            param_name = f"param_{len(self.query.parameters)}"
        
        self.query.where_conditions.append(f"{field} LIKE :{param_name}")
        self.query.parameters[param_name] = pattern
        return self
    
    def group_by(self, *fields: str) -> 'SQLQueryBuilder':
        """添加GROUP BY字段"""
        self.query.group_by_fields.extend(fields)
        return self
    
    def having(self, condition: str) -> 'SQLQueryBuilder':
        """添加HAVING条件"""
        self.query.having_conditions.append(condition)
        return self
    
    def order_by(self, field: str, direction: OrderDirection = OrderDirection.ASC) -> 'SQLQueryBuilder':
        """添加ORDER BY字段"""
        self.query.order_by_fields.append({
            'field': field,
            'direction': direction.value
        })
        return self
    
    def order_by_asc(self, field: str) -> 'SQLQueryBuilder':
        """按升序排序"""
        return self.order_by(field, OrderDirection.ASC)
    
    def order_by_desc(self, field: str) -> 'SQLQueryBuilder':
        """按降序排序"""
        return self.order_by(field, OrderDirection.DESC)
    
    def limit(self, count: int) -> 'SQLQueryBuilder':
        """限制结果数量"""
        self.query.limit_count = count
        return self
    
    def offset(self, count: int) -> 'SQLQueryBuilder':
        """设置偏移量"""
        self.query.offset_count = count
        return self
    
    def paginate(self, page: int, page_size: int) -> 'SQLQueryBuilder':
        """分页"""
        offset = (page - 1) * page_size
        return self.offset(offset).limit(page_size)
    
    def build(self) -> SQLQuery:
        """构建SQL查询对象"""
        return self.query
    
    def to_sql(self) -> str:
        """直接生成SQL语句"""
        return self.query.to_sql()


# ==================== HTTP请求建造者 ====================
class HTTPRequest:
    """HTTP请求产品类"""
    
    def __init__(self):
        self.method = "GET"
        self.url = ""
        self.headers = {}
        self.query_params = {}
        self.body = None
        self.timeout = 30
        self.auth = None
        self.cookies = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "params": self.query_params,
            "data": self.body,
            "timeout": self.timeout,
            "auth": self.auth,
            "cookies": self.cookies
        }
    
    def __str__(self):
        return f"{self.method} {self.url}"


class HTTPRequestBuilder:
    """流式HTTP请求建造者"""
    
    def __init__(self):
        self.request = HTTPRequest()
    
    def get(self, url: str) -> 'HTTPRequestBuilder':
        """GET请求"""
        self.request.method = "GET"
        self.request.url = url
        return self
    
    def post(self, url: str) -> 'HTTPRequestBuilder':
        """POST请求"""
        self.request.method = "POST"
        self.request.url = url
        return self
    
    def put(self, url: str) -> 'HTTPRequestBuilder':
        """PUT请求"""
        self.request.method = "PUT"
        self.request.url = url
        return self
    
    def delete(self, url: str) -> 'HTTPRequestBuilder':
        """DELETE请求"""
        self.request.method = "DELETE"
        self.request.url = url
        return self
    
    def header(self, key: str, value: str) -> 'HTTPRequestBuilder':
        """添加请求头"""
        self.request.headers[key] = value
        return self
    
    def headers(self, headers: Dict[str, str]) -> 'HTTPRequestBuilder':
        """批量添加请求头"""
        self.request.headers.update(headers)
        return self
    
    def content_type(self, content_type: str) -> 'HTTPRequestBuilder':
        """设置Content-Type"""
        return self.header("Content-Type", content_type)
    
    def json_content(self) -> 'HTTPRequestBuilder':
        """设置JSON内容类型"""
        return self.content_type("application/json")
    
    def form_content(self) -> 'HTTPRequestBuilder':
        """设置表单内容类型"""
        return self.content_type("application/x-www-form-urlencoded")
    
    def param(self, key: str, value: Any) -> 'HTTPRequestBuilder':
        """添加查询参数"""
        self.request.query_params[key] = value
        return self
    
    def params(self, params: Dict[str, Any]) -> 'HTTPRequestBuilder':
        """批量添加查询参数"""
        self.request.query_params.update(params)
        return self
    
    def body(self, data: Any) -> 'HTTPRequestBuilder':
        """设置请求体"""
        self.request.body = data
        return self
    
    def json_body(self, data: Dict[str, Any]) -> 'HTTPRequestBuilder':
        """设置JSON请求体"""
        import json
        self.request.body = json.dumps(data)
        return self.json_content()
    
    def timeout(self, seconds: int) -> 'HTTPRequestBuilder':
        """设置超时时间"""
        self.request.timeout = seconds
        return self
    
    def auth(self, username: str, password: str) -> 'HTTPRequestBuilder':
        """设置基本认证"""
        self.request.auth = (username, password)
        return self
    
    def bearer_token(self, token: str) -> 'HTTPRequestBuilder':
        """设置Bearer Token"""
        return self.header("Authorization", f"Bearer {token}")
    
    def cookie(self, key: str, value: str) -> 'HTTPRequestBuilder':
        """添加Cookie"""
        self.request.cookies[key] = value
        return self
    
    def cookies(self, cookies: Dict[str, str]) -> 'HTTPRequestBuilder':
        """批量添加Cookie"""
        self.request.cookies.update(cookies)
        return self
    
    def build(self) -> HTTPRequest:
        """构建HTTP请求对象"""
        return self.request


# ==================== 演示函数 ====================
def demonstrate_sql_builder():
    """演示SQL查询建造者"""
    print("=" * 60)
    print("SQL查询建造者演示")
    print("=" * 60)
    
    # 简单查询
    print("\n1. 简单查询:")
    simple_query = (SQLQueryBuilder()
                   .select("id", "name", "email")
                   .from_table("users")
                   .where_equals("status", "active")
                   .order_by_asc("name")
                   .limit(10)
                   .build())
    
    print(simple_query.to_sql())
    print(f"参数: {simple_query.get_parameters()}")
    
    # 复杂查询
    print("\n2. 复杂查询:")
    complex_query = (SQLQueryBuilder()
                    .select("u.name", "u.email", "p.title")
                    .select_count("p.id", "post_count")
                    .from_table("users", "u")
                    .left_join("posts p", "u.id = p.user_id")
                    .where_in("u.department", ["IT", "HR", "Finance"])
                    .where_between("u.created_at", "2023-01-01", "2023-12-31")
                    .group_by("u.id", "u.name", "u.email")
                    .having("COUNT(p.id) > 5")
                    .order_by_desc("post_count")
                    .paginate(2, 20)
                    .build())
    
    print(complex_query.to_sql())
    print(f"参数: {complex_query.get_parameters()}")


def demonstrate_http_builder():
    """演示HTTP请求建造者"""
    print("\n" + "=" * 60)
    print("HTTP请求建造者演示")
    print("=" * 60)
    
    # GET请求
    print("\n1. GET请求:")
    get_request = (HTTPRequestBuilder()
                  .get("https://api.example.com/users")
                  .param("page", 1)
                  .param("limit", 20)
                  .header("Accept", "application/json")
                  .bearer_token("abc123")
                  .timeout(30)
                  .build())
    
    print(f"请求: {get_request}")
    print(f"详情: {get_request.to_dict()}")
    
    # POST请求
    print("\n2. POST请求:")
    post_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "department": "IT"
    }
    
    post_request = (HTTPRequestBuilder()
                   .post("https://api.example.com/users")
                   .json_body(post_data)
                   .header("Accept", "application/json")
                   .bearer_token("abc123")
                   .timeout(60)
                   .build())
    
    print(f"请求: {post_request}")
    print(f"详情: {post_request.to_dict()}")


def main():
    """主函数"""
    print("流式建造者模式演示")
    
    demonstrate_sql_builder()
    demonstrate_http_builder()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
