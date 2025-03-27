import streamlit as st
# 设置页面配置（必须是第一个Streamlit命令）
st.set_page_config(page_title="年报分析系统", layout="wide")

from typing import List, Dict, Any
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from camel.scholaragent.config import Config
from camel.scholaragent.analysis import AnalysisManager
from camel.scholaragent.visualization import VisualizationManager

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_financial_data(line: str) -> str:
    """解析财务数据行"""
    try:
        if "：" in line:
            value = line.split("：")[-1].strip()
            if "亿元" in value:
                return value.split("亿元")[0].strip()
        return "0"
    except Exception as e:
        logger.error(f"解析财务数据时出错: {str(e)}")
        return "0"

def load_md_files(directory: str) -> List[Dict[str, Any]]:
    """加载目录下的所有md文件"""
    companies = []
    try:
        # 添加默认公司数据
        default_companies = [
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
        
        # 首先添加默认公司数据
        companies.extend(default_companies)
        
        # 然后尝试加载md文件
        for filename in os.listdir(directory):
            if not filename.endswith('.md'):
                continue
                
            file_path = os.path.join(directory, filename)
            logger.debug(f"正在加载文件: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 从文件名获取公司名称
                company_name = os.path.splitext(filename)[0]
                logger.debug(f"处理公司: {company_name}")
                
                # 解析md文件内容
                lines = content.split('\n')
                company_data = {
                    "name": company_name,
                    "business": "未找到主营业务信息",
                    "revenue": "0亿元",
                    "net_profit": "0亿元",
                    "rd_investment": "2.5亿元",
                    "patent_count": 150,
                    "gross_margin": "45%",
                    "debt_ratio": "35%",
                    "market_risk": "中等",
                    "operation_risk": "中等",
                    "financial_risk": "中等",
                    "tech_risk": "中等"
                }
                
                # 查找主要会计数据和财务指标部分
                start_idx = -1
                for i, line in enumerate(lines):
                    if "主要会计数据和财务指标" in line:
                        start_idx = i
                        break
                
                if start_idx != -1:
                    for i in range(start_idx, min(start_idx + 50, len(lines))):
                        line = lines[i]
                        if "营业收入" in line and "亿元" in line:
                            company_data["revenue"] = f"{parse_financial_data(line)}亿元"
                        elif "净利润" in line and "亿元" in line:
                            company_data["net_profit"] = f"{parse_financial_data(line)}亿元"
                
                # 查找主营业务部分
                for line in lines:
                    if "主营业务" in line:
                        company_data["business"] = line.split("：")[-1].strip()
                        break
                
                # 根据财务指标调整风险等级
                try:
                    revenue_float = float(company_data["revenue"].replace("亿元", ""))
                    net_profit_float = float(company_data["net_profit"].replace("亿元", ""))
                    
                    if revenue_float < 10 or net_profit_float < 1:
                        company_data["market_risk"] = "高"
                        company_data["financial_risk"] = "高"
                    elif revenue_float > 20 and net_profit_float > 2:
                        company_data["market_risk"] = "低"
                        company_data["financial_risk"] = "低"
                except Exception as e:
                    logger.error(f"调整风险等级时出错: {str(e)}")
                
                companies.append(company_data)
                logger.debug(f"成功添加公司: {company_name}")
                
            except Exception as e:
                logger.error(f"处理文件 {filename} 时出错: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"加载文件时出错: {str(e)}")
        st.error(f"加载文件时出错: {str(e)}")
    
    return companies

def analyze_company_with_timeout(analysis_manager: AnalysisManager, company: Dict[str, Any], timeout: int = 600) -> str:
    """带超时的公司分析函数"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(analysis_manager.analyze_company, company)
        try:
            # 增加重试机制
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return future.result(timeout=timeout)
                except TimeoutError:
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.warning(f"分析公司 {company['name']} 第 {retry_count} 次超时，正在重试...")
                        time.sleep(2)  # 等待2秒后重试
                        future = executor.submit(analysis_manager.analyze_company, company)
                    else:
                        logger.error(f"分析公司 {company['name']} 在 {max_retries} 次尝试后仍然超时")
                        return f"分析公司 {company['name']} 超时，请重试"
        except Exception as e:
            logger.error(f"分析公司 {company['name']} 时发生错误: {str(e)}")
            return f"分析公司 {company['name']} 时发生错误: {str(e)}"

def render_analysis_progress(progress_bar, status_text, current: int, total: int, message: str, sub_steps: List[str] = None):
    """渲染分析进度"""
    progress = int((current / total) * 100)
    progress_bar.progress(progress)
    
    # 显示主进度
    status_text.text(f"{message} ({current}/{total})")
    
    # 如果有子步骤，显示子步骤进度
    if sub_steps:
        for i, step in enumerate(sub_steps):
            st.write(f"• {step}")
    
    time.sleep(0.5)  # 添加短暂延迟，避免界面卡死

def main():
    """主程序入口"""
    try:
        # 初始化配置
        config = Config()
        logger.debug("配置初始化成功")
        
        # 初始化分析管理器和可视化管理器
        analysis_manager = AnalysisManager(config)
        visualization_manager = VisualizationManager()
        logger.debug("管理器初始化成功")
        
        # 设置页面标题
        st.title("📊 年报分析报告")
        
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
        
        # 创建进度条和状态文本
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 分析每个公司
            company_analyses = []
            total_companies = len(companies)
            
            for i, company in enumerate(companies):
                # 更新进度显示
                progress = int((i / total_companies) * 100)
                progress_bar.progress(progress)
                status_text.text(f"正在分析公司：{company['name']} ({i+1}/{total_companies})")
                
                # 创建分析步骤容器
                with st.expander(f"分析进度 - {company['name']}", expanded=True):
                    # 定义分析子步骤
                    sub_steps = [
                        "1. 基础信息分析",
                        "2. 财务数据分析",
                        "3. 研发创新分析",
                        "4. 风险评估",
                        "5. 投资建议生成"
                    ]
                    
                    # 显示子步骤
                    for step in sub_steps:
                        st.write(f"• {step}")
                        time.sleep(0.2)  # 添加短暂延迟，使进度显示更平滑
                
                logger.debug(f"开始分析公司: {company['name']}")
                analysis = analyze_company_with_timeout(analysis_manager, company)
                
                if analysis:
                    company_analyses.append({
                        "name": company["name"],
                        "analysis": analysis
                    })
                    logger.debug(f"完成公司分析: {company['name']}")
                    st.success(f"完成 {company['name']} 的分析")
                    
                    # 立即显示分析结果
                    with st.expander(f"{company['name']} 分析报告", expanded=True):
                        # 分段显示分析结果
                        sections = analysis.split('\n\n')
                        for section in sections:
                            if section.strip():
                                # 提取标题和内容
                                lines = section.split('\n')
                                title = lines[0]
                                content = '\n'.join(lines[1:])
                                
                                # 创建子折叠面板
                                with st.expander(title, expanded=False):
                                    st.markdown(content)
            
            # 比较公司
            status_text.text("正在进行公司比较分析...")
            logger.debug("开始公司比较分析")
            
            # 创建比较分析步骤容器
            with st.expander("比较分析进度", expanded=True):
                # 定义比较分析子步骤
                comparison_steps = [
                    "1. 财务指标对比",
                    "2. 研发投入对比",
                    "3. 风险水平对比",
                    "4. 发展潜力对比",
                    "5. 投资价值对比"
                ]
                
                # 显示子步骤
                for step in comparison_steps:
                    st.write(f"• {step}")
                    time.sleep(0.2)
            
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(analysis_manager.compare_companies, companies)
                try:
                    comparison_result = future.result(timeout=600)  # 增加超时时间到600秒
                except TimeoutError:
                    logger.error("公司比较分析超时")
                    comparison_result = "公司比较分析超时，请重试"
                except Exception as e:
                    logger.error(f"公司比较分析时发生错误: {str(e)}")
                    comparison_result = f"公司比较分析时发生错误: {str(e)}"
            
            # 显示比较分析结果
            if comparison_result:
                with st.expander("公司比较分析报告", expanded=True):
                    # 分段显示比较结果
                    sections = comparison_result.split('\n\n')
                    for section in sections:
                        if section.strip():
                            # 提取标题和内容
                            lines = section.split('\n')
                            title = lines[0]
                            content = '\n'.join(lines[1:])
                            
                            # 创建子折叠面板
                            with st.expander(title, expanded=False):
                                st.markdown(content)
            
            progress_bar.progress(100)
            status_text.text("分析完成！")
            logger.debug("完成所有分析")
            
        except Exception as e:
            logger.error(f"分析过程中出错: {str(e)}")
            st.error(f"分析过程中出错: {str(e)}")
            
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        st.error(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()