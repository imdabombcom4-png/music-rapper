# FL Studio Music Automation 🎵

Control FL Studio with natural language commands for sample processing and beat creation.

## Features

- **Sample Processing**: Pitch shift, time stretch, filter, and slice audio samples
- **Beat Generation**: Create genre-specific drum patterns (Memphis, Trap, Lo-fi, Boom Bap, Drill)
- **808 Basslines**: Generate bouncy, rolling, or simple 808 patterns
- **Natural Language Commands**: Control everything with plain English
- **FL Studio Integration**: Direct MIDI communication and Python scripting
- **Interactive CLI**: Real-time command execution

## Installation

### Prerequisites

- Python 3.8+
- FL Studio 20+ (with Python API enabled)
- Windows/macOS/Linux

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd music-rapper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure FL Studio paths**

   Copy `.env.example` to `.env` and update with your paths:
   ```bash
   cp .env.example .env
   ```

   Edit `config.yaml` to set:
   - FL Studio executable path
   - Projects directory
   - Samples directory
   - MIDI port name

4. **Enable FL Studio MIDI**

   In FL Studio:
   - Options → MIDI Settings
   - Enable your MIDI input device
   - Set to "FL Studio MIDI" or note the port name for config.yaml

## Usage

### Interactive Mode

Start the interactive CLI:

```bash
python main.py
```

You'll see:
```
FL Studio Music Automation - Interactive Mode
Type 'help' for command syntax, 'quit' to exit

fl-studio>
```

### Single Command Mode

Execute a single command:

```bash
python main.py -c "create a trap beat with 808s at 140 bpm"
```

## Command Examples

### Sample Processing

#### Basic Pitch Shift
```
take sample.wav, pitch down 3 semitones, insert at bar 40 beat 3
```

#### Time Stretch
```
load vocal.wav, pitch down 5 semitones, stretch by 0.82, insert at bar 16
```

#### Filter and Slice
```
use drums.wav, lowpass 5000 hz, slice into 8, insert at measure 8
```

#### Complex Chain
```
take melody.flac, pitch up 7 semitones, stretch by 1.2, highpass 200 hz, insert at bar 1
```

### Beat Generation

#### Memphis Style
```
create a memphis style beat with 808s at 170 bpm
```

#### Trap Beat
```
make a trap beat in key of Dm with 808s
```

#### Lo-fi Hip-Hop
```
generate a lofi beat at 80 bpm 8 bars
```

#### Boom Bap
```
create a boom bap beat at 90 bpm in key of Am
```

#### Drill
```
make a drill beat with 808s at 145 bpm in key of C#m 4 bars
```

## Command Syntax

### Sample Processing Commands

```
take <file> [operations] insert at bar <N> [beat <N>]
```

**Operations:**
- `pitch up/down <N> semitones` - Pitch shift
- `stretch by <factor>` - Time stretch (< 1.0 slows down, > 1.0 speeds up)
- `lowpass/highpass/bandpass <freq> hz` - Apply filter
- `slice into <N>` - Slice into N equal parts

**Position:**
- `bar <N> beat <N>` - Specific bar and beat
- `measure <N>` - End of measure N

### Beat Generation Commands

```
create [a] <genre> [style] beat [with 808s] [at <bpm> bpm] [in key of <key>] [<bars> bars]
```

**Genres:**
- `memphis` - 160-180 BPM, rolling hi-hats, snappy snares
- `trap` - 130-150 BPM, sparse kicks, rolling hi-hats
- `lofi` - 70-90 BPM, laid-back, swung hi-hats
- `boom bap` - 85-95 BPM, heavy kick and snare
- `drill` - 140-150 BPM, dark, rolling 808s

**Keys:**
- Major: `C`, `D`, `F#`, `Bb`, etc.
- Minor: `Cm`, `Dm`, `F#m`, `Bbm`, etc.

## Project Structure

```
music-rapper/
├── src/
│   ├── __init__.py
│   ├── sample_processor.py    # Audio manipulation
│   ├── fl_controller.py        # FL Studio integration
│   ├── music_generator.py      # Beat generation
│   ├── pattern_builder.py      # Drum patterns
│   └── command_parser.py       # Natural language parsing
├── examples/
│   └── sample_commands.txt     # Example commands
├── tests/
│   └── test_sample_processor.py
├── main.py                      # Entry point
├── config.yaml                  # Configuration
├── requirements.txt
└── README.md
```

## Module Reference

### SampleProcessor

Handles audio manipulation:

```python
from src.sample_processor import SampleProcessor

processor = SampleProcessor()
audio, sr = processor.load_sample("sample.wav")
shifted = processor.pitch_shift(audio, semitones=-3)
stretched = processor.time_stretch(audio, rate=0.82)
slices = processor.slice_sample(audio, num_slices=8)
```

### FLStudioController

Interfaces with FL Studio:

```python
from src.fl_controller import FLStudioController

fl = FLStudioController()
fl.insert_sample_at_position("sample.wav", bar=40, beat=3)
fl.send_midi_note(note=60, velocity=100)
fl.create_pattern("my_pattern", notes=[...])
```

### MusicGenerator

Generates musical patterns:

```python
from src.music_generator import MusicGenerator

gen = MusicGenerator()
beat = gen.generate_beat(genre="trap", bpm=140, key="Dm", include_808=True)
melody = gen.generate_melody(key="C", scale="pentatonic_minor")
```

### PatternBuilder

Creates drum patterns and basslines:

```python
from src.pattern_builder import PatternBuilder

builder = PatternBuilder(bpm=140)
drums = builder.create_drum_pattern(style="memphis", bars=4)
bass = builder.create_808_bassline(root_note=36, pattern_type="bouncy")
```

## Configuration

Edit `config.yaml` to customize:

- **FL Studio paths**: Executable, projects, samples
- **MIDI settings**: Port name
- **Audio defaults**: Sample rate, tempo, key
- **Genre templates**: BPM ranges, swing, drum patterns
- **Pattern defaults**: Length, quantization

## Troubleshooting

### MIDI Connection Failed

1. Check FL Studio MIDI settings (Options → MIDI Settings)
2. Verify MIDI port name in `config.yaml` matches FL Studio
3. Ensure FL Studio is running when starting automation

### Sample Not Found

1. Check sample path is correct
2. Add sample directory to config.yaml `samples_dir`
3. Use absolute paths or place samples in configured directory

### Import Errors

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version (3.8+ required)
3. Install system audio libraries if needed (libsndfile, etc.)

## Advanced Usage

### FL Studio Python Scripts

Generate FL Studio Python scripts for advanced automation:

```python
fl = FLStudioController()
script = fl.generate_sample_insert_script("sample.wav", bar=40, beat=3)
fl.create_flp_script(script, "auto_insert.pyscript")
```

Load in FL Studio: Tools → Scripting → Load script

### Custom Genre Templates

Add your own genre templates in `config.yaml`:

```yaml
music:
  genres:
    my_genre:
      tempo_range: [120, 140]
      swing: 0.6
      typical_drums: ["snare", "hihat", "kick", "808"]
```

### Batch Processing

Process multiple samples:

```python
from src.sample_processor import SampleProcessor

processor = SampleProcessor()
samples = ["sample1.wav", "sample2.wav", "sample3.wav"]

for sample in samples:
    audio, sr = processor.load_sample(sample)
    audio = processor.pitch_shift(audio, -3)
    processor.save_sample(audio, f"processed_{sample}")
```

## Interactive Commands

While in interactive mode:

- `help` - Show command syntax
- `genres` - List available genres
- `scales` - List available musical scales
- `quit` - Exit

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Patterns

Edit `src/pattern_builder.py` to add new drum patterns:

```python
def _my_custom_pattern(self, bars: int, complexity: float) -> List[Dict[str, Any]]:
    notes = []
    # Add your pattern logic
    return notes
```

### Adding New Commands

Edit `src/command_parser.py` to add new command patterns:

```python
self.patterns['my_command'] = r'pattern_regex_here'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with librosa, soundfile, mido
- Inspired by FL Studio's powerful automation capabilities
- Music theory patterns from various hip-hop and electronic music traditions

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Happy music making! 🎹🎧**
