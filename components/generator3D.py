import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.models.transmitter.base import Transmitter
from shap_e.util.image_util import load_image
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
import warnings
import os
import trimesh
from shap_e.util.notebooks import decode_latent_mesh


class ObjectGenerator:
    def __init__(self):
        if not torch.cuda.is_available():
            print('CUDA is not available')
        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=UserWarning)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.xm = load_model('transmitter', device=self.device)
        self.model = load_model('text300M', device=self.device)
        self.diffusion = diffusion_from_config(load_config('diffusion'))

        self.batch_size = 2

        self.guidance_scale_prompt = 15.0
        self.guidance_scale_image = 2.0

        self.render_mode = 'nerf'
        self.size = 64
        self.cameras = create_pan_cameras(self.size, self.device)

    def change_render_mode(self):
        if self.render_mode == 'nerf':
            self.render_mode = 'stf'
            return
        self.render_mode = 'nerf'

    def change_size(self, size):
        self.size = size

    def change_batch_size(self, batch_size):
        self.batch_size = batch_size

    def change_guidance_scale_prompt(self, scale):
        self.guidance_scale_prompt = scale

    def change_guidance_scale_image(self, scale):
        self.guidance_scale_image = scale

    def set_save_dir(self, save_dir):
        self.save_dir = save_dir

    def image_to_3d(self,image_url):
        image = load_image(image_url)
        if image.mode == "P":
            image = image.convert("RGBA")
        latents = sample_latents(
            batch_size=self.batch_size,
            model=self.model,
            diffusion=self.diffusion,
            guidance_scale=self.guidance_scale_image,
            model_kwargs=dict(images=[image] * self.batch_size),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps=64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0,
            device=self.device
        )
        return latents

    def prompt_to_3d(self,prompt):
        latents = sample_latents(
            batch_size=self.batch_size,
            model=self.model,
            diffusion=self.diffusion,
            guidance_scale=self.guidance_scale_prompt,
            model_kwargs=dict(texts=[prompt] * self.batch_size),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps=64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0,
            device=self.device
        )
        return latents

    def save_3dobjects(self,latents, *args):

        if len(args) == 1:
            filename = args[0]
            save_dir = "../default_save_dir"
        elif len(args) == 2:
            filename = args[1]
            save_dir = args[0]
        else:
            raise Exception("Add the filaname and director")

        for i, latent in enumerate(latents):
            t = decode_latent_mesh(self.xm, latent).tri_mesh()

            ply_path = os.path.join(save_dir, f"{filename}{i}.ply")
            obj_path = os.path.join(save_dir, f"{filename}{i}.obj")
            glb_path = os.path.join(save_dir, f"{filename}{i}.glb")

            with open(obj_path, 'w') as f:
                t.write_obj(f)
                print(f"Mesh {i} salvat ca {obj_path}")

            with open(ply_path, 'wb') as f:
                t.write_ply(f)
                print(f"Mesh {i} salvat ca {ply_path}")

            mesh_trimesh = trimesh.load(ply_path, force='mesh')
            mesh_trimesh.export(glb_path)
            print(f"Mesh {i} salvat ca {glb_path}")