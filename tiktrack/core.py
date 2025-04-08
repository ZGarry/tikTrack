import time
import pandas as pd
import os
import matplotlib
# 在导入pyplot之前设置后端为'Agg'，这是一个非交互式后端，不需要QApplication
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import atexit
import matplotlib.font_manager as fm
from matplotlib import rcParams

# 设置matplotlib支持中文显示
def set_chinese_font():
    """设置matplotlib中文字体支持"""
    # 尝试设置中文字体，有多种可能的字体
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'STSong', 'SimSun', 'Arial Unicode MS', 'WenQuanYi Zen Hei']
    found_font = False
    
    # 查找系统中已安装的字体
    font_paths = fm.findSystemFonts()
    system_fonts = set()
    for font_path in font_paths:
        try:
            font = fm.FontProperties(fname=font_path)
            system_fonts.add(font.get_name())
        except:
            pass
    
    # 尝试从可用字体列表中找到中文字体
    for font in chinese_fonts:
        if font in system_fonts:
            rcParams['font.family'] = ['sans-serif']
            rcParams['font.sans-serif'] = [font] + rcParams['font.sans-serif']
            rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            found_font = True
            break
    
    if not found_font:
        print("警告: 未找到中文字体，图表中的中文可能无法正确显示")
        print("Warning: No Chinese font found, Chinese characters might not display correctly in charts")

# 初始化中文字体支持
set_chinese_font()

# 全局变量，用于记录各阶段的执行时间
timing_data = []
default_output_dir = "results"  # 默认输出目录

def timed_stage(stage_name):
    """Decorator: Record function execution time
    
    装饰器：记录函数执行时间
    
    Args:
        stage_name (str): Stage name that will be displayed in the performance report
                          将在性能报告中显示的阶段名称
        
    Returns:
        function: Decorator function
                  装饰器函数
                  
    Example:
        @timed_stage("数据加载")
        def load_data():
            # function implementation
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            timing_data.append({"阶段": stage_name, "耗时(秒)": elapsed})
            return result
        return wrapper
    return decorator

def set_default_output_dir(output_dir):
    """Set default output directory for performance reports
    
    设置默认的性能报告输出目录
    
    Args:
        output_dir (str): Output directory path
                          输出目录路径
    """
    global default_output_dir
    default_output_dir = output_dir

def generate_performance_report(output_dir=None):
    """Generate performance report
    
    生成性能报告
    
    Args:
        output_dir (str, optional): Output directory path. Defaults to None (uses default_output_dir).
                                    输出目录路径。默认为None（使用default_output_dir）。
        
    Returns:
        pandas.DataFrame: Processed performance data
                          处理过的性能数据DataFrame
    """
    # 如果没有提供输出目录，使用默认目录
    if output_dir is None:
        output_dir = default_output_dir
        
    try:
        # 检查输出目录参数是否为None或空
        if output_dir is None or output_dir == "":
            output_dir = "results"
            print(f"Warning: No valid output directory specified, using default: {output_dir}")
            print(f"警告: 未指定有效的输出目录，将使用默认目录: {output_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建性能报告DataFrame
        perf_df = pd.DataFrame(timing_data)
        
        if perf_df.empty:
            print("No performance data collected / 没有收集到性能数据")
            return perf_df
        
        # 计算总时间和占比
        total_time = perf_df["耗时(秒)"].sum()
        perf_df["占比"] = perf_df["耗时(秒)"].apply(lambda x: f"{(x/total_time*100):.2f}%")
        
        # 格式化耗时数据，最多保留4位小数
        perf_df["耗时(秒)"] = perf_df["耗时(秒)"].apply(lambda x: round(x, 4))
        
        # 根据阶段名称聚合数据（如果有重复的阶段名称）
        if perf_df["阶段"].duplicated().any():
            summary_df = perf_df.groupby("阶段").agg({
                "耗时(秒)": ["sum", "mean", "count", "min", "max"],
            }).reset_index()
            summary_df.columns = ["阶段", "总耗时(秒)", "平均耗时(秒)", "调用次数", "最小耗时(秒)", "最大耗时(秒)"]
            
            # 计算总时间占比
            summary_df["占比"] = summary_df["总耗时(秒)"].apply(lambda x: f"{(x/total_time*100):.2f}%")
            
            # 格式化数值列，最多保留4位小数
            for col in ["总耗时(秒)", "平均耗时(秒)", "最小耗时(秒)", "最大耗时(秒)"]:
                summary_df[col] = summary_df[col].apply(lambda x: round(x, 4))
            
            # 为饼图计算添加占比数值（但不保存到最终输出）
            summary_df["占比数值"] = summary_df["总耗时(秒)"] / total_time * 100
            
            # 保存聚合的性能报告
            summary_file = os.path.join(output_dir, 'performance_summary.csv')
            # 保存前删除占比数值列
            summary_save_df = summary_df.drop(columns=["占比数值"])
            summary_save_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
            print(f"Performance summary saved to / 性能报告摘要已保存至: {summary_file}")
            
            # 打印摘要报告
            print("\nPerformance Summary / 性能报告摘要:")
            print(summary_save_df.sort_values("总耗时(秒)", ascending=False).head(10))
            
            # 创建耗时饼图
            create_time_pie_chart(summary_df, output_dir, "Performance by Stage / 阶段耗时占比")
        
        # 为饼图计算添加占比数值（但不保存到最终输出）
        perf_df["占比数值"] = perf_df["耗时(秒)"] / total_time * 100
        
        # 保存详细的性能报告
        performance_file = os.path.join(output_dir, 'performance_report.csv')
        # 保存前删除占比数值列
        perf_save_df = perf_df.drop(columns=["占比数值"])
        perf_save_df.to_csv(performance_file, index=False, encoding='utf-8-sig')
        print(f"Detailed performance report saved to / 详细性能报告已保存至: {performance_file}")
        
        # 如果没有聚合报告，为原始数据创建饼图
        if not perf_df["阶段"].duplicated().any():
            print("\nPerformance Summary / 性能报告摘要:")
            print(perf_save_df.sort_values("耗时(秒)", ascending=False).head(10))
            create_time_pie_chart(perf_df, output_dir, "Performance by Stage / 阶段耗时占比")
        
        return perf_save_df
    except Exception as e:
        print(f"Error generating performance report / 生成性能报告时发生错误: {e}")
        return pd.DataFrame()  # 返回空的DataFrame

def create_time_pie_chart(df, output_dir, title):
    """Create time proportion pie chart
    
    创建耗时占比饼图
    
    Args:
        df (pandas.DataFrame): Performance data DataFrame
                              性能数据DataFrame
        output_dir (str): Output directory path
                          输出目录路径
        title (str): Chart title
                     图表标题
    """
    try:
        # 检查输出目录参数是否为None或空
        if output_dir is None or output_dir == "":
            output_dir = "results"
            print(f"Warning: No valid output directory specified, using default: {output_dir}")
            print(f"警告: 未指定有效的输出目录，将使用默认目录: {output_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 为了更好的可视化，只显示占比大于1%的部分
        significant_df = df[df["占比数值"] > 1].copy()
        other_time = df[df["占比数值"] <= 1]["耗时(秒)"].sum() if "总耗时(秒)" not in df else df[df["占比数值"] <= 1]["总耗时(秒)"].sum()
        
        # 如果有占比小于1%的部分，将它们合并为"其他"
        if other_time > 0:
            # 确保other_time最多保留4位小数
            other_time = round(other_time, 4)
            
            time_column = "耗时(秒)" if "总耗时(秒)" not in df else "总耗时(秒)"
            total_time = df[time_column].sum()
            
            other_row = pd.DataFrame({
                "阶段": ["Other small times / 其他微小耗时"],
                time_column: [other_time],
                "占比数值": [other_time / total_time * 100]
            })
            plot_df = pd.concat([significant_df, other_row], ignore_index=True)
        else:
            plot_df = significant_df
        
        # 创建饼图
        plt.figure(figsize=(12, 8))
        time_column = "耗时(秒)" if "总耗时(秒)" not in df else "总耗时(秒)"
        
        # 使用中文标签时，确保字体正确设置
        patches, texts, autotexts = plt.pie(
            plot_df[time_column], 
            labels=plot_df["阶段"], 
            autopct='%1.2f%%',
            startangle=90,
            shadow=False,
            pctdistance=0.75,  # 将百分比标签放置在离中心较远但仍在饼图内部的位置
            labeldistance=1.1,  # 将标签放置在饼图外部
            textprops={'fontsize': 9}  # 设置统一字体大小
        )
        
        # 改善标签可读性
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('white')  # 在饼图内部使用白色
            autotext.set_fontweight('bold')  # 加粗百分比文字以提高可读性
        
        plt.axis('equal')
        
        # 将标题放在左上角
        plt.title(title, fontsize=14, loc='left', pad=20)
        
        plt.tight_layout()
        
        # 保存图表
        chart_file = os.path.join(output_dir, 'performance_chart.png')
        plt.savefig(chart_file, dpi=300)
        plt.close()
        print(f"Performance chart saved to / 性能图表已保存至: {chart_file}")
    except Exception as e:
        print(f"Error creating performance chart / 创建性能图表时发生错误: {e}")

# 注册在程序退出时自动生成性能报告
def auto_generate_report():
    """Automatically generate performance report when program exits
    
    在程序退出时自动生成性能报告
    """
    print("\nProgram is exiting, automatically generating performance report...")
    print("程序即将退出，自动生成性能报告...")
    if timing_data:  # 只有在收集到性能数据时才生成报告
        generate_performance_report()

# 注册退出函数
atexit.register(auto_generate_report) 