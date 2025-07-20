"""
适配器模式API集成 - API接口适配器

这个示例展示了适配器模式在API集成中的应用，演示如何
统一不同版本和协议的API接口。

作者: Adapter Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime
from enum import Enum


class APIVersion(Enum):
    """API版本枚举"""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class HTTPMethod(Enum):
    """HTTP方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


# ==================== 目标接口 - 统一API接口 ====================

class UnifiedAPIClient(ABC):
    """统一API客户端接口"""
    
    @abstractmethod
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        pass
    
    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        pass
    
    @abstractmethod
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户"""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        pass
    
    @abstractmethod
    def list_users(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """列出用户"""
        pass
    
    @abstractmethod
    def get_client_info(self) -> str:
        """获取客户端信息"""
        pass


# ==================== 被适配者 - 不同版本的API ====================

class RestAPIv1Client:
    """REST API v1 客户端 - 被适配者A"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.request_count = 0
    
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """获取用户信息（v1接口）"""
        print(f"🌐 REST API v1 GET /users/{user_id}")
        self.request_count += 1
        time.sleep(0.1)  # 模拟网络延迟
        
        # 模拟v1响应格式
        return {
            "status": "success",
            "user": {
                "id": user_id,
                "name": f"User{user_id}",
                "email": f"user{user_id}@example.com",
                "created": "2024-01-01T00:00:00Z",
                "active": True
            }
        }
    
    def create_new_user(self, name: str, email: str) -> Dict[str, Any]:
        """创建新用户（v1接口）"""
        print(f"🌐 REST API v1 POST /users")
        self.request_count += 1
        time.sleep(0.15)
        
        new_id = 1000 + self.request_count
        return {
            "status": "success",
            "message": "User created successfully",
            "user": {
                "id": new_id,
                "name": name,
                "email": email,
                "created": datetime.now().isoformat() + "Z",
                "active": True
            }
        }
    
    def modify_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """修改用户（v1接口）"""
        print(f"🌐 REST API v1 PUT /users/{user_id}")
        self.request_count += 1
        time.sleep(0.12)
        
        return {
            "status": "success",
            "message": "User updated successfully",
            "user": {
                "id": user_id,
                "name": kwargs.get("name", f"User{user_id}"),
                "email": kwargs.get("email", f"user{user_id}@example.com"),
                "updated": datetime.now().isoformat() + "Z",
                "active": kwargs.get("active", True)
            }
        }
    
    def remove_user(self, user_id: int) -> Dict[str, Any]:
        """移除用户（v1接口）"""
        print(f"🌐 REST API v1 DELETE /users/{user_id}")
        self.request_count += 1
        time.sleep(0.08)
        
        return {
            "status": "success",
            "message": "User deleted successfully"
        }
    
    def get_users_list(self, offset: int = 0, count: int = 10) -> Dict[str, Any]:
        """获取用户列表（v1接口）"""
        print(f"🌐 REST API v1 GET /users?offset={offset}&count={count}")
        self.request_count += 1
        time.sleep(0.2)
        
        users = []
        for i in range(offset + 1, offset + count + 1):
            users.append({
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "active": True
            })
        
        return {
            "status": "success",
            "users": users,
            "total": 100,
            "offset": offset,
            "count": len(users)
        }


class RestAPIv2Client:
    """REST API v2 客户端 - 被适配者B"""
    
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.token = token
        self.request_count = 0
    
    def fetch_user(self, user_id: str) -> Dict[str, Any]:
        """获取用户（v2接口）"""
        print(f"🌐 REST API v2 GET /api/v2/users/{user_id}")
        self.request_count += 1
        time.sleep(0.09)
        
        # 模拟v2响应格式
        return {
            "data": {
                "user_id": user_id,
                "username": f"user_{user_id}",
                "email_address": f"user{user_id}@company.com",
                "profile": {
                    "first_name": f"First{user_id}",
                    "last_name": f"Last{user_id}",
                    "created_at": "2024-01-01T00:00:00.000Z",
                    "is_active": True
                }
            },
            "meta": {
                "version": "2.0",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def add_user(self, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        """添加用户（v2接口）"""
        print(f"🌐 REST API v2 POST /api/v2/users")
        self.request_count += 1
        time.sleep(0.18)
        
        new_id = f"usr_{2000 + self.request_count}"
        return {
            "data": {
                "user_id": new_id,
                "username": user_payload.get("username", ""),
                "email_address": user_payload.get("email_address", ""),
                "profile": {
                    "first_name": user_payload.get("first_name", ""),
                    "last_name": user_payload.get("last_name", ""),
                    "created_at": datetime.now().isoformat(),
                    "is_active": True
                }
            },
            "meta": {
                "operation": "create",
                "success": True
            }
        }
    
    def patch_user(self, user_id: str, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        """部分更新用户（v2接口）"""
        print(f"🌐 REST API v2 PATCH /api/v2/users/{user_id}")
        self.request_count += 1
        time.sleep(0.14)
        
        return {
            "data": {
                "user_id": user_id,
                "updated_fields": list(patch_data.keys()),
                "updated_at": datetime.now().isoformat()
            },
            "meta": {
                "operation": "update",
                "success": True
            }
        }
    
    def archive_user(self, user_id: str) -> Dict[str, Any]:
        """归档用户（v2接口）"""
        print(f"🌐 REST API v2 POST /api/v2/users/{user_id}/archive")
        self.request_count += 1
        time.sleep(0.1)
        
        return {
            "data": {
                "user_id": user_id,
                "archived_at": datetime.now().isoformat()
            },
            "meta": {
                "operation": "archive",
                "success": True
            }
        }
    
    def query_users(self, page_number: int = 1, page_size: int = 10, 
                   filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """查询用户（v2接口）"""
        print(f"🌐 REST API v2 GET /api/v2/users?page={page_number}&size={page_size}")
        self.request_count += 1
        time.sleep(0.25)
        
        users = []
        start_id = (page_number - 1) * page_size + 1
        
        for i in range(start_id, start_id + page_size):
            users.append({
                "user_id": f"usr_{i}",
                "username": f"user_{i}",
                "email_address": f"user{i}@company.com",
                "profile": {
                    "is_active": True
                }
            })
        
        return {
            "data": {
                "users": users,
                "pagination": {
                    "page": page_number,
                    "size": page_size,
                    "total_pages": 10,
                    "total_items": 100
                }
            },
            "meta": {
                "query_time": datetime.now().isoformat()
            }
        }


class GraphQLAPIClient:
    """GraphQL API 客户端 - 被适配者C"""
    
    def __init__(self, endpoint: str, auth_header: str):
        self.endpoint = endpoint
        self.auth_header = auth_header
        self.query_count = 0
    
    def execute_query(self, query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行GraphQL查询"""
        print(f"🌐 GraphQL POST {self.endpoint}")
        print(f"   Query: {query[:50]}...")
        self.query_count += 1
        time.sleep(0.16)
        
        # 模拟GraphQL响应
        if "user(" in query:
            user_id = variables.get("id", "1") if variables else "1"
            return {
                "data": {
                    "user": {
                        "id": user_id,
                        "displayName": f"GraphQL User {user_id}",
                        "contactInfo": {
                            "email": f"gql_user{user_id}@api.com"
                        },
                        "metadata": {
                            "createdDate": "2024-01-01",
                            "status": "ACTIVE"
                        }
                    }
                }
            }
        elif "createUser" in query:
            return {
                "data": {
                    "createUser": {
                        "id": f"gql_{3000 + self.query_count}",
                        "displayName": variables.get("input", {}).get("displayName", ""),
                        "contactInfo": {
                            "email": variables.get("input", {}).get("email", "")
                        },
                        "metadata": {
                            "createdDate": datetime.now().strftime("%Y-%m-%d"),
                            "status": "ACTIVE"
                        }
                    }
                }
            }
        elif "updateUser" in query:
            return {
                "data": {
                    "updateUser": {
                        "id": variables.get("id", ""),
                        "success": True,
                        "updatedAt": datetime.now().isoformat()
                    }
                }
            }
        elif "deleteUser" in query:
            return {
                "data": {
                    "deleteUser": {
                        "success": True,
                        "deletedAt": datetime.now().isoformat()
                    }
                }
            }
        elif "users(" in query:
            page = variables.get("page", 1) if variables else 1
            limit = variables.get("limit", 10) if variables else 10
            
            users = []
            for i in range((page-1)*limit + 1, page*limit + 1):
                users.append({
                    "id": f"gql_{i}",
                    "displayName": f"GraphQL User {i}",
                    "contactInfo": {
                        "email": f"gql_user{i}@api.com"
                    },
                    "metadata": {
                        "status": "ACTIVE"
                    }
                })
            
            return {
                "data": {
                    "users": {
                        "nodes": users,
                        "pageInfo": {
                            "currentPage": page,
                            "totalPages": 10,
                            "totalCount": 100
                        }
                    }
                }
            }
        
        return {"data": None, "errors": [{"message": "Unknown query"}]}


# ==================== 适配器实现 ====================

class RestAPIv1Adapter(UnifiedAPIClient):
    """REST API v1 适配器"""
    
    def __init__(self, api_client: RestAPIv1Client):
        self.api_client = api_client
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        print(f"🔄 REST v1适配器获取用户: {user_id}")
        
        try:
            response = self.api_client.get_user_info(int(user_id))
            if response["status"] == "success":
                user = response["user"]
                return {
                    "id": str(user["id"]),
                    "name": user["name"],
                    "email": user["email"],
                    "created_at": user["created"],
                    "active": user["active"]
                }
        except (ValueError, KeyError):
            pass
        return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        print(f"🔄 REST v1适配器创建用户")
        
        response = self.api_client.create_new_user(
            user_data.get("name", ""),
            user_data.get("email", "")
        )
        
        if response["status"] == "success":
            user = response["user"]
            return {
                "success": True,
                "user": {
                    "id": str(user["id"]),
                    "name": user["name"],
                    "email": user["email"],
                    "created_at": user["created"]
                }
            }
        
        return {"success": False, "error": "创建失败"}
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户"""
        print(f"🔄 REST v1适配器更新用户: {user_id}")
        
        try:
            response = self.api_client.modify_user(int(user_id), **updates)
            if response["status"] == "success":
                return {"success": True, "message": response["message"]}
        except ValueError:
            pass
        
        return {"success": False, "error": "更新失败"}
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        print(f"🔄 REST v1适配器删除用户: {user_id}")
        
        try:
            response = self.api_client.remove_user(int(user_id))
            return response["status"] == "success"
        except ValueError:
            return False
    
    def list_users(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """列出用户"""
        print(f"🔄 REST v1适配器列出用户: page={page}, limit={limit}")
        
        offset = (page - 1) * limit
        response = self.api_client.get_users_list(offset, limit)
        
        if response["status"] == "success":
            users = []
            for user in response["users"]:
                users.append({
                    "id": str(user["id"]),
                    "name": user["name"],
                    "email": user["email"],
                    "active": user["active"]
                })
            
            return {
                "users": users,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": response["total"]
                }
            }
        
        return {"users": [], "pagination": {"page": page, "limit": limit, "total": 0}}
    
    def get_client_info(self) -> str:
        return f"REST API v1适配器 (请求次数: {self.api_client.request_count})"


class RestAPIv2Adapter(UnifiedAPIClient):
    """REST API v2 适配器"""
    
    def __init__(self, api_client: RestAPIv2Client):
        self.api_client = api_client
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        print(f"🔄 REST v2适配器获取用户: {user_id}")
        
        response = self.api_client.fetch_user(user_id)
        if "data" in response:
            user_data = response["data"]
            profile = user_data.get("profile", {})
            
            return {
                "id": user_data["user_id"],
                "name": f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip(),
                "email": user_data["email_address"],
                "created_at": profile.get("created_at", ""),
                "active": profile.get("is_active", True)
            }
        return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        print(f"🔄 REST v2适配器创建用户")
        
        # 分解姓名
        name_parts = user_data.get("name", "").split(" ", 1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        payload = {
            "username": user_data.get("name", "").replace(" ", "_").lower(),
            "email_address": user_data.get("email", ""),
            "first_name": first_name,
            "last_name": last_name
        }
        
        response = self.api_client.add_user(payload)
        if response.get("meta", {}).get("success"):
            user_data = response["data"]
            profile = user_data.get("profile", {})
            
            return {
                "success": True,
                "user": {
                    "id": user_data["user_id"],
                    "name": f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip(),
                    "email": user_data["email_address"],
                    "created_at": profile.get("created_at", "")
                }
            }
        
        return {"success": False, "error": "创建失败"}
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户"""
        print(f"🔄 REST v2适配器更新用户: {user_id}")
        
        # 转换更新字段
        patch_data = {}
        if "email" in updates:
            patch_data["email_address"] = updates["email"]
        if "name" in updates:
            name_parts = updates["name"].split(" ", 1)
            patch_data["first_name"] = name_parts[0] if name_parts else ""
            patch_data["last_name"] = name_parts[1] if len(name_parts) > 1 else ""
        
        response = self.api_client.patch_user(user_id, patch_data)
        if response.get("meta", {}).get("success"):
            return {"success": True, "message": "用户更新成功"}
        
        return {"success": False, "error": "更新失败"}
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        print(f"🔄 REST v2适配器删除用户: {user_id}")
        
        response = self.api_client.archive_user(user_id)
        return response.get("meta", {}).get("success", False)
    
    def list_users(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """列出用户"""
        print(f"🔄 REST v2适配器列出用户: page={page}, limit={limit}")
        
        response = self.api_client.query_users(page, limit)
        if "data" in response:
            data = response["data"]
            users = []
            
            for user in data["users"]:
                profile = user.get("profile", {})
                users.append({
                    "id": user["user_id"],
                    "name": user["username"],
                    "email": user["email_address"],
                    "active": profile.get("is_active", True)
                })
            
            pagination = data.get("pagination", {})
            return {
                "users": users,
                "pagination": {
                    "page": pagination.get("page", page),
                    "limit": pagination.get("size", limit),
                    "total": pagination.get("total_items", 0)
                }
            }
        
        return {"users": [], "pagination": {"page": page, "limit": limit, "total": 0}}
    
    def get_client_info(self) -> str:
        return f"REST API v2适配器 (请求次数: {self.api_client.request_count})"


class GraphQLAdapter(UnifiedAPIClient):
    """GraphQL API 适配器"""
    
    def __init__(self, api_client: GraphQLAPIClient):
        self.api_client = api_client
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息"""
        print(f"🔄 GraphQL适配器获取用户: {user_id}")
        
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                displayName
                contactInfo {
                    email
                }
                metadata {
                    createdDate
                    status
                }
            }
        }
        """
        
        response = self.api_client.execute_query(query, {"id": user_id})
        if response.get("data", {}).get("user"):
            user = response["data"]["user"]
            return {
                "id": user["id"],
                "name": user["displayName"],
                "email": user["contactInfo"]["email"],
                "created_at": user["metadata"]["createdDate"],
                "active": user["metadata"]["status"] == "ACTIVE"
            }
        return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        print(f"🔄 GraphQL适配器创建用户")
        
        mutation = """
        mutation CreateUser($input: UserInput!) {
            createUser(input: $input) {
                id
                displayName
                contactInfo {
                    email
                }
                metadata {
                    createdDate
                    status
                }
            }
        }
        """
        
        variables = {
            "input": {
                "displayName": user_data.get("name", ""),
                "email": user_data.get("email", "")
            }
        }
        
        response = self.api_client.execute_query(mutation, variables)
        if response.get("data", {}).get("createUser"):
            user = response["data"]["createUser"]
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "name": user["displayName"],
                    "email": user["contactInfo"]["email"],
                    "created_at": user["metadata"]["createdDate"]
                }
            }
        
        return {"success": False, "error": "创建失败"}
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户"""
        print(f"🔄 GraphQL适配器更新用户: {user_id}")
        
        mutation = """
        mutation UpdateUser($id: ID!, $input: UserUpdateInput!) {
            updateUser(id: $id, input: $input) {
                id
                success
                updatedAt
            }
        }
        """
        
        variables = {
            "id": user_id,
            "input": updates
        }
        
        response = self.api_client.execute_query(mutation, variables)
        if response.get("data", {}).get("updateUser", {}).get("success"):
            return {"success": True, "message": "用户更新成功"}
        
        return {"success": False, "error": "更新失败"}
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        print(f"🔄 GraphQL适配器删除用户: {user_id}")
        
        mutation = """
        mutation DeleteUser($id: ID!) {
            deleteUser(id: $id) {
                success
                deletedAt
            }
        }
        """
        
        response = self.api_client.execute_query(mutation, {"id": user_id})
        return response.get("data", {}).get("deleteUser", {}).get("success", False)
    
    def list_users(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """列出用户"""
        print(f"🔄 GraphQL适配器列出用户: page={page}, limit={limit}")
        
        query = """
        query ListUsers($page: Int!, $limit: Int!) {
            users(page: $page, limit: $limit) {
                nodes {
                    id
                    displayName
                    contactInfo {
                        email
                    }
                    metadata {
                        status
                    }
                }
                pageInfo {
                    currentPage
                    totalPages
                    totalCount
                }
            }
        }
        """
        
        response = self.api_client.execute_query(query, {"page": page, "limit": limit})
        if response.get("data", {}).get("users"):
            users_data = response["data"]["users"]
            users = []
            
            for user in users_data["nodes"]:
                users.append({
                    "id": user["id"],
                    "name": user["displayName"],
                    "email": user["contactInfo"]["email"],
                    "active": user["metadata"]["status"] == "ACTIVE"
                })
            
            page_info = users_data.get("pageInfo", {})
            return {
                "users": users,
                "pagination": {
                    "page": page_info.get("currentPage", page),
                    "limit": limit,
                    "total": page_info.get("totalCount", 0)
                }
            }
        
        return {"users": [], "pagination": {"page": page, "limit": limit, "total": 0}}
    
    def get_client_info(self) -> str:
        return f"GraphQL适配器 (查询次数: {self.api_client.query_count})"


# ==================== 客户端代码 ====================

class UnifiedUserService:
    """统一用户服务"""
    
    def __init__(self):
        self.clients: Dict[str, UnifiedAPIClient] = {}
        self.default_client = None
    
    def register_client(self, name: str, client: UnifiedAPIClient, 
                       is_default: bool = False) -> None:
        """注册API客户端"""
        self.clients[name] = client
        if is_default or not self.default_client:
            self.default_client = name
        print(f"✅ 已注册API客户端: {name} -> {client.get_client_info()}")
    
    def get_user(self, user_id: str, client_name: str = None) -> Optional[Dict[str, Any]]:
        """获取用户"""
        client_name = client_name or self.default_client
        if client_name in self.clients:
            return self.clients[client_name].get_user(user_id)
        return None
    
    def create_user(self, user_data: Dict[str, Any], client_name: str = None) -> Dict[str, Any]:
        """创建用户"""
        client_name = client_name or self.default_client
        if client_name in self.clients:
            return self.clients[client_name].create_user(user_data)
        return {"success": False, "error": "客户端不存在"}
    
    def list_users(self, page: int = 1, limit: int = 5, client_name: str = None) -> Dict[str, Any]:
        """列出用户"""
        client_name = client_name or self.default_client
        if client_name in self.clients:
            return self.clients[client_name].list_users(page, limit)
        return {"users": [], "pagination": {"page": page, "limit": limit, "total": 0}}
    
    def get_available_clients(self) -> List[str]:
        """获取可用的客户端"""
        return list(self.clients.keys())


def demo_api_adapter():
    """API适配器演示"""
    print("=" * 60)
    print("🌐 API接口适配器 - 适配器模式演示")
    print("=" * 60)
    
    # 创建不同版本的API客户端
    rest_v1_client = RestAPIv1Client("https://api.example.com/v1", "api_key_123")
    rest_v2_client = RestAPIv2Client("https://api.example.com/v2", "bearer_token_456")
    graphql_client = GraphQLAPIClient("https://api.example.com/graphql", "Bearer jwt_token_789")
    
    # 创建适配器
    rest_v1_adapter = RestAPIv1Adapter(rest_v1_client)
    rest_v2_adapter = RestAPIv2Adapter(rest_v2_client)
    graphql_adapter = GraphQLAdapter(graphql_client)
    
    # 创建统一服务
    user_service = UnifiedUserService()
    user_service.register_client("rest_v1", rest_v1_adapter, is_default=True)
    user_service.register_client("rest_v2", rest_v2_adapter)
    user_service.register_client("graphql", graphql_adapter)
    
    # 测试不同客户端的用户创建
    print(f"\n👤 测试用户创建:")
    test_users = [
        ({"name": "Alice Johnson", "email": "alice@example.com"}, "rest_v1"),
        ({"name": "Bob Smith", "email": "bob@company.com"}, "rest_v2"),
        ({"name": "Charlie Brown", "email": "charlie@api.com"}, "graphql")
    ]
    
    created_users = []
    for user_data, client_name in test_users:
        print(f"\n🔸 使用 {client_name} 创建用户:")
        result = user_service.create_user(user_data, client_name)
        if result["success"]:
            created_users.append((result["user"]["id"], client_name))
            print(f"   ✅ 创建成功: {result['user']['name']} (ID: {result['user']['id']})")
        else:
            print(f"   ❌ 创建失败: {result.get('error', '未知错误')}")
    
    # 测试用户查询
    print(f"\n🔍 测试用户查询:")
    for user_id, client_name in created_users:
        print(f"\n🔸 使用 {client_name} 查询用户 {user_id}:")
        user = user_service.get_user(user_id, client_name)
        if user:
            print(f"   用户: {user['name']} ({user['email']})")
            print(f"   状态: {'活跃' if user['active'] else '非活跃'}")
        else:
            print(f"   ❌ 用户不存在")
    
    # 测试用户列表
    print(f"\n📋 测试用户列表:")
    for client_name in user_service.get_available_clients():
        print(f"\n🔸 使用 {client_name} 获取用户列表:")
        result = user_service.list_users(1, 3, client_name)
        users = result["users"]
        pagination = result["pagination"]
        
        print(f"   找到 {len(users)} 个用户 (总计: {pagination['total']})")
        for user in users[:2]:  # 只显示前2个
            print(f"     - {user['name']} ({user['email']})")


if __name__ == "__main__":
    demo_api_adapter()
