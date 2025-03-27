import unittest
import sys
import os
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from camel.scholaragent.config import Config
from camel.scholaragent.analysis import AnalysisManager
from camel.scholaragent.toolkits import ToolkitManager
from camel.scholaragent.roles import RoleManager

class TestAnalysisManager(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        print("\n初始化测试环境...")
        self.config = Config()
        self.analysis_manager = AnalysisManager(self.config)
        self.toolkit_manager = ToolkitManager()
        self.role_manager = RoleManager(self.config)
        
        # 测试数据
        self.test_company = {
            "name": "测试公司",
            "business": "软件开发和信息技术服务",
            "rd_investment": "2.5亿元",
            "patent_count": 150,
            "revenue": "15.8亿元",
            "net_profit": "1.2亿元",
            "gross_margin": "45%",
            "debt_ratio": "35%",
            "market_risk": "中等",
            "operation_risk": "低",
            "financial_risk": "低",
            "tech_risk": "中等"
        }
        
        # 年报摘要测试数据
        self.test_annual_report = {
            "company_name": "测试公司",
            "year": 2023,
            "summary": """
            2023年，公司实现营业收入15.8亿元，同比增长25.3%；净利润1.2亿元，同比增长18.5%。
            研发投入2.5亿元，占营业收入比例15.8%；新增专利150项，其中发明专利80项。
            公司主营业务为软件开发和信息技术服务，在人工智能和云计算领域具有较强竞争力。
            市场风险评级为中等，经营风险评级为低，财务风险评级为低，技术风险评级为中等。
            """,
            "key_metrics": {
                "revenue_growth": "25.3%",
                "profit_growth": "18.5%",
                "rd_ratio": "15.8%",
                "patent_growth": "20%"
            }
        }
    
    def test_retrieve_academic_methodologies(self):
        """测试检索学术研究方法"""
        print("\n测试检索学术研究方法...")
        with tqdm(total=1, desc="检索进度") as pbar:
            papers = self.analysis_manager.retrieve_academic_methodologies()
            pbar.update(1)
        self.assertIsInstance(papers, list)
        if papers:  # 如果有论文返回
            self.assertIsInstance(papers[0], dict)
            self.assertIn('title', papers[0])
            self.assertIn('authors', papers[0])
    
    def test_analyze_company(self):
        """测试公司分析功能"""
        print("\n测试公司分析功能...")
        with tqdm(total=3, desc="分析进度") as pbar:
            # 学术分析
            academic_analysis = self.role_manager.analyze_from_academic_perspective(self.test_company)
            pbar.update(1)
            
            # 财务分析
            financial_analysis = self.role_manager.analyze_from_financial_perspective(self.test_company)
            pbar.update(1)
            
            # 风险分析
            risk_analysis = self.role_manager.analyze_from_risk_perspective(self.test_company)
            pbar.update(1)
        
        analysis = self.analysis_manager.analyze_company(self.test_company)
        self.assertIsInstance(analysis, str)
        self.assertGreater(len(analysis), 0)
    
    def test_compare_companies(self):
        """测试公司比较功能"""
        print("\n测试公司比较功能...")
        companies = [
            self.test_company,
            {
                "name": "对比公司",
                "business": "智能控制系统研发和制造",
                "rd_investment": "1.8亿元",
                "patent_count": 120,
                "revenue": "12.5亿元",
                "net_profit": "0.9亿元",
                "gross_margin": "40%",
                "debt_ratio": "42%",
                "market_risk": "高",
                "operation_risk": "中等",
                "financial_risk": "中等",
                "tech_risk": "低"
            }
        ]
        
        # 使用线程池执行比较分析，设置超时时间为120秒
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.analysis_manager.compare_companies, companies)
            try:
                with tqdm(total=len(companies), desc="比较进度") as pbar:
                    while not future.done():
                        time.sleep(1)
                        pbar.update(0)  # 更新进度条但不增加计数
                    comparison = future.result(timeout=120)  # 设置120秒超时
                    pbar.update(len(companies))
            except TimeoutError:
                print("\n比较分析超时，正在终止...")
                future.cancel()
                raise
            except Exception as e:
                print(f"\n比较分析出错: {str(e)}")
                raise
        
        self.assertIsInstance(comparison, str)
        self.assertGreater(len(comparison), 0)
    
    def test_role_analysis(self):
        """测试角色分析功能"""
        print("\n测试角色分析功能...")
        with tqdm(total=3, desc="角色分析进度") as pbar:
            # 测试学术分析
            academic_analysis = self.role_manager.analyze_from_academic_perspective(self.test_company)
            self.assertIsInstance(academic_analysis, str)
            self.assertGreater(len(academic_analysis), 0)
            pbar.update(1)
            
            # 测试财务分析
            financial_analysis = self.role_manager.analyze_from_financial_perspective(self.test_company)
            self.assertIsInstance(financial_analysis, str)
            self.assertGreater(len(financial_analysis), 0)
            pbar.update(1)
            
            # 测试风险分析
            risk_analysis = self.role_manager.analyze_from_risk_perspective(self.test_company)
            self.assertIsInstance(risk_analysis, str)
            self.assertGreater(len(risk_analysis), 0)
            pbar.update(1)
    
    def test_toolkit_functions(self):
        """测试工具包功能"""
        print("\n测试工具包功能...")
        with tqdm(total=3, desc="工具包测试进度") as pbar:
            # 测试搜索公司信息
            company_info = self.toolkit_manager.search_company_info("测试公司")
            self.assertIsInstance(company_info, list)
            pbar.update(1)
            
            # 测试搜索学术论文
            papers = self.toolkit_manager.search_academic_papers("financial analysis")
            self.assertIsInstance(papers, list)
            pbar.update(1)
            
            # 测试检索相关内容
            documents = ["测试文档1", "测试文档2", "测试文档3"]
            relevant_content = self.toolkit_manager.retrieve_relevant_content("测试", documents)
            self.assertIsInstance(relevant_content, list)
            pbar.update(1)
    
    def test_annual_report_analysis(self):
        """测试年报摘要分析功能"""
        print("\n测试年报摘要分析功能...")
        with tqdm(total=2, desc="年报分析进度") as pbar:
            # 测试年报摘要解析
            report_data = self.test_annual_report
            self.assertIn("summary", report_data)
            self.assertIn("key_metrics", report_data)
            pbar.update(1)
            
            # 测试关键指标提取
            metrics = report_data["key_metrics"]
            self.assertIn("revenue_growth", metrics)
            self.assertIn("profit_growth", metrics)
            self.assertIn("rd_ratio", metrics)
            self.assertIn("patent_growth", metrics)
            pbar.update(1)
    
    def test_investment_recommendation(self):
        """测试投资推荐功能"""
        print("\n测试投资推荐功能...")
        companies = [
            self.test_company,
            {
                "name": "对比公司",
                "business": "智能控制系统研发和制造",
                "rd_investment": "1.8亿元",
                "patent_count": 120,
                "revenue": "12.5亿元",
                "net_profit": "0.9亿元",
                "gross_margin": "40%",
                "debt_ratio": "42%",
                "market_risk": "高",
                "operation_risk": "中等",
                "financial_risk": "中等",
                "tech_risk": "低"
            }
        ]
        
        with tqdm(total=3, desc="推荐分析进度") as pbar:
            # 测试公司分析
            analysis = self.analysis_manager.analyze_company(companies[0])
            self.assertIsInstance(analysis, str)
            self.assertGreater(len(analysis), 0)
            pbar.update(1)
            
            # 测试公司比较
            comparison = self.analysis_manager.compare_companies(companies)
            self.assertIsInstance(comparison, str)
            self.assertGreater(len(comparison), 0)
            pbar.update(1)
            
            # 测试投资建议生成
            self.assertIn("投资建议", comparison)
            self.assertIn("公司排名", comparison)
            self.assertIn("财务表现比较", comparison)
            self.assertIn("风险状况比较", comparison)
            pbar.update(1)
    
    def test_error_handling(self):
        """测试错误处理功能"""
        print("\n测试错误处理功能...")
        with tqdm(total=3, desc="错误处理测试进度") as pbar:
            # 测试空数据
            empty_company = {}
            analysis = self.analysis_manager.analyze_company(empty_company)
            self.assertIsInstance(analysis, str)
            self.assertEqual(len(analysis), 0)
            pbar.update(1)
            
            # 测试无效数据
            invalid_company = {"name": "无效公司", "invalid_field": "无效值"}
            analysis = self.analysis_manager.analyze_company(invalid_company)
            self.assertIsInstance(analysis, str)
            self.assertEqual(len(analysis), 0)
            pbar.update(1)
            
            # 测试网络错误
            try:
                self.toolkit_manager.search_company_info("不存在的公司")
            except Exception as e:
                self.assertIsInstance(e, Exception)
            pbar.update(1)

if __name__ == '__main__':
    unittest.main() 