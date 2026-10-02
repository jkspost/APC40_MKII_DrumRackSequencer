from __future__ import absolute_import, print_function, unicode_literals
import math
import random
import time
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _APC.RingedEncoderElement import RING_OFF_VALUE, RING_VOL_VALUE, RING_SIN_VALUE, RING_PAN_VALUE

NUM_ROWS = 2
STEPS_PER_ROW = 8
STEPS_PER_PAGE = NUM_ROWS * STEPS_PER_ROW
NUM_PAGES = 8
TOTAL_STEPS = STEPS_PER_PAGE * NUM_PAGES
STEP_LENGTH = 0.25

STEP_RESOLUTIONS = (0.125, 1.0, 0.5, 0.25)
STEP_RESOLUTION_LABELS = (u'1/32', u'1/4', u'1/8', u'1/16')

TRIPLET_MULTIPLIER = 2.0 / 3.0
PITCH = 36
DEFAULT_VELOCITY = 100
MIN_VELOCITY = 1
MAX_VELOCITY = 127
DEFAULT_CHANCE = 127
MIN_CHANCE = 0
MAX_CHANCE = 127
DEFAULT_VELOCITY_DEVIATION = 0

MIN_VELOCITY_DEVIATION = 0
MAX_VELOCITY_DEVIATION = 127

DEFAULT_SWING = 0
MIN_SWING = 0
MAX_SWING = 127
MAX_SWING_DELAY_FRACTION = 1.0 / 3.0
DEFAULT_TIMING = 64
MIN_TIMING = 0
MAX_TIMING = 127
MAX_TIMING_DELAY_FRACTION = 0.10
TIMING_CENTER = 63.5
DEFAULT_HUMANIZE = 0
MIN_HUMANIZE = 0
MAX_HUMANIZE = 127

MAX_HUMANIZE_DELAY_FRACTION = 0.16
MAX_ACCENT_SPACING = 16

ACCENT_KNOB_MIDPOINT = 64

MAX_ACCENT_GROUP_SIZE = 8

ACCENT_TIER_PERCENT = 0.30

DEFAULT_VELOCITY_HUMANIZE = 0
MIN_VELOCITY_HUMANIZE = 0
MAX_VELOCITY_HUMANIZE = 127

MAX_VELOCITY_HUMANIZE_SWING = 65

RAMP_KNOB_CENTER = 64

MAX_RAMP_VELOCITY_SWING = 60

REMOVE_TOLERANCE = 0.01
DURATION_GAP_EPSILON = 0.005
LONG_PRESS_SECONDS = 0.5

DOUBLE_TAP_SECONDS = 0.4
PULSE_REFRESH_SECONDS = 0.5

NUDGE_FLASH_SECONDS = 0.15

COLOR_BUTTON_FLASH = 3

COLOR_OFF = 0
COLOR_EMPTY_STEP = 1

COLOR_BAR_START = 2

COLOR_ACTIVE_FULL_CHANCE = 21

COLOR_ACTIVE_PARTIAL_CHANCE = 22

COLOR_PLAYHEAD = 13

COLOR_HELD_STEP_PULSE = COLOR_ACTIVE_FULL_CHANCE

COLOR_FOLLOW_OFF = 127

COLOR_FOLLOW_ON = 13

COLOR_PAGE_BASE = COLOR_FOLLOW_OFF

COLOR_PAGE_LOOP = COLOR_FOLLOW_ON

COLOR_COPY_PULSE = 5

COLOR_PAGE_PULSE = 3

COLOR_NUDGE_STEP = 40

RHYTHM_PRESETS = (
    (u'Four on the floor', (0, 4, 8, 12)),
    (u'Offbeat hi-hat', (2, 6, 10, 14)),
    (u'Backbeat (snare 2 & 4)', (4, 12)),
    (u'Son clave (3-2)', (0, 3, 6, 10, 12)),
    (u'Son clave (2-3)', (2, 4, 8, 11, 14)),
    (u'Rumba clave (3-2)', (0, 3, 7, 10, 12)),
    (u'Rumba clave (2-3)', (2, 4, 8, 11, 15)),
    (u'Tresillo (3-3-2)', (0, 3, 6, 8, 11, 14)),
    (u'Baion', (0, 3, 6, 8)),
    (u'Habanera', (0, 3, 4, 6, 8, 11, 12, 14)),
    (u'Cascara', (0, 2, 4, 6, 7, 10, 12, 14)),
    (u'Dembow / reggaeton kick', (0, 3, 6, 8, 11)),
    (u'Trap hi-hat roll', (0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13)),
    (u'Samba (surdo bass)', (4, 8, 14)),
    (u'2-step / UK garage', (3, 7, 11, 15)),
    (u'Afro 6/8 feel (approximated)', (0, 3, 6, 8, 11, 13)),
)

COLOR_RHYTHM_CATEGORY_LATIN = 101

COLOR_RHYTHM_CATEGORY_WORLD = 37
COLOR_RHYTHM_CATEGORY_ELECTRONIC = 110

RHYTHM_PRESETS_LATIN = (
    RHYTHM_PRESETS[3], RHYTHM_PRESETS[4], RHYTHM_PRESETS[5], RHYTHM_PRESETS[6],
    RHYTHM_PRESETS[7], RHYTHM_PRESETS[8], RHYTHM_PRESETS[9], RHYTHM_PRESETS[10],
    RHYTHM_PRESETS[13],
    (u'Songo', (0, 3, 6, 10, 12, 14)),
    (u'Guaracha', (0, 2, 3, 6, 8, 10, 11, 14)),

    (u'Mozambique (simplified)', (0, 2, 4, 6, 8, 11, 12, 14)),

    (u'Cha cha cha (guiro)', (0, 4, 6, 8, 12, 14)),
    (u'Merengue (steady pulse)', (0, 2, 4, 6, 8, 10, 12, 14)),

    (u'Bossa nova (common variant)', (0, 3, 6, 10, 13)),
    (u'Bolero', (0, 3, 6, 8, 10, 12)),
)

RHYTHM_PRESETS_WORLD = (
    RHYTHM_PRESETS[15],
    (u'West African bell', (0, 3, 5, 7, 9, 12, 15)),

    (u'Maqsum', (0, 3, 6, 8, 12)),

    (u'Teental (dha strokes)', (0, 3, 4, 7, 8, 15)),

    (u'Bulerias (12-beat, scaled)', (0, 3, 7, 9, 12, 15)),

    (u'Balkan 7/8 feel (approximated)', (0, 3, 6, 9, 11, 14)),
    (u'Taiko-style (sparse accents)', (0, 6, 8, 14)),
    (u'Klezmer-style', (0, 3, 4, 8, 11, 12)),

    (u'Irish jig-style (approximated)', (0, 3, 6, 9, 10, 13)),
)

RHYTHM_PRESETS_ELECTRONIC = (
    RHYTHM_PRESETS[0], RHYTHM_PRESETS[1], RHYTHM_PRESETS[2],
    RHYTHM_PRESETS[11], RHYTHM_PRESETS[12], RHYTHM_PRESETS[14],
    (u'Boom bap', (0, 6, 10, 14)),
    (u'Drum & bass / jungle break', (0, 4, 6, 10, 12)),
    (u'Dubstep half-time', (0, 8, 10)),
    (u'Acid house 16th roll', (0, 2, 4, 6, 9, 11, 13, 15)),
    (u'IDM / glitch-style', (0, 1, 4, 5, 9, 10, 13)),
    (u'UK garage 4x4 variant', (0, 4, 7, 8, 12, 15)),
    (u'Breakbeat / Amen-inspired', (0, 4, 10, 12, 14)),
    (u'Deep house shuffle', (2, 5, 8, 11, 14)),
)

RHYTHM_PRESET_CATEGORIES = (
    (u'Latin/Afro-Cuban', COLOR_RHYTHM_CATEGORY_LATIN, RHYTHM_PRESETS_LATIN),
    (u'World/Traditional', COLOR_RHYTHM_CATEGORY_WORLD, RHYTHM_PRESETS_WORLD),
    (u'Electronic/Modern', COLOR_RHYTHM_CATEGORY_ELECTRONIC, RHYTHM_PRESETS_ELECTRONIC),
)

RHYTHM_OFF_THRESHOLD = 8

FILL_OFF_THRESHOLD = 8

FILL_KNOB_MIDPOINT = FILL_OFF_THRESHOLD + (128 - FILL_OFF_THRESHOLD) // 2

FILL_LENGTH_SHORT = 4

FILL_LENGTH_LONG = 8

FILL_LENGTH_1_5BAR = 12

FILL_LENGTH_2BAR = 16

COLOR_FILL_CATEGORY_ROLLS = 34

COLOR_FILL_CATEGORY_SYNCOPATED = 89

COLOR_FILL_CATEGORY_GLITCH = 50

FILLS_ROLLS_SHORT = (
    (u'Single hit', (0,)),
    (u'Late hit', (3,)),
    (u'Two-hit build', (0, 2)),
    (u'Push pair', (1, 3)),
    (u'Last-two roll', (2, 3)),
    (u'Bookend accents', (0, 3)),
    (u'Three-hit build', (0, 1, 2)),
    (u'Dotted build', (0, 2, 3)),
    (u'Offbeat build', (1, 2, 3)),
    (u'Straight roll', (0, 1, 2, 3)),
)
FILLS_ROLLS_LONG = (
    (u'Single late hit', (6,)),
    (u'Two-hit call', (0, 4)),
    (u'Triplet-feel build', (0, 3, 6)),
    (u'Last-beat roll', (4, 5, 6, 7)),
    (u'Half-time then roll', (0, 4, 5, 6, 7)),
    (u'Classic snare build', (0, 2, 4, 6, 7)),
    (u'Accent pyramid', (0, 3, 5, 6, 7)),
    (u'Gradual roll', (0, 2, 4, 5, 6, 7)),
    (u'Double-time build', (0, 1, 2, 3, 4, 6)),
    (u'Full roll', (0, 1, 2, 3, 4, 5, 6, 7)),
)

FILLS_SYNCOPATED_SHORT = (
    (u'Sparse syncop', (2,)),
    (u'Skip-beat', (1, 3)),
    (u'Front-loaded', (0, 1)),
    (u'Pocket fill', (1, 2)),
    (u'Ghost accent', (0, 3)),
    (u'Ghost-note roll', (0, 1, 3)),
    (u'Syncopated triple', (0, 2, 3)),
    (u'Swung pair', (1, 2, 3)),
    (u'Full syncop', (0, 1, 2, 3)),
)
FILLS_SYNCOPATED_LONG = (
    (u'Late accent', (5,)),
    (u'Call & response', (1, 6)),
    (u'Loose triplet', (0, 3, 5)),
    (u'Ghost groove', (0, 3, 5, 7)),
    (u'Pocket roll', (2, 3, 6, 7)),
    (u'Swung build', (0, 3, 4, 7)),
    (u'Backbeat ghost', (1, 3, 5, 7)),
    (u'Triplet groove', (0, 2, 5, 7)),
    (u'Syncop cascade', (0, 2, 3, 5, 7)),
    (u'Off-kilter build', (1, 2, 4, 6, 7)),
)

FILLS_GLITCH_SHORT = (
    (u'Single chop', (0,)),
    (u'Chop pair', (0, 1)),
    (u'Stutter gap', (0, 4, 8)),
    (u'Chop cascade', (0, 1, 6, 7)),
    (u'Split stutter', (0, 1, 10, 11)),
    (u'Skip-chop climb', (0, 1, 4, 7, 10)),
    (u'Stutter climb', (0, 1, 2, 6, 7, 8)),
    (u'Glitch pyramid', (0, 1, 2, 3, 8, 9, 10)),
    (u'Dense stutter', (0, 1, 2, 3, 4, 5, 6, 7)),
    (u'Full micro-chop', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)),
)

FILLS_GLITCH_LONG = (
    (u'Single late hit', (14,)),
    (u'Call across bars', (0, 8)),
    (u'Sparse pulse', (0, 8, 12)),
    (u'Building chop', (8, 10, 12, 14)),
    (u'Second-bar cascade', (8, 9, 10, 12, 14)),
    (u'Glitch build', (0, 4, 8, 10, 12, 14)),
    (u'Stutter explosion', (8, 9, 10, 11, 12, 13, 14, 15)),
    (u'Two-bar climb', (0, 4, 8, 9, 10, 11, 12, 13, 14, 15)),
    (u'Escalating chaos', (0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15)),
    (u'Full two-bar chop', (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)),
)

FILL_BANK_CATEGORIES = (
    (u'Rolls & Builds', COLOR_FILL_CATEGORY_ROLLS, FILLS_ROLLS_SHORT, FILLS_ROLLS_LONG, 0.5, 1.0, FILL_LENGTH_SHORT, FILL_LENGTH_LONG),
    (u'Syncopated & Groove', COLOR_FILL_CATEGORY_SYNCOPATED, FILLS_SYNCOPATED_SHORT, FILLS_SYNCOPATED_LONG, 0.5, 1.0, FILL_LENGTH_SHORT, FILL_LENGTH_LONG),
    (u'Glitch & Stutter', COLOR_FILL_CATEGORY_GLITCH, FILLS_GLITCH_SHORT, FILLS_GLITCH_LONG, 1.5, 2.0, FILL_LENGTH_1_5BAR, FILL_LENGTH_2BAR),
)

def _bjorklund_pattern(hits, steps):

    if steps <= 0:
        return []
    if hits <= 0:
        return [False] * steps
    if hits >= steps:
        return [True] * steps
    pattern = []
    counts = []
    remainders = []
    divisor = steps - hits
    remainders.append(hits)
    level = 0
    while remainders[level] > 1:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level += 1
    counts.append(divisor)

    def build(level):
        if level == -1:
            pattern.append(False)
        elif level == -2:
            pattern.append(True)
        else:
            for _ in range(counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(True)
    return pattern[i:] + pattern[:i]

class StepSequencerComponent(ControlSurfaceComponent):

    num_rows = NUM_ROWS
    steps_per_row = STEPS_PER_ROW
    steps_per_page = STEPS_PER_PAGE
    num_pages = NUM_PAGES
    total_steps = TOTAL_STEPS
    pitch = PITCH
    default_velocity = DEFAULT_VELOCITY
    min_velocity = MIN_VELOCITY
    max_velocity = MAX_VELOCITY
    default_chance = DEFAULT_CHANCE
    min_chance = MIN_CHANCE
    max_chance = MAX_CHANCE
    default_velocity_deviation = DEFAULT_VELOCITY_DEVIATION
    min_velocity_deviation = MIN_VELOCITY_DEVIATION
    max_velocity_deviation = MAX_VELOCITY_DEVIATION
    default_swing = DEFAULT_SWING
    min_swing = MIN_SWING
    max_swing = MAX_SWING
    max_swing_delay_fraction = MAX_SWING_DELAY_FRACTION
    default_timing = DEFAULT_TIMING
    min_timing = MIN_TIMING
    max_timing = MAX_TIMING
    max_timing_delay_fraction = MAX_TIMING_DELAY_FRACTION
    timing_center = TIMING_CENTER
    default_humanize = DEFAULT_HUMANIZE
    min_humanize = MIN_HUMANIZE
    max_humanize = MAX_HUMANIZE
    max_humanize_delay_fraction = MAX_HUMANIZE_DELAY_FRACTION
    default_velocity_humanize = DEFAULT_VELOCITY_HUMANIZE
    min_velocity_humanize = MIN_VELOCITY_HUMANIZE
    max_velocity_humanize = MAX_VELOCITY_HUMANIZE
    max_velocity_humanize_swing = MAX_VELOCITY_HUMANIZE_SWING
    ramp_knob_center = RAMP_KNOB_CENTER
    max_ramp_velocity_swing = MAX_RAMP_VELOCITY_SWING
    long_press_seconds = LONG_PRESS_SECONDS
    double_tap_seconds = DOUBLE_TAP_SECONDS
    pulse_refresh_seconds = PULSE_REFRESH_SECONDS

    def __init__(self, matrix_rows, page_buttons=None, velocity_encoder=None, swing_encoder=None, euclidean_encoder=None, velocity_deviation_encoder=None, follow_button=None, follow_pulse_led=None, nudge_up_button=None, nudge_down_button=None, page_button_pulse_leds=None, step_pulse_leds=None, shift_button=None, on_resolution_changed=None, on_copy_source_pulse_start=None, on_copy_source_pulse_stop=None, show_message_callback=None, sequence_nudge_back_button=None, sequence_nudge_forward_button=None, rhythm_category_button=None, rhythm_category_encoder=None, fill_category_button=None, fill_generator_encoder=None, velocity_humanize_encoder=None, locked_track_provider=None, has_drum_rack_provider=None, *a, **k):
        super(StepSequencerComponent, self).__init__(*a, **k)
        assert len(matrix_rows) == self.num_rows
        self._matrix_rows = matrix_rows
        self._page_buttons = list(page_buttons) if page_buttons else []
        assert not self._page_buttons or len(self._page_buttons) == self.num_pages

        self.step_length = STEP_LENGTH

        self._resolution_index = 3
        self.triplet_active = False

        self._bar_length_beats = 4.0

        self._resolution_buttons = []

        self._triplet_button = None

        self._fill_generator_encoder = fill_generator_encoder
        self._current_knob_fill_generator = 0

        self._fill_base_empty_steps = None

        self._fill_written_steps = set()

        self._fill_baseline_loop_range = None

        self._fill_max_tail_start = None
        self._fill_loop_end_step = None

        self._fill_category_button = fill_category_button
        self._fill_category_index = 0

        self._rhythm_category_encoder = rhythm_category_encoder
        self._current_knob_rhythm_category_preset = 0

        self._rhythm_base_empty_steps = None
        self._rhythm_written_steps = set()
        self._rhythm_baseline_loop_range = None
        self._rhythm_category_button = rhythm_category_button
        self._rhythm_category_index = 0
        self._shift_button = shift_button

        self._euclidean_encoder = euclidean_encoder
        self._current_knob_euclidean = 0

        self._velocity_deviation_encoder = velocity_deviation_encoder

        self._euclidean_base_empty_steps = None

        self._euclidean_written_steps = set()

        self._euclidean_loop_start_step = None
        self._euclidean_loop_step_count = None
        self._current_knob_accent = 0

        self._accent_base_steps = None

        self._accent_baseline_loop_range = None
        self._velocity_encoder = velocity_encoder

        self._chance_encoder = None
        self._swing_encoder = swing_encoder
        self._velocity_humanize_encoder = velocity_humanize_encoder

        self._locked_track_provider = locked_track_provider

        self._has_drum_rack_provider = has_drum_rack_provider
        self._follow_button = follow_button
        self._follow_pulse_led = follow_pulse_led
        self._follow_active = False
        self._copy_clipboard = None
        self._copy_all_clipboard = None
        self._nudge_up_button = nudge_up_button
        self._nudge_down_button = nudge_down_button
        self._sequence_nudge_back_button = sequence_nudge_back_button
        self._sequence_nudge_forward_button = sequence_nudge_forward_button
        self._show_message_callback = show_message_callback
        self._page_button_pulse_leds = list(page_button_pulse_leds) if page_button_pulse_leds else []
        assert not self._page_button_pulse_leds or len(self._page_button_pulse_leds) == self.num_pages
        self._on_copy_source_pulse_start = on_copy_source_pulse_start
        self._on_copy_source_pulse_stop = on_copy_source_pulse_stop
        self._on_resolution_changed = on_resolution_changed
        self._copy_pending_source = None
        self._pulsing_page_index = None

        self._copy_pulse_extra_indices = []
        self._active_page_pulse_state = None
        self._active_page_pulse_last_forced_time = None

        self._page_button_press_times = {}
        self._page_bar_preview_active = False
        self._page_bar_preview_range = None

        self._step_grid_last_forced_time = None

        self._knob_feedback_last_forced_time = None
        self._current_knob_velocity = self.default_velocity
        self._current_knob_chance = self.default_chance
        self._current_knob_velocity_deviation = self.default_velocity_deviation
        self._current_knob_swing = self.default_swing
        self._current_knob_timing = self.default_timing
        self._current_knob_humanize = self.default_humanize

        self._global_humanize_value = self.default_humanize

        self._pitch_humanize_overrides = {}
        self._current_knob_velocity_humanize = self.default_velocity_humanize

        self._global_velocity_humanize_value = self.default_velocity_humanize
        self._pitch_velocity_humanize_overrides = {}

        self._global_velocity_deviation_value = self.default_velocity_deviation
        self._pitch_velocity_deviation_overrides = {}

        self._current_knob_ramp = 0
        self._long_press_step = None
        self._long_press_start_time = None
        self._long_press_active = False
        self._last_nudge_delete_page_tap_time = None
        self._last_page_tap_index = None
        self._last_page_tap_time = None

        self._last_tapped_bar_index = 0
        self._active = False
        self._pitch = self.pitch
        self._page = 0

        self._page_group = 0
        self._note_cache = {}
        self._chance_cache = {}
        self._timing_cache = {}
        self._deviation_cache = {}
        self._playhead_step = None

        self._true_playhead_step = None
        self._playhead_pulse_last_forced_time = None

        self._nudge_flash_start_times = {}
        self._last_touched_step = None
        self._held_steps = {}
        self._velocity_touched_during_hold = False
        self._held_drum_pad_pitches = set()

        self._held_pitch_velocity_reference = {}
        self._held_pitch_velocity_baseline = {}
        self._held_step_press_times = {}

        self._step_nudge_tracking = {}

        self._drum_pad_long_press_pitch = None
        self._drum_pad_long_press_start_time = None
        self._drum_pad_long_press_active = False
        self._pulsing_held_steps = set()
        self._button_positions = {}
        self._step_pulse_leds = {}
        flat_buttons = []
        for row_index, row in enumerate(matrix_rows):
            assert len(row) == self.steps_per_row
            for col_index, button in enumerate(row):
                local_step_index = row_index * self.steps_per_row + col_index
                self._button_positions[button] = local_step_index
                flat_buttons.append(button)
        if step_pulse_leds:
            assert len(step_pulse_leds) == self.num_rows
            for row_index, row in enumerate(step_pulse_leds):
                assert len(row) == self.steps_per_row
                for col_index, pulse_led in enumerate(row):
                    local_step_index = row_index * self.steps_per_row + col_index
                    self._step_pulse_leds[local_step_index] = pulse_led
        self._on_step_button_value.replace_subjects(flat_buttons)
        self._on_page_button_value.replace_subjects(self._page_buttons)

        self._on_velocity_encoder_value.subject = self._velocity_encoder
        self._on_swing_encoder_value.subject = self._swing_encoder
        self._on_euclidean_encoder_value.subject = self._euclidean_encoder
        self._on_velocity_deviation_encoder_value.subject = self._velocity_deviation_encoder
        self._on_velocity_humanize_encoder_value.subject = self._velocity_humanize_encoder
        self._on_follow_button_value.subject = self._follow_button
        self._on_shift_button_value.subject = self._shift_button
        self._on_sequence_nudge_back_button_value.subject = self._sequence_nudge_back_button
        self._on_sequence_nudge_forward_button_value.subject = self._sequence_nudge_forward_button
        self._on_rhythm_category_button_value.subject = self._rhythm_category_button
        self._on_rhythm_category_encoder_value.subject = self._rhythm_category_encoder
        self._on_fill_category_button_value.subject = self._fill_category_button
        self._on_fill_generator_encoder_value.subject = self._fill_generator_encoder
        self._on_detail_clip_changed.subject = self.song().view
        self._on_notes_changed.subject = None
        self._on_selected_track_changed.subject = self.song().view
        self._on_selected_scene_changed.subject = self.song().view
        self._on_session_clip_slot_has_clip_changed.subject = None

    def _show_message(self, text):

        if self._show_message_callback is not None:
            try:
                self._show_message_callback(text)
            except Exception:
                pass

    def current_pitch(self):
        return self._pitch

    def current_page(self):
        return self._page

    def _view_start_step(self):

        return self._page_group * NUM_PAGES * self.steps_per_page

    def _view_start_time(self):

        return self._view_start_step() * self.step_length

    def _absolute_page_index(self, physical_page_index):

        return self._page_group * NUM_PAGES + physical_page_index

    def scroll_pages(self, direction):

        if self._page_group + direction < 0:
            self._show_message(u'Already at the start of the clip')
            return
        self._page_group += direction
        self._page = self._page_group * NUM_PAGES + (self._page % NUM_PAGES)
        if self._active:
            self._refresh()
            self._render_page_buttons()
        self._show_message(u'Scrolled to page group %d (pages %d-%d)' % (self._page_group + 1, self._page_group * NUM_PAGES + 1, (self._page_group + 1) * NUM_PAGES))

    def refresh_page_bar_preview(self):

        if not self._active:
            return
        clip = self._clip()
        loop_start, loop_end = self._clip_loop_range(clip) if clip is not None else (None, None)
        now = time.time()
        copy_pending = self._copy_clipboard is not None or self._copy_all_clipboard is not None
        any_qualifying_held = False
        nudge_up_pressed = self._nudge_up_button is not None and self._nudge_up_button.is_pressed()
        nudge_down_pressed = self._nudge_down_button is not None and self._nudge_down_button.is_pressed()
        if not copy_pending:

            if nudge_up_pressed or nudge_down_pressed:
                any_qualifying_held = True
        for index, button in enumerate(self._page_buttons):
            if button.is_pressed():
                if index not in self._page_button_press_times:
                    self._page_button_press_times[index] = now
                if not any_qualifying_held and not copy_pending and now - self._page_button_press_times[index] >= self.long_press_seconds:
                    any_qualifying_held = True
            else:
                self._page_button_press_times.pop(index, None)
        if any_qualifying_held == self._page_bar_preview_active:
            return
        self._page_bar_preview_active = any_qualifying_held
        if any_qualifying_held:
            self._active_page_pulse_state = None
        else:
            start_bar, end_bar = self._page_bar_preview_range if self._page_bar_preview_range is not None else (1, 0)
            for index in range(len(self._page_buttons)):
                if index == self._pulsing_page_index or index in self._copy_pulse_extra_indices:

                    continue

                if start_bar <= index + 1 <= end_bar:
                    color = COLOR_PAGE_LOOP if self._page_in_loop_range(index, loop_start, loop_end) else COLOR_PAGE_BASE
                    try:
                        self._page_buttons[index].send_value(color, force=True)
                    except Exception:
                        pass
            self._page_bar_preview_range = None

    def refresh_page_buttons(self):

        if self._active:
            self._render_page_buttons()

    def refresh_follow_button(self):

        if self._active:
            self._render_follow_button()

    def refresh_sequence_nudge_buttons(self):

        if self._active:
            self._render_sequence_nudge_buttons()

    def toggle_follow(self):

        self._follow_active = not self._follow_active
        if self._active:
            self._render_follow_button()
            if self._follow_active and self._true_playhead_step is not None:
                target_page = self._true_playhead_step // self.steps_per_page
                if target_page != self._page:
                    self.set_page(target_page)

    def set_page(self, page):

        page = max(0, page)
        new_page_group = page // NUM_PAGES
        page_group_changed = new_page_group != self._page_group
        if page == self._page and not page_group_changed:
            return
        self._page = page
        self._page_group = new_page_group
        self._last_touched_step = None

        if self._active:
            if page_group_changed:
                self._refresh()
            else:
                self._render_visible_page()
            self._render_page_buttons()

    def clear_pitch(self, pitch):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        clip.remove_notes_extended(pitch, 1, range_start, range_length)
        if pitch == self._pitch:
            self._note_cache = {}
            self._chance_cache = {}
            self._timing_cache = {}
            self._deviation_cache = {}
            if self._active:
                self._render_visible_page()

    def pitches_with_notes_on_page(self, base_pitch, pitch_count):

        clip = self._clip()
        if clip is None:
            return set()
        page_start_time = self._page * self.steps_per_page * self.step_length
        page_length_time = self.steps_per_page * self.step_length
        pitches = set()
        try:
            for note in clip.get_notes_extended(base_pitch, pitch_count, page_start_time, page_length_time):
                pitches.add(note.pitch)
        except Exception:
            pass
        return pitches

    def set_pitch(self, pitch):
        if pitch != self._pitch:
            self._pitch = pitch
            self._last_touched_step = None
            self._held_steps = {}
            self._velocity_touched_during_hold = False
            self._long_press_step = None
            self._long_press_active = False
            self._held_drum_pad_pitches = set()
            self._held_pitch_velocity_reference = {}
            self._held_pitch_velocity_baseline = {}
            self._held_step_press_times = {}
            self._step_nudge_tracking = {}
            self._drum_pad_long_press_pitch = None
            self._drum_pad_long_press_start_time = None
            self._drum_pad_long_press_active = False
            self._pulsing_held_steps = set()

            self._euclidean_base_empty_steps = None
            self._euclidean_written_steps = set()
            self._rhythm_base_empty_steps = None
            self._rhythm_written_steps = set()
            self._rhythm_baseline_loop_range = None
            self._euclidean_loop_start_step = None
            self._euclidean_loop_step_count = None

            self._fill_base_empty_steps = None
            self._fill_written_steps = set()
            self._fill_max_tail_start = None
            self._fill_loop_end_step = None

            self._accent_base_steps = None

            self._current_knob_ramp = 0
            self._current_knob_velocity_humanize = 0
            self._global_velocity_humanize_value = 0
            self._current_knob_velocity_deviation = 0
            self._global_velocity_deviation_value = 0
            self._current_knob_rhythm_category_preset = 0
            self._current_knob_fill_generator = 0
            self._current_knob_euclidean = 0
            self._update_knob_feedback()
            if self._active:
                self._refresh()

    def hold_pitch_for_velocity_edit(self, pitch):

        self._held_drum_pad_pitches.add(pitch)
        if pitch not in self._held_pitch_velocity_baseline:
            self._held_pitch_velocity_reference[pitch] = self._current_knob_velocity
            self._held_pitch_velocity_baseline[pitch] = self._pitch_velocity_snapshot(pitch)
        if len(self._held_drum_pad_pitches) == 1:

            self._drum_pad_long_press_pitch = pitch
            self._drum_pad_long_press_start_time = time.time()
            self._drum_pad_long_press_active = False
        if self._active:

            self._update_knob_feedback()

    def release_pitch_velocity_edit(self, pitch):

        self._held_drum_pad_pitches.discard(pitch)
        self._held_pitch_velocity_reference.pop(pitch, None)
        self._held_pitch_velocity_baseline.pop(pitch, None)
        if pitch == self._drum_pad_long_press_pitch:
            self._drum_pad_long_press_pitch = None
            self._drum_pad_long_press_start_time = None
            self._drum_pad_long_press_active = False
        if pitch == self._pitch:
            self._accent_base_steps = None
        if self._active:
            self._update_knob_feedback()

    def _pitch_velocity_snapshot(self, pitch):

        clip = self._clip()
        if clip is None:
            return {}
        try:
            range_start, range_length = self._loop_edit_range()
            notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return {}
        return dict((note.start_time, note.velocity) for note in notes)

    def _rebind_notes_listener(self):
        self._on_notes_changed.subject = self._clip()

    @subject_slot(u'notes')
    def _on_notes_changed(self):
        if self._active:
            self._refresh()

    def _rebind_signature_listeners(self):
        clip = self._clip()
        self._on_signature_numerator_changed.subject = clip
        self._on_signature_denominator_changed.subject = clip
        self._update_bar_length()

    @subject_slot(u'signature_numerator')
    def _on_signature_numerator_changed(self):
        self._update_bar_length()
        if self._active:
            self._render_visible_page()

    @subject_slot(u'signature_denominator')
    def _on_signature_denominator_changed(self):
        self._update_bar_length()
        if self._active:
            self._render_visible_page()

    def _update_bar_length(self):

        clip = self._clip()
        if clip is None:
            self._bar_length_beats = 4.0
            return
        try:
            numerator = clip.signature_numerator
            denominator = clip.signature_denominator
            self._bar_length_beats = 4.0 * numerator / float(denominator)
        except Exception:
            self._bar_length_beats = 4.0

    def _is_bar_start(self, absolute_step_index):

        if self._bar_length_beats <= 0:
            return False
        step_time = absolute_step_index * self.step_length
        beats_into_bar = step_time % self._bar_length_beats
        if beats_into_bar > self._bar_length_beats / 2.0:
            beats_into_bar -= self._bar_length_beats
        return abs(beats_into_bar) < self.step_length / 2.0

    def _snap_to_bar_end(self, beat_time, bar_length_beats=None):

        if bar_length_beats is None:
            bar_length_beats = self._bar_length_beats
        if bar_length_beats <= 0:
            return beat_time
        bar_index = beat_time / bar_length_beats
        rounded = round(bar_index)
        if abs(bar_index - rounded) < 1e-09:
            return rounded * bar_length_beats
        return math.ceil(bar_index) * bar_length_beats

    def _bar_copy_range(self, bar_index):

        self._update_bar_length()
        bar_length_beats = self._bar_length_beats
        if bar_length_beats is None or bar_length_beats <= 0:
            bar_length_beats = self.steps_per_page * self.step_length
        start_time = bar_index * bar_length_beats
        step_count = max(1, int(round(bar_length_beats / self.step_length)))
        start_absolute_step = int(round(start_time / self.step_length))
        return start_time, bar_length_beats, step_count, start_absolute_step

    def _page_containing_time(self, beat_time):

        page_length_beats = self.steps_per_page * self.step_length
        if page_length_beats <= 0:
            return 0
        return int(beat_time // page_length_beats)

    def _bar_page_range(self, bar_index):

        _, _, step_count, start_absolute_step = self._bar_copy_range(bar_index)
        end_absolute_step = start_absolute_step + max(0, step_count - 1)
        start_page = start_absolute_step // self.steps_per_page
        end_page = end_absolute_step // self.steps_per_page
        return start_page, end_page

    def set_active(self, active):
        if self._active != active:
            self._active = active
            if active:
                self._last_touched_step = None
                self._playhead_step = None
                self._true_playhead_step = None
                self._held_steps = {}
                self._velocity_touched_during_hold = False
                self._long_press_step = None
                self._long_press_active = False
                self._held_drum_pad_pitches = set()
                self._held_pitch_velocity_reference = {}
                self._held_pitch_velocity_baseline = {}
                self._held_step_press_times = {}
                self._step_nudge_tracking = {}
                self._drum_pad_long_press_pitch = None
                self._drum_pad_long_press_start_time = None
                self._drum_pad_long_press_active = False
                self._pulsing_held_steps = set()
                self._last_nudge_delete_page_tap_time = None
                self._last_page_tap_index = None
                self._last_page_tap_time = None
                self._euclidean_base_empty_steps = None
                self._euclidean_written_steps = set()
                self._rhythm_base_empty_steps = None
                self._rhythm_written_steps = set()
                self._rhythm_baseline_loop_range = None
                self._euclidean_loop_start_step = None
                self._euclidean_loop_step_count = None
                self._fill_base_empty_steps = None
                self._fill_written_steps = set()
                self._fill_max_tail_start = None
                self._fill_loop_end_step = None
                self._accent_base_steps = None
                self._page_button_press_times = {}
                self._page_bar_preview_active = False
                self._page_bar_preview_range = None
                self._rebind_notes_listener()
                self._rebind_signature_listeners()
                self._rebind_session_clip_slot_listener()
                self._refresh()
                self._step_grid_last_forced_time = None
                self._knob_feedback_last_forced_time = None
                self._render_page_buttons()
                self._render_follow_button()
                self._render_resolution_buttons()
                self._render_sequence_nudge_buttons()
                self._render_rhythm_category_button()
                self._render_fill_category_button()
                self._update_knob_feedback()
            else:
                self._on_notes_changed.subject = None
                self._on_signature_numerator_changed.subject = None
                self._on_signature_denominator_changed.subject = None
                self._on_session_clip_slot_has_clip_changed.subject = None
                self._held_steps = {}
                self._velocity_touched_during_hold = False
                self._long_press_step = None
                self._long_press_active = False
                self._held_drum_pad_pitches = set()
                self._held_pitch_velocity_reference = {}
                self._held_pitch_velocity_baseline = {}
                self._held_step_press_times = {}
                self._step_nudge_tracking = {}
                self._drum_pad_long_press_pitch = None
                self._drum_pad_long_press_start_time = None
                self._drum_pad_long_press_active = False
                self._pulsing_held_steps = set()
                self._last_nudge_delete_page_tap_time = None
                self._last_page_tap_index = None
                self._last_page_tap_time = None
                self._euclidean_base_empty_steps = None
                self._euclidean_written_steps = set()
                self._rhythm_base_empty_steps = None
                self._rhythm_written_steps = set()
                self._rhythm_baseline_loop_range = None
                self._euclidean_loop_start_step = None
                self._euclidean_loop_step_count = None
                self._fill_base_empty_steps = None
                self._fill_written_steps = set()
                self._fill_max_tail_start = None
                self._fill_loop_end_step = None
                self._accent_base_steps = None
                self._page_button_press_times = {}
                self._page_bar_preview_active = False
                self._page_bar_preview_range = None

                self._copy_clipboard = None
                self._copy_all_clipboard = None
                self._copy_pending_source = None
                self._copy_pulse_extra_indices = []
                self._pulsing_page_index = None
                self._active_page_pulse_state = None
                self._clear_lights()
                self._update_knob_feedback()

    def _button_for_step(self, local_step_index):
        row_index, col_index = divmod(local_step_index, self.steps_per_row)
        return self._matrix_rows[row_index][col_index]

    def _pulse_led_for_step(self, local_step_index):
        return self._step_pulse_leds.get(local_step_index)

    def _clip(self):

        if self._locked_track_provider is not None:
            try:
                locked_track = self._locked_track_provider()
            except Exception:
                locked_track = None
            if locked_track is not None:
                try:
                    scene = self.song().view.selected_scene
                    scene_index = list(self.song().scenes).index(scene)
                    clip_slot = locked_track.clip_slots[scene_index]
                except Exception:
                    return None
                if clip_slot.has_clip and clip_slot.clip.is_midi_clip:
                    return clip_slot.clip
                return None
        detail_clip = self.song().view.detail_clip
        if detail_clip is not None and detail_clip.is_midi_clip:
            return detail_clip
        return None

    def refresh_for_locked_track_change(self):

        self._on_detail_clip_changed()

    @subject_slot(u'detail_clip')
    def _on_detail_clip_changed(self):
        if self._active:
            self._last_touched_step = None
            self._held_steps = {}
            self._velocity_touched_during_hold = False
            self._long_press_step = None
            self._long_press_active = False
            self._held_drum_pad_pitches = set()
            self._held_pitch_velocity_reference = {}
            self._held_pitch_velocity_baseline = {}
            self._held_step_press_times = {}
            self._step_nudge_tracking = {}
            self._drum_pad_long_press_pitch = None
            self._drum_pad_long_press_start_time = None
            self._drum_pad_long_press_active = False
            self._pulsing_held_steps = set()
            self._playhead_step = None
            self._true_playhead_step = None

            self._euclidean_base_empty_steps = None
            self._euclidean_written_steps = set()
            self._rhythm_base_empty_steps = None
            self._rhythm_written_steps = set()
            self._rhythm_baseline_loop_range = None
            self._euclidean_loop_start_step = None
            self._euclidean_loop_step_count = None
            self._fill_base_empty_steps = None
            self._fill_written_steps = set()
            self._fill_max_tail_start = None
            self._fill_loop_end_step = None
            self._accent_base_steps = None
            self._update_knob_feedback()
            self._rebind_notes_listener()
            self._rebind_signature_listeners()
            self._refresh()
            self._render_page_buttons()

    @subject_slot(u'selected_track')
    def _on_selected_track_changed(self):
        if self._active:
            self._rebind_session_clip_slot_listener()
            self._render_page_buttons()

    @subject_slot(u'selected_scene')
    def _on_selected_scene_changed(self):
        if self._active:
            self._rebind_session_clip_slot_listener()
            self._render_page_buttons()

    def _rebind_session_clip_slot_listener(self):
        self._on_session_clip_slot_has_clip_changed.subject = self._session_clip_slot()

    @subject_slot(u'has_clip')
    def _on_session_clip_slot_has_clip_changed(self):
        if self._active:
            self._render_page_buttons()

    @subject_slot_group(u'value')
    def _on_step_button_value(self, value, button):
        if not self._active:
            return
        local_step_index = self._button_positions.get(button)
        if local_step_index is None:
            return
        absolute_step_index = self._page * self.steps_per_page + local_step_index
        if value:
            self._last_touched_step = absolute_step_index
            self._held_step_press_times[absolute_step_index] = time.time()
            if not self._held_steps:

                self._velocity_touched_during_hold = False
                self._long_press_step = absolute_step_index
                self._long_press_start_time = time.time()
                self._long_press_active = False
            if self._note_cache.get(absolute_step_index, 0) > 0:
                self._held_steps[absolute_step_index] = False
                self._step_nudge_tracking[absolute_step_index] = absolute_step_index
            else:
                self._held_steps[absolute_step_index] = True
                self._set_step_velocity(absolute_step_index, self._current_knob_velocity)
            self._update_knob_feedback()
        else:
            self._held_step_press_times.pop(absolute_step_index, None)
            self._step_nudge_tracking.pop(absolute_step_index, None)
            self._stop_step_hold_pulse(absolute_step_index)
            if absolute_step_index in self._held_steps:
                was_off = self._held_steps.pop(absolute_step_index)
                if not was_off and not self._velocity_touched_during_hold:
                    self._clear_step(absolute_step_index)
                if self._last_touched_step == absolute_step_index:

                    self._last_touched_step = next(iter(self._held_steps), None)
                if absolute_step_index == self._long_press_step:
                    self._long_press_step = None
                    self._long_press_active = False
                if not self._held_steps:
                    self._velocity_touched_during_hold = False
                self._update_knob_feedback()

    @subject_slot_group(u'value')
    def _on_page_button_value(self, value, button):

        if not self._active or not value:
            return
        if self._has_drum_rack_provider is not None:
            try:
                has_drum_rack = self._has_drum_rack_provider()
            except Exception:
                has_drum_rack = True
            if not has_drum_rack:
                return
        try:
            page_index = self._page_buttons.index(button)
        except ValueError:
            return
        absolute_page_index = self._absolute_page_index(page_index)
        if self._nudge_up_button is not None and self._nudge_up_button.is_pressed():
            self._copy_page_all_pitches(page_index)
            return
        if self._nudge_down_button is not None and self._nudge_down_button.is_pressed():
            now = time.time()
            if self._last_nudge_delete_page_tap_time is not None and now - self._last_nudge_delete_page_tap_time <= self.double_tap_seconds:
                self._last_nudge_delete_page_tap_time = None
                self._clear_all_pages_all_pitches()
            else:
                self._last_nudge_delete_page_tap_time = now
                self._clear_page_all_pitches(page_index)
            return
        if page_index == self._pulsing_page_index:

            self.cancel_pending_copy()
            return
        if self._copy_all_clipboard is not None:
            self._paste_page_all_pitches(page_index)
            return
        if self._copy_clipboard is not None:

            self._paste_pitch_loop_at_bar(page_index)
            return
        held_index = self._other_held_page_button_index(page_index)
        if held_index is not None:
            self._set_loop_pages(held_index + 1, page_index + 1)
            return
        now = time.time()
        is_double_tap = self._last_page_tap_index == page_index and self._last_page_tap_time is not None and now - self._last_page_tap_time <= self.double_tap_seconds
        self._last_page_tap_index = page_index
        self._last_page_tap_time = now
        self._ensure_session_clip(absolute_page_index + 1)

        self._last_tapped_bar_index = absolute_page_index
        self.set_page(absolute_page_index)
        self._render_page_buttons()
        if is_double_tap:
            self._last_page_tap_index = None
            self._last_page_tap_time = None
            self._set_loop_pages(page_index + 1, page_index + 1)

    def set_resolution_buttons(self, buttons):

        self._resolution_buttons = list(buttons) if buttons else []
        self._on_resolution_button_value.replace_subjects(self._resolution_buttons)
        self._render_resolution_buttons()

    @subject_slot_group(u'value')
    def _on_resolution_button_value(self, value, button):

        if not self._active or not value:
            return
        try:
            index = self._resolution_buttons.index(button)
        except ValueError:
            return
        self.set_step_resolution(index)

    def set_triplet_button(self, button):

        self._triplet_button = button
        self._on_triplet_button_value.subject = button
        self._render_resolution_buttons()

    @subject_slot(u'value')
    def _on_triplet_button_value(self, value):

        if not self._active or not value:
            return
        self.toggle_triplet()

    def set_chance_encoder(self, encoder):

        self._chance_encoder = encoder
        self._on_chance_encoder_value.subject = encoder
        self._update_chance_encoder_feedback()

    @subject_slot(u'value')
    def _on_fill_generator_encoder_value(self, value):

        if not self._active:
            return
        self._current_knob_fill_generator = max(0, min(127, value))
        allow_overwrite = self._shift_button is not None and self._shift_button.is_pressed()
        current_range = self._euclidean_loop_range_steps()
        start_step, step_count = current_range
        if not step_count:
            return
        max_bars_fraction = max(category[5] for category in FILL_BANK_CATEGORIES)
        max_tail_length = min(self._fill_actual_length_steps(max_bars_fraction), step_count)
        self._fill_loop_end_step = start_step + step_count
        self._fill_max_tail_start = self._fill_loop_end_step - max_tail_length
        if not allow_overwrite and (self._fill_base_empty_steps is None or self._fill_baseline_loop_range != current_range):
            self._fill_baseline_loop_range = current_range
            active_steps = self._loop_active_steps(self._fill_max_tail_start, max_tail_length)
            self._fill_base_empty_steps = set(
                absolute_step for absolute_step in range(self._fill_max_tail_start, self._fill_loop_end_step)
                if absolute_step not in active_steps
            )
            self._fill_written_steps = set()
        category_name, category_color, short_fills, long_fills, short_bars_fraction, long_bars_fraction, short_canvas, long_canvas = FILL_BANK_CATEGORIES[self._fill_category_index]
        if self._current_knob_fill_generator < FILL_OFF_THRESHOLD:
            self._apply_fill((u'No fill', ()), long_canvas, self._fill_actual_length_steps(long_bars_fraction), allow_overwrite=allow_overwrite)
            self._update_fill_generator_encoder_feedback()
            return
        if self._current_knob_fill_generator < FILL_KNOB_MIDPOINT:
            fills = short_fills
            canvas_size = short_canvas
            actual_length = self._fill_actual_length_steps(short_bars_fraction)
            fraction = (self._current_knob_fill_generator - FILL_OFF_THRESHOLD) / float(FILL_KNOB_MIDPOINT - FILL_OFF_THRESHOLD)
        else:
            fills = long_fills
            canvas_size = long_canvas
            actual_length = self._fill_actual_length_steps(long_bars_fraction)
            fraction = (self._current_knob_fill_generator - FILL_KNOB_MIDPOINT) / float(127 - FILL_KNOB_MIDPOINT)
        fill_index = min(len(fills) - 1, int(fraction * len(fills)))
        self._apply_fill(fills[fill_index], canvas_size, actual_length, allow_overwrite=allow_overwrite)
        self._update_fill_generator_encoder_feedback()

    @subject_slot(u'value')
    def _on_fill_category_button_value(self, value):

        if not self._active or not value:
            return
        self._fill_category_index = (self._fill_category_index + 1) % len(FILL_BANK_CATEGORIES)
        name = FILL_BANK_CATEGORIES[self._fill_category_index][0]
        self._render_fill_category_button()
        self._show_message(u'Fill category: %s' % name)

    def _render_fill_category_button(self):

        if self._fill_category_button is None:
            return
        color = FILL_BANK_CATEGORIES[self._fill_category_index][1]
        try:
            self._fill_category_button.send_value(color, force=True)
        except Exception:
            pass

    def refresh_fill_category_button(self):

        if self._active:
            self._render_fill_category_button()

    def _fill_scaled_hit_steps(self, hit_positions, canvas_size, actual_fill_length):

        sorted_positions = sorted(position for position in set(hit_positions) if 0 <= position < canvas_size)
        if not sorted_positions or canvas_size <= 0 or actual_fill_length <= 0:
            return set()
        runs = []
        run_start = sorted_positions[0]
        run_end = sorted_positions[0]
        for position in sorted_positions[1:]:
            if position == run_end + 1:
                run_end = position
                continue
            runs.append((run_start, run_end))
            run_start = position
            run_end = position
        runs.append((run_start, run_end))
        result = set()
        for first, last in runs:
            start = int(first * actual_fill_length / float(canvas_size))
            if first == last:
                result.add(min(start, actual_fill_length - 1))
                continue
            end = actual_fill_length if last == canvas_size - 1 else int((last + 1) * actual_fill_length / float(canvas_size))
            result.update(range(start, end))
        return result

    def _apply_fill(self, fill, canvas_size, actual_length, allow_overwrite=False):

        if self._fill_loop_end_step is None or self._fill_max_tail_start is None:
            return
        if not allow_overwrite and self._fill_base_empty_steps is None:
            return
        if self._clip() is None:
            return
        name, hit_positions = fill
        actual_fill_length = min(actual_length, self._fill_loop_end_step - self._fill_max_tail_start)
        fill_start_step = self._fill_loop_end_step - actual_fill_length
        hit_set = set(self._fill_scaled_hit_steps(hit_positions, canvas_size, actual_fill_length))
        active_steps = self._loop_active_steps(self._fill_max_tail_start, self._fill_loop_end_step - self._fill_max_tail_start)
        changed = False
        for absolute_step_index in range(self._fill_max_tail_start, self._fill_loop_end_step):
            if not allow_overwrite and absolute_step_index not in self._fill_base_empty_steps:
                continue
            local_position = absolute_step_index - fill_start_step
            wants_hit = 0 <= local_position < actual_fill_length and local_position in hit_set
            has_note = absolute_step_index in active_steps
            if wants_hit and not has_note:
                self._write_step_note(absolute_step_index, self._current_knob_velocity, self.default_chance, self.default_velocity_deviation)
                if not allow_overwrite:
                    self._fill_written_steps.add(absolute_step_index)
                changed = True
            elif not wants_hit and has_note and (allow_overwrite or absolute_step_index in self._fill_written_steps):
                self._clear_step(absolute_step_index)
                if not allow_overwrite:
                    self._fill_written_steps.discard(absolute_step_index)
                changed = True
        if changed:
            self._euclidean_base_empty_steps = None
            self._euclidean_written_steps = set()
            self._rhythm_base_empty_steps = None
            self._rhythm_written_steps = set()
            self._rhythm_baseline_loop_range = None
            self._euclidean_loop_start_step = None
            self._euclidean_loop_step_count = None
            self._accent_base_steps = None
        if self._active:
            self._show_message(u'Fill: %s' % name)

    def _apply_rhythm_preset(self, preset_list, preset_index, allow_overwrite=False):

        if allow_overwrite:
            self._apply_rhythm_preset_overwrite(preset_list, preset_index)
        else:
            self._apply_rhythm_preset_protected(preset_list, preset_index)

    def _apply_rhythm_preset_protected(self, preset_list, preset_index):

        if self._rhythm_base_empty_steps is None:
            return
        if self._clip() is None:
            return
        start_step, step_count = self._euclidean_loop_range_steps()
        if not step_count:
            return
        name, hit_positions = preset_list[preset_index]
        hit_set = set(hit_positions)
        end_step = start_step + step_count
        active_steps = self._loop_active_steps(start_step, step_count)
        changed = False
        for absolute_step_index in range(start_step, end_step):
            if absolute_step_index not in self._rhythm_base_empty_steps:
                continue
            local_position = (absolute_step_index - start_step) % 16
            wants_hit = local_position in hit_set
            has_note = absolute_step_index in active_steps
            if wants_hit and not has_note:
                self._write_step_note(absolute_step_index, self._current_knob_velocity, self.default_chance, self.default_velocity_deviation)
                self._rhythm_written_steps.add(absolute_step_index)
                changed = True
            elif not wants_hit and has_note and absolute_step_index in self._rhythm_written_steps:
                self._clear_step(absolute_step_index)
                self._rhythm_written_steps.discard(absolute_step_index)
                changed = True
        if changed:
            self._euclidean_base_empty_steps = None
            self._euclidean_written_steps = set()
            self._euclidean_loop_start_step = None
            self._euclidean_loop_step_count = None
            self._fill_base_empty_steps = None
            self._fill_written_steps = set()
            self._fill_max_tail_start = None
            self._fill_loop_end_step = None
            self._accent_base_steps = None
        if self._active:
            self._show_message(u'Rhythm preset: %s' % name)

    def _apply_rhythm_preset_overwrite(self, preset_list, preset_index):

        clip = self._clip()
        if clip is None:
            return
        start_step, step_count = self._euclidean_loop_range_steps()
        if not step_count:
            return
        name, hit_positions = preset_list[preset_index]
        hit_set = set(hit_positions)
        end_step = start_step + step_count
        try:
            clip.remove_notes_extended(self._pitch, 1, start_step * self.step_length, step_count * self.step_length)
        except Exception:
            return
        for absolute_step_index in range(start_step, end_step):
            self._note_cache.pop(absolute_step_index, None)
            self._chance_cache.pop(absolute_step_index, None)
            self._timing_cache.pop(absolute_step_index, None)
        self._euclidean_base_empty_steps = None
        self._euclidean_written_steps = set()
        self._rhythm_base_empty_steps = None
        self._rhythm_written_steps = set()
        self._rhythm_baseline_loop_range = None
        self._euclidean_loop_start_step = None
        self._euclidean_loop_step_count = None
        self._fill_base_empty_steps = None
        self._fill_written_steps = set()
        self._fill_max_tail_start = None
        self._fill_loop_end_step = None
        self._accent_base_steps = None
        velocity = self._current_knob_velocity
        new_notes = []
        rewritten_positions = []
        for absolute_step_index in range(start_step, end_step):
            local_position = (absolute_step_index - start_step) % 16
            if local_position not in hit_set:
                continue
            self._note_cache[absolute_step_index] = velocity
            self._chance_cache[absolute_step_index] = self.default_chance
            step_time = self._step_start_time(absolute_step_index)
            duration = self._step_duration(self._pitch, absolute_step_index, step_time)
            rewritten_positions.append((absolute_step_index, step_time))
            try:
                note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(self.default_chance))
            except Exception:
                note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity)
            new_notes.append(note)
        if new_notes:
            try:
                clip.add_new_notes(tuple(new_notes))
            except Exception:
                return

        self._shorten_preceding_notes_if_needed_batch(self._pitch, 1, start_step * self.step_length, step_count * self.step_length, ((None, absolute_step_index, new_start_time, None) for absolute_step_index, new_start_time in rewritten_positions))
        if self._active:
            self._show_message(u'Rhythm preset: %s' % name)
            self._refresh()

    def _apply_ramp_velocity(self, knob_value):

        if self._clip() is None:
            return
        start_step, step_count = self._euclidean_loop_range_steps()
        if not step_count:
            return
        loop_notes = self._loop_active_notes_full(start_step, step_count)
        active_steps = sorted(loop_notes.keys())
        if not active_steps:
            return
        if knob_value < self.ramp_knob_center:
            ascending = True
            depth_fraction = (self.ramp_knob_center - knob_value) / float(self.ramp_knob_center)
        else:
            ascending = False
            depth_fraction = (knob_value - self.ramp_knob_center) / float(127 - self.ramp_knob_center)
        base_velocity = self._current_knob_velocity
        swing = depth_fraction * self.max_ramp_velocity_swing
        low_velocity = max(self.min_velocity, min(self.max_velocity, int(round(base_velocity - swing))))
        high_velocity = max(self.min_velocity, min(self.max_velocity, int(round(base_velocity + swing))))
        active_count = len(active_steps)
        note_updates = []
        for position, absolute_step_index in enumerate(active_steps):
            if active_count > 1:
                fraction = position / float(active_count - 1)
                if ascending:
                    target_velocity = low_velocity + (high_velocity - low_velocity) * fraction
                else:
                    target_velocity = high_velocity - (high_velocity - low_velocity) * fraction
            else:

                target_velocity = base_velocity
            target_velocity = max(self.min_velocity, min(self.max_velocity, int(round(target_velocity))))
            start_time, duration, current_velocity, chance, deviation = loop_notes[absolute_step_index]
            if current_velocity != target_velocity:
                note_updates.append((absolute_step_index, start_time, duration, target_velocity, chance, deviation))
        if note_updates:
            self._batch_write_step_notes(self._pitch, note_updates)
            self._accent_base_steps = None
        if self._active:
            if depth_fraction <= 0:
                self._show_message(u'Ramp: flat (%d)' % base_velocity)
            else:
                self._show_message(u'Ramp: %s %d%%' % (u'up' if ascending else u'down', int(round(depth_fraction * 100))))

    @subject_slot(u'value')
    def _on_rhythm_category_button_value(self, value):

        if not self._active or not value:
            return
        self._rhythm_category_index = (self._rhythm_category_index + 1) % len(RHYTHM_PRESET_CATEGORIES)
        name, color, presets = RHYTHM_PRESET_CATEGORIES[self._rhythm_category_index]
        self._render_rhythm_category_button()
        self._show_message(u'Rhythm category: %s' % name)

    def _render_rhythm_category_button(self):

        if self._rhythm_category_button is None:
            return
        name, color, presets = RHYTHM_PRESET_CATEGORIES[self._rhythm_category_index]
        try:
            self._rhythm_category_button.send_value(color, force=True)
        except Exception:
            pass

    def refresh_rhythm_category_button(self):

        if self._active:
            self._render_rhythm_category_button()

    @subject_slot(u'value')
    def _on_rhythm_category_encoder_value(self, value):

        if not self._active:
            return
        self._current_knob_rhythm_category_preset = max(0, min(127, value))
        allow_overwrite = self._shift_button is not None and self._shift_button.is_pressed()
        if not allow_overwrite:
            current_range = self._euclidean_loop_range_steps()
            if self._rhythm_base_empty_steps is None or self._rhythm_baseline_loop_range != current_range:
                start_step, step_count = current_range
                if not step_count:
                    return
                active_steps = self._loop_active_steps(start_step, step_count)
                self._rhythm_base_empty_steps = set(
                    absolute_step for absolute_step in range(start_step, start_step + step_count)
                    if absolute_step not in active_steps
                )
                self._rhythm_written_steps = set()
                self._rhythm_baseline_loop_range = current_range
        if self._current_knob_rhythm_category_preset < RHYTHM_OFF_THRESHOLD:
            self._apply_rhythm_preset([(u'No pattern', ())], 0, allow_overwrite=allow_overwrite)
            self._update_rhythm_category_encoder_feedback()
            return
        name, color, presets = RHYTHM_PRESET_CATEGORIES[self._rhythm_category_index]
        fraction = (self._current_knob_rhythm_category_preset - RHYTHM_OFF_THRESHOLD) / float(127 - RHYTHM_OFF_THRESHOLD)
        preset_index = min(len(presets) - 1, int(fraction * len(presets)))
        self._apply_rhythm_preset(presets, preset_index, allow_overwrite=allow_overwrite)
        self._update_rhythm_category_encoder_feedback()

    def set_step_resolution(self, index):

        if not 0 <= index < len(STEP_RESOLUTIONS):
            return
        if index == self._resolution_index:
            return
        self._resolution_index = index
        self._apply_resolution_change()

    def toggle_triplet(self):

        self.triplet_active = not self.triplet_active
        self._apply_resolution_change()

    def _current_step_length(self):

        base = STEP_RESOLUTIONS[self._resolution_index]
        return base * TRIPLET_MULTIPLIER if self.triplet_active else base

    def _current_resolution_label(self):

        label = STEP_RESOLUTION_LABELS[self._resolution_index]
        return label + u'T' if self.triplet_active else label

    def _apply_resolution_change(self):

        new_step_length = self._current_step_length()
        if new_step_length == self.step_length:
            return
        self.step_length = new_step_length

        self._euclidean_base_empty_steps = None
        self._euclidean_written_steps = set()
        self._rhythm_base_empty_steps = None
        self._rhythm_written_steps = set()
        self._rhythm_baseline_loop_range = None
        self._euclidean_loop_start_step = None
        self._euclidean_loop_step_count = None
        self._fill_base_empty_steps = None
        self._fill_written_steps = set()
        self._fill_max_tail_start = None
        self._fill_loop_end_step = None

        self._accent_base_steps = None
        self._render_resolution_buttons()
        if self._active:
            self._refresh()
            self._render_page_buttons()
        label = self._current_resolution_label()
        self._show_message(u'Step resolution set to %s' % label)
        if self._on_resolution_changed is not None:
            self._on_resolution_changed(self.step_length)

    def _render_resolution_buttons(self):

        if self._resolution_buttons:
            for index, button in enumerate(self._resolution_buttons):
                try:
                    button.send_value(127 if index == self._resolution_index else 0, force=True)
                except Exception:
                    pass
        if self._triplet_button is not None:
            try:
                self._triplet_button.send_value(127 if self.triplet_active else 0, force=True)
            except Exception:
                pass

    def refresh_resolution_buttons(self):

        if not self._active or self._shift_button is None:
            return
        if self._shift_button.is_pressed():
            self._render_resolution_buttons()

    def _other_held_page_button_index(self, page_index):

        for index, page_button in enumerate(self._page_buttons):
            if index != page_index and page_button.is_pressed():
                return index
        return None

    def _set_loop_pages(self, page_a, page_b):

        clip = self._clip()
        if clip is None:
            return
        start_page = min(page_a, page_b)
        end_page = max(page_a, page_b)
        desired_start, bar_length_beats, _, _ = self._bar_copy_range(start_page - 1)
        desired_end = end_page * bar_length_beats
        loop_start = desired_start
        loop_end = desired_end
        if loop_end <= loop_start:
            self._show_message(u'Page %d is beyond the loop-length cap' % start_page)
            return
        try:
            if clip.end_marker < loop_end:
                clip.end_marker = loop_end
        except Exception:
            pass

        try:
            clip.looping = True
        except Exception:
            pass
        try:

            current_loop_start = clip.loop_start
            clip.loop_start = min(current_loop_start, loop_start)
            clip.loop_end = loop_end
            clip.loop_start = loop_start
        except Exception:
            pass
        if self._bar_length_beats > 0:
            start_bar = int(round(loop_start / self._bar_length_beats)) + 1
            end_bar = int(round(loop_end / self._bar_length_beats))
        else:
            start_bar = end_bar = 1
        if start_bar == end_bar:
            self._show_message(u'Loop set to bar %d' % start_bar)
        else:
            self._show_message(u'Loop set to bars %d-%d' % (start_bar, end_bar))

    def _nudge_bar(self, bar_index, direction):

        clip = self._clip()
        if clip is None:
            return
        start_time, length_time, _, _ = self._bar_copy_range(bar_index)
        shift = direction * self.step_length
        try:
            notes = list(clip.get_notes_extended(0, 128, start_time, length_time))
        except Exception:
            return
        if not notes:
            return
        moves = []
        for note in notes:
            if length_time > 0:
                new_start = start_time + ((note.start_time - start_time + shift) % length_time)
            else:
                new_start = note.start_time + shift
            moves.append((note, new_start))
        try:
            clip.remove_notes_extended(0, 128, start_time, length_time)
        except Exception:
            return
        new_notes = []
        for note, new_start in moves:
            new_notes.append(Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=new_start, duration=note.duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)))
        if new_notes:
            try:
                clip.add_new_notes(tuple(new_notes))
            except Exception:
                pass
        if self._active:
            self._refresh()
            self._render_page_buttons()
        self._show_message(u'Bar nudged %s' % (u'later' if direction > 0 else u'earlier'))

    def _nudge_all_pitches_loop(self, direction):

        clip = self._clip()
        if clip is None:
            return
        start_step, step_count = self._euclidean_loop_range_steps()
        if not step_count:
            return
        range_start = start_step * self.step_length
        range_length = step_count * self.step_length
        shift = direction * self.step_length
        try:
            notes = list(clip.get_notes_extended(0, 128, range_start, range_length))
        except Exception:
            return
        if not notes:
            return
        moves = []
        for note in notes:
            new_start = range_start + ((note.start_time - range_start + shift) % range_length)
            moves.append((note, new_start))
        try:
            clip.remove_notes_extended(0, 128, range_start, range_length)
        except Exception:
            return
        self._euclidean_base_empty_steps = None
        self._euclidean_written_steps = set()
        self._rhythm_base_empty_steps = None
        self._rhythm_written_steps = set()
        self._rhythm_baseline_loop_range = None
        self._euclidean_loop_start_step = None
        self._euclidean_loop_step_count = None
        self._fill_base_empty_steps = None
        self._fill_written_steps = set()
        self._fill_max_tail_start = None
        self._fill_loop_end_step = None
        self._accent_base_steps = None
        new_notes = []
        for note, new_start in moves:
            new_notes.append(Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=new_start, duration=note.duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)))
        if new_notes:
            try:
                clip.add_new_notes(tuple(new_notes))
            except Exception:
                pass
        if self._active:
            self._refresh()
        self._show_message(u'Loop nudged %s' % (u'later' if direction > 0 else u'earlier'))

    def copy_pitch_current_page(self, pitch):

        self._copy_pitch_loop(pitch)
        self._start_copy_pulse('drum_pad', pitch)

    def clear_pitch_current_page(self, pitch):

        self._clear_pitch_on_page(pitch, self._page)

    def _copy_pitch_loop(self, pitch):

        clip = self._clip()
        notes = []
        if clip is not None:
            range_start, range_length = self._loop_edit_range()
            try:
                for note in clip.get_notes_extended(pitch, 1, range_start, range_length):
                    chance = int(round(getattr(note, 'probability', 1.0) * self.max_chance))
                    deviation = getattr(note, 'velocity_deviation', 0.0)
                    notes.append((note.start_time - range_start, note.duration, int(note.velocity), chance, deviation))
            except Exception:
                pass
        self._copy_clipboard = (pitch, notes, self._last_tapped_bar_index)
        self._copy_all_clipboard = None

    def cancel_pending_copy(self):

        self._copy_clipboard = None
        self._copy_all_clipboard = None
        self._stop_copy_pulse()

    def _start_copy_pulse(self, kind, identifier):

        self._stop_copy_pulse()
        self._copy_pending_source = (kind, identifier)
        if kind == 'page':
            physical_index = identifier
            self._pulsing_page_index = physical_index
            if self._active and 0 <= physical_index < len(self._page_button_pulse_leds):
                try:
                    self._page_button_pulse_leds[physical_index].send_value(COLOR_COPY_PULSE, force=True)
                except Exception:
                    pass
            start_page, end_page = self._bar_page_range(identifier)
            self._copy_pulse_extra_indices = [i for i in range(start_page, end_page + 1) if i != physical_index and 0 <= i < len(self._page_buttons)]
            if self._active:
                for i in self._copy_pulse_extra_indices:
                    try:
                        self._page_buttons[i].send_value(COLOR_PAGE_BASE, force=True)
                        if i < len(self._page_button_pulse_leds):
                            self._page_button_pulse_leds[i].send_value(COLOR_COPY_PULSE, force=True)
                    except Exception:
                        pass
        elif kind == 'drum_pad' and self._on_copy_source_pulse_start is not None:
            self._on_copy_source_pulse_start(identifier)

    def _stop_copy_pulse(self):
        if self._copy_pending_source is None:
            return
        kind, identifier = self._copy_pending_source
        self._copy_pending_source = None
        if kind == 'page':
            self._pulsing_page_index = None
            extra_indices = self._copy_pulse_extra_indices
            self._copy_pulse_extra_indices = []
            if self._active:
                for i in extra_indices:

                    try:
                        self._page_buttons[i].send_value(COLOR_PAGE_BASE, force=True)
                    except Exception:
                        pass
                self._render_page_buttons()
        elif kind == 'drum_pad' and self._on_copy_source_pulse_stop is not None:
            self._on_copy_source_pulse_stop()

    def _clear_pitch_on_page(self, pitch, page_index):

        clip = self._clip()
        if clip is None:
            return
        bar_start_time, bar_length_time, step_count, start_absolute_step = self._bar_copy_range(page_index)
        clip.remove_notes_extended(pitch, 1, bar_start_time, bar_length_time)
        if pitch == self._pitch:
            for local_step in range(step_count):
                self._note_cache.pop(start_absolute_step + local_step, None)
                self._chance_cache.pop(start_absolute_step + local_step, None)
                self._timing_cache.pop(start_absolute_step + local_step, None)
            if self._active:
                self._render_visible_page()

    def _clear_page_all_pitches(self, page_index):

        clip = self._clip()
        if clip is not None:
            bar_start_time, bar_length_time, step_count, start_absolute_step = self._bar_copy_range(page_index)
            try:
                clip.remove_notes_extended(0, 128, bar_start_time, bar_length_time)
            except Exception:
                pass
            for local_step in range(step_count):
                self._note_cache.pop(start_absolute_step + local_step, None)
                self._chance_cache.pop(start_absolute_step + local_step, None)
                self._timing_cache.pop(start_absolute_step + local_step, None)
        if self._active:
            self._render_visible_page()
            self._render_page_buttons()

    def _clear_all_pages_all_pitches(self):

        clip = self._clip()
        if clip is not None:
            range_start, range_length = self._loop_edit_range()
            try:
                clip.remove_notes_extended(0, 128, range_start, range_length)
            except Exception:
                pass
            self._note_cache = {}
            self._chance_cache = {}
            self._timing_cache = {}
            self._deviation_cache = {}
        if self._active:
            self._render_visible_page()
            self._render_page_buttons()
        self._show_message(u'Cleared all pitches across the whole loop')

    def _copy_page_all_pitches(self, page_index):

        clip = self._clip()
        clipboard = {}
        if clip is not None:
            page_start_time, page_length_time, step_count, _ = self._bar_copy_range(page_index)
            try:
                for note in clip.get_notes_extended(0, 128, page_start_time, page_length_time):
                    local_step = int(round((note.start_time - page_start_time) / self.step_length))
                    if 0 <= local_step < step_count:
                        chance = int(round(getattr(note, 'probability', 1.0) * self.max_chance))
                        clipboard.setdefault(note.pitch, {})[local_step] = (int(note.velocity), chance)
            except Exception:
                pass
        self._copy_all_clipboard = clipboard
        self._copy_clipboard = None
        self._start_copy_pulse('page', page_index)

    def _paste_pitch_loop(self, destination_pitch):

        source_pitch, notes, _source_bar_index = self._copy_clipboard
        clip = self._clip()
        if clip is not None:
            range_start, range_length = self._loop_edit_range()
            try:
                clip.remove_notes_extended(destination_pitch, 1, range_start, range_length)
                new_notes = tuple(Live.Clip.MidiNoteSpecification(pitch=destination_pitch, start_time=range_start + offset, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation) for offset, duration, velocity, chance, deviation in notes)
                if new_notes:
                    clip.add_new_notes(new_notes)
            except Exception:
                pass
        self._copy_clipboard = None
        self._stop_copy_pulse()
        if destination_pitch == self._pitch:
            if self._active:
                self._refresh()
                self._render_page_buttons()
        elif self._active:
            self._render_visible_page()
            self._render_page_buttons()
        self._show_message(u'Pasted pattern onto note %d' % destination_pitch)

    def _paste_pitch_loop_at_bar(self, bar_index):

        if self._copy_clipboard is None:
            return
        source_pitch, notes, source_bar_index = self._copy_clipboard
        clip = self._clip()
        if clip is not None:
            source_bar_start, source_bar_length, _, _ = self._bar_copy_range(source_bar_index)
            source_bar_end = source_bar_start + source_bar_length
            filtered_notes = [n for n in notes if source_bar_start <= n[0] < source_bar_end]
        else:
            filtered_notes = []
        if clip is not None and filtered_notes:
            range_start, range_length = self._loop_edit_range()
            bar_start_time, _, _, _ = self._bar_copy_range(bar_index)
            earliest_offset = min(offset for offset, _, _, _, _ in filtered_notes)
            try:
                new_notes = []
                for offset, duration, velocity, chance, deviation in filtered_notes:
                    pattern_relative_offset = offset - earliest_offset
                    if range_length > 0:
                        wrapped_start = range_start + ((bar_start_time - range_start) + pattern_relative_offset) % range_length
                    else:
                        wrapped_start = bar_start_time + pattern_relative_offset
                    try:
                        clip.remove_notes_extended(source_pitch, 1, wrapped_start - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
                    except Exception:
                        pass
                    new_notes.append(Live.Clip.MidiNoteSpecification(pitch=source_pitch, start_time=wrapped_start, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation))
                if new_notes:
                    clip.add_new_notes(tuple(new_notes))
            except Exception:
                pass
        self._copy_clipboard = None
        self._stop_copy_pulse()
        if source_pitch == self._pitch:
            if self._active:
                self._refresh()
                self._render_page_buttons()
        elif self._active:
            self._render_visible_page()
            self._render_page_buttons()
        self._show_message(u'Pasted note %d\'s pattern starting at bar %d' % (source_pitch, bar_index + 1))

    def paste_pitch_current_page(self, destination_pitch):

        if self._copy_clipboard is None:
            return
        self._paste_pitch_loop(destination_pitch)

    def _paste_page_all_pitches(self, page_index):

        clip = self._clip()
        target_page = page_index
        if clip is not None:
            page_start_time, page_length_time, step_count, start_absolute_step = self._bar_copy_range(page_index)
            target_page = self._page_containing_time(page_start_time)
            try:
                clip.remove_notes_extended(0, 128, page_start_time, page_length_time)
            except Exception:
                pass
            notes = []
            for pitch, steps in self._copy_all_clipboard.items():
                for local_step, (velocity, chance) in steps.items():
                    absolute_step_index = start_absolute_step + local_step
                    start_time = self._step_start_time(absolute_step_index, timing_value=self.default_timing, pitch=pitch)
                    duration = self._step_duration(pitch, absolute_step_index, start_time)
                    notes.append(Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=start_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance)))
            if notes:
                clip.add_new_notes(tuple(notes))
        self._copy_all_clipboard = None
        self._stop_copy_pulse()
        self.set_page(target_page)
        if self._active:
            self._refresh()
            self._render_page_buttons()

    @subject_slot(u'value')
    def _on_follow_button_value(self, value):
        if not self._active or not value:
            return
        self.toggle_follow()

    @subject_slot(u'value')
    def _on_shift_button_value(self, value):

        if not self._active:
            return
        self._update_knob_feedback()

    @subject_slot(u'value')
    def _on_sequence_nudge_back_button_value(self, value):

        if not self._active or not value:
            return
        self._start_nudge_flash(self._sequence_nudge_back_button)
        self._dispatch_sequence_nudge(-1)

    @subject_slot(u'value')
    def _on_sequence_nudge_forward_button_value(self, value):

        if not self._active or not value:
            return
        self._start_nudge_flash(self._sequence_nudge_forward_button)
        self._dispatch_sequence_nudge(1)

    def _dispatch_sequence_nudge(self, direction):

        if self._has_drum_rack_provider is not None:
            try:
                has_drum_rack = self._has_drum_rack_provider()
            except Exception:
                has_drum_rack = True
        else:
            has_drum_rack = True
        if has_drum_rack:
            held_active_steps = [index for index, was_off in self._held_steps.items() if not was_off]
            if held_active_steps:
                for original_index in held_active_steps:
                    current_index = self._step_nudge_tracking.get(original_index, original_index)
                    new_index = self._nudge_held_step(current_index, direction)
                    if new_index is not None:
                        self._step_nudge_tracking[original_index] = new_index
                return
            for page_index, page_button in enumerate(self._page_buttons):
                if page_button.is_pressed():
                    self._nudge_bar(self._absolute_page_index(page_index), direction)
                    return
            if self._shift_button is not None and self._shift_button.is_pressed():
                self._nudge_all_pitches_loop(direction)
                return
        self.nudge_selected_pitch_sequence(direction)

    def _start_nudge_flash(self, button):

        if button is None:
            return
        try:
            button.send_value(COLOR_BUTTON_FLASH, force=True)
        except Exception:
            return
        self._nudge_flash_start_times[button] = time.time()

    @subject_slot(u'value')
    def _on_euclidean_encoder_value(self, value):

        if not self._active:
            return
        self._current_knob_euclidean = max(0, min(127, value))
        allow_overwrite = self._shift_button is not None and self._shift_button.is_pressed()
        if not allow_overwrite:
            current_range = self._euclidean_loop_range_steps()
            if self._euclidean_base_empty_steps is None or (self._euclidean_loop_start_step, self._euclidean_loop_step_count) != current_range:
                start_step, step_count = current_range
                self._euclidean_loop_start_step = start_step
                self._euclidean_loop_step_count = step_count
                active_steps = self._loop_active_steps(start_step, step_count)
                self._euclidean_base_empty_steps = set(
                    absolute_step for absolute_step in range(start_step, start_step + step_count)
                    if absolute_step not in active_steps
                )
                self._euclidean_written_steps = set()
        self._apply_euclidean_pattern(allow_overwrite=allow_overwrite)
        self._update_euclidean_encoder_feedback()

    def _euclidean_loop_range_steps(self):

        fallback = (self._page * self.steps_per_page, self.steps_per_page)
        clip = self._clip()
        if clip is None:
            return fallback
        try:
            loop_start_beats = clip.loop_start
            loop_end_beats = clip.loop_end
        except Exception:
            return fallback
        start_step = max(0, int(round(loop_start_beats / self.step_length)))
        end_step = max(start_step, int(round(loop_end_beats / self.step_length)))
        if end_step <= start_step:
            return fallback
        return start_step, end_step - start_step

    def _fill_actual_length_steps(self, bars_fraction):

        if self.step_length <= 0 or self._bar_length_beats <= 0:
            return 1
        return max(1, int(round(self._bar_length_beats * bars_fraction / self.step_length)))

    def _euclidean_hit_count(self):

        if not self._euclidean_loop_step_count:
            return 0
        fraction = self._current_knob_euclidean / 127.0
        return int(round(fraction * self._euclidean_loop_step_count))

    def _apply_euclidean_pattern(self, allow_overwrite=False):

        if self._clip() is None:
            return
        if allow_overwrite:
            start_step, step_count = self._euclidean_loop_range_steps()
            if not step_count:
                return
            hit_count = self._euclidean_hit_count()
            pattern = _bjorklund_pattern(hit_count, step_count)
            active_steps = self._loop_active_steps(start_step, step_count)
            for local_step, wants_hit in enumerate(pattern):
                absolute_step_index = start_step + local_step
                has_note = absolute_step_index in active_steps
                if wants_hit and not has_note:
                    self._write_step_note(absolute_step_index, self._current_knob_velocity, self.default_chance, self.default_velocity_deviation)
                elif not wants_hit and has_note:
                    self._clear_step(absolute_step_index)
            return
        if self._euclidean_base_empty_steps is None or not self._euclidean_loop_step_count:
            return
        hit_count = self._euclidean_hit_count()
        pattern = _bjorklund_pattern(hit_count, self._euclidean_loop_step_count)
        start_step = self._euclidean_loop_start_step
        active_steps = self._loop_active_steps(start_step, self._euclidean_loop_step_count)
        for local_step, wants_hit in enumerate(pattern):
            absolute_step_index = start_step + local_step
            if absolute_step_index not in self._euclidean_base_empty_steps:
                continue
            has_note = absolute_step_index in active_steps
            if wants_hit and not has_note:
                self._write_step_note(absolute_step_index, self._current_knob_velocity, self.default_chance, self.default_velocity_deviation)
                self._euclidean_written_steps.add(absolute_step_index)
            elif not wants_hit and has_note and absolute_step_index in self._euclidean_written_steps:
                self._clear_step(absolute_step_index)
                self._euclidean_written_steps.discard(absolute_step_index)

    def _accent_spacing(self):

        if self._current_knob_accent <= 0:
            return 0
        fraction = min(self._current_knob_accent, ACCENT_KNOB_MIDPOINT - 1) / float(ACCENT_KNOB_MIDPOINT - 1)
        return max(2, int(round(fraction * MAX_ACCENT_SPACING)))

    def _accent_group_size(self):

        fraction = (self._current_knob_accent - ACCENT_KNOB_MIDPOINT) / float(127 - ACCENT_KNOB_MIDPOINT)
        return 1 + int(round(fraction * (MAX_ACCENT_GROUP_SIZE - 1)))

    def _apply_accent_pattern(self):

        if self._accent_base_steps is None:
            return
        if self._clip() is None:
            return
        if self._accent_baseline_loop_range is not None:
            active_notes = self._loop_active_notes_full(*self._accent_baseline_loop_range)
        else:
            active_notes = {}
        note_updates = []
        if self._current_knob_accent < ACCENT_KNOB_MIDPOINT:
            spacing = self._accent_spacing()
            for position, (absolute_step_index, original_velocity) in enumerate(self._accent_base_steps):
                if absolute_step_index not in active_notes:
                    continue
                start_time, duration, current_velocity, chance, deviation = active_notes[absolute_step_index]
                if current_velocity <= 0:
                    continue
                is_accented = spacing > 0 and position % spacing == 0
                if is_accented:
                    target_velocity = original_velocity + int(round(original_velocity * ACCENT_TIER_PERCENT))
                    target_velocity = max(self.min_velocity, min(self.max_velocity, target_velocity))
                else:
                    target_velocity = original_velocity
                if current_velocity != target_velocity:
                    note_updates.append((absolute_step_index, start_time, duration, target_velocity, chance, deviation))
        else:
            group_size = self._accent_group_size()
            for position, (absolute_step_index, original_velocity) in enumerate(self._accent_base_steps):
                if absolute_step_index not in active_notes:
                    continue
                start_time, duration, current_velocity, chance, deviation = active_notes[absolute_step_index]
                if current_velocity <= 0:
                    continue
                tier_index = (position // group_size) % 3
                if tier_index == 0:
                    target_velocity = original_velocity + int(round(original_velocity * ACCENT_TIER_PERCENT))
                elif tier_index == 1:
                    target_velocity = original_velocity
                else:
                    target_velocity = original_velocity - int(round(original_velocity * ACCENT_TIER_PERCENT))
                target_velocity = max(self.min_velocity, min(self.max_velocity, target_velocity))
                if current_velocity != target_velocity:
                    note_updates.append((absolute_step_index, start_time, duration, target_velocity, chance, deviation))
        if note_updates:
            self._batch_write_step_notes(self._pitch, note_updates)

    @subject_slot(u'value')
    def _on_velocity_encoder_value(self, value):

        if not self._active:
            return
        if self._shift_button is not None and self._shift_button.is_pressed():
            self._current_knob_accent = max(0, min(127, value))
            current_range = self._euclidean_loop_range_steps()
            if self._accent_base_steps is None or self._accent_baseline_loop_range != current_range:
                start_step, step_count = current_range
                self._accent_baseline_loop_range = current_range
                self._accent_base_steps = sorted(self._loop_active_steps(start_step, step_count).items())
            self._apply_accent_pattern()
            self._update_knob_feedback()
            return
        new_velocity = max(self.min_velocity, min(self.max_velocity, value))
        self._current_knob_velocity = new_velocity

        self._long_press_active = False
        if self._held_steps:
            self._velocity_touched_during_hold = True
            for absolute_step_index in self._held_steps:
                current_velocity = self._note_cache.get(absolute_step_index, 0)
                if current_velocity > 0 and new_velocity != current_velocity:
                    self._set_step_velocity(absolute_step_index, new_velocity)
        for pitch in self._held_drum_pad_pitches:
            reference = self._held_pitch_velocity_reference.get(pitch, new_velocity)
            delta = new_velocity - reference
            self._adjust_pitch_velocity_all_pages(pitch, delta)
        self._update_knob_feedback()

    @subject_slot(u'value')
    def _on_chance_encoder_value(self, value):

        if not self._active:
            return
        new_chance = max(self.min_chance, min(self.max_chance, value))
        self._current_knob_chance = new_chance
        self._long_press_active = False
        if self._held_steps:
            self._velocity_touched_during_hold = True
            for absolute_step_index in self._held_steps:
                current_velocity = self._note_cache.get(absolute_step_index, 0)
                current_chance = self._chance_cache.get(absolute_step_index, self.default_chance)
                if current_velocity > 0 and new_chance != current_chance:
                    self._set_step_chance(absolute_step_index, new_chance)
        for pitch in self._held_drum_pad_pitches:
            self._set_pitch_chance_all_pages(pitch, new_chance)
        self._update_knob_feedback()

    @subject_slot(u'value')
    def _on_velocity_deviation_encoder_value(self, value):

        if not self._active:
            return
        new_deviation = max(self.min_velocity_deviation, min(self.max_velocity_deviation, value))
        self._current_knob_velocity_deviation = new_deviation
        self._long_press_active = False
        if self._held_steps:
            self._velocity_touched_during_hold = True
            for absolute_step_index in self._held_steps:
                current_velocity = self._note_cache.get(absolute_step_index, 0)
                current_deviation = self._deviation_cache.get(absolute_step_index, self.default_velocity_deviation)
                if current_velocity > 0 and new_deviation != current_deviation:
                    self._set_step_velocity_deviation(absolute_step_index, new_deviation)
        for pitch in self._held_drum_pad_pitches:
            self._apply_velocity_deviation_to_clip(new_deviation, pitch=pitch)
        if not self._held_steps and not self._held_drum_pad_pitches:
            self._apply_velocity_deviation_to_clip(new_deviation)
        self._update_knob_feedback()

    @subject_slot(u'value')
    def _on_velocity_humanize_encoder_value(self, value):

        if not self._active:
            return
        if self._shift_button is not None and self._shift_button.is_pressed():
            self._current_knob_ramp = max(0, min(127, value))
            self._apply_ramp_velocity(self._current_knob_ramp)
            self._update_knob_feedback()
            return
        new_humanize = max(self.min_velocity_humanize, min(self.max_velocity_humanize, value))
        if new_humanize == self._current_knob_velocity_humanize:
            self._update_knob_feedback()
            return
        self._current_knob_velocity_humanize = new_humanize
        if self._held_drum_pad_pitches:
            for pitch in self._held_drum_pad_pitches:
                self._apply_velocity_humanize_to_clip(new_humanize, pitch=pitch)
        else:
            self._apply_velocity_humanize_to_clip(new_humanize)
        self._update_knob_feedback()

    def _set_pitch_velocity_all_pages(self, pitch, velocity):

        clip = self._clip()
        if clip is None:
            return
        try:
            notes = list(clip.get_notes_extended(pitch, 1, self._view_start_time(), self.total_steps * self.step_length))
        except Exception:
            return
        if not notes:
            return
        try:
            clip.remove_notes_extended(pitch, 1, self._view_start_time(), self.total_steps * self.step_length)
            new_notes = tuple(Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=note.start_time, duration=note.duration, velocity=velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note in notes)
            clip.add_new_notes(new_notes)
        except Exception:
            return
        if pitch == self._pitch and self._active:

            self._refresh()

    def _adjust_pitch_velocity_all_pages(self, pitch, delta):

        clip = self._clip()
        if clip is None:
            return
        baseline = self._held_pitch_velocity_baseline.get(pitch)
        if baseline is None:
            return
        range_start, range_length = self._loop_edit_range()
        try:
            notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return
        if not notes:
            return
        specs = []
        for note in notes:
            original_velocity = baseline.get(note.start_time, note.velocity)
            new_velocity = max(self.min_velocity, min(self.max_velocity, original_velocity + delta))
            specs.append(Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=note.start_time, duration=note.duration, velocity=new_velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)))
        self._batch_rewrite_notes(pitch, 1, range_start, range_length, specs)
        if pitch == self._pitch and self._active:
            self._refresh()

    def _set_pitch_chance_all_pages(self, pitch, chance):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        try:
            notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return
        if not notes:
            return
        probability = self._chance_to_probability(chance)
        specs = [Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=note.start_time, duration=note.duration, velocity=note.velocity, probability=probability, velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note in notes]
        self._batch_rewrite_notes(pitch, 1, range_start, range_length, specs)
        if pitch == self._pitch and self._active:
            self._refresh()

    def nudge_selected_pitch_sequence(self, direction):

        clip = self._clip()
        if clip is None:
            return
        start_step, step_count = self._euclidean_loop_range_steps()
        if not step_count:
            return
        end_step = start_step + step_count
        old_note_items = [(index, velocity) for index, velocity in self._note_cache.items() if velocity > 0 and start_step <= index < end_step]
        if not old_note_items:
            return
        new_positions = {}
        new_chance_positions = {}
        new_timing_positions = {}
        new_deviation_positions = {}
        for absolute_step_index, velocity in old_note_items:
            offset = (absolute_step_index - start_step + direction) % step_count
            new_index = start_step + offset
            new_positions[new_index] = velocity
            if absolute_step_index in self._chance_cache:
                new_chance_positions[new_index] = self._chance_cache[absolute_step_index]
            if absolute_step_index in self._timing_cache:
                new_timing_positions[new_index] = self._timing_cache[absolute_step_index]
            if absolute_step_index in self._deviation_cache:
                new_deviation_positions[new_index] = self._deviation_cache[absolute_step_index]
        try:
            clip.remove_notes_extended(self._pitch, 1, start_step * self.step_length, step_count * self.step_length)
        except Exception:
            return

        for absolute_step_index, velocity in old_note_items:
            del self._note_cache[absolute_step_index]
            self._chance_cache.pop(absolute_step_index, None)
            self._timing_cache.pop(absolute_step_index, None)
            self._deviation_cache.pop(absolute_step_index, None)
        self._note_cache.update(new_positions)
        self._chance_cache.update(new_chance_positions)
        self._timing_cache.update(new_timing_positions)
        self._deviation_cache.update(new_deviation_positions)
        self._euclidean_base_empty_steps = None
        self._euclidean_written_steps = set()
        self._rhythm_base_empty_steps = None
        self._rhythm_written_steps = set()
        self._rhythm_baseline_loop_range = None
        self._euclidean_loop_start_step = None
        self._euclidean_loop_step_count = None
        self._fill_base_empty_steps = None
        self._fill_written_steps = set()
        self._fill_max_tail_start = None
        self._fill_loop_end_step = None
        self._accent_base_steps = None
        new_notes = []
        rewritten_positions = []
        for absolute_step_index, velocity in new_positions.items():
            chance = new_chance_positions.get(absolute_step_index, self.default_chance)
            deviation = new_deviation_positions.get(absolute_step_index, self.default_velocity_deviation)
            step_time = self._step_start_time(absolute_step_index)
            duration = self._step_duration(self._pitch, absolute_step_index, step_time)
            rewritten_positions.append((absolute_step_index, step_time))
            try:
                note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation)
            except Exception:
                note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity)
            new_notes.append(note)
        try:
            clip.add_new_notes(tuple(new_notes))
        except Exception:
            return
        for absolute_step_index, new_start_time in rewritten_positions:
            self._shorten_preceding_note_if_needed(self._pitch, absolute_step_index, new_start_time)
        if self._active:
            self._refresh()

    @subject_slot(u'value')
    def _on_swing_encoder_value(self, value):

        if not self._active:
            return
        self._long_press_active = False
        if self._held_steps:
            new_timing = max(self.min_timing, min(self.max_timing, value))
            self._current_knob_timing = new_timing
            self._velocity_touched_during_hold = True
            for absolute_step_index in self._held_steps:
                current_velocity = self._note_cache.get(absolute_step_index, 0)
                current_timing = self._timing_cache.get(absolute_step_index, self.default_timing)
                if current_velocity > 0 and new_timing != current_timing:
                    self._set_step_timing(absolute_step_index, new_timing)
            self._update_knob_feedback()
            return
        if self._held_drum_pad_pitches:
            new_humanize = max(self.min_humanize, min(self.max_humanize, value))
            if new_humanize != self._current_knob_humanize:
                self._current_knob_humanize = new_humanize
                for pitch in self._held_drum_pad_pitches:
                    self._apply_humanize_to_clip(new_humanize, pitch=pitch)
            self._update_knob_feedback()
            return
        if self._shift_button is not None and self._shift_button.is_pressed():
            new_humanize = max(self.min_humanize, min(self.max_humanize, value))
            if new_humanize != self._current_knob_humanize:
                self._current_knob_humanize = new_humanize
                self._apply_humanize_to_clip(new_humanize)
            self._update_knob_feedback()
            return
        new_swing = max(self.min_swing, min(self.max_swing, value))
        if new_swing == self._current_knob_swing:
            self._update_swing_encoder_feedback()
            return
        old_swing_delay = self._swing_delay_beats()
        self._current_knob_swing = new_swing
        self._apply_swing_to_clip(old_swing_delay)
        self._update_swing_encoder_feedback()

    def _apply_swing_to_clip(self, old_swing_delay):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        range_start_step = int(round(range_start / self.step_length))
        range_step_count = int(round(range_length / self.step_length))
        try:
            notes = list(clip.get_notes_extended(0, 128, range_start, range_length))
        except Exception:
            return
        if not notes:
            return
        to_rewrite = []
        unchanged = []
        for note in notes:
            absolute_step_index = int(round(note.start_time / self.step_length))
            if absolute_step_index % 2 == 1 and range_start_step <= absolute_step_index < range_start_step + range_step_count:
                grid_time = absolute_step_index * self.step_length
                humanize_component = self._humanize_delay_beats(absolute_step_index, pitch=note.pitch)
                residual_delay = note.start_time - grid_time - old_swing_delay - humanize_component
                timing_value = self._delay_to_timing_value(residual_delay)
                new_start_time = self._step_start_time(absolute_step_index, timing_value=timing_value, pitch=note.pitch)
                if abs(new_start_time - note.start_time) > 1e-6:
                    new_duration = self._step_duration(note.pitch, absolute_step_index, new_start_time)
                    to_rewrite.append((note, absolute_step_index, new_start_time, new_duration))
                    continue
            unchanged.append(note)
        if not to_rewrite:
            return
        specs = [Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=new_start_time, duration=new_duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note, absolute_step_index, new_start_time, new_duration in to_rewrite]
        if not self._batch_rewrite_notes(0, 128, range_start, range_length, specs, unchanged_notes=unchanged, allow_in_place=False):
            return

        for note, absolute_step_index, new_start_time, new_duration in to_rewrite:
            self._shorten_preceding_note_if_needed(note.pitch, absolute_step_index, new_start_time)
        if self._active:
            self._refresh()

    def _humanize_value_for_pitch(self, pitch):

        return self._pitch_humanize_overrides.get(pitch, self._global_humanize_value)

    def _velocity_deviation_value_for_pitch(self, pitch):

        return self._pitch_velocity_deviation_overrides.get(pitch, self._global_velocity_deviation_value)

    def _velocity_humanize_value_for_pitch(self, pitch):

        return self._pitch_velocity_humanize_overrides.get(pitch, self._global_velocity_humanize_value)

    def _velocity_humanize_random_fraction(self, absolute_step_index, pitch=None):

        seed_pitch = pitch if pitch is not None else self._pitch
        rng = random.Random(seed_pitch * 10000 + absolute_step_index + 1000000)
        return rng.uniform(-1.0, 1.0)

    def _velocity_humanize_delta(self, absolute_step_index, pitch=None, humanize_value=None, random_fraction=None):

        if humanize_value is None:
            humanize_value = self._current_knob_velocity_humanize
        if self.max_velocity_humanize <= 0 or humanize_value <= 0:
            return 0
        if random_fraction is None:
            random_fraction = self._velocity_humanize_random_fraction(absolute_step_index, pitch=pitch)
        amount_fraction = humanize_value / float(self.max_velocity_humanize)
        return int(round(random_fraction * amount_fraction * self.max_velocity_humanize_swing))

    def _apply_velocity_humanize_to_clip(self, new_humanize_value, pitch=None):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        range_start_step = int(round(range_start / self.step_length))
        range_step_count = int(round(range_length / self.step_length))
        try:
            if pitch is None:
                notes = list(clip.get_notes_extended(0, 128, range_start, range_length))
            else:
                notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return
        if not notes:
            if pitch is None:
                self._global_velocity_humanize_value = new_humanize_value
                self._pitch_velocity_humanize_overrides = {}
            else:
                self._pitch_velocity_humanize_overrides[pitch] = new_humanize_value
            return
        to_rewrite = []
        unchanged = []
        changed = False
        for note in notes:
            absolute_step_index = int(round(note.start_time / self.step_length))
            if not range_start_step <= absolute_step_index < range_start_step + range_step_count:
                unchanged.append(note)
                continue

            random_fraction = self._velocity_humanize_random_fraction(absolute_step_index, pitch=note.pitch)
            old_delta = self._velocity_humanize_delta(absolute_step_index, pitch=note.pitch, humanize_value=self._velocity_humanize_value_for_pitch(note.pitch), random_fraction=random_fraction)
            base_velocity = int(note.velocity) - old_delta
            new_delta = self._velocity_humanize_delta(absolute_step_index, pitch=note.pitch, humanize_value=new_humanize_value, random_fraction=random_fraction)
            new_velocity = max(self.min_velocity, min(self.max_velocity, base_velocity + new_delta))
            if new_velocity != int(note.velocity):
                to_rewrite.append((note, new_velocity))
                changed = True
                continue
            unchanged.append(note)
        if to_rewrite:
            specs = [Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=note.start_time, duration=note.duration, velocity=new_velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note, new_velocity in to_rewrite]
            if pitch is None:
                self._batch_rewrite_notes(0, 128, range_start, range_length, specs, unchanged_notes=unchanged)
            else:
                self._batch_rewrite_notes(pitch, 1, range_start, range_length, specs, unchanged_notes=unchanged)
        if pitch is None:
            self._global_velocity_humanize_value = new_humanize_value
            self._pitch_velocity_humanize_overrides = {}
        else:
            self._pitch_velocity_humanize_overrides[pitch] = new_humanize_value
        if changed:
            self._accent_base_steps = None
        if self._active:
            self._refresh()

    def _apply_velocity_deviation_to_clip(self, new_deviation_value, pitch=None):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        try:
            if pitch is None:
                notes = list(clip.get_notes_extended(0, 128, range_start, range_length))
            else:
                notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return
        if not notes:
            if pitch is None:
                self._global_velocity_deviation_value = new_deviation_value
                self._pitch_velocity_deviation_overrides = {}
            else:
                self._pitch_velocity_deviation_overrides[pitch] = new_deviation_value
            return
        specs = [Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=note.start_time, duration=note.duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=new_deviation_value) for note in notes]
        if pitch is None:
            self._batch_rewrite_notes(0, 128, range_start, range_length, specs)
        else:
            self._batch_rewrite_notes(pitch, 1, range_start, range_length, specs)
        if pitch is None:
            self._global_velocity_deviation_value = new_deviation_value
            self._pitch_velocity_deviation_overrides = {}
        else:
            self._pitch_velocity_deviation_overrides[pitch] = new_deviation_value
        if self._active:
            self._refresh()

    def _apply_humanize_to_clip(self, new_humanize_value, pitch=None):

        clip = self._clip()
        if clip is None:
            return
        range_start, range_length = self._loop_edit_range()
        range_start_step = int(round(range_start / self.step_length))
        range_step_count = int(round(range_length / self.step_length))
        try:
            if pitch is None:
                notes = list(clip.get_notes_extended(0, 128, range_start, range_length))
            else:
                notes = list(clip.get_notes_extended(pitch, 1, range_start, range_length))
        except Exception:
            return
        if not notes:
            if pitch is None:
                self._global_humanize_value = new_humanize_value
                self._pitch_humanize_overrides = {}
            else:
                self._pitch_humanize_overrides[pitch] = new_humanize_value
            return
        current_swing_delay = self._swing_delay_beats()
        to_rewrite = []
        unchanged = []
        for note in notes:
            absolute_step_index = int(round(note.start_time / self.step_length))
            if not range_start_step <= absolute_step_index < range_start_step + range_step_count:
                unchanged.append(note)
                continue
            grid_time = absolute_step_index * self.step_length
            swing_component = current_swing_delay if absolute_step_index % 2 == 1 else 0.0

            random_fraction = self._humanize_random_fraction(absolute_step_index, pitch=note.pitch)
            old_humanize_delay = self._humanize_delay_beats(absolute_step_index, pitch=note.pitch, humanize_value=self._humanize_value_for_pitch(note.pitch), random_fraction=random_fraction)
            residual_delay = note.start_time - grid_time - swing_component - old_humanize_delay
            timing_value = self._delay_to_timing_value(residual_delay)
            new_start_time = self._step_start_time(absolute_step_index, timing_value=timing_value, pitch=note.pitch, humanize_value=new_humanize_value, humanize_random_fraction=random_fraction)
            if abs(new_start_time - note.start_time) > 1e-6:
                new_duration = self._step_duration(note.pitch, absolute_step_index, new_start_time)
                to_rewrite.append((note, absolute_step_index, new_start_time, new_duration))
                continue
            unchanged.append(note)
        if to_rewrite:
            specs = [Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=new_start_time, duration=new_duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note, absolute_step_index, new_start_time, new_duration in to_rewrite]
            if pitch is None:
                wrote = self._batch_rewrite_notes(0, 128, range_start, range_length, specs, unchanged_notes=unchanged, allow_in_place=False)
            else:
                wrote = self._batch_rewrite_notes(pitch, 1, range_start, range_length, specs, unchanged_notes=unchanged, allow_in_place=False)
            if not wrote:
                if pitch is None:
                    self._global_humanize_value = new_humanize_value
                    self._pitch_humanize_overrides = {}
                else:
                    self._pitch_humanize_overrides[pitch] = new_humanize_value
                return

            for note, absolute_step_index, new_start_time, new_duration in to_rewrite:
                self._shorten_preceding_note_if_needed(note.pitch, absolute_step_index, new_start_time)
        if pitch is None:
            self._global_humanize_value = new_humanize_value
            self._pitch_humanize_overrides = {}
        else:
            self._pitch_humanize_overrides[pitch] = new_humanize_value
        if self._active:
            self._refresh()

    def _update_swing_encoder_feedback(self):

        if self._swing_encoder is None:
            return
        if self._active and self._held_steps:
            if self._long_press_active and self._long_press_step in self._held_steps:
                value = self._timing_cache.get(self._long_press_step, self.default_timing)
            else:
                value = self._current_knob_timing
            ring_mode = RING_SIN_VALUE
            display_value = max(1, value)
        elif self._active and self._held_drum_pad_pitches:
            if self._drum_pad_long_press_active and self._drum_pad_long_press_pitch in self._held_drum_pad_pitches:
                if self._pitch in self._held_drum_pad_pitches:
                    display_pitch = self._pitch
                else:
                    display_pitch = sorted(self._held_drum_pad_pitches)[0]
                value = self._humanize_value_for_pitch(display_pitch)
            else:
                value = self._current_knob_humanize
            ring_mode = RING_SIN_VALUE
            display_value = max(1, value)
        elif self._active and self._shift_button is not None and self._shift_button.is_pressed():
            value = self._global_humanize_value
            ring_mode = RING_VOL_VALUE if value > 0 else RING_OFF_VALUE
            display_value = value
        elif self._active:
            value = self._current_knob_swing
            ring_mode = RING_SIN_VALUE
            display_value = max(1, value)
        else:
            ring_mode = RING_OFF_VALUE
            display_value = 0
        ring_mode_button = getattr(self._swing_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(ring_mode, force=True)
            self._swing_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def refresh_velocity_hold_reveal(self):

        if not self._active or self._long_press_active or self._long_press_step is None:
            return
        if self._long_press_step not in self._held_steps:
            return
        if time.time() - self._long_press_start_time >= self.long_press_seconds:
            self._long_press_active = True
            self._velocity_touched_during_hold = True
            self._update_knob_feedback()

    def refresh_humanize_hold_reveal(self):

        if not self._active or self._drum_pad_long_press_active or self._drum_pad_long_press_pitch is None:
            return
        if self._drum_pad_long_press_pitch not in self._held_drum_pad_pitches:
            return
        if time.time() - self._drum_pad_long_press_start_time >= self.long_press_seconds:
            self._drum_pad_long_press_active = True
            self._update_knob_feedback()

    def _update_velocity_encoder_feedback(self):

        if self._velocity_encoder is None:
            return
        if self._active and self._shift_button is not None and self._shift_button.is_pressed():
            value = self._current_knob_accent if self._active else 0
            display_value = max(1, value) if self._active else 0
            ring_mode_button = getattr(self._velocity_encoder, '_ring_mode_button', None)
            try:
                if ring_mode_button is not None:
                    ring_mode_button.send_value(RING_SIN_VALUE if self._active else RING_OFF_VALUE, force=True)
                self._velocity_encoder.send_value(display_value, force=True)
            except Exception:
                pass
            return
        if self._active and self._long_press_active and self._long_press_step in self._held_steps:
            velocity = self._note_cache.get(self._long_press_step, 0)
        else:
            velocity = self._current_knob_velocity if self._active else 0
        ring_mode_button = getattr(self._velocity_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(RING_VOL_VALUE if velocity > 0 else RING_OFF_VALUE, force=True)
            self._velocity_encoder.send_value(velocity, force=True)
        except Exception:
            pass

    def _update_velocity_humanize_encoder_feedback(self):

        if self._velocity_humanize_encoder is None:
            return
        if self._active and self._shift_button is not None and self._shift_button.is_pressed():
            value = self._current_knob_ramp
            ring_mode = RING_PAN_VALUE
            display_value = value
        elif self._active and self._held_drum_pad_pitches:
            if self._drum_pad_long_press_active and self._drum_pad_long_press_pitch in self._held_drum_pad_pitches:
                if self._pitch in self._held_drum_pad_pitches:
                    display_pitch = self._pitch
                else:
                    display_pitch = sorted(self._held_drum_pad_pitches)[0]
                value = self._velocity_humanize_value_for_pitch(display_pitch)
            else:
                value = self._current_knob_velocity_humanize
            ring_mode = RING_SIN_VALUE
            display_value = max(1, value)
        elif self._active:
            value = self._global_velocity_humanize_value
            ring_mode = RING_VOL_VALUE
            display_value = max(1, value)
        else:
            ring_mode = RING_OFF_VALUE
            display_value = 0
        ring_mode_button = getattr(self._velocity_humanize_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(ring_mode, force=True)
            self._velocity_humanize_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def _update_chance_encoder_feedback(self):

        if self._chance_encoder is None:
            return
        if self._active and self._long_press_active and self._long_press_step in self._held_steps:
            chance = self._chance_cache.get(self._long_press_step, 0)
        else:
            chance = self._current_knob_chance if self._active else 0
        ring_mode_button = getattr(self._chance_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(RING_VOL_VALUE if chance > 0 else RING_OFF_VALUE, force=True)
            self._chance_encoder.send_value(chance, force=True)
        except Exception:
            pass

    def _update_velocity_deviation_encoder_feedback(self):

        if self._velocity_deviation_encoder is None:
            return
        if self._active and self._held_steps:
            if self._long_press_active and self._long_press_step in self._held_steps:
                deviation = self._deviation_cache.get(self._long_press_step, 0)
            else:
                deviation = self._current_knob_velocity_deviation
        elif self._active and self._held_drum_pad_pitches:
            if self._drum_pad_long_press_active and self._drum_pad_long_press_pitch in self._held_drum_pad_pitches:
                if self._pitch in self._held_drum_pad_pitches:
                    display_pitch = self._pitch
                else:
                    display_pitch = sorted(self._held_drum_pad_pitches)[0]
                deviation = self._velocity_deviation_value_for_pitch(display_pitch)
            else:
                deviation = self._current_knob_velocity_deviation
        else:
            deviation = self._global_velocity_deviation_value if self._active else 0
        ring_mode_button = getattr(self._velocity_deviation_encoder, '_ring_mode_button', None)
        if self._active:
            ring_mode = RING_VOL_VALUE
            display_value = max(1, deviation)
        else:
            ring_mode = RING_OFF_VALUE
            display_value = 0
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(ring_mode, force=True)
            self._velocity_deviation_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def _update_euclidean_encoder_feedback(self):

        if self._euclidean_encoder is None:
            return
        value = self._current_knob_euclidean if self._active else 0
        display_value = max(1, value) if self._active else 0
        ring_mode_button = getattr(self._euclidean_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(RING_SIN_VALUE if self._active else RING_OFF_VALUE, force=True)
            self._euclidean_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def _update_fill_generator_encoder_feedback(self):

        if self._fill_generator_encoder is None:
            return
        value = self._current_knob_fill_generator if self._active else 0
        display_value = max(1, value) if self._active else 0
        ring_mode_button = getattr(self._fill_generator_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(RING_SIN_VALUE if self._active else RING_OFF_VALUE, force=True)
            self._fill_generator_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def _update_rhythm_category_encoder_feedback(self):

        if self._rhythm_category_encoder is None:
            return
        value = self._current_knob_rhythm_category_preset if self._active else 0
        display_value = max(1, value) if self._active else 0
        ring_mode_button = getattr(self._rhythm_category_encoder, '_ring_mode_button', None)
        try:
            if ring_mode_button is not None:
                ring_mode_button.send_value(RING_SIN_VALUE if self._active else RING_OFF_VALUE, force=True)
            self._rhythm_category_encoder.send_value(display_value, force=True)
        except Exception:
            pass

    def _update_knob_feedback(self):

        self._update_velocity_encoder_feedback()
        self._update_velocity_humanize_encoder_feedback()
        self._update_chance_encoder_feedback()
        self._update_swing_encoder_feedback()
        self._update_euclidean_encoder_feedback()
        self._update_velocity_deviation_encoder_feedback()
        self._update_fill_generator_encoder_feedback()
        self._update_rhythm_category_encoder_feedback()

    def _session_clip_slot(self):

        if self._locked_track_provider is not None:
            try:
                locked_track = self._locked_track_provider()
            except Exception:
                locked_track = None
            if locked_track is not None:
                try:
                    scene = self.song().view.selected_scene
                    scene_index = list(self.song().scenes).index(scene)
                    return locked_track.clip_slots[scene_index]
                except Exception:
                    return None
        return self.song().view.highlighted_clip_slot

    def _ensure_session_clip(self, num_bars_length=1):

        clip_slot = self._session_clip_slot()
        if clip_slot is None or clip_slot.has_clip:
            return
        try:
            song = self.song()
            song_bar_length_beats = 4.0 * song.signature_numerator / float(song.signature_denominator)
        except Exception:
            song_bar_length_beats = 4.0
        if song_bar_length_beats <= 0:
            song_bar_length_beats = 4.0
        capped_bars = max(1, min(num_bars_length, 8))
        length = capped_bars * song_bar_length_beats
        try:
            clip_slot.create_clip(length)
        except Exception:
            pass

        try:
            clip_slot.clip.looping = True
        except Exception:
            pass

    def _chance_to_probability(self, chance):
        return max(0.0, min(1.0, chance / float(self.max_chance)))

    def _swing_delay_beats(self):

        if self.max_swing <= 0:
            return 0.0
        return (self._current_knob_swing / float(self.max_swing)) * (self.step_length * self.max_swing_delay_fraction)

    def _timing_to_delay_beats(self, timing_value):

        normalized = (timing_value - self.timing_center) / self.timing_center
        normalized = max(-1.0, min(1.0, normalized))
        return normalized * self.step_length * self.max_timing_delay_fraction

    def _delay_to_timing_value(self, delay_beats):

        max_delay = self.step_length * self.max_timing_delay_fraction
        if max_delay <= 0:
            return self.default_timing
        normalized = max(-1.0, min(1.0, delay_beats / max_delay))
        return int(round(self.timing_center + normalized * self.timing_center))

    def _step_start_time(self, absolute_step_index, timing_value=None, pitch=None, humanize_value=None, humanize_random_fraction=None):

        base_time = absolute_step_index * self.step_length
        if absolute_step_index % 2 == 1:
            base_time += self._swing_delay_beats()
        base_time += self._humanize_delay_beats(absolute_step_index, pitch=pitch, humanize_value=humanize_value, random_fraction=humanize_random_fraction)
        if timing_value is None:
            timing_value = self._timing_cache.get(absolute_step_index, self.default_timing)
        base_time += self._timing_to_delay_beats(timing_value)

        return max(0.0, base_time)

    def _humanize_random_fraction(self, absolute_step_index, pitch=None):

        seed_pitch = pitch if pitch is not None else self._pitch

        rng = random.Random(seed_pitch * 10000 + absolute_step_index)
        return rng.uniform(-1.0, 1.0)

    def _humanize_delay_beats(self, absolute_step_index, pitch=None, humanize_value=None, random_fraction=None):

        if humanize_value is None:
            humanize_value = self._current_knob_humanize
        if self.max_humanize <= 0 or humanize_value <= 0:
            return 0.0
        if random_fraction is None:
            random_fraction = self._humanize_random_fraction(absolute_step_index, pitch=pitch)
        amount_fraction = humanize_value / float(self.max_humanize)
        return random_fraction * amount_fraction * (self.step_length * self.max_humanize_delay_fraction)

    def _step_duration(self, pitch, absolute_step_index, actual_start_time):

        next_grid_time = (absolute_step_index + 1) * self.step_length
        cap = next_grid_time - actual_start_time - DURATION_GAP_EPSILON
        next_actual_start = self._actual_step_start_time(pitch, absolute_step_index + 1)
        if next_actual_start is not None and next_actual_start < next_grid_time:
            cap = min(cap, next_actual_start - actual_start_time - DURATION_GAP_EPSILON)
        return max(0.01, min(self.step_length, cap))

    def _actual_step_start_time(self, pitch, absolute_step_index):

        clip = self._clip()
        if clip is None:
            return None
        grid_time = absolute_step_index * self.step_length
        try:
            notes = clip.get_notes_extended(pitch, 1, max(0.0, grid_time - self.step_length), self.step_length * 2)
        except Exception:
            return None
        for note in notes:
            note_step = int(round(note.start_time / self.step_length))
            if note_step == absolute_step_index:
                return note.start_time
        return None

    def _shorten_preceding_note_if_needed(self, pitch, absolute_step_index, new_start_time):

        if absolute_step_index <= 0:
            return
        clip = self._clip()
        if clip is None:
            return
        preceding_index = absolute_step_index - 1
        preceding_grid_time = preceding_index * self.step_length
        try:
            preceding_notes = list(clip.get_notes_extended(pitch, 1, max(0.0, preceding_grid_time - self.step_length), self.step_length * 2))
        except Exception:
            return
        for note in preceding_notes:
            note_step = int(round(note.start_time / self.step_length))
            if note_step == preceding_index and note.start_time + note.duration > new_start_time - DURATION_GAP_EPSILON + 1e-6:
                capped_duration = max(0.01, new_start_time - note.start_time - DURATION_GAP_EPSILON)
                try:
                    clip.remove_notes_extended(pitch, 1, note.start_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
                    shortened = Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=note.start_time, duration=capped_duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0))
                    clip.add_new_notes((shortened,))
                except Exception:
                    pass
                break

    def _shorten_preceding_notes_if_needed_batch(self, pitch, pitch_count, range_start, range_length, rewritten, allow_in_place=True):

        clip = self._clip()
        if clip is None:
            return
        rewritten = list(rewritten)
        if not rewritten:
            return
        try:
            all_notes = list(clip.get_notes_extended(pitch, pitch_count, range_start, range_length))
        except Exception:
            return
        by_pitch_and_step = {}
        for note in all_notes:
            note_step = int(round(note.start_time / self.step_length))
            by_pitch_and_step[(note.pitch, note_step)] = note
        to_shorten = {}
        for note, absolute_step_index, new_start_time, new_duration in rewritten:
            if absolute_step_index <= 0:
                continue
            preceding_index = absolute_step_index - 1
            note_pitch = note.pitch if note is not None else pitch
            preceding_note = by_pitch_and_step.get((note_pitch, preceding_index))
            if preceding_note is None:
                continue
            if preceding_note.start_time + preceding_note.duration > new_start_time - DURATION_GAP_EPSILON + 1e-6:
                capped_duration = max(0.01, new_start_time - preceding_note.start_time - DURATION_GAP_EPSILON)

                key = (preceding_note.pitch, preceding_note.start_time)
                if key not in to_shorten or capped_duration < to_shorten[key][1]:
                    to_shorten[key] = (preceding_note, capped_duration)
        if not to_shorten:
            return
        specs = [Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=note.start_time, duration=capped_duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)) for note, capped_duration in to_shorten.values()]

        shortened_keys = set(to_shorten.keys())
        unchanged_notes = [note for note in all_notes if (note.pitch, note.start_time) not in shortened_keys]
        self._batch_rewrite_notes(pitch, pitch_count, range_start, range_length, specs, unchanged_notes=unchanged_notes, allow_in_place=allow_in_place)

    def _write_step_note(self, absolute_step_index, velocity, chance, deviation):

        clip = self._clip()
        if clip is None:
            return
        actual_start_time = self._actual_step_start_time(self._pitch, absolute_step_index)
        step_time = actual_start_time if actual_start_time is not None else self._step_start_time(absolute_step_index)
        clip.remove_notes_extended(self._pitch, 1, step_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
        duration = self._step_duration(self._pitch, absolute_step_index, step_time)
        try:
            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation)
        except Exception:

            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=step_time, duration=duration, velocity=velocity)
        clip.add_new_notes((note,))
        self._note_cache[absolute_step_index] = velocity
        self._chance_cache[absolute_step_index] = chance
        self._deviation_cache[absolute_step_index] = deviation
        local_step_index = absolute_step_index - self._page * self.steps_per_page
        if 0 <= local_step_index < self.steps_per_page:
            self._render_step(local_step_index)

    def _set_step_velocity(self, absolute_step_index, velocity):
        chance = self._chance_cache.get(absolute_step_index, self._current_knob_chance)
        deviation = self._deviation_cache.get(absolute_step_index, self._current_knob_velocity_deviation)
        self._write_step_note(absolute_step_index, velocity, chance, deviation)

    def _set_step_chance(self, absolute_step_index, chance):
        velocity = self._note_cache.get(absolute_step_index, self._current_knob_velocity)
        deviation = self._deviation_cache.get(absolute_step_index, self._current_knob_velocity_deviation)
        self._write_step_note(absolute_step_index, velocity, chance, deviation)

    def _set_step_velocity_deviation(self, absolute_step_index, deviation):
        velocity = self._note_cache.get(absolute_step_index, self._current_knob_velocity)
        chance = self._chance_cache.get(absolute_step_index, self._current_knob_chance)
        self._write_step_note(absolute_step_index, velocity, chance, deviation)

    def _nudge_held_step(self, absolute_step_index, direction):

        clip = self._clip()
        if clip is None:
            return None
        if self._bar_length_beats <= 0:
            return None
        bar_index = int((absolute_step_index * self.step_length) / self._bar_length_beats)
        bar_start_time, bar_length_time, bar_step_count, bar_start_absolute_step = self._bar_copy_range(bar_index)
        if bar_step_count <= 0:
            return None
        active_notes = self._loop_active_notes_full(bar_start_absolute_step, bar_step_count)
        if absolute_step_index not in active_notes:
            return None
        _, _, velocity, chance, deviation = active_notes[absolute_step_index]
        new_absolute_step_index = None
        for steps_away in range(1, bar_step_count + 1):
            offset = (absolute_step_index - bar_start_absolute_step + direction * steps_away) % bar_step_count
            candidate_index = bar_start_absolute_step + offset
            if candidate_index == absolute_step_index:

                return None
            if candidate_index not in active_notes:
                new_absolute_step_index = candidate_index
                break
        if new_absolute_step_index is None:
            return None
        wrapped = new_absolute_step_index != absolute_step_index + direction
        timing_value = self._timing_cache.get(absolute_step_index, self.default_timing)
        old_step_time = self._step_start_time(absolute_step_index, timing_value=timing_value)
        clip.remove_notes_extended(self._pitch, 1, old_step_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
        for cache in (self._note_cache, self._chance_cache, self._timing_cache, self._deviation_cache):
            cache.pop(absolute_step_index, None)
        new_step_time = self._step_start_time(new_absolute_step_index, timing_value=timing_value)
        clip.remove_notes_extended(self._pitch, 1, new_step_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
        duration = self._step_duration(self._pitch, new_absolute_step_index, new_step_time)
        try:
            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=new_step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation)
        except Exception:
            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=new_step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance))
        clip.add_new_notes((note,))
        if direction < 0 and not wrapped:
            self._shorten_preceding_note_if_needed(self._pitch, new_absolute_step_index, new_step_time)
        self._note_cache[new_absolute_step_index] = velocity
        self._chance_cache[new_absolute_step_index] = chance
        self._timing_cache[new_absolute_step_index] = timing_value
        self._deviation_cache[new_absolute_step_index] = deviation
        for idx in (absolute_step_index, new_absolute_step_index):
            local_step_index = idx - self._page * self.steps_per_page
            if 0 <= local_step_index < self.steps_per_page:
                self._render_step(local_step_index)
        return new_absolute_step_index

    def _set_step_timing(self, absolute_step_index, timing_value):

        clip = self._clip()
        if clip is None:
            return
        old_step_time = self._step_start_time(absolute_step_index)
        clip.remove_notes_extended(self._pitch, 1, old_step_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
        self._timing_cache[absolute_step_index] = timing_value
        new_step_time = self._step_start_time(absolute_step_index)
        duration = self._step_duration(self._pitch, absolute_step_index, new_step_time)
        velocity = self._note_cache.get(absolute_step_index, self._current_knob_velocity)
        chance = self._chance_cache.get(absolute_step_index, self._current_knob_chance)
        try:
            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=new_step_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance))
        except Exception:
            note = Live.Clip.MidiNoteSpecification(pitch=self._pitch, start_time=new_step_time, duration=duration, velocity=velocity)
        clip.add_new_notes((note,))
        self._shorten_preceding_note_if_needed(self._pitch, absolute_step_index, new_step_time)
        local_step_index = absolute_step_index - self._page * self.steps_per_page
        if 0 <= local_step_index < self.steps_per_page:
            self._render_step(local_step_index)

    def _clear_step(self, absolute_step_index):

        clip = self._clip()
        if clip is None:
            return
        actual_start_time = self._actual_step_start_time(self._pitch, absolute_step_index)
        step_time = actual_start_time if actual_start_time is not None else self._step_start_time(absolute_step_index)
        clip.remove_notes_extended(self._pitch, 1, step_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
        if absolute_step_index in self._note_cache:
            del self._note_cache[absolute_step_index]
        if absolute_step_index in self._chance_cache:
            del self._chance_cache[absolute_step_index]
        if absolute_step_index in self._timing_cache:
            del self._timing_cache[absolute_step_index]
        local_step_index = absolute_step_index - self._page * self.steps_per_page
        if 0 <= local_step_index < self.steps_per_page:
            self._render_step(local_step_index)

    def _render_step(self, local_step_index):
        absolute_step_index = self._page * self.steps_per_page + local_step_index
        if absolute_step_index in self._pulsing_held_steps:

            return
        button = self._button_for_step(local_step_index)
        if absolute_step_index == self._playhead_step:
            button.send_value(COLOR_PLAYHEAD)
            return
        velocity = self._note_cache.get(absolute_step_index, 0)
        if velocity <= 0:
            button.send_value(COLOR_BAR_START if self._is_bar_start(absolute_step_index) else COLOR_EMPTY_STEP)
            return
        chance = self._chance_cache.get(absolute_step_index, self.max_chance)
        button.send_value(COLOR_ACTIVE_FULL_CHANCE if chance >= self.max_chance else COLOR_ACTIVE_PARTIAL_CHANCE)

    def _start_step_hold_pulse(self, absolute_step_index):

        local_step_index = absolute_step_index - self._page * self.steps_per_page
        if not 0 <= local_step_index < self.steps_per_page:
            return
        button = self._button_for_step(local_step_index)
        pulse_led = self._pulse_led_for_step(local_step_index)
        if pulse_led is None:
            return
        try:
            button.send_value(COLOR_OFF, force=True)
        except Exception:
            pass
        try:
            pulse_led.send_value(COLOR_HELD_STEP_PULSE, force=True)
            self._pulsing_held_steps.add(absolute_step_index)
        except Exception:
            pass

    def _stop_step_hold_pulse(self, absolute_step_index):

        if absolute_step_index not in self._pulsing_held_steps:
            return
        self._pulsing_held_steps.discard(absolute_step_index)
        local_step_index = absolute_step_index - self._page * self.steps_per_page
        if 0 <= local_step_index < self.steps_per_page:
            self._render_step(local_step_index)

    def refresh_step_hold_pulse(self):

        if not self._active:
            return
        now = time.time()
        for absolute_step_index, press_time in list(self._held_step_press_times.items()):
            if absolute_step_index in self._pulsing_held_steps:
                continue
            if now - press_time < self.long_press_seconds:
                continue
            if self._note_cache.get(absolute_step_index, 0) <= 0:
                continue
            self._start_step_hold_pulse(absolute_step_index)

    def _render_visible_page(self):
        for local_step_index in range(self.steps_per_page):
            self._render_step(local_step_index)

    def _render_page_buttons(self):
        if self._page_bar_preview_active:
            self._render_page_bar_preview()
            return
        clip = self._clip()
        physical_page = self._page - self._page_group * NUM_PAGES
        active_index = physical_page if physical_page != self._pulsing_page_index else None
        if clip is None:

            colors = [COLOR_OFF] * len(self._page_buttons)
            if active_index is not None and 0 <= active_index < len(colors):
                colors[active_index] = COLOR_PAGE_BASE
        else:
            loop_start, loop_end = self._clip_loop_range(clip)
            colors = [COLOR_PAGE_LOOP if self._page_in_loop_range(i, loop_start, loop_end) else COLOR_PAGE_BASE for i in range(len(self._page_buttons))]
            if self._copy_clipboard is not None or self._copy_all_clipboard is not None:

                colors = [COLOR_PAGE_BASE] * len(colors)

        new_pulse_state = (active_index, clip is not None)
        previous_pulse_state = self._active_page_pulse_state
        previous_active_index = previous_pulse_state[0] if previous_pulse_state is not None else None
        state_changed = new_pulse_state != previous_pulse_state
        now = time.time()

        needs_refresh = active_index is not None and (self._active_page_pulse_last_forced_time is None or now - self._active_page_pulse_last_forced_time >= self.pulse_refresh_seconds)
        pulse_changed = state_changed or needs_refresh
        self._active_page_pulse_state = new_pulse_state
        for index, button in enumerate(self._page_buttons):
            if index == self._pulsing_page_index or index in self._copy_pulse_extra_indices:

                continue
            if index == active_index:
                if pulse_changed:

                    button.send_value(colors[index], force=True)
                    self._active_page_pulse_last_forced_time = now

                continue
            if state_changed and index == previous_active_index:

                button.send_value(colors[index], force=True)
                continue

            button.send_value(colors[index])
        if pulse_changed and active_index is not None and 0 <= active_index < len(self._page_button_pulse_leds):

            try:
                self._page_button_pulse_leds[active_index].send_value(COLOR_PAGE_PULSE, force=True)
            except Exception:
                pass

    def _render_page_bar_preview(self):

        clip = self._clip()
        if clip is None or self._bar_length_beats <= 0:
            start_bar, end_bar = 1, 1
        else:
            loop_start, loop_end = self._clip_loop_range(clip)
            if loop_start is None or loop_end is None:
                start_bar, end_bar = 1, 1
            else:
                start_bar = int(round(loop_start / self._bar_length_beats)) + 1
                end_bar = int(round(loop_end / self._bar_length_beats))
        old_start, old_end = self._page_bar_preview_range if self._page_bar_preview_range is not None else (1, 0)
        self._page_bar_preview_range = (start_bar, end_bar)
        for index, button in enumerate(self._page_buttons):
            page_number = index + 1
            now_in_range = start_bar <= page_number <= end_bar
            was_in_range = old_start <= page_number <= old_end
            if now_in_range and was_in_range:

                continue
            if now_in_range:

                button.send_value(COLOR_PAGE_LOOP, force=True)
                if index < len(self._page_button_pulse_leds):
                    try:
                        self._page_button_pulse_leds[index].send_value(COLOR_PAGE_PULSE, force=True)
                    except Exception:
                        pass
            elif was_in_range:

                button.send_value(COLOR_PAGE_BASE, force=True)
            else:

                button.send_value(COLOR_PAGE_BASE)

    def _clip_loop_range(self, clip):

        try:
            return (clip.loop_start, clip.loop_end)
        except Exception:
            return (None, None)

    def _loop_edit_range(self):

        clip = self._clip()
        if clip is not None:
            loop_start, loop_end = self._clip_loop_range(clip)
            if loop_start is not None and loop_end is not None and loop_end > loop_start:
                return (loop_start, loop_end - loop_start)
        return (self._view_start_time(), self.total_steps * self.step_length)

    def _loop_active_steps(self, start_step, step_count, pitch=None):

        clip = self._clip()
        if clip is None or not step_count:
            return {}
        if pitch is None:
            pitch = self._pitch
        range_start = start_step * self.step_length
        range_length = step_count * self.step_length
        result = {}
        try:
            for note in clip.get_notes_extended(pitch, 1, range_start, range_length):
                absolute_step_index = int(round(note.start_time / self.step_length))
                if start_step <= absolute_step_index < start_step + step_count:
                    result[absolute_step_index] = int(note.velocity)
        except Exception:
            pass
        return result

    def _loop_active_notes_full(self, start_step, step_count, pitch=None):

        clip = self._clip()
        if clip is None or not step_count:
            return {}
        if pitch is None:
            pitch = self._pitch
        range_start = start_step * self.step_length
        range_length = step_count * self.step_length
        result = {}
        try:
            for note in clip.get_notes_extended(pitch, 1, range_start, range_length):
                absolute_step_index = int(round(note.start_time / self.step_length))
                if start_step <= absolute_step_index < start_step + step_count:
                    chance = int(round(getattr(note, 'probability', 1.0) * self.max_chance))
                    deviation = getattr(note, 'velocity_deviation', 0.0)
                    result[absolute_step_index] = (note.start_time, note.duration, int(note.velocity), chance, deviation)
        except Exception:
            pass
        return result

    def _batch_write_step_notes(self, pitch, note_updates):

        clip = self._clip()
        if clip is None:
            return
        note_updates = list(note_updates)
        if not note_updates:
            return
        specs = []
        for absolute_step_index, start_time, duration, velocity, chance, deviation in note_updates:
            try:
                note = Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=start_time, duration=duration, velocity=velocity, probability=self._chance_to_probability(chance), velocity_deviation=deviation)
            except Exception:
                note = Live.Clip.MidiNoteSpecification(pitch=pitch, start_time=start_time, duration=duration, velocity=velocity)
            specs.append(note)
        applied_in_place = False
        try:
            clip.apply_note_modifications(tuple(specs))
            applied_in_place = True
        except Exception:
            applied_in_place = False
        if not applied_in_place:
            new_notes = []
            for note_index, (absolute_step_index, start_time, duration, velocity, chance, deviation) in enumerate(note_updates):
                try:
                    clip.remove_notes_extended(pitch, 1, start_time - REMOVE_TOLERANCE, REMOVE_TOLERANCE * 2)
                except Exception:
                    continue
                new_notes.append(specs[note_index])
            if new_notes:
                try:
                    clip.add_new_notes(tuple(new_notes))
                except Exception:
                    pass
        for absolute_step_index, start_time, duration, velocity, chance, deviation in note_updates:
            if pitch == self._pitch:
                self._note_cache[absolute_step_index] = velocity
                self._chance_cache[absolute_step_index] = chance
                self._deviation_cache[absolute_step_index] = deviation
        if pitch == self._pitch and self._active:
            for absolute_step_index, _, _, _, _, _ in note_updates:
                local_step_index = absolute_step_index - self._page * self.steps_per_page
                if 0 <= local_step_index < self.steps_per_page:
                    self._render_step(local_step_index)

    def _batch_rewrite_notes(self, pitch, pitch_count, range_start, range_length, changed_specs, unchanged_notes=None, allow_in_place=True):

        clip = self._clip()
        if clip is None:
            return False
        changed_specs = tuple(changed_specs)
        if not changed_specs:
            return False
        if allow_in_place:
            try:
                clip.apply_note_modifications(changed_specs)
                return True
            except Exception:
                pass
        try:
            clip.remove_notes_extended(pitch, pitch_count, range_start, range_length)
            all_specs = list(changed_specs)
            if unchanged_notes:
                for note in unchanged_notes:
                    all_specs.append(Live.Clip.MidiNoteSpecification(pitch=note.pitch, start_time=note.start_time, duration=note.duration, velocity=note.velocity, probability=getattr(note, 'probability', 1.0), velocity_deviation=getattr(note, 'velocity_deviation', 0.0)))
            clip.add_new_notes(tuple(all_specs))
            return True
        except Exception:
            return False

    def _page_in_loop_range(self, page_index, loop_start, loop_end):

        if loop_start is None or loop_end is None:
            return False
        absolute_page_index = self._absolute_page_index(page_index)
        page_start_time = absolute_page_index * self.steps_per_page * self.step_length
        page_end_time = page_start_time + self.steps_per_page * self.step_length
        return page_start_time < loop_end and page_end_time > loop_start

    def _render_follow_button(self):
        if self._follow_button is None:
            return
        self._follow_button.send_value(COLOR_FOLLOW_ON if self._follow_active else COLOR_FOLLOW_OFF, force=True)

    def _render_sequence_nudge_buttons(self):

        if self._sequence_nudge_back_button is not None and self._sequence_nudge_back_button not in self._nudge_flash_start_times:
            self._sequence_nudge_back_button.send_value(COLOR_NUDGE_STEP, force=True)
        if self._sequence_nudge_forward_button is not None and self._sequence_nudge_forward_button not in self._nudge_flash_start_times:
            self._sequence_nudge_forward_button.send_value(COLOR_NUDGE_STEP, force=True)

    def refresh_nudge_flash(self):

        if not self._active:
            return
        now = time.time()
        for button in list(self._nudge_flash_start_times.keys()):
            start_time = self._nudge_flash_start_times[button]
            if now - start_time < NUDGE_FLASH_SECONDS:
                continue
            del self._nudge_flash_start_times[button]
            try:
                button.send_value(COLOR_NUDGE_STEP, force=True)
            except Exception:
                pass

    def _refresh(self):

        clip = self._clip()
        self._note_cache = {}
        self._chance_cache = {}
        self._timing_cache = {}
        self._deviation_cache = {}
        if clip is not None:
            view_start_step = self._view_start_step()
            for note in clip.get_notes_extended(self._pitch, 1, self._view_start_time(), self.total_steps * self.step_length):
                absolute_step_index = int(round(note.start_time / self.step_length))
                if view_start_step <= absolute_step_index < view_start_step + self.total_steps:
                    self._note_cache[absolute_step_index] = int(note.velocity)
                    self._chance_cache[absolute_step_index] = int(round(getattr(note, 'probability', 1.0) * self.max_chance))
                    self._deviation_cache[absolute_step_index] = int(round(getattr(note, 'velocity_deviation', 0.0)))
                    grid_time = absolute_step_index * self.step_length
                    swing_component = self._swing_delay_beats() if absolute_step_index % 2 == 1 else 0.0
                    humanize_component = self._humanize_delay_beats(absolute_step_index)
                    residual_delay = note.start_time - grid_time - swing_component - humanize_component
                    self._timing_cache[absolute_step_index] = self._delay_to_timing_value(residual_delay)
        self._render_visible_page()

    def _clear_lights(self):
        for row in self._matrix_rows:
            for button in row:

                button.send_value(COLOR_OFF, force=True)
        for button in self._page_buttons:

            button.send_value(COLOR_OFF, force=True)
        for pulse_led in self._page_button_pulse_leds:

            try:
                pulse_led.send_value(COLOR_OFF, force=True)
            except Exception:
                pass
        if self._follow_button is not None:
            self._follow_button.send_value(COLOR_OFF, force=True)

        for button in self._resolution_buttons:
            try:
                button.send_value(COLOR_OFF, force=True)
            except Exception:
                pass
        if self._sequence_nudge_back_button is not None:
            self._sequence_nudge_back_button.send_value(COLOR_OFF, force=True)
        if self._sequence_nudge_forward_button is not None:
            self._sequence_nudge_forward_button.send_value(COLOR_OFF, force=True)
        if self._rhythm_category_button is not None:
            self._rhythm_category_button.send_value(COLOR_OFF, force=True)
        if self._fill_category_button is not None:
            self._fill_category_button.send_value(COLOR_OFF, force=True)

    def _local_step_if_visible(self, absolute_step_index):
        if absolute_step_index is None:
            return None
        page, local_step_index = divmod(absolute_step_index, self.steps_per_page)
        return local_step_index if page == self._page else None

    def update_playhead(self):

        if not self._active:
            return
        clip = self._clip()
        self._true_playhead_step = None
        if clip is not None and clip.is_playing:
            self._true_playhead_step = int(clip.playing_position / self.step_length)
        if self._follow_active and self._true_playhead_step is not None:
            target_page = self._true_playhead_step // self.steps_per_page
            if target_page != self._page:
                self.set_page(target_page)
        new_playhead_step = None
        if self._true_playhead_step is not None:
            view_start = self._view_start_step()
            if view_start <= self._true_playhead_step < view_start + self.total_steps:
                new_playhead_step = self._true_playhead_step
        if new_playhead_step == self._playhead_step:
            return
        old_step = self._playhead_step
        self._playhead_step = new_playhead_step
        old_local = self._local_step_if_visible(old_step)
        new_local = self._local_step_if_visible(new_playhead_step)
        if old_local is not None:
            self._render_step(old_local)
        if new_local is not None:
            self._render_step(new_local)
            if new_playhead_step not in self._pulsing_held_steps:
                pulse_led = self._pulse_led_for_step(new_local)
                if pulse_led is not None:
                    try:
                        pulse_led.send_value(COLOR_PAGE_PULSE, force=True)
                        self._playhead_pulse_last_forced_time = time.time()
                    except Exception:
                        pass

    def refresh_playhead_pulse(self):

        if not self._active:
            return
        if self._playhead_step is None or self._playhead_step in self._pulsing_held_steps:
            return
        local_step_index = self._local_step_if_visible(self._playhead_step)
        if local_step_index is None:
            return
        now = time.time()
        if self._playhead_pulse_last_forced_time is not None and now - self._playhead_pulse_last_forced_time < self.pulse_refresh_seconds:
            return
        pulse_led = self._pulse_led_for_step(local_step_index)
        if pulse_led is None:
            return
        try:
            pulse_led.send_value(COLOR_PAGE_PULSE, force=True)
            self._playhead_pulse_last_forced_time = now
        except Exception:
            pass

    def refresh_step_grid(self):

        if not self._active:
            return
        now = time.time()
        if self._step_grid_last_forced_time is not None and now - self._step_grid_last_forced_time < self.pulse_refresh_seconds:
            return
        self._render_visible_page()
        self._step_grid_last_forced_time = now

    def refresh_knob_feedback(self):

        if not self._active:
            return
        now = time.time()
        if self._knob_feedback_last_forced_time is not None and now - self._knob_feedback_last_forced_time < self.pulse_refresh_seconds:
            return
        self._update_knob_feedback()
        self._knob_feedback_last_forced_time = now