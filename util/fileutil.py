#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# 文件工具类
@author: yansheng
@file: bilibili_spider.py
@time: 2023/01/01
"""

import os
import re
# import json
import datetime
import requests
from lxml import html

etree = html.etree


def dealwith_filename(path):
    """
    辅助函数：处理文件夹名
    :param path: 文件夹名
    :return: 文件夹名
    """
    # 去除首末的空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    """
    windows下文件名中不能含有：\\ / : * ? " < > | 英文的这些字符 ，这里使用"'"、"-"进行替换。
    :?| 用-替换
    "<> 用'替换
    """
    # 对于文件夹，有没有.好像都是同一个文件
    # replace方法默认替换所有匹配项
    path = path.replace(":", "-").replace("?", "-").replace("|", "-")
    path = path.replace("<", "'").replace(">", "'").replace("\"", "'")
    path = path.replace("/", "-").replace("\\", "-")

    # 匹配连续重复字符并替换为单个字符
    path = re.sub(r'(.)\1+', r'\1', path)

    return path


def mkdirs(path):
    """
    辅助函数：创建文件夹
    :param path: 文件夹名
    :return:
    """
    # path = dealwith_filename(path)

    # 判断路径是否存在，存在True，不存在False
    is_exists = os.path.exists(path)
    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录，这里使用创建多重目录的函数
        os.makedirs(path)
        print('文件夹\'' + path + '\'创建成功！')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print('文件夹\'' + path + '\'目录已存在！')
        return False


def move_file_by_updatetime(filepath, target_dirpath='', target_filename='', data_format='%Y-%m-%d'):
    """
    移动文件
    :param filepath:
    :param target_dirpath: 文件夹名
    :param target_filepath:
    :return:
    """
    if not os.path.exists(filepath):
        print('%s 文件不存在，直接返回。' % filepath)
        return

    if target_filename == '':
        # 1. 获取文件的最近修改时间戳
        modify_timestamp = os.path.getmtime(filepath)  # 返回自Epoch以来的秒数（浮点数）
        # print(modify_timestamp)

        # 2. 将时间戳转换为可读格式，并生成时间后缀（格式示例：20251022143045）
        dt_object = datetime.datetime.fromtimestamp(modify_timestamp)  # 转换为datetime对象
        time_suffix = dt_object.strftime(data_format)  # 格式化为字符串作为后缀 %Y%m%d%H%M%S
        # print(dt_object)
        # print(time_suffix)
        name_part, ext = os.path.splitext(filepath)
        target_filename = name_part + '-' + time_suffix + ext
        # print(target_filename)

    if not os.path.exists(target_dirpath):
        mkdirs(target_dirpath)
    target_filepath = target_dirpath + target_filename
    # print(target_filepath)

    # 如果目标文件存在，直接替换；否则重命名（否则，如果存在会报错：FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。）
    if os.path.exists(target_filepath):
        os.replace(filepath, target_filepath)
    else:
        os.rename(filepath, target_filepath)


def remove_empty_dirs(dirpath):
    """
    辅助函数：递归删除空的文件夹
    :param dirpath: 文件夹名
    :return:
    """
    if os.path.exists(dirpath):
        filelist = os.listdir(dirpath)
        # if filelist == []:
        if not filelist:
            # print('存在空文件夹:' + dirpath)
            # os.remove(dirpath)
            os.removedirs(dirpath)


def get_suffix_from_url(url):
    """
    辅助函数：从url中获取文件后缀，如果没找到，默认jpg
    :param url: 文件夹名
    :return:
    """
    if len(url.split('/')) == 1:
        suffix = 'jpg'
    else:
        if len((url.split('/')[-1]).split('.')) == 1:
            suffix = 'jpg'
        else:
            suffix = (url.split('/')[-1]).split('.')[-1]
    # print('结果：' + suffix)
    return suffix


def download_image_with_dir(img_url, dir_path, pathname, timeout_image=10):
    """
    下载图片
    :param img_url: 照片URL
    :param dir_path: 文件目录
    :param pathname: 文件名
    """
    # print('进入了函数：download_image_with_dir')
    # 定义保存到本地的图片名称，如：
    if '.gif' in img_url:
        image_path = '%s%s.gif' % (dir_path, pathname)
    else:
        image_path = '%s%s.jpg' % (dir_path, pathname)

    image_path = dealwith_filename(image_path)

    print("图片文件名：" + image_path)
    # 将判断放到前面，进行优化
    # 判断文件（图片）是否存在，如果存在就不重复下载，不存在就下载
    if os.path.exists(image_path):
        # print(' ' + image_path + ' 图片已存在！')
        return

    # 获取图片的网址，如果返回状态码为200，下载图片
    try:
        # img = requests.get(img_url, image_header, timeout=timeout_image)
        # requests默认是不会获取 301/302 的状态码的。可以设置allow_redirects = False，这样就可以获取所有的状态码了
        requests.packages.urllib3.disable_warnings()
        connect = requests.session()
        connect.keep_alive = False
        # img = connect.get(img_url, headers=spider_util.image_header, timeout=spider_util.timeout_image,
        #                   allow_redirects=False)
        img = connect.get(img_url, timeout=timeout_image, allow_redirects=False, verify=False)
        # print(img)
        # print(img.status_code)
    # except requests.exceptions.RequestException as e:
    except Exception as e:
        # print(e)
        '''
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        print(type(e)) # <class 'requests.exceptions.ConnectionError'>
        '''
        # ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
        if 'Connection aborted' in str(e):
            # print('Connection aborted')
            return
        # print('哎，请求图片失败了……')
        write_error_csv(img_url, image_path)
        return

    # 重定向301的照片大多有问题，不要了
    # if img.status_code == 200 or img.status_code == 301:
    if img.status_code == 200:
        # print('图片地址：' + img_url)
        # 以二进制形式写文件（下载图片）
        with open(image_path, 'wb') as f:
            f.write(img.content)  # 写入图片的二进制数据
            print(' ' + image_path + ' 下载成功！')
    else:
        print('哎，请求图片失败了，状态码为：%s，图片地址为：%s' % (str(img.status_code), img_url))


def download_image(img_url, image_path, image_header={}, timeout_image=10):
    """
    下载图片
    :param img_url: 照片URL
    :param image_path: ./目录/文件名(xx.jpg)
    """

    # 创建目录
    # print(os.path.dirname(image_path))
    # print(os.path.basename(image_path))
    mkdirs(os.path.dirname(image_path))

    # print("图片文件名：" + image_path)
    # 将判断放到前面，进行优化
    # 判断文件（图片）是否存在，如果存在就不重复下载，不存在就下载
    if os.path.exists(image_path):
        print(' ' + image_path + ' 图片已存在！')
        return

    # 获取图片的网址，如果返回状态码为200，下载图片
    try:
        # img = requests.get(img_url, image_header, timeout=timeout_image)
        requests.packages.urllib3.disable_warnings()
        img = requests.get(img_url, headers=image_header, timeout=timeout_image, allow_redirects=False, verify=False)
    # except requests.exceptions.RequestException as e:
    except Exception as e:
        print('哎，请求图片失败了……')
        write_error_csv('', img_url, image_path)
        return

    if img.status_code == 200:
        # print('图片地址：' + img_url)
        try:
            # 以二进制形式写文件（下载图片）
            with open(image_path, 'wb') as f:
                f.write(img.content)  # 写入图片的二进制数据
                print(' ' + image_path + ' 图片下载成功！')
        except Exception as e:
            print('下载图片时，发生异常！')
            print(e)
            write_error_csv('', img_url, image_path)


def write_error_csv(img_url, image_path, filename=''):
    """
    当发生异常时，将图片信息保存到本地
    :param filename: 文件名
    :param img_url: 图片URL
    :param image_path: 保存照片的本地路径
    :return: None
    """
    import csv
    import time

    # 时间格式化："%Y-%m-%d %H:%M:%S" --> '2016-03-20 11:45:39'
    time_hour = time.strftime("%Y-%m-%d-%H", time.localtime())
    mkdirs('./log')
    if filename is None or filename == '':
        filename = './log/error_info-' + time_hour + '.csv'

    try:
        with open(filename, 'a', encoding='UTF8', newline='') as f:
            # 创建初始化写入对象
            writer = csv.writer(f)
            # 一行一行写入 ['color','red']
            writer.writerow([img_url, image_path])
    except Exception as e:
        print(e)


def write_arr_to_csv(arr, filename):
    """
    将对象数组写到csv文件中，格式为：url,文件名.jpg
    :param arr: 对象数组
    :param filename: 文件名 12
    :return: None
    """

    print('进入 write_arr_csv 函数了...')

    if arr is None:
        print('arr为空，请检查参数！')
        return

    longtext = ''

    for obj in arr:
        # print(obj)
        img_url = obj.url
        img_suffix = '.jpg'
        if '.gif' in img_url:
            img_suffix = '.gif'
        elif '.png' in img_url:
            image_path = '.png'

        dir_perfix = ''
        if obj.date != '':
            dir_perfix = obj.date + '-'

        # 因为csv中逗号是分隔符，需要替换一下，避免不必要的麻烦
        title = obj.title.replace(',', '-')
        title = dealwith_filename(title)
        longtext += ('./images/' + filename + '/' + dir_perfix + title + '/' + title + '-' + str(
            obj.count) + img_suffix) + ',' + obj.url + '\n'
    # print(longtext)

    try:
        with open('backup-' + filename + '.csv', 'a', encoding='UTF8', newline='\n') as f:
            # 创建初始化写入对象
            f.write(longtext)
    except Exception as e:
        print(e)


def write_arr_to_json(arr, filename):
    """
    将数据写到JSON文件
    :param arr: 数据
    :param filename:文件名
    :return:
    """
    import json

    if arr is None:
        print('arr 不能为空')
        return
    if filename is None:
        print('filename 不能为空')
        return
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(arr, file, ensure_ascii=False, indent=4)


def read_arr_from_csv(filename):
    """
    从csv文件中读取对象数组
    :param filename: 文件名 12
    :return: None
    """

    print('进入 read_arr_from_csv 函数了...')

    import csv
    # csv_reader = csv.reader(open("omjq.csv", encoding="utf-8"))
    csv_reader = csv.reader(open(filename + ".csv", encoding="utf-8"))

    # print(csv_reader)
    #  注意这里的 csv_reader 是文件对象，迭代器，不是常规数组类型对象   AttributeError: '_csv.reader' object has no attribute 'length'
    # print('获取对象数量：'+str(len(csv_reader)))

    arr = []
    for obj in csv_reader:
        # print(obj)
        arr.append(obj)
        # break # 测试用

    # 排序
    # 按照第二个字段排序，逆序
    arr = sorted(arr, key=lambda x: x[1], reverse=True)
    # arr = sorted(arr, key=lambda x: x[1], reverse=False)

    print('获取对象数量：' + str(len(arr)))
    return arr


def is_file_content_equal(filename, md_content):
    """
    判断文件内容是否一致，一致返回True，否则false
    :param filename: 文件名
    :param content: 文件内容
    :return: bool
    """
    # print('filename:' + filename)
    # print('md_content:'+md_content)
    # 如果文件不存在，直接返回false
    if not os.path.exists(filename):
        return False
    else:
        with open(filename, "r", encoding="utf-8") as f_md:
            content = f_md.read()
            # print('-----------\n' + content + '-----------')
        if md_content == content:
            return True
        else:
            return False


def list_remove_attributes(data_list, remove_keys):
    """高效移除字典列表中指定键

    Args:
        data_list: 字典列表
        remove_keys: 要移除的键列表

    Returns:
        处理后的新列表（不修改原数据）
    """
    return [{k: v for k, v in d.items() if k not in remove_keys}
            for d in data_list]


def list_retain_attributes(data_list, retain_keys):
    """高效保留字典列表中指定键

    Args:
        data_list: 字典列表
        retain_keys: 要保留的键列表

    Returns:
        处理后的新列表（不修改原数据）
    """
    return [{k: d[k] for k in retain_keys if k in d}
            for d in data_list]


def process_bilibili_data(data, sort_attributes, top_n=10):
    """
    读取data数组数据，按指定属性排序并返回前N项

    参数:
        data: data数组数据
        sort_attributes: 排序属性列表，如['stat.coin', 'stat.dm']
        top_n: 返回结果数量，默认为10

    返回:
        排序后的前N项数据列表
    """
    try:

        # 验证数据格式
        # if not isinstance(data, list) or not all('stat' in item for item in data):
        #     raise ValueError("JSON数据格式不符合要求")

        # 按多个属性排序（降序）
        for attr in reversed(sort_attributes):
            # 处理嵌套属性（如'stat.coin'）
            keys = attr.split('.')
            data.sort(
                key=lambda x: get_nested_value(x, keys),
                reverse=True
            )

        # 返回前N项
        if top_n == 0:
            return data
        return data[:top_n]

    except Exception as e:
        print(f"处理数据时出错: {e}")
        return []


def get_nested_value(obj, keys):
    """获取嵌套字典中的值"""
    for key in keys:
        obj = obj.get(key, {})
    return obj if isinstance(obj, (int, float)) else 0
