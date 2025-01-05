import json
import groq
import requests
from bs4 import BeautifulSoup
from groq import Groq
import time

# Initialize the Groq client with your API key
client = Groq(api_key="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")

# Path to the memory file
MEMORY_FILE = "conversation_memory.json"

# Load conversation history from the memory file
def load_conversation_history():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Start with an empty history if the file doesn't exist

# Save conversation history to the memory file
def save_conversation_history(history):
    with open(MEMORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Truncate the conversation history to fit within token limits
def truncate_history(history, max_tokens=3000):
    total_tokens = 0
    truncated_history = []
    for message in reversed(history):
        message_tokens = len(message["content"].split())  # Approximate token count
        if total_tokens + message_tokens > max_tokens:
            break
        truncated_history.insert(0, message)
        total_tokens += message_tokens
    return truncated_history

# Scrape webpage content from the given URL
def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract specific sections, like paragraphs and list items
        content = soup.find_all(["p", "li"])
        text = " ".join([item.get_text(strip=True) for item in content])
        return text[:5000]  # Limit to 5000 characters
    except requests.RequestException as e:
        return f"Error scraping the webpage: {e}"

# Initialize conversation history
conversation_history = load_conversation_history()

# Function to send a message and get a response
def chat_with_bot(user_input, url=None):
    # Scrape the webpage content if a URL is provided
    scraped_content = ""
    if url:
        print(f"Scraping content from: {url}")
        scraped_content = scrape_webpage(url)
        # Add the scraped content to the conversation history for context
        conversation_history.append({"role": "system", "content": f"Webpage content:\n{scraped_content}"})
    
    # Append the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Truncate conversation history to stay within token limits
    truncated_history = truncate_history(conversation_history)

    # Call the API with the updated conversation history
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=truncated_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Collect the response
        response = ""
        for chunk in completion:
            response_part = chunk.choices[0].delta.content or ""
            response += response_part
            print(response_part, end="")  # Print the response part by part
        
        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})
        print()  # Add a newline for readability

        # Save updated conversation history to the memory file
        save_conversation_history(conversation_history)
    
    except groq.APIStatusError as e:
        if "rate_limit_exceeded" in str(e):
            print("\nRate limit exceeded. Retrying after a delay...")
            time.sleep(60)  # Retry after a delay
            chat_with_bot(user_input, url=url)  # Retry the same input

# Example usage
url = "https://en.wikipedia.org/wiki/Shah_Rukh_Khan"  # Replace with the actual URL
chat_with_bot("Mention all movies mentioned here", url=url)
