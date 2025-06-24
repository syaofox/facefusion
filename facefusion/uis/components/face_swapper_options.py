from typing import List, Optional, Tuple

import gradio

from facefusion import state_manager, wording
from facefusion.common_helper import get_first
from facefusion.processors import choices as processors_choices
from facefusion.processors.core import load_processor_module
from facefusion.processors.types import FaceSwapperModel
from facefusion.uis.core import get_ui_component, register_ui_component

FACE_SWAPPER_MODEL_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_SWAPPER_PIXEL_BOOST_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_SWAPPER_VR_MODE_CHECKBOX : Optional[gradio.Checkbox] = None
FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN : Optional[gradio.Dropdown] = None

def render() -> None:
	global FACE_SWAPPER_MODEL_DROPDOWN
	global FACE_SWAPPER_PIXEL_BOOST_DROPDOWN
	global FACE_SWAPPER_VR_MODE_CHECKBOX
	global FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN

	has_face_swapper = 'face_swapper' in state_manager.get_item('processors')
	FACE_SWAPPER_MODEL_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.face_swapper_model_dropdown'),
		choices = processors_choices.face_swapper_models,
		value = state_manager.get_item('face_swapper_model'),
		visible = has_face_swapper
	)
	FACE_SWAPPER_PIXEL_BOOST_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.face_swapper_pixel_boost_dropdown'),
		choices = processors_choices.face_swapper_set.get(state_manager.get_item('face_swapper_model')),
		value = state_manager.get_item('face_swapper_pixel_boost'),
		visible = has_face_swapper
	)

	FACE_SWAPPER_VR_MODE_CHECKBOX = gradio.Checkbox(
		label = wording.get('uis.face_swapper_vr_mode_checkbox'),
		value = state_manager.get_item('face_swapper_vr_mode'),
		visible = has_face_swapper
	)
	

	current_mode = state_manager.get_item('face_swapper_vr_mode_split')
	
	FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.face_swapper_vr_mode_split_dropdown'),
		choices = ['horizontal', 'vertical'],
		value = current_mode,
		visible = has_face_swapper and state_manager.get_item('face_swapper_vr_mode')
	)


	register_ui_component('face_swapper_model_dropdown', FACE_SWAPPER_MODEL_DROPDOWN)
	register_ui_component('face_swapper_pixel_boost_dropdown', FACE_SWAPPER_PIXEL_BOOST_DROPDOWN)
	register_ui_component('face_swapper_vr_mode_checkbox', FACE_SWAPPER_VR_MODE_CHECKBOX)
	register_ui_component('face_swapper_vr_mode_split_dropdown', FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN)


def listen() -> None:
	FACE_SWAPPER_MODEL_DROPDOWN.change(update_face_swapper_model, inputs = FACE_SWAPPER_MODEL_DROPDOWN, outputs = [ FACE_SWAPPER_MODEL_DROPDOWN, FACE_SWAPPER_PIXEL_BOOST_DROPDOWN ])
	FACE_SWAPPER_PIXEL_BOOST_DROPDOWN.change(update_face_swapper_pixel_boost, inputs = FACE_SWAPPER_PIXEL_BOOST_DROPDOWN)
	FACE_SWAPPER_VR_MODE_CHECKBOX.change(update_face_swapper_vr_mode, inputs = FACE_SWAPPER_VR_MODE_CHECKBOX, outputs = FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN)
	FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN.change(update_face_swapper_vr_mode_split, inputs = FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN)


	processors_checkbox_group = get_ui_component('processors_checkbox_group')
	if processors_checkbox_group:
		processors_checkbox_group.change(remote_update, inputs = processors_checkbox_group, outputs = [ FACE_SWAPPER_MODEL_DROPDOWN, FACE_SWAPPER_PIXEL_BOOST_DROPDOWN , FACE_SWAPPER_VR_MODE_CHECKBOX, FACE_SWAPPER_VR_MODE_SPLIT_DROPDOWN ])


def remote_update(processors : List[str]) -> Tuple[gradio.Dropdown, gradio.Dropdown, gradio.Checkbox, gradio.Dropdown]:
	has_face_swapper = 'face_swapper' in processors
	is_vr_mode = state_manager.get_item('face_swapper_vr_mode') if has_face_swapper else False
	return gradio.Dropdown(visible = has_face_swapper), gradio.Dropdown(visible = has_face_swapper), gradio.Checkbox(visible = has_face_swapper), gradio.Dropdown(visible = has_face_swapper and is_vr_mode)


def update_face_swapper_model(face_swapper_model : FaceSwapperModel) -> Tuple[gradio.Dropdown, gradio.Dropdown]:
	face_swapper_module = load_processor_module('face_swapper')
	face_swapper_module.clear_inference_pool()
	state_manager.set_item('face_swapper_model', face_swapper_model)

	if face_swapper_module.pre_check():
		face_swapper_pixel_boost_choices = processors_choices.face_swapper_set.get(state_manager.get_item('face_swapper_model'))
		state_manager.set_item('face_swapper_pixel_boost', get_first(face_swapper_pixel_boost_choices))
		return gradio.Dropdown(value = state_manager.get_item('face_swapper_model')), gradio.Dropdown(value = state_manager.get_item('face_swapper_pixel_boost'), choices = face_swapper_pixel_boost_choices)
	return gradio.Dropdown(), gradio.Dropdown()


def update_face_swapper_pixel_boost(face_swapper_pixel_boost : str) -> None:
	state_manager.set_item('face_swapper_pixel_boost', face_swapper_pixel_boost)



def update_face_swapper_vr_mode(face_swapper_vr_mode : bool) -> gradio.Dropdown:
	state_manager.set_item('face_swapper_vr_mode', face_swapper_vr_mode)
	return gradio.Dropdown(visible = face_swapper_vr_mode)


def update_face_swapper_vr_mode_split(face_swapper_vr_mode_split : str) -> None:
	state_manager.set_item('face_swapper_vr_mode_split', face_swapper_vr_mode_split)
