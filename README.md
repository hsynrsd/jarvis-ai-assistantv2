# J.A.R.V.I.S. AI Assistant

A sophisticated AI assistant inspired by Iron Man's J.A.R.V.I.S., built with Python and powered by OpenRouter's AI models.

## Features

- 🤖 Natural Language Processing with OpenRouter's AI
- 🎙️ Voice Recognition and Response
- 🔍 Web Search Capabilities
- 📝 File Operations
- 🎵 Music Playback
- 📊 System Information
- 🔄 Command History
- 🎨 Rich Console Interface

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- OpenRouter API key
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hsynrsd/jarvis-ai-assistantv2.git
cd jarvis-ai-assistantv2
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your-api-key-here
```

## Usage

1. Start J.A.R.V.I.S.:
```bash
python jarvis.py
```

2. Available Commands:
- `help` - Show available commands
- `search <query>` - Search the web
- `voice on/off` - Toggle voice features
- `play <song>` - Play music
- `system` - Show system information
- `history` - Show command history
- `exit` or `quit` - Exit J.A.R.V.I.S.

## Voice Commands

Voice features are enabled by default. To use voice commands:
1. Speak clearly into your microphone
2. Wait for the "Listening..." prompt
3. Speak your command
4. J.A.R.V.I.S. will process and respond

## Project Structure

```
jarvis-ai-assistantv2/
├── commands/           # Command modules
│   ├── conversation.py # Natural language processing
│   ├── voice.py       # Voice recognition
│   └── ...            # Other command modules
├── jarvis.py          # Main application
├── requirements.txt   # Dependencies
└── .env              # Environment variables
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Iron Man's J.A.R.V.I.S.
- Powered by OpenRouter's AI models
- Built with Python and various open-source libraries

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

Made with ❤️ by Huseyin Rashid 