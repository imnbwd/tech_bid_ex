import requests
from typing import Optional, Tuple


class HttpUtils:
    """
    Http请求相关方法
    """

    @staticmethod
    def get_json_from_url(url) -> Tuple[Optional[str], Optional[str]]:
        """
        获取指定URL的内容
        :return: JSON内容，错误消息；如获取成功，JSON内容不空，错误消息为空，反之则相反
        """
        try:
            # 发送GET请求到指定的URL
            response = requests.get(url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 将JSON内容解析为Python对象
                json_data = response.content.decode(encoding="utf-8")
                return json_data, None
            else:
                return None, f"请求失败。状态码: {response.status_code}"
        except requests.RequestException as e:
            return None, f"请求出错: {str(e)}"
