# -*- coding: utf-8 -*-
"""
Created on 2025/8/7 13:24

@Project -> File: PythonProject -> dir_file_op.py

@Author: ouzhihui

@Describe: 
"""
import os
import yaml
import json
import numpy as np


def search_files_in_current_dir(dir_path: str, target_names: list = None) -> list:
    """
    从当前目录dir_path中搜索含有目标名字的文件, 返回名字列表
    :param dir_path: 目录名
    :param target_names: 包含的目标文件名列表
    """
    all_files_names = [p for p in os.listdir(dir_path)]
    if target_names is None:
        return []
    else:
        target_files = []
        for name in target_names:
            target_files += [p for p in all_files_names if name in p]
        target_files = list(set(target_files))
        return target_files


def erase_files(dir_path: str, names2erase: list = None, names2keep: list = None):
    """
    Delete files hitting target names in the dir path
    :param dir_path: str, target directory
    :param names2erase: list or None, file names to erase
    :param names2keep: list or None, file names to keep, keep first if the name arises in both erasing and keeping lists
    """
    if (names2erase is None) & (names2keep is None):
        all_files_names = [p for p in os.listdir(dir_path)]
        final_files2erase = all_files_names  # delete all files in the directory
    else:
        files2erase = search_files_in_current_dir(dir_path, names2erase)
        files2keep = search_files_in_current_dir(dir_path, names2keep)
        final_files2erase = list(set([p for p in files2erase if p not in files2keep]))

    for name in final_files2erase:
        os.remove(os.path.join(dir_path, name))


def mk_file(file_dir: str, file_name: str):
    if file_name not in os.listdir(file_dir):
        with open(os.path.join(file_dir, file_name), 'w') as f:
            f.write('')


def check_mkdirs(_dir):
    if not os.path.exists(_dir):
        os.makedirs(_dir)


def load_yaml(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        file = yaml.load(f, Loader=yaml.Loader)  # yaml.FullLoader
    return file


def load_json_file(fp: str) -> dict:
    """
    加载json文件
    :param fp: 文件路径
    :return:
    """
    try:
        with open(fp, 'r') as f:
            results = json.load(f)
    except Exception:
        raise ValueError(f'读取文件{fp}出错')
    return results


def save_json_file(obj: dict, fp: str):
    """
    保存json文件
    :param obj: 文件 dict
    :param fp: 保存路径
    :return:
    """
    with open(fp, 'w') as f:
        json.dump(obj, f, indent=4, cls=MyEncoder)


def check_file(fp):
    if os.path.isfile(fp):
        return True
    else:
        return False


def getEachFilePath(folder, base_path=''):
    """
    获取文件夹下的所有文件路径
    e.g.
        folder : 'folder1'
        base_path : '/home/Sam'
        return : ['/home/Sam/folder1/file1.csv', '/home/Sam/folder1/file2.csv']

    :param folder: str, 需要读取每个文件路径的父文件夹名
    :param base_path: str, 父文件夹名的基路径
    :return:
    """
    folder_path = os.path.join(base_path, folder)
    if not os.path.exists(folder_path):
        raise NotADirectoryError(folder_path)
    files = os.listdir(folder_path)
    files = [os.path.join(folder_path, file) for file in files]
    return files


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)