from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import argparse
import os
import random
import textwrap
import re

# List of user agents to rotate through
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/94.0.4606.76 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
]

def get_random_user_agent():
    """Return a random user agent from the list."""
    return random.choice(USER_AGENTS)

def add_random_delay(min_seconds=1, max_seconds=3):
    """Add a random delay to mimic human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def chunk_text(text, chunk_size=4000):
    """
    Split text into chunks of approximately chunk_size characters.
    Try to split at sentence endings for more natural breaks.
    
    Args:
        text (str): The text to split
        chunk_size (int): Maximum size of each chunk
        
    Returns:
        list: List of text chunks
    """
    # If text is smaller than chunk size, return it as is
    if len(text) <= chunk_size:
        return [text]
    
    # Use textwrap for initial chunking
    chunks = textwrap.wrap(text, width=chunk_size, replace_whitespace=False, break_long_words=False)
    
    # Refine chunks to try to end at sentences (., !, ?)
    refined_chunks = []
    current_chunk = ""
    
    for chunk in chunks:
        if not current_chunk:
            current_chunk = chunk
        else:
            # If adding this chunk exceeds size limit, store current and start new
            if len(current_chunk + chunk) > chunk_size:
                refined_chunks.append(current_chunk)
                current_chunk = chunk
            else:
                current_chunk += chunk
    
    # Add the last chunk if there's anything left
    if current_chunk:
        refined_chunks.append(current_chunk)
        
    return refined_chunks

def translate_text(text_to_translate, output_file="translated_output.txt", source_lang="gu", target_lang="en"):
    """
    Translates text using Google Translate and saves to a file.
    Handles text in chunks if longer than 4000 characters.
    
    Args:
        text_to_translate (str): The text to translate
        output_file (str): The filename to save the translation to
        source_lang (str): Source language code (default: 'gu' for Gujarati)
        target_lang (str): Target language code (default: 'en' for English)
    """
    # Split text into chunks of max 4000 characters
    text_chunks = chunk_text(text_to_translate, chunk_size=4000)
    print(f"Split text into {len(text_chunks)} chunks")
    
    all_translations = []
    
    # Set up the Chrome driver with anti-detection measures
    options = webdriver.ChromeOptions()
    
    # Add anti-detection measures
    options.add_argument(f"user-agent={get_random_user_agent()}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Run in headless mode
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    
    try:
        # Navigate to Google Translate with specified languages - only once
        url = f"https://translate.google.co.in/?sl={source_lang}&tl={target_lang}&op=translate"
        driver.get(url)
        print(f"Opened Google Translate ({source_lang} to {target_lang})")
        
        # Add random delay after loading page
        add_random_delay(2, 4)
        
        # Accept cookies if prompt appears - only once
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
            )
            cookie_button.click()
            print("Accepted cookies")
            add_random_delay(1, 2)
        except:
            print("No cookie prompt found")
            pass
        
        # Find the input text area - only once
        input_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
        )
        print("Found input area")
        
        # Process each chunk
        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i+1}/{len(text_chunks)}")
            
            # Add a longer delay between chunks if not first chunk
            if i > 0:
                delay = add_random_delay(3, 5)
                print(f"Waiting {delay:.2f} seconds before processing next chunk...")
            
            # Clear previous text with a small delay
            input_area.clear()
            add_random_delay(0.5, 1)
            
            # Paste entire chunk at once
            input_area.send_keys(chunk)
            print(f"Entered text chunk (length: {len(chunk)} characters)")
            
            # Wait for translation to appear with random timing
            print("Waiting for translation...")
            wait_time = add_random_delay(4, 6)
            print(f"Waited {wait_time:.2f} seconds for translation")
            
            # Get the translation output
            output_area = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lRu31"))
            )
            print("Found output area using the working selector")
            
            # Get the translated text
            translated_text = output_area.text
            print(f"Got translated text (length: {len(translated_text)} characters)")
            
            # Add the translated chunk to our collection
            all_translations.append(translated_text)
        
        # Combine all translated chunks
        complete_translation = " ".join(all_translations)
        print(f"Combined all translations (total length: {len(complete_translation)} characters)")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(complete_translation)
            
        print(f"Translation saved to {output_file}")
        return complete_translation
            
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

def read_input_file(file_path):
    """Read text from input file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Translate text using Google Translate via Selenium')
    
    # Add arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Text to translate')
    input_group.add_argument('--input-file', type=str, help='File containing text to translate')
    
    parser.add_argument('--output-file', type=str, default='translated_output.txt', 
                        help='File to save translation to (default: translated_output.txt)')
    parser.add_argument('--source-lang', type=str, default='gu', 
                        help='Source language code (default: gu for Gujarati)')
    parser.add_argument('--target-lang', type=str, default='en', 
                        help='Target language code (default: en for English)')
    parser.add_argument('--chunk-size', type=int, default=4000,
                        help='Maximum characters per chunk (default: 4000)')
    
    args = parser.parse_args()
    
    # Get the text to translate
    if args.text:
        text_to_translate = args.text
    else:
        text_to_translate = read_input_file(args.input_file)
    
    try:
        result = translate_text(
            text_to_translate=text_to_translate,
            output_file=args.output_file,
            source_lang=args.source_lang,
            target_lang=args.target_lang
        )
        print(f"Translation complete: {result[:100]}..." if len(result) > 100 else f"Translation complete: {result}")
    except Exception as e:
        print(f"Script failed with error: {e}")
