"""
04_data_processing.py - 数据处理策略系统

这个示例展示了策略模式在数据处理系统中的应用。
演示了数据验证、转换、存储策略的组合使用和异步处理。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, Union
import asyncio
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import hashlib


# ==================== 数据验证策略 ====================

class ValidationStrategy(ABC):
    """数据验证策略抽象类"""
    
    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        """验证数据，返回验证结果"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        pass


class EmailValidationStrategy(ValidationStrategy):
    """邮箱验证策略"""
    
    def validate(self, data: Any) -> Dict[str, Any]:
        """验证邮箱格式"""
        if not isinstance(data, str):
            return {'valid': False, 'error': '数据类型必须是字符串'}
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(email_pattern, data))
        
        result = {'valid': is_valid}
        if not is_valid:
            result['error'] = '邮箱格式不正确'
        else:
            result['normalized'] = data.lower().strip()
        
        return result
    
    def get_strategy_name(self) -> str:
        return "邮箱验证"


class PhoneValidationStrategy(ValidationStrategy):
    """手机号验证策略"""
    
    def validate(self, data: Any) -> Dict[str, Any]:
        """验证手机号格式"""
        if not isinstance(data, str):
            return {'valid': False, 'error': '数据类型必须是字符串'}
        
        # 移除所有非数字字符
        phone_digits = re.sub(r'\D', '', data)
        
        # 中国手机号验证
        if len(phone_digits) == 11 and phone_digits.startswith('1'):
            return {
                'valid': True,
                'normalized': phone_digits,
                'formatted': f"{phone_digits[:3]}-{phone_digits[3:7]}-{phone_digits[7:]}"
            }
        else:
            return {'valid': False, 'error': '手机号格式不正确'}
    
    def get_strategy_name(self) -> str:
        return "手机号验证"


class AgeValidationStrategy(ValidationStrategy):
    """年龄验证策略"""
    
    def __init__(self, min_age: int = 0, max_age: int = 150):
        self.min_age = min_age
        self.max_age = max_age
    
    def validate(self, data: Any) -> Dict[str, Any]:
        """验证年龄范围"""
        try:
            age = int(data)
            if self.min_age <= age <= self.max_age:
                return {'valid': True, 'normalized': age}
            else:
                return {
                    'valid': False,
                    'error': f'年龄必须在{self.min_age}-{self.max_age}之间'
                }
        except (ValueError, TypeError):
            return {'valid': False, 'error': '年龄必须是数字'}
    
    def get_strategy_name(self) -> str:
        return f"年龄验证({self.min_age}-{self.max_age})"


# ==================== 数据转换策略 ====================

class TransformStrategy(ABC):
    """数据转换策略抽象类"""
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """转换数据"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        pass


class UpperCaseTransformStrategy(TransformStrategy):
    """大写转换策略"""
    
    def transform(self, data: Any) -> Any:
        """转换为大写"""
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, dict):
            return {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}
        elif isinstance(data, list):
            return [item.upper() if isinstance(item, str) else item for item in data]
        return data
    
    def get_strategy_name(self) -> str:
        return "大写转换"


class HashTransformStrategy(TransformStrategy):
    """哈希转换策略"""
    
    def __init__(self, algorithm: str = 'md5'):
        self.algorithm = algorithm
    
    def transform(self, data: Any) -> Any:
        """转换为哈希值"""
        if isinstance(data, str):
            hash_obj = hashlib.new(self.algorithm)
            hash_obj.update(data.encode('utf-8'))
            return hash_obj.hexdigest()
        return data
    
    def get_strategy_name(self) -> str:
        return f"{self.algorithm.upper()}哈希转换"


class DateFormatTransformStrategy(TransformStrategy):
    """日期格式转换策略"""
    
    def __init__(self, target_format: str = '%Y-%m-%d'):
        self.target_format = target_format
    
    def transform(self, data: Any) -> Any:
        """转换日期格式"""
        if isinstance(data, str):
            try:
                # 尝试解析常见日期格式
                formats = ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%d-%m-%Y']
                for fmt in formats:
                    try:
                        dt = datetime.strptime(data, fmt)
                        return dt.strftime(self.target_format)
                    except ValueError:
                        continue
                return data  # 如果无法解析，返回原数据
            except Exception:
                return data
        elif isinstance(data, datetime):
            return data.strftime(self.target_format)
        return data
    
    def get_strategy_name(self) -> str:
        return f"日期格式转换({self.target_format})"


# ==================== 数据存储策略 ====================

class StorageStrategy(ABC):
    """数据存储策略抽象类"""
    
    @abstractmethod
    async def save(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存数据"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        pass


class JSONStorageStrategy(StorageStrategy):
    """JSON存储策略"""
    
    async def save(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存为JSON格式"""
        try:
            # 模拟异步IO操作
            await asyncio.sleep(0.1)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"📄 数据已保存为JSON: {filename}")
            return True
        except Exception as e:
            print(f"❌ JSON保存失败: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "JSON存储"


class CSVStorageStrategy(StorageStrategy):
    """CSV存储策略"""
    
    async def save(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存为CSV格式"""
        try:
            if not data:
                return False
            
            # 模拟异步IO操作
            await asyncio.sleep(0.1)
            
            fieldnames = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"📊 数据已保存为CSV: {filename}")
            return True
        except Exception as e:
            print(f"❌ CSV保存失败: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "CSV存储"


class XMLStorageStrategy(StorageStrategy):
    """XML存储策略"""
    
    async def save(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """保存为XML格式"""
        try:
            # 模拟异步IO操作
            await asyncio.sleep(0.1)
            
            root = ET.Element("data")
            
            for item in data:
                record = ET.SubElement(root, "record")
                for key, value in item.items():
                    element = ET.SubElement(record, key)
                    element.text = str(value)
            
            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            
            print(f"📋 数据已保存为XML: {filename}")
            return True
        except Exception as e:
            print(f"❌ XML保存失败: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "XML存储"


# ==================== 数据处理管道 ====================

class DataProcessingPipeline:
    """数据处理管道"""
    
    def __init__(self):
        self.validation_strategies: List[ValidationStrategy] = []
        self.transform_strategies: List[TransformStrategy] = []
        self.storage_strategy: Optional[StorageStrategy] = None
        self.processing_history: List[Dict[str, Any]] = []
    
    def add_validation_strategy(self, strategy: ValidationStrategy) -> None:
        """添加验证策略"""
        self.validation_strategies.append(strategy)
        print(f"✅ 添加验证策略: {strategy.get_strategy_name()}")
    
    def add_transform_strategy(self, strategy: TransformStrategy) -> None:
        """添加转换策略"""
        self.transform_strategies.append(strategy)
        print(f"🔄 添加转换策略: {strategy.get_strategy_name()}")
    
    def set_storage_strategy(self, strategy: StorageStrategy) -> None:
        """设置存储策略"""
        self.storage_strategy = strategy
        print(f"💾 设置存储策略: {strategy.get_strategy_name()}")
    
    async def process_data(self, raw_data: List[Dict[str, Any]], output_filename: str = None) -> Dict[str, Any]:
        """处理数据"""
        print(f"\n🚀 开始数据处理管道...")
        print(f"📊 输入数据: {len(raw_data)} 条记录")
        
        start_time = datetime.now()
        valid_data = []
        invalid_data = []
        
        # 数据验证阶段
        print(f"\n🔍 数据验证阶段...")
        for i, record in enumerate(raw_data):
            record_valid = True
            validation_errors = []
            validated_record = record.copy()
            
            for strategy in self.validation_strategies:
                for field, value in record.items():
                    if field in ['email', 'phone', 'age']:  # 根据字段名选择验证策略
                        if (field == 'email' and isinstance(strategy, EmailValidationStrategy)) or \
                           (field == 'phone' and isinstance(strategy, PhoneValidationStrategy)) or \
                           (field == 'age' and isinstance(strategy, AgeValidationStrategy)):
                            
                            result = strategy.validate(value)
                            if not result['valid']:
                                record_valid = False
                                validation_errors.append(f"{field}: {result['error']}")
                            elif 'normalized' in result:
                                validated_record[field] = result['normalized']
            
            if record_valid:
                valid_data.append(validated_record)
            else:
                invalid_data.append({
                    'record': record,
                    'errors': validation_errors
                })
        
        print(f"✅ 验证完成: {len(valid_data)} 条有效, {len(invalid_data)} 条无效")
        
        # 数据转换阶段
        print(f"\n🔄 数据转换阶段...")
        transformed_data = valid_data.copy()
        
        for strategy in self.transform_strategies:
            print(f"   应用策略: {strategy.get_strategy_name()}")
            for i, record in enumerate(transformed_data):
                for field, value in record.items():
                    transformed_data[i][field] = strategy.transform(value)
        
        print(f"✅ 转换完成: {len(transformed_data)} 条记录")
        
        # 数据存储阶段
        storage_success = False
        if self.storage_strategy and output_filename and transformed_data:
            print(f"\n💾 数据存储阶段...")
            storage_success = await self.storage_strategy.save(transformed_data, output_filename)
        
        # 记录处理历史
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        history_record = {
            'timestamp': start_time,
            'input_count': len(raw_data),
            'valid_count': len(valid_data),
            'invalid_count': len(invalid_data),
            'output_count': len(transformed_data),
            'processing_time': processing_time,
            'storage_success': storage_success,
            'validation_strategies': [s.get_strategy_name() for s in self.validation_strategies],
            'transform_strategies': [s.get_strategy_name() for s in self.transform_strategies],
            'storage_strategy': self.storage_strategy.get_strategy_name() if self.storage_strategy else None
        }
        
        self.processing_history.append(history_record)
        
        return {
            'valid_data': transformed_data,
            'invalid_data': invalid_data,
            'processing_time': processing_time,
            'storage_success': storage_success
        }
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """获取处理摘要"""
        if not self.processing_history:
            return {}
        
        total_processed = sum(h['input_count'] for h in self.processing_history)
        total_valid = sum(h['valid_count'] for h in self.processing_history)
        total_time = sum(h['processing_time'] for h in self.processing_history)
        
        return {
            'total_runs': len(self.processing_history),
            'total_processed': total_processed,
            'total_valid': total_valid,
            'success_rate': (total_valid / total_processed * 100) if total_processed > 0 else 0,
            'total_processing_time': total_time,
            'average_processing_time': total_time / len(self.processing_history)
        }


# ==================== 演示函数 ====================

async def demo_data_processing_pipeline():
    """数据处理管道演示"""
    print("=" * 60)
    print("🔄 数据处理策略系统演示")
    print("=" * 60)
    
    # 创建测试数据
    test_data = [
        {'name': 'zhang san', 'email': 'zhang@example.com', 'phone': '138-0013-8000', 'age': '25', 'city': 'beijing'},
        {'name': 'li si', 'email': 'invalid-email', 'phone': '139-0013-9000', 'age': '30', 'city': 'shanghai'},
        {'name': 'wang wu', 'email': 'wang@test.com', 'phone': '13700137000', 'age': 'invalid', 'city': 'guangzhou'},
        {'name': 'zhao liu', 'email': 'zhao@demo.com', 'phone': '136-0013-6000', 'age': '28', 'city': 'shenzhen'},
        {'name': 'qian qi', 'email': 'qian@sample.com', 'phone': '135-0013-5000', 'age': '200', 'city': 'hangzhou'},
    ]
    
    print(f"📊 原始数据:")
    for i, record in enumerate(test_data, 1):
        print(f"   {i}. {record}")
    
    # 创建数据处理管道
    pipeline = DataProcessingPipeline()
    
    # 添加验证策略
    pipeline.add_validation_strategy(EmailValidationStrategy())
    pipeline.add_validation_strategy(PhoneValidationStrategy())
    pipeline.add_validation_strategy(AgeValidationStrategy(min_age=18, max_age=100))
    
    # 添加转换策略
    pipeline.add_transform_strategy(UpperCaseTransformStrategy())
    pipeline.add_transform_strategy(DateFormatTransformStrategy())
    
    # 设置存储策略
    pipeline.set_storage_strategy(JSONStorageStrategy())
    
    # 处理数据
    result = await pipeline.process_data(test_data, "processed_data.json")
    
    # 显示结果
    print(f"\n📋 处理结果:")
    print(f"   有效数据: {len(result['valid_data'])} 条")
    print(f"   无效数据: {len(result['invalid_data'])} 条")
    print(f"   处理时间: {result['processing_time']:.3f} 秒")
    print(f"   存储成功: {'是' if result['storage_success'] else '否'}")
    
    if result['invalid_data']:
        print(f"\n❌ 无效数据详情:")
        for i, invalid in enumerate(result['invalid_data'], 1):
            print(f"   {i}. 错误: {', '.join(invalid['errors'])}")
    
    # 显示处理摘要
    summary = pipeline.get_processing_summary()
    print(f"\n📊 处理摘要:")
    print(f"   总运行次数: {summary['total_runs']}")
    print(f"   总处理记录: {summary['total_processed']}")
    print(f"   成功率: {summary['success_rate']:.1f}%")
    print(f"   平均处理时间: {summary['average_processing_time']:.3f} 秒")


async def demo_different_storage_strategies():
    """不同存储策略演示"""
    print("\n" + "=" * 60)
    print("💾 不同存储策略演示")
    print("=" * 60)
    
    # 简单的测试数据
    simple_data = [
        {'id': 1, 'name': 'ALICE', 'score': 95},
        {'id': 2, 'name': 'BOB', 'score': 87},
        {'id': 3, 'name': 'CHARLIE', 'score': 92}
    ]
    
    # 测试不同存储策略
    storage_strategies = [
        JSONStorageStrategy(),
        CSVStorageStrategy(),
        XMLStorageStrategy()
    ]
    
    for strategy in storage_strategies:
        print(f"\n测试 {strategy.get_strategy_name()}:")
        filename = f"test_data.{strategy.get_strategy_name().split('存储')[0].lower()}"
        success = await strategy.save(simple_data, filename)
        print(f"   保存结果: {'成功' if success else '失败'}")


if __name__ == "__main__":
    # 运行数据处理管道演示
    asyncio.run(demo_data_processing_pipeline())
    
    # 运行存储策略演示
    asyncio.run(demo_different_storage_strategies())
    
    print("\n" + "=" * 60)
    print("✅ 数据处理策略演示完成")
    print("💡 学习要点:")
    print("   - 策略模式可以组合使用形成处理管道")
    print("   - 验证、转换、存储策略可以独立配置")
    print("   - 异步处理提高了数据处理的效率")
    print("   - 策略的组合使用增强了系统的灵活性")
    print("=" * 60)
