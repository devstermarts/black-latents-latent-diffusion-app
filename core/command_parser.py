import os
import shlex
import subprocess

import scipy.io.wavfile as wav
from config.config import (
    RAVE_MODEL,
    TEMP_PATH,
)
from utils.resolve_model_ref import model_choice, resolve_model_ref


def command_parser(
    model_selection,
    multiplier,
    seed_a,
    seed_b,
    lerp,
    lerp_factor,
    temperature,
    diffusion_steps,
    latent_scale,
):
    model_ref = model_choice(model_selection)
    try:
        model_path = resolve_model_ref(model_ref)
        rave_path = resolve_model_ref(RAVE_MODEL)
    except Exception as e:
        print(f"Failed to resolve model path: {e}")
        return "Something went wrong!"

    command = (
        f"rldf-generate "
        f"--model_path={model_path} "
        f"--rave_model={rave_path} "
        f"--length_mult={multiplier} "
        f"--temperature={temperature} "
        f"--diffusion_steps={diffusion_steps} "
        f"--output_path={TEMP_PATH} "
        f"--latent_scale={latent_scale} "
    )
    if lerp:
        command += f"--seed_a={seed_a} --seed_b={seed_b} --lerp --lerp_factor={lerp_factor} --name=blld"
        audio_path = f"{TEMP_PATH}/blld_{seed_a}_{seed_b}_slerp.wav"
    else:
        command += f"--seed={seed_a} --name=blld"
        audio_path = f"{TEMP_PATH}/blld_{seed_a}.wav"
    try:
        args = shlex.split(command)
        result = subprocess.run(args, capture_output=True, text=True)

        if result.returncode != 0:
            print("Failed!")

    except Exception as e:
        return e

    print(f"Executing the following command: {command}")  # for debugging

    if os.path.exists(audio_path):
        sample_rate, audio_data = wav.read(audio_path)
        # os.remove(audio_path) # Remove temp audio file after readying for streaming in gr.Audio
        return sample_rate, audio_data
    return None
