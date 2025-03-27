import os
import textwrap
from typing import List, Dict, Optional
from datetime import datetime
from camel.toolkits import ArxivToolkit

from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.toolkits import SearchToolkit, BrowserToolkit
from camel.memories import AgentMemory
from camel.retrievers import BM25Retriever
from camel.prompts import PromptTemplate
from camel.societies import RolePlaying
from camel.embeddings import OpenAIEmbedding
from camel.retrievers import RAGRetriever
from dotenv import load_dotenv
from camel.typing import RoleType
from camel.utils import get_prompt_template_key
from camel.prompts import PromptTemplateGenerator

load_dotenv()

class FinancialAnalysisSociety:
    def __init__(self):
        # 初始化模型和工具
        self.model = "gpt-4-turbo-preview"
        self.search_toolkit = SearchToolkit()
        self.browser_toolkit = BrowserToolkit()
        self.memory = AgentMemory()
        self.arxiv_toolkit = ArxivToolkit()
        
        # 初始化角色扮演系统
        self.role_play_system = ChatAgent(
            role_name="Financial Analyst",
            role_type=RoleType.ASSISTANT,
            model=self.model,
            memory=self.memory
        )
        
        # 设置学术研究方法
        self.methodologies = self.retrieve_academic_methodologies()
        
        # 初始化检索器
        self.retriever = RAGRetriever(
            embedding_model=OpenAIEmbedding(),
            retrieval_model=BM25Retriever()
        )
        
        # 初始化角色
        self.roles = {
            "academic_researcher": {
                "name": "Academic Researcher",
                "role": "Financial academic researcher specializing in analyzing company annual reports using academic methodologies",
                "goal": "Analyze company annual reports using academic research methodologies and provide insights"
            },
            "financial_analyst": {
                "name": "Financial Analyst",
                "role": "Professional financial analyst specializing in company valuation and risk assessment",
                "goal": "Evaluate company performance and provide investment recommendations"
            },
            "risk_manager": {
                "name": "Risk Manager",
                "role": "Risk management expert focusing on financial risk assessment and mitigation",
                "goal": "Identify and analyze potential risks in company operations"
            }
        }
        
        # 初始化角色扮演系统
        self.society = RolePlaying(
            model=self.model,
            roles=self.roles,
            memory=self.memory
        )
        
        # 初始化系统提示词
        self.system_prompt = textwrap.dedent("""
            你是一个专业的金融分析团队，由以下角色组成：
            1. 学术研究员：负责检索和分析相关学术论文
            2. 财务分析师：负责评估公司财务表现
            3. 风险管理师：负责评估公司风险状况
            
            请按照以下步骤进行分析：
            1. 检索相关学术论文和方法论
            2. 分析公司财务数据
            3. 评估公司风险状况
            4. 生成综合分析报告
            5. 提供投资建议
            
            在分析过程中，请特别注意：
            - 使用定量和定性相结合的分析方法
            - 确保分析结果具有可解释性
            - 提供具体的改进建议
            - 明确标注数据来源和引用文献
        """)

    def retrieve_academic_methodologies(self) -> List[Dict]:
        """检索相关的学术研究方法论"""
        query = "financial analysis methodology"
        try:
            # 使用 ArxivToolkit 搜索论文
            papers = self.arxiv_toolkit.search_papers(query=query, max_results=5)
            return papers
        except Exception as e:
            print(f"arxiv 搜索出错: {str(e)}")
            return []

    def analyze_company(self, company_data: Dict, papers: List[Dict]) -> str:
        """使用多角色协作分析公司"""
        # 构建分析任务
        analysis_task = f"""
        请分析以下公司数据：
        {company_data}
        
        参考以下学术论文：
        {papers}
        
        请从以下三个角度进行分析：
        1. 学术研究角度：基于论文中的方法论
        2. 财务分析角度：评估公司财务表现
        3. 风险管理角度：评估公司风险状况
        
        在分析时请特别注意：
        - 论文的引用次数和发表时间
        - 论文的方法论是否适用于当前公司
        - 论文的结论是否与公司现状相符
        """
        
        # 启动角色扮演分析
        messages = self.society.start(analysis_task)
        
        # 生成最终报告
        report_prompt = PromptTemplate(
            template="""基于以下分析结果：
            {analysis}
            
            请生成一份完整的分析报告，包括：
            1. 执行摘要
            2. 方法论说明
            3. 财务分析
            4. 风险评估
            5. 投资建议
            6. 参考文献
            
            参考文献：
            {references}"""
        )
        
        # 构建参考文献
        references = "\n".join([
            f"{i+1}. {paper['title']} ({paper['year']}) - {', '.join(paper['authors'])} "
            f"[引用次数: {paper.get('citationCount', 0)}]"
            for i, paper in enumerate(papers)
        ])
        
        # 生成最终报告
        final_message = self.society.roles["academic_researcher"].step(
            report_prompt.format(
                analysis=messages[-1].content,
                references=references
            )
        )
        
        return final_message.content

    def compare_companies(self, companies_data: List[Dict]) -> str:
        """比较多个公司的表现"""
        # 构建比较任务
        comparison_task = f"""
        请比较以下公司的表现：
        {companies_data}
        
        请从以下维度进行比较：
        1. 财务表现
        2. 风险状况
        3. 发展潜力
        4. 投资价值
        
        在比较时请特别注意：
        - 使用学术论文中的方法论进行评估
        - 考虑行业特点和市场环境
        - 分析公司间的相对优势
        - 评估未来发展趋势
        
        最后给出综合排名和投资建议。
        """
        
        # 启动角色扮演比较
        messages = self.society.start(comparison_task)
        
        # 生成比较报告
        report_prompt = PromptTemplate(
            template="""基于以下比较结果：
            {comparison}
            
            请生成一份完整的比较报告，包括：
            1. 执行摘要
            2. 比较维度说明
            3. 各维度详细分析
            4. 综合排名
            5. 投资建议
            6. 风险提示
            """
        )
        
        # 生成最终报告
        final_message = self.society.roles["financial_analyst"].step(
            report_prompt.format(
                comparison=messages[-1].content
            )
        )
        
        return final_message.content

def main():
    print("开始分析拓维信息和振邦智能的年报摘要...")
    
    # 测试SearchToolkit配置
    try:
        search_toolkit = SearchToolkit()
        test_result = search_toolkit.search("test query", max_results=1)
        print("SearchToolkit配置验证成功")
    except Exception as e:
        print(f"SearchToolkit配置验证失败: {str(e)}")
    
    society = FinancialAnalysisSociety()
    
    # 拓维信息数据
    talkweb_data = {
        "company_name": "拓维信息",
        "year": 2023,
        "risk_metrics": {
            "capital_adequacy_ratio": 0.482,  # 总资产/净资产
            "profit_margin": 0.014,  # 净利润/营业收入
            "growth_rate": 0.4102  # 营业收入增长率
        },
        "financial_statements": {
            "total_assets": 5287129846.78,
            "net_profit": 44963139.28,
            "revenue": 3154141699.10,
            "operating_cash_flow": -1169883405.68
        }
    }
    
    # 振邦智能数据
    genbytech_data = {
        "company_name": "振邦智能",
        "year": 2023,
        "risk_metrics": {
            "capital_adequacy_ratio": 0.718,  # 总资产/净资产
            "profit_margin": 0.170,  # 净利润/营业收入
            "growth_rate": 0.1762  # 营业收入增长率
        },
        "financial_statements": {
            "total_assets": 2205862147.06,
            "net_profit": 208003811.78,
            "revenue": 1225771023.07,
            "operating_cash_flow": 354599217.99
        }
    }
    
    try:
        # 检索相关论文
        print("正在检索相关学术论文...")
        papers = society.retrieve_academic_methodologies()
        
        # 分析每个公司
        print("\n正在分析拓维信息...")
        talkweb_analysis = society.analyze_company(talkweb_data, papers)
        
        print("\n正在分析振邦智能...")
        genbytech_analysis = society.analyze_company(genbytech_data, papers)
        
        # 比较公司表现
        print("\n正在比较两家公司表现...")
        companies_data = [talkweb_data, genbytech_data]
        comparison = society.compare_companies(companies_data)
        
        # 输出结果
        print("\n分析报告：")
        print("=" * 80)
        print("\n拓维信息分析结果：")
        print(textwrap.fill(talkweb_analysis, width=80))
        
        print("\n振邦智能分析结果：")
        print(textwrap.fill(genbytech_analysis, width=80))
        
        print("\n公司比较结果：")
        print(textwrap.fill(comparison, width=80))
        print("=" * 80)
        
    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")

if __name__ == "__main__":
    main()