from PublishPosition.utils.check_html_keywords import dont_contain_html_keywords

def check_publish_position_form(data_dict):
    """
    :param data_dict: 数据参数， 目前检查以下字段：'position_name', 'salary', 'summary', 'detail', 'district', 'published_state'
    :return:
        data_dict: 清洗数据后的数据字典
        error_dict: 存在问题的字段以及对应的问题反馈
        valid: 检验是否通过，False 非通过， True 通过
    """
    check_passed_flag = True
    error_dict = {}
    # check position name
    if not (0 < len(data_dict['position_name']) < 32):
        error_dict['position_name'] = '职位名称需要在1至32字符之间'
        check_passed_flag = False
    # check salary
    try:
        data_dict['salary'] = int(data_dict['salary'])
        if data_dict['salary'] < 0:
            error_dict['salary'] = "薪水不得少于零"
            check_passed_flag = False
    except ValueError as e:
        error_dict['salary'] = '薪水需要是整数'
        check_passed_flag = False
    # check summary
    if not (0 < len(data_dict['summary']) < 100):
        error_dict['summary'] = "摘要需要在1至100字符以内"
        check_passed_flag = False
    # check detail
    # length check
    if not (0 < len(data_dict['detail']) < 3000):
        error_dict['detail'] = '详细介绍最多不超过3000字符'
        check_passed_flag = False
    # special security check
    if not dont_contain_html_keywords(data_dict['detail']):
        error_dict['detail'] = '包含非法的字符'
        check_passed_flag = False
    # check district
    try:
        data_dict['district'] = int(data_dict['district'])
        if not (0 <= data_dict['district'] <= 953):
            error_dict['district'] = "非法的省份代号"
            check_passed_flag = False
    except ValueError as e:
        error_dict['district'] = "非法的省份代号"
        check_passed_flag = False
    # 字段检查结束
    return data_dict, error_dict, check_passed_flag
