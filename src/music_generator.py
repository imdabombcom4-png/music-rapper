"""
Music Generator Module
High-level music generation combining patterns, scales, and genre templates.
"""

import random
from typing import Dict, Any, List, Optional
from .pattern_builder import PatternBuilder


class MusicGenerator:
    """Generate complete musical ideas based on genre and style."""

    # Musical scales (intervals from root)
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'pentatonic_major': [0, 2, 4, 7, 9],
        'pentatonic_minor': [0, 3, 5, 7, 10],
        'blues': [0, 3, 5, 6, 7, 10],
        'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
        'dorian': [0, 2, 3, 5, 7, 9, 10],
    }

    # Genre templates
    GENRE_TEMPLATES = {
        'memphis': {
            'tempo_range': (160, 180),
            'scale': 'minor',
            'drum_style': 'memphis',
            'bass_pattern': 'simple',
            'complexity': 0.7,
        },
        'trap': {
            'tempo_range': (130, 150),
            'scale': 'minor',
            'drum_style': 'trap',
            'bass_pattern': 'bouncy',
            'complexity': 0.6,
        },
        'lofi': {
            'tempo_range': (70, 90),
            'scale': 'pentatonic_minor',
            'drum_style': 'lofi',
            'bass_pattern': 'simple',
            'complexity': 0.4,
        },
        'boom_bap': {
            'tempo_range': (85, 95),
            'scale': 'minor',
            'drum_style': 'boom_bap',
            'bass_pattern': 'simple',
            'complexity': 0.5,
        },
        'drill': {
            'tempo_range': (140, 150),
            'scale': 'harmonic_minor',
            'drum_style': 'trap',
            'bass_pattern': 'rolling',
            'complexity': 0.8,
        },
    }

    def __init__(self):
        """Initialize music generator."""
        self.pattern_builder = None

    def generate_beat(
        self,
        genre: str,
        bpm: Optional[int] = None,
        key: str = 'C',
        bars: int = 4,
        include_808: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a complete beat based on genre.

        Args:
            genre: Genre style ('memphis', 'trap', 'lofi', etc.)
            bpm: Beats per minute (auto-selected if None)
            key: Musical key (e.g., 'C', 'Dm', 'F#')
            bars: Number of bars
            include_808: Whether to include 808 bassline

        Returns:
            Dictionary containing beat data and patterns
        """
        # Get genre template
        genre_lower = genre.lower()
        if genre_lower not in self.GENRE_TEMPLATES:
            print(f"Unknown genre '{genre}', using trap template")
            genre_lower = 'trap'

        template = self.GENRE_TEMPLATES[genre_lower]

        # Set BPM
        if bpm is None:
            bpm = random.randint(*template['tempo_range'])

        # Parse key to get root note and scale type
        root_note, scale_type = self._parse_key(key, template['scale'])

        # Initialize pattern builder with BPM
        self.pattern_builder = PatternBuilder(bpm=bpm)

        # Generate drum pattern
        drum_pattern = self.pattern_builder.create_drum_pattern(
            style=template['drum_style'],
            bars=bars,
            complexity=template['complexity']
        )

        # Generate 808 bassline if requested
        bass_pattern = []
        if include_808:
            bass_root = root_note - 12  # One octave lower
            scale_intervals = self.SCALES[scale_type]
            bass_pattern = self.pattern_builder.create_808_bassline(
                root_note=bass_root,
                scale=scale_intervals,
                bars=bars,
                pattern_type=template['bass_pattern']
            )

        # Combine patterns
        combined_pattern = self.pattern_builder.combine_patterns(drum_pattern, bass_pattern)

        return {
            'genre': genre,
            'bpm': bpm,
            'key': key,
            'bars': bars,
            'drum_pattern': drum_pattern,
            'bass_pattern': bass_pattern,
            'combined_pattern': combined_pattern,
            'scale': scale_type,
            'root_note': root_note,
        }

    def _parse_key(self, key: str, default_scale: str) -> tuple:
        """
        Parse key string to get root note and scale type.

        Args:
            key: Key string like 'C', 'Dm', 'F#m'
            default_scale: Default scale if not specified in key

        Returns:
            Tuple of (root_note_midi, scale_type)
        """
        # Note to MIDI mapping (C4 = 60)
        note_map = {
            'C': 60, 'C#': 61, 'Db': 61,
            'D': 62, 'D#': 63, 'Eb': 63,
            'E': 64,
            'F': 65, 'F#': 66, 'Gb': 66,
            'G': 67, 'G#': 68, 'Ab': 68,
            'A': 69, 'A#': 70, 'Bb': 70,
            'B': 71,
        }

        # Extract root note and quality
        key = key.strip()
        scale_type = default_scale

        # Check for minor indicator
        if key.endswith('m'):
            scale_type = 'minor'
            root_str = key[:-1]
        else:
            root_str = key
            if default_scale == 'minor':
                scale_type = 'major'  # If key doesn't specify, default to major

        # Get MIDI note
        root_note = note_map.get(root_str, 60)  # Default to C if not found

        return root_note, scale_type

    def generate_melody(
        self,
        key: str = 'C',
        scale: str = 'pentatonic_minor',
        bars: int = 4,
        note_density: float = 0.5,
        octave: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate a simple melody.

        Args:
            key: Root key
            scale: Scale type
            bars: Number of bars
            note_density: How many notes (0.0-1.0)
            octave: MIDI octave (4 = middle, 5 = higher)

        Returns:
            List of note events
        """
        root_note, _ = self._parse_key(key, scale)
        root_note = (octave * 12) + (root_note % 12)  # Adjust to octave

        scale_intervals = self.SCALES.get(scale, self.SCALES['pentatonic_minor'])

        if not self.pattern_builder:
            self.pattern_builder = PatternBuilder(bpm=120)

        notes = []
        total_steps = self.pattern_builder.steps_per_bar * bars

        for step in range(total_steps):
            # Probabilistic note placement
            if random.random() < note_density:
                # Choose note from scale
                interval = random.choice(scale_intervals)
                # Occasionally jump octaves
                if random.random() < 0.2:
                    octave_shift = random.choice([-12, 0, 12])
                else:
                    octave_shift = 0

                note = root_note + interval + octave_shift

                # Ensure note is in valid MIDI range
                note = max(0, min(127, note))

                notes.append({
                    'note': note,
                    'velocity': random.randint(70, 100),
                    'time': step * self.pattern_builder.step_duration,
                    'duration': self.pattern_builder.step_duration * random.choice([1, 2, 3, 4])
                })

        return notes

    def get_genre_info(self, genre: str) -> Optional[Dict[str, Any]]:
        """Get information about a genre template."""
        return self.GENRE_TEMPLATES.get(genre.lower())

    def list_genres(self) -> List[str]:
        """List all available genre templates."""
        return list(self.GENRE_TEMPLATES.keys())

    def list_scales(self) -> List[str]:
        """List all available scales."""
        return list(self.SCALES.keys())
