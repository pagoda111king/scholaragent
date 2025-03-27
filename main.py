import logging
from typing import List, Dict, Any
from camel.scholaragent.config import Config
from camel.scholaragent.toolkits import ToolkitManager
from camel.scholaragent.roles import RoleManager
from camel.scholaragent.analysis import AnalysisManager

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """主程序入口"""
    try:
        # 初始化配置
        config = Config()
        logger.debug("配置初始化成功")
        
        # 初始化分析管理器
        analysis_manager = AnalysisManager(config)
        logger.debug("分析管理器初始化成功")
        
        # 示例公司数据
        companies = [
            {
                "name": "拓维信息",
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
            },
            {
                "name": "振邦智能",
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
        
        # 分析每个公司
        for company in companies:
            logger.info(f"开始分析公司：{company['name']}")
            analysis = analysis_manager.analyze_company(company)
            print(f"\n{company['name']}分析报告：")
            print(analysis)
            print("-" * 80)
        
        # 比较公司
        logger.info("开始比较分析")
        comparison = analysis_manager.compare_companies(companies)
        print("\n公司比较分析报告：")
        print(comparison)
        
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        raise

if __name__ == "__main__":
    main() 