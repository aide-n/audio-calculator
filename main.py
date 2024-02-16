import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import operator

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define a dictionary mapping arithmetic operator symbols to corresponding functions
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv  # Use truediv for floating-point division
}


# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:

        print("\n\t\tListening...\n")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for speech
        print("Audio captured, processing...")

    try:
        print("\t\tRecognizing...")
        # Use Google Speech Recognition
        text = recognizer.recognize_google(audio)
        # Replace "x" with "*"
        text = text.replace("x", "*")
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return None


# Function to evaluate arithmetic expressions
def evaluate_expression(expression):
    # Split the expression into operands and operator
    elements = expression.split()
    try:
        # Extract operands and operator
        operand1 = float(elements[0])
        operator_symbol = elements[1]
        operand2 = float(elements[2])

        # Check if the operator is valid
        if operator_symbol not in operators:
            raise ValueError("Invalid operator")

        # Perform the operation
        result = operators[operator_symbol](operand1, operand2)
        print("Result:", result)
        speak_result(str(result))
    except Exception as e:
        print("Error:", e)


# Function to convert text to speech and play the audio
def speak_result(text):
    mp3_path = "result.mp3"

    tts = gTTS(text=text, lang='en')
    tts.save(mp3_path)

    # Use a context manager to ensure proper cleanup after audio playback
    with open(mp3_path, 'rb') as f:
        pygame.mixer.init()
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    # Delete the result.mp3 file
    if os.path.exists(mp3_path):
        os.remove(mp3_path)


# Main function
def main():
    while True:
        print("\n ----------xxxxx------------")
        print("\nSpeak an arithmetic expression \n\t say 'End program' to quit")
        expression = recognize_speech()
        if expression is None:
            continue
        if expression.lower() == "end program":
            print("\n-----XX Exiting XX-----")
            break
        evaluate_expression(expression)


if __name__ == "__main__":
    main()
