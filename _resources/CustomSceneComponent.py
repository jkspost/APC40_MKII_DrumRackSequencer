from _Framework.SceneComponent import SceneComponent
from .CustomClipSlotComponent import CustomClipSlotComponent as ClipSlotComponent

class CustomSceneComponent(SceneComponent):

  clip_slot_component_type = ClipSlotComponent
  _delete_button = None

  def _create_clip_slot(self):
    return self.clip_slot_component_type()

  def set_select_only_mode(self, value):
    for clip_slot in self._clip_slots:
      clip_slot.set_select_only_mode(value)

  def set_step_sequencer_active(self, value):
    for clip_slot in self._clip_slots:
      clip_slot.set_step_sequencer_active(value)

