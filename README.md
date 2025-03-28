# ScholarAgent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 CAMEL 框架开发的智能年报分析系统，通过多智能体协作实现对公司年报的深度分析。

## 功能特点

- 多智能体协作分析
- 实时进度显示
- 可视化分析结果
- 支持多公司对比
- 自动生成分析报告

## 快速开始

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/pagoda111king/scholaragent.git
cd scholaragent
```

2. 安装依赖：
```bash
pip install -r requirements.txt
还有camel 相关环境 配置过的直接增加我的环境就行没配置的我之后更新完整版本
```

3. 配置环境变量：
```bash
cp .env.example .env
```
然后编辑 `.env` 文件，填入你的 API 密钥和其他配置。

### 运行

1. 运行 Web 应用：
```bash
cd camel/scholaragent
streamlit run app.py --server.port 8501 --server.address localhost
```

2. 运行命令行版本：
```bash
cd camel/scholaragent
python main.py
```

## 项目结构

```
scholaragent/
├── camel/
│   └── scholaragent/
│       ├── app.py              # Web 应用入口
│       ├── main.py             # 命令行入口
│       ├── analysis.py         # 分析管理模块
│       ├── config.py           # 配置管理模块
│       ├── visualization.py    # 可视化模块
│       ├── toolkits.py         # 工具包管理
│       └── roles.py            # 角色管理
├── requirements.txt            # 项目依赖
├── .env.example               # 环境变量示例
└── README.md                  # 项目文档
```

## 详细教程

### 1. 系统概述

ScholarAgent 是一个基于 CAMEL 框架开发的智能年报分析系统,通过多智能体协作实现对公司年报的深度分析。本教程将详细介绍系统的实现原理和使用方法。感谢datawhale给我这个机会还要camel社区来学习多智能体。下面是这次的打卡和学习记录

### 2. 基于研报摘要分析多智能体系统的task章节打卡

#### Chapter 1: 多智能体协作系统实现

#### 1.1 学习要点
- 理解多智能体系统的设计原理
- 掌握角色扮演系统的实现方法
- 学习智能体间的协作机制
- 了解系统提示词的设计原则

#### 1.2 CAMEL 知识点应用
1. **多智能体系统设计** (参考 Chapter 1.1-1.3)
   - 使用 `camel.agents` 包中的 `ChatAgent` 类实现智能体
   - 应用 `camel.societies` 包中的 `RolePlaying` 类实现角色扮演
   - 参考 Chapter 1.4 中的智能体协作机制

2. **角色设计** (参考 Chapter 1.5-1.7)
   - 使用 `camel.types.RoleType` 定义角色类型
   - 应用 `camel.messages.BaseMessage` 实现消息传递
   - 利用 `camel.memories.AgentMemory` 管理对话历史

3. **系统提示词** (参考 Chapter 1.8-1.9)
   - 使用 `camel.prompts.PromptTemplate` 设计系统提示词
   - 应用 `camel.prompts.PromptTemplateGenerator` 生成提示词模板

#### 1.3 代码实现
```python
# scholar.py 中的实现
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from camel.societies import RolePlaying
from camel.memories import AgentMemory
from camel.prompts import PromptTemplate

class FinancialAnalysisSociety:
    def __init__(self):
        # 初始化记忆系统
        self.memory = AgentMemory()
        
        # 初始化角色扮演系统
        self.society = RolePlaying(
            model=self.model,
            roles=self.roles,
            memory=self.memory
        )
        
        # 初始化系统提示词
        self.system_prompt = PromptTemplate(
            template="""你是一个专业的金融分析团队，由以下角色组成：
            1. 学术研究员：负责检索和分析相关学术论文
            2. 财务分析师：负责评估公司财务表现
            3. 风险管理师：负责评估公司风险状况"""
        )
```

#### 1.4 实际应用
```python
# main.py 中的使用示例
def main():
    print("开始分析拓维信息和振邦智能的年报摘要...")
    
    society = FinancialAnalysisSociety()
    
    # 拓维信息数据
    talkweb_data = {
        "company_name": "拓维信息",
        "year": 2023,
        "risk_metrics": {
            "capital_adequacy_ratio": 0.482,
            "profit_margin": 0.014,
            "growth_rate": 0.4102
        },
        "financial_statements": {
            "total_assets": 5287129846.78,
            "net_profit": 44963139.28,
            "revenue": 3154141699.10,
            "operating_cash_flow": -1169883405.68
        }
    }
    
    # 运行分析
    analysis = society.analyze_company(talkweb_data)
```

#### 1.5 运行结果
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

### Chapter 2: 财务分析模块实现

#### 2.1 学习要点
- 掌握财务指标的计算方法
- 理解财务分析的关键维度
- 学习财务数据的处理技巧
- 了解财务分析报告的生成逻辑

#### 2.2 CAMEL 知识点应用
1. **数据处理** (参考 Chapter 2.1-2.3)
   - 使用 `camel.toolkits` 包中的数据处理工具
   - 应用 `camel.retrievers` 包中的检索器进行数据检索
   - 利用 `camel.embeddings` 包进行数据向量化

2. **分析报告生成** (参考 Chapter 2.4-2.6)
   - 使用 `camel.prompts` 包生成分析报告模板
   - 应用 `camel.visualization` 包进行数据可视化
   - 利用 `camel.memories` 包管理分析历史

#### 2.3 代码实现
```python
# analysis.py 中的实现
from camel.toolkits import SearchToolkit
from camel.retrievers import BM25Retriever
from camel.embeddings import OpenAIEmbedding
from camel.prompts import PromptTemplate
from camel.visualization import VisualizationManager

class AnalysisManager:
    def __init__(self, config: Config):
        # 初始化检索器
        self.retriever = BM25Retriever()
        
        # 初始化向量化工具
        self.embedding = OpenAIEmbedding()
        
        # 初始化可视化管理器
        self.visualization = VisualizationManager()
```

#### 2.4 实际应用
```python
# 在 main.py 中使用财务分析模块
def analyze_company_financials(company_data):
    analysis_manager = AnalysisManager(config)
    financial_analysis = analysis_manager.analyze_financial_metrics(company_data)
    return financial_analysis
```

#### 2.5 运行结果
```
💰 财务分析

财务分析师分析：
要全面分析一家公司的盈利能力和成长性，通常需要考虑多个财务指标和市场环境。对于"拓维信息"这家公司，根据您提供的信息——营业收入为15.8亿元，净利润为1.2亿元，我们可以做一些基本的分析。

盈利能力分析
1. 利润率
净利润率 = 净利润 / 营业收入 = 1.2亿 / 15.8亿 ≈ 7.59%
这个比率反映了每1元销售收入中，公司能赚取的净利润。7.59%的净利润率在不同行业中可能有不同的评价标准。
```

### Chapter 3: 研发创新分析模块实现

#### 3.1 学习要点
- 理解研发投入的分析方法
- 掌握专利密度的计算方式
- 学习创新效率的评估标准
- 了解技术风险的分析维度

#### 3.2 CAMEL 知识点应用
1. **向量数据库应用** (参考 Chapter 4.1-4.3)
   - 使用 `camel.storages.vectordb_storages` 包进行向量存储
   - 应用 Milvus 数据库存储专利向量
   - 利用向量相似度搜索进行专利分析

2. **检索系统** (参考 Chapter 4.4-4.6)
   - 使用 `camel.retrievers` 包实现专利检索
   - 应用 `camel.embeddings` 包进行专利文本向量化
   - 利用 `camel.memories` 包管理检索历史

3. **数据存储优化** (参考 Chapter 4.7)
   - 使用向量数据库的索引优化
   - 应用数据压缩和缓存策略
   - 实现高效的数据检索机制

#### 3.3 代码实现
```python
# analysis.py 中的实现
from camel.storages.vectordb_storages import MilvusStorage
from camel.retrievers import RAGRetriever
from camel.embeddings import OpenAIEmbedding

class RDInnovationAnalyzer:
    def __init__(self):
        # 初始化向量存储
        self.vector_storage = MilvusStorage()
        
        # 初始化检索器
        self.retriever = RAGRetriever(
            embedding_model=OpenAIEmbedding(),
            retrieval_model=BM25Retriever()
        )
```

#### 3.4 实际应用
```python
# 在 main.py 中使用研发分析模块
def analyze_company_rd(company_data):
    analysis_manager = AnalysisManager(config)
    rd_analysis = analysis_manager.analyze_rd_investment(company_data)
    return rd_analysis
```

#### 3.5 运行结果
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

### Chapter 4: 风险评估模块实现

#### 4.1 学习要点
- 掌握风险评分的计算方法
- 理解多维度风险评估体系
- 学习风险等级的划分标准
- 了解风险建议的生成逻辑

#### 4.2 CAMEL 知识点应用
1. **风险评估系统** (参考 Chapter 5.1-5.3)
   - 使用 `camel.agents` 包实现风险评估智能体
   - 应用 `camel.memories` 包管理风险评估历史
   - 利用 `camel.prompts` 包生成风险评估报告

2. **数据可视化** (参考 Chapter 5.4-5.6)
   - 使用 `camel.visualization` 包进行风险可视化
   - 应用 `camel.toolkits` 包进行数据处理
   - 利用 `camel.retrievers` 包检索历史风险数据

3. **风险预警机制** (参考 Chapter 5.7)
   - 实现实时风险监控
   - 应用风险预警规则
   - 生成风险预警报告

#### 4.3 代码实现
```python
# analysis.py 中的实现
from camel.agents import ChatAgent
from camel.memories import AgentMemory
from camel.prompts import PromptTemplate
from camel.visualization import VisualizationManager

class RiskAnalyzer:
    def __init__(self):
        # 初始化风险评估智能体
        self.risk_agent = ChatAgent(
            role_name="Risk Manager",
            role_type=RoleType.ASSISTANT,
            memory=AgentMemory()
        )
        
        # 初始化可视化管理器
        self.visualization = VisualizationManager()
```

#### 4.4 实际应用
```python
# 在 main.py 中使用风险评估模块
def analyze_company_risks(company_data):
    analysis_manager = AnalysisManager(config)
    risk_analysis = analysis_manager.analyze_risks(company_data)
    return risk_analysis
```

#### 4.5 运行结果
```
⚠️ 风险评估

风险经理分析：
对于拓维信息（股票代码：002261.SZ）的市场风险分析，我们可以从多个角度来考虑，包括但不限于行业环境、公司自身状况、宏观经济因素以及技术发展等。

1. 行业环境
竞争态势：拓维信息主要业务集中在信息技术服务领域，尤其是软件开发和系统集成服务。这一行业内的竞争非常激烈，不仅有众多国内外同行的竞争压力，还有来自互联网巨头在某些细分市场的挑战。
```

### Chapter 5: 投资建议生成模块实现

#### 5.1 学习要点
- 掌握投资价值评估方法
- 理解风险收益平衡原则
- 学习投资建议的生成逻辑
- 了解多维度评分体系

#### 5.2 CAMEL 知识点应用
1. **投资分析系统** (参考 Chapter 6.1-6.3)
   - 使用 `camel.agents` 包实现投资分析智能体
   - 应用 `camel.memories` 包管理投资分析历史
   - 利用 `camel.prompts` 包生成投资建议报告

2. **数据集成** (参考 Chapter 6.4-6.6)
   - 使用 `camel.toolkits` 包集成外部数据
   - 应用 `camel.retrievers` 包检索市场数据
   - 利用 `camel.embeddings` 包进行数据向量化

3. **投资策略优化** (参考 Chapter 6.7)
   - 实现投资组合优化
   - 应用风险评估模型
   - 生成投资策略建议

#### 5.3 代码实现
```python
# visualization.py 中的实现
from camel.agents import ChatAgent
from camel.memories import AgentMemory
from camel.prompts import PromptTemplate
from camel.toolkits import SearchToolkit
from camel.retrievers import BM25Retriever

class InvestmentAdvisor:
    def __init__(self):
        # 初始化投资分析智能体
        self.investment_agent = ChatAgent(
            role_name="Investment Advisor",
            role_type=RoleType.ASSISTANT,
            memory=AgentMemory()
        )
        
        # 初始化搜索工具
        self.search_toolkit = SearchToolkit()
        
        # 初始化检索器
        self.retriever = BM25Retriever()
```

#### 5.4 实际应用
```python
# 在 main.py 中使用投资建议模块
def generate_investment_advice(company_data):
    analysis_manager = AnalysisManager(config)
    investment_metrics = analysis_manager._calculate_investment_metrics(company_data)
    advice = analysis_manager._generate_specific_advice(
        investment_metrics['score'],
        investment_metrics['risk_score']
    )
    return advice
```

#### 5.5 运行结果
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


### 5. 注意事项

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

### 6. 常见问题

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

## 配置说明

1. 在 `.env` 文件中配置以下内容：
   - OpenAI API 密钥
   - 模型参数
   - 系统配置

2. 确保已安装所有必要的依赖包

## 注意事项

1. 请确保 API 密钥的安全性，不要将其提交到代码仓库
2. 建议使用虚拟环境运行项目
3. 确保 Python 版本 >= 3.8

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- huiwentang5@gmail.com
- 项目链接：[https://github.com/pagoda111king/scholaragent]

## 致谢

- 感谢 [CAMEL](https://github.com/camel-ai/camel) 框架
- 感谢 [Datawhale](https://github.com/datawhalechina) 社区
- 感谢所有贡献者的付出