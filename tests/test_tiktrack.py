"""
TikTrack 测试文件
Tests for TikTrack package
"""
import os
import time
import unittest
import pandas as pd
from tiktrack import timed_stage, generate_performance_report, set_default_output_dir

# 测试目录
TEST_OUTPUT_DIR = "test_output"

class TestTikTrack(unittest.TestCase):
    """TikTrack单元测试类"""
    
    def setUp(self):
        """每个测试前设置"""
        # 确保测试目录存在
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        set_default_output_dir(TEST_OUTPUT_DIR)
        
        # 清除之前的计时数据
        from tiktrack.core import timing_data
        timing_data.clear()
    
    def test_timed_stage_decorator(self):
        """测试timed_stage装饰器"""
        @timed_stage("test_stage")
        def test_function():
            time.sleep(0.1)
            return "result"
        
        # 调用被装饰的函数
        result = test_function()
        
        # 检查函数返回值
        self.assertEqual(result, "result")
        
        # 检查timing_data是否记录了函数调用
        from tiktrack.core import timing_data
        self.assertEqual(len(timing_data), 1)
        self.assertEqual(timing_data[0]["阶段"], "test_stage")
        self.assertGreaterEqual(timing_data[0]["耗时(秒)"], 0.1)
    
    def test_generate_performance_report(self):
        """测试性能报告生成"""
        @timed_stage("stage1")
        def func1():
            time.sleep(0.1)
        
        @timed_stage("stage2")
        def func2():
            time.sleep(0.2)
        
        # 调用函数几次
        func1()
        func2()
        func1()
        
        # 生成报告
        df = generate_performance_report(TEST_OUTPUT_DIR)
        
        # 验证报告文件是否生成
        self.assertTrue(os.path.exists(os.path.join(TEST_OUTPUT_DIR, "performance_report.csv")))
        self.assertTrue(os.path.exists(os.path.join(TEST_OUTPUT_DIR, "performance_summary.csv")))
        self.assertTrue(os.path.exists(os.path.join(TEST_OUTPUT_DIR, "performance_chart.png")))
        
        # 验证数据正确性
        self.assertEqual(len(df), 3)  # 应该有3条记录
        
        # 读取摘要文件
        summary_df = pd.read_csv(os.path.join(TEST_OUTPUT_DIR, "performance_summary.csv"))
        self.assertEqual(len(summary_df), 2)  # 应该有2个阶段
        
        # 验证阶段名称
        stage_names = set(summary_df["阶段"].tolist())
        self.assertEqual(stage_names, {"stage1", "stage2"})
        
        # 验证调用次数
        stage1_row = summary_df[summary_df["阶段"] == "stage1"].iloc[0]
        stage2_row = summary_df[summary_df["阶段"] == "stage2"].iloc[0]
        self.assertEqual(stage1_row["调用次数"], 2)
        self.assertEqual(stage2_row["调用次数"], 1)

if __name__ == "__main__":
    unittest.main() 