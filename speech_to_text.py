import speech_recognition as sr
import pyaudio
import time


recognizer = sr.Recognizer()


# Adjust for ambient noise and energy threshold
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("Ready! Speak now...")


def listen_and_transcribe(verbose=1, pause_threshold=0.8):
    # Initialize the recognizer
   
    recognizer.pause_threshold=pause_threshold
    try:
        # Listen for audio input with automatic silence detection
        with sr.Microphone() as source:
            # Set timeout and phrase_time_limit for better control
            audio = recognizer.listen(
                source, 
                timeout=100,  # Wait up to 10 seconds for speech to start
                phrase_time_limit=None  # Stop listening after 5 seconds of silence
            )
        
        print("Processing your speech...")
        
        # Use Google's speech recognition service
        text = recognizer.recognize_google(audio)
        
        print(f"\nYou said: '{text}'")
        return text
        
    except sr.WaitTimeoutError:
        print("No speech detected within timeout period.")
        return None
        
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try speaking more clearly.")
        return None
        
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        return None

def main():
    print("Voice Input Script")
    print("=" * 30)
    print("This script will listen for your voice input and print what you said.")
    print("Make sure you have a working microphone connected.\n")
    
    while True:
        # Get voice input
        result = listen_and_transcribe()
        
        if result:
            # Check if user wants to exit
            if result.lower() in ['exit', 'quit', 'stop']:
                print("Goodbye!")
                break
        
        # Ask if user wants to continue
        print("\nPress Enter to speak again, or type 'q' to quit: ", end="")
        user_input = input()
        if user_input.lower() == 'q':
            print("Goodbye!")
            break
        print()  # Add blank line for clarity

if __name__ == "__main__":
    main()
