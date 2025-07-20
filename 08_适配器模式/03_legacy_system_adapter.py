"""
适配器模式遗留系统集成 - 数据库访问层适配器

这个示例展示了适配器模式在遗留系统改造中的应用，演示如何
在不修改遗留代码的情况下集成新的系统架构。

作者: Adapter Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import sqlite3
import json
from datetime import datetime


# ==================== 目标接口 - 现代化数据访问接口 ====================

class DataRepository(ABC):
    """现代化数据仓库接口"""
    
    @abstractmethod
    def create(self, entity: Dict[str, Any]) -> str:
        """创建实体"""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查找实体"""
        pass
    
    @abstractmethod
    def find_all(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """查找所有实体"""
        pass
    
    @abstractmethod
    def update(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """更新实体"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """删除实体"""
        pass
    
    @abstractmethod
    def get_repository_info(self) -> str:
        """获取仓库信息"""
        pass


# ==================== 被适配者 - 遗留系统 ====================

class LegacyUserDatabase:
    """遗留用户数据库系统 - 被适配者A"""
    
    def __init__(self, db_file: str = ":memory:"):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.connection.row_factory = sqlite3.Row
        self._init_database()
        self.operation_count = 0
    
    def _init_database(self):
        """初始化数据库表"""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email_address TEXT,
                full_name TEXT,
                registration_date TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        self.connection.commit()
    
    def insert_user(self, username: str, email: str, full_name: str) -> int:
        """插入用户（遗留接口）"""
        print(f"🗄️  遗留系统插入用户: {username}")
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (username, email_address, full_name, registration_date)
            VALUES (?, ?, ?, ?)
        """, (username, email, full_name, datetime.now().isoformat()))
        
        self.connection.commit()
        self.operation_count += 1
        return cursor.lastrowid
    
    def get_user_by_id(self, user_id: int) -> Optional[sqlite3.Row]:
        """根据ID获取用户（遗留接口）"""
        print(f"🗄️  遗留系统查询用户: {user_id}")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        self.operation_count += 1
        return cursor.fetchone()
    
    def get_all_users(self) -> List[sqlite3.Row]:
        """获取所有用户（遗留接口）"""
        print(f"🗄️  遗留系统查询所有用户")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE is_active = 1")
        self.operation_count += 1
        return cursor.fetchall()
    
    def update_user_info(self, user_id: int, **kwargs) -> bool:
        """更新用户信息（遗留接口）"""
        print(f"🗄️  遗留系统更新用户: {user_id}")
        
        # 构建动态更新语句
        set_clauses = []
        values = []
        
        for field, value in kwargs.items():
            if field in ['username', 'email_address', 'full_name']:
                set_clauses.append(f"{field} = ?")
                values.append(value)
        
        if not set_clauses:
            return False
        
        values.append(user_id)
        sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = ?"
        
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        self.operation_count += 1
        
        return cursor.rowcount > 0
    
    def deactivate_user(self, user_id: int) -> bool:
        """停用用户（遗留接口）"""
        print(f"🗄️  遗留系统停用用户: {user_id}")
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,))
        self.connection.commit()
        self.operation_count += 1
        return cursor.rowcount > 0
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息（遗留接口）"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN is_active = 1 THEN 1 END) as active FROM users")
        stats = cursor.fetchone()
        
        return {
            "total_users": stats["total"],
            "active_users": stats["active"],
            "operations_performed": self.operation_count,
            "database_file": self.db_file
        }


class LegacyProductCatalog:
    """遗留产品目录系统 - 被适配者B"""
    
    def __init__(self):
        self.products = {}
        self.next_id = 1
        self.operation_count = 0
    
    def add_product(self, product_code: str, product_name: str, 
                   price: float, category: str) -> str:
        """添加产品（遗留接口）"""
        print(f"📦 遗留产品系统添加产品: {product_code}")
        
        product_id = f"PROD_{self.next_id:04d}"
        self.next_id += 1
        
        self.products[product_id] = {
            "product_id": product_id,
            "product_code": product_code,
            "product_name": product_name,
            "unit_price": price,
            "category_name": category,
            "created_at": datetime.now().isoformat(),
            "status": "ACTIVE"
        }
        
        self.operation_count += 1
        return product_id
    
    def find_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """查找产品（遗留接口）"""
        print(f"📦 遗留产品系统查找产品: {product_id}")
        self.operation_count += 1
        return self.products.get(product_id)
    
    def list_products_by_category(self, category: str = None) -> List[Dict[str, Any]]:
        """按类别列出产品（遗留接口）"""
        print(f"📦 遗留产品系统列出产品: {category or '全部'}")
        self.operation_count += 1
        
        if category:
            return [p for p in self.products.values() 
                   if p["category_name"] == category and p["status"] == "ACTIVE"]
        else:
            return [p for p in self.products.values() if p["status"] == "ACTIVE"]
    
    def modify_product(self, product_id: str, **changes) -> bool:
        """修改产品（遗留接口）"""
        print(f"📦 遗留产品系统修改产品: {product_id}")
        
        if product_id not in self.products:
            return False
        
        product = self.products[product_id]
        for key, value in changes.items():
            if key in product:
                product[key] = value
        
        self.operation_count += 1
        return True
    
    def remove_product(self, product_id: str) -> bool:
        """移除产品（遗留接口）"""
        print(f"📦 遗留产品系统移除产品: {product_id}")
        
        if product_id in self.products:
            self.products[product_id]["status"] = "DELETED"
            self.operation_count += 1
            return True
        return False
    
    def get_catalog_info(self) -> Dict[str, Any]:
        """获取目录信息（遗留接口）"""
        active_products = [p for p in self.products.values() if p["status"] == "ACTIVE"]
        categories = set(p["category_name"] for p in active_products)
        
        return {
            "total_products": len(self.products),
            "active_products": len(active_products),
            "categories": list(categories),
            "operations_performed": self.operation_count
        }


# ==================== 适配器实现 ====================

class LegacyUserAdapter(DataRepository):
    """遗留用户系统适配器"""
    
    def __init__(self, legacy_db: LegacyUserDatabase):
        self.legacy_db = legacy_db
    
    def create(self, entity: Dict[str, Any]) -> str:
        """创建用户实体"""
        print(f"🔄 用户适配器创建实体")
        
        # 提取必要字段
        username = entity.get("username", "")
        email = entity.get("email", "")
        full_name = entity.get("full_name", "")
        
        # 调用遗留系统接口
        user_id = self.legacy_db.insert_user(username, email, full_name)
        return str(user_id)
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查找用户"""
        print(f"🔄 用户适配器查找实体: {entity_id}")
        
        try:
            user_id = int(entity_id)
            legacy_user = self.legacy_db.get_user_by_id(user_id)
            
            if legacy_user:
                return self._convert_legacy_user(legacy_user)
            return None
        except ValueError:
            return None
    
    def find_all(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """查找所有用户"""
        print(f"🔄 用户适配器查找所有实体")
        
        legacy_users = self.legacy_db.get_all_users()
        users = [self._convert_legacy_user(user) for user in legacy_users]
        
        # 应用过滤器
        if filters:
            filtered_users = []
            for user in users:
                match = True
                for key, value in filters.items():
                    if key in user and user[key] != value:
                        match = False
                        break
                if match:
                    filtered_users.append(user)
            return filtered_users
        
        return users
    
    def update(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """更新用户实体"""
        print(f"🔄 用户适配器更新实体: {entity_id}")
        
        try:
            user_id = int(entity_id)
            
            # 转换字段名
            legacy_updates = {}
            if "username" in updates:
                legacy_updates["username"] = updates["username"]
            if "email" in updates:
                legacy_updates["email_address"] = updates["email"]
            if "full_name" in updates:
                legacy_updates["full_name"] = updates["full_name"]
            
            return self.legacy_db.update_user_info(user_id, **legacy_updates)
        except ValueError:
            return False
    
    def delete(self, entity_id: str) -> bool:
        """删除用户实体"""
        print(f"🔄 用户适配器删除实体: {entity_id}")
        
        try:
            user_id = int(entity_id)
            return self.legacy_db.deactivate_user(user_id)
        except ValueError:
            return False
    
    def _convert_legacy_user(self, legacy_user: sqlite3.Row) -> Dict[str, Any]:
        """转换遗留用户格式为现代格式"""
        return {
            "id": str(legacy_user["user_id"]),
            "username": legacy_user["username"],
            "email": legacy_user["email_address"],
            "full_name": legacy_user["full_name"],
            "created_at": legacy_user["registration_date"],
            "active": bool(legacy_user["is_active"])
        }
    
    def get_repository_info(self) -> str:
        """获取仓库信息"""
        stats = self.legacy_db.get_database_stats()
        return f"用户适配器 -> 遗留数据库 (活跃用户: {stats['active_users']}, 操作次数: {stats['operations_performed']})"


class LegacyProductAdapter(DataRepository):
    """遗留产品系统适配器"""
    
    def __init__(self, legacy_catalog: LegacyProductCatalog):
        self.legacy_catalog = legacy_catalog
    
    def create(self, entity: Dict[str, Any]) -> str:
        """创建产品实体"""
        print(f"🔄 产品适配器创建实体")
        
        # 提取必要字段
        code = entity.get("code", "")
        name = entity.get("name", "")
        price = entity.get("price", 0.0)
        category = entity.get("category", "")
        
        # 调用遗留系统接口
        product_id = self.legacy_catalog.add_product(code, name, price, category)
        return product_id
    
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查找产品"""
        print(f"🔄 产品适配器查找实体: {entity_id}")
        
        legacy_product = self.legacy_catalog.find_product(entity_id)
        
        if legacy_product and legacy_product["status"] == "ACTIVE":
            return self._convert_legacy_product(legacy_product)
        return None
    
    def find_all(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """查找所有产品"""
        print(f"🔄 产品适配器查找所有实体")
        
        category = filters.get("category") if filters else None
        legacy_products = self.legacy_catalog.list_products_by_category(category)
        
        products = [self._convert_legacy_product(product) for product in legacy_products]
        
        # 应用其他过滤器
        if filters:
            filtered_products = []
            for product in products:
                match = True
                for key, value in filters.items():
                    if key != "category" and key in product and product[key] != value:
                        match = False
                        break
                if match:
                    filtered_products.append(product)
            return filtered_products
        
        return products
    
    def update(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """更新产品实体"""
        print(f"🔄 产品适配器更新实体: {entity_id}")
        
        # 转换字段名
        legacy_updates = {}
        if "code" in updates:
            legacy_updates["product_code"] = updates["code"]
        if "name" in updates:
            legacy_updates["product_name"] = updates["name"]
        if "price" in updates:
            legacy_updates["unit_price"] = updates["price"]
        if "category" in updates:
            legacy_updates["category_name"] = updates["category"]
        
        return self.legacy_catalog.modify_product(entity_id, **legacy_updates)
    
    def delete(self, entity_id: str) -> bool:
        """删除产品实体"""
        print(f"🔄 产品适配器删除实体: {entity_id}")
        return self.legacy_catalog.remove_product(entity_id)
    
    def _convert_legacy_product(self, legacy_product: Dict[str, Any]) -> Dict[str, Any]:
        """转换遗留产品格式为现代格式"""
        return {
            "id": legacy_product["product_id"],
            "code": legacy_product["product_code"],
            "name": legacy_product["product_name"],
            "price": legacy_product["unit_price"],
            "category": legacy_product["category_name"],
            "created_at": legacy_product["created_at"]
        }
    
    def get_repository_info(self) -> str:
        """获取仓库信息"""
        info = self.legacy_catalog.get_catalog_info()
        return f"产品适配器 -> 遗留目录 (活跃产品: {info['active_products']}, 操作次数: {info['operations_performed']})"


# ==================== 现代化服务层 ====================

class ModernEntityService:
    """现代化实体服务"""
    
    def __init__(self):
        self.repositories: Dict[str, DataRepository] = {}
    
    def register_repository(self, entity_type: str, repository: DataRepository) -> None:
        """注册实体仓库"""
        self.repositories[entity_type] = repository
        print(f"✅ 已注册 {entity_type} 仓库: {repository.get_repository_info()}")
    
    def create_entity(self, entity_type: str, data: Dict[str, Any]) -> Optional[str]:
        """创建实体"""
        if entity_type not in self.repositories:
            print(f"❌ 未找到 {entity_type} 仓库")
            return None
        
        repository = self.repositories[entity_type]
        return repository.create(data)
    
    def get_entity(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """获取实体"""
        if entity_type not in self.repositories:
            return None
        
        repository = self.repositories[entity_type]
        return repository.find_by_id(entity_id)
    
    def list_entities(self, entity_type: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """列出实体"""
        if entity_type not in self.repositories:
            return []
        
        repository = self.repositories[entity_type]
        return repository.find_all(filters)
    
    def update_entity(self, entity_type: str, entity_id: str, 
                     updates: Dict[str, Any]) -> bool:
        """更新实体"""
        if entity_type not in self.repositories:
            return False
        
        repository = self.repositories[entity_type]
        return repository.update(entity_id, updates)
    
    def delete_entity(self, entity_type: str, entity_id: str) -> bool:
        """删除实体"""
        if entity_type not in self.repositories:
            return False
        
        repository = self.repositories[entity_type]
        return repository.delete(entity_id)
    
    def get_service_info(self) -> Dict[str, str]:
        """获取服务信息"""
        return {entity_type: repo.get_repository_info() 
                for entity_type, repo in self.repositories.items()}


def demo_legacy_system_adapter():
    """遗留系统适配器演示"""
    print("=" * 60)
    print("🏛️  遗留系统集成 - 适配器模式演示")
    print("=" * 60)
    
    # 创建遗留系统
    legacy_user_db = LegacyUserDatabase()
    legacy_product_catalog = LegacyProductCatalog()
    
    # 创建适配器
    user_adapter = LegacyUserAdapter(legacy_user_db)
    product_adapter = LegacyProductAdapter(legacy_product_catalog)
    
    # 创建现代化服务
    service = ModernEntityService()
    service.register_repository("user", user_adapter)
    service.register_repository("product", product_adapter)
    
    print(f"\n👥 测试用户管理:")
    
    # 创建用户
    user_data = [
        {"username": "alice", "email": "alice@example.com", "full_name": "Alice Smith"},
        {"username": "bob", "email": "bob@example.com", "full_name": "Bob Johnson"},
        {"username": "charlie", "email": "charlie@example.com", "full_name": "Charlie Brown"}
    ]
    
    user_ids = []
    for data in user_data:
        user_id = service.create_entity("user", data)
        user_ids.append(user_id)
        print(f"   ✅ 创建用户: {user_id}")
    
    # 查询用户
    print(f"\n🔍 查询用户:")
    for user_id in user_ids[:2]:
        user = service.get_entity("user", user_id)
        if user:
            print(f"   用户 {user_id}: {user['username']} ({user['email']})")
    
    # 更新用户
    print(f"\n✏️  更新用户:")
    if user_ids:
        success = service.update_entity("user", user_ids[0], {
            "email": "alice.smith@newcompany.com",
            "full_name": "Alice Smith-Johnson"
        })
        print(f"   更新结果: {'成功' if success else '失败'}")
    
    print(f"\n📦 测试产品管理:")
    
    # 创建产品
    product_data = [
        {"code": "LAPTOP001", "name": "高性能笔记本", "price": 8999.99, "category": "电脑"},
        {"code": "PHONE001", "name": "智能手机", "price": 3999.99, "category": "手机"},
        {"code": "TABLET001", "name": "平板电脑", "price": 2999.99, "category": "电脑"}
    ]
    
    product_ids = []
    for data in product_data:
        product_id = service.create_entity("product", data)
        product_ids.append(product_id)
        print(f"   ✅ 创建产品: {product_id}")
    
    # 按类别查询产品
    print(f"\n🔍 按类别查询产品:")
    computer_products = service.list_entities("product", {"category": "电脑"})
    for product in computer_products:
        print(f"   {product['name']}: ¥{product['price']}")
    
    # 显示服务信息
    print(f"\n📊 服务信息:")
    service_info = service.get_service_info()
    for entity_type, info in service_info.items():
        print(f"   {entity_type}: {info}")


if __name__ == "__main__":
    demo_legacy_system_adapter()
