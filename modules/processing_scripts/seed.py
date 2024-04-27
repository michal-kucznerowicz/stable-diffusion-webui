import json

import gradio as gr

from modules import infotext_utils
from modules import scripts, errors


class ScriptSeed(scripts.ScriptBuiltinUI):
    section = "seed"
    create_group = False

    def __init__(self):
        self.seed = None
        self.reuse_seed = None
        self.reuse_subseed = None

    def title(self):
        return "Seed"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        seed = -1
        sub_seed = -1
        sub_seed_strength = 0.0
        seed_resize_from_w_value = 0
        seed_resize_from_h_value = 0

        with gr.Row(elem_id=self.elem_id("seed_row")):
            self.seed = gr.Number(label='Seed', value=seed, elem_id=self.elem_id("seed"), visible=False)
            seed_checkbox = gr.Checkbox(label='Extra', elem_id=self.elem_id("subseed_show"), value=False, visible=False)

        with gr.Group(visible=False, elem_id=self.elem_id("seed_extras")):
            with gr.Row(elem_id=self.elem_id("subseed_row")):
                subseed = gr.Number(label='Variation seed', value=sub_seed, elem_id=self.elem_id("subseed"), visible=False)
                subseed_strength = gr.Slider(label='Variation strength', value=sub_seed_strength, elem_id=self.elem_id("subseed_strength"), visible=False)

            with gr.Row(elem_id=self.elem_id("seed_resize_from_row")):
                seed_resize_from_w = gr.Slider(label="Resize seed from width", value=seed_resize_from_w_value, elem_id=self.elem_id("seed_resize_from_w"), visible=False)
                seed_resize_from_h = gr.Slider(label="Resize seed from height", value=seed_resize_from_h_value, elem_id=self.elem_id("seed_resize_from_h"), visible=False)

        return self.seed, seed_checkbox, subseed, subseed_strength, seed_resize_from_w, seed_resize_from_h

    def setup(self, p, seed, seed_checkbox, subseed, subseed_strength, seed_resize_from_w, seed_resize_from_h):
        p.seed = seed

        if seed_checkbox and subseed_strength > 0:
            p.subseed = subseed
            p.subseed_strength = subseed_strength

        if seed_checkbox and seed_resize_from_w > 0 and seed_resize_from_h > 0:
            p.seed_resize_from_w = seed_resize_from_w
            p.seed_resize_from_h = seed_resize_from_h


def connect_reuse_seed(seed: gr.Number, reuse_seed: gr.Button, generation_info: gr.Textbox, is_subseed):
    """ Connects a 'reuse (sub)seed' button's click event so that it copies last used
        (sub)seed value from generation info the to the seed field. If copying subseed and subseed strength
        was 0, i.e. no variation seed was used, it copies the normal seed value instead."""

    def copy_seed(gen_info_string: str, index):
        res = -1
        try:
            gen_info = json.loads(gen_info_string)
            infotext = gen_info.get('infotexts')[index]
            gen_parameters = infotext_utils.parse_generation_parameters(infotext, [])
            res = int(gen_parameters.get('Variation seed' if is_subseed else 'Seed', -1))
        except Exception:
            if gen_info_string:
                errors.report(f"Error retrieving seed from generation info: {gen_info_string}", exc_info=True)

        return [res, gr.update()]

    reuse_seed.click(
        fn=copy_seed,
        _js="(x, y) => [x, selected_gallery_index()]",
        show_progress=False,
        inputs=[generation_info, seed],
        outputs=[seed, seed]
    )
