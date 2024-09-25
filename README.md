# YouTube Comment Analyzer 📊

Welcome to the **YouTube Comment Analyzer** project! This project leverages deep learning to analyze the sentiment of comments on YouTube videos. The application provides insights into whether the comments are positive, negative, or neutral.

## Table of Contents 📚

- [Features](#features-✨)
- [Installation](#installation-🛠️)
- [Usage](#usage-🚀)
- [Project Structure](#project-structure-📂)
- [Technologies Used](#technologies-used-🛠️)
- [Contributing](#contributing-🤝)
- [License](#license-📄)

## Features ✨

- **Sentiment Analysis**: Analyze comments to determine if they are positive, negative, or neutral.
- **Download Results**: Export the analyzed comments and summary as an Excel file.
- **Interactive Web Interface**: User-friendly web interface to input YouTube URLs and view results.

> **Note**:  
> This project is for educational purposes only. The sentiment analysis model achieves an accuracy of around **85%**. It is not intended for production-level use.

## Installation 🛠️

1. **Clone the repository**:

   ```bash
   git clone https://github.com/michaelswisa/YouTube-Comment-Analyzer.git
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - A `.env` file is already provided in the `config/` directory.
   - Open the `.env` file and replace `your_youtube_api_key` with your actual YouTube API key:
     ```plaintext
     API_KEY=your_youtube_api_key
     ```

## Usage 🚀

1. **Run the Flask server**:

   ```bash
   python server.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000`.

3. **Input a YouTube URL** and click "Analyze" to view the sentiment analysis results.

## Project Structure 📂

```plaintext
.
├── config/
│   └── .env
│
├── models/
│
├── src/
│   ├── __init__.py
│   ├── predict.py
│   ├── train.py
│   └── youtube.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── LICENSE
├── README.md
├── requirements.txt
└── server.py
```

### Key Files and Directories

- **`config/.env`**: Contains environment variables, including the YouTube API key.
- **`src/`**: All source code for the project:
  - **`src/predict.py`**: Script to load the trained model and make predictions.
  - **`src/train.py`**: Script to train the sentiment analysis model using the data from `data.csv`.
  - **`src/youtube.py`**: Script to interact with the YouTube API and fetch comments.
  
- **`static/style.css`**: CSS file for styling the web interface.
- **`templates/index.html`**: HTML template for the web interface.
- **`server.py`**: Flask server to handle web requests and render templates.

---

### Additional Information about `data/data.csv`:

The `data.csv` file is a crucial part of the training process for the sentiment analysis model. It must be structured properly to ensure the model learns effectively. If you are building your own dataset:

1. Make sure each row contains a YouTube comment and its corresponding sentiment label.
2. The sentiment labels should be balanced across `positive`, `negative`, and `neutral` to avoid bias in the model's predictions.
3. Example structure of `data.csv`:

```plaintext
comment,sentiment
"This video is amazing!",positive
"I didn't like this part.",negative
"It's okay, nothing special.",neutral
```

## Technologies Used 🛠️

- **Python**: Main programming language.
- **TensorFlow & Keras**: For building and training the deep learning model.
- **Flask**: Web framework for the server.
- **YouTube Data API**: To fetch video comments.
- **Openpyxl**: To create and manipulate Excel files.

## Contributing 🤝

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you have any questions or need further assistance. Happy coding! 😊
