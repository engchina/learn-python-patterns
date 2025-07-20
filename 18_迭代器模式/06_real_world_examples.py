#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
迭代器模式的实际应用场景

本模块演示了迭代器在实际项目中的应用，包括：
1. 网络爬虫数据迭代 - 分页API数据获取
2. 日志文件分析 - 大文件逐行处理
3. 数据库结果集迭代 - 批量数据处理
4. 配置文件解析 - 结构化数据读取

作者: Assistant
日期: 2024-01-20
"""

import json
import re
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Iterator, Generator
from urllib.parse import urljoin
import requests
from dataclasses import dataclass


@dataclass
class LogEntry:
    """日志条目数据类"""
    timestamp: datetime
    level: str
    message: str
    source: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level,
            'message': self.message,
            'source': self.source,
            'user_id': self.user_id,
            'ip_address': self.ip_address
        }


class WebCrawlerIterator:
    """网络爬虫迭代器 - 模拟分页API数据获取"""
    
    def __init__(self, base_url: str, total_pages: int = 5, page_size: int = 10):
        self.base_url = base_url
        self.total_pages = total_pages
        self.page_size = page_size
        self.current_page = 0
        self.items_fetched = 0
        self.session = self._create_session()
    
    def _create_session(self):
        """创建HTTP会话（模拟）"""
        # 在实际应用中，这里会创建真实的requests.Session
        return {"connected": True, "retry_count": 0}
    
    def _fetch_page(self, page: int) -> List[Dict[str, Any]]:
        """获取指定页面的数据（模拟）"""
        # 模拟网络延迟
        time.sleep(0.1)
        
        # 模拟API响应
        items = []
        start_id = page * self.page_size + 1
        
        for i in range(self.page_size):
            item_id = start_id + i
            items.append({
                'id': item_id,
                'title': f'文章标题_{item_id}',
                'content': f'这是第{item_id}篇文章的内容...',
                'author': f'作者_{item_id % 5 + 1}',
                'created_at': (datetime.now() - timedelta(days=item_id)).isoformat(),
                'tags': [f'标签{item_id % 3 + 1}', f'标签{item_id % 4 + 1}'],
                'view_count': random.randint(100, 10000)
            })
        
        print(f"🌐 获取第 {page + 1} 页数据，{len(items)} 条记录")
        return items
    
    def __iter__(self) -> 'WebCrawlerIterator':
        """重置迭代器状态"""
        self.current_page = 0
        self.items_fetched = 0
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """返回下一个数据项"""
        if self.current_page >= self.total_pages:
            print(f"🕷️ 爬虫完成，共获取 {self.items_fetched} 条数据")
            raise StopIteration
        
        # 如果当前页面没有数据，获取下一页
        if not hasattr(self, '_current_page_data') or not self._current_page_data:
            try:
                self._current_page_data = self._fetch_page(self.current_page)
                self.current_page += 1
            except Exception as e:
                print(f"❌ 获取数据失败: {e}")
                raise StopIteration
        
        # 返回当前页面的下一个项目
        if self._current_page_data:
            item = self._current_page_data.pop(0)
            self.items_fetched += 1
            return item
        else:
            raise StopIteration


class LogFileIterator:
    """日志文件迭代器 - 逐行解析日志文件"""
    
    def __init__(self, log_pattern: str = None):
        self.log_pattern = log_pattern or self._default_log_pattern()
        self.parsed_count = 0
        self.error_count = 0
    
    def _default_log_pattern(self) -> str:
        """默认日志格式正则表达式"""
        # 匹配格式: 2024-01-20 10:30:45 [INFO] source: message (user:123, ip:192.168.1.1)
        return (
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+'
            r'\[(?P<level>\w+)\]\s+'
            r'(?P<source>\w+):\s+'
            r'(?P<message>.*?)'
            r'(?:\s+\(user:(?P<user_id>\w+),\s+ip:(?P<ip_address>[\d.]+)\))?'
        )
    
    def parse_log_line(self, line: str) -> Optional[LogEntry]:
        """解析单行日志"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        match = re.match(self.log_pattern, line)
        if match:
            try:
                timestamp = datetime.strptime(match.group('timestamp'), '%Y-%m-%d %H:%M:%S')
                return LogEntry(
                    timestamp=timestamp,
                    level=match.group('level'),
                    message=match.group('message'),
                    source=match.group('source'),
                    user_id=match.group('user_id'),
                    ip_address=match.group('ip_address')
                )
            except ValueError as e:
                self.error_count += 1
                print(f"⚠️ 解析时间戳失败: {e}")
                return None
        else:
            self.error_count += 1
            return None
    
    def process_file(self, filename: str) -> Generator[LogEntry, None, None]:
        """处理日志文件"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    log_entry = self.parse_log_line(line)
                    if log_entry:
                        self.parsed_count += 1
                        yield log_entry
                    
                    # 每处理1000行显示进度
                    if line_num % 1000 == 0:
                        print(f"📊 已处理 {line_num} 行，解析成功 {self.parsed_count} 条")
        
        except FileNotFoundError:
            print(f"❌ 文件不存在: {filename}")
        except Exception as e:
            print(f"❌ 处理文件失败: {e}")
        finally:
            print(f"📋 处理完成: 成功 {self.parsed_count} 条，错误 {self.error_count} 条")


class DatabaseBatchIterator:
    """数据库批量迭代器 - 模拟大数据集的批量处理"""
    
    def __init__(self, table_name: str, batch_size: int = 1000, where_clause: str = ""):
        self.table_name = table_name
        self.batch_size = batch_size
        self.where_clause = where_clause
        self.offset = 0
        self.total_processed = 0
        self.connection = self._mock_connection()
    
    def _mock_connection(self) -> Dict[str, Any]:
        """模拟数据库连接"""
        return {
            'connected': True,
            'total_records': 10000,  # 模拟总记录数
            'query_count': 0
        }
    
    def _execute_query(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """执行查询（模拟）"""
        if not self.connection['connected']:
            raise Exception("数据库连接已断开")
        
        # 模拟查询延迟
        time.sleep(0.05)
        
        self.connection['query_count'] += 1
        
        # 计算实际返回的记录数
        remaining = self.connection['total_records'] - offset
        actual_limit = min(limit, remaining)
        
        if actual_limit <= 0:
            return []
        
        # 生成模拟数据
        records = []
        for i in range(actual_limit):
            record_id = offset + i + 1
            records.append({
                'id': record_id,
                'name': f'用户_{record_id}',
                'email': f'user{record_id}@example.com',
                'age': 20 + (record_id % 50),
                'department': f'部门_{record_id % 10 + 1}',
                'salary': 50000 + (record_id % 100) * 1000,
                'created_at': (datetime.now() - timedelta(days=record_id)).isoformat()
            })
        
        print(f"🗄️ 执行查询 #{self.connection['query_count']}: 偏移 {offset}, 获取 {len(records)} 条记录")
        return records
    
    def __iter__(self) -> 'DatabaseBatchIterator':
        """重置迭代器状态"""
        self.offset = 0
        self.total_processed = 0
        return self
    
    def __next__(self) -> List[Dict[str, Any]]:
        """返回下一批数据"""
        batch = self._execute_query(self.offset, self.batch_size)
        
        if not batch:
            print(f"📊 数据库迭代完成，共处理 {self.total_processed} 条记录")
            raise StopIteration
        
        self.offset += len(batch)
        self.total_processed += len(batch)
        
        return batch
    
    def close(self) -> None:
        """关闭数据库连接"""
        self.connection['connected'] = False
        print(f"🔌 数据库连接已关闭，共执行 {self.connection['query_count']} 次查询")


class ConfigFileIterator:
    """配置文件迭代器 - 解析结构化配置"""
    
    def __init__(self, config_format: str = 'json'):
        self.config_format = config_format.lower()
        self.sections_processed = 0
    
    def parse_json_config(self, content: str) -> Generator[Dict[str, Any], None, None]:
        """解析JSON配置"""
        try:
            config = json.loads(content)
            for section_name, section_data in config.items():
                self.sections_processed += 1
                yield {
                    'section': section_name,
                    'type': 'json',
                    'data': section_data,
                    'keys': list(section_data.keys()) if isinstance(section_data, dict) else []
                }
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
    
    def parse_ini_config(self, content: str) -> Generator[Dict[str, Any], None, None]:
        """解析INI配置"""
        current_section = None
        section_data = {}
        
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            
            # 检查是否是节标题
            if line.startswith('[') and line.endswith(']'):
                # 如果有之前的节，先返回
                if current_section:
                    self.sections_processed += 1
                    yield {
                        'section': current_section,
                        'type': 'ini',
                        'data': section_data.copy(),
                        'keys': list(section_data.keys())
                    }
                
                # 开始新节
                current_section = line[1:-1]
                section_data = {}
            
            # 检查是否是键值对
            elif '=' in line and current_section:
                key, value = line.split('=', 1)
                section_data[key.strip()] = value.strip()
        
        # 处理最后一个节
        if current_section:
            self.sections_processed += 1
            yield {
                'section': current_section,
                'type': 'ini',
                'data': section_data,
                'keys': list(section_data.keys())
            }
    
    def process_config(self, content: str) -> Generator[Dict[str, Any], None, None]:
        """处理配置文件内容"""
        if self.config_format == 'json':
            yield from self.parse_json_config(content)
        elif self.config_format == 'ini':
            yield from self.parse_ini_config(content)
        else:
            print(f"❌ 不支持的配置格式: {self.config_format}")


def create_sample_log_file():
    """创建示例日志文件"""
    log_entries = [
        "2024-01-20 10:30:45 [INFO] auth: 用户登录成功 (user:user123, ip:192.168.1.100)",
        "2024-01-20 10:31:02 [DEBUG] database: 执行查询: SELECT * FROM users",
        "2024-01-20 10:31:15 [WARN] cache: 缓存命中率低于阈值",
        "2024-01-20 10:31:30 [ERROR] payment: 支付处理失败 (user:user456, ip:192.168.1.101)",
        "2024-01-20 10:31:45 [INFO] api: API调用成功 /api/v1/users",
        "# 这是注释行",
        "2024-01-20 10:32:00 [INFO] auth: 用户退出 (user:user123, ip:192.168.1.100)",
        "无效的日志行",
        "2024-01-20 10:32:15 [CRITICAL] system: 系统内存不足",
    ]
    
    with open('23. Iterator/sample.log', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_entries))
    print("📝 已创建示例日志文件: sample.log")


def demo_web_crawler():
    """演示网络爬虫迭代器"""
    print("=" * 50)
    print("🕷️ 网络爬虫迭代器演示")
    print("=" * 50)
    
    # 创建爬虫迭代器
    crawler = WebCrawlerIterator("https://api.example.com/articles", total_pages=3, page_size=5)
    
    print("开始爬取数据...")
    articles = []
    
    for article in crawler:
        articles.append(article)
        print(f"  📄 {article['title']} (作者: {article['author']}, 浏览: {article['view_count']})")
        
        # 只显示前几条
        if len(articles) >= 8:
            print("  ... (省略更多数据)")
            break
    
    print(f"\n📊 爬取统计: 共获取 {len(articles)} 篇文章")


def demo_log_analysis():
    """演示日志文件分析"""
    print("\n" + "=" * 50)
    print("📋 日志文件分析演示")
    print("=" * 50)
    
    # 创建示例日志文件
    create_sample_log_file()
    
    # 创建日志迭代器
    log_parser = LogFileIterator()
    
    print("开始分析日志文件...")
    log_stats = {'INFO': 0, 'DEBUG': 0, 'WARN': 0, 'ERROR': 0, 'CRITICAL': 0}
    user_activities = {}
    
    for log_entry in log_parser.process_file('23. Iterator/sample.log'):
        # 统计日志级别
        log_stats[log_entry.level] = log_stats.get(log_entry.level, 0) + 1
        
        # 统计用户活动
        if log_entry.user_id:
            if log_entry.user_id not in user_activities:
                user_activities[log_entry.user_id] = []
            user_activities[log_entry.user_id].append(log_entry.message)
        
        print(f"  📝 [{log_entry.level}] {log_entry.timestamp.strftime('%H:%M:%S')} - {log_entry.message}")
    
    print(f"\n📊 日志统计:")
    for level, count in log_stats.items():
        if count > 0:
            print(f"  {level}: {count} 条")
    
    print(f"\n👥 用户活动:")
    for user_id, activities in user_activities.items():
        print(f"  {user_id}: {len(activities)} 次活动")


def demo_database_processing():
    """演示数据库批量处理"""
    print("\n" + "=" * 50)
    print("🗄️ 数据库批量处理演示")
    print("=" * 50)
    
    # 创建数据库迭代器
    db_iter = DatabaseBatchIterator("users", batch_size=500)
    
    print("开始批量处理数据库记录...")
    
    department_stats = {}
    salary_sum = 0
    record_count = 0
    
    try:
        for batch in db_iter:
            # 处理当前批次
            for record in batch:
                # 统计部门
                dept = record['department']
                department_stats[dept] = department_stats.get(dept, 0) + 1
                
                # 累计薪资
                salary_sum += record['salary']
                record_count += 1
            
            print(f"  📦 处理批次: {len(batch)} 条记录")
            
            # 只处理前几批，避免输出过多
            if record_count >= 2000:
                print("  ... (省略更多批次)")
                break
    
    finally:
        db_iter.close()
    
    print(f"\n📊 处理统计:")
    print(f"  总记录数: {record_count}")
    print(f"  平均薪资: {salary_sum / record_count:.2f}" if record_count > 0 else "  平均薪资: 0")
    print(f"  部门分布: {dict(list(department_stats.items())[:5])}")


def demo_config_parsing():
    """演示配置文件解析"""
    print("\n" + "=" * 50)
    print("⚙️ 配置文件解析演示")
    print("=" * 50)
    
    # JSON配置示例
    json_config = """
    {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp",
            "user": "admin"
        },
        "cache": {
            "type": "redis",
            "host": "localhost",
            "port": 6379,
            "ttl": 3600
        },
        "logging": {
            "level": "INFO",
            "file": "/var/log/app.log",
            "max_size": "100MB"
        }
    }
    """
    
    print("解析JSON配置:")
    json_parser = ConfigFileIterator('json')
    for section in json_parser.process_config(json_config):
        print(f"  📁 [{section['section']}] - {len(section['keys'])} 个配置项")
        for key in section['keys']:
            print(f"    {key}: {section['data'][key]}")
    
    # INI配置示例
    ini_config = """
    [database]
    host = localhost
    port = 5432
    name = myapp
    user = admin
    
    [cache]
    type = redis
    host = localhost
    port = 6379
    ttl = 3600
    
    # 日志配置
    [logging]
    level = INFO
    file = /var/log/app.log
    max_size = 100MB
    """
    
    print(f"\n解析INI配置:")
    ini_parser = ConfigFileIterator('ini')
    for section in ini_parser.process_config(ini_config):
        print(f"  📁 [{section['section']}] - {len(section['keys'])} 个配置项")
        for key in section['keys']:
            print(f"    {key}: {section['data'][key]}")


if __name__ == "__main__":
    print("🎯 迭代器模式实际应用演示")
    
    # 运行所有演示
    demo_web_crawler()
    demo_log_analysis()
    demo_database_processing()
    demo_config_parsing()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 这些示例展示了迭代器在实际项目中的强大应用")
    print("=" * 50)
