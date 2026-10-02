from __future__ import absolute_import, print_function, unicode_literals
import time
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group

DRUM_ROWS = 3
DRUM_COLS = 4
DRUM_BASE_NOTE = 36
DOUBLE_TAP_SECONDS = 0.4
MIN_BASE_NOTE = 0
MAX_BASE_NOTE = 128 - DRUM_ROWS * DRUM_COLS

COLOR_OFF = 0
COLOR_LOADED = 46

COLOR_SELECTED = 46

COLOR_COPY_PULSE = 5

COLOR_PAGE_NAV = 40

COLOR_PAGE_NAV_SHIFT = 96

COLOR_BUTTON_FLASH = 3

PAGE_NAV_FLASH_SECONDS = 0.15

COLOR_AUDITION_OFF = COLOR_LOADED
COLOR_AUDITION_ON = 45

COLOR_AUDITION_NO_QUANT_ON = 37

COLOR_MUTED = 7

SELECTION_PULSE_REFRESH_SECONDS = 0.3

SELECTION_PULSE_SETTLE_SECONDS = 1.5

class DrumPadComponent(ControlSurfaceComponent):

    num_rows = DRUM_ROWS
    num_cols = DRUM_COLS
    base_note = DRUM_BASE_NOTE
    min_base_note = MIN_BASE_NOTE
    max_base_note = MAX_BASE_NOTE
    double_tap_seconds = DOUBLE_TAP_SECONDS

    def __init__(self, matrix_rows, on_pad_selected=None, shift_button=None, notes_on_page_callback=None, nudge_up_button=None, nudge_down_button=None, on_pad_copy_page=None, on_pad_paste_page=None, on_pad_delete_page=None, on_pad_delete_all_pages=None, pulse_led_rows=None, on_pulsing_pad_tapped=None, page_up_button=None, page_down_button=None, audition_toggle_button=None, on_audition_toggled=None, on_audition_shift_changed=None, on_pad_held=None, on_pad_released=None, track_provider=None, shift_pressed_provider=None, show_message_callback=None, on_scroll_pages=None, *a, **k):
        super(DrumPadComponent, self).__init__(*a, **k)
        assert len(matrix_rows) == self.num_rows
        self._matrix_rows = matrix_rows
        self._on_pad_selected = on_pad_selected
        self._shift_button = shift_button

        self._shift_pressed = False

        self._shift_pressed_provider = shift_pressed_provider
        self._show_message_callback = show_message_callback
        self._on_scroll_pages = on_scroll_pages
        self._notes_on_page_callback = notes_on_page_callback
        self._nudge_up_button = nudge_up_button
        self._nudge_down_button = nudge_down_button
        self._on_pad_copy_page = on_pad_copy_page
        self._on_pad_paste_page = on_pad_paste_page
        self._on_pad_delete_page = on_pad_delete_page
        self._on_pad_delete_all_pages = on_pad_delete_all_pages
        self._last_nudge_delete_tap_note = None
        self._last_nudge_delete_tap_time = None
        self._on_pulsing_pad_tapped = on_pulsing_pad_tapped
        self._pulsing_note = None
        self._pulse_led_positions = {}
        self._page_up_button = page_up_button
        self._page_down_button = page_down_button

        self._page_nav_flash_start_times = {}
        self._base_note = self.base_note
        self._audition_toggle_button = audition_toggle_button
        self._on_audition_toggled = on_audition_toggled
        self._on_audition_shift_changed = on_audition_shift_changed
        self._audition_active = False

        self._audition_no_quant_active = False

        self._saved_midi_recording_quantization = None
        self._on_pad_held = on_pad_held
        self._on_pad_released = on_pad_released

        self._track_provider = track_provider
        self._held_plain_notes = set()
        self._active = False
        self._selected_note = None
        self._selected_note_base_note = None
        self._selection_pulse_last_forced_time = None
        self._selection_pulse_settle_deadline = None
        self._button_positions = {}
        self._pulse_led_rows = pulse_led_rows
        flat_buttons = []
        for row_index, row in enumerate(matrix_rows):
            assert len(row) == self.num_cols
            for col_index, button in enumerate(row):
                self._button_positions[button] = self._note_for_position(row_index, col_index)
                flat_buttons.append(button)
        if pulse_led_rows:
            assert len(pulse_led_rows) == self.num_rows
            for row_index, row in enumerate(pulse_led_rows):
                assert len(row) == self.num_cols
                for col_index, pulse_led in enumerate(row):
                    self._pulse_led_positions[self._note_for_position(row_index, col_index)] = pulse_led
        self._on_pad_button_value.replace_subjects(flat_buttons)
        self._on_page_up_button_value.subject = self._page_up_button
        self._on_page_down_button_value.subject = self._page_down_button
        self._on_audition_toggle_button_value.subject = self._audition_toggle_button
        self._on_shift_button_value.subject = self._shift_button

    def _note_for_position(self, row_index, col_index):
        relative_row_from_bottom = self.num_rows - 1 - row_index
        return self._base_note + relative_row_from_bottom * self.num_cols + col_index

    def set_active(self, active):

        if self._active != active:
            self._active = active
            if active:

                self._start_selection_pulse(self._selected_note, context=u'set_active')
                self.update_pads()
                self._render_page_nav_buttons()
                self._render_audition_button()
                if self._audition_active:
                    self._sync_drum_rack_scroll_position()
                    if self._on_audition_toggled is not None:
                        try:
                            self._on_audition_toggled(True)
                        except Exception:
                            pass
                    if self._audition_no_quant_active:
                        self._force_no_record_quantization()
            else:
                self._pulsing_note = None
                self._last_nudge_delete_tap_note = None
                self._last_nudge_delete_tap_time = None
                self._held_plain_notes = set()
                if self._audition_active:
                    if self._on_audition_toggled is not None:
                        try:
                            self._on_audition_toggled(False)
                        except Exception:
                            pass
                    if self._audition_no_quant_active:
                        self._restore_record_quantization()
                self._clear_lights()

    def set_selected_note(self, note):
        if note == self._selected_note:
            return
        previous_note = self._selected_note
        if previous_note is not None and previous_note != self._pulsing_note and self._active:

            previous_button = self._button_for_note(previous_note)
            if previous_button is not None:
                device = self._drum_rack_device()
                pitches_with_notes = self._pitches_with_notes_on_page()
                color_fn = self._audition_pad_color if self._audition_active else self._normal_pad_color
                try:
                    previous_button.send_value(color_fn(device, previous_note, pitches_with_notes), force=True)
                except Exception:
                    pass
        self._selected_note = note
        self._selected_note_base_note = self._base_note
        self._start_selection_pulse(note, context=u'set_selected_note')
        if self._active:
            self.update_pads()

    def _button_for_note(self, note):
        for button, button_note in self._button_positions.items():
            if button_note == note:
                return button
        return None

    def _start_selection_pulse(self, note, context=u'unknown'):

        if note is None or note == self._pulsing_note or not self._active or self._selected_note_base_note != self._base_note:
            return
        button = self._button_for_note(note)
        pulse_led = self._pulse_led_positions.get(note)
        device = self._drum_rack_device()
        muted = device is not None and self._pad_is_muted(device, note)
        if muted:
            primary_color = COLOR_OFF
            pulse_color = COLOR_MUTED
        else:
            primary_color = COLOR_AUDITION_ON if self._audition_active else COLOR_SELECTED
            pulse_color = COLOR_BUTTON_FLASH
        if button is not None:
            try:
                button.send_value(primary_color, force=True)
            except Exception:
                pass
        if pulse_led is not None:
            try:
                pulse_led.send_value(pulse_color, force=True)
                now = time.time()
                self._selection_pulse_last_forced_time = now

                if context != u'periodic_refresh':
                    self._selection_pulse_settle_deadline = now + SELECTION_PULSE_SETTLE_SECONDS
            except Exception:
                pass

    def _drum_rack_device(self):

        if self._track_provider is not None:
            try:
                track = self._track_provider()
            except Exception:
                track = None
        else:
            track = self.song().view.selected_track
        if track is None:
            return None
        selected_device = track.view.selected_device
        if selected_device is not None and getattr(selected_device, 'can_have_drum_pads', False):
            return selected_device
        for device in track.devices:
            if getattr(device, 'can_have_drum_pads', False):
                return device
        return None

    def _selected_pad_chain(self):

        if self._selected_note is None:
            return None
        device = self._drum_rack_device()
        if device is None:
            return None
        try:
            pad = device.drum_pads[self._selected_note]
        except Exception:
            return None
        if pad is None:
            return None
        try:
            chains = pad.chains
        except Exception:
            return None
        if not chains:
            return None
        return chains[0]

    def selected_pad_volume_parameter(self):

        chain = self._selected_pad_chain()
        if chain is None:
            return None
        return chain.mixer_device.volume

    def selected_pad_pan_parameter(self):

        chain = self._selected_pad_chain()
        if chain is None:
            return None
        return chain.mixer_device.panning

    @subject_slot_group(u'value')
    def _on_pad_button_value(self, value, button):
        if not self._active:
            return
        note = self._button_positions.get(button)
        if note is None:
            return
        if not value:

            if note in self._held_plain_notes:
                self._held_plain_notes.discard(note)
                if self._on_pad_released is not None:
                    try:
                        self._on_pad_released(note)
                    except Exception:
                        pass
            return
        if self._nudge_up_button is not None and self._nudge_up_button.is_pressed():
            if self._on_pad_copy_page is not None:
                self._on_pad_copy_page(note)
            return
        if self._shift_button is not None and self._shift_button.is_pressed():

            self._toggle_pad_mute(note)
            return
        if self._nudge_down_button is not None and self._nudge_down_button.is_pressed():
            now = time.time()
            if self._last_nudge_delete_tap_note == note and self._last_nudge_delete_tap_time is not None and now - self._last_nudge_delete_tap_time <= self.double_tap_seconds:
                self._last_nudge_delete_tap_note = None
                self._last_nudge_delete_tap_time = None
                if self._on_pad_delete_all_pages is not None:
                    self._on_pad_delete_all_pages(note)
            else:
                self._last_nudge_delete_tap_note = note
                self._last_nudge_delete_tap_time = now
                if self._on_pad_delete_page is not None:
                    self._on_pad_delete_page(note)
            return
        if note == self._pulsing_note:

            if self._on_pulsing_pad_tapped is not None:
                self._on_pulsing_pad_tapped(note)
            return
        if self._pulsing_note is not None:

            if self._on_pad_paste_page is not None:
                self._on_pad_paste_page(note)
            return

        device = self._drum_rack_device()
        if device is not None:
            try:
                pad = device.drum_pads[note]
                device.view.selected_drum_pad = pad
            except Exception:
                pass
        if self._on_pad_selected is not None:
            self._on_pad_selected(note)
        self._held_plain_notes.add(note)
        if self._on_pad_held is not None:
            try:
                self._on_pad_held(note)
            except Exception:
                pass

    @subject_slot(u'value')
    def _on_page_up_button_value(self, value):

        if not self._active or not value:
            return
        shift_held = self._shift_pressed_provider is not None and bool(self._shift_pressed_provider())
        if shift_held:
            if self._on_scroll_pages is not None:
                try:
                    self._on_scroll_pages(-1)
                except Exception:
                    pass
            self._start_page_nav_flash(self._page_up_button)
            return
        self._shift_page(self.num_rows * self.num_cols)
        self._start_page_nav_flash(self._page_up_button)

    @subject_slot(u'value')
    def _on_page_down_button_value(self, value):

        if not self._active or not value:
            return
        shift_held = self._shift_pressed_provider is not None and bool(self._shift_pressed_provider())
        if shift_held:
            if self._on_scroll_pages is not None:
                try:
                    self._on_scroll_pages(1)
                except Exception:
                    pass
            self._start_page_nav_flash(self._page_down_button)
            return
        self._shift_page(-(self.num_rows * self.num_cols))
        self._start_page_nav_flash(self._page_down_button)

    def _start_page_nav_flash(self, button):

        if button is None:
            return
        try:
            button.send_value(COLOR_BUTTON_FLASH, force=True)
        except Exception:
            return
        self._page_nav_flash_start_times[button] = time.time()

    @subject_slot(u'value')
    def _on_audition_toggle_button_value(self, value):

        if not self._active or not value:
            return
        if self._shift_pressed_provider is not None:
            try:
                shift_held = bool(self._shift_pressed_provider())
            except Exception:
                shift_held = False
        else:
            shift_held = self._shift_pressed
        if shift_held:
            if self._audition_active and self._audition_no_quant_active:
                self._audition_active = False
                self._audition_no_quant_active = False
                self._restore_record_quantization()
            else:
                self._audition_active = True
                self._audition_no_quant_active = True
                self._force_no_record_quantization()
        else:
            was_no_quant = self._audition_no_quant_active
            self._audition_active = not self._audition_active
            self._audition_no_quant_active = False
            if was_no_quant:
                self._restore_record_quantization()
        if self._audition_active:

            self._sync_drum_rack_scroll_position()
        if self._on_audition_toggled is not None:
            try:
                self._on_audition_toggled(self._audition_active)
            except Exception:
                pass

        self._start_selection_pulse(self._selected_note, context=u'audition_on' if self._audition_active else u'audition_off')
        self._render_audition_button()
        self.update_pads()

    def _force_no_record_quantization(self):

        try:
            if self._saved_midi_recording_quantization is None:
                self._saved_midi_recording_quantization = self.song().midi_recording_quantization
            self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
            if self._show_message_callback is not None:
                self._show_message_callback(u'Audition: record quantization off')
        except Exception:
            pass

    def _restore_record_quantization(self):

        if self._saved_midi_recording_quantization is not None:
            try:
                self.song().midi_recording_quantization = self._saved_midi_recording_quantization
                if self._show_message_callback is not None:
                    self._show_message_callback(u'Audition: record quantization restored')
            except Exception:
                pass
        self._saved_midi_recording_quantization = None

    @subject_slot(u'value')
    def _on_shift_button_value(self, value):

        self._shift_pressed = bool(value)
        if not self._active or not self._audition_active:
            return
        if self._on_audition_shift_changed is not None:
            try:
                self._on_audition_shift_changed(bool(value))
            except Exception:
                pass

    def is_audition_no_quant_active(self):

        return self._audition_no_quant_active

    def refresh_audition_button(self):

        if self._active:
            self._render_audition_button()

    def _render_audition_button(self):

        if self._audition_toggle_button is not None:
            if self._audition_active and self._audition_no_quant_active:
                color = COLOR_AUDITION_NO_QUANT_ON
            elif self._audition_active:
                color = COLOR_AUDITION_ON
            else:
                color = COLOR_AUDITION_OFF
            self._audition_toggle_button.send_value(color, force=True)

    def _shift_page(self, delta):
        new_base_note = max(self.min_base_note, min(self.max_base_note, self._base_note + delta))
        if new_base_note != self._base_note:

            device = self._drum_rack_device()
            pitches_with_notes = self._pitches_with_notes_on_page()
            color_fn = self._audition_pad_color if self._audition_active else self._normal_pad_color
            for button, note in self._button_positions.items():
                if note == self._pulsing_note:

                    continue
                try:
                    button.send_value(color_fn(device, note, pitches_with_notes), force=True)
                except Exception:
                    pass
            self._base_note = new_base_note
            self._button_positions = {}
            for row_index, row in enumerate(self._matrix_rows):
                for col_index, button in enumerate(row):
                    self._button_positions[button] = self._note_for_position(row_index, col_index)
            if self._pulse_led_rows:

                self._pulse_led_positions = {}
                for row_index, row in enumerate(self._pulse_led_rows):
                    for col_index, pulse_led in enumerate(row):
                        self._pulse_led_positions[self._note_for_position(row_index, col_index)] = pulse_led

            self._start_selection_pulse(self._selected_note, context=u'shift_page')
            self._sync_drum_rack_scroll_position()
            if self._audition_active and self._on_audition_toggled is not None:

                try:
                    self._on_audition_toggled(True)
                except Exception:
                    pass
            elif self._active:
                self.update_pads()
        self._render_page_nav_buttons()

    def _sync_drum_rack_scroll_position(self):

        device = self._drum_rack_device()
        if device is None:
            return
        try:
            device.view.drum_pads_scroll_position = self._base_note // self.num_cols
        except Exception:
            pass

    def refresh_page_nav_buttons(self):

        if self._active:
            self._render_page_nav_buttons()

    def _render_page_nav_buttons(self):

        shift_held = self._shift_pressed_provider is not None and bool(self._shift_pressed_provider())
        if self._page_up_button is not None and self._page_up_button not in self._page_nav_flash_start_times:
            if shift_held:
                color = COLOR_PAGE_NAV_SHIFT
            else:
                can_go_up = self._base_note + self.num_rows * self.num_cols <= self.max_base_note
                color = COLOR_PAGE_NAV if can_go_up else COLOR_OFF
            self._page_up_button.send_value(color, force=True)
        if self._page_down_button is not None and self._page_down_button not in self._page_nav_flash_start_times:
            if shift_held:
                color = COLOR_PAGE_NAV_SHIFT
            else:
                can_go_down = self._base_note - self.num_rows * self.num_cols >= self.min_base_note
                color = COLOR_PAGE_NAV if can_go_down else COLOR_OFF
            self._page_down_button.send_value(color, force=True)

    def refresh_page_nav_flash(self):

        if not self._active:
            return
        now = time.time()
        any_expired = False
        for button in list(self._page_nav_flash_start_times.keys()):
            if now - self._page_nav_flash_start_times[button] < PAGE_NAV_FLASH_SECONDS:
                continue
            del self._page_nav_flash_start_times[button]
            any_expired = True
        if any_expired:
            self._render_page_nav_buttons()

    def _normal_pad_color(self, device, note, pitches_with_notes):

        if device is not None and self._pad_is_muted(device, note):
            return COLOR_MUTED
        elif note in pitches_with_notes:
            return COLOR_AUDITION_ON
        elif device is not None and self._pad_has_content(device, note):
            return COLOR_LOADED
        else:
            return COLOR_OFF

    def _audition_pad_color(self, device, note, pitches_with_notes):

        if device is not None and self._pad_is_muted(device, note):
            return COLOR_MUTED
        elif note in pitches_with_notes:
            return COLOR_LOADED
        elif device is not None and self._pad_has_content(device, note):
            return COLOR_AUDITION_ON
        else:
            return COLOR_OFF

    def update_pads(self):
        if not self._active:
            return
        device = self._drum_rack_device()
        pitches_with_notes = self._pitches_with_notes_on_page()
        if self._audition_active:
            for row_index in range(self.num_rows):
                for col_index in range(self.num_cols):
                    note = self._note_for_position(row_index, col_index)
                    if note == self._pulsing_note or note == self._selected_note:

                        continue
                    button = self._matrix_rows[row_index][col_index]

                    if device is not None and self._pad_is_muted(device, note):
                        button.send_value(COLOR_MUTED, force=True)
                    elif note in pitches_with_notes:
                        button.send_value(COLOR_LOADED, force=True)
                    elif device is not None and self._pad_has_content(device, note):
                        button.send_value(COLOR_AUDITION_ON, force=True)
                    else:
                        button.send_value(COLOR_OFF, force=True)
        else:
            for row_index in range(self.num_rows):
                for col_index in range(self.num_cols):
                    note = self._note_for_position(row_index, col_index)
                    if note == self._pulsing_note or note == self._selected_note:

                        continue
                    button = self._matrix_rows[row_index][col_index]
                    button.send_value(self._normal_pad_color(device, note, pitches_with_notes))

        if (self._selected_note is not None and self._selected_note != self._pulsing_note
                and self._selection_pulse_settle_deadline is not None):
            now = time.time()
            if (now < self._selection_pulse_settle_deadline
                    and (self._selection_pulse_last_forced_time is None or now - self._selection_pulse_last_forced_time >= SELECTION_PULSE_REFRESH_SECONDS)):
                self._start_selection_pulse(self._selected_note, context=u'periodic_refresh')

    def start_pulsing_pad(self, note):
        self.stop_pulsing_pad()
        self._pulsing_note = note
        pulse_led = self._pulse_led_positions.get(note)
        if pulse_led is not None and self._active:
            try:
                pulse_led.send_value(COLOR_COPY_PULSE, force=True)
            except Exception:
                pass

    def stop_pulsing_pad(self):

        if self._pulsing_note is not None:
            stopped_note = self._pulsing_note
            self._pulsing_note = None
            if self._active:
                device = self._drum_rack_device()
                pitches_with_notes = self._pitches_with_notes_on_page()
                color_fn = self._audition_pad_color if self._audition_active else self._normal_pad_color
                for row_index, row in enumerate(self._matrix_rows):
                    for col_index, button in enumerate(row):
                        if self._note_for_position(row_index, col_index) == stopped_note:
                            try:
                                button.send_value(color_fn(device, stopped_note, pitches_with_notes), force=True)
                            except Exception:
                                pass
                            break
                if stopped_note == self._selected_note:
                    self._start_selection_pulse(stopped_note, context=u'copy_pulse_stopped')
                self.update_pads()

    def _pitches_with_notes_on_page(self):
        if self._notes_on_page_callback is None:
            return set()
        try:
            return self._notes_on_page_callback(self._base_note, self.num_rows * self.num_cols)
        except Exception:
            return set()

    def _pad_has_content(self, device, note):
        try:
            pad = device.drum_pads[note]
        except Exception:
            return False
        return pad is not None and len(pad.chains) > 0

    def _pad_is_muted(self, device, note):
        try:
            pad = device.drum_pads[note]
        except Exception:
            return False
        if pad is None:
            return False
        try:
            return bool(pad.mute)
        except Exception:
            return False

    def _toggle_pad_mute(self, note):

        device = self._drum_rack_device()
        if device is None:
            return
        try:
            pad = device.drum_pads[note]
        except Exception:
            return
        if pad is None:
            return
        try:
            pad.mute = not pad.mute
        except Exception:
            return
        self.update_pads()
        if note == self._selected_note:
            self._start_selection_pulse(note, context=u'mute_toggled')

    def _clear_lights(self):
        for row in self._matrix_rows:
            for button in row:

                button.send_value(COLOR_OFF, force=True)

        if self._page_up_button is not None:
            self._page_up_button.send_value(COLOR_OFF, force=True)
        if self._page_down_button is not None:
            self._page_down_button.send_value(COLOR_OFF, force=True)
        if self._audition_toggle_button is not None:
            self._audition_toggle_button.send_value(COLOR_OFF, force=True)
