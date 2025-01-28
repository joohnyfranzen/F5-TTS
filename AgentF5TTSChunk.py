import os
import re
import time
import logging
import subprocess
from f5_tts.api import F5TTS  # Correct import for F5-TTS API



logging.basicConfig(level=logging.INFO)


class AgentF5TTS:
    def __init__(self, ckpt_file, vocoder_name="vocos", delay=0, device="mps"):
        """
        Initialize the F5-TTS Agent.

        :param ckpt_file: Path to the safetensors model checkpoint.
        :param vocoder_name: Name of the vocoder to use ("vocos" or "bigvgan").
        :param delay: Delay in seconds between audio generations.
        :param device: Device to use ("cpu", "cuda", "mps").
        """
        self.model = F5TTS(ckpt_file=ckpt_file, vocoder_name=vocoder_name, device=device)
        self.delay = delay  # Delay in seconds

    def generate_emotion_speech(self, text_file, output_audio_file, speaker_emotion_refs, convert_to_mp3=False):
        """
        Generate speech using the F5-TTS model.

        :param text_file: Path to the input text file.
        :param output_audio_file: Path to save the combined audio output.
        :param speaker_emotion_refs: Dictionary mapping (speaker, emotion) tuples to reference audio paths.
        :param convert_to_mp3: Boolean flag to convert the output to MP3.
        """
        try:
            with open(text_file, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logging.error(f"Text file not found: {text_file}")
            return

        if not lines:
            logging.error("Input text file is empty.")
            return

        temp_files = []
        os.makedirs(os.path.dirname(output_audio_file), exist_ok=True)

        for i, line in enumerate(lines):
            
            speaker, emotion = self._determine_speaker_emotion(line)
            ref_audio = speaker_emotion_refs.get((speaker, emotion))
            line = re.sub(r'\[speaker:.*?\]\s*', '', line)
            if not ref_audio or not os.path.exists(ref_audio):
                logging.error(f"Reference audio not found for speaker '{speaker}', emotion '{emotion}'.")
                continue

            ref_text = ""  # Placeholder or load corresponding text
            temp_file = f"{output_audio_file}_line{i + 1}.wav"

            try:
                logging.info(f"Generating speech for line {i + 1}: '{line}' with speaker '{speaker}', emotion '{emotion}'")
                self.model.infer(
                    ref_file=ref_audio,
                    ref_text=ref_text,
                    gen_text=line,
                    file_wave=temp_file,
                    remove_silence=True,
                )
                temp_files.append(temp_file)
                time.sleep(self.delay)
            except Exception as e:
                logging.error(f"Error generating speech for line {i + 1}: {e}")

        self._combine_audio_files(temp_files, output_audio_file, convert_to_mp3)



    def generate_speech(self, text_file, output_audio_file, ref_audio, convert_to_mp3=False):
        try:
            with open(text_file, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logging.error(f"Text file not found: {text_file}")
            return

        if not lines:
            logging.error("Input text file is empty.")
            return

        temp_files = []
        os.makedirs(os.path.dirname(output_audio_file), exist_ok=True)

        for i, line in enumerate(lines):
            
            if not ref_audio or not os.path.exists(ref_audio):
                logging.error(f"Reference audio not found for speaker.")
                continue
            temp_file = f"{output_audio_file}_line{i + 1}.wav"

            try:
                logging.info(f"Generating speech for line {i + 1}: '{line}'")
                self.model.infer(
                    ref_file=ref_audio,  # No reference audio
                    ref_text="",  # No reference text
                    gen_text=line,
                    file_wave=temp_file,
                )
                temp_files.append(temp_file)
            except Exception as e:
                logging.error(f"Error generating speech for line {i + 1}: {e}")

        # Combine temp_files into output_audio_file if needed
        self._combine_audio_files(temp_files, output_audio_file, convert_to_mp3)




    def _determine_speaker_emotion(self, text):
        """
        Extract speaker and emotion from the text using regex.
        Default to "speaker1" and "neutral" if not specified.
        """
        speaker, emotion = "speaker1", "neutral"  # Default values

        # Use regex to find [speaker:speaker_name, emotion:emotion_name]
        match = re.search(r"\[speaker:(.*?), emotion:(.*?)\]", text)
        if match:
            speaker = match.group(1).strip()
            emotion = match.group(2).strip()

        logging.info(f"Determined speaker: '{speaker}', emotion: '{emotion}'")
        return speaker, emotion

    def _combine_audio_files(self, temp_files, output_audio_file, convert_to_mp3):
        """Combine multiple audio files into a single file using FFmpeg."""
        if not temp_files:
            logging.error("No audio files to combine.")
            return

        list_file = "file_list.txt"
        with open(list_file, "w") as f:
            for temp in temp_files:
                f.write(f"file '{temp}'\n")

        try:
            subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_audio_file], check=True)
            if convert_to_mp3:
                mp3_output = output_audio_file.replace(".wav", ".mp3")
                subprocess.run(["ffmpeg", "-y", "-i", output_audio_file, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_output], check=True)
                logging.info(f"Converted to MP3: {mp3_output}")
            for temp in temp_files:
                os.remove(temp)
            os.remove(list_file)
        except Exception as e:
            logging.error(f"Error combining audio files: {e}")


# Example usage, remove from this line on to import into other agents.
# make sure to adjust the paths to yourr files.
if __name__ == "__main__":
    
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    model_path = "./F5-TTS/ckpts/pt-br/model_last.safetensors"
    speaker_emotion_refs = {
        ("speaker1", "happy"): "ref_audios/speaker1_happy.wav",
        ("speaker1", "sad"): "ref_audios/speaker1_sad.wav",
        ("speaker1", "angry"): "ref_audios/speaker1_angry.wav",
    }
    agent = AgentF5TTS(ckpt_file=model_path, vocoder_name="vocos", delay=6)
    
    agent.generate_emotion_speech(
        text_file="input_text.txt",
        output_audio_file="output/final_output_emo.wav",
        speaker_emotion_refs=speaker_emotion_refs,
        convert_to_mp3=True,
    )
    
    agent.generate_speech(
        text_file="input_text2.txt",
        output_audio_file="output/final_output.wav",
        ref_audio="ref_audios/refaudio.mp3",
        convert_to_mp3=True,
    )




