"""
01_basic_observer.py - 观察者模式基础实现

这个示例展示了观察者模式的核心概念和基本实现。
通过一个简单的新闻发布系统来演示主题和观察者之间的关系。
"""

from abc import ABC, abstractmethod
from typing import List


# ==================== 抽象接口 ====================

class Observer(ABC):
    """抽象观察者接口"""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        """当主题状态改变时被调用的更新方法"""
        pass


class Subject(ABC):
    """抽象主题接口"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """注册观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"📝 观察者 {observer.__class__.__name__} 已注册")
    
    def detach(self, observer: Observer) -> None:
        """注销观察者"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"❌ 观察者 {observer.__class__.__name__} 已注销")
    
    def notify(self) -> None:
        """通知所有观察者"""
        print(f"📢 通知 {len(self._observers)} 个观察者")
        for observer in self._observers:
            observer.update(self)


# ==================== 具体实现 ====================

class NewsAgency(Subject):
    """新闻机构 - 具体主题"""
    
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._news = ""
        self._category = ""
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def news(self) -> str:
        return self._news
    
    @property
    def category(self) -> str:
        return self._category
    
    def publish_news(self, news: str, category: str = "综合") -> None:
        """发布新闻"""
        self._news = news
        self._category = category
        print(f"\n🏢 {self._name} 发布新闻:")
        print(f"   分类: {category}")
        print(f"   内容: {news}")
        self.notify()


class NewsChannel(Observer):
    """新闻频道 - 具体观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._latest_news = ""
    
    @property
    def name(self) -> str:
        return self._name
    
    def update(self, subject: NewsAgency) -> None:
        """接收新闻更新"""
        self._latest_news = subject.news
        print(f"📺 {self._name} 收到新闻: {subject.news}")
    
    def display_news(self) -> None:
        """显示最新新闻"""
        if self._latest_news:
            print(f"📺 {self._name} 正在播报: {self._latest_news}")
        else:
            print(f"📺 {self._name} 暂无新闻")


class Newspaper(Observer):
    """报纸 - 具体观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._news_archive: List[str] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    def update(self, subject: NewsAgency) -> None:
        """接收新闻更新"""
        news_item = f"[{subject.category}] {subject.news}"
        self._news_archive.append(news_item)
        print(f"📰 {self._name} 记录新闻: {news_item}")
    
    def print_archive(self) -> None:
        """打印新闻存档"""
        print(f"\n📰 {self._name} 新闻存档:")
        for i, news in enumerate(self._news_archive, 1):
            print(f"   {i}. {news}")


class MobileApp(Observer):
    """手机应用 - 具体观察者"""
    
    def __init__(self, name: str):
        self._name = name
        self._notifications: List[str] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    def update(self, subject: NewsAgency) -> None:
        """接收新闻更新"""
        notification = f"来自{subject.name}: {subject.news}"
        self._notifications.append(notification)
        print(f"📱 {self._name} 推送通知: {notification}")
    
    def show_notifications(self) -> None:
        """显示通知列表"""
        print(f"\n📱 {self._name} 通知列表:")
        for i, notification in enumerate(self._notifications, 1):
            print(f"   {i}. {notification}")


# ==================== 演示函数 ====================

def demo_basic_observer():
    """基础观察者模式演示"""
    print("=" * 60)
    print("🎯 观察者模式基础演示 - 新闻发布系统")
    print("=" * 60)
    
    # 创建新闻机构（主题）
    cnn = NewsAgency("CNN新闻")
    
    # 创建观察者
    tv_channel = NewsChannel("新闻频道")
    daily_paper = Newspaper("每日新闻报")
    news_app = MobileApp("新闻快报App")
    
    # 注册观察者
    print("\n📋 注册观察者:")
    cnn.attach(tv_channel)
    cnn.attach(daily_paper)
    cnn.attach(news_app)
    
    # 发布第一条新闻
    print("\n" + "=" * 40)
    cnn.publish_news("科技公司发布新产品", "科技")
    
    # 发布第二条新闻
    print("\n" + "=" * 40)
    cnn.publish_news("股市今日大涨3%", "财经")
    
    # 注销一个观察者
    print("\n📋 注销观察者:")
    cnn.detach(tv_channel)
    
    # 发布第三条新闻
    print("\n" + "=" * 40)
    cnn.publish_news("新的环保政策即将实施", "政策")
    
    # 显示各观察者的状态
    print("\n" + "=" * 40)
    print("📊 观察者状态总结:")
    tv_channel.display_news()
    daily_paper.print_archive()
    news_app.show_notifications()


def demo_dynamic_subscription():
    """动态订阅演示"""
    print("\n" + "=" * 60)
    print("🔄 动态订阅演示")
    print("=" * 60)
    
    # 创建体育新闻机构
    sports_news = NewsAgency("体育新闻网")
    
    # 创建观察者
    sports_channel = NewsChannel("体育频道")
    sports_app = MobileApp("体育资讯App")
    
    # 动态订阅和取消订阅
    print("\n📱 体育App订阅体育新闻:")
    sports_news.attach(sports_app)
    sports_news.publish_news("足球世界杯决赛今晚开始", "体育")
    
    print("\n📺 体育频道也订阅体育新闻:")
    sports_news.attach(sports_channel)
    sports_news.publish_news("篮球联赛季后赛激战正酣", "体育")
    
    print("\n📱 体育App取消订阅:")
    sports_news.detach(sports_app)
    sports_news.publish_news("游泳世锦赛破多项纪录", "体育")


if __name__ == "__main__":
    # 运行基础演示
    demo_basic_observer()
    
    # 运行动态订阅演示
    demo_dynamic_subscription()
    
    print("\n" + "=" * 60)
    print("✅ 观察者模式基础演示完成")
    print("=" * 60)
