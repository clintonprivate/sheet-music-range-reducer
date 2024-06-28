import music21
import os

def process_midi_file(input_file, output_midi_file, output_mxl_file):
    # Load the MIDI file
    score = music21.converter.parse(input_file)
    
    # Define the range of a 61-key piano
    min_pitch = music21.pitch.Pitch('C2').midi
    max_pitch = music21.pitch.Pitch('C7').midi
    
    for part in score.parts:
        for note in part.flat.notes:
            if isinstance(note, music21.note.Note):
                if note.pitch.midi < min_pitch:
                    note.pitch.midi += 12
                elif note.pitch.midi > max_pitch:
                    note.pitch.midi -= 12
            elif isinstance(note, music21.chord.Chord):
                for chord_note in note:
                    if chord_note.pitch.midi < min_pitch:
                        chord_note.pitch.midi += 12
                    elif chord_note.pitch.midi > max_pitch:
                        chord_note.pitch.midi -= 12
    
    # Save the modified score to a new MIDI file
    score.write('midi', output_midi_file)
    # Save the modified score to a new MXL file
    score.write('mxl', output_mxl_file)

def add_suffix_to_filename(file_path, suffix):
    base, ext = os.path.splitext(file_path)
    return f"{base}{suffix}{ext}"

# Define the directory containing MIDI files
input_directory = 'Reduce'

# Ensure the directory exists
if os.path.isdir(input_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            input_file = os.path.join(input_directory, filename)
            output_midi_file = add_suffix_to_filename(input_file, " - Reduced")
            output_mxl_file = add_suffix_to_filename(output_midi_file, ".mxl")
            
            # Ensure the input file exists
            if os.path.exists(input_file):
                process_midi_file(input_file, output_midi_file, output_mxl_file)
                print(f"Processed file saved as {output_midi_file} and {output_mxl_file}")
else:
    print(f"Input directory {input_directory} does not exist.")
