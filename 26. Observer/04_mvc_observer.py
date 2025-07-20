"""
04_mvc_observer.py - MVC架构中的观察者模式

这个示例展示了在MVC（Model-View-Controller）架构中如何使用观察者模式。
模型作为主题，视图作为观察者，当模型数据变化时自动更新所有视图。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


# ==================== 观察者接口 ====================

class Observer(ABC):
    """抽象观察者接口"""
    
    @abstractmethod
    def update(self, subject: 'Model') -> None:
        """当模型更新时被调用"""
        pass


class Subject(ABC):
    """抽象主题接口"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """注册观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"📝 视图 {observer.__class__.__name__} 已注册到模型")
    
    def detach(self, observer: Observer) -> None:
        """注销观察者"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"❌ 视图 {observer.__class__.__name__} 已从模型注销")
    
    def notify(self) -> None:
        """通知所有观察者"""
        print(f"📢 通知 {len(self._observers)} 个视图更新")
        for observer in self._observers:
            observer.update(self)


# ==================== 模型层 ====================

class ProductModel(Subject):
    """产品模型 - 具体主题"""
    
    def __init__(self):
        super().__init__()
        self._products: Dict[str, Dict[str, Any]] = {}
        self._last_updated = datetime.now()
    
    def add_product(self, product_id: str, name: str, price: float, category: str, stock: int) -> None:
        """添加产品"""
        self._products[product_id] = {
            'id': product_id,
            'name': name,
            'price': price,
            'category': category,
            'stock': stock,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self._last_updated = datetime.now()
        print(f"➕ 添加产品: {name} (ID: {product_id})")
        self.notify()
    
    def update_product(self, product_id: str, **kwargs) -> bool:
        """更新产品信息"""
        if product_id not in self._products:
            print(f"❌ 产品 {product_id} 不存在")
            return False
        
        old_data = self._products[product_id].copy()
        for key, value in kwargs.items():
            if key in self._products[product_id]:
                self._products[product_id][key] = value
        
        self._products[product_id]['updated_at'] = datetime.now()
        self._last_updated = datetime.now()
        
        print(f"✏️ 更新产品 {product_id}: {kwargs}")
        self.notify()
        return True
    
    def remove_product(self, product_id: str) -> bool:
        """删除产品"""
        if product_id in self._products:
            product_name = self._products[product_id]['name']
            del self._products[product_id]
            self._last_updated = datetime.now()
            print(f"🗑️ 删除产品: {product_name} (ID: {product_id})")
            self.notify()
            return True
        return False
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """获取单个产品"""
        return self._products.get(product_id)
    
    def get_all_products(self) -> Dict[str, Dict[str, Any]]:
        """获取所有产品"""
        return self._products.copy()
    
    def get_products_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """按分类获取产品"""
        return {pid: product for pid, product in self._products.items() 
                if product['category'] == category}
    
    def get_low_stock_products(self, threshold: int = 10) -> Dict[str, Dict[str, Any]]:
        """获取低库存产品"""
        return {pid: product for pid, product in self._products.items() 
                if product['stock'] <= threshold}
    
    @property
    def last_updated(self) -> datetime:
        return self._last_updated
    
    @property
    def product_count(self) -> int:
        return len(self._products)


# ==================== 视图层 ====================

class ListView(Observer):
    """列表视图 - 显示产品列表"""
    
    def __init__(self, name: str):
        self._name = name
        self._displayed_products: List[Dict[str, Any]] = []
    
    def update(self, subject: ProductModel) -> None:
        """更新产品列表显示"""
        products = subject.get_all_products()
        self._displayed_products = list(products.values())
        self._display_list()
    
    def _display_list(self) -> None:
        """显示产品列表"""
        print(f"\n📋 {self._name} - 产品列表:")
        if not self._displayed_products:
            print("   暂无产品")
            return
        
        print(f"   {'ID':<10} {'名称':<15} {'价格':<8} {'分类':<10} {'库存':<6}")
        print("   " + "-" * 55)
        for product in self._displayed_products:
            print(f"   {product['id']:<10} {product['name']:<15} "
                  f"¥{product['price']:<7.2f} {product['category']:<10} {product['stock']:<6}")


class DetailView(Observer):
    """详情视图 - 显示产品详细信息"""
    
    def __init__(self, name: str, focus_product_id: Optional[str] = None):
        self._name = name
        self._focus_product_id = focus_product_id
        self._current_product: Optional[Dict[str, Any]] = None
    
    def set_focus_product(self, product_id: str) -> None:
        """设置关注的产品"""
        self._focus_product_id = product_id
    
    def update(self, subject: ProductModel) -> None:
        """更新产品详情显示"""
        if self._focus_product_id:
            self._current_product = subject.get_product(self._focus_product_id)
            self._display_detail()
    
    def _display_detail(self) -> None:
        """显示产品详情"""
        print(f"\n🔍 {self._name} - 产品详情:")
        if not self._current_product:
            print(f"   产品 {self._focus_product_id} 不存在或已删除")
            return
        
        product = self._current_product
        print(f"   产品ID: {product['id']}")
        print(f"   名称: {product['name']}")
        print(f"   价格: ¥{product['price']:.2f}")
        print(f"   分类: {product['category']}")
        print(f"   库存: {product['stock']} 件")
        print(f"   创建时间: {product['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   更新时间: {product['updated_at'].strftime('%Y-%m-%d %H:%M:%S')}")


class ChartView(Observer):
    """图表视图 - 显示统计图表"""
    
    def __init__(self, name: str):
        self._name = name
        self._category_stats: Dict[str, int] = {}
        self._price_stats: Dict[str, float] = {}
    
    def update(self, subject: ProductModel) -> None:
        """更新统计图表"""
        products = subject.get_all_products()
        self._calculate_stats(products)
        self._display_chart()
    
    def _calculate_stats(self, products: Dict[str, Dict[str, Any]]) -> None:
        """计算统计数据"""
        # 按分类统计数量
        self._category_stats = {}
        price_by_category = {}
        
        for product in products.values():
            category = product['category']
            price = product['price']
            
            # 数量统计
            if category not in self._category_stats:
                self._category_stats[category] = 0
                price_by_category[category] = []
            
            self._category_stats[category] += 1
            price_by_category[category].append(price)
        
        # 计算平均价格
        self._price_stats = {}
        for category, prices in price_by_category.items():
            self._price_stats[category] = sum(prices) / len(prices) if prices else 0
    
    def _display_chart(self) -> None:
        """显示图表"""
        print(f"\n📊 {self._name} - 统计图表:")
        
        if not self._category_stats:
            print("   暂无数据")
            return
        
        print("   分类数量统计:")
        for category, count in self._category_stats.items():
            bar = "█" * min(count, 20)  # 最多显示20个字符
            print(f"   {category:<10} {bar} ({count})")
        
        print("\n   分类平均价格:")
        for category, avg_price in self._price_stats.items():
            print(f"   {category:<10} ¥{avg_price:.2f}")


class AlertView(Observer):
    """警报视图 - 显示库存警报"""
    
    def __init__(self, name: str, stock_threshold: int = 5):
        self._name = name
        self._stock_threshold = stock_threshold
        self._alerts: List[str] = []
    
    def update(self, subject: ProductModel) -> None:
        """检查库存警报"""
        low_stock_products = subject.get_low_stock_products(self._stock_threshold)
        self._alerts = []
        
        for product in low_stock_products.values():
            if product['stock'] == 0:
                alert = f"⚠️ 缺货警报: {product['name']} (ID: {product['id']})"
            else:
                alert = f"⚠️ 低库存警报: {product['name']} 仅剩 {product['stock']} 件"
            self._alerts.append(alert)
        
        self._display_alerts()
    
    def _display_alerts(self) -> None:
        """显示警报"""
        print(f"\n🚨 {self._name} - 库存警报:")
        if not self._alerts:
            print("   ✅ 库存正常")
        else:
            for alert in self._alerts:
                print(f"   {alert}")


# ==================== 控制器层 ====================

class ProductController:
    """产品控制器"""
    
    def __init__(self, model: ProductModel):
        self._model = model
    
    def create_product(self, product_id: str, name: str, price: float, 
                      category: str, stock: int) -> bool:
        """创建产品"""
        try:
            self._model.add_product(product_id, name, price, category, stock)
            return True
        except Exception as e:
            print(f"❌ 创建产品失败: {e}")
            return False
    
    def update_product_price(self, product_id: str, new_price: float) -> bool:
        """更新产品价格"""
        return self._model.update_product(product_id, price=new_price)
    
    def update_product_stock(self, product_id: str, new_stock: int) -> bool:
        """更新产品库存"""
        return self._model.update_product(product_id, stock=new_stock)
    
    def delete_product(self, product_id: str) -> bool:
        """删除产品"""
        return self._model.remove_product(product_id)
    
    def restock_product(self, product_id: str, quantity: int) -> bool:
        """补充库存"""
        product = self._model.get_product(product_id)
        if product:
            new_stock = product['stock'] + quantity
            return self._model.update_product(product_id, stock=new_stock)
        return False


# ==================== 演示函数 ====================

def demo_mvc_observer():
    """MVC观察者模式演示"""
    print("=" * 60)
    print("🏗️ MVC架构观察者模式演示")
    print("=" * 60)
    
    # 创建模型
    product_model = ProductModel()
    
    # 创建视图
    list_view = ListView("主页产品列表")
    detail_view = DetailView("产品详情页", "P001")
    chart_view = ChartView("数据分析面板")
    alert_view = AlertView("库存监控", stock_threshold=10)
    
    # 注册视图到模型
    print("\n📋 注册视图:")
    product_model.attach(list_view)
    product_model.attach(detail_view)
    product_model.attach(chart_view)
    product_model.attach(alert_view)
    
    # 创建控制器
    controller = ProductController(product_model)
    
    # 模拟用户操作
    print("\n" + "=" * 40)
    print("用户操作序列:")
    
    # 添加产品
    print("\n1. 添加产品:")
    controller.create_product("P001", "iPhone 15", 6999.0, "手机", 50)
    controller.create_product("P002", "MacBook Pro", 12999.0, "电脑", 8)
    controller.create_product("P003", "AirPods", 1299.0, "配件", 3)
    
    # 更新价格
    print("\n2. 更新产品价格:")
    controller.update_product_price("P001", 6499.0)
    
    # 更新库存
    print("\n3. 更新库存:")
    controller.update_product_stock("P002", 2)  # 触发低库存警报
    
    # 补充库存
    print("\n4. 补充库存:")
    controller.restock_product("P003", 20)
    
    # 删除产品
    print("\n5. 删除产品:")
    controller.delete_product("P002")
    
    # 切换详情视图关注的产品
    print("\n6. 切换详情视图:")
    detail_view.set_focus_product("P003")
    # 手动触发更新以显示新的关注产品
    detail_view.update(product_model)


def demo_view_management():
    """视图管理演示"""
    print("\n" + "=" * 60)
    print("🖥️ 视图管理演示")
    print("=" * 60)
    
    model = ProductModel()
    
    # 创建多个相同类型的视图
    mobile_list = ListView("手机端列表")
    web_list = ListView("网页端列表")
    admin_list = ListView("管理端列表")
    
    # 注册视图
    model.attach(mobile_list)
    model.attach(web_list)
    
    # 添加产品
    model.add_product("T001", "测试产品", 99.0, "测试", 100)
    
    # 动态添加新视图
    print("\n添加管理端视图:")
    model.attach(admin_list)
    
    # 再次更新
    model.update_product("T001", price=89.0)
    
    # 移除某个视图
    print("\n移除手机端视图:")
    model.detach(mobile_list)
    
    # 最后更新
    model.update_product("T001", stock=50)


if __name__ == "__main__":
    # 运行MVC演示
    demo_mvc_observer()
    
    # 运行视图管理演示
    demo_view_management()
    
    print("\n" + "=" * 60)
    print("✅ MVC观察者模式演示完成")
    print("💡 学习要点:")
    print("   - 模型作为主题，视图作为观察者")
    print("   - 数据变化时自动更新所有视图")
    print("   - 控制器负责处理用户输入")
    print("   - 视图可以动态注册和注销")
    print("   - 不同视图可以显示不同的数据维度")
    print("=" * 60)
