"""
装饰器模式实际应用示例
展示装饰器模式在真实项目中的应用场景
"""

import json
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 1. Web API 中间件装饰器模式
class APIHandler(ABC):
    """API处理器抽象基类"""
    
    @abstractmethod
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        pass

class BasicAPIHandler(APIHandler):
    """基础API处理器"""
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理基础请求"""
        return {
            "status": "success",
            "data": f"处理请求: {request.get('endpoint', 'unknown')}",
            "timestamp": datetime.now().isoformat()
        }

class APIMiddleware(APIHandler):
    """API中间件基类"""
    
    def __init__(self, handler: APIHandler):
        self._handler = handler
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """默认处理行为"""
        return self._handler.handle_request(request)

class AuthenticationMiddleware(APIMiddleware):
    """身份验证中间件"""
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """添加身份验证"""
        token = request.get("token")
        if not token or token != "valid_token":
            logger.warning("🚫 身份验证失败")
            return {
                "status": "error",
                "message": "身份验证失败",
                "code": 401
            }
        
        logger.info("✅ 身份验证通过")
        return self._handler.handle_request(request)

class RateLimitMiddleware(APIMiddleware):
    """限流中间件"""
    
    def __init__(self, handler: APIHandler, max_requests: int = 5):
        super().__init__(handler)
        self.max_requests = max_requests
        self.request_count = 0
        self.reset_time = time.time() + 60  # 1分钟重置
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """添加限流控制"""
        current_time = time.time()
        
        # 重置计数器
        if current_time > self.reset_time:
            self.request_count = 0
            self.reset_time = current_time + 60
        
        # 检查限流
        if self.request_count >= self.max_requests:
            logger.warning("🚫 请求频率过高")
            return {
                "status": "error",
                "message": "请求频率过高，请稍后再试",
                "code": 429
            }
        
        self.request_count += 1
        logger.info(f"📊 当前请求数: {self.request_count}/{self.max_requests}")
        return self._handler.handle_request(request)

class LoggingMiddleware(APIMiddleware):
    """日志记录中间件"""
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """添加日志记录"""
        start_time = time.time()
        logger.info(f"📝 开始处理请求: {request}")
        
        response = self._handler.handle_request(request)
        
        end_time = time.time()
        logger.info(f"📝 请求处理完成，耗时: {end_time - start_time:.3f}秒")
        logger.info(f"📝 响应: {response}")
        
        return response

class CacheMiddleware(APIMiddleware):
    """缓存中间件"""
    
    def __init__(self, handler: APIHandler):
        super().__init__(handler)
        self.cache = {}
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """添加缓存功能"""
        # 创建缓存键
        cache_key = json.dumps(request, sort_keys=True)
        
        # 检查缓存
        if cache_key in self.cache:
            logger.info("💾 缓存命中")
            return self.cache[cache_key]
        
        # 处理请求并缓存结果
        response = self._handler.handle_request(request)
        self.cache[cache_key] = response
        logger.info("💾 响应已缓存")
        
        return response

# 2. 数据处理管道装饰器模式
class DataProcessor(ABC):
    """数据处理器抽象基类"""
    
    @abstractmethod
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理数据"""
        pass

class BasicDataProcessor(DataProcessor):
    """基础数据处理器"""
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """基础数据处理"""
        logger.info(f"📊 处理 {len(data)} 条数据")
        return data

class DataProcessorDecorator(DataProcessor):
    """数据处理器装饰器基类"""
    
    def __init__(self, processor: DataProcessor):
        self._processor = processor
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """默认处理行为"""
        return self._processor.process(data)

class DataValidationDecorator(DataProcessorDecorator):
    """数据验证装饰器"""
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """添加数据验证"""
        logger.info("🔍 开始数据验证")
        
        valid_data = []
        for item in data:
            if self._validate_item(item):
                valid_data.append(item)
            else:
                logger.warning(f"⚠️ 无效数据项: {item}")
        
        logger.info(f"✅ 验证完成，有效数据: {len(valid_data)}/{len(data)}")
        return self._processor.process(valid_data)
    
    def _validate_item(self, item: Dict[str, Any]) -> bool:
        """验证单个数据项"""
        required_fields = ["id", "name"]
        return all(field in item for field in required_fields)

class DataTransformDecorator(DataProcessorDecorator):
    """数据转换装饰器"""
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """添加数据转换"""
        logger.info("🔄 开始数据转换")
        
        transformed_data = []
        for item in data:
            transformed_item = item.copy()
            # 添加处理时间戳
            transformed_item["processed_at"] = datetime.now().isoformat()
            # 转换名称为大写
            if "name" in transformed_item:
                transformed_item["name"] = transformed_item["name"].upper()
            transformed_data.append(transformed_item)
        
        logger.info("✅ 数据转换完成")
        return self._processor.process(transformed_data)

class DataEnrichmentDecorator(DataProcessorDecorator):
    """数据丰富化装饰器"""
    
    def __init__(self, processor: DataProcessor, enrichment_data: Dict[str, Any]):
        super().__init__(processor)
        self.enrichment_data = enrichment_data
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """添加数据丰富化"""
        logger.info("🌟 开始数据丰富化")
        
        enriched_data = []
        for item in data:
            enriched_item = item.copy()
            # 根据ID添加额外信息
            item_id = item.get("id")
            if item_id in self.enrichment_data:
                enriched_item.update(self.enrichment_data[item_id])
            enriched_data.append(enriched_item)
        
        logger.info("✅ 数据丰富化完成")
        return self._processor.process(enriched_data)

def demo_api_middleware():
    """演示API中间件装饰器"""
    print("=== API中间件装饰器演示 ===\n")
    
    # 构建中间件链
    handler = BasicAPIHandler()
    handler = CacheMiddleware(handler)
    handler = LoggingMiddleware(handler)
    handler = RateLimitMiddleware(handler, max_requests=3)
    handler = AuthenticationMiddleware(handler)
    
    # 测试请求
    requests = [
        {"endpoint": "/api/users", "token": "valid_token"},
        {"endpoint": "/api/users", "token": "valid_token"},  # 缓存命中
        {"endpoint": "/api/posts", "token": "invalid_token"},  # 认证失败
        {"endpoint": "/api/users", "token": "valid_token"},  # 缓存命中
        {"endpoint": "/api/data", "token": "valid_token"},
        {"endpoint": "/api/more", "token": "valid_token"},  # 超出限流
    ]
    
    for i, request in enumerate(requests, 1):
        print(f"\n--- 请求 {i} ---")
        response = handler.handle_request(request)
        print(f"响应: {response}")

def demo_data_processing():
    """演示数据处理管道装饰器"""
    print("\n=== 数据处理管道装饰器演示 ===\n")
    
    # 准备测试数据
    raw_data = [
        {"id": "001", "name": "alice", "age": 25},
        {"id": "002", "name": "bob"},  # 缺少age字段
        {"name": "charlie", "age": 30},  # 缺少id字段
        {"id": "003", "name": "diana", "age": 28},
    ]
    
    # 准备丰富化数据
    enrichment_data = {
        "001": {"department": "技术部", "level": "高级"},
        "003": {"department": "销售部", "level": "中级"},
    }
    
    # 构建处理管道
    processor = BasicDataProcessor()
    processor = DataEnrichmentDecorator(processor, enrichment_data)
    processor = DataTransformDecorator(processor)
    processor = DataValidationDecorator(processor)
    
    # 处理数据
    print("原始数据:")
    for item in raw_data:
        print(f"  {item}")
    
    print("\n开始处理...")
    result = processor.process(raw_data)
    
    print("\n处理结果:")
    for item in result:
        print(f"  {item}")

def main():
    """主函数"""
    print("=== 装饰器模式实际应用示例 ===\n")
    
    # 演示API中间件
    demo_api_middleware()
    
    # 演示数据处理管道
    demo_data_processing()

if __name__ == "__main__":
    main()