import os
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from multiprocessing import Pool, cpu_count

def extract_audio_from_video(video_file, output_audio_file):
    # Carregar o vídeo e extrair o áudio
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(output_audio_file)

def convert_audio_to_text(audio_file):
    # Carregar o áudio e converter para o formato correto
    sound = AudioSegment.from_file(audio_file)
    sound.export("converted_audio.wav", format="wav")

    # Usar SpeechRecognition para converter o áudio em texto
    recognizer = sr.Recognizer()
    with sr.AudioFile("converted_audio.wav") as source:
        audio_data = recognizer.record(source)

    try:
        # Usar o reconhecimento de fala para converter o áudio em texto
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        return text
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
        return ""
    except sr.RequestError as e:
        print(f"Erro na requisição ao Google Speech Recognition; {e}")
        return ""

def save_text_to_file(text, output_path):
    # Salvar o texto em um arquivo formatado
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_video(video_path):
    if not os.path.exists(video_path):
        print("O arquivo de vídeo informado não existe.")
        return ""

    # Definir o caminho do áudio extraído
    audio_path = "audio_extraido_" + os.path.basename(video_path) + ".wav"
    extract_audio_from_video(video_path, audio_path)

    # Converter o áudio em texto
    extracted_text = convert_audio_to_text(audio_path)

    return extracted_text

def main():
    video_path = input("Informe o caminho do vídeo (.mp4) que deseja converter: ").strip()

    if not os.path.exists(video_path):
        print("O arquivo de vídeo informado não existe.")
        return

    # Usar todas as CPUs disponíveis para acelerar o processo
    with Pool(cpu_count()) as p:
        extracted_text = p.apply(process_video, (video_path,))

    if not extracted_text:
        print("Nenhum texto foi extraído do áudio.")
        return

    # Perguntar ao usuário se ele deseja exibir o texto no console ou salvar em arquivo
    output_choice = input("Você deseja ver o texto extraído no console ou salvá-lo em um arquivo? (console/arquivo): ").strip().lower()

    if output_choice == 'console':
        print("\nTexto extraído:\n")
        print(extracted_text)
    elif output_choice == 'arquivo':
        # Definir o nome do arquivo de texto com base no nome do vídeo
        output_txt_file = os.path.splitext(video_path)[0] + "_texto_extraido.txt"
        save_text_to_file(extracted_text, output_txt_file)
        print(f"O texto foi salvo no arquivo: {output_txt_file}")
    else:
        print("Opção inválida. Por favor, escolha 'console' ou 'arquivo'.")

if __name__ == "__main__":
    main()
