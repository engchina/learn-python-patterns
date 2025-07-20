"""
02_weather_station.py - 天气监测站观察者模式

这个示例展示了一个更实际的观察者模式应用场景：天气监测站。
演示了推模式和拉模式的区别，以及多种显示设备的同步更新。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
from datetime import datetime


# ==================== 抽象接口 ====================

class Observer(ABC):
    """抽象观察者接口"""
    
    @abstractmethod
    def update(self, subject: 'WeatherStation') -> None:
        """更新方法 - 拉模式"""
        pass


class PushObserver(ABC):
    """推模式观察者接口"""
    
    @abstractmethod
    def update_weather(self, temperature: float, humidity: float, pressure: float) -> None:
        """更新方法 - 推模式"""
        pass


class Subject(ABC):
    """抽象主题接口"""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._push_observers: List[PushObserver] = []
    
    def attach(self, observer: Observer) -> None:
        """注册拉模式观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"🔗 拉模式观察者 {observer.__class__.__name__} 已注册")
    
    def attach_push(self, observer: PushObserver) -> None:
        """注册推模式观察者"""
        if observer not in self._push_observers:
            self._push_observers.append(observer)
            print(f"📤 推模式观察者 {observer.__class__.__name__} 已注册")
    
    def detach(self, observer: Observer) -> None:
        """注销拉模式观察者"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"❌ 拉模式观察者 {observer.__class__.__name__} 已注销")
    
    def detach_push(self, observer: PushObserver) -> None:
        """注销推模式观察者"""
        if observer in self._push_observers:
            self._push_observers.remove(observer)
            print(f"❌ 推模式观察者 {observer.__class__.__name__} 已注销")
    
    def notify(self) -> None:
        """通知所有拉模式观察者"""
        for observer in self._observers:
            observer.update(self)
    
    def notify_push(self, temperature: float, humidity: float, pressure: float) -> None:
        """通知所有推模式观察者"""
        for observer in self._push_observers:
            observer.update_weather(temperature, humidity, pressure)


# ==================== 具体主题 ====================

class WeatherStation(Subject):
    """天气监测站 - 具体主题"""
    
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0
        self._timestamp = datetime.now()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @property
    def humidity(self) -> float:
        return self._humidity
    
    @property
    def pressure(self) -> float:
        return self._pressure
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        """设置天气测量数据"""
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self._timestamp = datetime.now()
        
        print(f"\n🌡️ {self._name} 数据更新:")
        print(f"   温度: {temperature}°C")
        print(f"   湿度: {humidity}%")
        print(f"   气压: {pressure} hPa")
        print(f"   时间: {self._timestamp.strftime('%H:%M:%S')}")
        
        # 同时通知拉模式和推模式观察者
        self.notify()
        self.notify_push(temperature, humidity, pressure)
    
    def get_weather_data(self) -> Dict[str, Any]:
        """获取完整天气数据"""
        return {
            'temperature': self._temperature,
            'humidity': self._humidity,
            'pressure': self._pressure,
            'timestamp': self._timestamp,
            'station': self._name
        }


# ==================== 拉模式观察者 ====================

class CurrentConditionsDisplay(Observer):
    """当前状况显示 - 拉模式观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0
    
    def update(self, subject: WeatherStation) -> None:
        """从主题拉取数据并更新显示"""
        # 拉模式：主动从主题获取数据
        self._temperature = subject.temperature
        self._humidity = subject.humidity
        self._pressure = subject.pressure
        self.display()
    
    def display(self) -> None:
        """显示当前天气状况"""
        print(f"📺 {self._name} - 当前状况:")
        print(f"   温度: {self._temperature}°C")
        print(f"   湿度: {self._humidity}%")
        print(f"   气压: {self._pressure} hPa")


class StatisticsDisplay(Observer):
    """统计显示 - 拉模式观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._temperatures: List[float] = []
        self._humidity_values: List[float] = []
        self._pressure_values: List[float] = []
    
    def update(self, subject: WeatherStation) -> None:
        """收集统计数据"""
        self._temperatures.append(subject.temperature)
        self._humidity_values.append(subject.humidity)
        self._pressure_values.append(subject.pressure)
        self.display()
    
    def display(self) -> None:
        """显示统计信息"""
        if self._temperatures:
            avg_temp = sum(self._temperatures) / len(self._temperatures)
            max_temp = max(self._temperatures)
            min_temp = min(self._temperatures)
            
            print(f"📊 {self._name} - 统计信息:")
            print(f"   温度: 平均{avg_temp:.1f}°C, 最高{max_temp}°C, 最低{min_temp}°C")
            print(f"   数据点数: {len(self._temperatures)}")


# ==================== 推模式观察者 ====================

class WeatherAlert(PushObserver):
    """天气警报 - 推模式观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._alert_conditions = {
            'high_temp': 35.0,
            'low_temp': -10.0,
            'high_humidity': 90.0,
            'low_pressure': 980.0
        }
    
    def update_weather(self, temperature: float, humidity: float, pressure: float) -> None:
        """接收推送的天气数据并检查警报条件"""
        alerts = []
        
        if temperature > self._alert_conditions['high_temp']:
            alerts.append(f"高温警报: {temperature}°C")
        elif temperature < self._alert_conditions['low_temp']:
            alerts.append(f"低温警报: {temperature}°C")
        
        if humidity > self._alert_conditions['high_humidity']:
            alerts.append(f"高湿度警报: {humidity}%")
        
        if pressure < self._alert_conditions['low_pressure']:
            alerts.append(f"低气压警报: {pressure} hPa")
        
        if alerts:
            print(f"🚨 {self._name} - 天气警报:")
            for alert in alerts:
                print(f"   ⚠️ {alert}")
        else:
            print(f"✅ {self._name} - 天气正常")


class MobileNotification(PushObserver):
    """手机通知 - 推模式观察者"""
    
    def __init__(self, user_name: str):
        self._user_name = user_name
        self._notifications: List[str] = []
    
    def update_weather(self, temperature: float, humidity: float, pressure: float) -> None:
        """接收天气数据并生成通知"""
        # 简化的通知逻辑
        weather_desc = self._get_weather_description(temperature, humidity)
        notification = f"天气更新: {weather_desc}, {temperature}°C"
        self._notifications.append(notification)
        
        print(f"📱 {self._user_name}的手机 - 新通知:")
        print(f"   {notification}")
    
    def _get_weather_description(self, temperature: float, humidity: float) -> str:
        """根据温度和湿度生成天气描述"""
        if temperature > 30:
            return "炎热"
        elif temperature > 20:
            return "温暖"
        elif temperature > 10:
            return "凉爽"
        else:
            return "寒冷"
    
    def show_notifications(self) -> None:
        """显示所有通知"""
        print(f"\n📱 {self._user_name}的通知历史:")
        for i, notification in enumerate(self._notifications, 1):
            print(f"   {i}. {notification}")


# ==================== 演示函数 ====================

def demo_weather_station():
    """天气监测站演示"""
    print("=" * 60)
    print("🌤️ 天气监测站观察者模式演示")
    print("=" * 60)
    
    # 创建天气监测站
    station = WeatherStation("北京气象站")
    
    # 创建拉模式观察者
    current_display = CurrentConditionsDisplay("大厅显示屏")
    statistics_display = StatisticsDisplay("统计分析系统")
    
    # 创建推模式观察者
    weather_alert = WeatherAlert("天气警报系统")
    mobile_notification = MobileNotification("张三")
    
    # 注册观察者
    print("\n📋 注册观察者:")
    station.attach(current_display)
    station.attach(statistics_display)
    station.attach_push(weather_alert)
    station.attach_push(mobile_notification)
    
    # 模拟天气数据更新
    print("\n" + "=" * 40)
    print("第一次测量:")
    station.set_measurements(25.0, 65.0, 1013.2)
    
    print("\n" + "=" * 40)
    print("第二次测量:")
    station.set_measurements(28.0, 70.0, 1015.5)
    
    print("\n" + "=" * 40)
    print("第三次测量 - 高温警报:")
    station.set_measurements(36.0, 85.0, 1010.0)
    
    print("\n" + "=" * 40)
    print("第四次测量 - 低气压警报:")
    station.set_measurements(22.0, 75.0, 975.0)
    
    # 显示通知历史
    mobile_notification.show_notifications()


if __name__ == "__main__":
    demo_weather_station()
    
    print("\n" + "=" * 60)
    print("✅ 天气监测站演示完成")
    print("💡 学习要点:")
    print("   - 拉模式：观察者主动从主题获取数据")
    print("   - 推模式：主题主动推送数据给观察者")
    print("   - 不同观察者可以有不同的响应逻辑")
    print("=" * 60)
