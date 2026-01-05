#!/usr/bin/env python3
"""
FL Studio Music Automation
Main entry point for controlling FL Studio with natural language commands.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

from src.command_parser import CommandParser
from src.sample_processor import SampleProcessor
from src.fl_controller import FLStudioController
from src.music_generator import MusicGenerator


class FLStudioAutomation:
    """Main automation controller."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize FL Studio automation.

        Args:
            config_path: Path to configuration file
        """
        self.parser = CommandParser()
        self.sample_processor = SampleProcessor()
        self.fl_controller = FLStudioController(config_path)
        self.music_generator = MusicGenerator()

    def execute_command(self, command: str):
        """
        Execute a natural language command.

        Args:
            command: Natural language command string
        """
        print(f"\n> {command}")
        print("-" * 60)

        # Parse command
        parsed = self.parser.parse(command)
        print(f"Command type: {parsed['type']}")

        if parsed['type'] == 'sample_process':
            self._handle_sample_processing(parsed)
        elif parsed['type'] == 'generate_beat':
            self._handle_beat_generation(parsed)
        elif parsed['type'] == 'unknown':
            print("Could not parse command. Use 'help' for command syntax.")
            print(f"Raw: {parsed['raw']}")
        else:
            print(f"Unknown command type: {parsed['type']}")

    def _handle_sample_processing(self, parsed: Dict):
        """Handle sample processing command."""
        print("\nSample Processing:")
        print(f"  Sample: {parsed['sample_path']}")
        print(f"  Operations: {len(parsed['operations'])}")

        for i, op in enumerate(parsed['operations'], 1):
            print(f"    {i}. {op}")

        print(f"  Insert at: Bar {parsed['insert_bar']}, Beat {parsed['insert_beat']}")

        # Validate sample path
        sample_path = self.parser.validate_sample_path(
            parsed['sample_path'],
            search_dirs=[str(self.fl_controller.samples_dir)]
        )

        if not sample_path:
            print(f"\nError: Sample not found: {parsed['sample_path']}")
            print(f"Searched in: {self.fl_controller.samples_dir}")
            return

        print(f"\nProcessing sample: {sample_path}")

        try:
            # Process the sample
            output_path = Path(sample_path).stem + "_processed.wav"
            output_full = self.fl_controller.samples_dir / output_path

            processed_audio = self.sample_processor.process_command(
                file_path=sample_path,
                operations=parsed['operations'],
                output_path=str(output_full)
            )

            print(f"Processed sample saved: {output_full}")

            # Insert into FL Studio
            if parsed['insert_bar']:
                self.fl_controller.insert_sample_at_position(
                    sample_path=str(output_full),
                    bar=parsed['insert_bar'],
                    beat=parsed['insert_beat']
                )
                print(f"Sample inserted at Bar {parsed['insert_bar']}, Beat {parsed['insert_beat']}")

        except Exception as e:
            print(f"Error processing sample: {e}")
            import traceback
            traceback.print_exc()

    def _handle_beat_generation(self, parsed: Dict):
        """Handle beat generation command."""
        print("\nBeat Generation:")
        print(f"  Genre: {parsed['genre']}")
        print(f"  BPM: {parsed['bpm'] or 'auto'}")
        print(f"  Key: {parsed['key']}")
        print(f"  Bars: {parsed['bars']}")
        print(f"  Include 808s: {parsed['include_808']}")

        try:
            # Generate beat
            beat_data = self.music_generator.generate_beat(
                genre=parsed['genre'],
                bpm=parsed['bpm'],
                key=parsed['key'],
                bars=parsed['bars'],
                include_808=parsed['include_808']
            )

            print(f"\nGenerated {parsed['genre']} beat:")
            print(f"  BPM: {beat_data['bpm']}")
            print(f"  Key: {beat_data['key']} {beat_data['scale']}")
            print(f"  Drum hits: {len(beat_data['drum_pattern'])}")
            print(f"  Bass notes: {len(beat_data['bass_pattern'])}")
            print(f"  Total events: {len(beat_data['combined_pattern'])}")

            # Send to FL Studio via MIDI
            print("\nSending pattern to FL Studio...")
            self.fl_controller.create_pattern(
                pattern_name=f"{parsed['genre']}_{beat_data['bpm']}bpm",
                notes=beat_data['combined_pattern']
            )

            print("Pattern sent! Check FL Studio.")

        except Exception as e:
            print(f"Error generating beat: {e}")
            import traceback
            traceback.print_exc()

    def interactive_mode(self):
        """Run in interactive mode."""
        print("=" * 60)
        print("FL Studio Music Automation - Interactive Mode")
        print("=" * 60)
        print("\nType 'help' for command syntax, 'quit' to exit\n")

        while True:
            try:
                command = input("fl-studio> ").strip()

                if not command:
                    continue

                if command.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                if command.lower() == 'help':
                    print(self.parser.format_help())
                    continue

                if command.lower() == 'genres':
                    print("\nAvailable genres:")
                    for genre in self.music_generator.list_genres():
                        info = self.music_generator.get_genre_info(genre)
                        print(f"  - {genre}: {info['tempo_range'][0]}-{info['tempo_range'][1]} BPM")
                    continue

                if command.lower() == 'scales':
                    print("\nAvailable scales:")
                    for scale in self.music_generator.list_scales():
                        print(f"  - {scale}")
                    continue

                # Execute command
                self.execute_command(command)

            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()

    def close(self):
        """Clean up resources."""
        self.fl_controller.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="FL Studio Music Automation - Control FL Studio with natural language"
    )
    parser.add_argument(
        '-c', '--command',
        type=str,
        help='Execute a single command and exit'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (default if no command given)'
    )

    args = parser.parse_args()

    # Initialize automation
    automation = FLStudioAutomation(config_path=args.config)

    try:
        if args.command:
            # Single command mode
            automation.execute_command(args.command)
        else:
            # Interactive mode
            automation.interactive_mode()
    finally:
        automation.close()


if __name__ == '__main__':
    main()
