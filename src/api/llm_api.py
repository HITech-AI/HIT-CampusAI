import os
import requests
from dotenv import load_dotenv

# 加载环境变量（将API密钥存放在项目根目录的 .env 文件中）
load_dotenv()
API_KEY = os.getenv("HIT_AI_API_KEY")
API_URL = os.getenv("HIT_AI_API_URL")

# 校验环境变量，避免因未配置导致的调用失败
def check_env_variables() -> bool:
    """
    校验API_KEY和API_URL是否配置正确
    :return: 配置正确返回True，否则返回False并打印错误信息
    """
    if not API_KEY:
        print("错误：请在.env文件中配置HIT_AI_API_KEY（字节豆包火山方舟API密钥）")
        return False
    if not API_URL:
        print("错误：请在.env文件中配置HIT_AI_API_URL（字节豆包火山方舟调用地址）")
        print("提示：正确API_URL格式为 https://ark.cn-beijing.volces.com/api/v3/chat/completions")
        return False
    return True

def hit_llm_inference(prompt: str) -> str:
    """
    调用字节豆包（火山方舟）大模型进行推理（适配校园问答场景）
    :param prompt: 输入给模型的提示词（建议结合校园知识库内容构造）
    :return: 模型的回复文本，异常情况返回对应错误提示
    """
    # 先校验环境变量
    if not check_env_variables():
        return "大模型调用失败：环境变量配置错误，请检查.env文件"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # 新增火山方舟必填请求头，解决400/403调用失败问题
        "X-Volc-AccessKey": API_KEY.split("-")[0],
        "X-Volc-Region": "cn-beijing"
    }
    
    # 适配字节豆包（火山方舟）Doubao-Seed-2.0-mini模型，优化请求参数
    data = {
        "model": "Doubao-Seed-2.0-mini",  # 与你配置的模型完全一致
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False,
        "stop": [],  # 新增空stop参数，避免模型提前终止回复
        "request_id": f"hit_campusai_{os.urandom(8).hex()}"  # 新增请求ID，提升调用稳定性
    }
    
    try:
        # 发起POST请求，设置超时时间，避免卡顿
        response = requests.post(API_URL, headers=headers, json=data, timeout=15)  # 延长超时时间
        response.raise_for_status()  # 触发HTTP异常（如401、404等）
        response_json = response.json()
        
        # 解析字节豆包（火山方舟）返回格式，兼容不同返回场景
        if "choices" in response_json and len(response_json["choices"]) > 0:
            # 适配模型返回的不同格式，确保能提取到回复内容
            if "message" in response_json["choices"][0]:
                return response_json["choices"][0]["message"]["content"].strip()
            else:
                return response_json["choices"][0]["content"].strip()
        elif "response" in response_json:
            return response_json["response"].strip()
        else:
            return "抱歉，我暂时无法回答这个问题。"
    
    except requests.exceptions.Timeout:
        return "调用大模型失败：请求超时，请检查网络连接或平台可用性（可尝试重启网络）"
    except requests.exceptions.HTTPError as e:
        # 针对常见错误码给出具体提示，方便调试，同步适配当前模型
        error_code = response.status_code
        if error_code == 401:
            return f"调用大模型失败（错误码：{error_code}）：API密钥错误/过期/格式错误，请检查.env文件中的HIT_AI_API_KEY（当前密钥：{API_KEY[:8]}...）"
        elif error_code == 404:
            return f"调用大模型失败（错误码：{error_code}）：API_URL地址错误，请确认格式为https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        elif error_code == 403:
            return f"调用大模型失败（错误码：{error_code}）：无Doubao-Seed-2.0-mini模型调用权限，请登录火山方舟控制台开通权限，或检查API_KEY是否绑定正确账号"
        elif error_code == 400:
            return f"调用大模型失败（错误码：{error_code}）：请求参数异常，请检查代码中model名称是否为Doubao-Seed-2.0-mini，或prompt是否为空"
        else:
            return f"调用大模型失败（错误码：{error_code}）：{str(e)}，可尝试重启程序或检查火山方舟平台是否正常"
    except Exception as e:
        # 捕获其他未知异常，避免程序崩溃，给出具体排查方向
        error_info = str(e)
        if "Connection refused" in error_info:
            return f"调用大模型失败：网络连接被拒绝，请检查网络设置或API_URL是否可达"
        elif "JSON decode error" in error_info:
            return f"调用大模型失败：平台返回格式异常，可能是API_URL错误或平台临时故障，可稍后重试"
        else:
            return f"调用大模型失败：未知错误，错误信息：{error_info}，可检查.env配置或火山方舟平台状态"

# 测试代码（直接运行该文件即可测试接口连通性，贴合深圳校区场景）
if __name__ == "__main__":
    # 测试提示词（贴合深圳校区校园服务场景，联动知识库核心内容）
    test_prompt = "哈工大深圳校区食堂的开放时间是什么？"
    print(f"测试提示词：{test_prompt}")
    print("=" * 50)
    # 新增环境变量打印（仅测试用，可后续删除），方便排查配置问题
    print(f"当前API_KEY：{API_KEY[:8]}...（隐藏部分字符，保护隐私）")
    print(f"当前API_URL：{API_URL}")
    print("=" * 50)
    result = hit_llm_inference(test_prompt)
    print(f"模型回复：{result}")