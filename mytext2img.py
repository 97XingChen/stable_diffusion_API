import webuiapi
import tool
from Option import Option
import base64
from io import BytesIO
import os
from datetime import date

def main(opt):
    """
    传入opt参数，用于生成图片
    :param opt: 形参
    :return:
    """
    api = webuiapi.WebUIApi(host=tool.config['host'], port=tool.config['port'])
    result1 = api.txt2img(
        enable_hr=opt.enable_hr,
        hr_upscaler=opt.hr_upscaler,
        hr_scale=opt.hr_scale,
        hr_second_pass_steps=opt.hr_second_pass_steps,
        hr_resize_x=opt.hr_resize_x,
        hr_resize_y=opt.hr_resize_y,
        prompt=opt.prompt,
        negative_prompt=opt.negative_prompt,
        seed=opt.seed,
        cfg_scale=opt.cfg_scale,
        denoising_strength=opt.denoising_strength,
        batch_size=opt.batch_size,
        n_iter=opt.n_iter,
        steps=opt.steps,
        width=opt.width,
        height=opt.height,
        restore_faces=opt.restore_faces,
        tiling=opt.tiling,
        override_settings ={
            "sd_model_checkpoint":opt.sd_model_checkpoint
        },
        sampler_name=opt.sampler,
        controlnet_units = tool.prepare_unit(opt),
    )
    ##保存文件
    outdir='text2img'
    date_path,base_count=tool.save_2_path(outdir)
    result1_images=[]
    result1_path=[]

    for i in result1.images:
        while True:
            image_name = f"{base_count:05}.png"
            if image_name in os.listdir(date_path):
                base_count += 1
            else:
                save_path=os.path.join(date_path, image_name)
                i.save(save_path)
                base_count += 1
                break
        img_str=tool.im_2_b64(i)
        result1_images.append(img_str)
        result1_path.append(save_path)
    ##返回文件目录
    return result1_path

if __name__ == "__main__":
    ##添加三个controlnet名称
    controlnet_list=["Unit0","Unit1","Unit2"]
    img = Option()
    for controlnet in controlnet_list:
        img.Controlnet_parse_args(controlnet)
    print(main(img.opt.parse_args()))



