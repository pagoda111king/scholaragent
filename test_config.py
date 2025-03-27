import os
import sys
import pytest
from typing import List

from camel.memories import ChatHistoryMemory
from camel.retrievers import BM25Retriever
from camel.messages import BaseMessage
from camel.types import ChatCompletionUserMessageParam
from config import Config  # 直接从当前目录导入

def test_basic_config():
    """测试基础配置（不需要 API Key）"""
    try:
        config = Config()
        assert config is not None
        assert config.model_name == "Qwen/Qwen2.5-72B-Instruct"
        assert config.temperature == 0.7
        print("基础配置测试通过")
    except Exception as e:
        print(f"基础配置测试失败: {str(e)}")
        raise

def test_memory_system():
    """测试记忆系统（不需要 API Key）"""
    try:
        config = Config()
        memory = config.get_memory()
        assert memory is not None
        assert isinstance(memory, ChatHistoryMemory)
        print("记忆系统测试通过")
    except Exception as e:
        print(f"记忆系统测试失败: {str(e)}")
        raise

def test_retriever():
    """测试检索器（不需要 API Key）"""
    try:
        config = Config()
        retriever = config.get_retriever()
        assert retriever is not None
        assert isinstance(retriever, BM25Retriever)
        print("检索器测试通过")
    except Exception as e:
        print(f"检索器测试失败: {str(e)}")
        raise

def test_proxy_settings():
    """测试代理设置（不需要 API Key）"""
    try:
        config = Config()
        assert "HTTP_PROXY" not in os.environ
        assert "HTTPS_PROXY" not in os.environ
        print("代理设置测试通过")
    except Exception as e:
        print(f"代理设置测试失败: {str(e)}")
        raise

# 需要 API Key 的测试
def test_model_factory():
    """测试模型工厂（需要 API Key）"""
    try:
        config = Config()
        model = config.get_model()
        assert model is not None
        print("模型工厂测试通过")
    except Exception as e:
        print(f"模型工厂测试失败: {str(e)}")
        raise

def test_model_inference():
    """测试模型推理（需要 API Key）"""
    try:
        config = Config()
        model = config.get_model()
        messages = [ChatCompletionUserMessageParam(role="user", content="测试消息")]
        response = model._run(messages)
        assert response is not None
        print("模型推理测试通过")
    except Exception as e:
        print(f"模型推理测试失败: {str(e)}")
        raise

if __name__ == "__main__":
    print("开始运行基础测试（不需要 API Key）...")
    test_basic_config()
    test_memory_system()
    test_retriever()
    test_proxy_settings()
    print("\n基础测试完成！\n")
    
    print("开始运行需要 API Key 的测试...")
    test_model_factory()
    test_model_inference()
    print("\n所有测试完成！") 