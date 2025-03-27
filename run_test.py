import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scholaragent.test_browser import test_browser

if __name__ == "__main__":
    test_browser() 