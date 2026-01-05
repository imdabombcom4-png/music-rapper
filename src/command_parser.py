"""
Command Parser Module
Parse natural language commands for FL Studio automation.
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path


class CommandParser:
    """Parse natural language commands into structured operations."""

    def __init__(self):
        """Initialize command parser."""
        # Regex patterns for different command types
        self.patterns = {
            'sample_process': r'(?:take|load|use|get)\s+(.+?\.(?:wav|mp3|flac|aiff))',
            'pitch_shift': r'pitch\s+(?:down|up)?\s*(-?\d+)\s*(?:semitones?|st)?',
            'time_stretch': r'stretch\s+(?:by\s+)?([0-9.]+)',
            'filter': r'(lowpass|highpass|bandpass)\s+(?:filter\s+)?(?:at\s+)?(\d+)\s*(?:hz)?',
            'slice': r'(?:slice|chop)\s+(?:into\s+)?(\d+)\s*(?:slices?|parts?)?',
            'insert_position': r'insert\s+(?:at\s+)?(?:bar\s+)?(\d+)(?:\s+beat\s+)?(\d+)?',
            'measure_position': r'(?:at\s+)?(?:the\s+)?(?:end\s+of\s+)?(?:measure|bar)\s+(\d+)',
            'beat_position': r'(?:beat|count)\s+(\d+)',
            'create_beat': r'create\s+(?:a\s+)?(.+?)\s+(?:style\s+)?beat',
            'genre': r'(memphis|trap|lofi|boom\s*bap|drill)',
            'with_808': r'with\s+808s?',
            'bpm': r'(?:at\s+)?(\d+)\s*bpm',
            'key': r'(?:in\s+)?(?:key\s+of\s+)?([A-G][#b]?m?)',
            'bars': r'(\d+)\s+bars?',
        }

    def parse(self, command: str) -> Dict[str, Any]:
        """
        Parse a natural language command.

        Args:
            command: Natural language command string

        Returns:
            Structured command dictionary

        Examples:
            "take sample.wav, pitch down 3 semitones, stretch by .82, insert at bar 40 beat 3"
            "create a memphis style beat with 808s at 170 bpm"
        """
        command = command.lower().strip()

        # Determine command type
        if any(word in command for word in ['take', 'load', 'use', 'sample']):
            return self._parse_sample_command(command)
        elif any(word in command for word in ['create', 'make', 'generate']):
            return self._parse_generate_command(command)
        else:
            return {'type': 'unknown', 'raw': command}

    def _parse_sample_command(self, command: str) -> Dict[str, Any]:
        """Parse sample processing command."""
        result = {
            'type': 'sample_process',
            'sample_path': None,
            'operations': [],
            'insert_bar': None,
            'insert_beat': 1,
        }

        # Extract sample path
        sample_match = re.search(self.patterns['sample_process'], command)
        if sample_match:
            result['sample_path'] = sample_match.group(1)

        # Extract pitch shift
        pitch_match = re.search(self.patterns['pitch_shift'], command)
        if pitch_match:
            semitones = int(pitch_match.group(1))
            # Check if it's "pitch down"
            if 'pitch down' in command and semitones > 0:
                semitones = -semitones
            result['operations'].append({
                'type': 'pitch_shift',
                'semitones': semitones
            })

        # Extract time stretch
        stretch_match = re.search(self.patterns['time_stretch'], command)
        if stretch_match:
            result['operations'].append({
                'type': 'time_stretch',
                'rate': float(stretch_match.group(1))
            })

        # Extract filter
        filter_match = re.search(self.patterns['filter'], command)
        if filter_match:
            result['operations'].append({
                'type': 'filter',
                'filter_type': filter_match.group(1),
                'cutoff': int(filter_match.group(2))
            })

        # Extract slice
        slice_match = re.search(self.patterns['slice'], command)
        if slice_match:
            result['operations'].append({
                'type': 'slice',
                'num_slices': int(slice_match.group(1))
            })

        # Extract insert position
        insert_match = re.search(self.patterns['insert_position'], command)
        if insert_match:
            result['insert_bar'] = int(insert_match.group(1))
            result['insert_beat'] = int(insert_match.group(2)) if insert_match.group(2) else 1

        # Alternative: measure position
        measure_match = re.search(self.patterns['measure_position'], command)
        if measure_match and not result['insert_bar']:
            result['insert_bar'] = int(measure_match.group(1))
            # Check for beat position
            beat_match = re.search(self.patterns['beat_position'], command)
            if beat_match:
                result['insert_beat'] = int(beat_match.group(1))

        return result

    def _parse_generate_command(self, command: str) -> Dict[str, Any]:
        """Parse beat/music generation command."""
        result = {
            'type': 'generate_beat',
            'genre': None,
            'bpm': None,
            'key': 'C',
            'bars': 4,
            'include_808': False,
        }

        # Extract genre
        genre_match = re.search(self.patterns['genre'], command)
        if genre_match:
            genre = genre_match.group(1).replace(' ', '_')  # boom bap -> boom_bap
            result['genre'] = genre
        elif 'beat' in command:
            # Try to extract from "create a X beat" pattern
            beat_match = re.search(self.patterns['create_beat'], command)
            if beat_match:
                description = beat_match.group(1)
                # Check if description matches known genre
                for genre in ['memphis', 'trap', 'lofi', 'drill']:
                    if genre in description:
                        result['genre'] = genre
                        break

        # Default to trap if no genre found
        if not result['genre']:
            result['genre'] = 'trap'

        # Extract BPM
        bpm_match = re.search(self.patterns['bpm'], command)
        if bpm_match:
            result['bpm'] = int(bpm_match.group(1))

        # Extract key
        key_match = re.search(self.patterns['key'], command)
        if key_match:
            result['key'] = key_match.group(1).upper()

        # Extract bars
        bars_match = re.search(self.patterns['bars'], command)
        if bars_match:
            result['bars'] = int(bars_match.group(1))

        # Check for 808s
        if re.search(self.patterns['with_808'], command):
            result['include_808'] = True

        return result

    def validate_sample_path(self, path: str, search_dirs: Optional[List[str]] = None) -> Optional[str]:
        """
        Validate and resolve sample path.

        Args:
            path: Sample path from command
            search_dirs: Optional directories to search for the sample

        Returns:
            Resolved absolute path or None if not found
        """
        # Check if path is absolute and exists
        p = Path(path)
        if p.is_absolute() and p.exists():
            return str(p)

        # Search in provided directories
        if search_dirs:
            for search_dir in search_dirs:
                candidate = Path(search_dir) / path
                if candidate.exists():
                    return str(candidate)

        # Search in current directory
        if Path(path).exists():
            return str(Path(path).absolute())

        return None

    def format_help(self) -> str:
        """Generate help text for command syntax."""
        return """
FL Studio Automation Commands
==============================

SAMPLE PROCESSING:
  take <file> [operations] insert at bar <N> [beat <N>]

  Operations:
    - pitch up/down <N> semitones
    - stretch by <factor> (e.g., 0.82 for slower)
    - lowpass/highpass/bandpass <frequency> Hz
    - slice into <N> slices

  Examples:
    "take sample.wav, pitch down 3 semitones, stretch by 0.82, insert at bar 40 beat 3"
    "load vocal.wav, highpass 200 hz, slice into 8, insert at measure 16"

BEAT GENERATION:
  create [a] <genre> [style] beat [with 808s] [at <bpm> bpm] [in key of <key>] [<bars> bars]

  Genres: memphis, trap, lofi, boom bap, drill

  Examples:
    "create a memphis style beat with 808s at 170 bpm"
    "make a trap beat in key of Dm with 808s"
    "generate a lofi beat at 80 bpm 8 bars"

KEYS: C, Dm, F#, Bbm, etc. (append 'm' for minor)
"""


# Example usage functions
def parse_command(command: str) -> Dict[str, Any]:
    """
    Convenience function to parse a command.

    Args:
        command: Natural language command

    Returns:
        Parsed command dictionary
    """
    parser = CommandParser()
    return parser.parse(command)
