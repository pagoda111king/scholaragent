import logging
from typing import List, Dict, Any
from textwrap import dedent
from camel.prompts.base import TextPrompt
from .config import Config
from .toolkits import ToolkitManager
from .roles import RoleManager

logger = logging.getLogger(__name__)

class AnalysisManager:
    def __init__(self, config: Config):
        """初始化分析管理器"""
        self.config = config
        self.toolkit_manager = ToolkitManager()
        self.role_manager = RoleManager(config)
        logger.debug("分析管理器初始化成功")
    
    def retrieve_academic_methodologies(self) -> List[Dict[str, Any]]:
        """检索相关学术研究方法"""
        try:
            # 搜索多个相关领域的论文
            search_queries = [
                "annual report analysis methodology",
                "financial statement analysis techniques",
                "company valuation methods",
                "risk assessment in financial analysis",
                "industry comparison methodology"
            ]
            
            all_papers = []
            for query in search_queries:
                papers = self.toolkit_manager.search_academic_papers(
                    query=query,
                    max_results=3
                )
                all_papers.extend(papers)
            
            # 论文去重
            unique_papers = {paper['title']: paper for paper in all_papers}.values()
            
            # 论文评分
            scored_papers = []
            for paper in unique_papers:
                score = 0
                # 根据引用次数评分
                if 'citation_count' in paper:
                    score += min(paper['citation_count'] / 100, 5)
                # 根据发表年份评分
                if 'year' in paper:
                    current_year = 2024
                    year_diff = current_year - paper['year']
                    score += max(0, 5 - year_diff / 2)
                # 根据期刊影响因子评分
                if 'journal_impact_factor' in paper:
                    score += min(paper['journal_impact_factor'], 5)
                
                paper['score'] = score
                scored_papers.append(paper)
            
            # 按分数排序并返回前5篇
            scored_papers.sort(key=lambda x: x['score'], reverse=True)
            selected_papers = scored_papers[:5]
            
            logger.debug(f"检索到 {len(selected_papers)} 篇高质量相关论文")
            return selected_papers
        except Exception as e:
            logger.error(f"检索学术方法失败: {str(e)}")
            return []
    
    def analyze_company(self, company_data: Dict[str, Any]) -> str:
        """分析单个公司"""
        try:
            # 验证数据
            if not company_data or not isinstance(company_data, dict):
                logger.warning("无效的公司数据")
                return ""
            
            required_fields = ['name', 'business', 'rd_investment', 'patent_count', 
                             'revenue', 'net_profit', 'gross_margin', 'debt_ratio',
                             'market_risk', 'operation_risk', 'financial_risk', 'tech_risk']
            missing_fields = [field for field in required_fields if field not in company_data]
            if missing_fields:
                logger.warning(f"缺少必要字段: {missing_fields}")
                return ""
            
            # 获取相关学术论文
            papers = self.retrieve_academic_methodologies()
            
            # 计算关键财务指标
            financial_metrics = self._calculate_financial_metrics(company_data)
            
            # 从不同角度进行分析
            academic_analysis = self.role_manager.analyze_from_academic_perspective(company_data)
            if not academic_analysis:
                logger.warning("学术分析失败")
                return ""
            
            # 清理内存
            self.role_manager.academic_researcher.memory.clear()
            
            financial_analysis = self.role_manager.analyze_from_financial_perspective(company_data)
            if not financial_analysis:
                logger.warning("财务分析失败")
                return ""
            
            # 清理内存
            self.role_manager.financial_analyst.memory.clear()
            
            risk_analysis = self.role_manager.analyze_from_risk_perspective(company_data)
            if not risk_analysis:
                logger.warning("风险分析失败")
                return ""
            
            # 清理内存
            self.role_manager.risk_manager.memory.clear()
            
            # 生成最终报告
            report_template = TextPrompt(dedent("""
                公司分析报告
                
                1. 执行摘要
                {summary}
                
                2. 研究方法说明
                {methodology}
                
                3. 公司概况
                {company_profile}
                
                4. 财务分析
                {financial_analysis}
                
                5. 研发创新分析
                {rd_analysis}
                
                6. 风险评估
                {risk_analysis}
                
                7. 行业对比
                {industry_comparison}
                
                8. 投资建议
                {investment_advice}
                
                9. 参考文献
                {references}
                """))
            
            # 生成参考文献列表
            references_list = []
            for i, paper in enumerate(papers, 1):
                references_list.append(f"{i}. {paper.get('title', '未知标题')} - {paper.get('authors', '未知作者')}")
            references_text = "\n".join(references_list) if references_list else "暂无相关参考文献"
            
            report = report_template.format(
                summary=f"本报告对{company_data['name']}进行了全面分析...",
                methodology="采用多角度分析方法，结合学术研究和实践经验...",
                company_profile=self._generate_company_profile(company_data),
                financial_analysis=financial_analysis,
                rd_analysis=self._analyze_rd_innovation(company_data),
                risk_analysis=risk_analysis,
                industry_comparison=self._generate_industry_comparison(company_data),
                investment_advice="基于以上分析，建议...",
                references=references_text
            )
            
            logger.debug("公司分析完成")
            return report
        except Exception as e:
            logger.error(f"公司分析失败: {str(e)}")
            return ""
    
    def _calculate_financial_metrics(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """计算关键财务指标"""
        try:
            metrics = {}
            
            # 安全地转换数值，处理可能的格式问题
            revenue = float(company_data['revenue'].replace('亿元', '').strip())
            net_profit = float(company_data['net_profit'].replace('亿元', '').strip())
            rd_investment = float(company_data['rd_investment'].replace('亿元', '').strip())
            
            # 避免除零错误
            if revenue <= 0:
                logger.warning(f"公司 {company_data['name']} 的营业收入为0或负数，使用默认值1")
                revenue = 1
            
            # 计算净利润率
            metrics['net_profit_margin'] = (net_profit / revenue) * 100
            
            # 计算研发投入比例
            metrics['rd_ratio'] = (rd_investment / revenue) * 100
            
            # 计算专利密度
            metrics['patent_density'] = company_data['patent_count'] / revenue
            
            # 计算风险综合得分
            risk_scores = {
                '高': 3,
                '中等': 2,
                '低': 1
            }
            metrics['risk_score'] = (
                risk_scores.get(company_data['market_risk'], 0) +
                risk_scores.get(company_data['operation_risk'], 0) +
                risk_scores.get(company_data['financial_risk'], 0) +
                risk_scores.get(company_data['tech_risk'], 0)
            ) / 4
            
            return metrics
        except (ValueError, ZeroDivisionError) as e:
            logger.error(f"计算财务指标失败: {str(e)}")
            # 返回默认值
            return {
                'net_profit_margin': 0,
                'rd_ratio': 0,
                'patent_density': 0,
                'risk_score': 2
            }
        except Exception as e:
            logger.error(f"计算财务指标时发生未知错误: {str(e)}")
            return {}
    
    def _generate_company_profile(self, company_data: Dict[str, Any]) -> str:
        """生成公司概况"""
        try:
            profile = f"""
            公司名称：{company_data['name']}
            主营业务：{company_data['business']}
            营业收入：{company_data['revenue']}
            净利润：{company_data['net_profit']}
            研发投入：{company_data['rd_investment']}
            专利数量：{company_data['patent_count']}项
            毛利率：{company_data['gross_margin']}
            资产负债率：{company_data['debt_ratio']}
            """
            return profile
        except Exception as e:
            logger.error(f"生成公司概况失败: {str(e)}")
            return ""
    
    def _analyze_rd_innovation(self, company_data: Dict[str, Any]) -> str:
        """分析研发创新能力"""
        try:
            metrics = self._calculate_financial_metrics(company_data)
            rd_ratio = metrics.get('rd_ratio', 0)
            patent_density = metrics.get('patent_density', 0)
            
            analysis = f"""
            1. 研发投入分析
            - 研发投入占营业收入比例：{rd_ratio:.2f}%
            - 研发投入强度：{self._evaluate_rd_intensity(rd_ratio)}
            
            2. 创新能力分析
            - 专利密度：{patent_density:.2f}项/亿元
            - 创新效率：{self._evaluate_innovation_efficiency(patent_density)}
            
            3. 技术风险
            - 技术风险等级：{company_data['tech_risk']}
            - 风险应对建议：{self._generate_tech_risk_advice(company_data['tech_risk'])}
            """
            return analysis
        except Exception as e:
            logger.error(f"分析研发创新失败: {str(e)}")
            return ""
    
    def _evaluate_rd_intensity(self, rd_ratio: float) -> str:
        """评估研发投入强度"""
        if rd_ratio >= 10:
            return "极高"
        elif rd_ratio >= 5:
            return "高"
        elif rd_ratio >= 3:
            return "中等"
        else:
            return "低"
    
    def _evaluate_innovation_efficiency(self, patent_density: float) -> str:
        """评估创新效率"""
        if patent_density >= 10:
            return "极高"
        elif patent_density >= 5:
            return "高"
        elif patent_density >= 2:
            return "中等"
        else:
            return "低"
    
    def _generate_tech_risk_advice(self, tech_risk: str) -> str:
        """生成技术风险建议"""
        if tech_risk == "高":
            return "建议加强技术研发投入，建立技术储备，提高自主创新能力"
        elif tech_risk == "中等":
            return "建议保持技术研发投入，关注行业技术发展趋势"
        else:
            return "建议继续维持现有技术优势，适当增加创新投入"
    
    def _generate_industry_comparison(self, company_data: Dict[str, Any]) -> str:
        """生成行业对比分析"""
        try:
            metrics = self._calculate_financial_metrics(company_data)
            
            comparison = f"""
            1. 财务指标对比
            - 净利润率：{metrics.get('net_profit_margin', 0):.2f}%
            - 研发投入比例：{metrics.get('rd_ratio', 0):.2f}%
            
            2. 创新能力对比
            - 专利密度：{metrics.get('patent_density', 0):.2f}项/亿元
            
            3. 风险状况对比
            - 综合风险得分：{metrics.get('risk_score', 0):.2f}
            
            注：以上指标需要与行业平均水平进行对比才能得出更准确的结论。
            """
            return comparison
        except Exception as e:
            logger.error(f"生成行业对比失败: {str(e)}")
            return ""
    
    def compare_companies(self, companies: List[Dict[str, Any]]) -> str:
        """比较多个公司"""
        try:
            # 获取相关学术论文
            papers = self.retrieve_academic_methodologies()
            
            # 分析每个公司
            company_analyses = []
            company_metrics = []
            for company in companies:
                try:
                    # 设置超时时间为60秒
                    analysis = self.analyze_company(company)
                    if analysis:  # 只有在分析成功时才添加
                        metrics = self._calculate_financial_metrics(company)
                        company_analyses.append({
                            "name": company["name"],
                            "analysis": analysis
                        })
                        company_metrics.append({
                            "name": company["name"],
                            "metrics": metrics
                        })
                    else:
                        logger.warning(f"公司 {company['name']} 分析失败，跳过")
                except Exception as e:
                    logger.error(f"分析公司 {company['name']} 时发生错误: {str(e)}")
                    continue
            
            if not company_analyses:
                logger.error("没有成功分析任何公司")
                return "分析失败：无法获取有效的公司分析结果"
            
            # 生成比较报告
            report_template = TextPrompt(dedent("""
                公司比较分析报告
                
                1. 分析概述
                {overview}
                
                2. 公司排名
                {rankings}
                
                3. 财务指标对比
                {financial_comparison}
                
                4. 研发创新对比
                {rd_comparison}
                
                5. 风险状况对比
                {risk_comparison}
                
                6. 发展潜力对比
                {potential_comparison}
                
                7. 投资建议
                {investment_advice}
                
                8. 参考文献
                {references}
                """))
            
            # 生成排名
            rankings = self._generate_rankings(company_analyses)
            
            # 生成参考文献列表
            references_list = []
            for i, paper in enumerate(papers, 1):
                references_list.append(f"{i}. {paper.get('title', '未知标题')} - {paper.get('authors', '未知作者')}")
            references_text = "\n".join(references_list) if references_list else "暂无相关参考文献"
            
            report = report_template.format(
                overview="本报告对多家公司进行了全面比较分析...",
                rankings=rankings,
                financial_comparison=self._compare_financial_metrics(company_metrics),
                rd_comparison=self._compare_rd_innovation(company_metrics),
                risk_comparison=self._compare_risk_metrics(company_metrics),
                potential_comparison=self._compare_potential(company_metrics),
                investment_advice=self._generate_investment_advice(company_metrics),
                references=references_text
            )
            
            logger.debug("公司比较分析完成")
            return report
        except Exception as e:
            logger.error(f"公司比较分析失败: {str(e)}")
            return f"分析失败：{str(e)}"
    
    def _compare_financial_metrics(self, company_metrics: List[Dict[str, Any]]) -> str:
        """比较财务指标"""
        try:
            comparison = "财务指标对比分析：\n\n"
            
            # 计算各项指标的平均值
            metrics_sum = {
                'net_profit_margin': 0,
                'rd_ratio': 0,
                'patent_density': 0
            }
            for company in company_metrics:
                for metric in metrics_sum:
                    metrics_sum[metric] += company['metrics'].get(metric, 0)
            
            metrics_avg = {
                metric: value / len(company_metrics)
                for metric, value in metrics_sum.items()
            }
            
            # 生成对比表格
            comparison += "指标\t\t公司\t\t数值\t\t与平均值比较\n"
            comparison += "-" * 60 + "\n"
            
            for company in company_metrics:
                for metric, avg_value in metrics_avg.items():
                    value = company['metrics'].get(metric, 0)
                    diff = value - avg_value
                    diff_sign = "+" if diff > 0 else ""
                    comparison += f"{metric}\t\t{company['name']}\t\t{value:.2f}\t\t{diff_sign}{diff:.2f}\n"
            
            return comparison
        except Exception as e:
            logger.error(f"比较财务指标失败: {str(e)}")
            return ""
    
    def _compare_rd_innovation(self, company_metrics: List[Dict[str, Any]]) -> str:
        """比较研发创新能力"""
        try:
            comparison = "研发创新对比分析：\n\n"
            
            # 计算研发投入和专利密度的平均值
            rd_avg = sum(c['metrics'].get('rd_ratio', 0) for c in company_metrics) / len(company_metrics)
            patent_avg = sum(c['metrics'].get('patent_density', 0) for c in company_metrics) / len(company_metrics)
            
            comparison += "1. 研发投入对比\n"
            for company in company_metrics:
                rd_ratio = company['metrics'].get('rd_ratio', 0)
                diff = rd_ratio - rd_avg
                diff_sign = "+" if diff > 0 else ""
                comparison += f"- {company['name']}: {rd_ratio:.2f}% ({diff_sign}{diff:.2f}%)\n"
            
            comparison += "\n2. 专利密度对比\n"
            for company in company_metrics:
                patent_density = company['metrics'].get('patent_density', 0)
                diff = patent_density - patent_avg
                diff_sign = "+" if diff > 0 else ""
                comparison += f"- {company['name']}: {patent_density:.2f}项/亿元 ({diff_sign}{diff:.2f})\n"
            
            return comparison
        except Exception as e:
            logger.error(f"比较研发创新失败: {str(e)}")
            return ""
    
    def _compare_risk_metrics(self, company_metrics: List[Dict[str, Any]]) -> str:
        """比较风险指标"""
        try:
            comparison = "风险状况对比分析：\n\n"
            
            # 计算风险得分的平均值
            risk_avg = sum(c['metrics'].get('risk_score', 0) for c in company_metrics) / len(company_metrics)
            
            comparison += "综合风险得分对比：\n"
            for company in company_metrics:
                risk_score = company['metrics'].get('risk_score', 0)
                diff = risk_score - risk_avg
                diff_sign = "+" if diff > 0 else ""
                comparison += f"- {company['name']}: {risk_score:.2f} ({diff_sign}{diff:.2f})\n"
            
            # 风险等级分布
            comparison += "\n风险等级分布：\n"
            risk_levels = {'高': 0, '中等': 0, '低': 0}
            for company in company_metrics:
                risk_score = company['metrics'].get('risk_score', 0)
                if risk_score >= 2.5:
                    risk_levels['高'] += 1
                elif risk_score >= 1.5:
                    risk_levels['中等'] += 1
                else:
                    risk_levels['低'] += 1
            
            for level, count in risk_levels.items():
                comparison += f"- {level}风险: {count}家公司\n"
            
            return comparison
        except Exception as e:
            logger.error(f"比较风险指标失败: {str(e)}")
            return ""
    
    def _compare_potential(self, company_metrics: List[Dict[str, Any]]) -> str:
        """比较发展潜力"""
        try:
            comparison = "发展潜力对比分析：\n\n"
            
            # 计算综合得分
            for company in company_metrics:
                metrics = company['metrics']
                # 计算综合得分（考虑多个因素）
                score = (
                    metrics.get('net_profit_margin', 0) * 0.4 +  # 盈利能力权重40%
                    metrics.get('rd_ratio', 0) * 0.3 +          # 研发投入权重30%
                    metrics.get('patent_density', 0) * 0.3      # 创新能力权重30%
                )
                company['metrics']['potential_score'] = score
            
            # 按综合得分排序
            sorted_companies = sorted(
                company_metrics,
                key=lambda x: x['metrics'].get('potential_score', 0),
                reverse=True
            )
            
            comparison += "发展潜力排名：\n"
            for i, company in enumerate(sorted_companies, 1):
                score = company['metrics'].get('potential_score', 0)
                comparison += f"{i}. {company['name']}: {score:.2f}\n"
            
            return comparison
        except Exception as e:
            logger.error(f"比较发展潜力失败: {str(e)}")
            return ""
    
    def _generate_investment_advice(self, company_metrics: List[Dict[str, Any]]) -> str:
        """生成投资建议"""
        try:
            # 计算综合得分
            for company in company_metrics:
                metrics = company['metrics']
                # 计算投资价值得分
                score = (
                    metrics.get('net_profit_margin', 0) * 0.3 +  # 盈利能力权重30%
                    metrics.get('rd_ratio', 0) * 0.2 +          # 研发投入权重20%
                    metrics.get('patent_density', 0) * 0.2 +    # 创新能力权重20%
                    (3 - metrics.get('risk_score', 0)) * 0.3    # 风险因素权重30%（风险越低越好）
                )
                company['metrics']['investment_score'] = score
            
            # 按投资价值得分排序
            sorted_companies = sorted(
                company_metrics,
                key=lambda x: x['metrics'].get('investment_score', 0),
                reverse=True
            )
            
            advice = "投资建议：\n\n"
            for i, company in enumerate(sorted_companies, 1):
                score = company['metrics'].get('investment_score', 0)
                risk_score = company['metrics'].get('risk_score', 0)
                
                if risk_score <= 1.5:
                    risk_level = "低"
                elif risk_score <= 2.5:
                    risk_level = "中等"
                else:
                    risk_level = "高"
                
                advice += f"{i}. {company['name']}\n"
                advice += f"   - 投资价值得分：{score:.2f}\n"
                advice += f"   - 风险等级：{risk_level}\n"
                advice += f"   - 建议：{self._generate_specific_advice(score, risk_score)}\n\n"
            
            return advice
        except Exception as e:
            logger.error(f"生成投资建议失败: {str(e)}")
            return ""
    
    def _generate_specific_advice(self, score: float, risk_score: float) -> str:
        """生成具体投资建议"""
        if score >= 8 and risk_score <= 1.5:
            return "强烈推荐投资，公司具有高投资价值和低风险"
        elif score >= 6 and risk_score <= 2:
            return "建议投资，公司具有较好的投资价值和可控风险"
        elif score >= 4 and risk_score <= 2.5:
            return "可以考虑投资，但需要关注风险控制"
        else:
            return "建议观望，公司投资价值较低或风险较高"
    
    def _generate_rankings(self, company_analyses: List[Dict[str, Any]]) -> str:
        """生成公司排名"""
        try:
            rankings = []
            for i, company in enumerate(company_analyses, 1):
                rankings.append(f"{i}. {company['name']}")
            return "\n".join(rankings)
        except Exception as e:
            logger.error(f"生成排名失败: {str(e)}")
            return "" 