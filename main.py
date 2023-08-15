import webuiapi
import tool
from PIL import Image
from Option import Option

class MystableDiffusion:
    def __init__(self,host,port):
        self.api=webuiapi.WebUIApi(host=host, port=port)

    def mytext2img(self,opt):
        mytext2img_result = self.api.txt2img(
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
        for i in mytext2img_result.images:
            i.show()
        return mytext2img_result.images

    def myimg2img(self,opt):
        image_Load = Image.open(opt.image_path)
        myimg2img_result = self.api.img2img(
            images=[image_Load],
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
        for i in myimg2img_result.images:
            i.show()
        return myimg2img_result.images



    def myimg2img_inpaint(self,opt):
        image_Load = Image.open(opt.image_path)
        mask_Load = Image.open(opt.mask_path)
        myimg2img_inpaint_result = self.api.img2img(images=[image_Load],
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
        for i in myimg2img_inpaint_result.images:
            i.show()
        return myimg2img_inpaint_result.images


if __name__ == "__main__":
    controlnet_list = ["Unit0", "Unit1", "Unit2"]
    img = Option()
    Mysd=MystableDiffusion(host="127.0.0.1",port="7860")
    for controlnet in controlnet_list:
        img.Controlnet_parse_args(controlnet)
    Mysd.myimg2img(img.opt.parse_args())

