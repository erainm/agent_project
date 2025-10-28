# Created by erainm on 2025/10/28 16:59.
# IDE：PyCharm 
# @Project: agent_project
# @File：config
# @Description: 配置管理，加载config.ini
import configparser

class Config:
    # 初始化配置， 加载config.ini文件
    def __init__(self, config_file: str = "/Users/erainm/Documents/application/dev/workSpace/agent_project/config.ini"):
        # 创建配置解析器
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read(config_file)

        # LLM 配置
        # LLM 模型名
        self.LLM_MODEL = self.config.get('llm', 'model_name')
        # DashScope API 密钥
        self.DASHSCOPE_API_KEY = self.config.get('llm', 'dashscope_api_key')
        # DashScope API 地址
        self.DASHSCOPE_BASE_URL = self.config.get('llm', 'dashscope_base_url')
conf = Config()

if __name__ == '__main__':
    config = Config()
    print(config.LLM_MODEL)