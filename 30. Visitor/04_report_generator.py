"""
04_report_generator.py - 报表生成系统的访问者设计

这个示例展示了访问者模式在报表生成系统中的应用：
- 不同类型的数据元素
- 多种报表格式的生成
- 灵活的数据处理和格式化
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import json


# ==================== 抽象访问者 ====================
class ReportVisitor(ABC):
    """报表访问者抽象类"""

    @abstractmethod
    def visit_text_data(self, text_data):
        """访问文本数据"""
        pass

    @abstractmethod
    def visit_numeric_data(self, numeric_data):
        """访问数值数据"""
        pass

    @abstractmethod
    def visit_chart_data(self, chart_data):
        """访问图表数据"""
        pass

    @abstractmethod
    def visit_table_data(self, table_data):
        """访问表格数据"""
        pass

    @abstractmethod
    def visit_image_data(self, image_data):
        """访问图片数据"""
        pass


# ==================== 抽象数据元素 ====================
class ReportElement(ABC):
    """报表元素抽象类"""

    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.created_at = datetime.now()

    @abstractmethod
    def accept(self, visitor: ReportVisitor):
        """接受访问者"""
        pass


# ==================== 具体数据元素 ====================
class TextData(ReportElement):
    """文本数据元素"""

    def __init__(self, title: str, content: str, font_size: int = 12,
                 is_bold: bool = False, description: str = ""):
        super().__init__(title, description)
        self.content = content
        self.font_size = font_size
        self.is_bold = is_bold
        self.word_count = len(content.split())

    def accept(self, visitor: ReportVisitor):
        visitor.visit_text_data(self)

    def __str__(self):
        return f"文本: {self.title} ({self.word_count} 字)"


class NumericData(ReportElement):
    """数值数据元素"""

    def __init__(self, title: str, value: float, unit: str = "",
                 decimal_places: int = 2, description: str = ""):
        super().__init__(title, description)
        self.value = value
        self.unit = unit
        self.decimal_places = decimal_places
        self.formatted_value = f"{value:.{decimal_places}f}"

    def accept(self, visitor: ReportVisitor):
        visitor.visit_numeric_data(self)

    def get_display_value(self) -> str:
        """获取显示值"""
        return f"{self.formatted_value} {self.unit}".strip()

    def __str__(self):
        return f"数值: {self.title} = {self.get_display_value()}"


class ChartData(ReportElement):
    """图表数据元素"""

    def __init__(self, title: str, chart_type: str, data: Dict[str, Any],
                 width: int = 600, height: int = 400, description: str = ""):
        super().__init__(title, description)
        self.chart_type = chart_type  # bar, line, pie, scatter
        self.data = data
        self.width = width
        self.height = height
        self.data_points = len(data.get('labels', []))

    def accept(self, visitor: ReportVisitor):
        visitor.visit_chart_data(self)

    def __str__(self):
        return f"图表: {self.title} ({self.chart_type}, {self.data_points} 数据点)"


class TableData(ReportElement):
    """表格数据元素"""

    def __init__(self, title: str, headers: List[str], rows: List[List[Any]],
                 has_totals: bool = False, description: str = ""):
        super().__init__(title, description)
        self.headers = headers
        self.rows = rows
        self.has_totals = has_totals
        self.row_count = len(rows)
        self.col_count = len(headers)

    def accept(self, visitor: ReportVisitor):
        visitor.visit_table_data(self)

    def get_cell_value(self, row: int, col: int) -> Any:
        """获取单元格值"""
        if 0 <= row < len(self.rows) and 0 <= col < len(self.rows[row]):
            return self.rows[row][col]
        return None

    def __str__(self):
        return f"表格: {self.title} ({self.row_count}x{self.col_count})"


class ImageData(ReportElement):
    """图片数据元素"""

    def __init__(self, title: str, image_path: str, width: int = 400,
                 height: int = 300, alt_text: str = "", description: str = ""):
        super().__init__(title, description)
        self.image_path = image_path
        self.width = width
        self.height = height
        self.alt_text = alt_text or title
        self.file_size = width * height * 3  # 模拟文件大小

    def accept(self, visitor: ReportVisitor):
        visitor.visit_image_data(self)

    def __str__(self):
        return f"图片: {self.title} ({self.width}x{self.height})"


# ==================== 具体访问者 ====================
class HTMLReportGenerator(ReportVisitor):
    """HTML报表生成器"""

    def __init__(self, title: str = "报表"):
        self.title = title
        self.html_content: List[str] = []
        self.element_count = 0
        self._init_html()

    def _init_html(self):
        """初始化HTML结构"""
        self.html_content = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"    <title>{self.title}</title>",
            "    <meta charset='utf-8'>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 20px; }",
            "        .report-element { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }",
            "        .title { font-size: 18px; font-weight: bold; color: #333; }",
            "        .description { color: #666; font-style: italic; }",
            "        table { border-collapse: collapse; width: 100%; }",
            "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "        th { background-color: #f2f2f2; }",
            "        .numeric { text-align: right; font-weight: bold; color: #2e7d32; }",
            "    </style>",
            "</head>",
            "<body>",
            f"    <h1>{self.title}</h1>",
            f"    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        ]

    def visit_text_data(self, text_data: TextData):
        """生成文本HTML"""
        style = f"font-size: {text_data.font_size}px;"
        if text_data.is_bold:
            style += " font-weight: bold;"

        html = f"""
    <div class="report-element">
        <div class="title">{text_data.title}</div>
        {f'<div class="description">{text_data.description}</div>' if text_data.description else ''}
        <div style="{style}">{text_data.content}</div>
        <small>字数: {text_data.word_count}</small>
    </div>"""

        self.html_content.append(html)
        self.element_count += 1
        print(f"📝 生成HTML文本: {text_data.title}")

    def visit_numeric_data(self, numeric_data: NumericData):
        """生成数值HTML"""
        html = f"""
    <div class="report-element">
        <div class="title">{numeric_data.title}</div>
        {f'<div class="description">{numeric_data.description}</div>' if numeric_data.description else ''}
        <div class="numeric">{numeric_data.get_display_value()}</div>
    </div>"""

        self.html_content.append(html)
        self.element_count += 1
        print(f"📊 生成HTML数值: {numeric_data.title}")

    def visit_chart_data(self, chart_data: ChartData):
        """生成图表HTML"""
        # 简化的图表表示
        html = f"""
    <div class="report-element">
        <div class="title">{chart_data.title}</div>
        {f'<div class="description">{chart_data.description}</div>' if chart_data.description else ''}
        <div style="width: {chart_data.width}px; height: {chart_data.height}px;
                    border: 2px dashed #ccc; display: flex; align-items: center;
                    justify-content: center; background-color: #f9f9f9;">
            <div style="text-align: center;">
                <strong>{chart_data.chart_type.upper()} 图表</strong><br>
                {chart_data.data_points} 个数据点
            </div>
        </div>
    </div>"""

        self.html_content.append(html)
        self.element_count += 1
        print(f"📈 生成HTML图表: {chart_data.title}")

    def visit_table_data(self, table_data: TableData):
        """生成表格HTML"""
        html = f"""
    <div class="report-element">
        <div class="title">{table_data.title}</div>
        {f'<div class="description">{table_data.description}</div>' if table_data.description else ''}
        <table>
            <thead>
                <tr>"""

        # 表头
        for header in table_data.headers:
            html += f"<th>{header}</th>"
        html += "</tr></thead><tbody>"

        # 数据行
        for row in table_data.rows:
            html += "<tr>"
            for cell in row:
                if isinstance(cell, (int, float)):
                    html += f'<td class="numeric">{cell}</td>'
                else:
                    html += f"<td>{cell}</td>"
            html += "</tr>"

        html += """
            </tbody>
        </table>
    </div>"""

        self.html_content.append(html)
        self.element_count += 1
        print(f"📋 生成HTML表格: {table_data.title}")

    def visit_image_data(self, image_data: ImageData):
        """生成图片HTML"""
        html = f"""
    <div class="report-element">
        <div class="title">{image_data.title}</div>
        {f'<div class="description">{image_data.description}</div>' if image_data.description else ''}
        <img src="{image_data.image_path}"
             alt="{image_data.alt_text}"
             width="{image_data.width}"
             height="{image_data.height}"
             style="max-width: 100%; height: auto;">
        <br><small>尺寸: {image_data.width}x{image_data.height}</small>
    </div>"""

        self.html_content.append(html)
        self.element_count += 1
        print(f"🖼️  生成HTML图片: {image_data.title}")

    def finalize(self) -> str:
        """完成HTML生成"""
        self.html_content.extend([
            f"    <hr>",
            f"    <p><small>报表包含 {self.element_count} 个元素</small></p>",
            "</body>",
            "</html>"
        ])
        return "\n".join(self.html_content)


class PDFReportGenerator(ReportVisitor):
    """PDF报表生成器（模拟）"""

    def __init__(self, title: str = "报表"):
        self.title = title
        self.pdf_commands: List[str] = []
        self.element_count = 0
        self.current_y = 800  # PDF坐标

    def visit_text_data(self, text_data: TextData):
        """生成文本PDF命令"""
        self.pdf_commands.append(f"添加文本: '{text_data.title}' 在位置 (50, {self.current_y})")
        self.current_y -= 20
        self.pdf_commands.append(f"添加内容: '{text_data.content[:50]}...' 在位置 (50, {self.current_y})")
        self.current_y -= 30
        self.element_count += 1
        print(f"📝 生成PDF文本: {text_data.title}")

    def visit_numeric_data(self, numeric_data: NumericData):
        """生成数值PDF命令"""
        self.pdf_commands.append(f"添加标题: '{numeric_data.title}' 在位置 (50, {self.current_y})")
        self.current_y -= 20
        self.pdf_commands.append(f"添加数值: '{numeric_data.get_display_value()}' 在位置 (50, {self.current_y})")
        self.current_y -= 30
        self.element_count += 1
        print(f"📊 生成PDF数值: {numeric_data.title}")

    def visit_chart_data(self, chart_data: ChartData):
        """生成图表PDF命令"""
        self.pdf_commands.append(f"绘制{chart_data.chart_type}图表: '{chart_data.title}' 在位置 (50, {self.current_y})")
        self.pdf_commands.append(f"图表尺寸: {chart_data.width}x{chart_data.height}")
        self.current_y -= chart_data.height + 20
        self.element_count += 1
        print(f"📈 生成PDF图表: {chart_data.title}")

    def visit_table_data(self, table_data: TableData):
        """生成表格PDF命令"""
        self.pdf_commands.append(f"绘制表格: '{table_data.title}' 在位置 (50, {self.current_y})")
        self.pdf_commands.append(f"表格尺寸: {table_data.row_count}行 x {table_data.col_count}列")
        self.current_y -= (table_data.row_count + 2) * 20
        self.element_count += 1
        print(f"📋 生成PDF表格: {table_data.title}")

    def visit_image_data(self, image_data: ImageData):
        """生成图片PDF命令"""
        self.pdf_commands.append(f"插入图片: '{image_data.image_path}' 在位置 (50, {self.current_y})")
        self.pdf_commands.append(f"图片尺寸: {image_data.width}x{image_data.height}")
        self.current_y -= image_data.height + 20
        self.element_count += 1
        print(f"🖼️  生成PDF图片: {image_data.title}")

    def get_pdf_commands(self) -> List[str]:
        """获取PDF生成命令"""
        return [f"PDF报表: {self.title}"] + self.pdf_commands + [f"总计 {self.element_count} 个元素"]


class ExcelReportGenerator(ReportVisitor):
    """Excel报表生成器（模拟）"""

    def __init__(self, title: str = "报表"):
        self.title = title
        self.worksheets: Dict[str, List[Dict]] = {"主表": []}
        self.current_row = 1
        self.element_count = 0

    def visit_text_data(self, text_data: TextData):
        """生成文本Excel数据"""
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 1,
            "value": text_data.title,
            "type": "title"
        })
        self.current_row += 1
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 1,
            "value": text_data.content,
            "type": "text"
        })
        self.current_row += 2
        self.element_count += 1
        print(f"📝 生成Excel文本: {text_data.title}")

    def visit_numeric_data(self, numeric_data: NumericData):
        """生成数值Excel数据"""
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 1,
            "value": numeric_data.title,
            "type": "label"
        })
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 2,
            "value": numeric_data.value,
            "type": "number"
        })
        self.current_row += 1
        self.element_count += 1
        print(f"📊 生成Excel数值: {numeric_data.title}")

    def visit_chart_data(self, chart_data: ChartData):
        """生成图表Excel数据"""
        # 创建专门的图表工作表
        chart_sheet = f"图表_{len(self.worksheets)}"
        self.worksheets[chart_sheet] = []

        # 添加图表数据
        if 'labels' in chart_data.data and 'values' in chart_data.data:
            for i, (label, value) in enumerate(zip(chart_data.data['labels'], chart_data.data['values'])):
                self.worksheets[chart_sheet].append({
                    "row": i + 1,
                    "col": 1,
                    "value": label,
                    "type": "label"
                })
                self.worksheets[chart_sheet].append({
                    "row": i + 1,
                    "col": 2,
                    "value": value,
                    "type": "number"
                })

        self.element_count += 1
        print(f"📈 生成Excel图表: {chart_data.title}")

    def visit_table_data(self, table_data: TableData):
        """生成表格Excel数据"""
        # 添加表头
        for col, header in enumerate(table_data.headers):
            self.worksheets["主表"].append({
                "row": self.current_row,
                "col": col + 1,
                "value": header,
                "type": "header"
            })
        self.current_row += 1

        # 添加数据行
        for row_data in table_data.rows:
            for col, cell_value in enumerate(row_data):
                self.worksheets["主表"].append({
                    "row": self.current_row,
                    "col": col + 1,
                    "value": cell_value,
                    "type": "data"
                })
            self.current_row += 1

        self.current_row += 1  # 空行分隔
        self.element_count += 1
        print(f"📋 生成Excel表格: {table_data.title}")

    def visit_image_data(self, image_data: ImageData):
        """生成图片Excel数据"""
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 1,
            "value": f"图片: {image_data.title}",
            "type": "image_placeholder"
        })
        self.worksheets["主表"].append({
            "row": self.current_row,
            "col": 2,
            "value": image_data.image_path,
            "type": "image_path"
        })
        self.current_row += 2
        self.element_count += 1
        print(f"🖼️  生成Excel图片: {image_data.title}")

    def get_excel_data(self) -> Dict[str, Any]:
        """获取Excel数据"""
        return {
            "title": self.title,
            "worksheets": self.worksheets,
            "element_count": self.element_count
        }


class JSONReportGenerator(ReportVisitor):
    """JSON报表生成器"""

    def __init__(self, title: str = "报表"):
        self.title = title
        self.report_data: Dict[str, Any] = {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "elements": []
        }
        self.element_count = 0

    def visit_text_data(self, text_data: TextData):
        """生成文本JSON数据"""
        element = {
            "type": "text",
            "title": text_data.title,
            "description": text_data.description,
            "content": text_data.content,
            "properties": {
                "font_size": text_data.font_size,
                "is_bold": text_data.is_bold,
                "word_count": text_data.word_count
            }
        }
        self.report_data["elements"].append(element)
        self.element_count += 1
        print(f"📝 生成JSON文本: {text_data.title}")

    def visit_numeric_data(self, numeric_data: NumericData):
        """生成数值JSON数据"""
        element = {
            "type": "numeric",
            "title": numeric_data.title,
            "description": numeric_data.description,
            "value": numeric_data.value,
            "properties": {
                "unit": numeric_data.unit,
                "decimal_places": numeric_data.decimal_places,
                "formatted_value": numeric_data.formatted_value,
                "display_value": numeric_data.get_display_value()
            }
        }
        self.report_data["elements"].append(element)
        self.element_count += 1
        print(f"📊 生成JSON数值: {numeric_data.title}")

    def visit_chart_data(self, chart_data: ChartData):
        """生成图表JSON数据"""
        element = {
            "type": "chart",
            "title": chart_data.title,
            "description": chart_data.description,
            "chart_type": chart_data.chart_type,
            "data": chart_data.data,
            "properties": {
                "width": chart_data.width,
                "height": chart_data.height,
                "data_points": chart_data.data_points
            }
        }
        self.report_data["elements"].append(element)
        self.element_count += 1
        print(f"📈 生成JSON图表: {chart_data.title}")

    def visit_table_data(self, table_data: TableData):
        """生成表格JSON数据"""
        element = {
            "type": "table",
            "title": table_data.title,
            "description": table_data.description,
            "headers": table_data.headers,
            "rows": table_data.rows,
            "properties": {
                "row_count": table_data.row_count,
                "col_count": table_data.col_count,
                "has_totals": table_data.has_totals
            }
        }
        self.report_data["elements"].append(element)
        self.element_count += 1
        print(f"📋 生成JSON表格: {table_data.title}")

    def visit_image_data(self, image_data: ImageData):
        """生成图片JSON数据"""
        element = {
            "type": "image",
            "title": image_data.title,
            "description": image_data.description,
            "image_path": image_data.image_path,
            "properties": {
                "width": image_data.width,
                "height": image_data.height,
                "alt_text": image_data.alt_text,
                "file_size": image_data.file_size
            }
        }
        self.report_data["elements"].append(element)
        self.element_count += 1
        print(f"🖼️  生成JSON图片: {image_data.title}")

    def get_json_data(self) -> str:
        """获取JSON数据"""
        self.report_data["element_count"] = self.element_count
        return json.dumps(self.report_data, ensure_ascii=False, indent=2)


# ==================== 报表类 ====================
class Report:
    """报表类 - 包含多个报表元素"""

    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.elements: List[ReportElement] = []
        self.created_at = datetime.now()

    def add_element(self, element: ReportElement):
        """添加报表元素"""
        self.elements.append(element)
        print(f"➕ 添加元素: {element}")

    def accept(self, visitor: ReportVisitor):
        """让访问者访问所有元素"""
        print(f"\n📊 {type(visitor).__name__} 开始生成报表: {self.title}")
        print("-" * 60)

        for element in self.elements:
            element.accept(visitor)

        print("-" * 60)

    def get_summary(self) -> str:
        """获取报表摘要"""
        element_types = {}
        for element in self.elements:
            element_type = type(element).__name__
            element_types[element_type] = element_types.get(element_type, 0) + 1

        summary = [f"报表摘要: {self.title}"]
        summary.append(f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"总元素数: {len(self.elements)}")
        summary.append("元素类型分布:")
        for element_type, count in element_types.items():
            summary.append(f"  - {element_type}: {count} 个")

        return "\n".join(summary)


# ==================== 演示函数 ====================
def create_sample_report() -> Report:
    """创建示例报表"""
    print("🏗️  创建示例报表...")

    # 创建报表
    report = Report("2024年第一季度业务报表", "公司第一季度业务数据分析报告")

    # 添加标题文本
    report.add_element(TextData(
        "执行摘要",
        "本报表分析了2024年第一季度的业务表现。总体而言，公司在各个关键指标上都取得了显著进展，"
        "销售收入同比增长15%，客户满意度达到新高。",
        font_size=14,
        is_bold=True
    ))

    # 添加关键指标
    report.add_element(NumericData("总收入", 1250000.50, "元", 2))
    report.add_element(NumericData("净利润", 187500.75, "元", 2))
    report.add_element(NumericData("客户满意度", 4.8, "分", 1))
    report.add_element(NumericData("员工数量", 156, "人", 0))

    # 添加销售数据表格
    sales_headers = ["月份", "销售额(万元)", "订单数", "平均订单价值(元)"]
    sales_data = [
        ["1月", 42.5, 85, 5000],
        ["2月", 38.2, 76, 5026],
        ["3月", 44.3, 92, 4815]
    ]
    report.add_element(TableData("季度销售数据", sales_headers, sales_data, True))

    # 添加图表数据
    chart_data = {
        "labels": ["1月", "2月", "3月"],
        "values": [42.5, 38.2, 44.3],
        "colors": ["#FF6384", "#36A2EB", "#FFCE56"]
    }
    report.add_element(ChartData("月度销售趋势", "line", chart_data, 600, 300))

    # 添加产品分布图表
    product_data = {
        "labels": ["产品A", "产品B", "产品C", "产品D"],
        "values": [35, 25, 25, 15],
        "colors": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
    }
    report.add_element(ChartData("产品销售分布", "pie", product_data, 400, 400))

    # 添加图片
    report.add_element(ImageData(
        "公司logo",
        "assets/company_logo.png",
        200, 100,
        "公司标志"
    ))

    # 添加结论文本
    report.add_element(TextData(
        "结论与建议",
        "基于第一季度的数据分析，建议公司继续加大对产品A的投入，同时关注2月份销售下滑的原因。"
        "整体趋势积极，预计第二季度将继续保持增长势头。"
    ))

    print(f"✅ 报表创建完成: {report.title}")
    return report


def demo_report_generator():
    """报表生成器演示"""
    print("=" * 80)
    print("📊 报表生成系统访问者演示")
    print("=" * 80)

    # 创建示例报表
    report = create_sample_report()

    # 显示报表摘要
    print(f"\n{report.get_summary()}")

    # 创建不同的报表生成器
    generators = [
        ("HTML生成器", HTMLReportGenerator(report.title)),
        ("PDF生成器", PDFReportGenerator(report.title)),
        ("Excel生成器", ExcelReportGenerator(report.title)),
        ("JSON生成器", JSONReportGenerator(report.title))
    ]

    # 使用不同生成器处理报表
    for name, generator in generators:
        print(f"\n{'='*20} {name} {'='*20}")

        report.accept(generator)

        # 显示生成结果
        if isinstance(generator, HTMLReportGenerator):
            html_content = generator.finalize()
            print(f"\n📄 HTML报表生成完成 ({len(html_content)} 字符)")
            print("HTML预览 (前200字符):")
            print(html_content[:200] + "...")

        elif isinstance(generator, PDFReportGenerator):
            pdf_commands = generator.get_pdf_commands()
            print(f"\n📄 PDF报表生成完成 ({len(pdf_commands)} 个命令)")
            print("PDF命令预览:")
            for cmd in pdf_commands[:5]:
                print(f"  - {cmd}")
            if len(pdf_commands) > 5:
                print(f"  ... 还有 {len(pdf_commands) - 5} 个命令")

        elif isinstance(generator, ExcelReportGenerator):
            excel_data = generator.get_excel_data()
            print(f"\n📄 Excel报表生成完成")
            print(f"工作表数量: {len(excel_data['worksheets'])}")
            for sheet_name, sheet_data in excel_data['worksheets'].items():
                print(f"  - {sheet_name}: {len(sheet_data)} 个单元格")

        elif isinstance(generator, JSONReportGenerator):
            json_data = generator.get_json_data()
            print(f"\n📄 JSON报表生成完成 ({len(json_data)} 字符)")
            print("JSON预览 (前200字符):")
            print(json_data[:200] + "...")

    print("\n" + "=" * 80)
    print("🎉 报表生成系统演示完成!")
    print("💡 关键点:")
    print("   - 同一份数据可以生成多种格式的报表")
    print("   - 访问者模式使得添加新的报表格式变得简单")
    print("   - 数据结构与表现形式完全分离")
    print("=" * 80)


if __name__ == "__main__":
    import json  # 在这里导入以避免未使用的导入警告
    demo_report_generator()