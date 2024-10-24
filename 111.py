import asyncio
import base64
import sys
import time
import traceback

from cdp_socket.exceptions import CDPError
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import random
import json
from gologin import GoLogin
from gologin import getRandomPort
import os
from dotenv import load_dotenv
import json
import requests
import http.cookies
import whisper
import re
import aiohttp
import tempfile
from selenium_driverless.webdriver import Chrome, Target
from selenium_driverless.types.webelement import NoSuchElementException
import typing

async def download_audio(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    # 从响应中读取音频数据并写入临时文件
                    audio_data = await response.read()
                    tmp_file.write(audio_data)
                    # 获取临时文件的路径
                    tmp_file_path = tmp_file.name
                print("Audio file downloaded successfully.")
                return tmp_file_path
            else:
                print(f"Failed to download audio file: {response.status}")
                return None
            
asyncio.run(download_audio("https://www.google.com/recaptcha/api2/payload?p=06AFcWeA4ZqHIVI2XMFVp0_mUWHOQYYqRKW3fM_rCfyqqM4OBqby5BaZ4tc2FnwFZrXiJZLI6YWHoxVL3GvD5znDAQXZICSFlqPgn6cPCs8kiqS4K4OWTijgBtMf7J4eFrWLI5V-OVifS5CZkdXrY2uANWEZLgzuhwfFCy3GhKsJawG1CmcPapzQoOA9hE2GIhfXVd3Z2ng0EKB9rhLKSS7b7c7mOB2VhQAg&k=6LeU-80ZAAAAAFBnVut-1yPEUMRurAOfr_b-rMwo"))