
# Chatbot with Web Scraping and Memory Storage

This project implements a chatbot that interacts with users and can scrape content from a webpage to provide more context in the conversation. It stores conversation history in a memory file and utilizes the Groq API for generating responses. 

## Features

- Chat with the bot while providing a webpage URL for additional context.
- Scrape content from the provided webpage (e.g., Wikipedia) and include it in the conversation.
- Store conversation history in a local JSON file (`conversation_memory.json`).
- Truncate conversation history to stay within token limits for the Groq API.
- Automatically retry if the rate limit is exceeded by the API.

## Requirements

- Python 3.7 or higher
- `groq` package
- `requests` package
- `beautifulsoup4` package

## Installation

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Install dependencies

You can install the required dependencies using pip:

```bash
pip install groq requests beautifulsoup4
```

### Step 3: Set up your Groq API key

In the Python script, replace `"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"` with your actual Groq API key. Make sure you have access to the Groq API.

## Usage

1. **Scrape content and chat with the bot**: You can call the `chat_with_bot` function and provide the user's input and the URL of the webpage you want to scrape.

   Example:

   ```python
   url = "https://en.wikipedia.org/wiki/Shah_Rukh_Khan"
   chat_with_bot("Mention all movies mentioned here", url=url)
   ```

   The bot will:
   - Scrape the webpage at the provided URL.
   - Append the scraped content to the conversation.
   - Send the user's message along with the conversation history to the Groq API.
   - Print the response from the bot.

2. **Conversation Memory**: The conversation history will be stored in a JSON file named `conversation_memory.json`. This file will be updated after each conversation.

   - The memory file stores the entire conversation, including both user and assistant messages.
   - If the file does not exist, it will be created automatically.

3. **Handling Rate Limits**: If the Groq API rate limit is exceeded, the script will wait for 60 seconds and then retry the same request.

## Functions

### `load_conversation_history()`

Loads the conversation history from the memory file (`conversation_memory.json`).

### `save_conversation_history(history)`

Saves the updated conversation history to the memory file.

### `truncate_history(history, max_tokens=3000)`

Truncates the conversation history to ensure it doesn't exceed the maximum token limit of the API.

### `scrape_webpage(url)`

Scrapes the webpage content from the given URL and extracts text from paragraphs and list items.

### `chat_with_bot(user_input, url=None)`

Sends a message to the bot, optionally scraping a webpage if a URL is provided. The function interacts with the Groq API to generate a response and updates the conversation history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
