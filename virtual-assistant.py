import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit

def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Ouvindo..')
        recognizer.adjust_for_ambient_noise(source) #ajuste do ruído do ambiente
        audio = recognizer.listen(source)
    try:
        cmd = recognizer.recognize_google(audio, language='pt-BR')
        cmd = cmd.lower()
        print("Você disse: ", cmd)
        
        if 'karen' in cmd:
            cmd = cmd.replace('karen', '')
            print(f"Comando reconhecido: {cmd}")
        else: cmd = ''
        
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
        cmd = None
    return cmd

def speak(phrase):
    voice = pyttsx3.init()
    voice.setProperty('rate', 190) #velocidade da fala
    voice.say(phrase)
    voice.runAndWait()

def execute_command(cmd):
    if not cmd:
        return
        
    if 'horas são' in cmd or 'horario' in cmd:
        time = datetime.datetime.now().strftime('%H:%M')
        speak(f'Agora são {time}')
        
    elif 'procure por' in cmd:
        search_for = cmd.replace('procure por', '')
        wikipedia.set_lang('pt')
        try:
            result = wikipedia.summary(search_for, 2)
            print(result)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Vários resultados encontrados. Por favor, especifique sua busca")
            for i, option in enumerate(e.options[:5]):
                speak(f"{i+1}: {option}")
            new_cmd = recognize_command()
            try:
                selected_option = int(new_cmd) - 1
                search_for = e.options[selected_option]
                result = wikipedia.summary(search_for, 2)
                print(result)
                speak(result)
            except:
                speak("Não foi possível selecionar a opção. Tente novamente.")
            
    elif 'toque' in cmd:
        music = cmd.replace('toque','')
        pywhatkit.playonyt(music)
        speak('Tocando música')
        
    else:
        speak('Comando não reconhecido')

while True:
    cmd = recognize_command()
    execute_command(cmd)