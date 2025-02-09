import os
import re
import time
import logging
import subprocess
from f5_tts.api import F5TTS 
import argparse
from num2words import num2words

logging.basicConfig(level=logging.INFO)

class AgentF5TTS:
    def __init__(self, ckpt_file, vocoder_name="vocos", delay=0, device="cuda"):
        self.model = F5TTS(ckpt_file=ckpt_file, vocoder_name=vocoder_name, device=device)
        self.delay = delay

    def _convert_numbers_to_words(self, text, lang='pt'):
        def replace_number(match):
            num_str = match.group().replace(".", "").replace(",", ".")
            try:
                return num2words(float(num_str), lang=lang)
            except ValueError:
                return match.group()  
        return re.sub(r'\d+[.,]?\d*', replace_number, text)

    def _remove_unwanted_characters(self, text):
        unwanted_chars = r"[/\\*]" 
        return re.sub(unwanted_chars, "", text)

    def generate_speech(self, text_file, output_dir, ref_audio, convert_to_mp3=False):
        try:
            with open(text_file, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logging.error(f"Text file not found: {text_file}")
            return

        if not lines:
            logging.error("Input text file is empty.")
            return

        os.makedirs(output_dir, exist_ok=True)

        for i, line in enumerate(lines):
            if not ref_audio or not os.path.exists(ref_audio):
                logging.error(f"Reference audio not found for speaker.")
                continue

            line = self._remove_unwanted_characters(line)
            line = self._convert_numbers_to_words(line, lang=args.language)
            output_file = os.path.join(output_dir, f"{i+1}.wav")

            try:
                logging.info(f"Generating speech for line {i + 1}: '{line}'")
                self.model.infer(
                    ref_file=ref_audio,
                    ref_text="",
                    gen_text=line,
                    file_wave=output_file,
                )

                if convert_to_mp3:
                    mp3_output = output_file.replace(".wav", ".mp3")
                    subprocess.run(["ffmpeg", "-y", "-i", output_file, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_output], check=True)
                    logging.info(f"Converted to MP3: {mp3_output}")

            except Exception as e:
                logging.error(f"Error generating speech for line {i + 1}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate speech using F5-TTS.")
    parser.add_argument("--ckpt_file", required=True, help="Path to the model checkpoint.")
    parser.add_argument("--text_file", required=True, help="Path to the input text file.")
    parser.add_argument("--output_dir", required=True, help="Directory to save the generated audio files.")
    parser.add_argument("--ref_audio", required=True, help="Path to reference audio file.")
    parser.add_argument("--language", required=True, help="Language used for num2words conversion")
    parser.add_argument("--convert_to_mp3", action="store_true", help="Convert the output to MP3.")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds between audio generations.")
    parser.add_argument("--vocoder_name", default="vocos", help="Vocoder name to use ('vocos' or 'bigvgan').")
    parser.add_argument("--device", default="cuda", help="Device to use ('cpu', 'cuda', 'mps').")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    agent = AgentF5TTS(
        ckpt_file=args.ckpt_file,
        vocoder_name=args.vocoder_name,
        delay=args.delay,
        device=args.device
    )

    agent.generate_speech(
        text_file=args.text_file,
        output_dir=args.output_dir,
        ref_audio=args.ref_audio,
        convert_to_mp3=args.convert_to_mp3
    )
