"""
Pattern Builder Module
Create drum patterns, 808 basslines, and melodic sequences.
"""

import random
from typing import List, Dict, Any, Optional


class PatternBuilder:
    """Build drum patterns and basslines for various genres."""

    # MIDI note numbers for drums (General MIDI)
    DRUM_NOTES = {
        'kick': 36,
        'snare': 38,
        'clap': 39,
        'hihat': 42,
        'hihat_open': 46,
        'crash': 49,
        'ride': 51,
        'tom_low': 45,
        'tom_mid': 47,
        'tom_high': 50,
        '808': 35,  # Acoustic bass drum, typically used for 808s
    }

    def __init__(self, bpm: int = 140, steps_per_bar: int = 16):
        """
        Initialize pattern builder.

        Args:
            bpm: Beats per minute
            steps_per_bar: Number of steps per bar (16 = 16th notes)
        """
        self.bpm = bpm
        self.steps_per_bar = steps_per_bar
        self.step_duration = 60.0 / bpm / (steps_per_bar / 4)

    def create_drum_pattern(
        self,
        style: str,
        bars: int = 4,
        complexity: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Create a drum pattern based on style.

        Args:
            style: Genre style ('memphis', 'trap', 'lofi', 'boom_bap', etc.)
            bars: Number of bars
            complexity: Pattern complexity (0.0-1.0)

        Returns:
            List of note events with timing
        """
        if style.lower() == 'memphis':
            return self._memphis_pattern(bars, complexity)
        elif style.lower() == 'trap':
            return self._trap_pattern(bars, complexity)
        elif style.lower() == 'lofi':
            return self._lofi_pattern(bars, complexity)
        elif style.lower() == 'boom_bap':
            return self._boom_bap_pattern(bars, complexity)
        else:
            return self._basic_pattern(bars)

    def _memphis_pattern(self, bars: int, complexity: float) -> List[Dict[str, Any]]:
        """Memphis-style drum pattern: rolling hi-hats, snappy snares."""
        notes = []
        total_steps = self.steps_per_bar * bars

        for step in range(total_steps):
            time = step * self.step_duration
            bar_position = step % self.steps_per_bar

            # Kick on 1 and 3 (sometimes 4)
            if bar_position in [0, 8] or (bar_position == 12 and random.random() < complexity):
                notes.append({
                    'note': self.DRUM_NOTES['kick'],
                    'velocity': random.randint(90, 110),
                    'time': time,
                    'duration': self.step_duration * 2
                })

            # Snare on 2 and 4
            if bar_position in [4, 12]:
                notes.append({
                    'note': self.DRUM_NOTES['snare'],
                    'velocity': random.randint(100, 120),
                    'time': time,
                    'duration': self.step_duration
                })

            # Rolling hi-hats (16th notes with variations)
            if bar_position % 2 == 0 or random.random() < complexity:
                velocity = random.randint(60, 90) if bar_position % 2 == 1 else random.randint(70, 100)
                notes.append({
                    'note': self.DRUM_NOTES['hihat'],
                    'velocity': velocity,
                    'time': time,
                    'duration': self.step_duration * 0.8
                })

        return notes

    def _trap_pattern(self, bars: int, complexity: float) -> List[Dict[str, Any]]:
        """Trap-style pattern: sparse kicks, rolling hi-hats, snare on 3."""
        notes = []
        total_steps = self.steps_per_bar * bars

        for step in range(total_steps):
            time = step * self.step_duration
            bar_position = step % self.steps_per_bar

            # Sparse kick pattern
            if bar_position in [0, 6, 10]:
                notes.append({
                    'note': self.DRUM_NOTES['kick'],
                    'velocity': random.randint(100, 127),
                    'time': time,
                    'duration': self.step_duration * 3
                })

            # Snare on 3 (step 8)
            if bar_position == 8:
                notes.append({
                    'note': self.DRUM_NOTES['snare'],
                    'velocity': random.randint(110, 127),
                    'time': time,
                    'duration': self.step_duration * 2
                })

            # Hi-hat rolls
            if bar_position % 2 == 0:
                velocity = random.randint(60, 80)
                notes.append({
                    'note': self.DRUM_NOTES['hihat'],
                    'velocity': velocity,
                    'time': time,
                    'duration': self.step_duration * 0.7
                })

            # Triplet hi-hat rolls (complexity-dependent)
            if complexity > 0.6 and bar_position in [7, 15] and random.random() < 0.7:
                for i in range(3):
                    notes.append({
                        'note': self.DRUM_NOTES['hihat'],
                        'velocity': random.randint(80, 100),
                        'time': time + (i * self.step_duration / 3),
                        'duration': self.step_duration / 3
                    })

        return notes

    def _lofi_pattern(self, bars: int, complexity: float) -> List[Dict[str, Any]]:
        """Lo-fi hip-hop pattern: laid-back, swung hi-hats."""
        notes = []
        total_steps = self.steps_per_bar * bars
        swing = 0.7  # Swing factor

        for step in range(total_steps):
            # Apply swing to off-beats
            if step % 2 == 1:
                time = (step - 1) * self.step_duration + self.step_duration * swing
            else:
                time = step * self.step_duration

            bar_position = step % self.steps_per_bar

            # Soft kick on 1 and 3
            if bar_position in [0, 8]:
                notes.append({
                    'note': self.DRUM_NOTES['kick'],
                    'velocity': random.randint(70, 90),
                    'time': time,
                    'duration': self.step_duration * 2
                })

            # Snare on 2 and 4
            if bar_position in [4, 12]:
                notes.append({
                    'note': self.DRUM_NOTES['snare'],
                    'velocity': random.randint(60, 80),
                    'time': time,
                    'duration': self.step_duration
                })

            # Swung hi-hats
            if bar_position % 2 == 0:
                notes.append({
                    'note': self.DRUM_NOTES['hihat'],
                    'velocity': random.randint(40, 60),
                    'time': time,
                    'duration': self.step_duration
                })

        return notes

    def _boom_bap_pattern(self, bars: int, complexity: float) -> List[Dict[str, Any]]:
        """Boom-bap pattern: heavy kick and snare."""
        notes = []
        total_steps = self.steps_per_bar * bars

        for step in range(total_steps):
            time = step * self.step_duration
            bar_position = step % self.steps_per_bar

            # Heavy kick
            if bar_position in [0, 10]:
                notes.append({
                    'note': self.DRUM_NOTES['kick'],
                    'velocity': random.randint(110, 127),
                    'time': time,
                    'duration': self.step_duration * 2
                })

            # Snare on 2 and 4
            if bar_position in [4, 12]:
                notes.append({
                    'note': self.DRUM_NOTES['snare'],
                    'velocity': random.randint(100, 120),
                    'time': time,
                    'duration': self.step_duration
                })

            # Hi-hats
            if bar_position % 4 == 0:
                notes.append({
                    'note': self.DRUM_NOTES['hihat'],
                    'velocity': random.randint(50, 70),
                    'time': time,
                    'duration': self.step_duration
                })

        return notes

    def _basic_pattern(self, bars: int) -> List[Dict[str, Any]]:
        """Basic four-on-the-floor pattern."""
        notes = []
        total_steps = self.steps_per_bar * bars

        for step in range(total_steps):
            time = step * self.step_duration
            bar_position = step % self.steps_per_bar

            # Kick on every beat
            if bar_position % 4 == 0:
                notes.append({
                    'note': self.DRUM_NOTES['kick'],
                    'velocity': 100,
                    'time': time,
                    'duration': self.step_duration
                })

            # Snare on 2 and 4
            if bar_position in [4, 12]:
                notes.append({
                    'note': self.DRUM_NOTES['snare'],
                    'velocity': 100,
                    'time': time,
                    'duration': self.step_duration
                })

            # Hi-hats on 8th notes
            if bar_position % 2 == 0:
                notes.append({
                    'note': self.DRUM_NOTES['hihat'],
                    'velocity': 80,
                    'time': time,
                    'duration': self.step_duration
                })

        return notes

    def create_808_bassline(
        self,
        root_note: int = 36,
        scale: List[int] = [0, 2, 4, 5, 7, 9, 11],  # Major scale
        bars: int = 4,
        pattern_type: str = 'simple'
    ) -> List[Dict[str, Any]]:
        """
        Create an 808 bassline.

        Args:
            root_note: Root MIDI note
            scale: Scale intervals from root
            bars: Number of bars
            pattern_type: 'simple', 'bouncy', or 'rolling'

        Returns:
            List of note events
        """
        notes = []
        total_steps = self.steps_per_bar * bars

        if pattern_type == 'simple':
            # Root note on beats 1 and 3
            for bar in range(bars):
                for beat in [0, 8]:
                    step = bar * self.steps_per_bar + beat
                    notes.append({
                        'note': root_note,
                        'velocity': random.randint(100, 120),
                        'time': step * self.step_duration,
                        'duration': self.step_duration * 3
                    })

        elif pattern_type == 'bouncy':
            # More rhythmic 808 pattern
            for bar in range(bars):
                pattern_steps = [0, 3, 6, 8, 11, 14]
                for pos in pattern_steps:
                    step = bar * self.steps_per_bar + pos
                    # Vary notes using scale
                    note = root_note + random.choice(scale[:4])
                    notes.append({
                        'note': note,
                        'velocity': random.randint(90, 110),
                        'time': step * self.step_duration,
                        'duration': self.step_duration * 2
                    })

        elif pattern_type == 'rolling':
            # Fast 808 rolls
            for step in range(0, total_steps, 2):
                note = root_note + random.choice(scale[:3])
                notes.append({
                    'note': note,
                    'velocity': random.randint(80, 100),
                    'time': step * self.step_duration,
                    'duration': self.step_duration * 1.5
                })

        return notes

    def combine_patterns(self, *patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine multiple patterns into one.

        Args:
            *patterns: Variable number of pattern lists

        Returns:
            Combined pattern sorted by time
        """
        combined = []
        for pattern in patterns:
            combined.extend(pattern)

        # Sort by time
        combined.sort(key=lambda x: x['time'])
        return combined
