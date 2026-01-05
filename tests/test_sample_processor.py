"""
Tests for sample processor module.
"""

import unittest
import numpy as np
from src.sample_processor import SampleProcessor


class TestSampleProcessor(unittest.TestCase):
    """Test cases for SampleProcessor."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = SampleProcessor(sample_rate=44100)

    def test_pitch_shift(self):
        """Test pitch shifting."""
        # Create simple sine wave
        duration = 1.0
        freq = 440.0  # A4
        t = np.linspace(0, duration, int(self.processor.sample_rate * duration))
        audio = np.sin(2 * np.pi * freq * t)

        # Pitch shift up 12 semitones (one octave)
        shifted = self.processor.pitch_shift(audio, semitones=12)

        self.assertIsNotNone(shifted)
        self.assertEqual(shifted.shape, audio.shape)

    def test_time_stretch(self):
        """Test time stretching."""
        # Create simple audio
        duration = 1.0
        t = np.linspace(0, duration, int(self.processor.sample_rate * duration))
        audio = np.sin(2 * np.pi * 440 * t)

        # Stretch to half speed
        stretched = self.processor.time_stretch(audio, rate=0.5)

        self.assertIsNotNone(stretched)
        # Should be roughly twice as long
        self.assertGreater(len(stretched), len(audio) * 1.5)

    def test_slice_sample(self):
        """Test slicing audio."""
        # Create 4-second audio
        duration = 4.0
        audio = np.random.randn(int(self.processor.sample_rate * duration))

        # Slice into 8 parts
        slices = self.processor.slice_sample(audio, num_slices=8)

        self.assertEqual(len(slices), 8)
        # Each slice should be roughly equal length
        expected_length = len(audio) // 8
        for slice_audio in slices:
            self.assertGreater(len(slice_audio), expected_length * 0.9)

    def test_process_command(self):
        """Test command processing pipeline."""
        # This would require actual audio files
        # For now, just test that the method exists
        operations = [
            {'type': 'pitch_shift', 'semitones': -3},
            {'type': 'time_stretch', 'rate': 0.82},
        ]

        # Would need actual file for full test
        # self.processor.process_command('test.wav', operations)
        self.assertTrue(hasattr(self.processor, 'process_command'))


if __name__ == '__main__':
    unittest.main()
