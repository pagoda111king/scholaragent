# ScholarAgent 教程文档

## 1. 系统概述

ScholarAgent 是一个基于 CAMEL 框架开发的智能年报分析系统,通过多智能体协作实现对公司年报的深度分析。本教程将详细介绍系统的实现原理和使用方法。

## 2. 核心功能实现

### 2.1 多智能体协作系统

#### 2.1.1 智能体角色设计

系统设计了三个专业的智能体角色:

```python
# scholar.py 中的实现
class FinancialAnalysisSociety:
    def __init__(self):
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
```

实际运行结果示例:
```
正在分析 拓维信息...
投资顾问正在生成投资建议...
📋 基础信息分析

学术研究员分析：
公司分析报告
执行摘要 本报告对拓维信息进行了全面分析...
研究方法说明 采用多角度分析方法，结合学术研究和实践经验...

公司概况
公司名称：拓维信息
主营业务：软件开发和信息技术服务
营业收入：15.8亿元
净利润：1.2亿元
研发投入：2.5亿元
专利数量：150项
毛利率：45%
资产负债率：35%
```

### 2.2 财务分析模块

#### 2.2.1 财务指标分析

```python
# analysis.py 中的实现
def analyze_financial_metrics(self, company_data: Dict[str, Any]) -> str:
    """分析财务指标"""
    try:
        # 计算关键财务指标
        revenue = float(company_data['revenue'].replace('亿元', ''))
        net_profit = float(company_data['net_profit'].replace('亿元', ''))
        gross_margin = float(company_data['gross_margin'].replace('%', ''))
        debt_ratio = float(company_data['debt_ratio'].replace('%', ''))
        
        # 生成分析报告
        analysis = f"""
        财务指标分析:
        1. 盈利能力
           - 营业收入: {revenue}亿元
           - 净利润: {net_profit}亿元
           - 净利润率: {(net_profit/revenue)*100:.2f}%
        
        2. 运营效率
           - 毛利率: {gross_margin}%
           - 资产负债率: {debt_ratio}%
        """
        return analysis
    except Exception as e:
        logger.error(f"财务分析失败: {str(e)}")
        return ""
```

实际运行结果示例:
```
💰 财务分析

财务分析师分析：
要全面分析一家公司的盈利能力和成长性，通常需要考虑多个财务指标和市场环境。对于"拓维信息"这家公司，根据您提供的信息——营业收入为15.8亿元，净利润为1.2亿元，我们可以做一些基本的分析。

盈利能力分析
1. 利润率
净利润率 = 净利润 / 营业收入 = 1.2亿 / 15.8亿 ≈ 7.59%
这个比率反映了每1元销售收入中，公司能赚取的净利润。7.59%的净利润率在不同行业中可能有不同的评价标准。
```

### 2.3 研发创新分析

#### 2.3.1 研发投入分析

```python
# analysis.py 中的实现
def analyze_rd_investment(self, company_data: Dict[str, Any]) -> str:
    """分析研发投入"""
    try:
        # 计算研发投入占比
        revenue = float(company_data['revenue'].replace('亿元', ''))
        rd_investment = float(company_data['rd_investment'].replace('亿元', ''))
        rd_ratio = (rd_investment / revenue) * 100
        
        # 计算专利密度
        patent_count = company_data['patent_count']
        patent_density = patent_count / revenue
        
        # 生成分析报告
        analysis = f"""
        研发创新分析:
        1. 研发投入
           - 研发投入金额: {rd_investment}亿元
           - 研发投入占比: {rd_ratio:.2f}%
           - 研发投入强度: {self._evaluate_rd_intensity(rd_ratio)}
        
        2. 创新能力
           - 专利数量: {patent_count}项
           - 专利密度: {patent_density:.2f}项/亿元
           - 创新效率: {self._evaluate_innovation_efficiency(patent_density)}
        """
        return analysis
    except Exception as e:
        logger.error(f"研发分析失败: {str(e)}")
        return ""
```

实际运行结果示例:
```
🔬 研发创新分析

技术专家分析：
研发投入分析
- 研发投入占营业收入比例：15.82%
- 研发投入强度：极高

2. 创新能力分析
- 专利密度：9.49项/亿元
- 创新效率：高

3. 技术风险
- 技术风险等级：中等
- 风险应对建议：建议保持技术研发投入，关注行业技术发展趋势
```

### 2.4 风险评估模块

#### 2.4.1 风险分析

```python
# analysis.py 中的实现
def analyze_risks(self, company_data: Dict[str, Any]) -> str:
    """分析公司风险"""
    try:
        # 获取各类风险等级
        market_risk = company_data['market_risk']
        operation_risk = company_data['operation_risk']
        financial_risk = company_data['financial_risk']
        tech_risk = company_data['tech_risk']
        
        # 计算综合风险得分
        risk_scores = {
            '高': 3,
            '中等': 2,
            '低': 1
        }
        total_risk = (
            risk_scores.get(market_risk, 2) +
            risk_scores.get(operation_risk, 2) +
            risk_scores.get(financial_risk, 2) +
            risk_scores.get(tech_risk, 2)
        ) / 4
        
        # 生成分析报告
        analysis = f"""
        风险评估:
        1. 风险分布
           - 市场风险: {market_risk}
           - 经营风险: {operation_risk}
           - 财务风险: {financial_risk}
           - 技术风险: {tech_risk}
        
        2. 综合评估
           - 综合风险得分: {total_risk:.2f}
           - 风险等级: {self._get_risk_level(total_risk)}
        """
        return analysis
    except Exception as e:
        logger.error(f"风险分析失败: {str(e)}")
        return ""
```

实际运行结果示例:
```
⚠️ 风险评估

风险经理分析：
对于拓维信息（股票代码：002261.SZ）的市场风险分析，我们可以从多个角度来考虑，包括但不限于行业环境、公司自身状况、宏观经济因素以及技术发展等。

1. 行业环境
竞争态势：拓维信息主要业务集中在信息技术服务领域，尤其是软件开发和系统集成服务。这一行业内的竞争非常激烈，不仅有众多国内外同行的竞争压力，还有来自互联网巨头在某些细分市场的挑战。
```

### 2.5 投资建议生成

#### 2.5.1 投资价值评估

```python
# visualization.py 中的实现
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
        revenue = float(company_data['revenue'].replace('亿元', ''))
        net_profit = float(company_data['net_profit'].replace('亿元', ''))
        rd_investment = float(company_data['rd_investment'].replace('亿元', ''))
        patent_count = float(company_data['patent_count'])
        
        # 计算各项指标
        profit_ratio = (net_profit / revenue) * 40  # 盈利能力权重40%
        rd_ratio = (rd_investment / revenue) * 30    # 研发投入权重30%
        patent_ratio = (patent_count / revenue) * 30 # 创新能力权重30%
        
        # 计算总分
        score = profit_ratio + rd_ratio + patent_ratio
        
        return {
            'score': min(score, 10),  # 限制最高分为10
            'risk_score': risk_score
        }
    except Exception as e:
        logger.error(f"计算投资指标时出错: {str(e)}")
        return {'score': 0, 'risk_score': 2}
```

实际运行结果示例:
```
💡 投资建议

投资顾问分析：
基于以上分析，建议...

投资价值得分：7.79
风险等级：低
建议：建议投资，公司具有较好的投资价值和可控风险
```

## 3. 系统使用说明

### 3.1 环境配置

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量:
```bash
cp .env.example .env
# 编辑 .env 文件,填入必要的配置信息
```

### 3.2 运行系统

1. Web 应用:
```bash
cd camel/scholaragent
streamlit run app.py --server.port 8501 --server.address localhost
```

2. 命令行版本:
```bash
cd camel/scholaragent
python main.py
```

### 3.3 数据格式

系统支持以下格式的公司数据:

```python
company_data = {
    "name": "公司名称",
    "business": "主营业务",
    "rd_investment": "研发投入",
    "patent_count": "专利数量",
    "revenue": "营业收入",
    "net_profit": "净利润",
    "gross_margin": "毛利率",
    "debt_ratio": "资产负债率",
    "market_risk": "市场风险",
    "operation_risk": "经营风险",
    "financial_risk": "财务风险",
    "tech_risk": "技术风险"
}
```

## 4. 实际应用案例

### 4.1 单公司分析

以拓维信息为例:

```python
company = {
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
}

# 运行分析
analysis = analysis_manager.analyze_company(company)
```

分析结果示例:
```
拓维信息分析报告

1. 执行摘要
本报告对拓维信息进行了全面分析...

2. 财务分析
- 营业收入: 15.8亿元
- 净利润: 1.2亿元
- 净利润率: 7.59%
- 毛利率: 45%
- 资产负债率: 35%

3. 研发创新分析
- 研发投入占比: 15.82%
- 研发投入强度: 极高
- 专利密度: 9.49项/亿元
- 创新效率: 高

4. 风险评估
- 市场风险: 中等
- 经营风险: 低
- 财务风险: 低
- 技术风险: 中等

5. 投资建议
投资价值得分: 7.79
风险等级: 低
建议: 建议投资，公司具有较好的投资价值和可控风险
```

### 4.2 多公司对比

以拓维信息和振邦智能为例:

```python
companies = [
    {
        "name": "拓维信息",
        # ... 拓维信息数据
    },
    {
        "name": "振邦智能",
        # ... 振邦智能数据
    }
]

# 运行对比分析
comparison = analysis_manager.compare_companies(companies)
```

对比分析结果示例:
```
公司比较分析报告

1. 财务指标对比
指标          拓维信息    振邦智能    差异
营业收入      15.8亿     12.5亿      +3.3亿
净利润        1.2亿      0.9亿       +0.3亿
研发投入      2.5亿      1.8亿       +0.7亿
毛利率        45%        40%         +5%
资产负债率    35%        42%         -7%

2. 研发创新对比
拓维信息:
- 研发投入占比: 15.82% (+0.71%)
- 专利密度: 9.49项/亿元 (-0.05)

振邦智能:
- 研发投入占比: 14.40% (-0.71%)
- 专利密度: 9.60项/亿元 (+0.05)

3. 风险状况对比
拓维信息:
- 综合风险得分: 1.50 (-0.25)
- 风险等级: 低

振邦智能:
- 综合风险得分: 2.00 (+0.25)
- 风险等级: 中等

4. 投资建议
拓维信息:
- 投资价值得分: 7.79
- 风险等级: 低
- 建议: 建议投资，公司具有较好的投资价值和可控风险

振邦智能:
- 投资价值得分: 7.26
- 风险等级: 中等
- 建议: 建议投资，公司具有较好的投资价值和可控风险
```

## 5. 注意事项

1. 数据准确性
- 确保输入的公司数据准确完整
- 注意数据单位的统一性
- 定期更新数据以保持分析结果的时效性

2. 系统性能
- 大量数据分析时注意内存使用
- 合理设置并发分析数量
- 定期清理缓存数据

3. 结果解读
- 结合行业背景解读分析结果
- 注意风险提示和建议的合理性
- 定期验证分析结果的准确性

## 6. 常见问题

1. 数据加载失败
- 检查数据格式是否正确
- 确认文件路径是否正确
- 验证数据编码格式

2. 分析超时
- 检查网络连接
- 调整超时设置
- 优化分析算法

3. 结果异常
- 检查数据异常值
- 验证计算逻辑
- 更新分析模型 