"""
05_real_world_examples.py - 实际项目中的观察者模式应用

这个示例展示了观察者模式在实际项目中的复杂应用场景，
包括股票价格监控、用户行为分析、系统监控等。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import threading
import time
import random
from enum import Enum


# ==================== 股票价格监控系统 ====================

class StockPriceSubject(ABC):
    """股票价格主题接口"""
    
    def __init__(self):
        self._observers: List['StockObserver'] = []
    
    def subscribe(self, observer: 'StockObserver') -> None:
        """订阅股票价格变化"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"📈 {observer.name} 订阅了股票价格监控")
    
    def unsubscribe(self, observer: 'StockObserver') -> None:
        """取消订阅"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"📉 {observer.name} 取消了股票价格监控")
    
    def notify_price_change(self, symbol: str, old_price: float, new_price: float) -> None:
        """通知价格变化"""
        change_percent = ((new_price - old_price) / old_price) * 100
        for observer in self._observers:
            observer.on_price_change(symbol, old_price, new_price, change_percent)


class StockMarket(StockPriceSubject):
    """股票市场 - 具体主题"""
    
    def __init__(self):
        super().__init__()
        self._stocks: Dict[str, float] = {}
        self._is_running = False
        self._update_thread: Optional[threading.Thread] = None
    
    def add_stock(self, symbol: str, initial_price: float) -> None:
        """添加股票"""
        self._stocks[symbol] = initial_price
        print(f"📊 添加股票 {symbol}，初始价格 ¥{initial_price:.2f}")
    
    def get_price(self, symbol: str) -> Optional[float]:
        """获取股票价格"""
        return self._stocks.get(symbol)
    
    def update_price(self, symbol: str, new_price: float) -> None:
        """手动更新股票价格"""
        if symbol in self._stocks:
            old_price = self._stocks[symbol]
            self._stocks[symbol] = new_price
            print(f"💹 {symbol} 价格更新: ¥{old_price:.2f} → ¥{new_price:.2f}")
            self.notify_price_change(symbol, old_price, new_price)
    
    def start_simulation(self) -> None:
        """开始价格模拟"""
        if not self._is_running:
            self._is_running = True
            self._update_thread = threading.Thread(target=self._simulate_price_changes)
            self._update_thread.daemon = True
            self._update_thread.start()
            print("🎯 股票价格模拟已开始")
    
    def stop_simulation(self) -> None:
        """停止价格模拟"""
        self._is_running = False
        print("⏹️ 股票价格模拟已停止")
    
    def _simulate_price_changes(self) -> None:
        """模拟价格变化"""
        while self._is_running:
            for symbol in list(self._stocks.keys()):
                if not self._is_running:
                    break
                
                old_price = self._stocks[symbol]
                # 随机价格变化 -5% 到 +5%
                change_percent = random.uniform(-0.05, 0.05)
                new_price = old_price * (1 + change_percent)
                new_price = max(0.01, round(new_price, 2))  # 确保价格为正
                
                self._stocks[symbol] = new_price
                self.notify_price_change(symbol, old_price, new_price)
                
                time.sleep(random.uniform(1, 3))  # 随机间隔


class StockObserver(ABC):
    """股票观察者接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def on_price_change(self, symbol: str, old_price: float, new_price: float, change_percent: float) -> None:
        """价格变化回调"""
        pass


class TradingBot(StockObserver):
    """交易机器人 - 自动交易"""
    
    def __init__(self, name: str, buy_threshold: float = -2.0, sell_threshold: float = 3.0):
        self._name = name
        self._buy_threshold = buy_threshold  # 跌幅超过此值时买入
        self._sell_threshold = sell_threshold  # 涨幅超过此值时卖出
        self._portfolio: Dict[str, int] = {}  # 持仓
        self._cash = 100000.0  # 现金
        self._transactions: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    def on_price_change(self, symbol: str, old_price: float, new_price: float, change_percent: float) -> None:
        """根据价格变化执行交易策略"""
        if change_percent <= self._buy_threshold and self._cash >= new_price * 100:
            # 买入信号
            shares = min(100, int(self._cash // new_price))
            if shares > 0:
                cost = shares * new_price
                self._cash -= cost
                self._portfolio[symbol] = self._portfolio.get(symbol, 0) + shares
                
                transaction = {
                    'type': 'BUY',
                    'symbol': symbol,
                    'shares': shares,
                    'price': new_price,
                    'cost': cost,
                    'time': datetime.now()
                }
                self._transactions.append(transaction)
                print(f"🤖 {self._name} 买入: {symbol} {shares}股 @ ¥{new_price:.2f}")
        
        elif change_percent >= self._sell_threshold and symbol in self._portfolio and self._portfolio[symbol] > 0:
            # 卖出信号
            shares = self._portfolio[symbol]
            revenue = shares * new_price
            self._cash += revenue
            self._portfolio[symbol] = 0
            
            transaction = {
                'type': 'SELL',
                'symbol': symbol,
                'shares': shares,
                'price': new_price,
                'revenue': revenue,
                'time': datetime.now()
            }
            self._transactions.append(transaction)
            print(f"🤖 {self._name} 卖出: {symbol} {shares}股 @ ¥{new_price:.2f}")
    
    def get_portfolio_value(self, market: StockMarket) -> float:
        """计算投资组合价值"""
        total_value = self._cash
        for symbol, shares in self._portfolio.items():
            if shares > 0:
                current_price = market.get_price(symbol)
                if current_price:
                    total_value += shares * current_price
        return total_value
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取交易表现摘要"""
        return {
            'cash': self._cash,
            'portfolio': self._portfolio,
            'transaction_count': len(self._transactions),
            'transactions': self._transactions[-5:]  # 最近5笔交易
        }


class PriceAlert(StockObserver):
    """价格警报系统"""
    
    def __init__(self, name: str):
        self._name = name
        self._alerts: Dict[str, Dict[str, float]] = {}  # symbol -> {high: price, low: price}
        self._triggered_alerts: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    def set_price_alert(self, symbol: str, high_price: Optional[float] = None, low_price: Optional[float] = None) -> None:
        """设置价格警报"""
        if symbol not in self._alerts:
            self._alerts[symbol] = {}
        
        if high_price is not None:
            self._alerts[symbol]['high'] = high_price
            print(f"🔔 设置 {symbol} 高价警报: ¥{high_price:.2f}")
        
        if low_price is not None:
            self._alerts[symbol]['low'] = low_price
            print(f"🔔 设置 {symbol} 低价警报: ¥{low_price:.2f}")
    
    def on_price_change(self, symbol: str, old_price: float, new_price: float, change_percent: float) -> None:
        """检查价格警报"""
        if symbol in self._alerts:
            alerts = self._alerts[symbol]
            
            # 检查高价警报
            if 'high' in alerts and new_price >= alerts['high'] and old_price < alerts['high']:
                alert = {
                    'type': 'HIGH_PRICE',
                    'symbol': symbol,
                    'trigger_price': alerts['high'],
                    'current_price': new_price,
                    'time': datetime.now()
                }
                self._triggered_alerts.append(alert)
                print(f"🚨 {self._name} 高价警报: {symbol} 达到 ¥{new_price:.2f}")
            
            # 检查低价警报
            if 'low' in alerts and new_price <= alerts['low'] and old_price > alerts['low']:
                alert = {
                    'type': 'LOW_PRICE',
                    'symbol': symbol,
                    'trigger_price': alerts['low'],
                    'current_price': new_price,
                    'time': datetime.now()
                }
                self._triggered_alerts.append(alert)
                print(f"🚨 {self._name} 低价警报: {symbol} 跌至 ¥{new_price:.2f}")
    
    def get_alert_history(self) -> List[Dict[str, Any]]:
        """获取警报历史"""
        return self._triggered_alerts.copy()


class MarketAnalyzer(StockObserver):
    """市场分析器"""
    
    def __init__(self, name: str):
        self._name = name
        self._price_history: Dict[str, List[Dict[str, Any]]] = {}
        self._volatility_threshold = 5.0  # 波动率阈值
    
    @property
    def name(self) -> str:
        return self._name
    
    def on_price_change(self, symbol: str, old_price: float, new_price: float, change_percent: float) -> None:
        """记录价格变化并分析"""
        if symbol not in self._price_history:
            self._price_history[symbol] = []
        
        price_record = {
            'price': new_price,
            'change_percent': change_percent,
            'time': datetime.now()
        }
        self._price_history[symbol].append(price_record)
        
        # 保持最近100条记录
        if len(self._price_history[symbol]) > 100:
            self._price_history[symbol] = self._price_history[symbol][-100:]
        
        # 分析波动率
        if abs(change_percent) > self._volatility_threshold:
            print(f"📊 {self._name} 高波动警告: {symbol} 变化 {change_percent:+.2f}%")
        
        # 趋势分析（简化版）
        if len(self._price_history[symbol]) >= 5:
            recent_changes = [record['change_percent'] for record in self._price_history[symbol][-5:]]
            avg_change = sum(recent_changes) / len(recent_changes)
            
            if avg_change > 1.0:
                print(f"📈 {self._name} 趋势分析: {symbol} 呈上升趋势")
            elif avg_change < -1.0:
                print(f"📉 {self._name} 趋势分析: {symbol} 呈下降趋势")
    
    def get_volatility_report(self, symbol: str) -> Dict[str, Any]:
        """获取波动率报告"""
        if symbol not in self._price_history or len(self._price_history[symbol]) < 2:
            return {'error': '数据不足'}
        
        changes = [record['change_percent'] for record in self._price_history[symbol]]
        avg_change = sum(changes) / len(changes)
        volatility = sum((change - avg_change) ** 2 for change in changes) / len(changes)
        
        return {
            'symbol': symbol,
            'data_points': len(changes),
            'average_change': avg_change,
            'volatility': volatility ** 0.5,
            'max_change': max(changes),
            'min_change': min(changes)
        }


# ==================== 演示函数 ====================

def demo_stock_monitoring():
    """股票监控系统演示"""
    print("=" * 60)
    print("📈 股票价格监控系统演示")
    print("=" * 60)
    
    # 创建股票市场
    market = StockMarket()
    
    # 添加股票
    market.add_stock("AAPL", 150.00)
    market.add_stock("GOOGL", 2800.00)
    market.add_stock("TSLA", 800.00)
    
    # 创建观察者
    trading_bot = TradingBot("智能交易机器人", buy_threshold=-3.0, sell_threshold=4.0)
    price_alert = PriceAlert("价格警报系统")
    market_analyzer = MarketAnalyzer("市场分析器")
    
    # 设置价格警报
    price_alert.set_price_alert("AAPL", high_price=160.0, low_price=140.0)
    price_alert.set_price_alert("TSLA", high_price=850.0, low_price=750.0)
    
    # 订阅市场更新
    print("\n📋 订阅市场更新:")
    market.subscribe(trading_bot)
    market.subscribe(price_alert)
    market.subscribe(market_analyzer)
    
    # 手动触发一些价格变化
    print("\n" + "=" * 40)
    print("手动价格更新:")
    market.update_price("AAPL", 145.50)  # 触发低价警报和买入
    market.update_price("TSLA", 820.00)  # 小幅上涨
    market.update_price("GOOGL", 2750.00)  # 小幅下跌
    market.update_price("AAPL", 155.00)  # 上涨，可能触发卖出
    
    # 显示交易机器人表现
    print("\n📊 交易机器人表现:")
    performance = trading_bot.get_performance_summary()
    print(f"   现金余额: ¥{performance['cash']:.2f}")
    print(f"   持仓: {performance['portfolio']}")
    print(f"   总交易次数: {performance['transaction_count']}")
    
    # 显示投资组合价值
    portfolio_value = trading_bot.get_portfolio_value(market)
    print(f"   投资组合总价值: ¥{portfolio_value:.2f}")
    
    # 显示警报历史
    print("\n🚨 警报历史:")
    alert_history = price_alert.get_alert_history()
    for alert in alert_history:
        print(f"   {alert['type']}: {alert['symbol']} @ ¥{alert['current_price']:.2f}")
    
    # 显示波动率报告
    print("\n📊 波动率报告:")
    for symbol in ["AAPL", "TSLA", "GOOGL"]:
        report = market_analyzer.get_volatility_report(symbol)
        if 'error' not in report:
            print(f"   {symbol}: 平均变化 {report['average_change']:+.2f}%, "
                  f"波动率 {report['volatility']:.2f}%")


def demo_real_time_simulation():
    """实时模拟演示"""
    print("\n" + "=" * 60)
    print("⏱️ 实时价格模拟演示 (5秒)")
    print("=" * 60)
    
    market = StockMarket()
    market.add_stock("BTC", 50000.00)
    market.add_stock("ETH", 3000.00)
    
    # 创建简单的观察者
    class SimpleObserver(StockObserver):
        def __init__(self, name):
            self._name = name
        
        @property
        def name(self):
            return self._name
        
        def on_price_change(self, symbol, old_price, new_price, change_percent):
            if abs(change_percent) > 2.0:  # 只显示大幅变化
                direction = "📈" if change_percent > 0 else "📉"
                print(f"{direction} {symbol}: {change_percent:+.2f}% → ¥{new_price:.2f}")
    
    observer = SimpleObserver("实时监控")
    market.subscribe(observer)
    
    # 开始模拟
    market.start_simulation()
    time.sleep(5)  # 运行5秒
    market.stop_simulation()


if __name__ == "__main__":
    # 运行股票监控演示
    demo_stock_monitoring()
    
    # 运行实时模拟演示
    demo_real_time_simulation()
    
    print("\n" + "=" * 60)
    print("✅ 实际项目应用演示完成")
    print("💡 学习要点:")
    print("   - 观察者模式在金融系统中的应用")
    print("   - 多种观察者的协同工作")
    print("   - 实时数据处理和分析")
    print("   - 自动化交易策略实现")
    print("   - 异常检测和警报系统")
    print("=" * 60)
