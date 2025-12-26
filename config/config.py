import os

DIFFUSION_MODEL_XS = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-256+16+aug01+mod_best_epoch228_loss_0.8337311961434104.pt",
)

DIFFUSION_MODEL_S = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-512+8+aug01+mod_best_epoch235_loss_0.8336052786220204.pt",
)
DIFFUSION_MODEL_M = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-1024+4+aug01+mod_best_epoch235_loss_0.8470401709729974.pt",
)
DIFFUSION_MODEL_L = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-2048+4+aug02+mod_best_epoch327_loss_0.8674218753973643.pt",
)
DIFFUSION_MODEL_XL = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-4096+4+aug03+mod_best_epoch337_loss_0.8850460449854533.pt",
)
DIFFUSION_MODEL_XXL = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-8192+4+aug04+mod_best_epoch622_loss_0.8956325948238373.pt",
)

DIFFUSION_MODEL_XXXL = (
    "martstilde/black-latents-latent-diffusion-models",
    "diffusion/rldf-16384+4+aug05+mod_best_epoch758_loss_0.9205791354179382.pt",
)
RAVE_MODEL = (
    "martstilde/black-latents-latent-diffusion-models",
    "vae/rave-v2_cap128_black-latents__dec_stereo.ts",
)
TEMP_PATH = "./temp"

os.makedirs(TEMP_PATH, exist_ok=True)
