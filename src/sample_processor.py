"""
Sample Processing Module
Handles audio manipulation: pitch shifting, time stretching, slicing, and effects.
"""

import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pathlib import Path
from typing import Optional, List, Tuple


class SampleProcessor:
    """Process audio samples with various transformations."""

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def load_sample(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load an audio file.

        Args:
            file_path: Path to audio file

        Returns:
            Tuple of (audio_data, sample_rate)
        """
        audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=False)
        return audio, sr

    def pitch_shift(self, audio: np.ndarray, semitones: float, sr: int = None) -> np.ndarray:
        """
        Pitch shift audio by semitones.

        Args:
            audio: Audio data
            semitones: Number of semitones to shift (positive or negative)
            sr: Sample rate

        Returns:
            Pitch-shifted audio
        """
        sr = sr or self.sample_rate

        # Handle stereo/mono
        if audio.ndim == 2:
            shifted = np.array([
                librosa.effects.pitch_shift(audio[0], sr=sr, n_steps=semitones),
                librosa.effects.pitch_shift(audio[1], sr=sr, n_steps=semitones)
            ])
        else:
            shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=semitones)

        return shifted

    def time_stretch(self, audio: np.ndarray, rate: float) -> np.ndarray:
        """
        Time stretch audio by a rate factor.

        Args:
            audio: Audio data
            rate: Stretch rate (< 1.0 slows down, > 1.0 speeds up)

        Returns:
            Time-stretched audio
        """
        if audio.ndim == 2:
            stretched = np.array([
                librosa.effects.time_stretch(audio[0], rate=rate),
                librosa.effects.time_stretch(audio[1], rate=rate)
            ])
        else:
            stretched = librosa.effects.time_stretch(audio, rate=rate)

        return stretched

    def slice_sample(self, audio: np.ndarray, num_slices: int, sr: int = None) -> List[np.ndarray]:
        """
        Slice audio into equal parts.

        Args:
            audio: Audio data
            num_slices: Number of slices to create
            sr: Sample rate

        Returns:
            List of audio slices
        """
        sr = sr or self.sample_rate

        # Calculate slice length
        total_length = audio.shape[-1]
        slice_length = total_length // num_slices

        slices = []
        for i in range(num_slices):
            start = i * slice_length
            end = start + slice_length if i < num_slices - 1 else total_length

            if audio.ndim == 2:
                slice_data = audio[:, start:end]
            else:
                slice_data = audio[start:end]

            slices.append(slice_data)

        return slices

    def detect_bpm(self, audio: np.ndarray, sr: int = None) -> float:
        """
        Detect the BPM of an audio sample.

        Args:
            audio: Audio data
            sr: Sample rate

        Returns:
            Detected BPM
        """
        sr = sr or self.sample_rate

        # Use first channel for stereo
        if audio.ndim == 2:
            audio = audio[0]

        tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
        return float(tempo)

    def apply_filter(self, audio: np.ndarray, filter_type: str, cutoff: float, sr: int = None) -> np.ndarray:
        """
        Apply a filter to audio.

        Args:
            audio: Audio data
            filter_type: 'lowpass', 'highpass', or 'bandpass'
            cutoff: Cutoff frequency in Hz
            sr: Sample rate

        Returns:
            Filtered audio
        """
        sr = sr or self.sample_rate

        if filter_type == 'lowpass':
            # Simple lowpass using librosa
            if audio.ndim == 2:
                filtered = np.array([
                    librosa.effects.preemphasis(audio[0], coef=-0.97),
                    librosa.effects.preemphasis(audio[1], coef=-0.97)
                ])
            else:
                filtered = librosa.effects.preemphasis(audio, coef=-0.97)
        elif filter_type == 'highpass':
            if audio.ndim == 2:
                filtered = np.array([
                    librosa.effects.preemphasis(audio[0], coef=0.97),
                    librosa.effects.preemphasis(audio[1], coef=0.97)
                ])
            else:
                filtered = librosa.effects.preemphasis(audio, coef=0.97)
        else:
            # Default to no filtering for now
            filtered = audio

        return filtered

    def save_sample(self, audio: np.ndarray, output_path: str, sr: int = None):
        """
        Save processed audio to file.

        Args:
            audio: Audio data
            output_path: Output file path
            sr: Sample rate
        """
        sr = sr or self.sample_rate
        sf.write(output_path, audio.T if audio.ndim == 2 else audio, sr)

    def process_command(self, file_path: str, operations: List[dict], output_path: Optional[str] = None) -> np.ndarray:
        """
        Process a sample with a series of operations.

        Args:
            file_path: Input audio file
            operations: List of operations like [{'type': 'pitch_shift', 'semitones': -3}, ...]
            output_path: Optional output path to save result

        Returns:
            Processed audio

        Example:
            operations = [
                {'type': 'pitch_shift', 'semitones': -3},
                {'type': 'time_stretch', 'rate': 0.82},
                {'type': 'filter', 'filter_type': 'lowpass', 'cutoff': 5000}
            ]
        """
        audio, sr = self.load_sample(file_path)

        for op in operations:
            op_type = op.get('type')

            if op_type == 'pitch_shift':
                audio = self.pitch_shift(audio, op['semitones'], sr)
            elif op_type == 'time_stretch':
                audio = self.time_stretch(audio, op['rate'])
            elif op_type == 'filter':
                audio = self.apply_filter(audio, op['filter_type'], op['cutoff'], sr)
            elif op_type == 'slice':
                # Return slices instead of continuing processing
                return self.slice_sample(audio, op['num_slices'], sr)

        if output_path:
            self.save_sample(audio, output_path, sr)

        return audio
