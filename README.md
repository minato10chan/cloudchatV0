# Streamlit Chatbot

A simple chatbot application built with Streamlit that can be deployed to Streamlit Cloud.

## Features

- Interactive chat interface
- Integration with OpenAI's API
- Message history tracking
- Responsive design

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running Locally

Run the application with:

```
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and link to your GitHub repository
4. Set the main file path as `app.py`
5. Add your `OPENAI_API_KEY` as a secret in the Streamlit Cloud dashboard

## License

MIT 