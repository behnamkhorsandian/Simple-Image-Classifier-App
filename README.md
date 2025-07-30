
[![Open in Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://tokencounter.streamlit.app)

# Simple File Token Counter App

A simple Streamlit app to count tokens in documents using various LLM tokenization methods (OpenAI encodings).

## Features
- Upload a document (PDF, EPUB, DOC, DOCX, TXT, Markdown)
- Select from multiple OpenAI token encodings (cl100k_base, p50k_base, r50k_base, o200k_base)
- See file size, character count, word count, and token count

## Usage
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open the app in your browser, upload a file, and view the token statistics.

## Notes
- Only OpenAI encodings are directly supported.
- Other LLM tokenizers (Claude, PaLM/Gemini, LLaMA/Mistral, Grok) are not yet available.

## License
MIT
