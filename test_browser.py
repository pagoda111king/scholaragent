from camel.toolkits import BrowserToolkit
from .config import Config

def test_browser():
    # 初始化配置
    config = Config()
    
    # 初始化 BrowserToolkit
    browser = BrowserToolkit()
    
    # 测试网页浏览功能
    url = "https://www.baidu.com"
    print(f"\n测试浏览网页: {url}")
    try:
        result = browser.browse_webpage(url)
        print("浏览结果:", result[:200] + "...")  # 只显示前200个字符
    except Exception as e:
        print("浏览失败:", str(e))
    
    # 测试网页内容提取功能
    print("\n测试网页内容提取:")
    try:
        content = browser.extract_content(url)
        print("提取的内容:", content[:200] + "...")  # 只显示前200个字符
    except Exception as e:
        print("内容提取失败:", str(e))

if __name__ == "__main__":
    test_browser() 