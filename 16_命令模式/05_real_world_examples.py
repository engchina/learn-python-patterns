"""
05_real_world_examples.py - 命令模式实际应用场景

这个示例展示了命令模式在实际项目中的应用，包括：
1. 游戏操作记录和回放系统
2. HTTP请求重试机制
3. 图形编辑器的操作历史
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import time
import json
import random
from enum import Enum


# ==================== 游戏操作记录和回放系统 ====================
class GameAction(ABC):
    """游戏动作抽象基类"""
    
    def __init__(self, timestamp: float = None):
        self.timestamp = timestamp or time.time()
        self.player_id: Optional[str] = None
    
    @abstractmethod
    def execute(self, game_state: 'GameState') -> str:
        """执行动作"""
        pass
    
    @abstractmethod
    def undo(self, game_state: 'GameState') -> str:
        """撤销动作"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameAction':
        """从字典反序列化"""
        pass


class GameState:
    """游戏状态"""
    
    def __init__(self):
        self.players: Dict[str, Dict[str, Any]] = {}
        self.game_objects: Dict[str, Dict[str, Any]] = {}
        self.score: Dict[str, int] = {}
        self.game_time = 0.0
    
    def add_player(self, player_id: str, x: float, y: float):
        """添加玩家"""
        self.players[player_id] = {'x': x, 'y': y, 'health': 100, 'items': []}
        self.score[player_id] = 0
    
    def move_player(self, player_id: str, dx: float, dy: float) -> Tuple[float, float]:
        """移动玩家，返回之前的位置"""
        if player_id in self.players:
            old_x, old_y = self.players[player_id]['x'], self.players[player_id]['y']
            self.players[player_id]['x'] += dx
            self.players[player_id]['y'] += dy
            return old_x, old_y
        return 0.0, 0.0
    
    def add_score(self, player_id: str, points: int) -> int:
        """增加分数，返回之前的分数"""
        if player_id in self.score:
            old_score = self.score[player_id]
            self.score[player_id] += points
            return old_score
        return 0
    
    def get_player_info(self, player_id: str) -> Dict[str, Any]:
        """获取玩家信息"""
        return self.players.get(player_id, {})


class MoveAction(GameAction):
    """移动动作"""
    
    def __init__(self, player_id: str, dx: float, dy: float, timestamp: float = None):
        super().__init__(timestamp)
        self.player_id = player_id
        self.dx = dx
        self.dy = dy
        self.old_x = 0.0
        self.old_y = 0.0
    
    def execute(self, game_state: GameState) -> str:
        self.old_x, self.old_y = game_state.move_player(self.player_id, self.dx, self.dy)
        player_info = game_state.get_player_info(self.player_id)
        return f"玩家 {self.player_id} 移动到 ({player_info['x']:.1f}, {player_info['y']:.1f})"
    
    def undo(self, game_state: GameState) -> str:
        if self.player_id in game_state.players:
            game_state.players[self.player_id]['x'] = self.old_x
            game_state.players[self.player_id]['y'] = self.old_y
            return f"玩家 {self.player_id} 位置恢复到 ({self.old_x:.1f}, {self.old_y:.1f})"
        return f"无法撤销：玩家 {self.player_id} 不存在"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'move',
            'player_id': self.player_id,
            'dx': self.dx,
            'dy': self.dy,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoveAction':
        return cls(data['player_id'], data['dx'], data['dy'], data['timestamp'])


class ScoreAction(GameAction):
    """得分动作"""
    
    def __init__(self, player_id: str, points: int, timestamp: float = None):
        super().__init__(timestamp)
        self.player_id = player_id
        self.points = points
        self.old_score = 0
    
    def execute(self, game_state: GameState) -> str:
        self.old_score = game_state.add_score(self.player_id, self.points)
        new_score = game_state.score.get(self.player_id, 0)
        return f"玩家 {self.player_id} 获得 {self.points} 分，总分: {new_score}"
    
    def undo(self, game_state: GameState) -> str:
        if self.player_id in game_state.score:
            game_state.score[self.player_id] = self.old_score
            return f"玩家 {self.player_id} 分数恢复到 {self.old_score}"
        return f"无法撤销：玩家 {self.player_id} 不存在"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'score',
            'player_id': self.player_id,
            'points': self.points,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScoreAction':
        return cls(data['player_id'], data['points'], data['timestamp'])


class GameRecorder:
    """游戏录制器"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.actions: List[GameAction] = []
        self.current_position = -1
    
    def record_action(self, action: GameAction) -> str:
        """记录动作"""
        result = action.execute(self.game_state)
        
        # 如果当前位置不在末尾，清除后面的记录
        if self.current_position < len(self.actions) - 1:
            self.actions = self.actions[:self.current_position + 1]
        
        self.actions.append(action)
        self.current_position += 1
        return result
    
    def undo_last_action(self) -> str:
        """撤销最后一个动作"""
        if self.current_position >= 0:
            action = self.actions[self.current_position]
            result = action.undo(self.game_state)
            self.current_position -= 1
            return result
        return "没有可撤销的动作"
    
    def redo_action(self) -> str:
        """重做动作"""
        if self.current_position < len(self.actions) - 1:
            self.current_position += 1
            action = self.actions[self.current_position]
            result = action.execute(self.game_state)
            return f"重做: {result}"
        return "没有可重做的动作"
    
    def save_replay(self, filename: str):
        """保存回放文件"""
        replay_data = {
            'actions': [action.to_dict() for action in self.actions],
            'total_actions': len(self.actions),
            'duration': self.actions[-1].timestamp - self.actions[0].timestamp if self.actions else 0
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(replay_data, f, ensure_ascii=False, indent=2)
        
        return f"回放已保存到 {filename}"
    
    def load_replay(self, filename: str) -> str:
        """加载回放文件"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                replay_data = json.load(f)
            
            self.actions.clear()
            self.current_position = -1
            
            action_factories = {
                'move': MoveAction.from_dict,
                'score': ScoreAction.from_dict
            }
            
            for action_data in replay_data['actions']:
                action_type = action_data['type']
                if action_type in action_factories:
                    action = action_factories[action_type](action_data)
                    self.actions.append(action)
            
            return f"回放已加载，共 {len(self.actions)} 个动作"
        
        except Exception as e:
            return f"加载回放失败: {str(e)}"
    
    def replay_actions(self, speed_multiplier: float = 1.0) -> List[str]:
        """回放所有动作"""
        results = []
        
        # 重置游戏状态
        original_position = self.current_position
        while self.current_position >= 0:
            self.actions[self.current_position].undo(self.game_state)
            self.current_position -= 1
        
        # 重新执行所有动作
        for i, action in enumerate(self.actions):
            if i > 0:
                # 计算延迟时间
                delay = (action.timestamp - self.actions[i-1].timestamp) / speed_multiplier
                if delay > 0:
                    time.sleep(min(delay, 1.0))  # 最大延迟1秒
            
            result = action.execute(self.game_state)
            results.append(f"回放 {i+1}: {result}")
            self.current_position = i
        
        return results


# ==================== HTTP请求重试机制 ====================
class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpRequest:
    """HTTP请求"""
    
    def __init__(self, method: HttpMethod, url: str, headers: Dict[str, str] = None, 
                 data: Any = None, timeout: float = 30.0):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.timeout = timeout


class HttpResponse:
    """HTTP响应"""
    
    def __init__(self, status_code: int, headers: Dict[str, str] = None, 
                 content: str = "", error: str = ""):
        self.status_code = status_code
        self.headers = headers or {}
        self.content = content
        self.error = error
        self.timestamp = time.time()


class HttpClient:
    """模拟HTTP客户端"""
    
    def __init__(self, failure_rate: float = 0.3):
        self.failure_rate = failure_rate
        self.request_count = 0
    
    def send_request(self, request: HttpRequest) -> HttpResponse:
        """发送HTTP请求"""
        self.request_count += 1
        
        # 模拟网络延迟
        time.sleep(0.1)
        
        # 模拟随机失败
        if random.random() < self.failure_rate:
            error_codes = [500, 502, 503, 504, 408]
            status_code = random.choice(error_codes)
            return HttpResponse(
                status_code=status_code,
                error=f"服务器错误: {status_code}"
            )
        
        # 模拟成功响应
        return HttpResponse(
            status_code=200,
            content=f"成功响应 {request.method.value} {request.url}",
            headers={"Content-Type": "application/json"}
        )


class HttpRequestCommand(ABC):
    """HTTP请求命令基类"""
    
    def __init__(self, client: HttpClient, request: HttpRequest, max_retries: int = 3):
        self.client = client
        self.request = request
        self.max_retries = max_retries
        self.attempt_count = 0
        self.responses: List[HttpResponse] = []
        self.final_response: Optional[HttpResponse] = None
    
    @abstractmethod
    def should_retry(self, response: HttpResponse) -> bool:
        """判断是否应该重试"""
        pass
    
    def execute(self) -> str:
        """执行HTTP请求（带重试）"""
        self.attempt_count = 0
        self.responses.clear()
        
        while self.attempt_count < self.max_retries:
            self.attempt_count += 1
            
            try:
                response = self.client.send_request(self.request)
                self.responses.append(response)
                
                if response.status_code == 200:
                    self.final_response = response
                    return f"请求成功 (尝试 {self.attempt_count}/{self.max_retries}): {response.content}"
                
                elif not self.should_retry(response):
                    self.final_response = response
                    return f"请求失败，不重试: {response.error}"
                
                elif self.attempt_count < self.max_retries:
                    # 指数退避
                    delay = 2 ** (self.attempt_count - 1)
                    time.sleep(min(delay, 10))  # 最大延迟10秒
                    continue
                
            except Exception as e:
                error_response = HttpResponse(0, error=str(e))
                self.responses.append(error_response)
        
        self.final_response = self.responses[-1] if self.responses else None
        return f"请求最终失败 (尝试 {self.attempt_count}/{self.max_retries}): {self.final_response.error if self.final_response else '未知错误'}"
    
    def get_description(self) -> str:
        return f"{self.request.method.value} {self.request.url}"


class ApiRequestCommand(HttpRequestCommand):
    """API请求命令"""
    
    def should_retry(self, response: HttpResponse) -> bool:
        """API请求的重试策略"""
        # 5xx错误和408超时错误可以重试
        return response.status_code in [500, 502, 503, 504, 408]


class CriticalRequestCommand(HttpRequestCommand):
    """关键请求命令"""
    
    def should_retry(self, response: HttpResponse) -> bool:
        """关键请求的重试策略 - 更激进的重试"""
        # 除了4xx客户端错误外都重试
        return response.status_code >= 500 or response.status_code == 408


# ==================== 演示函数 ====================
def demonstrate_game_recorder():
    """演示游戏录制和回放"""
    print("=" * 60)
    print("游戏操作记录和回放系统演示")
    print("=" * 60)
    
    # 创建游戏状态和录制器
    game_state = GameState()
    recorder = GameRecorder(game_state)
    
    # 添加玩家
    game_state.add_player("player1", 0.0, 0.0)
    game_state.add_player("player2", 10.0, 10.0)
    
    print("1. 记录游戏动作:")
    
    # 记录一系列动作
    actions = [
        MoveAction("player1", 5.0, 3.0),
        ScoreAction("player1", 100),
        MoveAction("player2", -2.0, 5.0),
        ScoreAction("player2", 150),
        MoveAction("player1", 2.0, -1.0),
        ScoreAction("player1", 50)
    ]
    
    for action in actions:
        result = recorder.record_action(action)
        print(f"   {result}")
        time.sleep(0.1)  # 模拟时间间隔
    
    print(f"\n2. 当前游戏状态:")
    for player_id, info in game_state.players.items():
        score = game_state.score.get(player_id, 0)
        print(f"   {player_id}: 位置({info['x']:.1f}, {info['y']:.1f}), 分数: {score}")
    
    print(f"\n3. 撤销最后两个动作:")
    print(f"   {recorder.undo_last_action()}")
    print(f"   {recorder.undo_last_action()}")
    
    print(f"\n4. 撤销后的游戏状态:")
    for player_id, info in game_state.players.items():
        score = game_state.score.get(player_id, 0)
        print(f"   {player_id}: 位置({info['x']:.1f}, {info['y']:.1f}), 分数: {score}")
    
    print(f"\n5. 重做一个动作:")
    print(f"   {recorder.redo_action()}")
    
    # 保存和加载回放
    print(f"\n6. 保存回放:")
    save_result = recorder.save_replay("game_replay.json")
    print(f"   {save_result}")


def demonstrate_http_retry():
    """演示HTTP请求重试机制"""
    print("\n" + "=" * 60)
    print("HTTP请求重试机制演示")
    print("=" * 60)
    
    # 创建HTTP客户端（30%失败率）
    client = HttpClient(failure_rate=0.7)  # 高失败率以演示重试
    
    print("1. 执行API请求（带重试）:")
    
    # 创建不同类型的请求
    requests = [
        ApiRequestCommand(
            client,
            HttpRequest(HttpMethod.GET, "https://api.example.com/users"),
            max_retries=3
        ),
        CriticalRequestCommand(
            client,
            HttpRequest(HttpMethod.POST, "https://api.example.com/orders", data={"item": "book"}),
            max_retries=5
        ),
        ApiRequestCommand(
            client,
            HttpRequest(HttpMethod.PUT, "https://api.example.com/profile"),
            max_retries=2
        )
    ]
    
    for i, request_cmd in enumerate(requests, 1):
        print(f"\n   请求 {i}: {request_cmd.get_description()}")
        result = request_cmd.execute()
        print(f"   结果: {result}")
        print(f"   尝试次数: {request_cmd.attempt_count}")
        
        if request_cmd.responses:
            print(f"   响应历史:")
            for j, response in enumerate(request_cmd.responses, 1):
                status = "成功" if response.status_code == 200 else "失败"
                print(f"     尝试 {j}: {status} (状态码: {response.status_code})")


if __name__ == "__main__":
    demonstrate_game_recorder()
    demonstrate_http_retry()
