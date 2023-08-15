import webuiapi
import tool
from PIL import Image
from Option import Option
import os


def main(opt):
    api = webuiapi.WebUIApi(host=tool.config['host'], port=tool.config['port'])
    image_Load = Image.open(opt.image_path)
    mask_Load = Image.open(opt.mask_path)
    result1 = api.img2img(images=[image_Load],
                                    mask_image=mask_Load,
                                    inpainting_fill=opt.inpainting_fill,
                                    inpaint_full_res=opt.inpaint_full_res,
                                    inpainting_mask_invert=opt.inpainting_mask_invert,
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
                                    override_settings={
                                        "sd_model_checkpoint": opt.sd_model_checkpoint
                                    },
                                    sampler_name=opt.sampler,
                                    controlnet_units=tool.prepare_unit(opt),
                                    )

    outdir='img2img_inpaint'
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

    return result1_path


if __name__ == "__main__":
    controlnet_list=["Unit0","Unit1","Unit2"]
    img = Option()
    for controlnet in controlnet_list:
        img.Controlnet_parse_args(controlnet)
    print(main(img.opt.parse_args()))
