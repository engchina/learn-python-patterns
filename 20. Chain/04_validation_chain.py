"""
04_validation_chain.py - 数据验证链示例

这个示例展示了责任链模式在数据验证中的应用。
包括多层数据验证、表单验证处理链和错误收集报告机制。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
import re
from datetime import datetime, date
from enum import Enum


class ValidationResult:
    """验证结果"""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validator_chain: List[str] = []
    
    def add_error(self, message: str):
        """添加错误"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """添加警告"""
        self.warnings.append(message)
    
    def add_validator_record(self, validator_name: str):
        """添加验证器记录"""
        self.validator_chain.append(validator_name)
    
    def merge(self, other: 'ValidationResult'):
        """合并其他验证结果"""
        if not other.is_valid:
            self.is_valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.validator_chain.extend(other.validator_chain)
    
    def get_summary(self) -> Dict[str, Any]:
        """获取验证摘要"""
        return {
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "validator_chain": self.validator_chain
        }


# ==================== 抽象验证器 ====================
class Validator(ABC):
    """抽象验证器"""
    
    def __init__(self, name: str, required: bool = True):
        self.name = name
        self.required = required
        self._next_validator: Optional['Validator'] = None
        self.validation_count = 0
        self.error_count = 0
    
    def set_next(self, validator: 'Validator') -> 'Validator':
        """设置下一个验证器"""
        self._next_validator = validator
        return validator
    
    def validate(self, field_name: str, value: Any, context: Dict[str, Any] = None) -> ValidationResult:
        """验证数据"""
        result = ValidationResult()
        result.add_validator_record(self.name)
        
        self.validation_count += 1
        context = context or {}
        
        # 检查必填项
        if self.required and (value is None or value == ""):
            result.add_error(f"{field_name} 是必填项")
            self.error_count += 1
            print(f"{self.name}: {field_name} 验证失败 - 必填项为空")
        else:
            # 执行具体验证逻辑
            validation_result = self._validate_value(field_name, value, context)
            result.merge(validation_result)
            
            if not validation_result.is_valid:
                self.error_count += 1
                print(f"{self.name}: {field_name} 验证失败")
            else:
                print(f"{self.name}: {field_name} 验证通过")
        
        # 传递给下一个验证器
        if self._next_validator:
            next_result = self._next_validator.validate(field_name, value, context)
            result.merge(next_result)
        
        return result
    
    @abstractmethod
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """具体的验证逻辑"""
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取验证统计"""
        success_rate = ((self.validation_count - self.error_count) / self.validation_count * 100) if self.validation_count > 0 else 0
        return {
            "name": self.name,
            "validation_count": self.validation_count,
            "error_count": self.error_count,
            "success_rate": round(success_rate, 1)
        }


# ==================== 具体验证器实现 ====================
class TypeValidator(Validator):
    """类型验证器"""
    
    def __init__(self, expected_type: type, required: bool = True):
        super().__init__(f"类型验证器({expected_type.__name__})", required)
        self.expected_type = expected_type
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证数据类型"""
        result = ValidationResult()
        
        if value is not None and not isinstance(value, self.expected_type):
            result.add_error(f"{field_name} 必须是 {self.expected_type.__name__} 类型，当前是 {type(value).__name__}")
        
        return result


class LengthValidator(Validator):
    """长度验证器"""
    
    def __init__(self, min_length: int = None, max_length: int = None, required: bool = True):
        super().__init__("长度验证器", required)
        self.min_length = min_length
        self.max_length = max_length
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证长度"""
        result = ValidationResult()
        
        if value is None:
            return result
        
        try:
            length = len(value)
            
            if self.min_length is not None and length < self.min_length:
                result.add_error(f"{field_name} 长度不能少于 {self.min_length} 个字符，当前 {length} 个字符")
            
            if self.max_length is not None and length > self.max_length:
                result.add_error(f"{field_name} 长度不能超过 {self.max_length} 个字符，当前 {length} 个字符")
            
            # 添加警告
            if self.max_length and length > self.max_length * 0.8:
                result.add_warning(f"{field_name} 长度接近上限")
                
        except TypeError:
            result.add_error(f"{field_name} 不支持长度检查")
        
        return result


class RegexValidator(Validator):
    """正则表达式验证器"""
    
    def __init__(self, pattern: str, error_message: str = None, required: bool = True):
        super().__init__("正则验证器", required)
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.error_message = error_message or f"格式不正确，应匹配模式: {pattern}"
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证正则表达式"""
        result = ValidationResult()
        
        if value is None:
            return result
        
        if not isinstance(value, str):
            result.add_error(f"{field_name} 必须是字符串类型才能进行正则验证")
            return result
        
        if not self.regex.match(value):
            result.add_error(f"{field_name} {self.error_message}")
        
        return result


class RangeValidator(Validator):
    """范围验证器"""
    
    def __init__(self, min_value: Union[int, float] = None, 
                 max_value: Union[int, float] = None, required: bool = True):
        super().__init__("范围验证器", required)
        self.min_value = min_value
        self.max_value = max_value
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证数值范围"""
        result = ValidationResult()
        
        if value is None:
            return result
        
        try:
            numeric_value = float(value)
            
            if self.min_value is not None and numeric_value < self.min_value:
                result.add_error(f"{field_name} 不能小于 {self.min_value}，当前值 {numeric_value}")
            
            if self.max_value is not None and numeric_value > self.max_value:
                result.add_error(f"{field_name} 不能大于 {self.max_value}，当前值 {numeric_value}")
            
        except (ValueError, TypeError):
            result.add_error(f"{field_name} 必须是数值类型")
        
        return result


class EmailValidator(Validator):
    """邮箱验证器"""
    
    def __init__(self, required: bool = True):
        super().__init__("邮箱验证器", required)
        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.regex = re.compile(self.email_pattern)
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证邮箱格式"""
        result = ValidationResult()
        
        if value is None:
            return result
        
        if not isinstance(value, str):
            result.add_error(f"{field_name} 必须是字符串类型")
            return result
        
        if not self.regex.match(value):
            result.add_error(f"{field_name} 邮箱格式不正确")
        else:
            # 检查常见的邮箱域名
            domain = value.split('@')[1].lower()
            suspicious_domains = ['test.com', 'example.com', 'temp.com']
            if domain in suspicious_domains:
                result.add_warning(f"{field_name} 使用了测试邮箱域名")
        
        return result


class DateValidator(Validator):
    """日期验证器"""
    
    def __init__(self, min_date: date = None, max_date: date = None, required: bool = True):
        super().__init__("日期验证器", required)
        self.min_date = min_date
        self.max_date = max_date
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """验证日期"""
        result = ValidationResult()
        
        if value is None:
            return result
        
        # 尝试解析日期
        parsed_date = None
        if isinstance(value, str):
            try:
                parsed_date = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                try:
                    parsed_date = datetime.strptime(value, '%Y/%m/%d').date()
                except ValueError:
                    result.add_error(f"{field_name} 日期格式不正确，应为 YYYY-MM-DD 或 YYYY/MM/DD")
                    return result
        elif isinstance(value, (date, datetime)):
            parsed_date = value.date() if isinstance(value, datetime) else value
        else:
            result.add_error(f"{field_name} 必须是日期字符串或日期对象")
            return result
        
        if parsed_date:
            if self.min_date and parsed_date < self.min_date:
                result.add_error(f"{field_name} 不能早于 {self.min_date}")
            
            if self.max_date and parsed_date > self.max_date:
                result.add_error(f"{field_name} 不能晚于 {self.max_date}")
            
            # 检查是否是未来日期
            if parsed_date > date.today():
                result.add_warning(f"{field_name} 是未来日期")
        
        return result


class CustomValidator(Validator):
    """自定义验证器"""
    
    def __init__(self, name: str, validation_func: callable, required: bool = True):
        super().__init__(f"自定义验证器({name})", required)
        self.validation_func = validation_func
    
    def _validate_value(self, field_name: str, value: Any, context: Dict[str, Any]) -> ValidationResult:
        """执行自定义验证"""
        result = ValidationResult()
        
        try:
            is_valid, message = self.validation_func(value, context)
            if not is_valid:
                result.add_error(f"{field_name} {message}")
        except Exception as e:
            result.add_error(f"{field_name} 自定义验证失败: {e}")
        
        return result


# ==================== 表单验证器 ====================
class FormValidator:
    """表单验证器"""
    
    def __init__(self, name: str):
        self.name = name
        self.field_validators: Dict[str, Validator] = {}
        self.validation_count = 0
    
    def add_field_validator(self, field_name: str, validator: Validator):
        """添加字段验证器"""
        self.field_validators[field_name] = validator
        print(f"表单验证器 '{self.name}': 为字段 '{field_name}' 添加验证器")
    
    def validate_form(self, form_data: Dict[str, Any]) -> ValidationResult:
        """验证整个表单"""
        self.validation_count += 1
        overall_result = ValidationResult()
        
        print(f"\n表单验证器 '{self.name}': 开始验证表单")
        
        # 验证每个字段
        for field_name, validator in self.field_validators.items():
            field_value = form_data.get(field_name)
            print(f"\n--- 验证字段: {field_name} ---")
            
            field_result = validator.validate(field_name, field_value, form_data)
            overall_result.merge(field_result)
        
        # 执行表单级别的验证
        form_level_result = self._validate_form_level(form_data)
        overall_result.merge(form_level_result)
        
        print(f"\n表单验证完成: {'通过' if overall_result.is_valid else '失败'}")
        return overall_result
    
    def _validate_form_level(self, form_data: Dict[str, Any]) -> ValidationResult:
        """表单级别的验证（可以被子类重写）"""
        result = ValidationResult()
        result.add_validator_record(f"{self.name}_表单级验证")
        
        # 示例：密码确认验证
        if 'password' in form_data and 'confirm_password' in form_data:
            if form_data['password'] != form_data['confirm_password']:
                result.add_error("密码和确认密码不匹配")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取验证统计"""
        field_stats = {}
        for field_name, validator in self.field_validators.items():
            field_stats[field_name] = self._get_validator_chain_stats(validator)
        
        return {
            "form_name": self.name,
            "validation_count": self.validation_count,
            "field_count": len(self.field_validators),
            "field_statistics": field_stats
        }
    
    def _get_validator_chain_stats(self, validator: Validator) -> List[Dict[str, Any]]:
        """获取验证器链统计"""
        stats = []
        current = validator
        while current:
            stats.append(current.get_statistics())
            current = current._next_validator
        return stats


# ==================== 使用示例 ====================
def demo_validation_chain():
    """验证链演示"""
    print("=" * 60)
    print("✅ 数据验证链演示")
    print("=" * 60)
    
    # 创建用户注册表单验证器
    user_form = FormValidator("用户注册表单")
    
    # 用户名验证链
    username_validator = (TypeValidator(str)
                         .set_next(LengthValidator(min_length=3, max_length=20))
                         .set_next(RegexValidator(r'^[a-zA-Z0-9_]+$', "只能包含字母、数字和下划线")))
    
    # 邮箱验证链
    email_validator = (TypeValidator(str)
                      .set_next(EmailValidator()))
    
    # 年龄验证链
    age_validator = (TypeValidator(int)
                    .set_next(RangeValidator(min_value=18, max_value=120)))
    
    # 密码验证链
    password_validator = (TypeValidator(str)
                         .set_next(LengthValidator(min_length=8, max_length=50))
                         .set_next(RegexValidator(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
                                                "必须包含大小写字母和数字")))
    
    # 生日验证链
    birthday_validator = DateValidator(min_date=date(1900, 1, 1), max_date=date.today())
    
    # 添加字段验证器
    user_form.add_field_validator("username", username_validator)
    user_form.add_field_validator("email", email_validator)
    user_form.add_field_validator("age", age_validator)
    user_form.add_field_validator("password", password_validator)
    user_form.add_field_validator("confirm_password", TypeValidator(str))
    user_form.add_field_validator("birthday", birthday_validator)
    
    # 测试数据
    test_forms = [
        {
            "name": "有效表单",
            "data": {
                "username": "john_doe",
                "email": "john@example.com",
                "age": 25,
                "password": "SecurePass123",
                "confirm_password": "SecurePass123",
                "birthday": "1998-05-15"
            }
        },
        {
            "name": "无效表单1",
            "data": {
                "username": "jo",  # 太短
                "email": "invalid-email",  # 邮箱格式错误
                "age": 15,  # 年龄太小
                "password": "weak",  # 密码太弱
                "confirm_password": "different",  # 密码不匹配
                "birthday": "2030-01-01"  # 未来日期
            }
        },
        {
            "name": "无效表单2",
            "data": {
                "username": "user@with#special!chars",  # 包含特殊字符
                "email": "test@test.com",  # 测试域名
                "age": "not_a_number",  # 类型错误
                "password": "NoNumbers",  # 缺少数字
                "confirm_password": "NoNumbers",
                "birthday": "invalid-date"  # 日期格式错误
            }
        }
    ]
    
    # 验证所有测试表单
    for i, test_form in enumerate(test_forms, 1):
        print(f"\n{'='*20} 测试表单 {i}: {test_form['name']} {'='*20}")
        
        result = user_form.validate_form(test_form["data"])
        summary = result.get_summary()
        
        print(f"\n📋 验证结果摘要:")
        print(f"  验证状态: {'✅ 通过' if summary['is_valid'] else '❌ 失败'}")
        print(f"  错误数量: {summary['error_count']}")
        print(f"  警告数量: {summary['warning_count']}")
        
        if summary['errors']:
            print(f"\n❌ 错误列表:")
            for error in summary['errors']:
                print(f"    • {error}")
        
        if summary['warnings']:
            print(f"\n⚠️ 警告列表:")
            for warning in summary['warnings']:
                print(f"    • {warning}")
        
        print(f"\n🔗 验证器链路: {' -> '.join(summary['validator_chain'])}")
    
    # 显示统计信息
    print(f"\n📊 表单验证统计:")
    stats = user_form.get_statistics()
    print(f"表单名称: {stats['form_name']}")
    print(f"验证次数: {stats['validation_count']}")
    print(f"字段数量: {stats['field_count']}")


def demo_custom_validator():
    """自定义验证器演示"""
    print("\n" + "=" * 60)
    print("🔧 自定义验证器演示")
    print("=" * 60)
    
    # 自定义验证函数
    def validate_phone_number(value, context):
        """验证手机号码"""
        if not isinstance(value, str):
            return False, "必须是字符串"
        
        # 简单的手机号验证
        if not re.match(r'^1[3-9]\d{9}$', value):
            return False, "手机号格式不正确"
        
        return True, ""
    
    def validate_id_card(value, context):
        """验证身份证号"""
        if not isinstance(value, str):
            return False, "必须是字符串"
        
        if len(value) != 18:
            return False, "身份证号必须是18位"
        
        if not re.match(r'^\d{17}[\dXx]$', value):
            return False, "身份证号格式不正确"
        
        return True, ""
    
    # 创建包含自定义验证器的表单
    contact_form = FormValidator("联系信息表单")
    
    # 手机号验证链
    phone_validator = (TypeValidator(str)
                      .set_next(CustomValidator("手机号", validate_phone_number)))
    
    # 身份证验证链
    id_card_validator = CustomValidator("身份证", validate_id_card)
    
    contact_form.add_field_validator("phone", phone_validator)
    contact_form.add_field_validator("id_card", id_card_validator)
    
    # 测试自定义验证
    test_data = [
        {"phone": "13812345678", "id_card": "110101199001011234"},  # 有效数据
        {"phone": "12345678901", "id_card": "12345"},  # 无效数据
        {"phone": 13812345678, "id_card": None}  # 类型错误
    ]
    
    for i, data in enumerate(test_data, 1):
        print(f"\n--- 测试数据 {i} ---")
        result = contact_form.validate_form(data)
        summary = result.get_summary()
        
        print(f"验证结果: {'通过' if summary['is_valid'] else '失败'}")
        if summary['errors']:
            for error in summary['errors']:
                print(f"  错误: {error}")


def main():
    """主演示函数"""
    demo_validation_chain()
    demo_custom_validator()
    
    print("\n" + "=" * 60)
    print("🎉 数据验证链演示完成！")
    print("💡 关键要点:")
    print("   • 验证器链实现了多层数据验证")
    print("   • 每个验证器专注于特定的验证规则")
    print("   • 支持自定义验证逻辑")
    print("   • 可以收集所有验证错误和警告")
    print("   • 广泛应用于表单验证和数据处理")
    print("=" * 60)


if __name__ == "__main__":
    main()
