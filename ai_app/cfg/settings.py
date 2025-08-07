# -*- coding: utf-8 -*-
"""
Created on 2025/8/7 15:03

@Project -> File: Chat_Assistant -> settings.py

@Author: ouzhihui

@Describe: 
"""
import asyncio
import logging
import sys

import yaml

sys.path.append('../')

from ai_app.tools.config_loader import config_loader


class Settings:
    def __init__(self):
        self.proj_dir, self.proj_cmap = config_loader.proj_dir, config_loader.proj_cmap
        self.environ_config = config_loader.environ_config
        self.proj_conf = config_loader.proj_config
        self.semaphore = asyncio.Semaphore(10)

    def get_base_url(self):
        return self.proj_conf['base_url']

    def get_api_key(self):
        return self.proj_conf['api_key']

    def get_model(self):
        return self.proj_conf['model']

    def get_semaphore(self):
        return self.semaphore

settings = Settings()

base_url = settings.get_base_url()
api_key = settings.get_api_key()
model = settings.get_model()
semaphore = settings.get_semaphore()