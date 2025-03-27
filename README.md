# ScholarAgent - 智能年报分析系统

基于 CAMEL 框架开发的智能年报分析系统，通过多智能体协作实现对公司年报的深度分析。

## 功能特点

- 多智能体协作分析
- 实时进度显示
- 可视化分析结果
- 支持多公司对比
- 自动生成分析报告
详情请参考逻辑讲解DIALOGUE_PROCESS.md和代码讲解TECHNICAL_DETAILS.md

## 安装说明

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

## 使用方法

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