from setuptools import find_packages,setup

setup(
    name="multilingual assistant",
    version="0.0.0",
    packages=find_packages(),
    author="Tushar Sharma",
    author_email="tusharsharma7024@gmail.com",
    install_requires=["SpeechRecognition","pipwin","pyaudio","gTTS","google-generativeai","python-dotenv","streamlit"]

)