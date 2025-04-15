# J.A.R.V.I.S. - Just A Rather Very Intelligent System

A personal AI assistant inspired by Iron Man's J.A.R.V.I.S., built with Python.

## Features

- Cross-platform support (Windows, Linux, macOS)
- Modular command system
- Natural language processing capabilities
- Plugin-based architecture for easy extension
- Voice activation and speech recognition
- Text-to-speech responses

## Installation

1. Clone this repository:
```bash
git clone https://github.com/hsynrsd/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
# Add other API keys as needed
```

## Usage

Run the assistant:
```bash
python jarvis.py
```

### Basic Commands

- `open [website]` - Opens a website in your default browser
- `browse [website]` - Alternative command to open websites
- `listen` - Start voice recognition mode
- `stop listening` - Stop voice recognition mode
- `speak [text]` - Make J.A.R.V.I.S. say something
- `exit` - Exits the assistant

### Voice Commands

Once voice recognition is activated with the `listen` command, you can:
1. Say "Jarvis" or "Hey Jarvis" to get J.A.R.V.I.S.'s attention
2. Wait for the "Yes?" response
3. Speak your command
4. J.A.R.V.I.S. will respond verbally

Example voice interactions:
- "Hey Jarvis, open YouTube"
- "Jarvis, what's the weather?"
- "Hey Jarvis, remind me to study at 6 PM"

## Adding New Commands

1. Create a new Python file in the `commands` directory
2. Implement your command handlers
3. Add a `register_commands` function to register your commands
4. Import your module in `commands/__init__.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 