"""
03_config_interpreter.py - 配置文件解释器

这个示例展示了如何使用解释器模式来解析和执行配置文件。
支持变量定义、条件表达式、函数调用等特性，
可以用于复杂的配置管理和动态配置生成。
"""

import re
from typing import Dict, List, Any, Union, Optional
from enum import Enum
import os


# ==================== 配置值类型 ====================
class ConfigValue:
    """配置值基类"""

    def __init__(self, value: Any):
        self.value = value

    def get_value(self) -> Any:
        return self.value

    def __str__(self):
        return str(self.value)


class StringValue(ConfigValue):
    """字符串值"""

    def __init__(self, value: str):
        super().__init__(value)

    def get_value(self) -> str:
        return self.value


class NumberValue(ConfigValue):
    """数字值"""

    def __init__(self, value: Union[int, float]):
        super().__init__(value)

    def get_value(self) -> Union[int, float]:
        return self.value


class BooleanValue(ConfigValue):
    """布尔值"""

    def __init__(self, value: bool):
        super().__init__(value)

    def get_value(self) -> bool:
        return self.value


class ListValue(ConfigValue):
    """列表值"""

    def __init__(self, value: List[ConfigValue]):
        super().__init__(value)

    def get_value(self) -> List[Any]:
        return [item.get_value() for item in self.value]


class DictValue(ConfigValue):
    """字典值"""

    def __init__(self, value: Dict[str, ConfigValue]):
        super().__init__(value)

    def get_value(self) -> Dict[str, Any]:
        return {key: val.get_value() for key, val in self.value.items()}


# ==================== 配置上下文 ====================
class ConfigContext:
    """配置解释器上下文"""

    def __init__(self):
        self.variables: Dict[str, ConfigValue] = {}
        self.functions: Dict[str, callable] = {}
        self.environment_vars = dict(os.environ)
        self.debug = False

        # 注册内置函数
        self._register_builtin_functions()

    def _register_builtin_functions(self):
        """注册内置函数"""
        self.functions.update({
            'env': self._env_function,
            'default': self._default_function,
            'concat': self._concat_function,
            'upper': self._upper_function,
            'lower': self._lower_function,
            'len': self._len_function,
            'int': self._int_function,
            'float': self._float_function,
            'bool': self._bool_function,
            'str': self._str_function,
        })

    def _env_function(self, *args) -> str:
        """获取环境变量"""
        if len(args) < 1 or len(args) > 2:
            raise ValueError("env() 函数需要1-2个参数")
        var_name = args[0]
        default_value = args[1] if len(args) > 1 else ""
        return self.environment_vars.get(var_name, default_value)

    def _default_function(self, *args) -> Any:
        """如果值为空则返回默认值"""
        if len(args) != 2:
            raise ValueError("default() 函数需要2个参数")
        value, default_value = args
        return default_value if not value else value

    def _concat_function(self, *args) -> str:
        """连接字符串"""
        return ''.join(str(arg) for arg in args)

    def _upper_function(self, *args) -> str:
        """转换为大写"""
        if len(args) != 1:
            raise ValueError("upper() 函数需要1个参数")
        return str(args[0]).upper()

    def _lower_function(self, *args) -> str:
        """转换为小写"""
        if len(args) != 1:
            raise ValueError("lower() 函数需要1个参数")
        return str(args[0]).lower()

    def _len_function(self, *args) -> int:
        """获取长度"""
        if len(args) != 1:
            raise ValueError("len() 函数需要1个参数")
        obj = args[0]
        if isinstance(obj, (list, dict, str)):
            return len(obj)
        return 0

    def _int_function(self, *args) -> int:
        """转换为整数"""
        if len(args) != 1:
            raise ValueError("int() 函数需要1个参数")
        return int(args[0])

    def _float_function(self, *args) -> float:
        """转换为浮点数"""
        if len(args) != 1:
            raise ValueError("float() 函数需要1个参数")
        return float(args[0])

    def _bool_function(self, *args) -> bool:
        """转换为布尔值"""
        if len(args) != 1:
            raise ValueError("bool() 函数需要1个参数")
        value = args[0]
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'on')
        return bool(value)

    def _str_function(self, *args) -> str:
        """转换为字符串"""
        if len(args) != 1:
            raise ValueError("str() 函数需要1个参数")
        return str(args[0])

    def set_variable(self, name: str, value: ConfigValue):
        """设置变量"""
        self.variables[name] = value
        if self.debug:
            print(f"设置变量: {name} = {value}")

    def get_variable(self, name: str) -> ConfigValue:
        """获取变量"""
        if name not in self.variables:
            raise ValueError(f"未定义的变量: {name}")
        return self.variables[name]

    def has_variable(self, name: str) -> bool:
        """检查变量是否存在"""
        return name in self.variables

    def call_function(self, name: str, *args) -> Any:
        """调用函数"""
        if name not in self.functions:
            raise ValueError(f"未定义的函数: {name}")

        func = self.functions[name]
        try:
            result = func(*args)
            if self.debug:
                print(f"调用函数: {name}({', '.join(map(str, args))}) = {result}")
            return result
        except Exception as e:
            raise ValueError(f"函数 {name} 执行错误: {str(e)}")

    def set_debug(self, debug: bool):
        """设置调试模式"""
        self.debug = debug


# ==================== 配置表达式 ====================
class ConfigExpression:
    """配置表达式基类"""

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        raise NotImplementedError


class LiteralExpression(ConfigExpression):
    """字面量表达式"""

    def __init__(self, value: ConfigValue):
        self.value = value

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        return self.value

    def __str__(self):
        return str(self.value)


class VariableExpression(ConfigExpression):
    """变量表达式"""

    def __init__(self, name: str):
        self.name = name

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        return context.get_variable(self.name)

    def __str__(self):
        return f"${self.name}"


class FunctionCallExpression(ConfigExpression):
    """函数调用表达式"""

    def __init__(self, name: str, args: List[ConfigExpression]):
        self.name = name
        self.args = args

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        # 评估所有参数
        arg_values = [arg.evaluate(context).get_value() for arg in self.args]

        # 调用函数
        result = context.call_function(self.name, *arg_values)

        # 包装结果
        if isinstance(result, str):
            return StringValue(result)
        elif isinstance(result, (int, float)):
            return NumberValue(result)
        elif isinstance(result, bool):
            return BooleanValue(result)
        elif isinstance(result, list):
            return ListValue([self._wrap_value(item) for item in result])
        elif isinstance(result, dict):
            return DictValue({k: self._wrap_value(v) for k, v in result.items()})
        else:
            return StringValue(str(result))

    def _wrap_value(self, value: Any) -> ConfigValue:
        """包装值为ConfigValue"""
        if isinstance(value, str):
            return StringValue(value)
        elif isinstance(value, (int, float)):
            return NumberValue(value)
        elif isinstance(value, bool):
            return BooleanValue(value)
        else:
            return StringValue(str(value))

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"


class ConditionalExpression(ConfigExpression):
    """条件表达式"""

    def __init__(self, condition: ConfigExpression, true_expr: ConfigExpression, false_expr: ConfigExpression):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        condition_value = self.condition.evaluate(context)

        # 判断条件真假
        if isinstance(condition_value, BooleanValue):
            is_true = condition_value.get_value()
        elif isinstance(condition_value, StringValue):
            is_true = bool(condition_value.get_value().strip())
        elif isinstance(condition_value, NumberValue):
            is_true = condition_value.get_value() != 0
        else:
            is_true = bool(condition_value.get_value())

        if is_true:
            return self.true_expr.evaluate(context)
        else:
            return self.false_expr.evaluate(context)

    def __str__(self):
        return f"if {self.condition} then {self.true_expr} else {self.false_expr}"


class StringInterpolationExpression(ConfigExpression):
    """字符串插值表达式"""

    def __init__(self, template: str, expressions: Dict[str, ConfigExpression]):
        self.template = template
        self.expressions = expressions

    def evaluate(self, context: ConfigContext) -> ConfigValue:
        result = self.template

        for placeholder, expr in self.expressions.items():
            value = expr.evaluate(context).get_value()
            result = result.replace(f"${{{placeholder}}}", str(value))

        return StringValue(result)

    def __str__(self):
        return f'"{self.template}"'


# ==================== 配置解析器 ====================
class ConfigParser:
    """配置文件解析器"""

    def __init__(self):
        self.context = ConfigContext()

    def parse_file(self, filename: str) -> Dict[str, Any]:
        """解析配置文件"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_content(content)

    def parse_content(self, content: str) -> Dict[str, Any]:
        """解析配置内容"""
        lines = content.strip().split('\n')
        config = {}

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue

            try:
                key, value = self._parse_line(line)
                if key:
                    config[key] = value
            except Exception as e:
                raise ValueError(f"配置解析错误在第 {line_num} 行: {str(e)}")

        return config

    def _parse_line(self, line: str) -> tuple[Optional[str], Any]:
        """解析单行配置"""
        # 匹配赋值语句: key = value
        match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$', line)
        if not match:
            return None, None

        key = match.group(1)
        value_str = match.group(2).strip()

        # 解析值表达式
        expr = self._parse_expression(value_str)
        value = expr.evaluate(self.context)

        # 将值存储到上下文中
        self.context.set_variable(key, value)

        return key, value.get_value()

    def _parse_expression(self, expr_str: str) -> ConfigExpression:
        """解析表达式"""
        expr_str = expr_str.strip()

        # 字符串字面量
        if expr_str.startswith('"') and expr_str.endswith('"'):
            content = expr_str[1:-1]
            # 检查字符串插值
            interpolations = re.findall(r'\$\{([^}]+)\}', content)
            if interpolations:
                expressions = {}
                for placeholder in interpolations:
                    expressions[placeholder] = self._parse_expression(placeholder)
                return StringInterpolationExpression(content, expressions)
            else:
                return LiteralExpression(StringValue(content))

        # 数字字面量
        if re.match(r'^-?\d+(\.\d+)?$', expr_str):
            if '.' in expr_str:
                return LiteralExpression(NumberValue(float(expr_str)))
            else:
                return LiteralExpression(NumberValue(int(expr_str)))

        # 布尔字面量
        if expr_str.lower() in ('true', 'false'):
            return LiteralExpression(BooleanValue(expr_str.lower() == 'true'))

        # 变量引用
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr_str):
            return VariableExpression(expr_str)

        # 函数调用
        func_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)$', expr_str)
        if func_match:
            func_name = func_match.group(1)
            args_str = func_match.group(2).strip()

            args = []
            if args_str:
                # 改进的参数分割，处理引号内的逗号
                arg_parts = self._split_function_args(args_str)
                for arg_part in arg_parts:
                    args.append(self._parse_expression(arg_part.strip()))

            return FunctionCallExpression(func_name, args)

        # 条件表达式 (简化版) - 只在不是字符串字面量时处理
        if not (expr_str.startswith('"') and expr_str.endswith('"')):
            if ' if ' in expr_str and ' else ' in expr_str:
                # 找到 if 和 else 的位置
                if_pos = expr_str.find(' if ')
                else_pos = expr_str.find(' else ')

                if if_pos != -1 and else_pos != -1 and if_pos < else_pos:
                    true_part = expr_str[:if_pos].strip()
                    condition_part = expr_str[if_pos + 4:else_pos].strip()
                    false_part = expr_str[else_pos + 5:].strip()

                    return ConditionalExpression(
                        self._parse_expression(condition_part),
                        self._parse_expression(true_part),
                        self._parse_expression(false_part)
                    )

        # 默认作为字符串处理
        return LiteralExpression(StringValue(expr_str))

    def _split_function_args(self, args_str: str) -> List[str]:
        """分割函数参数，处理引号内的逗号"""
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None
        paren_depth = 0

        for char in args_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_arg += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_arg += char
            elif char == '(' and not in_quotes:
                paren_depth += 1
                current_arg += char
            elif char == ')' and not in_quotes:
                paren_depth -= 1
                current_arg += char
            elif char == ',' and not in_quotes and paren_depth == 0:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char

        if current_arg.strip():
            args.append(current_arg.strip())

        return args

    def set_debug(self, debug: bool):
        """设置调试模式"""
        self.context.set_debug(debug)


# ==================== 演示函数 ====================
def demonstrate_config_interpreter():
    """演示配置解释器功能"""
    print("=" * 60)
    print("配置文件解释器演示")
    print("=" * 60)

    # 创建示例配置内容
    config_content = '''
# 应用配置示例
app_name = "MyApplication"
app_version = "1.0.0"
debug_mode = true
port = 8080
max_connections = 100

# 环境相关配置
environment = env("ENVIRONMENT", "development")
database_url = "postgresql://localhost:5432/${app_name}_${environment}"

# 条件配置
log_level = "DEBUG" if debug_mode else "INFO"
worker_count = 4 if environment == "production" else 2

# 函数调用示例
app_title = upper(app_name)
config_summary = concat("App: ", app_name, " v", app_version)

# 复杂表达式
is_production = bool(env("PRODUCTION", "false"))
cache_size = int(env("CACHE_SIZE", "1000"))
'''

    print("配置内容:")
    print(config_content)
    print("-" * 60)

    # 解析配置
    parser = ConfigParser()
    parser.set_debug(True)

    try:
        config = parser.parse_content(config_content)

        print("解析结果:")
        for key, value in config.items():
            print(f"{key} = {value} ({type(value).__name__})")

    except Exception as e:
        print(f"解析错误: {e}")


def demonstrate_advanced_config():
    """演示高级配置特性"""
    print("\n" + "=" * 60)
    print("高级配置特性演示")
    print("=" * 60)

    # 设置环境变量
    import os
    os.environ['APP_ENV'] = 'production'
    os.environ['DB_HOST'] = 'prod-db.example.com'
    os.environ['DB_PORT'] = '5432'

    advanced_config = '''
# 高级配置示例
environment = env("APP_ENV", "development")
db_host = env("DB_HOST", "localhost")
db_port = int(env("DB_PORT", "5432"))

# 复杂字符串插值
database_url = "postgresql://${db_host}:${db_port}/myapp_${environment}"

# 嵌套条件
max_workers = 8 if environment == "production" else 2 if environment == "staging" else 1

# 函数组合
app_config = concat("Environment: ", upper(environment), ", Workers: ", str(max_workers))

# 默认值处理
redis_url = default(env("REDIS_URL"), "redis://localhost:6379")
cache_enabled = bool(env("CACHE_ENABLED", "true"))
'''

    print("高级配置内容:")
    print(advanced_config)
    print("-" * 60)

    parser = ConfigParser()

    try:
        config = parser.parse_content(advanced_config)

        print("解析结果:")
        for key, value in config.items():
            print(f"{key} = {value}")

    except Exception as e:
        print(f"解析错误: {e}")


if __name__ == "__main__":
    demonstrate_config_interpreter()
    demonstrate_advanced_config()
