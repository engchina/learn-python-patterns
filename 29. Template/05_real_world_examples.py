"""
05_real_world_examples.py - 实际项目中的模板方法应用

这个示例展示了模板方法模式在实际开发中的常见应用：
- 测试框架的设计
- 报告生成系统
- 工作流引擎
- 数据备份系统
"""

from abc import ABC, abstractmethod
import time
import json
from typing import List, Dict, Any, Optional
from enum import Enum


class TestResult(Enum):
    """测试结果枚举"""
    PASS = "通过"
    FAIL = "失败"
    SKIP = "跳过"
    ERROR = "错误"


# ==================== 测试框架示例 ====================
class TestCase(ABC):
    """测试用例模板类
    
    定义了测试用例的标准执行流程：
    1. 测试前准备 (setUp)
    2. 执行测试 (runTest)
    3. 测试后清理 (tearDown)
    4. 生成测试报告
    """
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.result = None
        self.error_message = None
        self.start_time = None
        self.end_time = None
        self.test_data = {}
    
    def run(self) -> Dict[str, Any]:
        """模板方法 - 定义测试执行流程"""
        print(f"🧪 开始测试: {self.test_name}")
        print("-" * 50)
        
        self.start_time = time.time()
        
        try:
            # 1. 测试前准备
            print("📋 步骤1: 测试前准备")
            self.setUp()
            print("✅ 准备完成")
            
            # 2. 执行测试
            print("\n🔬 步骤2: 执行测试")
            if self.should_run_test():
                self.runTest()
                if self.result is None:
                    self.result = TestResult.PASS
                print(f"✅ 测试执行完成: {self.result.value}")
            else:
                self.result = TestResult.SKIP
                print("⏭️  测试被跳过")
            
        except AssertionError as e:
            self.result = TestResult.FAIL
            self.error_message = str(e)
            print(f"❌ 测试失败: {self.error_message}")
            
        except Exception as e:
            self.result = TestResult.ERROR
            self.error_message = str(e)
            print(f"💥 测试错误: {self.error_message}")
            
        finally:
            # 3. 测试后清理
            print("\n🧹 步骤3: 测试后清理")
            try:
                self.tearDown()
                print("✅ 清理完成")
            except Exception as e:
                print(f"⚠️  清理时发生错误: {str(e)}")
        
        self.end_time = time.time()
        
        # 4. 生成测试报告
        report = self.generate_test_report()
        
        print("-" * 50)
        print(f"🎯 测试完成: {self.result.value}")
        return report
    
    # 抽象方法 - 子类必须实现
    @abstractmethod
    def runTest(self):
        """执行具体测试逻辑"""
        pass
    
    # 具体方法 - 提供默认实现
    def setUp(self):
        """测试前准备 - 默认实现"""
        print("初始化测试环境...")
    
    def tearDown(self):
        """测试后清理 - 默认实现"""
        print("清理测试环境...")
    
    def generate_test_report(self) -> Dict[str, Any]:
        """生成测试报告"""
        duration = round(self.end_time - self.start_time, 3)
        
        report = {
            "test_name": self.test_name,
            "result": self.result.value,
            "duration_seconds": duration,
            "error_message": self.error_message,
            "test_data": self.test_data,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"测试名称: {report['test_name']}")
        print(f"测试结果: {report['result']}")
        print(f"执行时间: {report['duration_seconds']} 秒")
        if report['error_message']:
            print(f"错误信息: {report['error_message']}")
        
        return report
    
    # 钩子方法
    def should_run_test(self) -> bool:
        """是否应该运行测试"""
        return True
    
    # 断言方法
    def assertEqual(self, expected, actual, message=""):
        """断言相等"""
        if expected != actual:
            error_msg = f"断言失败: 期望 {expected}, 实际 {actual}"
            if message:
                error_msg += f" - {message}"
            raise AssertionError(error_msg)
    
    def assertTrue(self, condition, message=""):
        """断言为真"""
        if not condition:
            error_msg = "断言失败: 条件为假"
            if message:
                error_msg += f" - {message}"
            raise AssertionError(error_msg)


class DatabaseTestCase(TestCase):
    """数据库测试用例"""
    
    def __init__(self):
        super().__init__("数据库连接测试")
        self.connection = None
    
    def setUp(self):
        """数据库测试准备"""
        super().setUp()
        print("连接测试数据库...")
        print("创建测试表...")
        self.connection = "mock_db_connection"
        self.test_data["setup_time"] = time.time()
    
    def runTest(self):
        """执行数据库测试"""
        print("测试数据库连接...")
        self.assertTrue(self.connection is not None, "数据库连接不能为空")
        
        print("测试数据插入...")
        # 模拟数据插入
        inserted_rows = 5
        self.test_data["inserted_rows"] = inserted_rows
        self.assertTrue(inserted_rows > 0, "应该插入数据")
        
        print("测试数据查询...")
        # 模拟数据查询
        query_result = ["row1", "row2", "row3", "row4", "row5"]
        self.test_data["query_result_count"] = len(query_result)
        self.assertEqual(inserted_rows, len(query_result), "查询结果数量应该等于插入数量")
    
    def tearDown(self):
        """数据库测试清理"""
        super().tearDown()
        print("删除测试数据...")
        print("关闭数据库连接...")
        self.connection = None


class APITestCase(TestCase):
    """API测试用例"""
    
    def __init__(self):
        super().__init__("API接口测试")
        self.api_client = None
    
    def setUp(self):
        """API测试准备"""
        super().setUp()
        print("初始化API客户端...")
        print("设置认证信息...")
        self.api_client = "mock_api_client"
    
    def runTest(self):
        """执行API测试"""
        print("测试GET请求...")
        # 模拟GET请求
        get_response = {"status": 200, "data": {"id": 1, "name": "测试用户"}}
        self.test_data["get_response"] = get_response
        self.assertEqual(200, get_response["status"], "GET请求应该返回200")
        
        print("测试POST请求...")
        # 模拟POST请求
        post_data = {"name": "新用户", "email": "test@example.com"}
        post_response = {"status": 201, "data": {"id": 2, **post_data}}
        self.test_data["post_response"] = post_response
        self.assertEqual(201, post_response["status"], "POST请求应该返回201")
        
        print("测试错误处理...")
        # 模拟错误响应
        error_response = {"status": 404, "error": "Not Found"}
        self.test_data["error_response"] = error_response
        self.assertEqual(404, error_response["status"], "错误请求应该返回404")
    
    def tearDown(self):
        """API测试清理"""
        super().tearDown()
        print("清理测试数据...")
        print("关闭API连接...")


# ==================== 报告生成系统示例 ====================
class ReportGenerator(ABC):
    """报告生成器模板类"""
    
    def __init__(self, report_name: str):
        self.report_name = report_name
        self.data_source = None
        self.processed_data = None
        self.report_content = None
    
    def generate_report(self, data_source: str) -> Dict[str, Any]:
        """模板方法 - 定义报告生成流程"""
        print(f"📊 开始生成报告: {self.report_name}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # 1. 连接数据源
            print("🔗 步骤1: 连接数据源")
            self.connect_data_source(data_source)
            print("✅ 数据源连接成功")
            
            # 2. 收集数据
            print("\n📥 步骤2: 收集数据")
            raw_data = self.collect_data()
            print(f"✅ 收集到 {len(raw_data)} 条原始数据")
            
            # 3. 处理数据
            print("\n🔄 步骤3: 处理数据")
            self.processed_data = self.process_data(raw_data)
            print(f"✅ 处理完成，得到 {len(self.processed_data)} 条处理后数据")
            
            # 4. 生成报告内容
            print("\n📝 步骤4: 生成报告内容")
            self.report_content = self.create_report_content(self.processed_data)
            print("✅ 报告内容生成完成")
            
            # 5. 格式化输出
            print("\n🎨 步骤5: 格式化输出")
            formatted_report = self.format_report(self.report_content)
            
            # 6. 保存报告
            print("\n💾 步骤6: 保存报告")
            self.save_report(formatted_report)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            result = {
                "report_name": self.report_name,
                "status": "success",
                "data_count": len(self.processed_data),
                "duration_seconds": duration,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print("-" * 50)
            print("🎉 报告生成完成!")
            return result
            
        except Exception as e:
            print(f"❌ 报告生成失败: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    # 抽象方法
    @abstractmethod
    def collect_data(self) -> List[Dict[str, Any]]:
        """收集数据"""
        pass
    
    @abstractmethod
    def create_report_content(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建报告内容"""
        pass
    
    # 具体方法
    def connect_data_source(self, data_source: str):
        """连接数据源"""
        print(f"连接到数据源: {data_source}")
        self.data_source = data_source
    
    def process_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理数据 - 默认实现"""
        print("执行数据清洗和转换...")
        # 简单的数据处理：移除空值
        processed = [item for item in raw_data if item and any(item.values())]
        return processed
    
    def format_report(self, content: Dict[str, Any]) -> str:
        """格式化报告 - 默认实现"""
        print("应用报告模板...")
        return json.dumps(content, ensure_ascii=False, indent=2)
    
    def save_report(self, formatted_report: str):
        """保存报告 - 默认实现"""
        filename = f"{self.report_name.replace(' ', '_')}_report.json"
        print(f"保存报告到: {filename}")


class SalesReportGenerator(ReportGenerator):
    """销售报告生成器"""
    
    def __init__(self):
        super().__init__("销售业绩报告")
    
    def collect_data(self) -> List[Dict[str, Any]]:
        """收集销售数据"""
        print("从销售数据库收集数据...")
        
        # 模拟销售数据
        sales_data = []
        for i in range(20):
            sales_data.append({
                "order_id": f"ORD{1000 + i}",
                "product": f"产品{i % 5 + 1}",
                "amount": random.randint(100, 2000),
                "salesperson": f"销售员{i % 3 + 1}",
                "date": f"2024-01-{(i % 30) + 1:02d}"
            })
        
        return sales_data
    
    def create_report_content(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建销售报告内容"""
        print("分析销售数据...")
        
        # 计算销售统计
        total_sales = sum(item['amount'] for item in data)
        avg_sales = total_sales / len(data) if data else 0
        
        # 按销售员统计
        salesperson_stats = {}
        for item in data:
            person = item['salesperson']
            if person not in salesperson_stats:
                salesperson_stats[person] = {"count": 0, "total": 0}
            salesperson_stats[person]["count"] += 1
            salesperson_stats[person]["total"] += item['amount']
        
        return {
            "summary": {
                "total_orders": len(data),
                "total_sales": total_sales,
                "average_order": round(avg_sales, 2)
            },
            "salesperson_performance": salesperson_stats,
            "top_products": self._get_top_products(data)
        }
    
    def _get_top_products(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """获取热销产品"""
        product_stats = {}
        for item in data:
            product = item['product']
            if product not in product_stats:
                product_stats[product] = {"count": 0, "total": 0}
            product_stats[product]["count"] += 1
            product_stats[product]["total"] += item['amount']
        
        # 按销售额排序
        sorted_products = sorted(product_stats.items(), 
                               key=lambda x: x[1]['total'], reverse=True)
        
        return [{"product": k, **v} for k, v in sorted_products[:3]]


# ==================== 演示函数 ====================
def demo_test_framework():
    """测试框架演示"""
    print("=" * 60)
    print("🧪 测试框架模板方法演示")
    print("=" * 60)
    
    test_cases = [
        DatabaseTestCase(),
        APITestCase()
    ]
    
    test_results = []
    
    for test_case in test_cases:
        print(f"\n{'='*20} {test_case.test_name} {'='*20}")
        result = test_case.run()
        test_results.append(result)
        time.sleep(1)
    
    # 测试汇总
    print("\n" + "="*60)
    print("📈 测试汇总报告")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r['result'] == '通过')
    failed_tests = sum(1 for r in test_results if r['result'] == '失败')
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {failed_tests}")
    print(f"通过率: {round(passed_tests / total_tests * 100, 1)}%")


def demo_report_generator():
    """报告生成器演示"""
    print("\n" + "=" * 60)
    print("📊 报告生成系统模板方法演示")
    print("=" * 60)
    
    generator = SalesReportGenerator()
    result = generator.generate_report("sales_database")
    
    print(f"\n报告生成结果: {result}")


def main():
    """主演示函数"""
    print("=" * 80)
    print("🏭 实际项目中的模板方法应用演示")
    print("=" * 80)
    
    # 演示测试框架
    demo_test_framework()
    
    # 演示报告生成
    demo_report_generator()
    
    print("\n" + "="*80)
    print("✨ 所有演示完成!")
    print("="*80)


if __name__ == "__main__":
    import random
    main()
