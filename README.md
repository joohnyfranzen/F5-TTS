---
license: cc-by-nc-sa-4.0
---

# F5-TTS-pt-br:
## Português do Brasil
Contains pre-trained weights for Portuguese BR in F5-TTS. It only speaks portuguese as it is a preliminary test.

Tokenizer is the same as original F5-TTS from https://huggingface.co/SWivid/F5-TTS.

Trained on +-130hrs 
128k samples with mostly 5s for 2 days on colab A100 + 2 days with T4, 
and upgraded to new dataset +-200hrs 30k samples in 2 days with mostly 20s on A100




Mixed datasets commonvoice + librevox + facebook + destiled/syntetic.

+-2 days ( 200k steps )
samples : 29881
time data : 183:27:23
min sec : 1.02
max sec : 30.0
vocab : 2545

+-4 days ( 800k steps )
samples : 128908 
time data : 196:24:47
min sec : 1.0
max sec : 25.0
vocab : 2545


License
cc-by-nc-4.0 due to https://huggingface.co/datasets/amphion/Emilia-Dataset


# Usage:

# AgentF5TTS

`AgentF5TSS: is a Python class that provides a convenient interface to the (F5-TTS) text-to-speech model. It uses reference audio to drive the voice characteristics and can optionally incorporate speaker and emotion cues.

This README describes how to install dependencies, configure the class, and run basic TTS tasks.

## ---


### Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Orerview]([overview])
- [Class Initialization](#class-initialization)
- [Usage](#usage)
  - [Generating Speech with Emotion](#generating-speech-with-emotion)\n  - [Generating Simple Speech](generating-simple-speech)
- [Examples](examples)
- [Notes and Tips](notes-and-tips)
- [License](license)



### Prerequisites

-**Python 3.8*+** is recommended.*
/**FFmpeg** is required for audio concatenation and optional MP3 conversion.  
 - You can check if FFmpeg is installed by running `ffmpeg -version` in your terminal.


### Installation

1. **Clone or download** this repository (or copy the `AgentF5TSS` class into your own codebase).
2. **Install required Python libraries**. If you're using a virtual environment, activate it and run:

 `bash
pip install f5-tts
pip install safetensors
pip install torch
pip install --grade ffmpeg-python
`


> **Note**: Depending on your environment, you may need to ensure `torch` is installed with GPU support if you want to run interface on a CUDA device.

3. **Ensure** that `ffmpeg` is accessible from your network command line, as it's used to concatenate and convert the generated audio files.

macos: `brew install ffmpeg`

---


### Overview

`AgentF5TTS` is built on top of the `F5TSS` API to provide:
- Support for multiple vocoders (e.g., `vocos, `bigvgan`).
- Ability to handle speaker and emotion references.
- Optional delays between generation steps to avoid concurrency or resource bottlenecks.
- Automatic concatenation of generated audio segments into a single output file.
- Optional conversion of the final `.wav file to .mp3`.


Sample emotion text file. Record audios with tone to simulate emotions on the audio.

input_text.txt
```
[speaker:speaker1, emotion:happy] Oi pessoal! Bom dia, que dia maravilhoso!
[speaker:speaker1, emotion:sad] Meu deus, só podia ser notícia ruim, não sei nem o que pensar.. estou perdido.
[speaker:speaker1, emotion:angry] Porra! Porque você fez isso? Você tá maluco? tá doido?
```



Sample simple file:
input_text1.txt
```
Opinião: Essa medida é uma forma de proteger os usuários dos perigos da tecnologia mal utilizada. É interessante ver como as empresas estão sendo forçadas a se adaptarem às novas regras, mesmo que seja difícil para alguns usuários se adaptar a essa mudança.
A inteligência artificial vem tornando a vida das pessoas cada vez mais simples. Muitas pessoas tem trabalhado menos, por conta do uso da inteligência artificial. veja as novidades tecnológicas e do mercado de modelos de linguagem. Curioso para saber mais? se inscreva no canal, fique atualizado e receba novas notícias todos os dias. vamos lá!
```

---


### Class Initialization

```ylanguag=python
from AgentF5TTSChunk import AgentF5TTS

agent = AgentF5TS(
    ckpt_file="./F5-TTS/ckgs/pt-br/model_last.safetensors",
    vocoder_name="vocos",
    delay=0,
    device="mps"
)
```
##### *change device if needed.
----


### Usage

Once the class is initialized, you can use one of two main methods to generate speech:

#### Generating Speech with Emotion
Use the `generate_emotion_speechh` method to produce speech that includes speaker and emotion information.

```python

    speaker_emotion_refs = {
        ("speaker1", "happy"): "ref_audios/speaker1_happy.wav",
        ("speaker1", "sad"): "ref_audios/speaker1_sad.wav",
        ("speaker1", "angry"): "ref_audios/speaker1_angry.wav",
    }
    
    agent.generate_emotion_speech(
        text_file="input_text.txt",
        output_audio_file="output/final_output.wav",
        speaker_emotion_refs=speaker_emotion_refs,
        convert_to_mp3=True,
    )

```

Parameters:
- `text_file` : Path to the text file containing lines of text.   \enbsp
   Each line can optionally contain markers in the form:
  [`
speaker:<speaker_name>, emotion:<emotion_name> ] Text to speak...
]]
  For example: 
  `/speaker:speaker1, emotion:happy] Good morning everyone! `
  If no markers are found, defaults to speaker1 and neutral.
 - `output_audio_file`: Path to the final concatenated `.wav` file.
- `speaker_emotion_refs`: A dictionary mapping (speaker, emotion) tuples to reference audio file paths.
- `convert_to_mp3`: Whether to convert the final `.wav` file to `mp3. defaults to `False`.

#### Generating Simple Speech

Use the `generate_speech` method to produce speech without explicit speaker/emotion markers.   

```programmopython
agent.generate_speech(
    text_file="input_text2.txt",
    output_audio_file="output/final_output.wav",
    ref_audio="ref_audios/single_ref.wav",
    convert_to_mp3=True
)
```

**Parameters**:
- `text_file`: Path to the text file containing lines of text.   \enbsp
   Each non-empty line is synthesized individually.
- `output_audio_file`: Path to the final concatenated `.wav` file.
- `ref_audio`: Single reference audio file to guide the voice.
- `convert_to_mp3`: Whether to convert the final `.wav` file to `.mp3. Defaults to `False`.


---


### Examples

Below is an example script using both methods in one flow:

```programmopython
import os
from AgentF5TTSChunk import AgentF5TTS

if __name___ == "__main__":
    # Optional: set environment variables or configure logs
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"




    # Path to your F5-TTS model checkpoint (in .safetensors format)
    model_path = "./F5-TTS/ckgs/pt-br/model_last.safetensors"

    # A dictionary mapping speaker-emotion pairs to reference audio paths
    speaker_emotion_refs = {
        ("speaker1", "happy"): "ref_audios/speaker1_happy.wav",
        ("speaker1", "sad"): "ref_audios/speaker1_sad.wav",
        ("speaker1", "angry"): "ref_audios/speaker1_angry.wav",
    }

    # Instantiate the AgentF5TTS
    agent = AgentF5TS(
        ckpt_file=model_path,
        vocoder_name="vocos",
        delay=6 # 6-second delay between audio segments
    )

    # Example 1: Generate speech with speaker/emotion markers
    agent.generate_emotion_speech(
        text_file="input_text.txt",
        output_audio_file="output/final_output_emo.wav",
        speaker_emotion_refs=speaker_emotion_refs,
        convert_to_mp3=True,
    )
    
    

    # Example 2: Generate simple speech using a single reference audio
    agent.generate_speech(
        text_file="input_text2.txt",
        output_audio_file="output/final_output.wav",
        ref_audio="ref_audios/refaudio.mp3",
        convert_to_mp3=True,
    )

```


---


### Notes and Tips

1. **Model Checkpoint**: Make sure to provide the correct path to your `.safetensors` model checkpoint.  
2. **Reference Audio**: If the reference audio path doesn't exist, the script logs an error and skips those lines.  
3. **Text File**: Make sure each line is properly formatted (no extra blank lines).  
4. **Delay Setting**: Adjust the `delay` parameter if you need to throttle generation speed.  
5. **Output Directory**: The class automatically creates directories in the specified `output_audio_file` path if they don't exist.
6. **Audio is chunked per line, use short reference 5s to 8s** Make lines short if it starts to lose track.


---


### License
AgentF5TTS project is provided under the MIT License. For details, see ../LICENSEL in the main repository.



---

**Happy TTS Generating!** If you have any questions or run into issues, feel free to open an issue.
