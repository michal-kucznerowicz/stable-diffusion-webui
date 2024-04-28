import json
from contextlib import closing

import gradio as gr
from PIL import Image

import modules.scripts
import modules.shared as shared
from modules import processing, infotext_utils
from modules.infotext_utils import create_override_settings_dict, parse_generation_parameters
from modules.shared import opts
from modules.ui import plaintext_to_html


def txt2img_create_processing(
        id_task: str,
        request: gr.Request,
        base,
        number_of_people,
        body,
        age,
        face,
        hair_color,
        hair_style,
        ethnicity,
        style,
        setting,
        view,
        action,
        clothing,
        clothing_modifiers,
        accessories,
        effects,
        enable_hr: bool,
        override_settings_texts,
        *args,
        force_enable_hr=False,  # TODO
):
    override_settings = create_override_settings_dict(override_settings_texts)

    if force_enable_hr:
        enable_hr = True

    prompt = (
            tag_to_prompt(base) +
            tag_to_prompt(number_of_people) +
            tag_to_prompt(body) +
            tag_to_prompt(age) +
            tag_to_prompt(face) +
            tag_to_prompt(hair_color) +
            tag_to_prompt(hair_style) +
            tag_to_prompt(ethnicity) +
            tag_to_prompt(style) +
            tag_to_prompt(setting) +
            tag_to_prompt(view) +
            tag_to_prompt(action) +
            tag_to_prompt(clothing) +
            tag_to_prompt(clothing_modifiers) +
            tag_to_prompt(accessories) +
            tag_to_prompt(effects)
    )
    prompt = f"""{prompt}"""
    prompt = prompt[:-2]
    print("Prompt: " + prompt)

    negative_prompt = """deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, text, cropped, out of frame, worst quality, low quality, 
    jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, 
    bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, 
    long neck"""
    print("Negative prompt: " + negative_prompt)

    p = processing.StableDiffusionProcessingTxt2Img(
        sd_model=shared.sd_model,
        outpath_samples=opts.outdir_samples or opts.outdir_txt2img_samples,
        outpath_grids=opts.outdir_grids or opts.outdir_txt2img_grids,
        prompt=prompt,
        styles=[],
        negative_prompt=negative_prompt,
        batch_size=1,
        n_iter=1,
        cfg_scale=7.0,
        width=512,
        height=512,
        enable_hr=enable_hr,
        denoising_strength=0.7,
        hr_scale=2.0,
        hr_upscaler="Latent",
        hr_second_pass_steps=0,
        hr_resize_x=0,
        hr_resize_y=0,
        hr_checkpoint_name=None,
        hr_sampler_name=None,
        hr_scheduler=None,
        hr_prompt="",
        hr_negative_prompt="",
        override_settings=override_settings,
    )

    p.scripts = modules.scripts.scripts_txt2img
    p.script_args = args

    p.user = request.username

    if shared.opts.enable_console_prompts:
        print(f"\ntxt2img: {prompt}", file=shared.progress_print_out)

    return p


def tag_to_prompt(tag):
    prompt = ''.join([str(e) + " " for e in tag])
    if prompt != "":
        prompt = prompt[:-1]
        prompt += ", "
    return prompt


def txt2img_upscale(id_task: str, request: gr.Request, gallery, gallery_index, generation_info, *args):
    assert len(gallery) > 0, 'No image to upscale'
    assert 0 <= gallery_index < len(gallery), f'Bad image index: {gallery_index}'

    p = txt2img_create_processing(id_task, request, *args, force_enable_hr=True)
    p.batch_size = 1
    p.n_iter = 1
    # txt2img_upscale attribute that signifies this is called by txt2img_upscale
    p.txt2img_upscale = True

    geninfo = json.loads(generation_info)

    image_info = gallery[gallery_index] if 0 <= gallery_index < len(gallery) else gallery[0]
    p.firstpass_image = infotext_utils.image_from_url_text(image_info)

    parameters = parse_generation_parameters(geninfo.get('infotexts')[gallery_index], [])
    p.seed = parameters.get('Seed', -1)
    p.subseed = parameters.get('Variation seed', -1)

    p.override_settings['save_images_before_highres_fix'] = False

    with closing(p):
        processed = modules.scripts.scripts_txt2img.run(p, *p.script_args)

        if processed is None:
            processed = processing.process_images(p)

    shared.total_tqdm.clear()

    new_gallery = []
    for i, image in enumerate(gallery):
        if i == gallery_index:
            geninfo["infotexts"][gallery_index: gallery_index+1] = processed.infotexts
            new_gallery.extend(processed.images)
        else:
            fake_image = Image.new(mode="RGB", size=(1, 1))
            fake_image.already_saved_as = image["name"].rsplit('?', 1)[0]
            new_gallery.append(fake_image)

    geninfo["infotexts"][gallery_index] = processed.info

    return new_gallery, json.dumps(geninfo), plaintext_to_html(processed.info), plaintext_to_html(processed.comments, classname="comments")


def txt2img(id_task: str, request: gr.Request, *args):
    p = txt2img_create_processing(id_task, request, *args)

    with closing(p):
        processed = modules.scripts.scripts_txt2img.run(p, *p.script_args)

        if processed is None:
            processed = processing.process_images(p)

    shared.total_tqdm.clear()

    generation_info_js = processed.js()
    if opts.samples_log_stdout:
        print(generation_info_js)

    if opts.do_not_show_images:
        processed.images = []

    return processed.images, generation_info_js, plaintext_to_html(processed.info), plaintext_to_html(processed.comments, classname="comments")
