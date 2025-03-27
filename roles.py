import logging
from typing import List, Dict, Any
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from .config import Config

logger = logging.getLogger(__name__)

class RoleManager:
    def __init__(self, config: Config):
        """初始化角色管理器"""
        self.config = config
        self.model = config.get_model()
        self.memory = config.get_memory()
        
        try:
            # 初始化学术研究员角色
            self.academic_researcher = self._create_academic_researcher()
            logger.debug("学术研究员角色初始化成功")
            
            # 初始化财务分析师角色
            self.financial_analyst = self._create_financial_analyst()
            logger.debug("财务分析师角色初始化成功")
            
            # 初始化风险管理师角色
            self.risk_manager = self._create_risk_manager()
            logger.debug("风险管理师角色初始化成功")
            
        except Exception as e:
            logger.error(f"角色初始化失败: {str(e)}")
            raise
    
    def _create_academic_researcher(self) -> ChatAgent:
        """创建学术研究员角色"""
        system_message = """你是一位专业的学术研究员，擅长分析公司年报中的学术价值和研究意义。
        你需要：
        1. 识别年报中的创新点和研究价值
        2. 评估公司的研发能力和技术实力
        3. 分析公司的学术影响力和行业地位
        4. 提供基于学术视角的投资建议"""
        
        return ChatAgent(
            system_message=system_message,
            model=self.model,
            memory=self.memory
        )
    
    def _create_financial_analyst(self) -> ChatAgent:
        """创建财务分析师角色"""
        system_message = """你是一位专业的财务分析师，擅长分析公司年报中的财务数据。
        你需要：
        1. 分析公司的财务状况和经营成果
        2. 评估公司的盈利能力和成长性
        3. 识别财务风险和潜在问题
        4. 提供基于财务视角的投资建议"""
        
        return ChatAgent(
            system_message=system_message,
            model=self.model,
            memory=self.memory
        )
    
    def _create_risk_manager(self) -> ChatAgent:
        """创建风险管理师角色"""
        system_message = """你是一位专业的风险管理师，擅长评估公司年报中的各类风险。
        你需要：
        1. 识别公司面临的各类风险
        2. 评估风险的影响程度和发生概率
        3. 分析公司的风险管理措施
        4. 提供基于风险视角的投资建议"""
        
        return ChatAgent(
            system_message=system_message,
            model=self.model,
            memory=self.memory
        )
    
    def analyze_from_academic_perspective(self, company_data: Dict[str, Any]) -> str:
        """从学术角度分析公司"""
        try:
            # 验证数据
            if not company_data or not isinstance(company_data, dict):
                logger.warning("无效的公司数据")
                return ""
            
            required_fields = ['name', 'business', 'rd_investment', 'patent_count']
            missing_fields = [field for field in required_fields if field not in company_data]
            if missing_fields:
                logger.warning(f"缺少必要字段: {missing_fields}")
                return ""
            
            # 清理历史消息
            self.academic_researcher.memory.clear()
            
            # 分块构建分析任务
            tasks = [
                f"""请分析公司的创新能力和技术实力：
                公司名称：{company_data['name']}
                主营业务：{company_data['business']}
                研发投入：{company_data['rd_investment']}
                专利数量：{company_data['patent_count']}""",
                
                f"""请分析研发投入的合理性和效果：
                研发投入：{company_data['rd_investment']}
                专利数量：{company_data['patent_count']}""",
                
                f"""请分析知识产权保护情况：
                专利数量：{company_data['patent_count']}""",
                
                f"""请分析行业技术地位：
                公司名称：{company_data['name']}
                主营业务：{company_data['business']}"""
            ]
            
            # 分块执行分析
            results = []
            for task in tasks:
                message = BaseMessage.make_user_message(role_name="User", content=task)
                response = self.academic_researcher.step(message)
                results.append(response.msgs[0].content)
                
                # 清理中间结果
                self.academic_researcher.memory.clear()
            
            # 合并分析结果
            final_analysis = "\n\n".join(results)
            logger.debug("学术分析完成")
            return final_analysis
            
        except Exception as e:
            logger.error(f"学术分析失败: {str(e)}")
            return f"分析失败：{str(e)}"
    
    def analyze_from_financial_perspective(self, company_data: Dict[str, Any]) -> str:
        """从财务角度分析公司"""
        try:
            # 验证数据
            if not company_data or not isinstance(company_data, dict):
                logger.warning("无效的公司数据")
                return ""
            
            required_fields = ['name', 'revenue', 'net_profit', 'gross_margin', 'debt_ratio']
            missing_fields = [field for field in required_fields if field not in company_data]
            if missing_fields:
                logger.warning(f"缺少必要字段: {missing_fields}")
                return ""
            
            # 清理历史消息
            self.financial_analyst.memory.clear()
            
            # 分块构建分析任务
            tasks = [
                f"""请分析公司的盈利能力和成长性：
                公司名称：{company_data['name']}
                营业收入：{company_data['revenue']}
                净利润：{company_data['net_profit']}""",
                
                f"""请分析财务健康状况：
                毛利率：{company_data['gross_margin']}
                资产负债率：{company_data['debt_ratio']}""",
                
                f"""请分析现金流情况：
                营业收入：{company_data['revenue']}
                净利润：{company_data['net_profit']}""",
                
                f"""请分析投资回报率：
                净利润：{company_data['net_profit']}
                营业收入：{company_data['revenue']}"""
            ]
            
            # 分块执行分析
            results = []
            for task in tasks:
                message = BaseMessage.make_user_message(role_name="User", content=task)
                response = self.financial_analyst.step(message)
                results.append(response.msgs[0].content)
                
                # 清理中间结果
                self.financial_analyst.memory.clear()
            
            # 合并分析结果
            final_analysis = "\n\n".join(results)
            logger.debug("财务分析完成")
            return final_analysis
            
        except Exception as e:
            logger.error(f"财务分析失败: {str(e)}")
            return f"分析失败：{str(e)}"
    
    def analyze_from_risk_perspective(self, company_data: Dict[str, Any]) -> str:
        """从风险角度分析公司"""
        try:
            # 验证数据
            if not company_data or not isinstance(company_data, dict):
                logger.warning("无效的公司数据")
                return ""
            
            required_fields = ['name', 'market_risk', 'operation_risk', 'financial_risk', 'tech_risk']
            missing_fields = [field for field in required_fields if field not in company_data]
            if missing_fields:
                logger.warning(f"缺少必要字段: {missing_fields}")
                return ""
            
            # 清理历史消息
            self.risk_manager.memory.clear()
            
            # 分块构建分析任务
            tasks = [
                f"""请分析市场风险：
                公司名称：{company_data['name']}
                市场风险：{company_data['market_risk']}""",
                
                f"""请分析经营风险：
                经营风险：{company_data['operation_risk']}""",
                
                f"""请分析财务风险：
                财务风险：{company_data['financial_risk']}""",
                
                f"""请分析技术风险：
                技术风险：{company_data['tech_risk']}"""
            ]
            
            # 分块执行分析
            results = []
            for task in tasks:
                message = BaseMessage.make_user_message(role_name="User", content=task)
                response = self.risk_manager.step(message)
                results.append(response.msgs[0].content)
                
                # 清理中间结果
                self.risk_manager.memory.clear()
            
            # 合并分析结果
            final_analysis = "\n\n".join(results)
            logger.debug("风险分析完成")
            return final_analysis
            
        except Exception as e:
            logger.error(f"风险分析失败: {str(e)}")
            return f"分析失败：{str(e)}" 