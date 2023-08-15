import tool
from io import BytesIO
import subprocess
from PIL import Image
import base64
import re
import pandas as pd
import jsonlines


def run_command(cmd):
    """
    ### 在cmd中运行，并返回代码
    :param cmd: 批处理的运行代码
    :return: 返回终端运行信息
    """
    (status, output) = subprocess.getstatusoutput(cmd)
    # 检查返回代码
    return (status, output)


def process_sd_api(python_path, py_path, Formal_parameters):
    """
    在终端中运行
    :param python_path:python.exe的地址
    :param py_path:py文件的地址
    :param Formal_parameters:
    :return:返回终端运行信息
    """
    wav2lip_cmd = f"{python_path} {py_path} {Formal_parameters}"
    ###利用终端运行
    result = run_command(wav2lip_cmd)
    if result[0] != 0:
        print("An error occurred while running sd_tool")
    return result[1]


def base4_2_img(python_path,py_path,Formal_parameters):
    """
    ####将图片转化为base64格式,可用于上传到web网站上
    :param python_path: python.exe的地址
    :param py_path: py文件的地址
    :param Formal_parameters: 运行py文件的参数
    :return:
    """
    images=process_sd_api(python_path,py_path,Formal_parameters)
    images_list=eval(images)
    for base64_str in images_list:
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.show()


def path_2_img(python_path,py_path,Formal_parameters):
    """
    返回图片的地址用于下一步的整理文件夹
    :param python_path:
    :param py_path:
    :param Formal_parameters:运行py文件的参数
    :return:返回图片的地址列表
    """
    images=process_sd_api(python_path,py_path,Formal_parameters)
    images_list=eval(images)
    return images_list


def data_group_sample(texture_data):
    """
    在texture_data每一个Class_zh中各抽取2个模型关键词，不够两个只抽取一个
    :param texture_data:
    :return:返回 Class_zh，模型关键词
    """
    class_name=list(set(texture_data['Class_zh']))
    typicalNDict={}
    for i in class_name:
        typicalNDict[i]=2
    def typicalsamling(group, typicalNDict):
        name = group.name
        n = typicalNDict[name]
        if len(group)==1:
            n=1
        return group.sample(n=n)
    result = texture_data.groupby('Class_zh', as_index=False).apply(typicalsamling, typicalNDict,)
    return result

if __name__ == "__main__":
    python_path=r'D:\PyCharm2022.1.3\PycharmProject\stable_diffusion_API\venv\Scripts\python.exe'
    py_path= r'D:\PyCharm2022.1.3\PycharmProject\stable_diffusion_API\mytext2img.py'
    texture_data=pd.read_excel(r'text2img/texture_data.xlsx')
    texture_data_sample=data_group_sample(texture_data).reset_index()
    ###循环跑数
    for i in range(0, len(texture_data_sample)):
        image_dict={}
        prompt=texture_data_sample.loc[i,'prompt']
        Formal_parameters=f'--prompt="seamless pattern, {prompt},symmetry,repeat,texture" '\
                          '--negative_prompt="deformed,low quality，irregular shape, deformed, asymmetrical, wavy lines, blurred, (low quality), (real photo)，text,logo,wordmark,writing,heading,signature" ' \
                          '--sd_model_checkpoint="v1-5-pruned-emaonly.ckpt [cc6cb27103]" ' \
                          '--batch_size=5 ' \
                          '--height=512 ' \
                          '--width=512 ' \
                          '--enable_hr=True ' \
                          '--hr_upscaler=None ' \
                          '--hr_resize_x=1200 ' \
                          '--hr_resize_y=1200 ' \
                          '--denoising_strength=0.7 ' \
                          # f'--prompt="seamless pattern, {prompt},symmetry,repeat,texture" ' \
        # '--tiling'

        image_path=path_2_img(python_path,py_path,Formal_parameters)

        image_dict['date']=str(tool.get_date())
        image_dict['Category_zh'] =texture_data_sample.loc[i,'Category_zh']
        image_dict['Category_en'] = texture_data_sample.loc[i, 'Category_en']
        image_dict['Class_zh'] = texture_data_sample.loc[i, 'Class_zh']
        image_dict['Class_en'] = texture_data_sample.loc[i, 'Class_en']
        image_dict['prompt'] = prompt
        image_dict['image_path'] = image_path

###保存图片信息存储到jsonl文件中
        with jsonlines.open('metadata.jsonl', mode='a') as writer:
            writer.write(image_dict)
        print(i,texture_data_sample.loc[i,'Category_zh'],texture_data_sample.loc[i, 'Class_zh'])

