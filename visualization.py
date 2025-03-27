import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import logging
import time

logger = logging.getLogger(__name__)

class VisualizationManager:
    def __init__(self):
        """初始化可视化管理器"""
        logger.debug("可视化管理器初始化成功")
    
    
    def render_analysis_progress(self, stage: str, progress: float):
        """渲染分析进度"""
        try:
            st.progress(progress)
            st.write(f"当前阶段：{stage}")
        except Exception as e:
            logger.error(f"渲染进度时出错: {str(e)}")
    
    def render_company_analysis(self, company_data: Dict[str, Any], analysis_result: str):
        """渲染单个公司分析结果"""
        try:
            st.title(f"📈 {company_data['name']} 分析报告")
            
            # 创建进度条和状态文本
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 第一阶段：基础信息展示
            status_text.text("正在分析基础信息...")
            with st.expander("📋 基础信息分析", expanded=True):
                self._render_basic_info(company_data)
            progress_bar.progress(20)
            time.sleep(0.5)
            
            # 第二阶段：财务分析
            status_text.text("正在进行财务分析...")
            with st.expander("💰 财务分析", expanded=True):
                self._render_financial_analysis(company_data)
            progress_bar.progress(40)
            time.sleep(0.5)
            
            # 第三阶段：研发创新分析
            status_text.text("正在分析研发创新能力...")
            with st.expander("🔬 研发创新分析", expanded=False):
                self._render_rd_analysis(company_data)
            progress_bar.progress(60)
            time.sleep(0.5)
            
            # 第四阶段：风险评估
            status_text.text("正在进行风险评估...")
            with st.expander("⚠️ 风险评估", expanded=False):
                self._render_risk_analysis(company_data)
            progress_bar.progress(80)
            time.sleep(0.5)
            
            # 第五阶段：投资建议
            status_text.text("正在生成投资建议...")
            with st.expander("💡 投资建议", expanded=True):
                self._render_investment_advice(company_data)
            progress_bar.progress(100)
            
            # 显示详细分析结果
            with st.expander("📊 详细分析报告", expanded=False):
                st.write(analysis_result)
            
            # 完成分析
            status_text.text("分析完成！")
            st.success("分析完成！")
            
        except Exception as e:
            logger.error(f"渲染公司分析时出错: {str(e)}")
            st.error(f"渲染分析结果时出错: {str(e)}")
    
    def _render_basic_info(self, company_data: Dict[str, Any]):
        """渲染基础信息"""
        try:
            st.subheader("📋 公司基本信息")
            
            # 创建三列布局
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("营业收入", company_data['revenue'])
                st.metric("净利润", company_data['net_profit'])
                st.metric("研发投入", company_data['rd_investment'])
            
            with col2:
                st.metric("毛利率", company_data['gross_margin'])
                st.metric("资产负债率", company_data['debt_ratio'])
                st.metric("专利数量", f"{company_data['patent_count']}项")
            
            with col3:
                risk_levels = {
                    '高': '🔴',
                    '中等': '🟡',
                    '低': '🟢'
                }
                st.metric("市场风险", f"{risk_levels.get(company_data['market_risk'], '⚪')} {company_data['market_risk']}")
                st.metric("经营风险", f"{risk_levels.get(company_data['operation_risk'], '⚪')} {company_data['operation_risk']}")
                st.metric("财务风险", f"{risk_levels.get(company_data['financial_risk'], '⚪')} {company_data['financial_risk']}")
            
            # 添加公司简介
            st.write("### 公司简介")
            st.write(f"**主营业务**：{company_data['business']}")
            
        except Exception as e:
            logger.error(f"渲染基础信息时出错: {str(e)}")
            st.error(f"渲染基础信息时出错: {str(e)}")
    
    def render_comparison_analysis(self, companies: List[Dict[str, Any]], comparison_result: str):
        """渲染公司比较分析结果"""
        try:
            st.title("📊 公司比较分析")
            
            # 创建进度条和状态文本
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 第一阶段：基础信息对比
            status_text.text("正在对比基础信息...")
            with st.expander("📋 基础信息对比", expanded=True):
                self._render_comparison_basic_info(companies)
            progress_bar.progress(20)
            time.sleep(0.5)
            
            # 第二阶段：财务指标对比
            status_text.text("正在对比财务指标...")
            with st.expander("💰 财务指标对比", expanded=True):
                self._render_financial_radar(companies)
            progress_bar.progress(40)
            time.sleep(0.5)
            
            # 第三阶段：风险对比
            status_text.text("正在对比风险状况...")
            with st.expander("⚠️ 风险状况对比", expanded=False):
                self._render_risk_comparison(companies)
            progress_bar.progress(60)
            time.sleep(0.5)
            
            # 第四阶段：发展潜力对比
            status_text.text("正在分析发展潜力...")
            with st.expander("🚀 发展潜力分析", expanded=False):
                self._render_potential_comparison(companies)
            progress_bar.progress(80)
            time.sleep(0.5)
            
            # 第五阶段：投资建议
            status_text.text("正在生成投资建议...")
            with st.expander("💡 投资建议", expanded=True):
                self._render_investment_comparison(companies)
            progress_bar.progress(100)
            
            # 显示详细比较分析结果
            with st.expander("📊 详细比较分析报告", expanded=False):
                st.write(comparison_result)
            
            # 完成分析
            status_text.text("比较分析完成！")
            st.success("比较分析完成！")
            
        except Exception as e:
            logger.error(f"渲染比较分析时出错: {str(e)}")
            st.error(f"渲染比较分析时出错: {str(e)}")
    
    def _render_comparison_basic_info(self, companies: List[Dict[str, Any]]):
        """渲染比较分析的基础信息"""
        try:
            st.subheader("📋 公司基本信息对比")
            
            # 创建对比表格
            comparison_data = []
            for company in companies:
                comparison_data.append({
                    '公司': company['name'],
                    '主营业务': company['business'],
                    '营业收入': company['revenue'],
                    '净利润': company['net_profit'],
                    '研发投入': company['rd_investment'],
                    '专利数量': company['patent_count']
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df)
            
            # 添加业务领域对比
            st.write("### 业务领域对比")
            for company in companies:
                st.write(f"**{company['name']}**：{company['business']}")
                
        except Exception as e:
            logger.error(f"渲染比较基础信息时出错: {str(e)}")
            st.error(f"渲染比较基础信息时出错: {str(e)}")
    
    def _render_financial_analysis(self, company_data: Dict[str, Any]):
        """渲染财务分析图表"""
        try:
            # 创建财务指标仪表盘
            with st.expander("📊 关键财务指标", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    # 毛利率仪表盘
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=float(company_data['gross_margin'].replace('%', '')),
                        title={'text': "毛利率"},
                        gauge={'axis': {'range': [0, 100]},
                              'bar': {'color': "darkblue"},
                              'steps': [
                                  {'range': [0, 30], 'color': "lightgray"},
                                  {'range': [30, 60], 'color': "gray"},
                                  {'range': [60, 100], 'color': "darkgray"}
                              ]}
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # 资产负债率仪表盘
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=float(company_data['debt_ratio'].replace('%', '')),
                        title={'text': "资产负债率"},
                        gauge={'axis': {'range': [0, 100]},
                              'bar': {'color': "darkred"},
                              'steps': [
                                  {'range': [0, 40], 'color': "lightgray"},
                                  {'range': [40, 70], 'color': "gray"},
                                  {'range': [70, 100], 'color': "darkgray"}
                              ]}
                    ))
                    st.plotly_chart(fig, use_container_width=True)
            
            # 创建财务指标条形图
            with st.expander("📈 财务指标趋势", expanded=True):
                metrics = {
                    '营业收入': float(company_data['revenue'].replace('亿元', '')),
                    '净利润': float(company_data['net_profit'].replace('亿元', '')),
                    '研发投入': float(company_data['rd_investment'].replace('亿元', ''))
                }
                
                # 计算同比增长率
                revenue_growth = (metrics['营业收入'] - 10) / 10 * 100  # 假设上年为10亿
                profit_growth = (metrics['净利润'] - 1) / 1 * 100      # 假设上年为1亿
                
                # 显示增长率
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("营业收入增长率", f"{revenue_growth:.1f}%")
                with col2:
                    st.metric("净利润增长率", f"{profit_growth:.1f}%")
                
                # 财务指标条形图
                fig = px.bar(x=list(metrics.keys()), y=list(metrics.values()),
                            title="主要财务指标对比")
                st.plotly_chart(fig, use_container_width=True)
            
            # 添加财务健康度分析
            with st.expander("💪 财务健康度分析", expanded=False):
                health_metrics = {
                    '毛利率': float(company_data['gross_margin'].replace('%', '')),
                    '资产负债率': float(company_data['debt_ratio'].replace('%', '')),
                    '净利润率': float(company_data['net_profit'].replace('亿元', '')) / float(company_data['revenue'].replace('亿元', '')) * 100
                }
                
                # 创建雷达图
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=list(health_metrics.values()),
                    theta=list(health_metrics.keys()),
                    fill='toself',
                    name='财务健康度'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            logger.error(f"渲染财务分析时出错: {str(e)}")
            st.error(f"渲染财务分析时出错: {str(e)}")
    
    def _render_rd_analysis(self, company_data: Dict[str, Any]):
        """渲染研发创新分析"""
        try:
            # 创建研发投入分析
            with st.expander("🔬 研发投入分析", expanded=True):
                rd_investment = float(company_data['rd_investment'].replace('亿元', ''))
                revenue = float(company_data['revenue'].replace('亿元', ''))
                rd_ratio = (rd_investment / revenue) * 100
                
                # 研发投入占比仪表盘
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=rd_ratio,
                    title={'text': "研发投入占比"},
                    gauge={'axis': {'range': [0, 20]},
                          'bar': {'color': "darkgreen"},
                          'steps': [
                              {'range': [0, 5], 'color': "lightgray"},
                              {'range': [5, 10], 'color': "gray"},
                              {'range': [10, 20], 'color': "darkgray"}
                          ]}
                ))
                st.plotly_chart(fig, use_container_width=True)
                
                # 研发投入分析
                st.write("### 研发投入分析")
                st.write(f"- 研发投入金额：{rd_investment:.2f}亿元")
                st.write(f"- 研发投入占比：{rd_ratio:.2f}%")
                st.write(f"- 研发强度评估：{self._evaluate_rd_intensity(rd_ratio)}")
            
            # 创建专利分析
            with st.expander("📝 专利分析", expanded=True):
                patent_count = company_data['patent_count']
                patent_density = patent_count / float(company_data['revenue'].replace('亿元', ''))
                
                # 专利数量条形图
                fig = px.bar(x=['专利数量'], y=[patent_count],
                           title="专利数量")
                st.plotly_chart(fig, use_container_width=True)
                
                # 专利分析
                st.write("### 专利分析")
                st.write(f"- 专利总数：{patent_count}项")
                st.write(f"- 专利密度：{patent_density:.2f}项/亿元")
                st.write(f"- 创新效率评估：{self._evaluate_innovation_efficiency(patent_density)}")
            
            # 添加技术创新分析
            with st.expander("💡 技术创新分析", expanded=False):
                st.write("### 技术创新能力评估")
                st.write(f"- 技术风险等级：{company_data['tech_risk']}")
                st.write(f"- 风险应对建议：{self._generate_tech_risk_advice(company_data['tech_risk'])}")
                
        except Exception as e:
            logger.error(f"渲染研发分析时出错: {str(e)}")
            st.error(f"渲染研发分析时出错: {str(e)}")
    
    def _render_risk_analysis(self, company_data: Dict[str, Any]):
        """渲染风险评估"""
        try:
            # 创建风险雷达图
            with st.expander("⚠️ 风险雷达图", expanded=True):
                risk_metrics = {
                    '市场风险': self._get_risk_score(company_data['market_risk']),
                    '经营风险': self._get_risk_score(company_data['operation_risk']),
                    '财务风险': self._get_risk_score(company_data['financial_risk']),
                    '技术风险': self._get_risk_score(company_data['tech_risk'])
                }
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=list(risk_metrics.values()),
                    theta=list(risk_metrics.keys()),
                    fill='toself',
                    name='风险分布'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 3]
                        )),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 添加风险详细分析
            with st.expander("📊 风险详细分析", expanded=True):
                st.write("### 风险等级分布")
                for risk_type, risk_level in risk_metrics.items():
                    risk_icon = self._get_risk_icon(risk_level)
                    st.write(f"- {risk_icon} {risk_type}：{company_data[risk_type.lower().replace('风险', '_risk')]}")
                
                # 计算综合风险得分
                total_risk = sum(risk_metrics.values()) / len(risk_metrics)
                st.write(f"\n### 综合风险评估")
                st.write(f"- 综合风险得分：{total_risk:.2f}")
                st.write(f"- 风险等级：{self._get_risk_level(total_risk)}")
                
        except Exception as e:
            logger.error(f"渲染风险分析时出错: {str(e)}")
            st.error(f"渲染风险分析时出错: {str(e)}")
    
    def _render_investment_advice(self, company_data: Dict[str, Any]):
        """渲染投资建议"""
        try:
            # 计算投资价值得分
            metrics = self._calculate_investment_metrics(company_data)
            score = metrics['score']
            risk_score = metrics['risk_score']
            
            # 创建投资价值仪表盘
            with st.expander("💡 投资价值评估", expanded=True):
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={'text': "投资价值得分"},
                    gauge={'axis': {'range': [0, 10]},
                          'bar': {'color': "darkblue"},
                          'steps': [
                              {'range': [0, 3], 'color': "lightgray"},
                              {'range': [3, 7], 'color': "gray"},
                              {'range': [7, 10], 'color': "darkgray"}
                          ]}
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            # 添加投资建议
            with st.expander("📝 投资建议", expanded=True):
                st.write("### 投资价值分析")
                st.write(f"- 投资价值得分：{score:.2f}")
                st.write(f"- 风险等级：{self._get_risk_level(risk_score)}")
                st.write(f"- 投资建议：{self._generate_specific_advice(score, risk_score)}")
                
        except Exception as e:
            logger.error(f"渲染投资建议时出错: {str(e)}")
            st.error(f"渲染投资建议时出错: {str(e)}")
    
    def _render_financial_radar(self, companies: List[Dict[str, Any]]):
        """渲染财务雷达图"""
        try:
            # 准备数据
            metrics = ['营业收入', '净利润', '研发投入', '毛利率', '资产负债率']
            data = []
            
            for company in companies:
                company_metrics = {
                    '营业收入': float(company['revenue'].replace('亿元', '')),
                    '净利润': float(company['net_profit'].replace('亿元', '')),
                    '研发投入': float(company['rd_investment'].replace('亿元', '')),
                    '毛利率': float(company['gross_margin'].replace('%', '')),
                    '资产负债率': float(company['debt_ratio'].replace('%', ''))
                }
                data.append(company_metrics)
            
            # 创建雷达图
            fig = go.Figure()
            for i, company in enumerate(companies):
                fig.add_trace(go.Scatterpolar(
                    r=[data[i][metric] for metric in metrics],
                    theta=metrics,
                    fill='toself',
                    name=company['name']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(max(d.values()) for d in data)]
                    )),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            logger.error(f"渲染财务雷达图时出错: {str(e)}")
            st.error(f"渲染财务雷达图时出错: {str(e)}")
    
    def _render_risk_comparison(self, companies: List[Dict[str, Any]]):
        """渲染风险对比"""
        try:
            # 准备风险数据
            risk_types = ['市场风险', '经营风险', '财务风险', '技术风险']
            data = []
            
            for company in companies:
                company_risks = {
                    '市场风险': self._get_risk_score(company['market_risk']),
                    '经营风险': self._get_risk_score(company['operation_risk']),
                    '财务风险': self._get_risk_score(company['financial_risk']),
                    '技术风险': self._get_risk_score(company['tech_risk'])
                }
                data.append(company_risks)
            
            # 创建风险对比图
            fig = go.Figure()
            for i, company in enumerate(companies):
                fig.add_trace(go.Scatterpolar(
                    r=[data[i][risk] for risk in risk_types],
                    theta=risk_types,
                    fill='toself',
                    name=company['name']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 3]
                    )),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 添加风险详细对比
            st.write("### 风险等级详细对比")
            for risk_type in risk_types:
                st.write(f"\n**{risk_type}**")
                for company in companies:
                    risk_icon = self._get_risk_icon(self._get_risk_score(company[risk_type.lower().replace('风险', '_risk')]))
                    st.write(f"- {company['name']}：{risk_icon} {company[risk_type.lower().replace('风险', '_risk')]}")
            
        except Exception as e:
            logger.error(f"渲染风险对比时出错: {str(e)}")
            st.error(f"渲染风险对比时出错: {str(e)}")
    
    def _render_potential_comparison(self, companies: List[Dict[str, Any]]):
        """渲染发展潜力对比"""
        try:
            # 计算每个公司的发展潜力得分
            potential_scores = []
            for company in companies:
                metrics = self._calculate_investment_metrics(company)
                potential_scores.append({
                    'name': company['name'],
                    'score': metrics['score']
                })
            
            # 创建发展潜力对比图
            fig = px.bar(x=[score['name'] for score in potential_scores],
                        y=[score['score'] for score in potential_scores],
                        title="发展潜力对比")
            st.plotly_chart(fig, use_container_width=True)
            
            # 添加详细分析
            st.write("### 发展潜力详细分析")
            for score in sorted(potential_scores, key=lambda x: x['score'], reverse=True):
                st.write(f"- {score['name']}：{score['score']:.2f}")
            
        except Exception as e:
            logger.error(f"渲染发展潜力对比时出错: {str(e)}")
            st.error(f"渲染发展潜力对比时出错: {str(e)}")
    
    def _render_investment_comparison(self, companies: List[Dict[str, Any]]):
        """渲染投资建议对比"""
        try:
            # 计算每个公司的投资价值
            investment_scores = []
            for company in companies:
                metrics = self._calculate_investment_metrics(company)
                investment_scores.append({
                    'name': company['name'],
                    'score': metrics['score'],
                    'risk_score': metrics['risk_score']
                })
            
            # 创建投资价值对比图
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[score['name'] for score in investment_scores],
                y=[score['score'] for score in investment_scores],
                name='投资价值得分'
            ))
            fig.update_layout(title="投资价值对比")
            st.plotly_chart(fig, use_container_width=True)
            
            # 添加投资建议
            st.write("### 投资建议")
            for score in sorted(investment_scores, key=lambda x: x['score'], reverse=True):
                st.write(f"\n**{score['name']}**")
                st.write(f"- 投资价值得分：{score['score']:.2f}")
                st.write(f"- 风险等级：{self._get_risk_level(score['risk_score'])}")
                st.write(f"- 建议：{self._generate_specific_advice(score['score'], score['risk_score'])}")
            
        except Exception as e:
            logger.error(f"渲染投资建议对比时出错: {str(e)}")
            st.error(f"渲染投资建议对比时出错: {str(e)}")
    
    def _get_risk_score(self, risk_level: str) -> float:
        """获取风险等级对应的分数"""
        risk_scores = {
            '高': 3,
            '中等': 2,
            '低': 1
        }
        return risk_scores.get(risk_level, 2)
    
    def _get_risk_icon(self, risk_score: float) -> str:
        """获取风险等级对应的图标"""
        if risk_score >= 2.5:
            return '🔴'
        elif risk_score >= 1.5:
            return '🟡'
        else:
            return '🟢'
    
    def _get_risk_level(self, risk_score: float) -> str:
        """获取风险等级描述"""
        if risk_score >= 2.5:
            return '高'
        elif risk_score >= 1.5:
            return '中等'
        else:
            return '低'
    
    def _calculate_investment_metrics(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """计算投资相关指标"""
        try:
            # 计算风险得分
            risk_scores = {
                '高': 3,
                '中等': 2,
                '低': 1
            }
            risk_score = (
                risk_scores.get(company_data['market_risk'], 2) +
                risk_scores.get(company_data['operation_risk'], 2) +
                risk_scores.get(company_data['financial_risk'], 2) +
                risk_scores.get(company_data['tech_risk'], 2)
            ) / 4
            
            # 计算投资价值得分
            try:
                # 安全地转换数值，处理可能的格式问题
                revenue = float(company_data['revenue'].replace('亿元', '').strip())
                net_profit = float(company_data['net_profit'].replace('亿元', '').strip())
                rd_investment = float(company_data['rd_investment'].replace('亿元', '').strip())
                patent_count = float(company_data['patent_count'])
                
                # 避免除零错误
                if revenue <= 0:
                    revenue = 1  # 设置一个默认值
                    logger.warning(f"公司 {company_data['name']} 的营业收入为0或负数，使用默认值1")
                
                # 计算各项指标
                profit_ratio = (net_profit / revenue) * 40  # 盈利能力权重40%
                rd_ratio = (rd_investment / revenue) * 30    # 研发投入权重30%
                patent_ratio = (patent_count / revenue) * 30 # 创新能力权重30%
                
                # 计算总分
                score = profit_ratio + rd_ratio + patent_ratio
                
            except (ValueError, ZeroDivisionError) as e:
                logger.error(f"计算投资价值得分时出错: {str(e)}")
                score = 0
            
            return {
                'score': min(score, 10),  # 限制最高分为10
                'risk_score': risk_score
            }
            
        except Exception as e:
            logger.error(f"计算投资指标时出错: {str(e)}")
            return {'score': 0, 'risk_score': 2}
    
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
            return "建议加强技术研发投入，提升自主创新能力"
        elif tech_risk == "中等":
            return "建议保持现有研发投入，关注技术发展趋势"
        else:
            return "建议继续发挥技术优势，保持创新领先地位"
    
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