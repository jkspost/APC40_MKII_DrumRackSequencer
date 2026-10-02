#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APCJ40_MKII/MixerComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import chr
from builtins import filter
from future.moves.itertools import zip_longest
from _Framework.Control import RadioButtonControl, control_list
from _Framework.Dependency import depends
from _Framework.Util import nop
from _APC.MixerComponent import MixerComponent as MixerComponentBase, ChanStripComponent as ChannelStripComponentBase

MONITOR_STATE_COLORS = {0: u'Mixer.Crossfade.B',
 1: u'Mixer.Crossfade.A',
 2: u'Mixer.Crossfade.Off'}

class ChannelStripComponent(ChannelStripComponentBase):
    _monitor_button = None

    def _on_cf_assign_changed(self):
        if self.is_enabled() and self._crossfade_toggle:
            state = self._track.mixer_device.crossfade_assign if self._track else 1
            value_to_send = None
            if state == 0:
                value_to_send = u'Mixer.Crossfade.A'
            elif state == 1:
                value_to_send = u'Mixer.Crossfade.Off'
            elif state == 2:
                value_to_send = u'Mixer.Crossfade.B'
            self._crossfade_toggle.set_light(value_to_send)
        # This callback already fires whenever this strip's assigned track
        # changes (e.g. paging the mixer bank left/right), so piggyback on
        # it to refresh our monitor button's LED for the new track.
        self._update_monitor_led()

    def set_monitor_button(self, button):
        if self._monitor_button is not None and self._monitor_button.value_has_listener(self._monitor_button_value):
            self._monitor_button.remove_value_listener(self._monitor_button_value)
        self._monitor_button = button
        if button is not None:
            button.add_value_listener(self._monitor_button_value)
        self._update_monitor_led()

    def _monitor_button_value(self, value):
        if self.is_enabled() and value > 0 and self._track is not None:
            if self._track.can_be_armed:
                self._track.current_monitoring_state = (self._track.current_monitoring_state + 1) % 3
            self._update_monitor_led()

    def _update_monitor_led(self):
        if self._monitor_button is None:
            return
        track = self._track
        state = track.current_monitoring_state if track and track.can_be_armed else 1
        self._monitor_button.set_light(MONITOR_STATE_COLORS.get(state, u'Mixer.Crossfade.Off'))

    def disconnect(self):
        if self._monitor_button is not None:
            if self._monitor_button.value_has_listener(self._monitor_button_value):
                self._monitor_button.remove_value_listener(self._monitor_button_value)
            self._monitor_button = None
        super(ChannelStripComponent, self).disconnect()


def _set_channel(controls, channel):
    for control in filter(None, controls or []):
        control.set_channel(channel)


class MixerComponent(MixerComponentBase):
    send_select_buttons = control_list(RadioButtonControl)

    @depends(show_message=nop)
    def __init__(self, num_tracks = 0, show_message = nop, *a, **k):
        super(MixerComponent, self).__init__(num_tracks=num_tracks, *a, **k)
        self._show_message = show_message
        self.on_num_sends_changed()
        self._pan_controls = None
        self._send_controls = None
        self._user_controls = None

    def _create_strip(self):
        return ChannelStripComponent()

    @send_select_buttons.checked
    def send_select_buttons(self, button):
        self.send_index = button.index

    def on_num_sends_changed(self):
        self.send_select_buttons.control_count = self.num_sends

    def on_send_index_changed(self):
        if self.send_index is None:
            self.send_select_buttons.control_count = 0
        elif self.send_index < self.send_select_buttons.control_count:
            self.send_select_buttons[self.send_index].is_checked = True
        if self.is_enabled() and self._send_controls:
            self._show_controlled_sends_message()

    def _show_controlled_sends_message(self):
        if self._send_index is not None:
            send_name = chr(ord(u'A') + self._send_index)
            self._show_message(u'Controlling Send %s' % send_name)

    def set_pan_controls(self, controls):
        super(MixerComponent, self).set_pan_controls(controls)
        self._pan_controls = controls
        self._update_pan_controls()
        if self.is_enabled() and controls:
            self._show_message(u'Controlling Pans')

    def set_send_controls(self, controls):
        super(MixerComponent, self).set_send_controls(controls)
        self._send_controls = controls
        self._update_send_controls()
        if self.is_enabled() and controls:
            self._show_controlled_sends_message()

    def set_user_controls(self, controls):
        self._user_controls = controls
        self._update_user_controls()
        if self.is_enabled() and controls:
            self._show_message(u'Controlling User Mappings')

    def set_crossfade_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_crossfade_toggle(button)

    def set_monitor_buttons(self, buttons):
        for strip, button in zip_longest(self._channel_strips, buttons or []):
            strip.set_monitor_button(button)

    def _update_pan_controls(self):
        _set_channel(self._pan_controls, 0)

    def _update_send_controls(self):
        _set_channel(self._send_controls, 1)

    def _update_user_controls(self):
        _set_channel(self._user_controls, 2)

    def update(self):
        super(MixerComponent, self).update()
        if self.is_enabled():
            self._update_pan_controls()
            self._update_send_controls()
            self._update_user_controls()
