import numpy as np
import pypianoroll

# --- Step 1: Load the data using NumPy ---
file_path = 'src/Jsb16thSeparated.npz'
# Use allow_pickle=True if you encounter an object array error
data = np.load(file_path, encoding="bytes", allow_pickle=True)

# --- Step 2: Select the data you want to convert ---
# The file contains 'test', 'train', and 'valid' arrays. Let's use the training data.
train_data = data['train']

# The shape is likely (num_songs, num_timesteps, num_pitches, num_tracks).
# We'll convert the first song (at index 0).
song_pianoroll = train_data[0]

# --- Step 3: Manually create a Multitrack object ---
# The JS Bach Chorale dataset is usually quantized to 16th notes (4 per beat)
# and has 4 tracks (Soprano, Alto, Tenor, Bass).
beat_resolution = 4
multitrack = pypianoroll.Multitrack(resolution=beat_resolution, name='Bach Chorale')

# Get the number of tracks from the data's shape
num_tracks = song_pianoroll.shape[-1]
track_names = ['Soprano', 'Alto', 'Tenor', 'Bass']

# For each track in the song, create a pypianoroll.Track object
for i in range(num_tracks):
    # Extract the piano roll for the current track
    track_pianoroll = song_pianoroll[:, i]

    # Create the track. Program=0 is Acoustic Grand Piano.
    track = pypianoroll.Track(
        pianoroll=track_pianoroll,
        program=0,
        is_drum=False,
        name=track_names[i]
    )
    multitrack.tracks.append(track)

# --- Step 4: Write the Multitrack object to a MIDI file ---
output_midi_path = 'output_song1.mid'
multitrack.write(output_midi_path)

print(f"Successfully converted and saved to {output_midi_path}")