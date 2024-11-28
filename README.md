# AI Assistant

A comprehensive multi-functional AI assistant with advanced capabilities for visual detection, audio processing, system monitoring, internet search, and OSINT tools.

## Features

- **Visual Detection**: Face detection, motion tracking, and object detection using OpenCV
- **Audio Detection**: Real-time audio monitoring and visualization
- **Device Monitoring**: System information and resource usage tracking
- **Internet Search**: Multi-engine web search with history
- **OSINT Tools**: Network analysis and domain information gathering

## Installation Guide

### Windows Installation

1. **Prerequisites**:
   - Python 3.8 or higher
   - Git (optional)
   - Webcam (for visual detection)
   - Microphone (for audio detection)

2. **Download the Project**:
   ```bash
   git clone https://github.com/yourusername/ai_assistant.git
   # or download and extract the ZIP file
   ```

3. **Set Up Virtual Environment**:
   ```bash
   cd ai_assistant
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python -m ai_assistant.main
   ```

### Android Installation

1. **Prerequisites**:
   - Termux app from F-Droid
   - Storage permission for Termux
   - Python package in Termux

2. **Install Required Packages in Termux**:
   ```bash
   pkg update && pkg upgrade
   pkg install python opencv-python numpy
   pkg install x11-repo
   pkg install qt5-python
   ```

3. **Set Up Project**:
   ```bash
   cd storage/shared
   git clone https://github.com/yourusername/ai_assistant.git
   cd ai_assistant
   ```

4. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application**:
   ```bash
   python -m ai_assistant.main
   ```

## Usage Guide

1. **Starting the Application**:
   - Launch the application using the command above
   - A floating window will appear with the AI Assistant interface

2. **Feature Navigation**:
   - Use the buttons at the top to switch between features
   - Each feature has its own set of controls and options

3. **Visual Detection**:
   - Select detection mode (Face/Motion/Object)
   - Click "Start Camera" to begin detection
   - Adjust settings as needed

4. **Audio Detection**:
   - Select input device from dropdown
   - Start audio monitoring
   - View real-time audio levels

5. **Device Monitoring**:
   - View system information
   - Monitor CPU, Memory, and Disk usage
   - Track running processes

6. **Internet Search**:
   - Enter search query
   - Select search engine
   - View and manage search history

7. **OSINT Tools**:
   - Enter domain/IP for analysis
   - Select scanning options
   - View detailed results

## Troubleshooting

### Common Issues on Windows:

1. **Camera Access Error**:
   - Ensure webcam is connected
   - Grant camera permissions
   - Check if other applications are using the camera

2. **Audio Device Error**:
   - Verify microphone is connected
   - Check Windows sound settings
   - Update audio drivers if needed

3. **PyQt5 Installation Error**:
   - Try installing wheel file manually
   - Update pip: `python -m pip install --upgrade pip`
   - Install Visual C++ Redistributable if needed

### Common Issues on Android:

1. **Display Error**:
   - Install VNC server: `pkg install tigervnc`
   - Start VNC server: `vncserver`
   - Install VNC viewer app

2. **Permission Error**:
   - Grant Termux storage permission
   - Run: `termux-setup-storage`

3. **Package Installation Error**:
   - Update package lists
   - Install python-dev package
   - Use pip with `--no-cache-dir` flag

## Security Considerations

- Grant camera and microphone access only when needed
- Review OSINT tool permissions before scanning
- Keep dependencies updated for security patches
- Don't store sensitive information in search history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
