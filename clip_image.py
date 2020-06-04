# -*- coding: utf-8 -*-

__AUTHOR__ = "Master_lxj"
__WEBSITE__ = "http://www.dagouzi.cn"
__DOC__ = "To do something"

import os
import requests
import base64
import cv2 as cv
import numpy as np


def make_pure_img(width, height, color):
	img = np.zeros((width, height, 3), dtype=np.uint8)
	img[:, :, 0] = color[0]
	img[:, :, 1] = color[1]
	img[:, :, 2] = color[2]

	return img


def load_images(images_path):
	all_images = []
	image_type = [".PNG", ".JPG", ".JPEG", ".BMP", ".png", ".jpg", ".jpeg", ".bmp"]
	images = os.listdir(images_path)
	for image in images:
		if os.path.splitext(image)[-1] in image_type:
			all_images.append(os.path.join(images_path, image))

	return all_images


def get_token():
	import requests

	# client_id 为官网获取的AK， client_secret 为官网获取的SK
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=lK6HPRDHuU9guKCe6MeMvfdV&client_secret=eenu8wkdRiyL7CvXHgwvxtY5RoVCkGOk'
	response = requests.get(host)
	if response:
		return response.json().get("access_token")


def request_ai(image):
	access_token = get_token()
	request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"
	with open(image, "rb") as f:
		img = base64.b64encode(f.read())
		params = {"image": img, "with_face": 1}
		request_url = request_url + "?access_token=" + access_token
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		response = requests.post(request_url, data=params, headers=headers)
		if response:
			result = response.json()
			rect = result.get("result", None)
			if rect:
				return True, rect
			else:
				error_msg = result.get("error_msg", None)
				return False, error_msg

	return False, "未知错误"


def clip(old_image, new_image, left, top, width, height):

	img = old_image
	x1 = left
	x2 = left + width
	y1 = top
	y2 = top + height
	img2 = img[y1:y2, x1:x2]
	cv.imencode(os.path.splitext(new_image)[-1], img2)[1].tofile(new_image)

	return True, new_image


def rect(rect_left, rect_top, rect_width, rect_height, image, width, height):
	"""
	image: 原图
	"""
	image_height, image_width, _ = image.shape
	right = image_width - rect_left - rect_width
	bottom = image_height - rect_top - rect_height
	min_width = min(rect_left, right)
	min_height = min(rect_top, bottom)

	if min_width == 0 or min_height == 0:
		return rect_left, rect_top, rect_width, rect_height

	if min_height <= min_width:
		width_g = gcd(min_height, height)
		width_d = min_height * height / width_g
		width_dx = (width * (width_d / height)) / (width_d / min_height)
		left = rect_left - width_dx
		top = rect_top - min_height
		width = rect_width + width_dx * 2
		height = rect_height + min_height * 2
	else:
		height_g = gcd(min_width, width)
		height_d = min_width * width / height_g
		height_dx = (height * (height_d / width)) / (height_d / min_width)
		left = rect_left - min_width
		top = rect_top - height_dx
		width = rect_width + min_width * 2
		height = rect_height + height_dx * 2

	return int(left), int(top), int(width), int(height)


def clip_plus(old_image, new_image, rect_left, rect_top, rect_width, rect_height, width, height, tag, color):
	rect_left = int(rect_left)
	rect_top = int(rect_top)
	rect_width = int(rect_width)
	rect_height = int(rect_height)
	rect_left, rect_top, rect_width, rect_height = rect(
		rect_left, rect_top, rect_width, rect_height, old_image, width, height
	)
	bg_image = make_pure_img(height, width, color)  # 创建背景
	img = old_image[rect_top:rect_top + rect_height, rect_left:rect_left + rect_width]  # 裁剪原图图片
	d = height / rect_height if tag else width / rect_width  # 比例
	img = cv.resize(img, (0, 0), fx=d, fy=d)  # 缩放
	# 防止缩放后超出
	w, h, _ = img.shape
	if w > width:
		w = width
	if h > height:
		h = height
	# 生成新的图像
	img = img[0:height, 0:width]
	rows, cols, channels = img.shape
	roi = bg_image[0:rows, 0:cols]
	img2gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	ret, mask = cv.threshold(img2gray, 255, 255, cv.THRESH_BINARY)
	mask_inv = cv.bitwise_not(mask)
	bg = cv.bitwise_and(roi, roi, mask=mask)
	img2_fg = cv.bitwise_and(img, img, mask=mask_inv)
	dst = cv.add(bg, img2_fg)
	width_center = (width - cols) // 2
	height_center = (height - rows) // 2
	bg_image[height_center:rows + height_center, width_center:cols + width_center] = dst
	# if tag:
	# 	print(width, cols)
	# 	center = (width - cols) // 2
	# 	bg_image[0:rows, center:cols+center] = dst	# 覆盖图像
	# else:
	# 	print("补高")
	# 	center = (height - rows) // 2
	# 	bg_image[center:rows+center, 0:cols] = dst	# 覆盖图像
	# 保存
	cv.imencode(os.path.splitext(new_image)[-1], bg_image)[1].tofile(new_image)

	return True, new_image


def gcd(n1, n2):
	_max, _min = (n1, n2) if n1 >= n2 else (n2, n1)
	d = _max % _min
	if d == 0:
		return _min
	else:
		return gcd(_min, d)


def parse_rect(total, sid, rect):
	"""
	解析主体图像rect方位
	"""
	rest = total - sid - rect
	if rest >= sid:
		# 靠左
		return True, rest
	else:
		# 靠右
		return False, rest


def cut(image, save_path, rect, color, width=None, height=None):

	# 生成新的图片路径
	new_image_file = os.path.join(save_path, os.path.split(image)[-1])
	# 提取图像主体rect
	ai_left = rect.get("left", None)
	ai_top = rect.get("top", None)
	ai_width = rect.get("width", None)
	ai_height = rect.get("height", None)

	img = cv.imdecode(np.fromfile(image, dtype=np.uint8), -1)
	img_height, img_width, _ = img.shape

	# 指定尺寸
	if width and height:
		width = int(width)
		height = int(height)
		# 宽高比
		if (width / height) >= (ai_width / ai_height):
			# 补宽
			tag = True
			height_g = gcd(height, ai_height)  # 高度最大公约数
			height_d = (height * ai_height) / height_g  # 高度最小公倍数
			# 宽度差值
			width_dx = (width * (height_d / height) - ai_width * (height_d / ai_height)) // (height_d / ai_height)
			is_left, right = parse_rect(img_width, ai_left, ai_width)
			# 主体靠左
			if is_left:
				# 左边够补
				if ai_left >= width_dx / 2:
					ai_left -= width_dx / 2
					ai_width += width_dx
				else:
					ai_width += ai_left * 2
					ai_left = 0
			# 主体靠右
			else:
				# 右边够补
				if right >= width_dx / 2:
					ai_left -= width_dx / 2
					ai_width += width_dx
				else:
					ai_left -= right
					ai_width += right * 2
		else:
			# 补高
			tag = False
			width_g = gcd(width, ai_width)  # 宽度最大公约数
			width_d = (width * ai_width) / width_g  # 宽度最小公倍数
			# 高度差值
			height_dx = (height * (width_d / width) - ai_height * (width_d / ai_width)) // (width_d / ai_width)
			is_top, bottom = parse_rect(img_height, ai_top, ai_height)
			# 主体靠上
			if is_top:
				# 上边够补
				if ai_top >= height_dx / 2:
					ai_top -= height_dx / 2
					ai_height += height_dx
				else:
					ai_height += ai_top * 2
					ai_top = 0
			# 主体靠下
			else:
				# 下边够补
				if bottom >= height_dx / 2:
					ai_top -= height_dx / 2
					ai_height += height_dx
				else:
					ai_top -= bottom
					ai_height += bottom * 2
		return clip_plus(img, new_image_file, ai_left, ai_top, ai_width, ai_height, width, height, tag, color)
	else:
		return clip(img, new_image_file, ai_left, ai_top, ai_width, ai_height)
