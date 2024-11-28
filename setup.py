from setuptools import setup, find_packages

setup(
    name="ai_assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.8.0',
        'mediapipe>=0.10.0',
        'SpeechRecognition>=3.10.0',
        'pyttsx3>=2.90',
        'PyQt5>=5.15.0',
        'langchain>=0.0.300',
        'beautifulsoup4>=4.12.0',
        'selenium>=4.12.0',
        'pygetwindow>=0.0.9',
        'Pillow>=10.0.0',
        'openai-whisper>=20230918',
        'torch>=2.0.0',
        'transformers>=4.33.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ai_assistant=ai_assistant.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI assistant with visual/audio detection and OSINT capabilities",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="ai, assistant, computer-vision, audio-detection, osint",
    python_requires='>=3.8',
)
