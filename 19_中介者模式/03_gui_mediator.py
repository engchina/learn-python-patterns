#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI界面中介者模式

本模块演示了中介者模式在GUI界面中的应用，包括：
1. 表单组件间的交互
2. 动态UI状态管理
3. 事件处理和响应
4. 复杂表单逻辑管理

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import re


class ComponentType(Enum):
    """组件类型枚举"""
    BUTTON = "按钮"
    TEXT_INPUT = "文本输入框"
    CHECKBOX = "复选框"
    RADIO_BUTTON = "单选按钮"
    DROPDOWN = "下拉框"
    LABEL = "标签"
    LIST_BOX = "列表框"


class ComponentState(Enum):
    """组件状态枚举"""
    ENABLED = "启用"
    DISABLED = "禁用"
    HIDDEN = "隐藏"
    READONLY = "只读"


class GUIMediator(ABC):
    """GUI中介者接口"""
    
    @abstractmethod
    def notify(self, sender: 'Component', event: str, data: Any = None) -> None:
        """处理组件事件通知"""
        pass
    
    @abstractmethod
    def register_component(self, component: 'Component') -> None:
        """注册组件"""
        pass


class Component(ABC):
    """GUI组件基类"""
    
    def __init__(self, component_id: str, component_type: ComponentType, mediator: GUIMediator = None):
        self.component_id = component_id
        self.component_type = component_type
        self.mediator = mediator
        self.state = ComponentState.ENABLED
        self.visible = True
        
        if mediator:
            mediator.register_component(self)
    
    def set_mediator(self, mediator: GUIMediator) -> None:
        """设置中介者"""
        self.mediator = mediator
        mediator.register_component(self)
    
    def notify_mediator(self, event: str, data: Any = None) -> None:
        """通知中介者"""
        if self.mediator:
            self.mediator.notify(self, event, data)
    
    def set_state(self, state: ComponentState) -> None:
        """设置组件状态"""
        old_state = self.state
        self.state = state
        print(f"🔧 {self.component_id} 状态: {old_state.value} -> {state.value}")
    
    def set_visible(self, visible: bool) -> None:
        """设置组件可见性"""
        self.visible = visible
        status = "显示" if visible else "隐藏"
        print(f"👁️ {self.component_id} {status}")
    
    @abstractmethod
    def get_value(self) -> Any:
        """获取组件值"""
        pass
    
    @abstractmethod
    def set_value(self, value: Any) -> None:
        """设置组件值"""
        pass


class Button(Component):
    """按钮组件"""
    
    def __init__(self, component_id: str, text: str, mediator: GUIMediator = None):
        super().__init__(component_id, ComponentType.BUTTON, mediator)
        self.text = text
        self.click_handler: Optional[Callable] = None
    
    def click(self) -> None:
        """点击按钮"""
        if self.state == ComponentState.ENABLED and self.visible:
            print(f"🖱️ 点击按钮: {self.text}")
            self.notify_mediator("click", {"button_id": self.component_id})
            
            if self.click_handler:
                self.click_handler()
    
    def set_click_handler(self, handler: Callable) -> None:
        """设置点击处理器"""
        self.click_handler = handler
    
    def get_value(self) -> str:
        return self.text
    
    def set_value(self, value: str) -> None:
        self.text = value
        print(f"📝 {self.component_id} 文本设置为: {value}")


class TextInput(Component):
    """文本输入框组件"""
    
    def __init__(self, component_id: str, placeholder: str = "", mediator: GUIMediator = None):
        super().__init__(component_id, ComponentType.TEXT_INPUT, mediator)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = None
        self.validation_pattern = None
    
    def set_text(self, text: str) -> None:
        """设置文本"""
        if self.state == ComponentState.READONLY:
            print(f"⚠️ {self.component_id} 为只读状态，无法修改")
            return
        
        # 长度验证
        if self.max_length and len(text) > self.max_length:
            print(f"⚠️ {self.component_id} 文本长度超过限制 ({self.max_length})")
            return
        
        # 格式验证
        if self.validation_pattern and not re.match(self.validation_pattern, text):
            print(f"⚠️ {self.component_id} 文本格式不正确")
            self.notify_mediator("validation_failed", {"text": text})
            return
        
        old_text = self.text
        self.text = text
        print(f"📝 {self.component_id} 文本: '{old_text}' -> '{text}'")
        self.notify_mediator("text_changed", {"old_text": old_text, "new_text": text})
    
    def set_validation(self, pattern: str) -> None:
        """设置验证模式"""
        self.validation_pattern = pattern
    
    def set_max_length(self, max_length: int) -> None:
        """设置最大长度"""
        self.max_length = max_length
    
    def get_value(self) -> str:
        return self.text
    
    def set_value(self, value: str) -> None:
        self.set_text(value)
    
    def is_valid(self) -> bool:
        """检查文本是否有效"""
        if self.validation_pattern:
            return bool(re.match(self.validation_pattern, self.text))
        return True


class CheckBox(Component):
    """复选框组件"""
    
    def __init__(self, component_id: str, label: str, mediator: GUIMediator = None):
        super().__init__(component_id, ComponentType.CHECKBOX, mediator)
        self.label = label
        self.checked = False
    
    def toggle(self) -> None:
        """切换选中状态"""
        if self.state == ComponentState.ENABLED and self.visible:
            self.checked = not self.checked
            status = "选中" if self.checked else "取消选中"
            print(f"☑️ {self.component_id} ({self.label}) {status}")
            self.notify_mediator("toggled", {"checked": self.checked})
    
    def set_checked(self, checked: bool) -> None:
        """设置选中状态"""
        if self.checked != checked:
            self.checked = checked
            status = "选中" if checked else "取消选中"
            print(f"☑️ {self.component_id} ({self.label}) {status}")
            self.notify_mediator("toggled", {"checked": self.checked})
    
    def get_value(self) -> bool:
        return self.checked
    
    def set_value(self, value: bool) -> None:
        self.set_checked(value)


class DropDown(Component):
    """下拉框组件"""
    
    def __init__(self, component_id: str, options: List[str], mediator: GUIMediator = None):
        super().__init__(component_id, ComponentType.DROPDOWN, mediator)
        self.options = options
        self.selected_index = -1
        self.selected_value = ""
    
    def select_option(self, index: int) -> None:
        """选择选项"""
        if self.state != ComponentState.ENABLED or not self.visible:
            return
        
        if 0 <= index < len(self.options):
            old_value = self.selected_value
            self.selected_index = index
            self.selected_value = self.options[index]
            print(f"📋 {self.component_id} 选择: {self.selected_value}")
            self.notify_mediator("selection_changed", {
                "old_value": old_value,
                "new_value": self.selected_value,
                "index": index
            })
    
    def add_option(self, option: str) -> None:
        """添加选项"""
        self.options.append(option)
        print(f"➕ {self.component_id} 添加选项: {option}")
    
    def get_value(self) -> str:
        return self.selected_value
    
    def set_value(self, value: str) -> None:
        if value in self.options:
            index = self.options.index(value)
            self.select_option(index)


class UserRegistrationForm(GUIMediator):
    """用户注册表单中介者"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self._setup_form()
    
    def _setup_form(self) -> None:
        """设置表单组件"""
        # 用户名输入
        self.username_input = TextInput("username", "请输入用户名", self)
        self.username_input.set_validation(r"^[a-zA-Z0-9_]{3,20}$")
        self.username_input.set_max_length(20)
        
        # 邮箱输入
        self.email_input = TextInput("email", "请输入邮箱", self)
        self.email_input.set_validation(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        
        # 密码输入
        self.password_input = TextInput("password", "请输入密码", self)
        self.password_input.set_validation(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$")
        
        # 确认密码输入
        self.confirm_password_input = TextInput("confirm_password", "请确认密码", self)
        
        # 年龄下拉框
        age_options = [str(i) for i in range(18, 101)]
        self.age_dropdown = DropDown("age", age_options, self)
        
        # 同意条款复选框
        self.terms_checkbox = CheckBox("terms", "我同意用户协议", self)
        
        # 接收邮件复选框
        self.newsletter_checkbox = CheckBox("newsletter", "接收产品更新邮件", self)
        
        # 提交按钮
        self.submit_button = Button("submit", "注册", self)
        self.submit_button.set_state(ComponentState.DISABLED)  # 初始禁用
        
        # 重置按钮
        self.reset_button = Button("reset", "重置", self)
        
        print("📋 用户注册表单已初始化")
    
    def register_component(self, component: Component) -> None:
        """注册组件"""
        self.components[component.component_id] = component
    
    def notify(self, sender: Component, event: str, data: Any = None) -> None:
        """处理组件事件"""
        print(f"🔔 表单中介者收到事件: {sender.component_id} -> {event}")
        
        if sender == self.username_input:
            self._handle_username_change(event, data)
        elif sender == self.email_input:
            self._handle_email_change(event, data)
        elif sender == self.password_input:
            self._handle_password_change(event, data)
        elif sender == self.confirm_password_input:
            self._handle_confirm_password_change(event, data)
        elif sender == self.age_dropdown:
            self._handle_age_change(event, data)
        elif sender == self.terms_checkbox:
            self._handle_terms_change(event, data)
        elif sender == self.submit_button and event == "click":
            self._handle_submit()
        elif sender == self.reset_button and event == "click":
            self._handle_reset()
        
        # 每次事件后更新表单状态
        self._update_form_state()
    
    def _handle_username_change(self, event: str, data: Dict) -> None:
        """处理用户名变化"""
        if event == "text_changed":
            username = data["new_text"]
            if len(username) >= 3:
                print("✅ 用户名长度符合要求")
            else:
                print("⚠️ 用户名至少需要3个字符")
        elif event == "validation_failed":
            print("❌ 用户名格式不正确（只能包含字母、数字和下划线）")
    
    def _handle_email_change(self, event: str, data: Dict) -> None:
        """处理邮箱变化"""
        if event == "validation_failed":
            print("❌ 邮箱格式不正确")
    
    def _handle_password_change(self, event: str, data: Dict) -> None:
        """处理密码变化"""
        if event == "text_changed":
            password = data["new_text"]
            if len(password) >= 8:
                print("✅ 密码长度符合要求")
                # 检查确认密码是否匹配
                if self.confirm_password_input.get_value():
                    self._check_password_match()
            else:
                print("⚠️ 密码至少需要8个字符")
        elif event == "validation_failed":
            print("❌ 密码必须包含大小写字母和数字")
    
    def _handle_confirm_password_change(self, event: str, data: Dict) -> None:
        """处理确认密码变化"""
        if event == "text_changed":
            self._check_password_match()
    
    def _check_password_match(self) -> None:
        """检查密码匹配"""
        password = self.password_input.get_value()
        confirm_password = self.confirm_password_input.get_value()
        
        if password and confirm_password:
            if password == confirm_password:
                print("✅ 密码匹配")
            else:
                print("❌ 两次输入的密码不一致")
    
    def _handle_age_change(self, event: str, data: Dict) -> None:
        """处理年龄变化"""
        if event == "selection_changed":
            age = int(data["new_value"])
            if age < 18:
                print("⚠️ 年龄必须满18岁")
                # 可以在这里添加额外的验证逻辑
    
    def _handle_terms_change(self, event: str, data: Dict) -> None:
        """处理条款同意变化"""
        if event == "toggled":
            if data["checked"]:
                print("✅ 已同意用户协议")
            else:
                print("⚠️ 必须同意用户协议才能注册")
    
    def _handle_submit(self) -> None:
        """处理提交"""
        if self._validate_form():
            print("🎉 注册成功！")
            self._show_registration_summary()
        else:
            print("❌ 表单验证失败，请检查输入")
    
    def _handle_reset(self) -> None:
        """处理重置"""
        print("🔄 重置表单")
        self.username_input.set_value("")
        self.email_input.set_value("")
        self.password_input.set_value("")
        self.confirm_password_input.set_value("")
        self.age_dropdown.selected_index = -1
        self.age_dropdown.selected_value = ""
        self.terms_checkbox.set_checked(False)
        self.newsletter_checkbox.set_checked(False)
    
    def _validate_form(self) -> bool:
        """验证表单"""
        # 检查必填字段
        if not self.username_input.get_value():
            print("❌ 用户名不能为空")
            return False
        
        if not self.email_input.get_value():
            print("❌ 邮箱不能为空")
            return False
        
        if not self.password_input.get_value():
            print("❌ 密码不能为空")
            return False
        
        # 检查格式验证
        if not self.username_input.is_valid():
            print("❌ 用户名格式不正确")
            return False
        
        if not self.email_input.is_valid():
            print("❌ 邮箱格式不正确")
            return False
        
        if not self.password_input.is_valid():
            print("❌ 密码格式不正确")
            return False
        
        # 检查密码匹配
        if self.password_input.get_value() != self.confirm_password_input.get_value():
            print("❌ 两次输入的密码不一致")
            return False
        
        # 检查年龄
        if not self.age_dropdown.get_value():
            print("❌ 请选择年龄")
            return False
        
        # 检查条款同意
        if not self.terms_checkbox.get_value():
            print("❌ 必须同意用户协议")
            return False
        
        return True
    
    def _update_form_state(self) -> None:
        """更新表单状态"""
        # 检查是否可以启用提交按钮
        can_submit = (
            self.username_input.get_value() and
            self.email_input.get_value() and
            self.password_input.get_value() and
            self.confirm_password_input.get_value() and
            self.age_dropdown.get_value() and
            self.terms_checkbox.get_value() and
            self.username_input.is_valid() and
            self.email_input.is_valid() and
            self.password_input.is_valid() and
            self.password_input.get_value() == self.confirm_password_input.get_value()
        )
        
        if can_submit:
            self.submit_button.set_state(ComponentState.ENABLED)
        else:
            self.submit_button.set_state(ComponentState.DISABLED)
    
    def _show_registration_summary(self) -> None:
        """显示注册摘要"""
        print("\n📊 注册信息摘要:")
        print(f"  用户名: {self.username_input.get_value()}")
        print(f"  邮箱: {self.email_input.get_value()}")
        print(f"  年龄: {self.age_dropdown.get_value()}")
        print(f"  接收邮件: {'是' if self.newsletter_checkbox.get_value() else '否'}")


def demo_gui_mediator():
    """演示GUI中介者"""
    print("=" * 50)
    print("🖥️ GUI界面中介者演示")
    print("=" * 50)
    
    # 创建注册表单
    form = UserRegistrationForm()
    
    print("\n📝 开始填写表单:")
    
    # 模拟用户输入
    print("\n1. 输入用户名:")
    form.username_input.set_text("john_doe")
    
    print("\n2. 输入邮箱:")
    form.email_input.set_text("john.doe@example.com")
    
    print("\n3. 输入密码:")
    form.password_input.set_text("Password123")
    
    print("\n4. 确认密码:")
    form.confirm_password_input.set_text("Password123")
    
    print("\n5. 选择年龄:")
    form.age_dropdown.select_option(7)  # 25岁
    
    print("\n6. 同意条款:")
    form.terms_checkbox.toggle()
    
    print("\n7. 选择接收邮件:")
    form.newsletter_checkbox.toggle()
    
    print("\n8. 尝试提交:")
    form.submit_button.click()
    
    print("\n9. 演示验证失败:")
    form.reset_button.click()
    form.username_input.set_text("ab")  # 太短
    form.email_input.set_text("invalid-email")  # 格式错误
    form.submit_button.click()


if __name__ == "__main__":
    print("🎯 GUI界面中介者模式演示")
    
    demo_gui_mediator()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 中介者模式简化了GUI组件间的复杂交互逻辑")
    print("=" * 50)
