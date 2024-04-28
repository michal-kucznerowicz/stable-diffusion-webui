import gradio as gr

from modules import shared, ui_common
from modules.shared import opts
from modules.ui_components import ToolButton
from modules.ui_prompt_tag import PromptTag


class Toprow:
    base = None
    __base_prompt_tag = PromptTag(label="Base", choices=["woman", "man"])
    number_of_people = None
    __number_of_people_prompt_tag = PromptTag(label="Number of people", choices=["one", "two", "several"])
    body = None
    __body_prompt_tag = PromptTag(label="Body", choices=["skinny", "slim", "chubby", "fat"])
    age = None
    __age_prompt_tag = PromptTag(label="Age", choices=["20", "30", "40", "50", "60", "70", "80"])
    face = None
    __face_prompt_tag = PromptTag(label="Face", choices=["happy", "sad"])
    hair_color = None
    __hair_color_prompt_tag = PromptTag(label="Hair color", choices=["blonde", "brunette", "redhead", "black hair"])
    hair_style = None
    __hair_style_prompt_tag = PromptTag(label="Hair style", choices=["bobcut", "bun hair", "ponytail", "braided"])
    ethnicity = None
    __ethnicity_prompt_tag = PromptTag(label="Ethnicity", choices=["latina", "slavic", "asian"])
    style = None
    __style_prompt_tag = PromptTag(label="Style", choices=["painting", "vintage", "black and white"])
    setting = None
    __setting_prompt_tag = PromptTag(label="Setting", choices=["cafe", "car", "office"])
    view = None
    __view_prompt_tag = PromptTag(label="View", choices=["front", "side", "back"])
    action = None
    __action_prompt_tag = PromptTag(label="Action", choices=["standing", "sitting", "lying down"])
    clothing = None
    __clothing_prompt_tag = PromptTag(label="Clothing", choices=["police", "nurse", "waitress"])
    clothing_modifiers = None
    __clothing_modifiers_prompt_tag = PromptTag(label="Clothing modifiers", choices=["cleavage", "transparent"])
    accessories = None
    __accessories_prompt_tag = PromptTag(label="Accessories", choices=["gold jewelry", "silver jewelry"])
    effects = None
    __effects_prompt_tag = PromptTag(label="Effects", choices=["bright lighting", "dark lighting"])

    button_interrogate = None
    button_deepbooru = None

    interrupt = None
    interrupting = None
    submit = None

    restore_progress_button = None

    submit_box = None
    output_panel = None

    def __init__(self, is_img2img, id_part=None):
        if id_part is None:
            id_part = "img2img" if is_img2img else "txt2img"

        self.id_part = id_part
        self.is_img2img = is_img2img

        self.create_classic_toprow()

    def create_classic_toprow(self):
        with gr.Row(elem_id=f"{self.id_part}_toprow", variant="compact"):
            with gr.Column(elem_id=f"{self.id_part}_prompt_container", scale=2):
                self.create_prompts()

            with gr.Column(elem_id=f"{self.id_part}_actions_column", scale=1):
                with gr.Group(elem_id=f"{self.id_part}_sticky_actions"):
                    self.output_panel = self.create_output_panel()
                    self.create_submit_box()
                    self.create_tools_row()

    def create_prompts(self):
        self.base = gr.CheckboxGroup(label=self.__base_prompt_tag.label, choices=self.__base_prompt_tag.choices)
        self.number_of_people = gr.CheckboxGroup(label=self.__number_of_people_prompt_tag.label, choices=self.__number_of_people_prompt_tag.choices)
        self.body = gr.CheckboxGroup(label=self.__body_prompt_tag.label, choices=self.__body_prompt_tag.choices)
        self.age = gr.CheckboxGroup(label=self.__age_prompt_tag.label, choices=self.__age_prompt_tag.choices)
        self.face = gr.CheckboxGroup(label=self.__face_prompt_tag.label, choices=self.__face_prompt_tag.choices)
        self.hair_color = gr.CheckboxGroup(label=self.__hair_color_prompt_tag.label, choices=self.__hair_color_prompt_tag.choices)
        self.hair_style = gr.CheckboxGroup(label=self.__hair_style_prompt_tag.label, choices=self.__hair_style_prompt_tag.choices)
        self.ethnicity = gr.CheckboxGroup(label=self.__ethnicity_prompt_tag.label, choices=self.__ethnicity_prompt_tag.choices)
        self.style = gr.CheckboxGroup(label=self.__style_prompt_tag.label, choices=self.__style_prompt_tag.choices)
        self.setting = gr.CheckboxGroup(label=self.__setting_prompt_tag.label, choices=self.__setting_prompt_tag.choices)
        self.view = gr.CheckboxGroup(label=self.__view_prompt_tag.label, choices=self.__view_prompt_tag.choices)
        self.action = gr.CheckboxGroup(label=self.__action_prompt_tag.label, choices=self.__action_prompt_tag.choices)
        self.clothing = gr.CheckboxGroup(label=self.__clothing_prompt_tag.label, choices=self.__clothing_prompt_tag.choices)
        self.clothing_modifiers = gr.CheckboxGroup(label=self.__clothing_modifiers_prompt_tag.label, choices=self.__clothing_modifiers_prompt_tag.choices)
        self.accessories = gr.CheckboxGroup(label=self.__accessories_prompt_tag.label, choices=self.__accessories_prompt_tag.choices)
        self.effects = gr.CheckboxGroup(label=self.__effects_prompt_tag.label, choices=self.__effects_prompt_tag.choices)

    def create_submit_box(self):
        with gr.Row(elem_id=f"{self.id_part}_generate_box", elem_classes=["generate-box"] + ([]), render=not False) as submit_box:
            self.submit_box = submit_box

            self.interrupt = gr.Button('Cancel', elem_id=f"{self.id_part}_interrupt", elem_classes="generate-box-interrupt", tooltip="End generation immediately or after completing current batch")
            self.interrupting = gr.Button('Canceling...', elem_id=f"{self.id_part}_interrupting", elem_classes="generate-box-interrupting", tooltip="Interrupting generation...")
            self.submit = gr.Button('Generate', elem_id=f"{self.id_part}_generate", variant='primary', tooltip="Right click generate forever menu")

            def interrupt_function():
                if not shared.state.stopping_generation and shared.state.job_count > 1 and shared.opts.interrupt_after_current:
                    shared.state.stop_generating()
                    gr.Info("Generation will stop after finishing this image, click again to stop immediately.")
                else:
                    shared.state.interrupt()

            self.interrupt.click(fn=interrupt_function, _js='function(){ showSubmitInterruptingPlaceholder("' + self.id_part + '"); }')
            self.interrupting.click(fn=interrupt_function)

    def create_tools_row(self):
        with gr.Row(elem_id=f"{self.id_part}_tools"):
            from modules.ui import restore_progress_symbol

            if self.is_img2img:
                self.button_interrogate = ToolButton('📎', tooltip='Interrogate CLIP - use CLIP neural network to create a text describing the image, and put it into the prompt field', elem_id="interrogate")
                self.button_deepbooru = ToolButton('📦', tooltip='Interrogate DeepBooru - use DeepBooru neural network to create a text describing the image, and put it into the prompt field', elem_id="deepbooru")

            self.restore_progress_button = ToolButton(value=restore_progress_symbol, elem_id=f"{self.id_part}_restore_progress", visible=False, tooltip="Restore progress")

    def create_output_panel(self):
        out_dir = opts.outdir_txt2img_samples if self.id_part == "txt2img" else opts.outdir_img2img_samples
        return ui_common.create_output_panel(self.id_part, out_dir)
