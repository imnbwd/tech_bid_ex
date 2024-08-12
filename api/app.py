from flask import Flask, request, jsonify, Response
from model import Result
from loguru import logger
from services import InfoExtractionService, TechStandardIdentifyService,InvalidContentIdentifyService
from concurrent.futures import ThreadPoolExecutor
from app_const import ServiceType

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=20)  # 创建一个线程池，设置最大线程数


# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )


@app.route('/health', methods=['GET'])
def health() -> Response:
    return jsonify("OK")


@app.route('/service', methods=['POST'])
def service() -> Response:
    """
    技术标智能相关服务
    :return: 响应结果
    """
    # 检查服务ID
    service_id: str = request.args.get('id')
    if service_id is None or service_id == "":
        return jsonify(Result(100, "缺少ServiceId").to_dict())
    if request.content_type != "application/json":
        return jsonify(Result(100, "缺少请求内容").to_dict())

    # 检查正文中的关键信息
    url = request.json.get("url")
    notify_url = request.json.get("notify_url")
    task_id = request.json.get("task_id")
    if not notify_url or not task_id or not url:
        return jsonify(Result(-1, "缺少notify_url、task_id或url").to_dict())

    service_type: ServiceType = ServiceType.get_service_by_value(int(service_id))
    if service_type == ServiceType.INFO_EXTRACTED:
        # 提取服务
        return handle_service_info_extracted(url, notify_url, task_id)

    elif service_type == ServiceType.INVALID_CONTENT_IDENTIFY:
        # 无效内容检测
        return handle_service_invalid_content_identify(url, notify_url, task_id)

    else:
        return jsonify(Result(101, "ServiceId不正确").to_dict())


@app.errorhandler(Exception)
def handle_global_exception(e) -> Response:
    """
    全局异常处理
    :param e:
    :return:
    """
    logger.exception(e)
    return jsonify(Result(-1, "请求出错").to_dict())


def handle_service_info_extracted(url: str, notify_url: str, task_id: str) -> Response:
    """
    请求信息提取服务
    :param url:
    :param notify_url:
    :param task_id:
    :return:
    """
    schema = request.json.get("options")

    check_result = None
    if not schema:
        check_result = Result(-1, "缺少要提取的信息options或url")

    # 判断要提取的内容
    is_valid_schema = isinstance(schema, list) and len(list(schema)) > 0
    if not is_valid_schema:
        check_result = Result(-1, "未指定要提取的项目")

    if check_result is not None:
        # 检查没通过
        return jsonify(check_result.to_dict())

    # 通过线程进行提取
    info_extract_service = InfoExtractionService()
    executor.submit(info_extract_service.process, schema, url, notify_url, task_id)
    return jsonify(Result.default_success("请求成功").to_dict())


def handle_service_invalid_content_identify(url: str, notify_url: str, task_id: str) -> Response:
    """
    无效内容识别服务
    :param url:
    :param notify_url:
    :param task_id:
    :return:
    """
    check_result = None

    check_option = request.json.get("options")
    if not check_option:
        check_result = Result(-1, "缺少要识别的信息")

    if check_result is not None:
        # 检查没通过
        return jsonify(check_result.to_dict())

    invalid_content_identify = InvalidContentIdentifyService()
    invalid_content_identify.process(url, notify_url, task_id,check_option)
    # executor.submit(tech_standard_identify.process, url, notify_url, task_id)
    return jsonify(Result.default_success("请求成功").to_dict())


# 运行 Flask 应用
if __name__ == '__main__':
    # 设置日志文件每天切割，文件名中包含日期
    logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="1 day", format="{time} {level} {message}")
    app.run(debug=True)
