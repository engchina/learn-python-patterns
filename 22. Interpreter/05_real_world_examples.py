"""
05_real_world_examples.py - 解释器模式实际应用场景

这个示例展示了解释器模式在实际项目中的应用，包括：
1. 模板引擎解释器
2. 业务规则引擎
3. 简单脚本语言解释器
"""

import re
from typing import Dict, List, Any, Union, Optional, Callable
from abc import ABC, abstractmethod
from datetime import datetime, date
import json


# ==================== 模板引擎解释器 ====================
class TemplateContext:
    """模板上下文"""

    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self._register_builtin_functions()

    def _register_builtin_functions(self):
        """注册内置函数"""
        self.functions.update({
            'upper': str.upper,
            'lower': str.lower,
            'title': str.title,
            'len': len,
            'format_date': self._format_date,
            'format_number': self._format_number,
            'default': self._default_value,
            'join': self._join_list,
        })

    def _format_date(self, date_obj: Any, format_str: str = "%Y-%m-%d") -> str:
        """格式化日期"""
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime(format_str)
        return str(date_obj)

    def _format_number(self, number: Union[int, float], decimals: int = 2) -> str:
        """格式化数字"""
        return f"{number:.{decimals}f}"

    def _default_value(self, value: Any, default: Any) -> Any:
        """默认值"""
        return default if value is None or value == "" else value

    def _join_list(self, items: List[Any], separator: str = ", ") -> str:
        """连接列表"""
        return separator.join(str(item) for item in items)

    def set_variable(self, name: str, value: Any):
        """设置变量"""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """获取变量"""
        return self.variables.get(name)

    def call_function(self, name: str, *args) -> Any:
        """调用函数"""
        if name not in self.functions:
            raise ValueError(f"未定义的函数: {name}")
        return self.functions[name](*args)


class TemplateExpression(ABC):
    """模板表达式基类"""

    @abstractmethod
    def render(self, context: TemplateContext) -> str:
        pass


class TextExpression(TemplateExpression):
    """文本表达式"""

    def __init__(self, text: str):
        self.text = text

    def render(self, context: TemplateContext) -> str:
        return self.text


class VariableExpression(TemplateExpression):
    """变量表达式"""

    def __init__(self, name: str):
        self.name = name

    def render(self, context: TemplateContext) -> str:
        value = context.get_variable(self.name)
        return str(value) if value is not None else ""


class FunctionExpression(TemplateExpression):
    """函数表达式"""

    def __init__(self, name: str, args: List[TemplateExpression]):
        self.name = name
        self.args = args

    def render(self, context: TemplateContext) -> str:
        # 渲染所有参数
        arg_values = []
        for arg in self.args:
            if isinstance(arg, VariableExpression):
                arg_values.append(context.get_variable(arg.name))
            else:
                arg_values.append(arg.render(context))

        # 调用函数
        result = context.call_function(self.name, *arg_values)
        return str(result)


class ConditionalExpression(TemplateExpression):
    """条件表达式"""

    def __init__(self, condition: str, true_expr: TemplateExpression, false_expr: TemplateExpression = None):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr or TextExpression("")

    def render(self, context: TemplateContext) -> str:
        # 简单的条件评估
        var_name = self.condition.strip()
        value = context.get_variable(var_name)

        # 判断真假
        is_true = bool(value) if value is not None else False

        if is_true:
            return self.true_expr.render(context)
        else:
            return self.false_expr.render(context)


class LoopExpression(TemplateExpression):
    """循环表达式"""

    def __init__(self, var_name: str, list_name: str, body: TemplateExpression):
        self.var_name = var_name
        self.list_name = list_name
        self.body = body

    def render(self, context: TemplateContext) -> str:
        items = context.get_variable(self.list_name)
        if not isinstance(items, list):
            return ""

        results = []
        for item in items:
            # 设置循环变量
            context.set_variable(self.var_name, item)
            results.append(self.body.render(context))

        return "".join(results)


class TemplateEngine:
    """模板引擎"""

    def __init__(self):
        self.context = TemplateContext()

    def parse(self, template: str) -> List[TemplateExpression]:
        """解析模板"""
        expressions = []
        pos = 0

        while pos < len(template):
            # 查找下一个表达式
            start = template.find('{{', pos)
            if start == -1:
                # 没有更多表达式，添加剩余文本
                if pos < len(template):
                    expressions.append(TextExpression(template[pos:]))
                break

            # 添加表达式前的文本
            if start > pos:
                expressions.append(TextExpression(template[pos:start]))

            # 查找表达式结束
            end = template.find('}}', start)
            if end == -1:
                raise ValueError("未闭合的表达式")

            # 解析表达式内容
            expr_content = template[start + 2:end].strip()
            expressions.append(self._parse_expression(expr_content))

            pos = end + 2

        return expressions

    def _parse_expression(self, content: str) -> TemplateExpression:
        """解析单个表达式"""
        content = content.strip()

        # 条件表达式: {% if condition %}...{% endif %}
        if content.startswith('if '):
            condition = content[3:].strip()
            return ConditionalExpression(condition, TextExpression(""))

        # 循环表达式: {% for item in items %}...{% endfor %}
        if content.startswith('for '):
            match = re.match(r'for\s+(\w+)\s+in\s+(\w+)', content)
            if match:
                var_name, list_name = match.groups()
                return LoopExpression(var_name, list_name, TextExpression(""))

        # 函数调用: function(arg1, arg2)
        func_match = re.match(r'(\w+)\((.*)\)', content)
        if func_match:
            func_name, args_str = func_match.groups()
            args = []
            if args_str.strip():
                for arg in args_str.split(','):
                    arg = arg.strip()
                    if arg.startswith('"') and arg.endswith('"'):
                        args.append(TextExpression(arg[1:-1]))
                    else:
                        args.append(VariableExpression(arg))
            return FunctionExpression(func_name, args)

        # 变量引用
        if re.match(r'^\w+$', content):
            return VariableExpression(content)

        # 默认作为文本
        return TextExpression(content)

    def render(self, template: str, variables: Dict[str, Any] = None) -> str:
        """渲染模板"""
        # 设置变量
        if variables:
            for name, value in variables.items():
                self.context.set_variable(name, value)

        # 解析并渲染
        expressions = self.parse(template)
        return "".join(expr.render(self.context) for expr in expressions)


# ==================== 业务规则引擎 ====================
class RuleCondition(ABC):
    """规则条件基类"""

    @abstractmethod
    def evaluate(self, facts: Dict[str, Any]) -> bool:
        pass


class SimpleCondition(RuleCondition):
    """简单条件"""

    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator
        self.value = value

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        fact_value = facts.get(self.field)

        # 如果字段不存在，返回False
        if fact_value is None:
            return False

        if self.operator == '==':
            return fact_value == self.value
        elif self.operator == '!=':
            return fact_value != self.value
        elif self.operator == '>':
            try:
                return fact_value > self.value
            except TypeError:
                return False
        elif self.operator == '>=':
            try:
                return fact_value >= self.value
            except TypeError:
                return False
        elif self.operator == '<':
            try:
                return fact_value < self.value
            except TypeError:
                return False
        elif self.operator == '<=':
            try:
                return fact_value <= self.value
            except TypeError:
                return False
        elif self.operator == 'in':
            return fact_value in self.value
        elif self.operator == 'contains':
            return self.value in fact_value if fact_value else False

        return False


class CompositeCondition(RuleCondition):
    """复合条件"""

    def __init__(self, left: RuleCondition, operator: str, right: RuleCondition):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        if self.operator == 'and':
            return self.left.evaluate(facts) and self.right.evaluate(facts)
        elif self.operator == 'or':
            return self.left.evaluate(facts) or self.right.evaluate(facts)

        return False


class RuleAction(ABC):
    """规则动作基类"""

    @abstractmethod
    def execute(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        pass


class SetValueAction(RuleAction):
    """设置值动作"""

    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def execute(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        facts[self.field] = self.value
        return facts


class CalculateAction(RuleAction):
    """计算动作"""

    def __init__(self, field: str, expression: str):
        self.field = field
        self.expression = expression

    def execute(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        # 简单的表达式计算
        try:
            # 替换变量
            expr = self.expression
            for key, value in facts.items():
                expr = expr.replace(f'{{{key}}}', str(value))

            # 安全的表达式评估（仅支持基本运算）
            if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expr):
                result = eval(expr)
                facts[self.field] = result
        except:
            pass

        return facts


class BusinessRule:
    """业务规则"""

    def __init__(self, name: str, condition: RuleCondition, action: RuleAction, priority: int = 0):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        """评估规则条件"""
        return self.condition.evaluate(facts)

    def execute(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则动作"""
        return self.action.execute(facts)


class RuleEngine:
    """规则引擎"""

    def __init__(self):
        self.rules: List[BusinessRule] = []

    def add_rule(self, rule: BusinessRule):
        """添加规则"""
        self.rules.append(rule)
        # 按优先级排序
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def execute(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则引擎"""
        result_facts = facts.copy()
        executed_rules = []

        for rule in self.rules:
            if rule.evaluate(result_facts):
                result_facts = rule.execute(result_facts)
                executed_rules.append(rule.name)

        result_facts['_executed_rules'] = executed_rules
        return result_facts


# ==================== 演示函数 ====================
def demonstrate_template_engine():
    """演示模板引擎"""
    print("=" * 60)
    print("模板引擎解释器演示")
    print("=" * 60)

    engine = TemplateEngine()

    # 简单变量替换
    template1 = "Hello, {{name}}! Welcome to {{company}}."
    variables1 = {"name": "张三", "company": "科技公司"}

    result1 = engine.render(template1, variables1)
    print(f"模板1: {template1}")
    print(f"结果1: {result1}")

    # 函数调用
    template2 = "用户名: {{upper(name)}}, 注册日期: {{format_date(register_date, \"%Y年%m月%d日\")}}"
    variables2 = {
        "name": "李四",
        "register_date": datetime(2023, 6, 15)
    }

    result2 = engine.render(template2, variables2)
    print(f"\n模板2: {template2}")
    print(f"结果2: {result2}")

    # 邮件模板示例
    email_template = """
亲爱的 {{name}}，

感谢您注册我们的服务！

您的账户信息：
- 用户名: {{username}}
- 邮箱: {{email}}
- 注册时间: {{format_date(register_time, \"%Y-%m-%d %H:%M\")}}

{{default(welcome_message, \"欢迎使用我们的服务！\")}}

祝好！
{{company}} 团队
"""

    email_vars = {
        "name": "王五",
        "username": "wangwu",
        "email": "wangwu@example.com",
        "register_time": datetime.now(),
        "company": "ABC科技"
    }

    email_result = engine.render(email_template, email_vars)
    print(f"\n邮件模板结果:")
    print(email_result)


def demonstrate_rule_engine():
    """演示规则引擎"""
    print("\n" + "=" * 60)
    print("业务规则引擎演示")
    print("=" * 60)

    engine = RuleEngine()

    # 添加规则：VIP客户折扣
    vip_condition = SimpleCondition("customer_type", "==", "VIP")
    vip_action = SetValueAction("discount", 0.2)
    vip_rule = BusinessRule("VIP折扣", vip_condition, vip_action, priority=10)
    engine.add_rule(vip_rule)

    # 添加规则：大额订单折扣
    large_order_condition = SimpleCondition("order_amount", ">", 1000)
    large_order_action = SetValueAction("discount", 0.1)
    large_order_rule = BusinessRule("大额订单折扣", large_order_condition, large_order_action, priority=5)
    engine.add_rule(large_order_rule)

    # 添加规则：计算最终价格
    calc_condition = SimpleCondition("discount", ">", 0)
    calc_action = CalculateAction("final_price", "{order_amount} * (1 - {discount})")
    calc_rule = BusinessRule("计算最终价格", calc_condition, calc_action, priority=1)
    engine.add_rule(calc_rule)

    # 测试案例
    test_cases = [
        {
            "customer_name": "张三",
            "customer_type": "VIP",
            "order_amount": 800
        },
        {
            "customer_name": "李四",
            "customer_type": "普通",
            "order_amount": 1200
        },
        {
            "customer_name": "王五",
            "customer_type": "普通",
            "order_amount": 500
        }
    ]

    print("规则执行结果:")
    for i, facts in enumerate(test_cases, 1):
        print(f"\n案例 {i}: {facts}")
        result = engine.execute(facts)
        print(f"执行后: {result}")
        print(f"执行的规则: {result.get('_executed_rules', [])}")


def demonstrate_simple_script():
    """演示简单脚本语言"""
    print("\n" + "=" * 60)
    print("简单脚本语言解释器演示")
    print("=" * 60)

    # 简单的脚本解释器（基于配置解释器的扩展）
    from typing import Dict, Any

    class SimpleScript:
        def __init__(self):
            self.variables: Dict[str, Any] = {}

        def execute(self, script: str) -> Dict[str, Any]:
            """执行脚本"""
            lines = script.strip().split('\n')

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 变量赋值
                if '=' in line:
                    parts = line.split('=', 1)
                    var_name = parts[0].strip()
                    value_expr = parts[1].strip()

                    # 简单的值解析
                    if value_expr.startswith('"') and value_expr.endswith('"'):
                        self.variables[var_name] = value_expr[1:-1]
                    elif value_expr.isdigit():
                        self.variables[var_name] = int(value_expr)
                    elif value_expr.replace('.', '').isdigit():
                        self.variables[var_name] = float(value_expr)
                    elif value_expr.lower() in ('true', 'false'):
                        self.variables[var_name] = value_expr.lower() == 'true'
                    else:
                        # 变量引用或表达式
                        self.variables[var_name] = self._evaluate_expression(value_expr)

                # 打印语句
                elif line.startswith('print '):
                    expr = line[6:].strip()
                    value = self._evaluate_expression(expr)
                    print(f"脚本输出: {value}")

            return self.variables

        def _evaluate_expression(self, expr: str) -> Any:
            """评估表达式"""
            expr = expr.strip()

            # 字符串字面量
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]

            # 数字
            if expr.isdigit():
                return int(expr)

            # 变量引用
            if expr in self.variables:
                return self.variables[expr]

            # 简单算术表达式
            try:
                # 替换变量
                for var, value in self.variables.items():
                    expr = expr.replace(var, str(value))

                # 安全评估
                if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expr):
                    return eval(expr)
            except:
                pass

            return expr

    # 示例脚本
    script = '''
# 简单计算脚本
x = 10
y = 20
sum = x + y
product = x * y

print sum
print product

# 字符串处理
name = "Python"
greeting = "Hello, " + name
print greeting

# 条件逻辑（简化）
is_positive = true
result = 100
print result
'''

    interpreter = SimpleScript()
    print("执行脚本:")
    print(script)
    print("-" * 40)

    variables = interpreter.execute(script)
    print(f"\n最终变量状态: {variables}")


if __name__ == "__main__":
    demonstrate_template_engine()
    demonstrate_rule_engine()
    demonstrate_simple_script()
