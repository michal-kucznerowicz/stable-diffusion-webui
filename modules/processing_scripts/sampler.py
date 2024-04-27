import gradio as gr

from modules import scripts, sd_samplers, sd_schedulers
from modules.ui_components import FormRow


class ScriptSampler(scripts.ScriptBuiltinUI):
    section = "sampler"

    def __init__(self):
        self.steps = None
        self.sampler_name = None
        self.scheduler = None

    def title(self):
        return "Sampler"

    def ui(self, is_img2img):
        sampler_names = [x.name for x in sd_samplers.visible_samplers()]
        scheduler_names = [x.label for x in sd_schedulers.schedulers]

        sampler = sampler_names[0]
        scheduler = scheduler_names[0]
        steps = 20

        with FormRow(elem_id=f"sampler_selection_{self.tabname}"):
            self.sampler_name = gr.Dropdown(label='Sampling method', elem_id=f"{self.tabname}_sampling", choices=sampler_names, value=sampler, visible=False)
            self.scheduler = gr.Dropdown(label='Schedule type', elem_id=f"{self.tabname}_scheduler", choices=scheduler_names, value=scheduler, visible=False)
            self.steps = gr.Slider(elem_id=f"{self.tabname}_steps", label="Sampling steps", value=steps, visible=False)

        return self.steps, self.sampler_name, self.scheduler

    def setup(self, p, steps, sampler_name, scheduler):
        p.steps = steps
        p.sampler_name = sampler_name
        p.scheduler = scheduler
