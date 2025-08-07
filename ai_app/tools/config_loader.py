# -*- coding: utf-8 -*-
"""
Created on 2025/8/7 13:23

@Project -> File: PythonProject -> config_loader.py

@Author: ouzhihui

@Describe: 
"""
import os
import sys
import logging
import logging.config

import lake.decorator
import lake.dir

from ai_app.tools.dir_file_op import load_yaml, check_mkdirs

if len(logging.getLogger().handlers) == 0:
	logging.basicConfig(level=logging.DEBUG)

logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

_color_map = {
	'blue': '#1f77b4',  # 蓝色
	'orange': '#ff7f0e',  # 黄橙色
	'green': '#2ca02c',  # 绿色
	'red': '#d62728',  # 红色
	'purple': '#9467bd',  # 紫色
	'cyan': '#17becf',  # 青色
	'grey': '#7f7f7f',  # 灰色
	'black': 'k'  # 黑色
}


@lake.decorator.singleton
class ConfigLoader(object):
	"""项目配置装载器"""

	def __init__(self):
		self._get_proj_root_dir()
		self._config_path = os.path.join(self.proj_dir, 'config/')
		self._set_proj_cmap()
		self._load_model_config()
		self._load_environ_config()

	# self._load_test_params()

	def _get_proj_root_dir(self):
		"""获取项目根目录"""
		self._proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

	@property
	def proj_dir(self):
		return self._proj_dir

	def _set_proj_cmap(self):
		"""设置项目颜色方案"""
		self._proj_cmap = _color_map

	@property
	def proj_cmap(self):
		return self._proj_cmap

	def _load_model_config(self):
		"""载入模型参数配置文件"""
		self._model_config_path = os.path.join(self._config_path, 'project_config.yml')
		self._model_config = load_yaml(self._model_config_path)

	@property
	def proj_config(self):
		return self._model_config

	def _load_environ_config(self):
		"""载入环境变量配置"""
		# 读取本地文件中的环境变量设置.
		# 如果本地config中有master.yml则优先使用, 否则使用default.yml, 否则为空字典.
		_environ_config_path_ = None
		for _file_name in ['master.yml', 'default.yml']:
			if _file_name in os.listdir(self._config_path):
				# print('Use environmental variables in {}'.format(_file_name))
				_environ_config_path_ = os.path.join(self._config_path, _file_name)
				break

		if _environ_config_path_ is None:
			self._local_environ_config = {}
		else:
			self._local_environ_config = load_yaml(_environ_config_path_)

		# 线上环境变量注入.
		# 如果存在可注入环境变量, 则采用注入值, 否则采用环境变量配置文件中的值.
		self._environ_config = self._local_environ_config
		for key in self._local_environ_config.keys():
			if key in os.environ.keys():
				self._environ_config.update({key: os.environ[key]})

	@property
	def environ_config(self):
		return self._environ_config

	def _load_test_params(self):
		_test_params_path = os.path.join(self._config_path, 'test_params.yml')
		self._test_params = load_yaml(_test_params_path)

	@property
	def test_params(self):
		return self._test_params

	def set_logging(self):
		"""日志配置"""

		# 配置日志.
		try:
			_log_config = self._model_config['logging']
			path = os.path.join(self.proj_dir, _log_config['handlers']['info_handler']['filename'])
			direc = os.path.dirname(path)
			check_mkdirs(direc)
			_log_config['handlers']['info_handler']['filename'] = path
			path = os.path.join(self.proj_dir, _log_config['handlers']['error_handler']['filename'])
			direc = os.path.dirname(path)
			check_mkdirs(direc)
			_log_config['handlers']['error_handler']['filename'] = path

		except Exception as e:
			raise RuntimeError('Cannot load logging params in model_config.yml, {}'.format(e))

		logging.config.dictConfig(_log_config)


config_loader = ConfigLoader()
