import random

import gradio as gr
from core.command_parser import command_parser

theme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="teal",
    font=gr.themes.GoogleFont("Inter"),
    radius_size="sm",
)

# Todos:
# - Make more robust
#   - when seed empty, don't add --seed_* to command
#   - when seed_a == seed_b, deactivate Generate button

head = """
<meta name="description" content="Spawn audio items with latent diffusion models">
<meta name="author" content="Martin Heinze | marts~">
<meta property="og:title" content="Black Latents | Latent Diffusion">
<meta property="og:description" content="Spawn audio items with latent diffusion models">
"""

# Interface and layout
with gr.Blocks(title="Black Latents | Latent Diffusion") as demo:
    gr.Markdown("# *Black Latents* | Latent Diffusion")
    gr.Markdown(
        "With this app you can spawn millions of unheard audio items using [RAVE-Latent Diffusion](https://github.com/devstermarts/RAVE-Latent-Diffusion-Flex-Ed) and *[Black Latents](https://forum.ircam.fr/projects/detail/black-latents)*, a RAVE V2 VAE trained on the [Black Plastics series](https://martsman.bandcamp.com)."
    )
    gr.Markdown(
        "<small>Set up by [Martin Heinze | marts~](https://www.martstil.de) in December 2025. Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)</small>"
    )
    with gr.Column():
        model_selection = gr.Dropdown(
            choices=[
                "XS (256)",
                "S (512)",
                "M (1024)",
                "L (2048)",
                "XL (4096)",
                "XXL (8192)",
                "XXXL (16384)",
            ],
            value="XS (256)",
            interactive=True,
            visible=True,
            label="Diffusion model selection",
            info="Select pre trained diffusion model.",
        )
        with gr.Group():
            with gr.Row():
                seed_a = gr.Number(
                    label="Seed A",
                    precision=0,
                    value=(random.randint(0, 999999999)),
                    minimum=1,
                    maximum=999999999,
                    step=1,
                    scale=2,
                    interactive=True,
                    visible=True,
                )
                seed_b = gr.Number(
                    label="Seed B",
                    precision=0,
                    value=(random.randint(0, 999999999)),
                    minimum=1,
                    maximum=999999999,
                    step=1,
                    scale=2,
                    interactive=True,
                    visible=True,
                )
            with gr.Row():
                lerp = gr.Checkbox(
                    label="Lerp between seeds",
                    value=True,
                )
        with gr.Row():
            randomize_button = gr.Button(
                "Randomize seeds",
                variant="huggingface",
                size="sm",
            )

        with gr.Accordion("Advanced Settings", open=False):
            lerp_factor = gr.Slider(
                label="Lerp factor",
                info="Crossfade amount from Seed A to B during total length.",
                minimum=0.0,
                maximum=1.0,
                value=1.0,
                step=0.1,
                interactive=True,
                visible=True,
            )
            temperature = gr.Slider(
                label="Temperature",
                info="Model dependent. Select high value when in doubt.",
                minimum=0.1,
                maximum=1.0,
                value=1.0,
                step=0.01,
                interactive=True,
                visible=True,
            )
            diffusion_steps = gr.Slider(
                label="Diffusion Steps",
                info="Model dependent. Select high value when in doubt.",
                minimum=1,
                maximum=100,
                value=100,
                step=1,
                interactive=True,
                visible=True,
            )
            latent_scale = gr.Slider(
                label="Normalization",
                info="Scale/ normalize latents.",
                minimum=0.1,
                maximum=3,
                value=1,
                step=0.1,
                interactive=True,
                visible=True,
            )
            multiplier = gr.Slider(
                label="Audio length",
                info="Model base window size * length multiplier",
                minimum=1,
                maximum=10,
                step=1,
                value=1,
                interactive=True,
                visible=True,
            )
        generate_audio_button = gr.Button(
            "Generate",
            variant="primary",
        )
        audio_player = gr.Audio(
            label="Generated audio file",
            show_label=True,
        )

    # Event listeners
    randomize_button.click(
        fn=lambda: [
            gr.update(value=random.randint(0, 999999999)),
            gr.update(value=random.randint(0, 999999999)),
        ],
        outputs=[seed_a, seed_b],
        api_name=False,
    )
    lerp.change(
        fn=lambda x: [
            gr.update(interactive=x, visible=x),
            gr.update(interactive=x, visible=x),
            gr.update(label="Seed A" if x else "Seed"),
        ],
        inputs=lerp,
        outputs=[lerp_factor, seed_b, seed_a],
        api_name=False,
    )
    generate_audio_button.click(
        fn=command_parser,
        inputs=[
            model_selection,
            multiplier,
            seed_a,
            seed_b,
            lerp,
            lerp_factor,
            temperature,
            diffusion_steps,
            latent_scale,
        ],
        outputs=audio_player,
        api_name=False,
    )

demo.launch(
    head=head,
    theme=theme,
)
