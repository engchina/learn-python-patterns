#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
树形结构的迭代器

本模块演示了树形结构的不同遍历方式，包括：
1. 深度优先遍历迭代器 - 使用栈实现
2. 广度优先遍历迭代器 - 使用队列实现
3. 文件系统遍历示例 - 实际应用场景
4. 表达式树遍历 - 数学表达式的解析

作者: Assistant
日期: 2024-01-20
"""

import os
from collections import deque
from typing import Any, List


class TreeNode:
    """通用树节点"""

    def __init__(self, value: Any, children: List['TreeNode'] = None):
        self.value = value
        self.children = children or []
        self.parent = None

        # 设置子节点的父节点引用
        for child in self.children:
            child.parent = self

    def add_child(self, child: 'TreeNode') -> None:
        """添加子节点"""
        child.parent = self
        self.children.append(child)
        print(f"🌳 添加子节点: {child.value} -> {self.value}")

    def remove_child(self, child: 'TreeNode') -> bool:
        """移除子节点"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            print(f"🗑️ 移除子节点: {child.value}")
            return True
        return False

    def is_leaf(self) -> bool:
        """判断是否为叶子节点"""
        return len(self.children) == 0

    def get_depth(self) -> int:
        """获取节点深度"""
        depth = 0
        current = self.parent
        while current:
            depth += 1
            current = current.parent
        return depth

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"TreeNode({self.value})"


class DepthFirstIterator:
    """深度优先遍历迭代器"""

    def __init__(self, root: TreeNode, pre_order: bool = True):
        self.root = root
        self.pre_order = pre_order  # True: 前序, False: 后序
        self.stack = []
        self.visited = set()
        self.node_count = 0

    def __iter__(self) -> 'DepthFirstIterator':
        """重置迭代器状态"""
        self.stack = [self.root] if self.root else []
        self.visited = set()
        self.node_count = 0
        return self

    def __next__(self) -> TreeNode:
        """返回下一个节点"""
        if self.pre_order:
            return self._next_preorder()
        else:
            return self._next_postorder()

    def _next_preorder(self) -> TreeNode:
        """前序遍历：根 -> 左 -> 右"""
        if not self.stack:
            print(f"🔍 深度优先遍历完成，共访问 {self.node_count} 个节点")
            raise StopIteration

        node = self.stack.pop()
        self.node_count += 1

        # 逆序添加子节点，保证从左到右的遍历顺序
        for child in reversed(node.children):
            self.stack.append(child)

        return node

    def _next_postorder(self) -> TreeNode:
        """后序遍历：左 -> 右 -> 根"""
        while self.stack:
            node = self.stack[-1]

            # 如果节点未访问过，添加其子节点到栈中
            if node not in self.visited:
                self.visited.add(node)
                # 逆序添加子节点
                for child in reversed(node.children):
                    if child not in self.visited:
                        self.stack.append(child)
            else:
                # 节点已访问过，可以输出
                self.stack.pop()
                self.node_count += 1
                return node

        print(f"🔍 深度优先后序遍历完成，共访问 {self.node_count} 个节点")
        raise StopIteration


class BreadthFirstIterator:
    """广度优先遍历迭代器"""

    def __init__(self, root: TreeNode):
        self.root = root
        self.queue = deque()
        self.node_count = 0
        self.level_count = 0

    def __iter__(self) -> 'BreadthFirstIterator':
        """重置迭代器状态"""
        self.queue = deque([(self.root, 0)] if self.root else [])
        self.node_count = 0
        self.level_count = 0
        return self

    def __next__(self) -> tuple[TreeNode, int]:
        """返回下一个节点和其层级"""
        if not self.queue:
            print(f"🔍 广度优先遍历完成，共访问 {self.node_count} 个节点，{self.level_count + 1} 层")
            raise StopIteration

        node, level = self.queue.popleft()
        self.node_count += 1
        self.level_count = max(self.level_count, level)

        # 添加子节点到队列
        for child in node.children:
            self.queue.append((child, level + 1))

        return node, level


class FileSystemIterator:
    """文件系统遍历迭代器"""

    def __init__(self, root_path: str, max_depth: int = None):
        self.root_path = root_path
        self.max_depth = max_depth
        self.stack = []
        self.file_count = 0
        self.dir_count = 0

    def __iter__(self) -> 'FileSystemIterator':
        """重置迭代器状态"""
        if os.path.exists(self.root_path):
            self.stack = [(self.root_path, 0)]
        else:
            self.stack = []
        self.file_count = 0
        self.dir_count = 0
        return self

    def __next__(self) -> dict:
        """返回下一个文件或目录信息"""
        while self.stack:
            current_path, depth = self.stack.pop()

            # 检查深度限制
            if self.max_depth is not None and depth > self.max_depth:
                continue

            try:
                is_dir = os.path.isdir(current_path)
                file_info = {
                    'path': current_path,
                    'name': os.path.basename(current_path),
                    'is_directory': is_dir,
                    'depth': depth,
                    'size': 0 if is_dir else os.path.getsize(current_path)
                }

                if is_dir:
                    self.dir_count += 1
                    # 添加子目录和文件到栈中
                    try:
                        for item in reversed(sorted(os.listdir(current_path))):
                            item_path = os.path.join(current_path, item)
                            self.stack.append((item_path, depth + 1))
                    except PermissionError:
                        file_info['error'] = '权限不足'
                else:
                    self.file_count += 1

                return file_info

            except (OSError, PermissionError) as e:
                # 跳过无法访问的文件
                continue

        print(f"📁 文件系统遍历完成: {self.dir_count} 个目录, {self.file_count} 个文件")
        raise StopIteration


class ExpressionNode:
    """表达式树节点"""

    def __init__(self, value: str, left: 'ExpressionNode' = None, right: 'ExpressionNode' = None):
        self.value = value
        self.left = left
        self.right = right

    def is_operator(self) -> bool:
        """判断是否为操作符"""
        return self.value in ['+', '-', '*', '/', '(', ')']

    def is_number(self) -> bool:
        """判断是否为数字"""
        try:
            float(self.value)
            return True
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.value


class ExpressionTreeIterator:
    """表达式树遍历迭代器"""

    def __init__(self, root: ExpressionNode, traversal_type: str = 'infix'):
        self.root = root
        self.traversal_type = traversal_type  # 'infix', 'prefix', 'postfix'
        self.result = []
        self.node_count = 0

    def __iter__(self) -> 'ExpressionTreeIterator':
        """重置迭代器状态"""
        self.result = []
        self.node_count = 0
        self._traverse(self.root)
        self.index = 0
        return self

    def __next__(self) -> str:
        """返回下一个表达式元素"""
        if self.index >= len(self.result):
            print(f"🧮 表达式遍历完成，共 {self.node_count} 个节点")
            raise StopIteration

        value = self.result[self.index]
        self.index += 1
        return value

    def _traverse(self, node: ExpressionNode) -> None:
        """根据遍历类型进行遍历"""
        if not node:
            return

        self.node_count += 1

        if self.traversal_type == 'prefix':
            # 前缀表达式：根 -> 左 -> 右
            self.result.append(node.value)
            self._traverse(node.left)
            self._traverse(node.right)
        elif self.traversal_type == 'infix':
            # 中缀表达式：左 -> 根 -> 右
            if node.left:
                self.result.append('(')
            self._traverse(node.left)
            self.result.append(node.value)
            self._traverse(node.right)
            if node.right:
                self.result.append(')')
        elif self.traversal_type == 'postfix':
            # 后缀表达式：左 -> 右 -> 根
            self._traverse(node.left)
            self._traverse(node.right)
            self.result.append(node.value)


def create_sample_tree() -> TreeNode:
    """创建示例树结构"""
    # 创建一个组织架构树
    root = TreeNode("CEO")

    # 第二层
    cto = TreeNode("CTO")
    cfo = TreeNode("CFO")
    cmo = TreeNode("CMO")

    root.add_child(cto)
    root.add_child(cfo)
    root.add_child(cmo)

    # 第三层 - CTO下属
    dev_manager = TreeNode("开发经理")
    qa_manager = TreeNode("测试经理")
    cto.add_child(dev_manager)
    cto.add_child(qa_manager)

    # 第三层 - CFO下属
    accountant = TreeNode("会计")
    auditor = TreeNode("审计")
    cfo.add_child(accountant)
    cfo.add_child(auditor)

    # 第四层 - 开发团队
    frontend_dev = TreeNode("前端开发")
    backend_dev = TreeNode("后端开发")
    dev_manager.add_child(frontend_dev)
    dev_manager.add_child(backend_dev)

    return root


def create_expression_tree() -> ExpressionNode:
    """创建表达式树: (3 + 4) * (2 - 1)"""
    # 构建表达式树
    #       *
    #      / \
    #     +   -
    #    / \ / \
    #   3  4 2  1

    multiply = ExpressionNode("*")
    plus = ExpressionNode("+")
    minus = ExpressionNode("-")

    num3 = ExpressionNode("3")
    num4 = ExpressionNode("4")
    num2 = ExpressionNode("2")
    num1 = ExpressionNode("1")

    plus.left = num3
    plus.right = num4
    minus.left = num2
    minus.right = num1

    multiply.left = plus
    multiply.right = minus

    return multiply


def demo_depth_first_traversal():
    """演示深度优先遍历"""
    print("=" * 50)
    print("🌳 深度优先遍历演示")
    print("=" * 50)

    tree = create_sample_tree()

    # 前序遍历
    print("前序遍历 (根->左->右):")
    dfs_pre = DepthFirstIterator(tree, pre_order=True)
    for node in dfs_pre:
        depth = node.get_depth()
        indent = "  " * depth
        print(f"{indent}├─ {node.value} (深度: {depth})")

    # 后序遍历
    print("\n后序遍历 (左->右->根):")
    dfs_post = DepthFirstIterator(tree, pre_order=False)
    for node in dfs_post:
        depth = node.get_depth()
        indent = "  " * depth
        print(f"{indent}├─ {node.value} (深度: {depth})")


def demo_breadth_first_traversal():
    """演示广度优先遍历"""
    print("\n" + "=" * 50)
    print("🌊 广度优先遍历演示")
    print("=" * 50)

    tree = create_sample_tree()

    print("按层级遍历:")
    bfs = BreadthFirstIterator(tree)
    current_level = -1

    for node, level in bfs:
        if level != current_level:
            current_level = level
            print(f"\n第 {level + 1} 层:")
        print(f"  ├─ {node.value}")


def demo_file_system_traversal():
    """演示文件系统遍历"""
    print("\n" + "=" * 50)
    print("📁 文件系统遍历演示")
    print("=" * 50)

    # 遍历当前目录的Iterator文件夹
    current_dir = "23. Iterator"

    if os.path.exists(current_dir):
        print(f"遍历目录: {current_dir}")
        fs_iter = FileSystemIterator(current_dir, max_depth=2)

        for item in fs_iter:
            depth = item['depth']
            indent = "  " * depth
            icon = "📁" if item['is_directory'] else "📄"
            size_info = f" ({item['size']} bytes)" if not item['is_directory'] else ""

            print(f"{indent}{icon} {item['name']}{size_info}")

            # 限制输出数量
            if fs_iter.file_count + fs_iter.dir_count > 10:
                print(f"{indent}... (省略更多文件)")
                break
    else:
        print(f"目录不存在: {current_dir}")


def demo_expression_tree():
    """演示表达式树遍历"""
    print("\n" + "=" * 50)
    print("🧮 表达式树遍历演示")
    print("=" * 50)

    expr_tree = create_expression_tree()
    print("表达式树: (3 + 4) * (2 - 1)")

    # 中缀表达式
    print("\n中缀表达式:")
    infix_iter = ExpressionTreeIterator(expr_tree, 'infix')
    infix_result = ' '.join(infix_iter)
    print(f"  {infix_result}")

    # 前缀表达式
    print("\n前缀表达式:")
    prefix_iter = ExpressionTreeIterator(expr_tree, 'prefix')
    prefix_result = ' '.join(prefix_iter)
    print(f"  {prefix_result}")

    # 后缀表达式
    print("\n后缀表达式:")
    postfix_iter = ExpressionTreeIterator(expr_tree, 'postfix')
    postfix_result = ' '.join(postfix_iter)
    print(f"  {postfix_result}")


if __name__ == "__main__":
    print("🎯 树形结构迭代器演示")

    # 运行所有演示
    demo_depth_first_traversal()
    demo_breadth_first_traversal()
    demo_file_system_traversal()
    demo_expression_tree()

    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 不同的遍历方式适用于不同的应用场景")
    print("=" * 50)
