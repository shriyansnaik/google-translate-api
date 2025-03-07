# Google Translate Automation

A simple tool for automated translations using Google's web interface without the API. The core script is `google_translate.py` (~300 lines) which controls a browser to interact with Google Translate, while `translate_api.py` wraps this in a basic FastAPI server.

What it does is pretty straightforward. When you make a translation request, it launches a headless Chrome browser using Selenium and navigates to the Google Translate website. Since Google Translate only supports around 5000 characters at once, the script splits your text into manageable chunks. It then pastes each chunk into the input field, waits for the translation to appear, and extracts the result. After processing all chunks, it combines them into your final translated text.

I added some basic measures like random delays between actions and rotating through different user agents to make it less obvious that it's automation. The tool works with all 190+ languages that Google Translate supports.

I built this as a learning project to practice with Selenium and FastAPI. It's worth mentioning that this is strictly for personal use and education. Using this at scale would probably go against Google's terms of service, so for any serious applications, you should use their official API.

## How to Use It

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/google-translate-automation

# Install dependencies
pip install -r requirements.txt

# Make sure you have Chrome installed!
```

### Command Line Usage

```bash
# Translate a single line of text
python google_translate.py --text "हेलो, कैसे हो?" --source-lang hi --target-lang en

# Translate a file
python google_translate.py --input-file my_text.txt --output-file translation.txt --source-lang gu --target-lang en
```

### API Usage

```bash
# Start the API server
python translate_api.py

# Now you can access it at http://localhost:8080
# Check out the auto-generated docs at http://localhost:8080/docs
```
