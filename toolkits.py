from camel.toolkits import SearchToolkit, ArxivToolkit
from .config import Config
import time
from functools import lru_cache
from typing import List, Dict, Optional, Any
import logging
from camel.retrievers import BM25Retriever

logger = logging.getLogger(__name__)

class ToolkitManager:
    def __init__(self):
        """初始化工具包管理器"""
        try:
            # 初始化搜索工具
            self.search_toolkit = SearchToolkit()
            logger.debug("搜索工具初始化成功")
            
            # 初始化学术论文工具
            self.arxiv_toolkit = ArxivToolkit()
            logger.debug("学术论文工具初始化成功")
            
            # 初始化检索器
            self.retriever = BM25Retriever()
            logger.debug("检索器初始化成功")
            
        except Exception as e:
            logger.error(f"工具包初始化失败: {str(e)}")
            raise
    
    def search_company_info(self, company_name: str) -> List[Dict[str, Any]]:
        """搜索公司相关信息"""
        try:
            # 使用搜索工具查找公司信息
            results = self.search_toolkit.search_google(
                query=f"{company_name} 公司简介 主营业务",
                num_result_pages=3
            )
            logger.debug(f"搜索到 {len(results)} 条公司信息")
            return results
        except Exception as e:
            logger.error(f"搜索公司信息失败: {str(e)}")
            return []
    
    def get_annual_report(self, company_name: str, year: int) -> str:
        """获取公司年报内容"""
        try:
            # 使用浏览器工具获取年报内容
            url = f"https://www.cninfo.com.cn/new/fulltextSearch/full?searchkey={company_name} {year}年报"
            content = self.browser_toolkit.get_webpage_content(url)
            logger.debug(f"成功获取 {company_name} {year}年报内容")
            return content
        except Exception as e:
            logger.error(f"获取年报内容失败: {str(e)}")
            return ""
    
    def search_academic_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """搜索相关学术论文"""
        try:
            # 使用学术论文工具搜索相关论文
            papers = self.arxiv_toolkit.search_papers(
                query=query,
                max_results=max_results
            )
            logger.debug(f"搜索到 {len(papers)} 篇相关论文")
            return papers
        except Exception as e:
            logger.error(f"搜索学术论文失败: {str(e)}")
            return []
    
    def retrieve_relevant_content(self, query: str, documents: List[str]) -> List[str]:
        """检索相关文档内容"""
        try:
            # 使用检索器查找相关文档
            results = self.retriever.get_relevant_documents(
                query=query,
                documents=documents,
                top_k=3
            )
            logger.debug(f"检索到 {len(results)} 条相关文档")
            return results
        except Exception as e:
            logger.error(f"检索文档失败: {str(e)}")
            return []
    
    def _validate_toolkits(self):
        """验证所有工具包是否正常工作"""
        try:
            # 测试搜索工具
            test_query = "financial analysis methodology"
            results = self.search_toolkit.search_duckduckgo(test_query)
            print("搜索工具测试成功")
        except Exception as e:
            print(f"搜索工具测试失败: {str(e)}")
        
        try:
            # 测试 Arxiv 工具
            papers = self.arxiv_toolkit.search_papers(test_query)
            print("Arxiv 工具测试成功")
        except Exception as e:
            print(f"Arxiv 工具测试失败: {str(e)}")
    
    def _retry_with_backoff(self, func, *args, max_retries=3, initial_delay=1, **kwargs):
        """带退避的重试机制"""
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"尝试 {attempt + 1} 失败，{delay} 秒后重试...")
                time.sleep(delay)
                delay *= 2
    
    @lru_cache(maxsize=100)
    def search_papers(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索学术论文（带缓存）"""
        try:
            return self._retry_with_backoff(
                self.arxiv_toolkit.search_papers,
                query,
                max_results=max_results
            )
        except Exception as e:
            print(f"搜索论文失败: {str(e)}")
            return []
    
    @lru_cache(maxsize=100)
    def search_web(self, query: str) -> List[Dict]:
        """搜索网页内容（带缓存）"""
        try:
            return self._retry_with_backoff(
                self.search_toolkit.search_duckduckgo,
                query
            )
        except Exception as e:
            print(f"网页搜索失败: {str(e)}")
            return []
    
    @lru_cache(maxsize=100)
    def browse_webpage(self, url: str) -> str:
        """浏览网页内容（带缓存）"""
        try:
            return self._retry_with_backoff(
                self.browser_toolkit.browse_webpage,
                url
            )
        except Exception as e:
            print(f"浏览网页失败: {str(e)}")
            return "" 