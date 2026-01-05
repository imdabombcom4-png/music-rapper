"""
FL Studio Controller Module
Interfaces with FL Studio via MIDI, Python API, and command line.
"""

import mido
import subprocess
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
import yaml


class FLStudioController:
    """Control FL Studio for pattern insertion and project manipulation."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize FL Studio controller.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.fl_path = self.config['fl_studio']['executable_path']
        self.projects_dir = Path(self.config['fl_studio']['projects_dir'])
        self.samples_dir = Path(self.config['fl_studio']['samples_dir'])
        self.midi_port = self.config['fl_studio']['midi_port']

        self.midi_output = None
        self._setup_midi()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_midi(self):
        """Setup MIDI connection to FL Studio."""
        try:
            available_ports = mido.get_output_names()
            print(f"Available MIDI ports: {available_ports}")

            # Try to find FL Studio's MIDI port
            for port_name in available_ports:
                if self.midi_port.lower() in port_name.lower():
                    self.midi_output = mido.open_output(port_name)
                    print(f"Connected to {port_name}")
                    return

            # If FL Studio port not found, use first available
            if available_ports:
                self.midi_output = mido.open_output(available_ports[0])
                print(f"Using default port: {available_ports[0]}")
        except Exception as e:
            print(f"MIDI setup failed: {e}")
            print("FL Studio control will be limited without MIDI connection")

    def open_project(self, project_name: str):
        """
        Open an FL Studio project.

        Args:
            project_name: Name of the project file (without path)
        """
        project_path = self.projects_dir / project_name
        if not project_path.exists():
            print(f"Creating new project: {project_path}")
            project_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.Popen([self.fl_path, str(project_path)])
            time.sleep(2)  # Wait for FL Studio to open
        except Exception as e:
            print(f"Failed to open FL Studio: {e}")

    def insert_sample_at_position(self, sample_path: str, bar: int, beat: int = 1, channel: int = 1):
        """
        Insert a sample at a specific position in the FL Studio timeline.

        Args:
            sample_path: Path to the sample file
            bar: Bar number (measure)
            beat: Beat within the bar (1-4)
            channel: Channel/track number to insert into

        Note: This uses MIDI commands. For full automation, FL Studio's Python API
        or command scripts would be more robust.
        """
        if not self.midi_output:
            print("No MIDI connection available. Cannot insert sample.")
            return

        # Copy sample to FL Studio samples directory
        sample_file = Path(sample_path)
        dest_path = self.samples_dir / sample_file.name

        try:
            import shutil
            shutil.copy2(sample_path, dest_path)
            print(f"Sample copied to: {dest_path}")
        except Exception as e:
            print(f"Failed to copy sample: {e}")

        # Calculate position in MIDI ticks
        # FL Studio uses PPQN (Pulses Per Quarter Note), typically 96
        ppqn = 96
        position_ticks = ((bar - 1) * 4 + (beat - 1)) * ppqn

        print(f"Sample ready to insert at Bar {bar}, Beat {beat}")
        print(f"Position: {position_ticks} ticks")
        print(f"Path: {dest_path}")

    def send_midi_note(self, note: int, velocity: int, duration: float = 0.5, channel: int = 0):
        """
        Send a MIDI note to FL Studio.

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            duration: Note duration in seconds
            channel: MIDI channel
        """
        if not self.midi_output:
            print("No MIDI connection available")
            return

        # Note on
        msg_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
        self.midi_output.send(msg_on)

        # Wait for duration
        time.sleep(duration)

        # Note off
        msg_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
        self.midi_output.send(msg_off)

    def create_pattern(self, pattern_name: str, notes: List[Dict[str, Any]], channel: int = 0):
        """
        Create a pattern by sending MIDI notes.

        Args:
            pattern_name: Name for the pattern
            notes: List of note dictionaries with 'note', 'velocity', 'time', 'duration'
            channel: MIDI channel

        Example:
            notes = [
                {'note': 60, 'velocity': 100, 'time': 0.0, 'duration': 0.5},
                {'note': 64, 'velocity': 100, 'time': 0.5, 'duration': 0.5},
            ]
        """
        if not self.midi_output:
            print("No MIDI connection available")
            return

        print(f"Creating pattern: {pattern_name}")

        for note_data in notes:
            wait_time = note_data.get('time', 0)
            time.sleep(wait_time)

            self.send_midi_note(
                note=note_data['note'],
                velocity=note_data['velocity'],
                duration=note_data.get('duration', 0.5),
                channel=channel
            )

    def set_tempo(self, bpm: int):
        """
        Set project tempo.

        Args:
            bpm: Beats per minute
        """
        print(f"Setting tempo to {bpm} BPM")
        # This would require FL Studio Python API access
        # For now, log the command
        print("Note: Tempo setting requires FL Studio Python API")

    def create_flp_script(self, script_content: str, script_name: str = "automation_script.pyscript"):
        """
        Create an FL Studio Python script file.

        Args:
            script_content: Python script content
            script_name: Name for the script file

        This creates a script that can be run from FL Studio's Script menu.
        """
        script_path = self.projects_dir / script_name

        with open(script_path, 'w') as f:
            f.write(script_content)

        print(f"FL Studio script created: {script_path}")
        print("Load this script in FL Studio via Tools > Scripting > Load script")

        return script_path

    def generate_sample_insert_script(self, sample_path: str, bar: int, beat: int, channel: int = 0) -> str:
        """
        Generate FL Studio Python script to insert a sample.

        Args:
            sample_path: Path to sample
            bar: Bar number
            beat: Beat number
            channel: Channel number

        Returns:
            Python script content
        """
        script = f"""
# FL Studio Python Script - Auto-generated
import channels
import patterns
import playlist

# Sample path
sample_path = r"{sample_path}"

# Position
bar = {bar}
beat = {beat}
channel = {channel}

# Calculate position in beats
position = (bar - 1) * 4 + (beat - 1)

# Load sample to channel
channels.addOneShot()
channels.setChannelName(channel, "AutoSample")
# Note: Full sample loading requires additional FL Studio API calls

print(f"Sample ready to insert at bar {{bar}}, beat {{beat}}")
"""
        return script

    def close(self):
        """Close MIDI connection."""
        if self.midi_output:
            self.midi_output.close()
            print("MIDI connection closed")
