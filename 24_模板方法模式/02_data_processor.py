"""
02_data_processor.py - 数据处理系统的模板方法应用

这个示例展示了在数据处理系统中如何使用模板方法模式：
- 统一的数据处理流程
- 不同数据格式的具体处理实现
- 灵活的验证和转换机制
"""

from abc import ABC, abstractmethod
import json
import csv
import io
from typing import List, Dict, Any
import time


# ==================== 抽象数据处理器 ====================
class DataProcessor(ABC):
    """数据处理器模板类
    
    定义了数据处理的标准ETL流程：
    Extract（提取） -> Transform（转换） -> Load（加载）
    """
    
    def __init__(self, name: str):
        self.name = name
        self.processed_count = 0
        self.error_count = 0
    
    def process_data(self, source: str, destination: str) -> Dict[str, Any]:
        """模板方法 - 定义完整的数据处理流程"""
        print(f"🚀 开始数据处理: {self.name}")
        print(f"源: {source} -> 目标: {destination}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            # 1. 提取数据 (Extract)
            print("📥 步骤1: 提取数据")
            raw_data = self.extract_data(source)
            print(f"✅ 提取完成，获得 {len(raw_data)} 条原始数据")
            
            # 2. 验证数据
            print("\n🔍 步骤2: 验证数据")
            if self.should_validate():
                valid_data = self.validate_data(raw_data)
                invalid_count = len(raw_data) - len(valid_data)
                if invalid_count > 0:
                    print(f"⚠️  发现 {invalid_count} 条无效数据")
                    self.error_count += invalid_count
                print(f"✅ 验证完成，{len(valid_data)} 条数据有效")
            else:
                valid_data = raw_data
                print("⏭️  跳过数据验证")
            
            # 3. 转换数据 (Transform)
            print("\n🔄 步骤3: 转换数据")
            transformed_data = self.transform_data(valid_data)
            print(f"✅ 转换完成，处理了 {len(transformed_data)} 条数据")
            
            # 4. 加载数据 (Load)
            print("\n💾 步骤4: 加载数据")
            self.load_data(transformed_data, destination)
            self.processed_count = len(transformed_data)
            print(f"✅ 加载完成，保存了 {self.processed_count} 条数据")
            
            # 5. 生成报告
            print("\n📊 步骤5: 生成处理报告")
            report = self.generate_report(start_time)
            
            print("-" * 60)
            print("🎉 数据处理完成!")
            return report
            
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    # 抽象方法 - 子类必须实现
    @abstractmethod
    def extract_data(self, source: str) -> List[Dict[str, Any]]:
        """提取数据 - 子类必须实现"""
        pass
    
    @abstractmethod
    def load_data(self, data: List[Dict[str, Any]], destination: str):
        """加载数据 - 子类必须实现"""
        pass
    
    # 具体方法 - 提供默认实现
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证数据 - 默认实现：移除空记录"""
        valid_data = []
        for record in data:
            if record and any(str(value).strip() for value in record.values() if value is not None):
                valid_data.append(record)
        return valid_data
    
    def transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换数据 - 默认实现：不做转换"""
        return data
    
    def generate_report(self, start_time: float) -> Dict[str, Any]:
        """生成处理报告"""
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        report = {
            "processor": self.name,
            "status": "success",
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "duration_seconds": duration,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"处理器: {report['processor']}")
        print(f"状态: {report['status']}")
        print(f"处理数量: {report['processed_count']}")
        print(f"错误数量: {report['error_count']}")
        print(f"耗时: {report['duration_seconds']} 秒")
        
        return report
    
    # 钩子方法 - 子类可选择重写
    def should_validate(self) -> bool:
        """是否需要验证数据"""
        return True


# ==================== 具体数据处理器 ====================
class CSVProcessor(DataProcessor):
    """CSV数据处理器"""
    
    def __init__(self):
        super().__init__("CSV处理器")
    
    def extract_data(self, source: str) -> List[Dict[str, Any]]:
        """从CSV文件提取数据"""
        print(f"读取CSV文件: {source}")
        
        # 模拟CSV数据（实际应用中会读取真实文件）
        csv_content = """name,age,city,salary
张三,25,北京,8000
李四,30,上海,12000
王五,,广州,9000
,35,深圳,15000
赵六,28,杭州,11000"""
        
        data = []
        reader = csv.DictReader(io.StringIO(csv_content))
        for row in reader:
            data.append(dict(row))
        
        return data
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证CSV数据：确保姓名和城市不为空"""
        valid_data = []
        for record in data:
            if record.get('name', '').strip() and record.get('city', '').strip():
                valid_data.append(record)
            else:
                print(f"⚠️  无效记录: {record}")
        return valid_data
    
    def transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换CSV数据：标准化格式，添加年龄组"""
        transformed = []
        for record in data:
            new_record = record.copy()
            
            # 处理年龄
            try:
                age = int(record.get('age', 0)) if record.get('age') else 0
                new_record['age'] = age
                
                # 添加年龄组
                if age < 30:
                    new_record['age_group'] = '青年'
                elif age < 50:
                    new_record['age_group'] = '中年'
                else:
                    new_record['age_group'] = '老年'
            except ValueError:
                new_record['age'] = 0
                new_record['age_group'] = '未知'
            
            # 处理薪资
            try:
                salary = float(record.get('salary', 0)) if record.get('salary') else 0
                new_record['salary'] = salary
                
                # 添加薪资等级
                if salary < 8000:
                    new_record['salary_level'] = '初级'
                elif salary < 15000:
                    new_record['salary_level'] = '中级'
                else:
                    new_record['salary_level'] = '高级'
            except ValueError:
                new_record['salary'] = 0
                new_record['salary_level'] = '未知'
            
            transformed.append(new_record)
        
        return transformed
    
    def load_data(self, data: List[Dict[str, Any]], destination: str):
        """保存为CSV格式"""
        print(f"保存到CSV文件: {destination}")
        
        if data:
            # 模拟保存过程
            fieldnames = data[0].keys()
            print(f"字段: {', '.join(fieldnames)}")
            print(f"样例数据: {data[0]}")


class JSONProcessor(DataProcessor):
    """JSON数据处理器"""
    
    def __init__(self):
        super().__init__("JSON处理器")
    
    def extract_data(self, source: str) -> List[Dict[str, Any]]:
        """从JSON文件提取数据"""
        print(f"读取JSON文件: {source}")
        
        # 模拟JSON数据
        json_data = [
            {"id": 1, "product": "笔记本电脑", "price": 5999, "stock": 10, "category": "电子产品"},
            {"id": 2, "product": "手机", "price": 3999, "stock": 0, "category": "电子产品"},
            {"id": 3, "product": "平板电脑", "price": 2999, "stock": 5, "category": "电子产品"},
            {"id": 4, "product": "", "price": 1999, "stock": 8, "category": "电子产品"},
            {"id": 5, "product": "耳机", "price": 299, "stock": 20, "category": "配件"}
        ]
        
        return json_data
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证JSON数据：移除库存为0或产品名为空的记录"""
        valid_data = []
        for record in data:
            if (record.get('stock', 0) > 0 and 
                record.get('product', '').strip() and
                record.get('price', 0) > 0):
                valid_data.append(record)
            else:
                print(f"⚠️  无效产品: {record}")
        return valid_data
    
    def transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换JSON数据：添加价格等级和库存状态"""
        transformed = []
        for record in data:
            new_record = record.copy()
            
            # 添加价格等级
            price = record.get('price', 0)
            if price < 1000:
                new_record['price_level'] = '经济型'
            elif price < 5000:
                new_record['price_level'] = '中端'
            else:
                new_record['price_level'] = '高端'
            
            # 添加库存状态
            stock = record.get('stock', 0)
            if stock > 15:
                new_record['stock_status'] = '充足'
            elif stock > 5:
                new_record['stock_status'] = '正常'
            else:
                new_record['stock_status'] = '紧张'
            
            # 计算总价值
            new_record['total_value'] = price * stock
            
            transformed.append(new_record)
        
        return transformed
    
    def load_data(self, data: List[Dict[str, Any]], destination: str):
        """保存为JSON格式"""
        print(f"保存到JSON文件: {destination}")
        
        # 模拟保存过程
        print(f"保存了 {len(data)} 个产品记录")
        if data:
            print(f"样例数据: {json.dumps(data[0], ensure_ascii=False, indent=2)}")


class DatabaseProcessor(DataProcessor):
    """数据库数据处理器"""
    
    def __init__(self):
        super().__init__("数据库处理器")
    
    def extract_data(self, source: str) -> List[Dict[str, Any]]:
        """从数据库提取数据"""
        print(f"连接数据库: {source}")
        print("执行查询...")
        
        # 模拟数据库数据
        db_data = [
            {"user_id": 1, "username": "alice", "email": "alice@example.com", "status": "active", "login_count": 150},
            {"user_id": 2, "username": "bob", "email": "invalid-email", "status": "active", "login_count": 89},
            {"user_id": 3, "username": "charlie", "email": "charlie@example.com", "status": "inactive", "login_count": 0},
            {"user_id": 4, "username": "", "email": "test@example.com", "status": "active", "login_count": 45},
            {"user_id": 5, "username": "diana", "email": "diana@example.com", "status": "active", "login_count": 203}
        ]
        
        return db_data
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """验证数据库数据：检查用户名和邮箱格式"""
        valid_data = []
        for record in data:
            username = record.get('username', '').strip()
            email = record.get('email', '').strip()
            
            # 简单的邮箱格式验证
            is_valid_email = '@' in email and '.' in email.split('@')[-1]
            
            if username and is_valid_email:
                valid_data.append(record)
            else:
                print(f"⚠️  无效用户: {record}")
        
        return valid_data
    
    def transform_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """转换数据库数据：添加用户等级"""
        transformed = []
        for record in data:
            new_record = record.copy()
            
            # 根据登录次数确定用户等级
            login_count = record.get('login_count', 0)
            if login_count > 200:
                new_record['user_level'] = 'VIP'
            elif login_count > 100:
                new_record['user_level'] = '高级用户'
            elif login_count > 50:
                new_record['user_level'] = '普通用户'
            else:
                new_record['user_level'] = '新用户'
            
            # 添加活跃度标记
            if record.get('status') == 'active' and login_count > 0:
                new_record['is_active'] = True
            else:
                new_record['is_active'] = False
            
            transformed.append(new_record)
        
        return transformed
    
    def load_data(self, data: List[Dict[str, Any]], destination: str):
        """保存到数据库"""
        print(f"保存到数据库表: {destination}")
        
        # 模拟数据库保存
        print(f"插入了 {len(data)} 条用户记录")
        if data:
            print(f"样例记录: {data[0]}")
    
    def should_validate(self) -> bool:
        """数据库数据需要严格验证"""
        return True


# ==================== 演示函数 ====================
def demo_data_processors():
    """数据处理器演示"""
    print("=" * 80)
    print("数据处理系统模板方法演示")
    print("=" * 80)
    
    # 创建不同类型的数据处理器
    processors = [
        (CSVProcessor(), "employees.csv", "processed_employees.csv"),
        (JSONProcessor(), "products.json", "processed_products.json"),
        (DatabaseProcessor(), "user_database", "processed_users")
    ]
    
    reports = []
    
    # 执行数据处理
    for processor, source, destination in processors:
        print(f"\n{'='*20} {processor.name} {'='*20}")
        report = processor.process_data(source, destination)
        reports.append(report)
        time.sleep(1)
    
    # 汇总报告
    print("\n" + "="*80)
    print("📈 处理汇总报告")
    print("="*80)
    
    total_processed = sum(r.get('processed_count', 0) for r in reports)
    total_errors = sum(r.get('error_count', 0) for r in reports)
    total_duration = sum(r.get('duration_seconds', 0) for r in reports)
    
    print(f"总处理数量: {total_processed}")
    print(f"总错误数量: {total_errors}")
    print(f"总耗时: {round(total_duration, 2)} 秒")
    print(f"成功率: {round((total_processed / (total_processed + total_errors)) * 100, 1)}%")


if __name__ == "__main__":
    demo_data_processors()
