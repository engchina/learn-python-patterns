"""
02_calculator_interpreter.py - 完整的计算器解释器

这个示例展示了一个完整的计算器解释器实现，包括：
1. 词法分析器（Lexer）- 将输入文本分解为词法单元
2. 语法分析器（Parser）- 构建抽象语法树
3. 解释器（Interpreter）- 执行计算
支持括号、运算符优先级、浮点数等特性。
"""

import re
from typing import List, Union, Optional
from enum import Enum


# ==================== 词法单元定义 ====================
class TokenType(Enum):
    """词法单元类型"""
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POWER = "POWER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    ASSIGN = "ASSIGN"


class Token:
    """词法单元"""
    
    def __init__(self, type_: TokenType, value: str, position: int = 0):
        self.type = type_
        self.value = value
        self.position = position
    
    def __str__(self):
        return f"Token({self.type.value}, '{self.value}', {self.position})"
    
    def __repr__(self):
        return self.__str__()


# ==================== 词法分析器 ====================
class Lexer:
    """词法分析器 - 将输入文本转换为词法单元序列"""
    
    def __init__(self, text: str):
        self.text = text.strip()
        self.position = 0
        self.current_char = self.text[0] if self.text else None
    
    def error(self, message: str = ""):
        """抛出词法分析错误"""
        raise ValueError(f"词法分析错误在位置 {self.position}: {message}")
    
    def advance(self):
        """移动到下一个字符"""
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.position]
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def read_number(self) -> str:
        """读取数字（支持浮点数）"""
        result = ""
        start_pos = self.position
        
        # 读取整数部分
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # 读取小数部分
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            
            if not (self.current_char and self.current_char.isdigit()):
                self.error(f"小数点后必须有数字")
            
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        # 读取科学计数法
        if self.current_char and self.current_char.lower() == 'e':
            result += self.current_char
            self.advance()
            
            if self.current_char in ['+', '-']:
                result += self.current_char
                self.advance()
            
            if not (self.current_char and self.current_char.isdigit()):
                self.error("科学计数法指数部分必须是数字")
            
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        
        return result
    
    def read_identifier(self) -> str:
        """读取标识符"""
        result = ""
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self) -> Token:
        """获取下一个词法单元"""
        while self.current_char is not None:
            pos = self.position
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number(), pos)
            
            if self.current_char.isalpha() or self.current_char == '_':
                return Token(TokenType.IDENTIFIER, self.read_identifier(), pos)
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', pos)
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', pos)
            
            if self.current_char == '*':
                self.advance()
                if self.current_char == '*':  # 支持 ** 作为幂运算
                    self.advance()
                    return Token(TokenType.POWER, '**', pos)
                return Token(TokenType.MULTIPLY, '*', pos)
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', pos)
            
            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POWER, '^', pos)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', pos)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', pos)
            
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=', pos)
            
            self.error(f"无效字符: '{self.current_char}'")
        
        return Token(TokenType.EOF, '', self.position)


# ==================== 抽象语法树节点 ====================
class ASTNode:
    """抽象语法树节点基类"""
    pass


class NumberNode(ASTNode):
    """数字节点"""
    
    def __init__(self, value: Union[int, float]):
        self.value = value
    
    def __str__(self):
        return str(self.value)


class VariableNode(ASTNode):
    """变量节点"""
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name


class BinaryOpNode(ASTNode):
    """二元运算节点"""
    
    def __init__(self, left: ASTNode, operator: Token, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.operator.value} {self.right})"


class UnaryOpNode(ASTNode):
    """一元运算节点"""
    
    def __init__(self, operator: Token, operand: ASTNode):
        self.operator = operator
        self.operand = operand
    
    def __str__(self):
        return f"{self.operator.value}{self.operand}"


class AssignNode(ASTNode):
    """赋值节点"""
    
    def __init__(self, variable: str, value: ASTNode):
        self.variable = variable
        self.value = value
    
    def __str__(self):
        return f"{self.variable} = {self.value}"


# ==================== 语法分析器 ====================
class Parser:
    """语法分析器 - 构建抽象语法树"""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, message: str = ""):
        """抛出语法分析错误"""
        raise ValueError(f"语法错误在位置 {self.current_token.position}: {message}")
    
    def eat(self, token_type: TokenType):
        """消费指定类型的词法单元"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"期望 {token_type.value}, 但得到 {self.current_token.type.value}")
    
    def factor(self) -> ASTNode:
        """
        因子: NUMBER | IDENTIFIER | LPAREN expr RPAREN | (PLUS | MINUS) factor
        """
        token = self.current_token
        
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOpNode(token, self.factor())
        
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOpNode(token, self.factor())
        
        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            # 尝试转换为整数，如果失败则转换为浮点数
            try:
                value = int(token.value)
            except ValueError:
                value = float(token.value)
            return NumberNode(value)
        
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return VariableNode(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        else:
            self.error(f"无效的因子: {token}")
    
    def power(self) -> ASTNode:
        """
        幂运算: factor (POWER factor)*
        右结合，即 2^3^2 = 2^(3^2) = 2^9 = 512
        """
        node = self.factor()
        
        if self.current_token.type == TokenType.POWER:
            token = self.current_token
            self.eat(TokenType.POWER)
            # 右结合：递归调用 power() 而不是 factor()
            node = BinaryOpNode(node, token, self.power())
        
        return node
    
    def term(self) -> ASTNode:
        """
        项: power ((MULTIPLY | DIVIDE) power)*
        """
        node = self.power()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            
            node = BinaryOpNode(node, token, self.power())
        
        return node
    
    def expr(self) -> ASTNode:
        """
        表达式: term ((PLUS | MINUS) term)*
        """
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            node = BinaryOpNode(node, token, self.term())
        
        return node
    
    def assignment(self) -> ASTNode:
        """
        赋值: IDENTIFIER ASSIGN expr | expr
        """
        if (self.current_token.type == TokenType.IDENTIFIER and 
            self.lexer.text[self.lexer.position:].lstrip().startswith('=')):
            
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            self.eat(TokenType.ASSIGN)
            value = self.expr()
            return AssignNode(var_name, value)
        else:
            return self.expr()
    
    def parse(self) -> ASTNode:
        """解析输入并返回抽象语法树"""
        node = self.assignment()
        if self.current_token.type != TokenType.EOF:
            self.error("表达式解析不完整")
        return node


# ==================== 解释器 ====================
class Calculator:
    """计算器解释器"""
    
    def __init__(self):
        self.variables = {}
        self.debug = False
    
    def set_debug(self, debug: bool):
        """设置调试模式"""
        self.debug = debug
    
    def visit(self, node: ASTNode) -> Union[int, float]:
        """访问AST节点并执行相应操作"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode):
        """通用访问方法"""
        raise ValueError(f"没有为节点类型 {type(node).__name__} 定义访问方法")
    
    def visit_NumberNode(self, node: NumberNode) -> Union[int, float]:
        """访问数字节点"""
        if self.debug:
            print(f"访问数字: {node.value}")
        return node.value
    
    def visit_VariableNode(self, node: VariableNode) -> Union[int, float]:
        """访问变量节点"""
        if node.name not in self.variables:
            raise ValueError(f"未定义的变量: {node.name}")
        
        value = self.variables[node.name]
        if self.debug:
            print(f"访问变量: {node.name} = {value}")
        return value
    
    def visit_BinaryOpNode(self, node: BinaryOpNode) -> Union[int, float]:
        """访问二元运算节点"""
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        
        if node.operator.type == TokenType.PLUS:
            result = left_val + right_val
        elif node.operator.type == TokenType.MINUS:
            result = left_val - right_val
        elif node.operator.type == TokenType.MULTIPLY:
            result = left_val * right_val
        elif node.operator.type == TokenType.DIVIDE:
            if right_val == 0:
                raise ValueError("除零错误")
            result = left_val / right_val
        elif node.operator.type == TokenType.POWER:
            result = left_val ** right_val
        else:
            raise ValueError(f"未知的二元运算符: {node.operator.type}")
        
        if self.debug:
            print(f"二元运算: {left_val} {node.operator.value} {right_val} = {result}")
        
        return result
    
    def visit_UnaryOpNode(self, node: UnaryOpNode) -> Union[int, float]:
        """访问一元运算节点"""
        operand_val = self.visit(node.operand)
        
        if node.operator.type == TokenType.PLUS:
            result = +operand_val
        elif node.operator.type == TokenType.MINUS:
            result = -operand_val
        else:
            raise ValueError(f"未知的一元运算符: {node.operator.type}")
        
        if self.debug:
            print(f"一元运算: {node.operator.value}{operand_val} = {result}")
        
        return result
    
    def visit_AssignNode(self, node: AssignNode) -> Union[int, float]:
        """访问赋值节点"""
        value = self.visit(node.value)
        self.variables[node.variable] = value
        
        if self.debug:
            print(f"赋值: {node.variable} = {value}")
        
        return value
    
    def evaluate(self, text: str) -> Union[int, float]:
        """评估表达式"""
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()
            return self.visit(ast)
        except Exception as e:
            raise ValueError(f"计算错误: {str(e)}")
    
    def get_variables(self) -> dict:
        """获取所有变量"""
        return self.variables.copy()
    
    def clear_variables(self):
        """清空所有变量"""
        self.variables.clear()


# ==================== 演示函数 ====================
def demonstrate_calculator():
    """演示计算器功能"""
    print("=" * 60)
    print("完整计算器解释器演示")
    print("=" * 60)
    
    calc = Calculator()
    calc.set_debug(True)
    
    expressions = [
        "3 + 5",
        "10 - 4 * 2",
        "(2 + 3) * 4",
        "2 ** 3 ** 2",  # 右结合: 2^(3^2) = 2^9 = 512
        "2^3^2",        # 同上
        "-5 + 3",
        "+(10 - 5)",
        "3.14 * 2",
        "10 / 3",
        "x = 5",
        "y = x * 2",
        "x + y",
        "z = (x + y) / 2",
        "z"
    ]
    
    print("计算表达式:")
    for expr in expressions:
        try:
            result = calc.evaluate(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> 错误: {e}")
        print()
    
    print(f"最终变量状态: {calc.get_variables()}")


def interactive_calculator():
    """交互式计算器"""
    print("\n" + "=" * 60)
    print("交互式计算器")
    print("=" * 60)
    print("输入数学表达式进行计算，输入 'quit' 退出")
    print("支持: +, -, *, /, ^, **, (), 变量赋值")
    print("示例: x = 5, y = x * 2, (x + y) / 2")
    print("-" * 60)
    
    calc = Calculator()
    
    while True:
        try:
            expr = input(">>> ").strip()
            if expr.lower() in ['quit', 'exit', 'q']:
                break
            
            if expr.lower() == 'vars':
                print(f"变量: {calc.get_variables()}")
                continue
            
            if expr.lower() == 'clear':
                calc.clear_variables()
                print("变量已清空")
                continue
            
            if not expr:
                continue
            
            result = calc.evaluate(expr)
            print(f"= {result}")
            
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    demonstrate_calculator()
    # 取消注释下面的行来启动交互式计算器
    # interactive_calculator()
