"""
TikTrack 基本使用示例
展示如何使用装饰器和自动报告生成功能

Basic TikTrack usage example
Demonstrates how to use decorators and automatic report generation
"""
from tiktrack import timed_stage, set_default_output_dir

# 设置报告输出目录
# Set report output directory
set_default_output_dir("example_results")

@timed_stage("数据加载 / Data Loading")
def load_data():
    """模拟数据加载过程"""
    import time
    time.sleep(1)
    return "data"

@timed_stage("数据处理 / Data Processing")
def process_data(data):
    """模拟数据处理过程"""
    import time
    time.sleep(0.5)
    return f"processed {data}"

@timed_stage("结果存储 / Result Storage")
def save_results(processed_data):
    """模拟结果存储过程"""
    import time
    time.sleep(0.3)
    print(f"Saved: {processed_data}")

def main():
    """主程序流程"""
    print("开始执行示例程序 / Starting example program")
    
    # 调用被装饰的函数
    data = load_data()
    processed_data = process_data(data)
    save_results(processed_data)
    
    # 重复调用以展示聚合功能
    for i in range(3):
        load_data()
    
    print("示例程序执行完毕，退出时将自动生成性能报告")
    print("Example program completed, performance reports will be generated on exit")

if __name__ == "__main__":
    main()
    # 程序退出时会自动生成性能报告
    # Performance reports will be automatically generated when the program exits 