import jsonlines
import shutil
import os
from datetime import date
from PIL import Image
import datetime

def desktop_path():
    """
    :return: 返回桌面路径
    """
    return os.path.join(os.path.expanduser('~'),"Desktop")


def get_date():
    """
    :return:返回当下时间
    """
    return date.today()

def save_2_path(out_dir, Category_zh, Class_zh):
    """
    将use_sd_get_patterns.py保存出来的图片进行转存
    :param out_dir: 输出文件夹
    :param Category_zh: 大类中文名
    :param Class_zh: 小类中文名
    :return: 小类路径
    """
    os.makedirs(out_dir, exist_ok=True)
    date = get_date()
    date_path = os.path.join(out_dir, str(date).replace('-',''))
    os.makedirs(date_path, exist_ok=True)
    Category_zh_path = os.path.join(date_path, Category_zh)
    os.makedirs(Category_zh_path, exist_ok=True)
    Class_zh_path = os.path.join(Category_zh_path, Class_zh)
    os.makedirs(Class_zh_path, exist_ok=True)
    return Class_zh_path

def transfer(infile, outfile):
    """
    图片格式的转化
    :param infile: 输入文件
    :param outfile: 输出文件
    :return:
    """
    im = Image.open(infile)
    im.save(outfile,dpi=(150.0,150.0)) ##500.0,500.0分别为想要设定的dpi值

"""
打开metadata.jsonl，获取今生成的图片，复制图片，转移到桌面
"""
deskpath=desktop_path()
chonice_date=str(datetime.datetime.today())[:10]

with jsonlines.open("metadata.jsonl") as f:
    for line in f:
        if line['date'] ==chonice_date:
            save_dirs=save_2_path(deskpath,line['Category_zh'],line['Class_zh'])
            image_path_list=line['image_path']
            for image_path in image_path_list:
                name=image_path.split('\\')[-1].replace('png','jpg')
                transfer(image_path,save_dirs+'\\'+name)
