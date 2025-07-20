"""
06_composition_example.py - 组合关系的应用

这个示例通过汽车制造系统展示组合的核心概念：
- 对象间的组合关系
- "有一个"关系 vs "是一个"关系
- 复杂对象的构建
- 组合与继承的区别
"""

from typing import List, Dict, Optional
from datetime import datetime, date
from enum import Enum


# ==================== 枚举类型 ====================
class EngineType(Enum):
    """发动机类型"""
    GASOLINE = "汽油发动机"
    DIESEL = "柴油发动机"
    ELECTRIC = "电动机"
    HYBRID = "混合动力"


class TransmissionType(Enum):
    """变速箱类型"""
    MANUAL = "手动变速箱"
    AUTOMATIC = "自动变速箱"
    CVT = "无级变速箱"


class TireType(Enum):
    """轮胎类型"""
    SUMMER = "夏季轮胎"
    WINTER = "冬季轮胎"
    ALL_SEASON = "四季轮胎"
    PERFORMANCE = "高性能轮胎"


# ==================== 汽车组件类 ====================
class Engine:
    """发动机类 - 汽车的核心组件"""
    
    def __init__(self, engine_type: EngineType, displacement: float, 
                 horsepower: int, manufacturer: str):
        """
        初始化发动机
        
        参数:
            engine_type: 发动机类型
            displacement: 排量(L)
            horsepower: 马力
            manufacturer: 制造商
        """
        self.engine_type = engine_type
        self.displacement = displacement
        self.horsepower = horsepower
        self.manufacturer = manufacturer
        self.is_running = False
        self.temperature = 20  # 温度(°C)
        self.mileage = 0  # 里程
        self.maintenance_due = False
        
        print(f"🔧 {engine_type.value} 已制造完成 ({horsepower}马力)")
    
    def start(self) -> str:
        """启动发动机"""
        if self.is_running:
            return "发动机已经在运行"
        
        self.is_running = True
        self.temperature = 90
        return f"🚗 {self.engine_type.value} 启动成功"
    
    def stop(self) -> str:
        """停止发动机"""
        if not self.is_running:
            return "发动机已经停止"
        
        self.is_running = False
        self.temperature = 20
        return f"🛑 {self.engine_type.value} 已停止"
    
    def accelerate(self, rpm: int) -> str:
        """加速"""
        if not self.is_running:
            return "发动机未启动，无法加速"
        
        if rpm > 6000:
            return "⚠️  转速过高，请注意安全"
        
        return f"🏃 发动机转速提升至 {rpm} RPM"
    
    def check_maintenance(self) -> bool:
        """检查是否需要保养"""
        if self.mileage > 10000:
            self.maintenance_due = True
        return self.maintenance_due
    
    def perform_maintenance(self):
        """执行保养"""
        self.maintenance_due = False
        self.mileage = 0
        print(f"🔧 {self.engine_type.value} 保养完成")
    
    def get_info(self) -> str:
        """获取发动机信息"""
        status = "运行中" if self.is_running else "停止"
        maintenance = "需要保养" if self.maintenance_due else "状态良好"
        
        return (f"🔧 发动机信息:\n"
                f"   类型: {self.engine_type.value}\n"
                f"   排量: {self.displacement}L\n"
                f"   马力: {self.horsepower}HP\n"
                f"   制造商: {self.manufacturer}\n"
                f"   状态: {status}\n"
                f"   温度: {self.temperature}°C\n"
                f"   里程: {self.mileage}km\n"
                f"   保养状态: {maintenance}")
    
    def __str__(self) -> str:
        return f"{self.engine_type.value}({self.horsepower}HP)"


class Transmission:
    """变速箱类"""
    
    def __init__(self, transmission_type: TransmissionType, gears: int, manufacturer: str):
        """
        初始化变速箱
        
        参数:
            transmission_type: 变速箱类型
            gears: 档位数
            manufacturer: 制造商
        """
        self.transmission_type = transmission_type
        self.gears = gears
        self.manufacturer = manufacturer
        self.current_gear = 0  # 当前档位（0=停车档）
        self.is_engaged = False
        
        print(f"⚙️  {transmission_type.value} 已制造完成 ({gears}档)")
    
    def engage(self) -> str:
        """接合变速箱"""
        self.is_engaged = True
        return f"⚙️  {self.transmission_type.value} 已接合"
    
    def disengage(self) -> str:
        """分离变速箱"""
        self.is_engaged = False
        self.current_gear = 0
        return f"⚙️  {self.transmission_type.value} 已分离"
    
    def shift_gear(self, gear: int) -> str:
        """换档"""
        if not self.is_engaged:
            return "变速箱未接合，无法换档"
        
        if gear < 0 or gear > self.gears:
            return f"无效档位，有效范围: 0-{self.gears}"
        
        old_gear = self.current_gear
        self.current_gear = gear
        
        if gear == 0:
            return "🅿️  切换到停车档"
        elif gear == 1:
            return "1️⃣  切换到1档"
        else:
            return f"⬆️  从{old_gear}档切换到{gear}档"
    
    def get_info(self) -> str:
        """获取变速箱信息"""
        status = "接合" if self.is_engaged else "分离"
        gear_info = f"{self.current_gear}档" if self.current_gear > 0 else "停车档"
        
        return (f"⚙️  变速箱信息:\n"
                f"   类型: {self.transmission_type.value}\n"
                f"   档位数: {self.gears}\n"
                f"   制造商: {self.manufacturer}\n"
                f"   状态: {status}\n"
                f"   当前档位: {gear_info}")
    
    def __str__(self) -> str:
        return f"{self.transmission_type.value}({self.gears}档)"


class Tire:
    """轮胎类"""
    
    def __init__(self, tire_type: TireType, size: str, brand: str):
        """
        初始化轮胎
        
        参数:
            tire_type: 轮胎类型
            size: 尺寸
            brand: 品牌
        """
        self.tire_type = tire_type
        self.size = size
        self.brand = brand
        self.pressure = 2.3  # 胎压(bar)
        self.wear_level = 0  # 磨损程度(0-100%)
        self.is_flat = False
        
        print(f"🛞 {tire_type.value} 已制造完成 ({size})")
    
    def inflate(self, pressure: float) -> str:
        """充气"""
        if pressure < 1.8 or pressure > 3.0:
            return "⚠️  胎压超出安全范围(1.8-3.0 bar)"
        
        self.pressure = pressure
        return f"💨 轮胎充气至 {pressure} bar"
    
    def check_pressure(self) -> str:
        """检查胎压"""
        if self.pressure < 2.0:
            return "⚠️  胎压过低，需要充气"
        elif self.pressure > 2.8:
            return "⚠️  胎压过高，需要放气"
        else:
            return "✅ 胎压正常"
    
    def wear(self, amount: float):
        """磨损"""
        self.wear_level = min(100, self.wear_level + amount)
        if self.wear_level > 80:
            print(f"⚠️  轮胎磨损严重({self.wear_level:.1f}%)，建议更换")
    
    def puncture(self):
        """爆胎"""
        self.is_flat = True
        self.pressure = 0
        print(f"💥 轮胎爆胎!")
    
    def repair(self):
        """修补"""
        if self.is_flat:
            self.is_flat = False
            self.pressure = 2.3
            print(f"🔧 轮胎修补完成")
    
    def get_info(self) -> str:
        """获取轮胎信息"""
        condition = "爆胎" if self.is_flat else f"磨损{self.wear_level:.1f}%"
        
        return (f"🛞 轮胎信息:\n"
                f"   类型: {self.tire_type.value}\n"
                f"   尺寸: {self.size}\n"
                f"   品牌: {self.brand}\n"
                f"   胎压: {self.pressure} bar\n"
                f"   状态: {condition}")
    
    def __str__(self) -> str:
        return f"{self.brand} {self.tire_type.value}({self.size})"


class GPS:
    """GPS导航系统类"""
    
    def __init__(self, brand: str, has_voice: bool = True):
        """
        初始化GPS系统
        
        参数:
            brand: 品牌
            has_voice: 是否有语音导航
        """
        self.brand = brand
        self.has_voice = has_voice
        self.is_on = False
        self.current_location = (0.0, 0.0)  # 经纬度
        self.destination = None
        self.route_calculated = False
        
        print(f"🗺️  {brand} GPS导航系统已安装")
    
    def power_on(self) -> str:
        """开机"""
        self.is_on = True
        return f"📡 {self.brand} GPS已启动"
    
    def power_off(self) -> str:
        """关机"""
        self.is_on = False
        return f"📴 {self.brand} GPS已关闭"
    
    def set_destination(self, address: str) -> str:
        """设置目的地"""
        if not self.is_on:
            return "GPS未启动"
        
        self.destination = address
        self.route_calculated = True
        return f"🎯 目的地已设置: {address}"
    
    def navigate(self) -> str:
        """开始导航"""
        if not self.is_on:
            return "GPS未启动"
        
        if not self.destination:
            return "请先设置目的地"
        
        voice_msg = "语音导航已开启" if self.has_voice else "请查看屏幕指示"
        return f"🧭 导航开始，前往 {self.destination}。{voice_msg}"
    
    def get_info(self) -> str:
        """获取GPS信息"""
        status = "开启" if self.is_on else "关闭"
        dest = self.destination if self.destination else "未设置"
        
        return (f"🗺️  GPS信息:\n"
                f"   品牌: {self.brand}\n"
                f"   状态: {status}\n"
                f"   语音导航: {'支持' if self.has_voice else '不支持'}\n"
                f"   目的地: {dest}")
    
    def __str__(self) -> str:
        return f"{self.brand} GPS导航"


# ==================== 汽车类（组合示例）====================
class Car:
    """汽车类 - 展示组合关系的核心应用"""
    
    def __init__(self, make: str, model: str, year: int, color: str):
        """
        初始化汽车
        
        参数:
            make: 制造商
            model: 型号
            year: 年份
            color: 颜色
        """
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.vin = self._generate_vin()
        self.mileage = 0
        self.is_running = False
        
        # 组合关系：汽车"有一个"发动机、变速箱等
        self.engine: Optional[Engine] = None
        self.transmission: Optional[Transmission] = None
        self.tires: List[Tire] = []
        self.gps: Optional[GPS] = None
        
        # 其他属性
        self.fuel_level = 100  # 燃油水平(%)
        self.speed = 0  # 当前速度
        self.maintenance_records: List[Dict] = []
        
        print(f"🚗 {year} {make} {model} 车架已制造完成")
    
    def _generate_vin(self) -> str:
        """生成车辆识别号"""
        import random
        return f"VIN{random.randint(100000, 999999)}"
    
    # ==================== 组件安装方法 ====================
    def install_engine(self, engine: Engine):
        """安装发动机"""
        self.engine = engine
        print(f"🔧 发动机已安装到 {self.make} {self.model}")
    
    def install_transmission(self, transmission: Transmission):
        """安装变速箱"""
        self.transmission = transmission
        print(f"🔧 变速箱已安装到 {self.make} {self.model}")
    
    def install_tires(self, tires: List[Tire]):
        """安装轮胎"""
        if len(tires) != 4:
            print("❌ 需要安装4个轮胎")
            return
        
        self.tires = tires
        print(f"🔧 4个轮胎已安装到 {self.make} {self.model}")
    
    def install_gps(self, gps: GPS):
        """安装GPS"""
        self.gps = gps
        print(f"🔧 GPS已安装到 {self.make} {self.model}")
    
    # ==================== 汽车操作方法 ====================
    def start_car(self) -> str:
        """启动汽车"""
        if not self._check_components():
            return "❌ 汽车组件不完整，无法启动"
        
        if self.is_running:
            return "汽车已经启动"
        
        # 启动各个组件
        results = []
        results.append(self.engine.start())
        results.append(self.transmission.engage())
        
        if self.gps:
            results.append(self.gps.power_on())
        
        self.is_running = True
        results.append(f"🚗 {self.make} {self.model} 启动成功")
        
        return "\n".join(results)
    
    def stop_car(self) -> str:
        """停止汽车"""
        if not self.is_running:
            return "汽车已经停止"
        
        results = []
        self.speed = 0
        
        if self.transmission:
            results.append(self.transmission.shift_gear(0))
            results.append(self.transmission.disengage())
        
        if self.engine:
            results.append(self.engine.stop())
        
        self.is_running = False
        results.append(f"🛑 {self.make} {self.model} 已停止")
        
        return "\n".join(results)
    
    def accelerate(self, target_speed: int) -> str:
        """加速"""
        if not self.is_running:
            return "汽车未启动"
        
        if target_speed > 180:
            return "⚠️  速度过快，请注意安全"
        
        results = []
        
        # 根据速度自动换档
        if target_speed > 0 and self.transmission.current_gear == 0:
            results.append(self.transmission.shift_gear(1))
        elif target_speed > 30 and self.transmission.current_gear == 1:
            results.append(self.transmission.shift_gear(2))
        elif target_speed > 60 and self.transmission.current_gear == 2:
            results.append(self.transmission.shift_gear(3))
        
        # 发动机加速
        rpm = target_speed * 30  # 简化的RPM计算
        results.append(self.engine.accelerate(rpm))
        
        self.speed = target_speed
        self.fuel_level = max(0, self.fuel_level - target_speed * 0.1)
        
        # 轮胎磨损
        for tire in self.tires:
            tire.wear(target_speed * 0.01)
        
        results.append(f"🏃 当前速度: {self.speed} km/h")
        
        return "\n".join(results)
    
    def brake(self) -> str:
        """刹车"""
        if self.speed == 0:
            return "汽车已经停止"
        
        self.speed = max(0, self.speed - 30)
        
        if self.speed == 0:
            return "🛑 汽车已停止"
        else:
            return f"🚗 减速至 {self.speed} km/h"
    
    def refuel(self, amount: float) -> str:
        """加油"""
        if amount <= 0:
            return "加油量必须大于0"
        
        old_level = self.fuel_level
        self.fuel_level = min(100, self.fuel_level + amount)
        added = self.fuel_level - old_level
        
        return f"⛽ 加油 {added:.1f}%，当前油量: {self.fuel_level:.1f}%"
    
    # ==================== 检查和维护方法 ====================
    def _check_components(self) -> bool:
        """检查组件完整性"""
        return (self.engine is not None and 
                self.transmission is not None and 
                len(self.tires) == 4)
    
    def check_tire_pressure(self) -> str:
        """检查轮胎胎压"""
        if not self.tires:
            return "未安装轮胎"
        
        results = []
        for i, tire in enumerate(self.tires, 1):
            results.append(f"轮胎{i}: {tire.check_pressure()}")
        
        return "\n".join(results)
    
    def perform_maintenance(self):
        """执行保养"""
        maintenance_record = {
            "date": date.today(),
            "mileage": self.mileage,
            "items": []
        }
        
        # 发动机保养
        if self.engine and self.engine.check_maintenance():
            self.engine.perform_maintenance()
            maintenance_record["items"].append("发动机保养")
        
        # 轮胎检查
        for i, tire in enumerate(self.tires, 1):
            if tire.wear_level > 80:
                print(f"🔧 更换轮胎{i}")
                maintenance_record["items"].append(f"更换轮胎{i}")
                tire.wear_level = 0
        
        self.maintenance_records.append(maintenance_record)
        print(f"🔧 {self.make} {self.model} 保养完成")
    
    def get_car_info(self) -> str:
        """获取汽车信息"""
        component_status = "完整" if self._check_components() else "不完整"
        running_status = "运行中" if self.is_running else "停止"
        
        info = [
            f"🚗 汽车信息:",
            f"   制造商: {self.make}",
            f"   型号: {self.model}",
            f"   年份: {self.year}",
            f"   颜色: {self.color}",
            f"   VIN: {self.vin}",
            f"   里程: {self.mileage} km",
            f"   状态: {running_status}",
            f"   速度: {self.speed} km/h",
            f"   油量: {self.fuel_level:.1f}%",
            f"   组件状态: {component_status}",
            f"   保养记录: {len(self.maintenance_records)} 次"
        ]
        
        return "\n".join(info)
    
    def get_detailed_info(self) -> str:
        """获取详细信息"""
        info = [self.get_car_info()]
        
        if self.engine:
            info.append(f"\n{self.engine.get_info()}")
        
        if self.transmission:
            info.append(f"\n{self.transmission.get_info()}")
        
        if self.tires:
            info.append(f"\n🛞 轮胎信息:")
            for i, tire in enumerate(self.tires, 1):
                info.append(f"   轮胎{i}: {tire}")
        
        if self.gps:
            info.append(f"\n{self.gps.get_info()}")
        
        return "\n".join(info)
    
    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model} ({self.color})"


# ==================== 汽车工厂类 ====================
class CarFactory:
    """汽车工厂 - 展示组合关系的构建过程"""
    
    def __init__(self, name: str):
        """初始化汽车工厂"""
        self.name = name
        self.cars_produced = 0
        
        print(f"🏭 {name} 汽车工厂已建立")
    
    def build_economy_car(self, make: str, model: str, year: int, color: str) -> Car:
        """制造经济型汽车"""
        print(f"\n🏭 开始制造经济型汽车: {make} {model}")
        
        # 创建汽车主体
        car = Car(make, model, year, color)
        
        # 安装组件
        engine = Engine(EngineType.GASOLINE, 1.6, 120, "EcoMotors")
        transmission = Transmission(TransmissionType.MANUAL, 5, "BasicGears")
        tires = [Tire(TireType.ALL_SEASON, "195/65R15", "EcoTire") for _ in range(4)]
        
        car.install_engine(engine)
        car.install_transmission(transmission)
        car.install_tires(tires)
        
        self.cars_produced += 1
        print(f"✅ 经济型汽车制造完成")
        return car
    
    def build_luxury_car(self, make: str, model: str, year: int, color: str) -> Car:
        """制造豪华汽车"""
        print(f"\n🏭 开始制造豪华汽车: {make} {model}")
        
        # 创建汽车主体
        car = Car(make, model, year, color)
        
        # 安装高端组件
        engine = Engine(EngineType.HYBRID, 3.5, 300, "LuxuryPower")
        transmission = Transmission(TransmissionType.AUTOMATIC, 8, "SmoothShift")
        tires = [Tire(TireType.PERFORMANCE, "245/40R18", "PremiumGrip") for _ in range(4)]
        gps = GPS("NaviLux", True)
        
        car.install_engine(engine)
        car.install_transmission(transmission)
        car.install_tires(tires)
        car.install_gps(gps)
        
        self.cars_produced += 1
        print(f"✅ 豪华汽车制造完成")
        return car
    
    def build_electric_car(self, make: str, model: str, year: int, color: str) -> Car:
        """制造电动汽车"""
        print(f"\n🏭 开始制造电动汽车: {make} {model}")
        
        # 创建汽车主体
        car = Car(make, model, year, color)
        
        # 安装电动组件
        engine = Engine(EngineType.ELECTRIC, 0.0, 250, "ElectricDrive")
        transmission = Transmission(TransmissionType.AUTOMATIC, 1, "DirectDrive")
        tires = [Tire(TireType.ALL_SEASON, "215/50R17", "EcoElectric") for _ in range(4)]
        gps = GPS("SmartNav", True)
        
        car.install_engine(engine)
        car.install_transmission(transmission)
        car.install_tires(tires)
        car.install_gps(gps)
        
        self.cars_produced += 1
        print(f"✅ 电动汽车制造完成")
        return car
    
    def get_factory_stats(self) -> str:
        """获取工厂统计"""
        return f"🏭 {self.name} 统计: 已生产 {self.cars_produced} 辆汽车"


# ==================== 演示函数 ====================
def demo_composition():
    """组合关系演示"""
    print("=" * 80)
    print("🚗 面向对象组合关系演示")
    print("=" * 80)
    
    # 创建汽车工厂
    factory = CarFactory("Python汽车制造厂")
    
    print(f"\n{'='*20} 制造不同类型的汽车 {'='*20}")
    
    # 制造不同类型的汽车
    economy_car = factory.build_economy_car("Toyota", "Corolla", 2024, "白色")
    luxury_car = factory.build_luxury_car("BMW", "X5", 2024, "黑色")
    electric_car = factory.build_electric_car("Tesla", "Model 3", 2024, "红色")
    
    cars = [economy_car, luxury_car, electric_car]
    
    print(f"\n{'='*20} 汽车操作演示 {'='*20}")
    
    # 演示汽车操作
    for car in cars:
        print(f"\n🚗 测试 {car}:")
        print(car.start_car())
        print(car.accelerate(60))
        
        if car.gps:
            print(car.gps.set_destination("购物中心"))
            print(car.gps.navigate())
        
        print(car.brake())
        print(car.stop_car())
    
    print(f"\n{'='*20} 组件独立性演示 {'='*20}")
    
    # 演示组件的独立性
    print(f"\n🔧 组件独立操作演示:")
    test_car = luxury_car
    
    # 单独操作发动机
    print(f"发动机独立操作:")
    print(f"   {test_car.engine.start()}")
    print(f"   {test_car.engine.accelerate(3000)}")
    print(f"   {test_car.engine.stop()}")
    
    # 单独操作GPS
    if test_car.gps:
        print(f"\nGPS独立操作:")
        print(f"   {test_car.gps.power_on()}")
        print(f"   {test_car.gps.set_destination('机场')}")
        print(f"   {test_car.gps.power_off()}")
    
    print(f"\n{'='*20} 维护和检查 {'='*20}")
    
    # 维护演示
    print(f"\n🔧 汽车维护演示:")
    for car in cars[:2]:  # 只演示前两辆车
        print(f"\n维护 {car}:")
        print(car.check_tire_pressure())
        
        # 模拟一些磨损
        car.mileage = 12000
        car.engine.mileage = 12000
        for tire in car.tires:
            tire.wear(85)
        
        car.perform_maintenance()
    
    print(f"\n{'='*20} 组合 vs 继承对比 {'='*20}")
    
    # 组合vs继承的对比说明
    print(f"\n💡 组合关系的优势:")
    print(f"   ✅ 汽车'有一个'发动机（组合）vs 汽车'是一个'发动机（继承）")
    print(f"   ✅ 可以在运行时更换组件")
    print(f"   ✅ 组件可以独立开发和测试")
    print(f"   ✅ 避免了复杂的继承层次")
    print(f"   ✅ 更好的代码复用性")
    
    # 演示组件替换
    print(f"\n🔄 组件替换演示:")
    new_engine = Engine(EngineType.DIESEL, 2.0, 180, "PowerDiesel")
    old_engine = economy_car.engine
    
    print(f"   原发动机: {old_engine}")
    economy_car.install_engine(new_engine)
    print(f"   新发动机: {economy_car.engine}")
    
    print(f"\n{'='*20} 详细信息展示 {'='*20}")
    
    # 显示汽车详细信息
    for car in cars:
        print(f"\n{car.get_detailed_info()}")
        print("-" * 60)
    
    print(f"\n{'='*20} 工厂统计 {'='*20}")
    
    # 工厂统计
    print(f"\n{factory.get_factory_stats()}")
    
    print("\n" + "=" * 80)
    print("🎉 组合关系演示完成!")
    print("💡 关键点:")
    print("   - 组合表示'有一个'关系，继承表示'是一个'关系")
    print("   - 组合提供了更大的灵活性和可维护性")
    print("   - 组件可以独立开发、测试和替换")
    print("   - 避免了深层继承带来的复杂性")
    print("   - 更好地反映了现实世界中对象间的关系")
    print("=" * 80)


if __name__ == "__main__":
    demo_composition()
