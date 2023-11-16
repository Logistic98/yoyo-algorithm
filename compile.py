# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from setuptools import setup, Extension
from Cython.Build import cythonize

# 指定你的源文件目录
source_dir = './fast-text-rank'
output_dir = source_dir + '_build'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 创建临时目录
with tempfile.TemporaryDirectory() as temp_dir:
    temp_source_dir = os.path.join(temp_dir, 'src')

    # 递归复制文件夹并保留目录结构
    shutil.copytree(source_dir, temp_source_dir, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))

    # 找到所有的 .py 文件并创建一个扩展对象列表
    extensions = []
    for root, dirs, files in os.walk(temp_source_dir):
        for filename in files:
            if filename.endswith('.py'):
                abs_file_path = os.path.join(root, filename)
                relative_file_path = os.path.relpath(abs_file_path, temp_source_dir)
                module_name = os.path.splitext(relative_file_path.replace(os.path.sep, '.'))[0]
                pyx_file_path = abs_file_path + 'x'  # Append 'x' to make .pyx extension
                os.rename(abs_file_path, pyx_file_path)
                extensions.append(Extension(module_name, [pyx_file_path]))

    # 编写 setup.py 文件内容并构建
    setup(
        name='My Package',
        ext_modules=cythonize(extensions),
        script_args=["build_ext", "--build-lib", output_dir]
    )

    # 复制临时目录中编译生成的文件到输出目录
    for root, dirs, files in os.walk(temp_dir):
        for filename in files:
            if filename.endswith('.so') or filename.endswith('.pyd'):
                # 相对于临时源目录的路径
                relative_path = os.path.relpath(root, temp_source_dir)
                # 构建目标目录
                dest_dir = os.path.join(output_dir, relative_path)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(os.path.join(root, filename), dest_dir)

# 拷贝源目录下的非 .py 文件到输出目录，并保留目录结构
for root, dirs, files in os.walk(source_dir):
    for item in dirs + files:
        src_path = os.path.join(root, item)
        dst_path = src_path.replace(source_dir, output_dir, 1)
        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
        elif not item.endswith('.py') and not item.endswith('.pyc') and not os.path.exists(dst_path):
            shutil.copy2(src_path, dst_path)
