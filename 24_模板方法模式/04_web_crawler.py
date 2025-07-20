"""
04_web_crawler.py - 网络爬虫系统的模板方法设计

这个示例展示了在网络爬虫系统中如何使用模板方法模式：
- 统一的爬虫处理流程
- 不同网站的具体爬取策略
- 灵活的数据处理和存储机制
- 错误处理和重试机制
"""

from abc import ABC, abstractmethod
import time
import random
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import json


# ==================== 抽象网络爬虫 ====================
class WebCrawler(ABC):
    """网络爬虫模板类
    
    定义了网络爬虫的标准流程：
    1. 初始化爬虫配置
    2. 获取目标URL列表
    3. 爬取网页内容
    4. 解析和提取数据
    5. 数据清洗和验证
    6. 保存数据
    7. 清理资源
    """
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.crawled_urls = set()
        self.failed_urls = set()
        self.extracted_data = []
        self.start_time = None
        self.request_count = 0
        self.success_count = 0
    
    def crawl(self, max_pages: int = 10) -> Dict[str, Any]:
        """模板方法 - 定义完整的爬虫流程"""
        print(f"🕷️  开始爬虫任务: {self.name}")
        print(f"目标网站: {self.base_url}")
        print("-" * 60)
        
        self.start_time = time.time()
        
        try:
            # 1. 初始化爬虫配置
            print("⚙️  步骤1: 初始化爬虫配置")
            self.initialize_crawler()
            print("✅ 爬虫配置完成")
            
            # 2. 获取目标URL列表
            print("\n🔗 步骤2: 获取目标URL列表")
            target_urls = self.get_target_urls(max_pages)
            print(f"✅ 获得 {len(target_urls)} 个目标URL")
            
            # 3. 爬取网页内容
            print("\n📥 步骤3: 爬取网页内容")
            for i, url in enumerate(target_urls, 1):
                print(f"正在爬取 ({i}/{len(target_urls)}): {url}")
                
                if self.should_crawl_url(url):
                    page_content = self.fetch_page_content(url)
                    if page_content:
                        # 4. 解析和提取数据
                        extracted_items = self.extract_data(url, page_content)
                        if extracted_items:
                            # 5. 数据清洗和验证
                            cleaned_items = self.clean_and_validate_data(extracted_items)
                            self.extracted_data.extend(cleaned_items)
                            self.success_count += 1
                            print(f"✅ 成功提取 {len(cleaned_items)} 条数据")
                        else:
                            print("⚠️  未提取到有效数据")
                    else:
                        self.failed_urls.add(url)
                        print("❌ 页面获取失败")
                else:
                    print("⏭️  跳过此URL")
                
                self.crawled_urls.add(url)
                
                # 延迟请求，避免过于频繁
                if self.should_delay():
                    delay = self.get_request_delay()
                    print(f"⏱️  延迟 {delay} 秒...")
                    time.sleep(delay)
            
            # 6. 保存数据
            print(f"\n💾 步骤4: 保存数据")
            if self.extracted_data:
                self.save_data(self.extracted_data)
                print(f"✅ 保存了 {len(self.extracted_data)} 条数据")
            else:
                print("⚠️  没有数据需要保存")
            
            # 7. 清理资源
            print("\n🧹 步骤5: 清理资源")
            self.cleanup_crawler()
            
            # 生成爬虫报告
            report = self.generate_crawl_report()
            
            print("-" * 60)
            print("🎉 爬虫任务完成!")
            return report
            
        except Exception as e:
            print(f"❌ 爬虫任务失败: {str(e)}")
            return {"status": "failed", "error": str(e)}
    
    # 抽象方法 - 子类必须实现
    @abstractmethod
    def get_target_urls(self, max_pages: int) -> List[str]:
        """获取目标URL列表"""
        pass
    
    @abstractmethod
    def extract_data(self, url: str, content: str) -> List[Dict[str, Any]]:
        """从页面内容中提取数据"""
        pass
    
    # 具体方法 - 提供默认实现
    def initialize_crawler(self):
        """初始化爬虫配置 - 默认实现"""
        print("设置请求头...")
        print("配置代理设置...")
        print("初始化会话...")
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """获取页面内容 - 模拟实现"""
        self.request_count += 1
        
        # 模拟网络请求
        print(f"发送HTTP请求到: {url}")
        
        # 模拟请求可能失败
        if random.random() < 0.1:  # 10%失败率
            print("❌ 网络请求失败")
            return None
        
        # 模拟页面内容
        mock_content = f"""
        <html>
            <head><title>页面标题 - {url}</title></head>
            <body>
                <h1>这是来自 {url} 的内容</h1>
                <div class="content">
                    <p>这是一些示例内容...</p>
                    <span class="price">¥{random.randint(10, 1000)}</span>
                    <div class="description">产品描述信息</div>
                </div>
            </body>
        </html>
        """
        
        print("✅ 页面内容获取成功")
        return mock_content
    
    def clean_and_validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """数据清洗和验证 - 默认实现"""
        cleaned_data = []
        for item in data:
            # 移除空值和无效数据
            cleaned_item = {k: v for k, v in item.items() if v and str(v).strip()}
            if cleaned_item:
                cleaned_data.append(cleaned_item)
        
        print(f"数据清洗: {len(data)} -> {len(cleaned_data)}")
        return cleaned_data
    
    def save_data(self, data: List[Dict[str, Any]]):
        """保存数据 - 默认实现"""
        filename = f"{self.name.replace(' ', '_')}_data.json"
        print(f"保存数据到文件: {filename}")
        
        # 模拟保存过程
        print(f"写入 {len(data)} 条记录")
        if data:
            print(f"样例数据: {json.dumps(data[0], ensure_ascii=False, indent=2)}")
    
    def cleanup_crawler(self):
        """清理爬虫资源 - 默认实现"""
        print("关闭网络连接...")
        print("清理临时文件...")
    
    def generate_crawl_report(self) -> Dict[str, Any]:
        """生成爬虫报告"""
        end_time = time.time()
        duration = round(end_time - self.start_time, 2)
        
        report = {
            "crawler_name": self.name,
            "base_url": self.base_url,
            "total_requests": self.request_count,
            "successful_pages": self.success_count,
            "failed_pages": len(self.failed_urls),
            "extracted_items": len(self.extracted_data),
            "duration_seconds": duration,
            "success_rate": round(self.success_count / max(self.request_count, 1) * 100, 1),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"爬虫名称: {report['crawler_name']}")
        print(f"总请求数: {report['total_requests']}")
        print(f"成功页面: {report['successful_pages']}")
        print(f"失败页面: {report['failed_pages']}")
        print(f"提取数据: {report['extracted_items']} 条")
        print(f"成功率: {report['success_rate']}%")
        print(f"总耗时: {report['duration_seconds']} 秒")
        
        return report
    
    # 钩子方法 - 子类可选择重写
    def should_crawl_url(self, url: str) -> bool:
        """是否应该爬取此URL"""
        return url not in self.crawled_urls
    
    def should_delay(self) -> bool:
        """是否需要延迟请求"""
        return True
    
    def get_request_delay(self) -> float:
        """获取请求延迟时间"""
        return random.uniform(0.5, 2.0)


# ==================== 具体爬虫实现 ====================
class EcommerceCrawler(WebCrawler):
    """电商网站爬虫"""
    
    def __init__(self):
        super().__init__("电商产品爬虫", "https://example-shop.com")
    
    def get_target_urls(self, max_pages: int) -> List[str]:
        """获取电商产品页面URL"""
        print("生成产品页面URL...")
        
        # 模拟生成产品页面URL
        urls = []
        for i in range(1, min(max_pages + 1, 11)):
            urls.append(f"{self.base_url}/products/page/{i}")
            urls.append(f"{self.base_url}/category/electronics/page/{i}")
        
        return urls[:max_pages]
    
    def extract_data(self, url: str, content: str) -> List[Dict[str, Any]]:
        """提取产品信息"""
        print("解析产品信息...")
        
        # 模拟从HTML中提取产品数据
        products = []
        for i in range(random.randint(1, 5)):
            product = {
                "name": f"产品 {random.randint(1000, 9999)}",
                "price": random.randint(50, 2000),
                "category": random.choice(["电子产品", "服装", "家居", "图书"]),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "stock": random.randint(0, 100),
                "url": url,
                "crawl_time": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            products.append(product)
        
        return products
    
    def clean_and_validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """电商数据特殊清洗"""
        cleaned_data = super().clean_and_validate_data(data)
        
        # 过滤掉无库存或价格异常的产品
        valid_products = []
        for product in cleaned_data:
            if (product.get('stock', 0) > 0 and 
                product.get('price', 0) > 0 and
                product.get('rating', 0) >= 3.0):
                valid_products.append(product)
        
        print(f"电商数据验证: {len(cleaned_data)} -> {len(valid_products)}")
        return valid_products
    
    def get_request_delay(self) -> float:
        """电商网站需要更长延迟"""
        return random.uniform(1.0, 3.0)


class NewsCrawler(WebCrawler):
    """新闻网站爬虫"""
    
    def __init__(self):
        super().__init__("新闻文章爬虫", "https://example-news.com")
    
    def get_target_urls(self, max_pages: int) -> List[str]:
        """获取新闻文章URL"""
        print("生成新闻文章URL...")
        
        # 模拟生成新闻页面URL
        urls = []
        categories = ["tech", "business", "sports", "entertainment"]
        
        for category in categories:
            for i in range(1, max_pages // len(categories) + 2):
                urls.append(f"{self.base_url}/{category}/page/{i}")
        
        return urls[:max_pages]
    
    def extract_data(self, url: str, content: str) -> List[Dict[str, Any]]:
        """提取新闻信息"""
        print("解析新闻文章...")
        
        # 模拟从HTML中提取新闻数据
        articles = []
        for i in range(random.randint(2, 8)):
            article = {
                "title": f"新闻标题 {random.randint(1000, 9999)}",
                "author": random.choice(["张记者", "李编辑", "王通讯员", "赵主编"]),
                "publish_date": time.strftime('%Y-%m-%d'),
                "category": random.choice(["科技", "财经", "体育", "娱乐"]),
                "summary": f"这是一篇关于...的新闻摘要 {random.randint(100, 999)}",
                "word_count": random.randint(500, 3000),
                "url": url,
                "crawl_time": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            articles.append(article)
        
        return articles
    
    def should_delay(self) -> bool:
        """新闻网站可以更频繁地请求"""
        return random.random() < 0.7  # 70%概率延迟
    
    def get_request_delay(self) -> float:
        """新闻网站延迟较短"""
        return random.uniform(0.3, 1.5)


class SocialMediaCrawler(WebCrawler):
    """社交媒体爬虫"""
    
    def __init__(self):
        super().__init__("社交媒体爬虫", "https://example-social.com")
        self.api_rate_limit = 0
    
    def initialize_crawler(self):
        """社交媒体爬虫特殊初始化"""
        super().initialize_crawler()
        print("配置API密钥...")
        print("设置OAuth认证...")
        self.api_rate_limit = 100  # 模拟API限制
    
    def get_target_urls(self, max_pages: int) -> List[str]:
        """获取社交媒体API端点"""
        print("生成API请求URL...")
        
        # 模拟API端点
        urls = []
        for i in range(max_pages):
            urls.append(f"{self.base_url}/api/posts?page={i+1}")
        
        return urls
    
    def extract_data(self, url: str, content: str) -> List[Dict[str, Any]]:
        """提取社交媒体数据"""
        print("解析社交媒体数据...")
        
        # 模拟API响应数据
        posts = []
        for i in range(random.randint(10, 20)):
            post = {
                "post_id": f"post_{random.randint(100000, 999999)}",
                "user": f"user_{random.randint(1000, 9999)}",
                "content": f"这是一条社交媒体内容 #{random.randint(1, 100)}",
                "likes": random.randint(0, 1000),
                "shares": random.randint(0, 100),
                "comments": random.randint(0, 50),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "hashtags": [f"#标签{i}" for i in range(random.randint(1, 4))],
                "url": url
            }
            posts.append(post)
        
        return posts
    
    def should_crawl_url(self, url: str) -> bool:
        """检查API限制"""
        if self.api_rate_limit <= 0:
            print("⚠️  API限制已达上限，跳过请求")
            return False
        
        self.api_rate_limit -= 1
        return super().should_crawl_url(url)
    
    def clean_and_validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """社交媒体数据特殊清洗"""
        cleaned_data = super().clean_and_validate_data(data)
        
        # 过滤掉互动量过低的帖子
        popular_posts = []
        for post in cleaned_data:
            total_engagement = post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0)
            if total_engagement >= 5:  # 至少5个互动
                popular_posts.append(post)
        
        print(f"社交媒体数据过滤: {len(cleaned_data)} -> {len(popular_posts)}")
        return popular_posts
    
    def get_request_delay(self) -> float:
        """API请求需要遵守限制"""
        return random.uniform(2.0, 4.0)


# ==================== 演示函数 ====================
def demo_web_crawlers():
    """网络爬虫演示"""
    print("=" * 80)
    print("🕷️  网络爬虫系统模板方法演示")
    print("=" * 80)
    
    # 创建不同类型的爬虫
    crawlers = [
        EcommerceCrawler(),
        NewsCrawler(),
        SocialMediaCrawler()
    ]
    
    max_pages_per_crawler = 5
    all_reports = []
    
    # 执行爬虫任务
    for crawler in crawlers:
        print(f"\n{'='*20} {crawler.name} {'='*20}")
        report = crawler.crawl(max_pages_per_crawler)
        all_reports.append(report)
        time.sleep(1)
    
    # 汇总报告
    print("\n" + "="*80)
    print("📊 爬虫任务汇总报告")
    print("="*80)
    
    total_requests = sum(r.get('total_requests', 0) for r in all_reports)
    total_items = sum(r.get('extracted_items', 0) for r in all_reports)
    total_duration = sum(r.get('duration_seconds', 0) for r in all_reports)
    avg_success_rate = sum(r.get('success_rate', 0) for r in all_reports) / len(all_reports)
    
    print(f"总爬虫数量: {len(crawlers)}")
    print(f"总请求数量: {total_requests}")
    print(f"总提取数据: {total_items} 条")
    print(f"总耗时: {round(total_duration, 2)} 秒")
    print(f"平均成功率: {round(avg_success_rate, 1)}%")
    
    print("\n📋 各爬虫详情:")
    for report in all_reports:
        print(f"  {report['crawler_name']}: {report['extracted_items']}条数据, "
              f"{report['success_rate']}%成功率")


if __name__ == "__main__":
    demo_web_crawlers()
