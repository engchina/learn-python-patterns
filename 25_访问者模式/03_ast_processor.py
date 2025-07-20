"""
03_ast_processor.py - 抽象语法树处理的访问者实现

这个示例展示了访问者模式在编译器设计中的应用：
- 抽象语法树的表示
- 不同类型的AST节点处理
- 代码分析、优化、生成等操作
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum


class NodeType(Enum):
    """AST节点类型"""
    PROGRAM = "程序"
    FUNCTION = "函数"
    VARIABLE = "变量"
    BINARY_OP = "二元运算"
    ASSIGNMENT = "赋值"
    IF_STATEMENT = "条件语句"
    WHILE_LOOP = "循环语句"
    LITERAL = "字面量"


# ==================== 抽象访问者 ====================
class ASTVisitor(ABC):
    """AST访问者抽象类"""
    
    @abstractmethod
    def visit_program(self, program):
        """访问程序节点"""
        pass
    
    @abstractmethod
    def visit_function(self, function):
        """访问函数节点"""
        pass
    
    @abstractmethod
    def visit_variable(self, variable):
        """访问变量节点"""
        pass
    
    @abstractmethod
    def visit_binary_operation(self, binary_op):
        """访问二元运算节点"""
        pass
    
    @abstractmethod
    def visit_assignment(self, assignment):
        """访问赋值节点"""
        pass
    
    @abstractmethod
    def visit_if_statement(self, if_stmt):
        """访问条件语句节点"""
        pass
    
    @abstractmethod
    def visit_while_loop(self, while_loop):
        """访问循环语句节点"""
        pass
    
    @abstractmethod
    def visit_literal(self, literal):
        """访问字面量节点"""
        pass


# ==================== 抽象AST节点 ====================
class ASTNode(ABC):
    """AST节点抽象类"""
    
    def __init__(self, node_type: NodeType, line: int = 0):
        self.node_type = node_type
        self.line = line
        self.parent: Optional[ASTNode] = None
        self.children: List[ASTNode] = []
    
    @abstractmethod
    def accept(self, visitor: ASTVisitor):
        """接受访问者"""
        pass
    
    def add_child(self, child: 'ASTNode'):
        """添加子节点"""
        child.parent = self
        self.children.append(child)


# ==================== 具体AST节点 ====================
class ProgramNode(ASTNode):
    """程序节点"""
    
    def __init__(self, name: str):
        super().__init__(NodeType.PROGRAM)
        self.name = name
        self.functions: List['FunctionNode'] = []
        self.global_variables: List['VariableNode'] = []
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_program(self)
    
    def add_function(self, function: 'FunctionNode'):
        """添加函数"""
        self.functions.append(function)
        self.add_child(function)
    
    def add_global_variable(self, variable: 'VariableNode'):
        """添加全局变量"""
        self.global_variables.append(variable)
        self.add_child(variable)
    
    def __str__(self):
        return f"程序: {self.name}"


class FunctionNode(ASTNode):
    """函数节点"""
    
    def __init__(self, name: str, return_type: str, line: int = 0):
        super().__init__(NodeType.FUNCTION, line)
        self.name = name
        self.return_type = return_type
        self.parameters: List['VariableNode'] = []
        self.body: List[ASTNode] = []
        self.local_variables: List['VariableNode'] = []
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_function(self)
    
    def add_parameter(self, param: 'VariableNode'):
        """添加参数"""
        self.parameters.append(param)
        self.add_child(param)
    
    def add_statement(self, stmt: ASTNode):
        """添加语句"""
        self.body.append(stmt)
        self.add_child(stmt)
    
    def __str__(self):
        return f"函数: {self.name}({len(self.parameters)}参数) -> {self.return_type}"


class VariableNode(ASTNode):
    """变量节点"""
    
    def __init__(self, name: str, var_type: str, line: int = 0):
        super().__init__(NodeType.VARIABLE, line)
        self.name = name
        self.var_type = var_type
        self.is_used = False
        self.is_modified = False
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_variable(self)
    
    def __str__(self):
        return f"变量: {self.name}: {self.var_type}"


class BinaryOperationNode(ASTNode):
    """二元运算节点"""
    
    def __init__(self, operator: str, left: ASTNode, right: ASTNode, line: int = 0):
        super().__init__(NodeType.BINARY_OP, line)
        self.operator = operator
        self.left = left
        self.right = right
        self.add_child(left)
        self.add_child(right)
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_binary_operation(self)
    
    def __str__(self):
        return f"二元运算: {self.operator}"


class AssignmentNode(ASTNode):
    """赋值节点"""
    
    def __init__(self, variable: VariableNode, value: ASTNode, line: int = 0):
        super().__init__(NodeType.ASSIGNMENT, line)
        self.variable = variable
        self.value = value
        self.add_child(variable)
        self.add_child(value)
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_assignment(self)
    
    def __str__(self):
        return f"赋值: {self.variable.name} = ..."


class IfStatementNode(ASTNode):
    """条件语句节点"""
    
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], 
                 else_branch: Optional[List[ASTNode]] = None, line: int = 0):
        super().__init__(NodeType.IF_STATEMENT, line)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch or []
        
        self.add_child(condition)
        for stmt in then_branch:
            self.add_child(stmt)
        for stmt in self.else_branch:
            self.add_child(stmt)
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_if_statement(self)
    
    def __str__(self):
        return f"条件语句: if (...) {len(self.then_branch)}语句 else {len(self.else_branch)}语句"


class WhileLoopNode(ASTNode):
    """循环语句节点"""
    
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int = 0):
        super().__init__(NodeType.WHILE_LOOP, line)
        self.condition = condition
        self.body = body
        
        self.add_child(condition)
        for stmt in body:
            self.add_child(stmt)
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_while_loop(self)
    
    def __str__(self):
        return f"循环语句: while (...) {len(self.body)}语句"


class LiteralNode(ASTNode):
    """字面量节点"""
    
    def __init__(self, value: Any, literal_type: str, line: int = 0):
        super().__init__(NodeType.LITERAL, line)
        self.value = value
        self.literal_type = literal_type
    
    def accept(self, visitor: ASTVisitor):
        visitor.visit_literal(self)
    
    def __str__(self):
        return f"字面量: {self.value} ({self.literal_type})"


# ==================== 具体访问者 ====================
class CodeGeneratorVisitor(ASTVisitor):
    """代码生成访问者"""
    
    def __init__(self, target_language: str = "Python"):
        self.target_language = target_language
        self.generated_code: List[str] = []
        self.indent_level = 0
    
    def _add_line(self, line: str):
        """添加代码行"""
        indent = "    " * self.indent_level
        self.generated_code.append(f"{indent}{line}")
    
    def visit_program(self, program: ProgramNode):
        """生成程序代码"""
        self._add_line(f"# 程序: {program.name}")
        self._add_line("")
        
        # 生成全局变量
        for var in program.global_variables:
            var.accept(self)
        
        if program.global_variables:
            self._add_line("")
        
        # 生成函数
        for func in program.functions:
            func.accept(self)
            self._add_line("")
        
        print(f"🔧 生成程序代码: {program.name}")
    
    def visit_function(self, function: FunctionNode):
        """生成函数代码"""
        params = ", ".join([f"{p.name}: {p.var_type}" for p in function.parameters])
        self._add_line(f"def {function.name}({params}) -> {function.return_type}:")
        
        self.indent_level += 1
        
        if not function.body:
            self._add_line("pass")
        else:
            for stmt in function.body:
                stmt.accept(self)
        
        self.indent_level -= 1
        print(f"🔧 生成函数: {function.name}")
    
    def visit_variable(self, variable: VariableNode):
        """生成变量代码"""
        if variable.parent and isinstance(variable.parent, ProgramNode):
            # 全局变量
            self._add_line(f"{variable.name}: {variable.var_type} = None")
        print(f"🔧 处理变量: {variable.name}")
    
    def visit_binary_operation(self, binary_op: BinaryOperationNode):
        """生成二元运算代码"""
        # 这里简化处理，实际应该递归生成左右操作数
        print(f"🔧 生成二元运算: {binary_op.operator}")
    
    def visit_assignment(self, assignment: AssignmentNode):
        """生成赋值代码"""
        self._add_line(f"{assignment.variable.name} = # 赋值表达式")
        print(f"🔧 生成赋值: {assignment.variable.name}")
    
    def visit_if_statement(self, if_stmt: IfStatementNode):
        """生成条件语句代码"""
        self._add_line("if condition:")  # 简化条件
        self.indent_level += 1
        
        for stmt in if_stmt.then_branch:
            stmt.accept(self)
        
        self.indent_level -= 1
        
        if if_stmt.else_branch:
            self._add_line("else:")
            self.indent_level += 1
            for stmt in if_stmt.else_branch:
                stmt.accept(self)
            self.indent_level -= 1
        
        print(f"🔧 生成条件语句")
    
    def visit_while_loop(self, while_loop: WhileLoopNode):
        """生成循环语句代码"""
        self._add_line("while condition:")  # 简化条件
        self.indent_level += 1
        
        for stmt in while_loop.body:
            stmt.accept(self)
        
        self.indent_level -= 1
        print(f"🔧 生成循环语句")
    
    def visit_literal(self, literal: LiteralNode):
        """生成字面量代码"""
        print(f"🔧 处理字面量: {literal.value}")
    
    def get_generated_code(self) -> str:
        """获取生成的代码"""
        return "\n".join(self.generated_code)


class StaticAnalyzerVisitor(ASTVisitor):
    """静态分析访问者"""
    
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []
        self.variables: Dict[str, VariableNode] = {}
        self.functions: Dict[str, FunctionNode] = {}
        self.complexity_score = 0
    
    def _add_issue(self, severity: str, message: str, node: ASTNode):
        """添加问题"""
        self.issues.append({
            "severity": severity,
            "message": message,
            "line": node.line,
            "node_type": node.node_type.value
        })
    
    def visit_program(self, program: ProgramNode):
        """分析程序"""
        print(f"🔍 分析程序: {program.name}")
        
        # 检查程序结构
        if not program.functions:
            self._add_issue("警告", "程序没有定义任何函数", program)
        
        # 分析全局变量
        for var in program.global_variables:
            self.variables[var.name] = var
            var.accept(self)
        
        # 分析函数
        for func in program.functions:
            self.functions[func.name] = func
            func.accept(self)
    
    def visit_function(self, function: FunctionNode):
        """分析函数"""
        print(f"🔍 分析函数: {function.name}")
        
        # 检查函数复杂度
        if len(function.body) > 20:
            self._add_issue("警告", f"函数 {function.name} 过于复杂 ({len(function.body)} 语句)", function)
            self.complexity_score += 2
        
        # 检查参数数量
        if len(function.parameters) > 5:
            self._add_issue("警告", f"函数 {function.name} 参数过多 ({len(function.parameters)} 个)", function)
        
        # 分析函数体
        for stmt in function.body:
            stmt.accept(self)
    
    def visit_variable(self, variable: VariableNode):
        """分析变量"""
        print(f"🔍 分析变量: {variable.name}")
        
        # 检查变量命名
        if not variable.name.islower():
            self._add_issue("建议", f"变量 {variable.name} 建议使用小写命名", variable)
    
    def visit_binary_operation(self, binary_op: BinaryOperationNode):
        """分析二元运算"""
        print(f"🔍 分析二元运算: {binary_op.operator}")
        
        # 递归分析操作数
        binary_op.left.accept(self)
        binary_op.right.accept(self)
        
        # 检查除零操作
        if (binary_op.operator == "/" and 
            isinstance(binary_op.right, LiteralNode) and 
            binary_op.right.value == 0):
            self._add_issue("错误", "除零操作", binary_op)
    
    def visit_assignment(self, assignment: AssignmentNode):
        """分析赋值"""
        print(f"🔍 分析赋值: {assignment.variable.name}")
        
        assignment.variable.is_modified = True
        assignment.value.accept(self)
    
    def visit_if_statement(self, if_stmt: IfStatementNode):
        """分析条件语句"""
        print(f"🔍 分析条件语句")
        
        self.complexity_score += 1
        
        # 分析条件
        if_stmt.condition.accept(self)
        
        # 分析分支
        for stmt in if_stmt.then_branch:
            stmt.accept(self)
        
        for stmt in if_stmt.else_branch:
            stmt.accept(self)
    
    def visit_while_loop(self, while_loop: WhileLoopNode):
        """分析循环语句"""
        print(f"🔍 分析循环语句")
        
        self.complexity_score += 2
        
        # 分析条件
        while_loop.condition.accept(self)
        
        # 分析循环体
        for stmt in while_loop.body:
            stmt.accept(self)
    
    def visit_literal(self, literal: LiteralNode):
        """分析字面量"""
        print(f"🔍 分析字面量: {literal.value}")
        
        # 检查魔法数字
        if (literal.literal_type == "int" and 
            isinstance(literal.value, int) and 
            literal.value > 100):
            self._add_issue("建议", f"考虑将魔法数字 {literal.value} 定义为常量", literal)
    
    def get_analysis_report(self) -> str:
        """获取分析报告"""
        report = [f"静态分析报告:"]
        report.append(f"复杂度评分: {self.complexity_score}")
        report.append(f"发现问题: {len(self.issues)} 个")
        report.append("")
        
        # 按严重程度分组
        errors = [issue for issue in self.issues if issue["severity"] == "错误"]
        warnings = [issue for issue in self.issues if issue["severity"] == "警告"]
        suggestions = [issue for issue in self.issues if issue["severity"] == "建议"]
        
        if errors:
            report.append("❌ 错误:")
            for issue in errors:
                report.append(f"   行 {issue['line']}: {issue['message']}")
            report.append("")
        
        if warnings:
            report.append("⚠️  警告:")
            for issue in warnings:
                report.append(f"   行 {issue['line']}: {issue['message']}")
            report.append("")
        
        if suggestions:
            report.append("💡 建议:")
            for issue in suggestions:
                report.append(f"   行 {issue['line']}: {issue['message']}")
        
        return "\n".join(report)


class OptimizationVisitor(ASTVisitor):
    """代码优化访问者"""
    
    def __init__(self):
        self.optimizations: List[str] = []
        self.optimization_count = 0
    
    def _add_optimization(self, description: str, node: ASTNode):
        """添加优化"""
        self.optimizations.append(f"行 {node.line}: {description}")
        self.optimization_count += 1
    
    def visit_program(self, program: ProgramNode):
        """优化程序"""
        print(f"⚡ 优化程序: {program.name}")
        
        for func in program.functions:
            func.accept(self)
    
    def visit_function(self, function: FunctionNode):
        """优化函数"""
        print(f"⚡ 优化函数: {function.name}")
        
        for stmt in function.body:
            stmt.accept(self)
    
    def visit_variable(self, variable: VariableNode):
        """优化变量"""
        print(f"⚡ 检查变量: {variable.name}")
    
    def visit_binary_operation(self, binary_op: BinaryOperationNode):
        """优化二元运算"""
        print(f"⚡ 优化二元运算: {binary_op.operator}")
        
        # 常量折叠优化
        if (isinstance(binary_op.left, LiteralNode) and 
            isinstance(binary_op.right, LiteralNode)):
            self._add_optimization(f"常量折叠: {binary_op.left.value} {binary_op.operator} {binary_op.right.value}", binary_op)
        
        # 递归优化操作数
        binary_op.left.accept(self)
        binary_op.right.accept(self)
    
    def visit_assignment(self, assignment: AssignmentNode):
        """优化赋值"""
        print(f"⚡ 检查赋值: {assignment.variable.name}")
        assignment.value.accept(self)
    
    def visit_if_statement(self, if_stmt: IfStatementNode):
        """优化条件语句"""
        print(f"⚡ 优化条件语句")
        
        # 检查空分支
        if not if_stmt.then_branch:
            self._add_optimization("移除空的then分支", if_stmt)
        
        if not if_stmt.else_branch:
            self._add_optimization("移除空的else分支", if_stmt)
        
        # 递归优化
        if_stmt.condition.accept(self)
        for stmt in if_stmt.then_branch:
            stmt.accept(self)
        for stmt in if_stmt.else_branch:
            stmt.accept(self)
    
    def visit_while_loop(self, while_loop: WhileLoopNode):
        """优化循环语句"""
        print(f"⚡ 优化循环语句")
        
        # 检查无限循环
        if (isinstance(while_loop.condition, LiteralNode) and 
            while_loop.condition.value is True):
            self._add_optimization("检测到无限循环", while_loop)
        
        # 递归优化
        while_loop.condition.accept(self)
        for stmt in while_loop.body:
            stmt.accept(self)
    
    def visit_literal(self, literal: LiteralNode):
        """优化字面量"""
        print(f"⚡ 检查字面量: {literal.value}")
    
    def get_optimization_report(self) -> str:
        """获取优化报告"""
        report = [f"代码优化报告:"]
        report.append(f"发现优化机会: {self.optimization_count} 个")
        report.append("")
        
        if self.optimizations:
            report.append("⚡ 优化建议:")
            for opt in self.optimizations:
                report.append(f"   {opt}")
        else:
            report.append("✅ 代码已经很好优化了！")
        
        return "\n".join(report)


# ==================== 演示函数 ====================
def create_sample_ast() -> ProgramNode:
    """创建示例AST"""
    print("🏗️  创建示例抽象语法树...")
    
    # 创建程序节点
    program = ProgramNode("示例程序")
    
    # 创建全局变量
    global_var = VariableNode("GLOBAL_CONSTANT", "int", 1)
    program.add_global_variable(global_var)
    
    # 创建主函数
    main_func = FunctionNode("main", "int", 3)
    
    # 添加参数
    param1 = VariableNode("argc", "int", 3)
    param2 = VariableNode("argv", "str[]", 3)
    main_func.add_parameter(param1)
    main_func.add_parameter(param2)
    
    # 创建函数体
    # 变量声明
    var_x = VariableNode("x", "int", 4)
    var_y = VariableNode("y", "int", 5)
    
    # 赋值语句
    literal_10 = LiteralNode(10, "int", 6)
    literal_20 = LiteralNode(20, "int", 7)
    assignment1 = AssignmentNode(var_x, literal_10, 6)
    assignment2 = AssignmentNode(var_y, literal_20, 7)
    
    # 二元运算
    binary_op = BinaryOperationNode("+", var_x, var_y, 8)
    var_sum = VariableNode("sum", "int", 8)
    assignment3 = AssignmentNode(var_sum, binary_op, 8)
    
    # 条件语句
    condition = BinaryOperationNode(">", var_sum, LiteralNode(25, "int", 9), 9)
    then_branch = [AssignmentNode(var_x, LiteralNode(100, "int", 10), 10)]
    else_branch = [AssignmentNode(var_x, LiteralNode(0, "int", 12), 12)]
    if_stmt = IfStatementNode(condition, then_branch, else_branch, 9)
    
    # 循环语句
    loop_condition = BinaryOperationNode("<", var_x, LiteralNode(5, "int", 14), 14)
    loop_body = [
        BinaryOperationNode("+", var_x, LiteralNode(1, "int", 15), 15)
    ]
    while_loop = WhileLoopNode(loop_condition, loop_body, 14)
    
    # 添加语句到函数
    main_func.add_statement(assignment1)
    main_func.add_statement(assignment2)
    main_func.add_statement(assignment3)
    main_func.add_statement(if_stmt)
    main_func.add_statement(while_loop)
    
    # 添加函数到程序
    program.add_function(main_func)
    
    print(f"✅ AST创建完成: {program}")
    return program


def demo_ast_processor():
    """AST处理器演示"""
    print("=" * 80)
    print("🌳 抽象语法树处理访问者演示")
    print("=" * 80)
    
    # 创建示例AST
    ast = create_sample_ast()
    
    # 创建不同的访问者
    visitors = [
        ("代码生成器", CodeGeneratorVisitor("Python")),
        ("静态分析器", StaticAnalyzerVisitor()),
        ("优化器", OptimizationVisitor())
    ]
    
    # 使用不同访问者处理AST
    for name, visitor in visitors:
        print(f"\n{'='*20} {name} {'='*20}")
        
        ast.accept(visitor)
        
        # 显示处理结果
        if isinstance(visitor, CodeGeneratorVisitor):
            print(f"\n📝 生成的代码:")
            print("-" * 40)
            print(visitor.get_generated_code())
        
        elif isinstance(visitor, StaticAnalyzerVisitor):
            print(f"\n📊 分析报告:")
            print("-" * 40)
            print(visitor.get_analysis_report())
        
        elif isinstance(visitor, OptimizationVisitor):
            print(f"\n⚡ 优化报告:")
            print("-" * 40)
            print(visitor.get_optimization_report())
    
    print("\n" + "=" * 80)
    print("🎉 AST处理访问者演示完成!")
    print("💡 关键点:")
    print("   - 访问者模式非常适合编译器设计")
    print("   - 可以轻松添加新的分析和优化pass")
    print("   - AST结构保持稳定，操作可以灵活扩展")
    print("=" * 80)


if __name__ == "__main__":
    demo_ast_processor()
