# README - AgentF5TTS

Este projeto utiliza o modelo **F5-TTS** para gerar fala sintetizada a partir de um arquivo de texto. O modelo foi treinado pela **firstpixel** e é baseado no trabalho do criador **SWivid**. O código foi adaptado para facilitar a geração de áudio em português brasileiro (pt-br) e suporta a conversão de arquivos de saída para MP3.

---

## Créditos

- **Modelo F5-TTS**: [firstpixel/F5-TTS-pt-br](https://huggingface.co/firstpixel/F5-TTS-pt-br)
- **Criador do Projeto**: [SWivid/F5-TTS](https://huggingface.co/SWivid/F5-TTS)
- **Voz Utilizada**: [Leandro/Vox Forge](https://www.voxforge.org/home/downloads/speech/portuguese-speech-files/leandro-20141007-fmw#IyWYVieK6ZXufm_oX1jyig)

---

## Requisitos

Antes de executar o código, certifique-se de que o ambiente de desenvolvimento está configurado corretamente. Você precisará de:

- **Python 3.10 ou superior**
- **FFmpeg** instalado na máquina (para conversão de áudio)

### Configuração do Ambiente Python

1. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```
2. **Ative o ambiente virtual**:

   - No Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
     **Observação**: O código foi testado em um Ubuntu 22.04

3. **Instale as dependências**:
   No terminal, execute os seguintes comandos para instalar as dependências necessárias:

   ```bash
   pip install wheel
   pip install f5-tts
   pip install safetensors
   pip install torch
   pip install jieba transformers_stream_generator
   pip install num2words
   pip install --upgrade ffmpeg-python
   ```

   **Observação**: Se houve demora na instalação, tente algum ou ambos antes do nome do pacote.

   ```
   --no-cache-dir --use-deprecated=legacy-resolver
   ```

4. **Baixe um modelo compatível**. Apenas o arquivo `model_last.safetensors` é necessário para o uso:
   [https://huggingface.co/firstpixel/F5-TTS-pt-br](https://huggingface.co/firstpixel/F5-TTS-pt-br)

## Como Usar

### Estrutura do Projeto

Certifique-se de que a estrutura do projeto esteja organizada da seguinte forma:

```bash
/projeto
│
├── AgentF5TTSChunk.py
├── input_text.txt
├── ckpt/
│       └── pt-br/
│               └── model_last.safetensors
├── ref_audio/
│           └── pt-br/
│                   └── Leandro.wav
├── output/
└── venv/
```

### Executando o Script

Para gerar áudio a partir de um arquivo de texto, execute o seguinte comando no terminal:

```bash
python3 AgentF5TTSChunk.py \
    --ckpt_file "./ckpt/pt-br/model_last.safetensors" \
    --text_file "./input_text.txt" \
    --output_dir "./output" \
    --ref_audio "./ref_audio/pt-br/Leandro.wav" \
    --language "pt"
```

## Parâmetros do Script

- `--ckpt_file`: Caminho para o arquivo de checkpoint do modelo (.safetensors).
- `--text_file`: Caminho para o arquivo de texto de entrada.
- `--output_dir`: Diretório onde os arquivos de áudio gerados serão salvos.
- `--ref_audio`: Caminho para o arquivo de áudio de referência (usado para clonar a voz).
- `--language`: Idioma para conversão de números em palavras (ex: pt).
- `--convert_to_mp3`: (Opcional) Converte os arquivos de saída para MP3.
- `--delay`: (Opcional) Atraso em segundos entre gerações de áudio (padrão: 0).
- `--vocoder_name`: (Opcional) Nome do vocoder a ser usado (vocos ou bigvgan, padrão: vocos).
- `--device`: (Opcional) Dispositivo de execução (cpu, cuda, mps, padrão: cuda).

## Exemplo de Uso

1. Crie um arquivo `input_text.txt` com o texto que deseja converter em áudio. Por exemplo:

   ```
   Olá, mundo! Este é um exemplo de geração de fala com F5-TTS.
   O número 42 é muito importante.
   ```

   **Observação:** Cada arquivo de áudio é gerado a partir de uma nova linha.

2. Execute o script conforme mostrado acima.

3. Os arquivos de áudio gerados serão salvos na pasta `./output`. Se a opção `--convert_to_mp3` for usada, os arquivos serão convertidos para MP3.

## Observações

- Certifique-se de que o arquivo de áudio de referência (`ref_audio`) esteja no formato `.wav` e corresponda ao idioma desejado.
- O script suporta a conversão de números em palavras (ex: 42 → quarenta e dois) para melhorar a qualidade da fala gerada.
- Para melhores resultados, utilize uma GPU (`cuda`) para execução. Caso não disponha de uma, o script também pode ser executado em CPU.

## Licença

Este projeto é baseado no modelo F5-TTS, disponível sob licença no Hugging Face. Consulte os links de créditos acima para mais informações sobre licenciamento e uso do modelo.
