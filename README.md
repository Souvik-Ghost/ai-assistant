pip install -r requirements.txt
pip install -r requirements.txt
pip install -r requirements.txt

# AI Assistant Web Application

A comprehensive web-based AI assistant with multiple intelligent modules for visual detection, system monitoring, and OSINT analysis.

## Features

1. **Visual Detection**
   - Face detection using MediaPipe
   - Real-time image processing
   - Visual feedback with detected faces

2. **Device Monitoring**
   - System information
   - CPU usage and details
   - Memory statistics
   - Disk space analysis
   - Battery information (if available)

3. **OSINT Tools**
   - Domain information lookup
   - WHOIS data retrieval
   - DNS record analysis
   - IP geolocation
   - HTTP header inspection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python -m ai_assistant.main
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Requirements

- Python 3.8+
- Flask
- OpenCV
- MediaPipe
- psutil
- python-whois
- dnspython
- requests

## Project Structure

```
ai_assistant/
├── main.py           # Flask application entry point
├── templates/
│   └── index.html    # Main web interface
├── static/
│   ├── css/
│   │   └── style.css # Styling
│   └── js/
│       └── main.js   # Client-side interactions
└── modules/          # Future module expansion
```

## Development

This project is in active development. Future improvements include:
- User authentication
- Additional AI modules
- Enhanced security features
- Production deployment optimizations

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
