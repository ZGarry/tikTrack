# TikTrack

一个简单易用的Python性能跟踪和可视化工具。(A simple performance tracking and visualization tool for Python applications.)

## 安装 (Installation)

```bash
pip install tikTrack
```

## 功能特点 (Features)

- 使用装饰器轻松跟踪函数执行时间 (Track function execution time easily with decorators)
- 自动生成性能报告和可视化图表 (Automatically generate performance reports and visualization charts)
- 支持多种输出格式：CSV报表和饼图 (Support for multiple output formats: CSV reports and pie charts)
- 程序退出时自动生成报告 (Automatically generate reports when the program exits)
- 聚合相同阶段的执行时间 (Aggregate execution times for the same stages)
- 支持中文字体显示 (Support for Chinese fonts in charts)

## 使用示例 (Usage Examples)

### 基本用法 (Basic Usage)

```python
from tiktrack import timed_stage

@timed_stage("数据加载")
def load_data():
    # 模拟数据加载过程
    import time
    time.sleep(1)
    return "data"

@timed_stage("数据处理")
def process_data(data):
    # 模拟数据处理过程
    import time
    time.sleep(0.5)
    return f"processed {data}"

def main():
    data = load_data()
    processed_data = process_data(data)
    print(processed_data)

if __name__ == "__main__":
    main()
    # 程序退出时会自动生成性能报告
```

### 自定义输出目录 (Custom Output Directory)

```python
from tiktrack import timed_stage, set_default_output_dir

# 设置性能报告输出目录
set_default_output_dir("my_performance_reports")

@timed_stage("任务1")
def task1():
    import time
    time.sleep(0.8)

@timed_stage("任务2")
def task2():
    import time
    time.sleep(1.2)

def main():
    task1()
    task2()

if __name__ == "__main__":
    main()
```

### 手动生成性能报告 (Manually Generate Reports)

```python
from tiktrack import timed_stage, generate_performance_report

@timed_stage("任务A")
def task_a():
    import time
    time.sleep(0.5)

@timed_stage("任务B")
def task_b():
    import time
    time.sleep(0.7)

def main():
    for i in range(3):
        task_a()
        task_b()
    
    # 手动生成性能报告
    generate_performance_report("custom_reports")

if __name__ == "__main__":
    main()
```

## 输出文件 (Output Files)

执行代码后，将生成以下文件：

1. `performance_report.csv` - 详细的每次函数调用性能数据
2. `performance_summary.csv` - 按阶段聚合的性能摘要数据
3. `performance_chart.png` - 性能分布饼图

## 许可证 (License)

MIT 