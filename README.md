# 🌎 Google Translate Automation Tool

## What's This?

Hey there! This is a fun little project I built to automate translations through Google Translate. I was messing around with web automation and wanted to see if I could create something useful while learning more about Selenium, FastAPI, and web scraping.

## Why I Made This

I mostly built this as a learning project to:
- Get better at web automation with Selenium
- Practice creating APIs with FastAPI
- Understand how to handle background tasks and job queuing
- Learn how to bypass some basic bot detection (for educational purposes only!)

## Features

- Translate text between 190+ languages using Google Translate (without using any paid API)
- Split long texts into manageable chunks automatically
- API access with job status tracking
- Random delays and user agent rotation to mimic human behavior

## Components

The project has a few main pieces:
1. `google_translate.py` - The core translation engine using Selenium automation
2. `translate_api.py` - A REST API built with FastAPI that makes the translation service available over HTTP
3. Both can be used independently depending on your needs!

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

## ⚠️ Important Disclaimer

**This is a personal learning project and is NOT intended for commercial use!** 

Google Translate's terms of service don't allow automated access to their service outside of their official API. This project was created solely for:
- Educational purposes
- Personal learning
- Understanding web automation techniques

I don't take any responsibility if you get your IP blocked by Google or face any other consequences from using this tool beyond personal experimentation. Please respect Google's terms of service and consider using their official Translation API for any serious or commercial applications.

## What I Learned

Building this taught me a ton about:
- Handling CAPTCHAs and anti-bot measures (ethically)
- Building a job queue system for long-running tasks
- Web automation best practices
- Creating clean API documentation

Feel free to check out the code, learn from it, or suggest improvements! Just remember - this is for educational purposes only!

## Future Ideas

If I keep working on this, I might add:
- A simple UI with Streamlit
- Better error handling
- Support for more complex documents
- Batch processing

Let me know if you have any questions or suggestions!
