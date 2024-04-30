import gradio as gr

from modules import shared, ui_common
from modules.shared import opts
from modules.ui_components import ToolButton
from modules.ui_prompt_tag import PromptTag


class Toprow:
    base = None
    __base_prompt_tag = PromptTag(label="Base", choices=["woman", "milf", "celebrity", "lingerie model", "athlete", "bodybuilder", "cyborg", "sorority", "bimbo"])
    number_of_people = None
    __number_of_people_prompt_tag = PromptTag(label="Number of people", choices=["one", "two", "several"])
    body = None
    __body_prompt_tag = PromptTag(label="Body", choices=["busty", "huge boobs", "perfect boobs", "small boobs", "beautiful", "muscular", "big ass", "perfect ass", "small ass", "thick", "big hips", "long legs", "short", "tall", "perfect body", "skinny", "slim", "chubby", "fat", "oiled body"])
    age = None
    __age_prompt_tag = PromptTag(label="Age", choices=["18", "20", "30", "40", "50", "60", "70", "80"])
    face = None
    __face_prompt_tag = PromptTag(label="Face", choices=["happy", "sad", "serious", "laughing", "orgasm", "seductive", "pouting lips", "shocked", "angry", "ahegao"])
    hair_color = None
    __hair_color_prompt_tag = PromptTag(label="Hair color", choices=["blonde", "brunette", "redhead", "black hair", "blue hair", "green hair", "purple hair", "pink hair"])
    hair_style = None
    __hair_style_prompt_tag = PromptTag(label="Hair style", choices=["bobcut", "pigtails", "bun hair", "pixie", "ponytail", "messy", "bangs", "braided", "slicked", "straight", "curly"])
    ethnicity = None
    __ethnicity_prompt_tag = PromptTag(label="Ethnicity", choices=["african", "arabic", "asian", "brazilian", "british", "caucasian", "chinese", "czech", "dutch", "egyptian", "ethiopian", "filipina", "french", "german", "greek", "hungarian", "indian", "indonesian", "irish", "italian", "japanese", "jewish", "korean", "latina", "malaysian", "mongolian", "american", "nigerian", "nilotic", "persian", "polynesian", "polish", "portuguese", "russian", "scandinavian", "slavic", "spanish", "thai", "turkish", "vietnamese"])
    style = None
    __style_prompt_tag = PromptTag(label="Style", choices=["mirror selfie", "painting", "black and white", "vintage", "film photo", "illustration", "charcoal", "watercolor", "comic"])
    setting = None
    __setting_prompt_tag = PromptTag(label="Setting", choices=["bar", "bathroom", "beach", "bedroom", "bus", "cafe", "car", "casino", "cave", "changing room", "church", "club", "couch", "desert", "forest", "grocery", "gym", "hospital", "hot tub", "jungle", "kitchen", "lake", "locker room", "mall", "meadow", "moon", "mountains", "oasis", "office", "onsen", "party", "pool", "prison", "restaurant", "sauna", "shower", "snow", "stage", "street", "strip club", "tent", "train", "underwater", "wedding", "yacht"])
    view = None
    __view_prompt_tag = PromptTag(label="View", choices=["front view", "side view", "back view", "close-up view"])
    action = None
    __action_prompt_tag = PromptTag(label="Action", choices=["standing", "sitting", "lying down", "yoga", "sleeping", "squatting", "cooking", "eating", "jumping", "working out", "t-pose", "bathing", "gaming", "plank", "massage", "bending over", "spreading legs", "cumshot", "on back", "straddling"])
    clothing = None
    __clothing_prompt_tag = PromptTag(label="Clothing", choices=["nude", "60s", "70s", "80s", "90s", "angel", "apron", "basketball", "bathrobe", "bdsm", "beach volleyball", "bikini", "blouse", "bodypaint", "bomber", "boots", "bow tie", "bra", "casual", "cheerleader", "chemise", "choker", "clown", "construction worker", "corset", "cosplay", "crop top", "daisy dukes", "devil", "dirndl", "doctor", "dominatrix", "dress", "face mask", "fanstasy armor", "firefighter", "fishnet", "flight attendant", "fur", "hgeisha", "gloves", "golf", "goth", "halloween", "harem pants", "harlequin", "hat", "high heels", "high socks", "hijab", "hip hop", "jacket", "jeans", "jumpsuit", "kilt", "kimono", "lab coat", "latex", "leather", "lingerie", "long skirt", "lumberjack", "maid", "martial arts", "mech suit", "medieval", "mesh", "micro skirt", "microkini", "military", "mini skirt", "nightgown", "ninja", "niqab", "nun", "nurse", "one piece swimsuit", "onesie", "pajamas", "panties", "pantyhose", "parka", "pilot", "pirate", "police", "polo", "professor", "push-up bra", "race driver", "roman", "sailor", "salwar", "santa", "sari", "satin", "scarf", "sci-fi armor", "secretary", "shirt", "short shorts", "soccer", "space suit", "spandex", "sports", "sports bra", "steampunk", "stockings", "stylish", "suit", "sundress", "superhero", "suspender belt", "sweater", "tailcoat", "tank top", "teacher", "tennis", "thigh socks", "thong", "tie", "towel", "traditional", "trench coat", "tribal", "tunic", "underwear", "vampire", "victorian", "viking", "waitress", "wedding", "western", "witch", "yoga pants"])
    clothing_modifiers = None
    __clothing_modifiers_prompt_tag = PromptTag(label="Clothing modifiers", choices=["cleavage", "partially nude", "topless", "transparent"])
    accessories = None
    __accessories_prompt_tag = PromptTag(label="Accessories", choices=["beer", "gold jewelry", "silver jewelry", "diamond jewelry", "pearl jewelry", "wine"])
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
        self.base = gr.CheckboxGroup(label=self.__base_prompt_tag.label, choices=self.__base_prompt_tag.choices, elem_classes="prompt-tag")
        self.number_of_people = gr.CheckboxGroup(label=self.__number_of_people_prompt_tag.label, choices=self.__number_of_people_prompt_tag.choices, elem_classes="prompt-tag")
        self.body = gr.CheckboxGroup(label=self.__body_prompt_tag.label, choices=self.__body_prompt_tag.choices, elem_classes="prompt-tag")
        self.age = gr.CheckboxGroup(label=self.__age_prompt_tag.label, choices=self.__age_prompt_tag.choices, elem_classes="prompt-tag")
        self.face = gr.CheckboxGroup(label=self.__face_prompt_tag.label, choices=self.__face_prompt_tag.choices, elem_classes="prompt-tag")
        self.hair_color = gr.CheckboxGroup(label=self.__hair_color_prompt_tag.label, choices=self.__hair_color_prompt_tag.choices, elem_classes="prompt-tag")
        self.hair_style = gr.CheckboxGroup(label=self.__hair_style_prompt_tag.label, choices=self.__hair_style_prompt_tag.choices, elem_classes="prompt-tag")
        self.ethnicity = gr.CheckboxGroup(label=self.__ethnicity_prompt_tag.label, choices=self.__ethnicity_prompt_tag.choices, elem_classes="prompt-tag")
        self.style = gr.CheckboxGroup(label=self.__style_prompt_tag.label, choices=self.__style_prompt_tag.choices, elem_classes="prompt-tag")
        self.setting = gr.CheckboxGroup(label=self.__setting_prompt_tag.label, choices=self.__setting_prompt_tag.choices, elem_classes="prompt-tag")
        self.view = gr.CheckboxGroup(label=self.__view_prompt_tag.label, choices=self.__view_prompt_tag.choices, elem_classes="prompt-tag")
        self.action = gr.CheckboxGroup(label=self.__action_prompt_tag.label, choices=self.__action_prompt_tag.choices, elem_classes="prompt-tag")
        self.clothing = gr.CheckboxGroup(label=self.__clothing_prompt_tag.label, choices=self.__clothing_prompt_tag.choices, elem_classes="prompt-tag")
        self.clothing_modifiers = gr.CheckboxGroup(label=self.__clothing_modifiers_prompt_tag.label, choices=self.__clothing_modifiers_prompt_tag.choices, elem_classes="prompt-tag")
        self.accessories = gr.CheckboxGroup(label=self.__accessories_prompt_tag.label, choices=self.__accessories_prompt_tag.choices, elem_classes="prompt-tag")
        self.effects = gr.CheckboxGroup(label=self.__effects_prompt_tag.label, choices=self.__effects_prompt_tag.choices, elem_classes="prompt-tag")

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
