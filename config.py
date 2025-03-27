import os
import logging
from typing import List
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.models.model_factory import ModelType, ModelPlatformType
from camel.retrievers import BM25Retriever
from camel.messages import BaseMessage
from camel.utils import OpenAITokenCounter
from camel.memories import ChatHistoryMemory, ScoreBasedContextCreator

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class Config:
    def __init__(self):
        # 模型配置
        self.model_name = "Qwen/Qwen2.5-72B-Instruct"
        self.temperature = 0.7
        self.api_key = "85cac904-b94b-4c92-8ec3-bf1c6611c5f3"  # 直接使用 API Key
        
        logger.debug(f"初始化配置: model_name={self.model_name}")
        
        # 检查并清除代理设置
        if "HTTP_PROXY" in os.environ:
            logger.debug(f"清除 HTTP_PROXY: {os.environ['HTTP_PROXY']}")
            del os.environ["HTTP_PROXY"]
        if "HTTPS_PROXY" in os.environ:
            logger.debug(f"清除 HTTPS_PROXY: {os.environ['HTTPS_PROXY']}")
            del os.environ["HTTPS_PROXY"]
        
        # 初始化基础组件
        self._init_basic_components()
        
        # 如果有 API Key，初始化模型工厂
        if self.api_key:
            self._init_model_factory()
    
    def _init_basic_components(self):
        """初始化基本组件"""
        # 初始化模型
        self.model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4,
        )
        
        # 初始化 token counter
        self.token_counter = OpenAITokenCounter(ModelType.GPT_4)
        
        # 初始化 context creator
        self.context_creator = ScoreBasedContextCreator(
            token_counter=self.token_counter,
            token_limit=self.model.token_limit,
        )
        
        # 初始化记忆
        self.memory = ChatHistoryMemory(
            context_creator=self.context_creator,
            window_size=10,
            agent_id="scholar_agent"
        )
    
    def _init_model_factory(self):
        """初始化模型工厂（需要 API Key）"""
        try:
            logger.debug("开始初始化模型工厂...")
            self.model_factory = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
                model_type=self.model_name,
                api_key=self.api_key,
                url="https://api-inference.modelscope.cn/v1",
                model_config_dict={
                    "temperature": self.temperature,
                    "max_tokens": 2000
                }
            )
            logger.debug("模型工厂初始化成功")
        except Exception as e:
            logger.error(f"模型工厂初始化失败: {str(e)}")
            raise
    
    def _validate_config(self):
        """验证配置是否正确"""
        # 验证代理设置
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        logger.debug(f"当前代理设置 - HTTP_PROXY: {http_proxy}, HTTPS_PROXY: {https_proxy}")
    
    def get_model(self):
        """获取模型实例"""
        if not hasattr(self, 'model_factory'):
            raise ValueError("模型工厂未初始化，请先设置 OPENAI_API_KEY")
        return self.model_factory
    
    def get_memory(self):
        """获取记忆系统实例"""
        return self.memory
    
    def get_retriever(self):
        """获取检索器实例"""
        return self.retriever 