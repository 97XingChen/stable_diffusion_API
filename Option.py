import argparse
import tool
import webuiapi

class Option():
    def __init__(self):
        self.opt=self.parse_args()
    def parse_args(self, *args, **kwargs):
        """
        添加图生图，文生图的参数信息
        :param args:
        :param kwargs:
        :return:
        """
        self.sd_models= tool.get_option_message('sd-models')
        self.samplers=tool.get_option_message('samplers')
        self.parser = argparse.ArgumentParser(description="Simple example of text to image.")
        self.parser.add_argument(
            "--image_path",
            type=str,
            default=False,
            help="Path to load image",
        )
        self.parser.add_argument(
            "--mask_path",
            type=str,
            default=False,
            help="Path to load mask",
        )
        self.parser.add_argument(
            "--sd_model_checkpoint",
            type=str,
            default="v1-5-pruned-emaonly.ckpt [cc6cb27103]",
            choices=[model['title'] for model  in self.sd_models ],
            help="Path to pretrained model or model identifier from huggingface.co/models.",
        )
        self.parser.add_argument(
            "--sampler",
            type=str,
            default="Euler a",
            choices=[ sampler['name'] for sampler in self.samplers],
            help="这是模型的采样器",
        )

        self.parser.add_argument(
            "--enable_hr",
            type=str,
            default=False,
            help="use Hires.fix 使用高清修复，enable_hr=True的时候 后面一高清工具系列才会启用"
        )
        self.parser.add_argument(
            "--hr_upscaler",
            default=webuiapi.HiResUpscaler.Latent,
            help="use Hires.fix 使用高清修复的放大方法"
        )

        self.parser.add_argument(
            "--hr_scale",
            type=float,
            default=2,
            help="use Hires.fix 使用高清修复的方法倍数"
        )
        self.parser.add_argument(
            "--hr_second_pass_steps",
            type=int,
            default=0,
            help="use Hires.fix 使用高清修复的高清修复采样次数"
        )


        self.parser.add_argument(
            "--hr_resize_x",
            type=float,
            default=0,
            help="use Hires.fix 使用高清修复调整宽度"
        )
        self.parser.add_argument(
            "--hr_resize_y",
            type=float,
            default=0,
            help="use Hires.fix 使用高清修复调整高度"
        )

        self.parser.add_argument(
            "--prompt",
            type=str,
            default="a professional photograph of an astronaut riding a triceratops",
            help="the prompt to render"
        )
        self.parser.add_argument(
            "--negative_prompt",
            type=str,
            default="",
            help="the negative_prompt to render"
        )
        self.parser.add_argument(
            "--seed",
            type=int,
            default=-1,
            help="seed contorl picture"
        )

        self.parser.add_argument(
            "--cfg_scale",
            type=float,
            default=7,
            help="关键词相关性"
        )

        self.parser.add_argument(
            "--denoising_strength",
            type=float,
            default=0.75,
            help="降噪强度,强度越高，与原图片越无关"
        )

        self.parser.add_argument(
            "--batch_size",
            type=int,
            default=1,
            help="训练出图的数量"
        )

        self.parser.add_argument(
            "--n_iter",
            type=int,
            default=1,
            help="连续训练的轮数"
        )

        self.parser.add_argument(
            "--steps",
            type=int,
            help="The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference.int",
            default=20
        )

        self.parser.add_argument(
            "--height",
            type=int,
            help="The height in pixels of the generated image",
            default=512
        )
        self.parser.add_argument(
            "--width",
            type=int,
            help="The width in pixels of the generated image",
            default=512
        )

        self.parser.add_argument(
            "--inpainting_fill",
            type=int,
            help="[fill,original,latent noise, latent nothing]",
            default=0,
            choices=[0,1,2,3]
        )
        self.parser.add_argument(
            "--inpaint_full_res",
            type=int,
            help="",
            default=0,
            choices=[0, 1]
        )

        self.parser.add_argument(
            "--inpainting_mask_invert",
            type=int,
            help="[0:inpaint masked;1:Inpaint not masked]",
            default=0,
            choices=[0,1]
        )
        self.parser.add_argument(
            "--restore_faces",
            action='store_true',
            default=False,
            help='restore_faces'
        )
        self.parser.add_argument(
            "--tiling",
            action='store_true',
            default=False,
            help='tiling'
        )
        return self.parser

    def Controlnet_parse_args(self,name):
        """
        用于添加Controlnet形参信息
        :param name:controlnet 名称
        :return:
        """

        self.Controlnet_name=name
        self.Controlnet_types=tool.config['ControlnetOption']
        self.parser=self.opt
        self.parser.add_argument(
            f"--{self.Controlnet_name}_enable",
            action='store_true',
            help='is enable Controlnet？ '
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_input_image",
            default=False,
            type=str,
            help='input_image'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_Controlnet_type",
            default=None,
            type=str,
            choices=list(self.Controlnet_types.keys())+[None],
            help='Control types'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_module",
            default=None,
            type=str,
            help='Preprocessor'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_model",
            default=None,
            type=str,
            help='Control model'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_weight",
            default=1.0,
            type=float,
            help='weight'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_resize_mode",
            default="Resize and Fill",
            type=str,
            choices=["Just Resize","Crop and Resize","Resize and Fill"],
            help='resize_mode'
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_lowvram",
            default=False,
            type=bool,
            help=" is enable lowvram"
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_staring_contorl_step",
            default=0.0,
            type=float,
            help=" staring_contorl_step"
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_ending_contorl_step",
            default=1.0,
            type=float,
            help=" ending_contorl_step"
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_control_mode",
            default=0,
            type=int,
            choices=[0,1,2],
        help = " control_mode"
        )
        self.parser.add_argument(
            f"--{self.Controlnet_name}_pixel_perfect",
            default=False,
            type=bool,
            help=" pixel_perfect"
        )
        return self.parser



# if __name__ == "__main__":
    # img=ImgOption()
    # img.Controlnet_parse_args('Unit0')
    # img.Controlnet_parse_args('Unit1')
    # img.Controlnet_parse_args('Unit2')
    # print(img.opt.parse_args())
