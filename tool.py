import requests
import json
from PIL import Image
import webuiapi
from datetime import date
from io import BytesIO
import base64
import os

with open("config.json","r") as con:
    config=json.load(con)
url_base=r'http://'+config['host']+':'+str(config['port'])

def get_option_message(option):
    """
    :param option: sd_api的选项
    :return: 选项中的信息
    choince=['options','sd-models','samplers','realesrgan-models','embeddings','loras']
    """
    response = requests.get(url=f'{url_base}/sdapi/v1/{option}')
    message = response.json()
    return message

def get_controlnet_message(option):
    """
    :param option: sd_api的选项
    :return: 选项中的信息
    choince=['module_list','model_list']
    """
    response = requests.get(url=f'{url_base}/controlnet/{option}')
    message = response.json()
    return message



def prepare_unit(opt):
    """
    建立三个ControlNetUnit 名称分别为 Unit0，Unit1，Unit2，同时利用在opt里面传入形参的方式添加ControlNetUnit
    当Unit0_enable=ture 即 Unit0_enable传入store_true的时候触发建立ControlNetUnit
    :param opt: Option中的opt
    :return: 三个ControlNetUnit功能
    """
    controlnet_list=[]
    if opt.Unit0_enable:
        image0_Load = Image.open(opt.Unit0_input_image,)
        unit0 = webuiapi.ControlNetUnit(input_image=image0_Load,
                                        module=opt.Unit0_module,
                                        model=opt.Unit0_model,
                                        weight=opt.Unit0_weight,
                                        resize_mode=opt.Unit0_resize_mode,
                                        lowvram=opt.Unit0_lowvram,
                                        guidance_start=opt.Unit0_staring_contorl_step,
                                        guidance_end=opt.Unit0_ending_contorl_step,
                                        control_mode=opt.Unit0_control_mode,
                                        pixel_perfect=opt.Unit0_pixel_perfect, )
        controlnet_list.append(unit0)
    else:
        pass
    if opt.Unit1_enable:
        image1_Load = Image.open(opt.Unit1_input_image, )
        unit1 = webuiapi.ControlNetUnit(input_image=image1_Load,
                                        module=opt.Unit1_module,
                                        model=opt.Unit1_model,
                                        weight=opt.Unit1_weight,
                                        resize_mode=opt.Unit1_resize_mode,
                                        lowvram=opt.Unit1_lowvram,
                                        guidance_start=opt.Unit1_staring_contorl_step,
                                        guidance_end=opt.Unit1_ending_contorl_step,
                                        control_mode=opt.Unit1_control_mode,
                                        pixel_perfect=opt.Unit1_pixel_perfect, )
        controlnet_list.append(unit1)
    else:
        pass

    if opt.Unit2_enable:
        image2_Load = Image.open(opt.Unit2_input_image, )
        Unit2 = webuiapi.ControlNetUnit(input_image=image2_Load,
                                        module=opt.Unit2_module,
                                        model=opt.Unit2_model,
                                        weight=opt.Unit2_weight,
                                        resize_mode=opt.Unit2_resize_mode,
                                        lowvram=opt.Unit2_lowvram,
                                        guidance_start=opt.Unit2_staring_contorl_step,
                                        guidance_end=opt.Unit2_ending_contorl_step,
                                        control_mode=opt.Unit2_control_mode,
                                        pixel_perfect=opt.Unit2_pixel_perfect, )
        controlnet_list.append(Unit2)
    else:
        pass

    return controlnet_list


def get_date():
    return date.today()


def im_2_b64(image):
    """
    :param image: 图片
    :return: base64的字符串形式的图片
    """
    buff = BytesIO()
    image.save(buff, format="png")
    img_str = base64.b64encode(buff.getvalue())
    img_str = str(img_str, "utf-8")
    return img_str

def save_2_path(out_dir):
    """
    :param out_dir:输出的目录
    :return: 日期，目录里面文件的个数
    """
    os.makedirs(out_dir, exist_ok=True)
    sample_path = os.path.join(out_dir, "samples")
    os.makedirs(sample_path, exist_ok=True)
    date=get_date()
    date_path= os.path.join(sample_path, str(date))
    os.makedirs(date_path, exist_ok=True)
    base_count = len(os.listdir(date_path))
    return date_path,base_count
