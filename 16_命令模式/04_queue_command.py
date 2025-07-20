"""
04_queue_command.py - 命令队列和异步执行实现

这个示例展示了如何使用命令模式实现命令队列、异步执行和任务调度。
通过将命令放入队列中，我们可以实现延迟执行、批量处理和优先级调度。
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Callable
import time
import threading
from queue import Queue, PriorityQueue
from enum import Enum
import uuid


# ==================== 命令优先级枚举 ====================
class Priority(Enum):
    """命令优先级"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


# ==================== 基础命令接口 ====================
class AsyncCommand(ABC):
    """异步命令接口"""
    
    def __init__(self, priority: Priority = Priority.NORMAL):
        self.id = str(uuid.uuid4())[:8]
        self.priority = priority
        self.created_at = time.time()
        self.executed_at: Optional[float] = None
        self.execution_time: Optional[float] = None
        self.status = "pending"  # pending, executing, completed, failed
        self.result: Optional[str] = None
        self.error: Optional[str] = None
    
    @abstractmethod
    def execute(self) -> str:
        """执行命令"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass
    
    def __lt__(self, other):
        """用于优先级队列排序"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at


# ==================== 接收者：任务处理器 ====================
class EmailService:
    """邮件服务"""
    
    def __init__(self):
        self.sent_emails = []
    
    def send_email(self, to: str, subject: str, body: str) -> str:
        """发送邮件"""
        # 模拟邮件发送延迟
        time.sleep(0.5)
        
        email = {
            'to': to,
            'subject': subject,
            'body': body,
            'sent_at': time.time()
        }
        self.sent_emails.append(email)
        return f"邮件已发送至 {to}: {subject}"


class FileProcessor:
    """文件处理器"""
    
    def __init__(self):
        self.processed_files = []
    
    def process_file(self, filename: str, operation: str) -> str:
        """处理文件"""
        # 模拟文件处理延迟
        time.sleep(1.0)
        
        file_info = {
            'filename': filename,
            'operation': operation,
            'processed_at': time.time()
        }
        self.processed_files.append(file_info)
        return f"文件 {filename} 已完成 {operation} 操作"


class DatabaseService:
    """数据库服务"""
    
    def __init__(self):
        self.operations = []
    
    def backup_database(self, database_name: str) -> str:
        """备份数据库"""
        # 模拟数据库备份延迟
        time.sleep(2.0)
        
        operation = {
            'type': 'backup',
            'database': database_name,
            'completed_at': time.time()
        }
        self.operations.append(operation)
        return f"数据库 {database_name} 备份完成"


# ==================== 具体命令实现 ====================
class SendEmailCommand(AsyncCommand):
    """发送邮件命令"""
    
    def __init__(self, email_service: EmailService, to: str, subject: str, body: str, priority: Priority = Priority.NORMAL):
        super().__init__(priority)
        self.email_service = email_service
        self.to = to
        self.subject = subject
        self.body = body
    
    def execute(self) -> str:
        self.status = "executing"
        self.executed_at = time.time()
        
        try:
            start_time = time.time()
            result = self.email_service.send_email(self.to, self.subject, self.body)
            self.execution_time = time.time() - start_time
            self.status = "completed"
            self.result = result
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
    
    def get_description(self) -> str:
        return f"发送邮件至 {self.to}: {self.subject}"


class ProcessFileCommand(AsyncCommand):
    """文件处理命令"""
    
    def __init__(self, file_processor: FileProcessor, filename: str, operation: str, priority: Priority = Priority.NORMAL):
        super().__init__(priority)
        self.file_processor = file_processor
        self.filename = filename
        self.operation = operation
    
    def execute(self) -> str:
        self.status = "executing"
        self.executed_at = time.time()
        
        try:
            start_time = time.time()
            result = self.file_processor.process_file(self.filename, self.operation)
            self.execution_time = time.time() - start_time
            self.status = "completed"
            self.result = result
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
    
    def get_description(self) -> str:
        return f"处理文件 {self.filename}: {self.operation}"


class BackupDatabaseCommand(AsyncCommand):
    """数据库备份命令"""
    
    def __init__(self, db_service: DatabaseService, database_name: str, priority: Priority = Priority.HIGH):
        super().__init__(priority)
        self.db_service = db_service
        self.database_name = database_name
    
    def execute(self) -> str:
        self.status = "executing"
        self.executed_at = time.time()
        
        try:
            start_time = time.time()
            result = self.db_service.backup_database(self.database_name)
            self.execution_time = time.time() - start_time
            self.status = "completed"
            self.result = result
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
    
    def get_description(self) -> str:
        return f"备份数据库: {self.database_name}"


# ==================== 命令队列处理器 ====================
class CommandQueueProcessor:
    """命令队列处理器"""
    
    def __init__(self, max_workers: int = 3):
        self.command_queue = PriorityQueue()
        self.completed_commands: List[AsyncCommand] = []
        self.failed_commands: List[AsyncCommand] = []
        self.max_workers = max_workers
        self.workers: List[threading.Thread] = []
        self.running = False
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'total_execution_time': 0.0
        }
    
    def add_command(self, command: AsyncCommand):
        """添加命令到队列"""
        self.command_queue.put(command)
        print(f"命令已添加到队列: {command.get_description()} (优先级: {command.priority.name})")
    
    def start_processing(self):
        """开始处理命令队列"""
        if self.running:
            print("队列处理器已在运行")
            return
        
        self.running = True
        print(f"启动 {self.max_workers} 个工作线程处理命令队列")
        
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def stop_processing(self):
        """停止处理命令队列"""
        self.running = False
        print("正在停止命令队列处理器...")
        
        for worker in self.workers:
            worker.join(timeout=1.0)
        
        self.workers.clear()
        print("命令队列处理器已停止")
    
    def _worker_loop(self, worker_id: int):
        """工作线程循环"""
        while self.running:
            try:
                # 从队列获取命令（超时1秒）
                command = self.command_queue.get(timeout=1.0)
                
                print(f"工作线程 {worker_id} 开始执行: {command.get_description()}")
                
                try:
                    result = command.execute()
                    self.completed_commands.append(command)
                    self.stats['successful'] += 1
                    print(f"工作线程 {worker_id} 完成: {result}")
                    
                except Exception as e:
                    command.status = "failed"
                    command.error = str(e)
                    self.failed_commands.append(command)
                    self.stats['failed'] += 1
                    print(f"工作线程 {worker_id} 失败: {command.get_description()} - {str(e)}")
                
                finally:
                    self.stats['total_processed'] += 1
                    if command.execution_time:
                        self.stats['total_execution_time'] += command.execution_time
                    self.command_queue.task_done()
                
            except:
                # 队列为空或超时，继续循环
                continue
    
    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.command_queue.qsize()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def get_completed_commands(self) -> List[AsyncCommand]:
        """获取已完成的命令"""
        return self.completed_commands.copy()
    
    def get_failed_commands(self) -> List[AsyncCommand]:
        """获取失败的命令"""
        return self.failed_commands.copy()


# ==================== 任务调度器 ====================
class TaskScheduler:
    """任务调度器 - 支持定时和延迟执行"""
    
    def __init__(self, processor: CommandQueueProcessor):
        self.processor = processor
        self.scheduled_tasks: List[dict] = []
        self.scheduler_thread: Optional[threading.Thread] = None
        self.running = False
    
    def schedule_command(self, command: AsyncCommand, delay_seconds: float):
        """调度命令在指定延迟后执行"""
        execute_at = time.time() + delay_seconds
        task = {
            'command': command,
            'execute_at': execute_at,
            'scheduled_at': time.time()
        }
        self.scheduled_tasks.append(task)
        print(f"命令已调度，将在 {delay_seconds} 秒后执行: {command.get_description()}")
    
    def start_scheduler(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        print("任务调度器已启动")
    
    def stop_scheduler(self):
        """停止调度器"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=1.0)
        print("任务调度器已停止")
    
    def _scheduler_loop(self):
        """调度器循环"""
        while self.running:
            current_time = time.time()
            ready_tasks = []
            
            # 找出准备执行的任务
            for task in self.scheduled_tasks[:]:
                if task['execute_at'] <= current_time:
                    ready_tasks.append(task)
                    self.scheduled_tasks.remove(task)
            
            # 将准备好的任务添加到处理队列
            for task in ready_tasks:
                self.processor.add_command(task['command'])
                print(f"调度任务已添加到执行队列: {task['command'].get_description()}")
            
            time.sleep(0.1)  # 检查间隔
    
    def get_pending_tasks_count(self) -> int:
        """获取待调度任务数量"""
        return len(self.scheduled_tasks)


# ==================== 演示函数 ====================
def demonstrate_command_queue():
    """演示命令队列功能"""
    print("=" * 60)
    print("命令队列和异步执行演示")
    print("=" * 60)
    
    # 创建服务
    email_service = EmailService()
    file_processor = FileProcessor()
    db_service = DatabaseService()
    
    # 创建队列处理器
    processor = CommandQueueProcessor(max_workers=2)
    processor.start_processing()
    
    print("1. 添加不同优先级的命令到队列:")
    
    # 添加各种优先级的命令
    commands = [
        SendEmailCommand(email_service, "user1@example.com", "普通邮件", "这是一封普通邮件", Priority.NORMAL),
        BackupDatabaseCommand(db_service, "production_db", Priority.HIGH),
        ProcessFileCommand(file_processor, "data.csv", "数据清洗", Priority.LOW),
        SendEmailCommand(email_service, "admin@example.com", "紧急通知", "系统出现问题", Priority.URGENT),
        ProcessFileCommand(file_processor, "report.pdf", "生成报告", Priority.NORMAL),
        BackupDatabaseCommand(db_service, "backup_db", Priority.HIGH)
    ]
    
    for cmd in commands:
        processor.add_command(cmd)
        time.sleep(0.1)  # 稍微延迟以观察优先级效果
    
    print(f"\n2. 队列大小: {processor.get_queue_size()}")
    
    # 等待所有命令执行完成
    print("\n3. 等待命令执行完成...")
    while processor.get_queue_size() > 0 or processor.stats['total_processed'] < len(commands):
        time.sleep(0.5)
        print(f"   队列剩余: {processor.get_queue_size()}, 已处理: {processor.stats['total_processed']}")
    
    processor.stop_processing()
    
    print("\n4. 执行统计:")
    stats = processor.get_stats()
    print(f"   总处理数: {stats['total_processed']}")
    print(f"   成功数: {stats['successful']}")
    print(f"   失败数: {stats['failed']}")
    print(f"   总执行时间: {stats['total_execution_time']:.2f} 秒")
    
    print("\n5. 已完成的命令:")
    for cmd in processor.get_completed_commands():
        print(f"   {cmd.get_description()} - 执行时间: {cmd.execution_time:.2f}s")


def demonstrate_task_scheduler():
    """演示任务调度功能"""
    print("\n" + "=" * 60)
    print("任务调度器演示")
    print("=" * 60)
    
    # 创建服务和处理器
    email_service = EmailService()
    processor = CommandQueueProcessor(max_workers=1)
    scheduler = TaskScheduler(processor)
    
    processor.start_processing()
    scheduler.start_scheduler()
    
    print("1. 调度延迟执行的任务:")
    
    # 调度不同延迟的任务
    scheduler.schedule_command(
        SendEmailCommand(email_service, "user@example.com", "立即执行", "这个任务立即执行"),
        0.5
    )
    
    scheduler.schedule_command(
        SendEmailCommand(email_service, "user@example.com", "2秒后执行", "这个任务2秒后执行"),
        2.0
    )
    
    scheduler.schedule_command(
        SendEmailCommand(email_service, "user@example.com", "4秒后执行", "这个任务4秒后执行"),
        4.0
    )
    
    print(f"\n2. 待调度任务数: {scheduler.get_pending_tasks_count()}")
    
    # 等待所有任务完成
    print("\n3. 等待调度任务执行...")
    start_time = time.time()
    while scheduler.get_pending_tasks_count() > 0 or processor.get_queue_size() > 0:
        elapsed = time.time() - start_time
        print(f"   已等待 {elapsed:.1f}s, 待调度: {scheduler.get_pending_tasks_count()}, 队列: {processor.get_queue_size()}")
        time.sleep(0.5)
    
    # 等待最后的任务完成
    time.sleep(1.0)
    
    scheduler.stop_scheduler()
    processor.stop_processing()
    
    print("\n4. 调度完成，所有任务已执行")
    print(f"   发送的邮件数量: {len(email_service.sent_emails)}")


if __name__ == "__main__":
    demonstrate_command_queue()
    demonstrate_task_scheduler()
