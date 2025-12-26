import os

from config.config import (
    DIFFUSION_MODEL_L,
    DIFFUSION_MODEL_M,
    DIFFUSION_MODEL_S,
    DIFFUSION_MODEL_XL,
    DIFFUSION_MODEL_XS,
    DIFFUSION_MODEL_XXL,
    DIFFUSION_MODEL_XXXL,
    TEMP_PATH,
)
from huggingface_hub import hf_hub_download, snapshot_download


def model_choice(model_selection):
    if model_selection == "XS (256)":
        return DIFFUSION_MODEL_XS
    elif model_selection == "S (512)":
        return DIFFUSION_MODEL_S
    elif model_selection == "M (1024)":
        return DIFFUSION_MODEL_M
    elif model_selection == "L (2048)":
        return DIFFUSION_MODEL_L
    elif model_selection == "XL (4096)":
        return DIFFUSION_MODEL_XL
    elif model_selection == "XXL (8192)":
        return DIFFUSION_MODEL_XXL
    elif model_selection == "XXXL (16384)":
        return DIFFUSION_MODEL_XXXL
    else:
        raise ValueError("Invalid diffusion model selection")


def resolve_model_ref(model_ref):
    if isinstance(model_ref, str):
        if os.path.exists(model_ref):
            return model_ref
        raise ValueError(f"Local model path does not exist: {model_ref}")

    if isinstance(model_ref, (tuple, list)) and len(model_ref) == 2:
        repo_id, filename = model_ref
        token = os.getenv("HF_TOKEN")
        print(f"Attempting to download: {repo_id}/{filename}")  # Debug print
        print(f"Token present: {bool(token)}")  # Debug print
        try:
            local_path = snapshot_download(  # Use this to download the entire model repo to a local folder
                repo_id=repo_id,
                ignore_patterns=["*.md", ".gitattributes", ".gitignore"],
                token=token,
                local_dir=f"{TEMP_PATH}",
            )
            return f"{local_path}/{filename}"
            # local_path = hf_hub_download( # Use this for individual file download
            #     repo_id=repo_id,
            #     filename=filename,
            #     token=token,
            #     local_dir=f"{TEMP_PATH}",
            # )
            # return f"./{local_path}"
            print(f"Downloaded to: {local_path}")  # Debug print
        except Exception as e:
            print(f"Download failed with error: {e}")  # Debug print
            raise RuntimeError(f"Failed to load model: {repo_id}/{filename}") from e
    raise ValueError(f"Model reference not valid: {model_ref}")
