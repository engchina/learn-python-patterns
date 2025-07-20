"""
适配器模式基础实现 - 数据格式转换系统

这个示例展示了适配器模式的基本概念，通过数据格式转换来演示
如何让不兼容的接口协同工作。

作者: Adapter Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import json
import xml.etree.ElementTree as ET


# ==================== 目标接口 ====================

class DataProcessor(ABC):
    """数据处理器接口 - 客户端期望的接口"""
    
    @abstractmethod
    def process_data(self, data: str) -> Dict[str, Any]:
        """处理数据并返回标准格式"""
        pass
    
    @abstractmethod
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        pass


# ==================== 被适配者 ====================

class XMLDataSource:
    """XML数据源 - 被适配者A"""
    
    def __init__(self):
        self.processed_count = 0
    
    def read_xml_data(self, xml_string: str) -> ET.Element:
        """读取XML数据（原有接口）"""
        print(f"📄 XML数据源读取数据")
        self.processed_count += 1
        try:
            root = ET.fromstring(xml_string)
            return root
        except ET.ParseError as e:
            print(f"❌ XML解析错误: {e}")
            return None
    
    def get_xml_info(self) -> str:
        """获取XML数据源信息"""
        return f"XML数据源 (已处理: {self.processed_count} 次)"


class CSVDataSource:
    """CSV数据源 - 被适配者B"""
    
    def __init__(self):
        self.processed_count = 0
    
    def parse_csv_content(self, csv_string: str) -> List[List[str]]:
        """解析CSV内容（原有接口）"""
        print(f"📊 CSV数据源解析数据")
        self.processed_count += 1
        
        lines = csv_string.strip().split('\n')
        result = []
        for line in lines:
            row = [cell.strip() for cell in line.split(',')]
            result.append(row)
        return result
    
    def get_csv_info(self) -> str:
        """获取CSV数据源信息"""
        return f"CSV数据源 (已处理: {self.processed_count} 次)"


class BinaryDataSource:
    """二进制数据源 - 被适配者C"""
    
    def __init__(self):
        self.processed_count = 0
    
    def decode_binary_data(self, binary_data: bytes) -> str:
        """解码二进制数据（原有接口）"""
        print(f"🔢 二进制数据源解码数据")
        self.processed_count += 1
        try:
            return binary_data.decode('utf-8')
        except UnicodeDecodeError:
            return binary_data.decode('latin-1')
    
    def get_binary_info(self) -> str:
        """获取二进制数据源信息"""
        return f"二进制数据源 (已处理: {self.processed_count} 次)"


# ==================== 适配器实现 ====================

class XMLDataAdapter(DataProcessor):
    """XML数据适配器 - 对象适配器"""
    
    def __init__(self, xml_source: XMLDataSource):
        self.xml_source = xml_source
    
    def process_data(self, data: str) -> Dict[str, Any]:
        """将XML数据转换为标准格式"""
        print(f"🔄 XML适配器处理数据")
        
        # 调用被适配者的方法
        xml_root = self.xml_source.read_xml_data(data)
        
        if xml_root is None:
            return {"error": "XML解析失败"}
        
        # 转换为标准格式
        result = {
            "type": "xml",
            "data": self._xml_to_dict(xml_root),
            "source": "XML数据源"
        }
        
        print(f"✅ XML数据转换完成")
        return result
    
    def _xml_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """将XML元素转换为字典"""
        result = {}
        
        # 添加属性
        if element.attrib:
            result["@attributes"] = element.attrib
        
        # 添加文本内容
        if element.text and element.text.strip():
            result["text"] = element.text.strip()
        
        # 添加子元素
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                # 如果标签已存在，转换为列表
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        return f"XML适配器 -> {self.xml_source.get_xml_info()}"


class CSVDataAdapter(DataProcessor):
    """CSV数据适配器 - 对象适配器"""
    
    def __init__(self, csv_source: CSVDataSource):
        self.csv_source = csv_source
    
    def process_data(self, data: str) -> Dict[str, Any]:
        """将CSV数据转换为标准格式"""
        print(f"🔄 CSV适配器处理数据")
        
        # 调用被适配者的方法
        csv_rows = self.csv_source.parse_csv_content(data)
        
        if not csv_rows:
            return {"error": "CSV解析失败"}
        
        # 转换为标准格式
        headers = csv_rows[0] if csv_rows else []
        data_rows = csv_rows[1:] if len(csv_rows) > 1 else []
        
        records = []
        for row in data_rows:
            record = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    record[headers[i]] = value
            records.append(record)
        
        result = {
            "type": "csv",
            "data": {
                "headers": headers,
                "records": records,
                "total_rows": len(data_rows)
            },
            "source": "CSV数据源"
        }
        
        print(f"✅ CSV数据转换完成")
        return result
    
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        return f"CSV适配器 -> {self.csv_source.get_csv_info()}"


class BinaryDataAdapter(DataProcessor):
    """二进制数据适配器 - 对象适配器"""
    
    def __init__(self, binary_source: BinaryDataSource):
        self.binary_source = binary_source
    
    def process_data(self, data: str) -> Dict[str, Any]:
        """将二进制数据转换为标准格式"""
        print(f"🔄 二进制适配器处理数据")
        
        # 将字符串转换为字节
        if isinstance(data, str):
            binary_data = data.encode('utf-8')
        else:
            binary_data = data
        
        # 调用被适配者的方法
        decoded_text = self.binary_source.decode_binary_data(binary_data)
        
        # 转换为标准格式
        result = {
            "type": "binary",
            "data": {
                "decoded_text": decoded_text,
                "original_size": len(binary_data),
                "encoding": "utf-8"
            },
            "source": "二进制数据源"
        }
        
        print(f"✅ 二进制数据转换完成")
        return result
    
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        return f"二进制适配器 -> {self.binary_source.get_binary_info()}"


# ==================== 类适配器示例 ====================

class JSONDataSource:
    """JSON数据源"""
    
    def __init__(self):
        self.processed_count = 0
    
    def load_json_data(self, json_string: str) -> Dict[str, Any]:
        """加载JSON数据"""
        print(f"📋 JSON数据源加载数据")
        self.processed_count += 1
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            return {}


class JSONDataClassAdapter(DataProcessor, JSONDataSource):
    """JSON数据类适配器 - 使用多重继承"""
    
    def __init__(self):
        JSONDataSource.__init__(self)
    
    def process_data(self, data: str) -> Dict[str, Any]:
        """将JSON数据转换为标准格式"""
        print(f"🔄 JSON类适配器处理数据")
        
        # 直接调用继承的方法
        json_data = self.load_json_data(data)
        
        # 转换为标准格式
        result = {
            "type": "json",
            "data": json_data,
            "source": "JSON数据源"
        }
        
        print(f"✅ JSON数据转换完成")
        return result
    
    def get_processor_info(self) -> str:
        """获取处理器信息"""
        return f"JSON类适配器 (已处理: {self.processed_count} 次)"


# ==================== 客户端代码 ====================

class DataAnalyzer:
    """数据分析器 - 客户端"""
    
    def __init__(self):
        self.processors: List[DataProcessor] = []
    
    def add_processor(self, processor: DataProcessor) -> None:
        """添加数据处理器"""
        self.processors.append(processor)
        print(f"➕ 已添加处理器: {processor.get_processor_info()}")
    
    def analyze_data(self, data: str, processor_index: int = 0) -> Dict[str, Any]:
        """分析数据"""
        if 0 <= processor_index < len(self.processors):
            processor = self.processors[processor_index]
            print(f"\n📊 使用处理器分析数据: {processor.get_processor_info()}")
            return processor.process_data(data)
        else:
            print(f"❌ 无效的处理器索引: {processor_index}")
            return {"error": "无效的处理器"}
    
    def analyze_with_all_processors(self, data_samples: List[tuple]) -> None:
        """使用所有处理器分析数据样本"""
        print(f"\n🔍 使用所有处理器分析数据样本")
        
        for i, (data, description) in enumerate(data_samples):
            print(f"\n--- 样本 {i+1}: {description} ---")
            if i < len(self.processors):
                result = self.analyze_data(data, i)
                print(f"📋 分析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            else:
                print(f"⚠️  没有对应的处理器")


def demo_basic_adapter():
    """基础适配器模式演示"""
    print("=" * 60)
    print("🔄 数据格式转换系统 - 适配器模式演示")
    print("=" * 60)
    
    # 创建被适配者
    xml_source = XMLDataSource()
    csv_source = CSVDataSource()
    binary_source = BinaryDataSource()
    
    # 创建适配器
    xml_adapter = XMLDataAdapter(xml_source)
    csv_adapter = CSVDataAdapter(csv_source)
    binary_adapter = BinaryDataAdapter(binary_source)
    json_adapter = JSONDataClassAdapter()
    
    # 创建客户端
    analyzer = DataAnalyzer()
    
    # 添加处理器
    analyzer.add_processor(xml_adapter)
    analyzer.add_processor(csv_adapter)
    analyzer.add_processor(binary_adapter)
    analyzer.add_processor(json_adapter)
    
    # 准备测试数据
    xml_data = """<?xml version="1.0"?>
    <users>
        <user id="1">
            <name>张三</name>
            <age>25</age>
        </user>
        <user id="2">
            <name>李四</name>
            <age>30</age>
        </user>
    </users>"""
    
    csv_data = """姓名,年龄,部门
张三,25,开发部
李四,30,测试部
王五,28,产品部"""
    
    binary_data = "Hello, 适配器模式!"
    
    json_data = """{"users": [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]}"""
    
    # 测试数据样本
    data_samples = [
        (xml_data, "XML用户数据"),
        (csv_data, "CSV员工数据"),
        (binary_data, "二进制文本数据"),
        (json_data, "JSON用户数据")
    ]
    
    # 使用所有处理器分析数据
    analyzer.analyze_with_all_processors(data_samples)


def demo_adapter_flexibility():
    """适配器灵活性演示"""
    print("\n" + "=" * 60)
    print("🔧 适配器灵活性演示")
    print("=" * 60)
    
    # 创建数据分析器
    analyzer = DataAnalyzer()
    
    # 动态添加不同的适配器
    adapters = [
        XMLDataAdapter(XMLDataSource()),
        CSVDataAdapter(CSVDataSource()),
        JSONDataClassAdapter()
    ]
    
    for adapter in adapters:
        analyzer.add_processor(adapter)
    
    # 测试相同接口的不同实现
    test_data = [
        ("<data><item>测试</item></data>", "XML测试数据"),
        ("标题,内容\n测试,数据", "CSV测试数据"),
        ('{"test": "数据"}', "JSON测试数据")
    ]
    
    print(f"\n🧪 测试统一接口的不同实现:")
    for i, (data, desc) in enumerate(test_data):
        print(f"\n🔸 {desc}:")
        result = analyzer.analyze_data(data, i)
        print(f"   类型: {result.get('type', 'unknown')}")
        print(f"   来源: {result.get('source', 'unknown')}")


if __name__ == "__main__":
    demo_basic_adapter()
    demo_adapter_flexibility()
