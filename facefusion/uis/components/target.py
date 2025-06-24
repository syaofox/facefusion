import os
import time
from typing import Optional, Tuple

import gradio

from facefusion import state_manager, wording
from facefusion.face_store import clear_reference_faces, clear_static_faces
from facefusion.filesystem import is_image, is_video
from facefusion.uis.core import register_ui_component
from facefusion.uis.types import ComponentOptions, File

TARGET_FILE : Optional[gradio.File] = None
TARGET_IMAGE : Optional[gradio.Image] = None
TARGET_VIDEO : Optional[gradio.Video] = None


def render() -> None:
	global TARGET_FILE
	global TARGET_IMAGE
	global TARGET_VIDEO

	is_target_image = is_image(state_manager.get_item('target_path'))
	is_target_video = is_video(state_manager.get_item('target_path'))
	TARGET_FILE = gradio.File(
		label = wording.get('uis.target_file'),
		value = state_manager.get_item('target_path') if is_target_image or is_target_video else None
	)
	target_image_options : ComponentOptions =\
	{
		'show_label': False,
		'visible': False
	}
	target_video_options : ComponentOptions =\
	{
		'show_label': False,
		'visible': False
	}
	if is_target_image:
		target_image_options['value'] = TARGET_FILE.value.get('path')
		target_image_options['visible'] = True
	if is_target_video:
		target_video_options['value'] = TARGET_FILE.value.get('path')
		target_video_options['visible'] = True
	TARGET_IMAGE = gradio.Image(**target_image_options)
	TARGET_VIDEO = gradio.Video(**target_video_options)
	register_ui_component('target_image', TARGET_IMAGE)
	register_ui_component('target_video', TARGET_VIDEO)


def listen() -> None:
	TARGET_FILE.change(update, inputs = TARGET_FILE, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])


def update(file : File) -> Tuple[gradio.Image, gradio.Video]:
	clear_reference_faces()
	clear_static_faces()

	if file:
		# 确保文件路径存在
		# --- 关键改进点：添加延迟和文件稳定性检查 ---
		# 延迟是为了给操作系统和杀毒软件时间释放文件锁
		time.sleep(1) # 尝试 1 秒的延迟，如果仍然有问题可以增加到 2-3 秒

		# 检查文件大小是否稳定，防止在文件写入未完成时读取
		initial_size = -1
		for _ in range(5): # 尝试等待最多 5 * 0.5 = 2.5 秒
			current_size = os.path.getsize(file.name)
			if current_size == initial_size and current_size > 0:
				print(f"文件 {file.name} 大小稳定：{current_size} 字节。")
				break
			initial_size = current_size
			time.sleep(0.5)
		else: # 循环结束后如果文件大小仍不稳定
			print(f"警告: 文件 {file.name} 大小在等待后仍不稳定或为0。当前大小: {current_size}")
			if current_size == 0:
				state_manager.clear_item('target_path')
				return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)
		# --- 结束改进点 ---

		if file and is_image(file.name):
			state_manager.set_item('target_path', file.name)
			return gradio.Image(value = file.name, visible = True), gradio.Video(value = None, visible = False)

		if file and is_video(file.name):
			state_manager.set_item('target_path', file.name)
			return gradio.Image(value = None, visible = False), gradio.Video(value = file.name, visible = True)

	state_manager.clear_item('target_path')
	return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)
