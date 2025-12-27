# 🎬 Text2Reel Professional

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![MoviePy](https://img.shields.io/badge/MoviePy-Sound%20%26%20Vision-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Text2Reel Professional** is a powerful, AI-driven tool designed to transform simple text scripts into viral, short-form video content (Reels, TikToks, Shorts) in seconds. It combines neural voiceovers with dynamic, highlighted captions for a premium, professional look.

## ✨ Key Features

*   **🎙️ Neural Voiceovers**: Access a library of high-quality, realistic voices (Microsoft Edge TTS) including US, UK, and Indian accents.
*   **⚡ Dynamic Captions**: Generates synchronized captions with word-level highlighting (karaoke style) to boost engagement.
*   **🎨 Fully Customizable**: Control every aspect of your video:
    *   **Fonts**: Choose from popular fonts (Arial, Georgia, Impact, etc.).
    *   **Colors**: Customize text, highlight, and background colors.
    *   **Layout**: Adjust font size, words per chunk, and vertical alignment.
*   **🎞️ Transparent Export**: Pro feature! Export videos with a transparent background (`.webm`) to use as overlays in your favorite video editor (Premiere, CapCut, DaVinci).
*   **⏱️ Smart Timing**: Automatically estimates video duration based on script length.
*   **🔊 Instant Preview**: Listen to your generated voiceover before rendering the full video.

## 🚀 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/SanTiwari07/Text2ReelGenerator.git
    cd Text2ReelGenerator
    ```

2.  **Set up Virtual Environment** (Recommended)
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage

1.  **Run the App**
    ```bash
    streamlit run app.py
    ```

2.  **Create Your Reel**
    *   **Input Script**: Type your text in the left panel.
    *   **Select Voice**: Choose a voice character and adjust the speed.
    *   **Customize**: Use the tabs on the right to set colors, fonts, and layout.
    *   **Preview**: Click `Previews Voice` to hear the audio.
    *   **Generate**: Click `🚀 GENERATE REEL` to render your video.

3.  **Download**: Once production is complete, download your `.mp4` or `.webm` file!

## 🧩 Configuration Details

<details>
<summary><b>Audio Settings</b></summary>
<br>
<ul>
    <li><b>Voice Character</b>: Select from male and female voices across different regions (US, UK, IN).</li>
    <li><b>Speed</b>: Adjust speech rate from 0.5x (slow) to 1.5x (fast).</li>
</ul>
</details>

<details>
<summary><b>Visual Design</b></summary>
<br>
<ul>
    <li><b>Background</b>: Choose "Solid Color" for standalone videos or "Transparent (WebM)" for overlays.</li>
    <li><b>Fonts</b>: Includes system-safe fallbacks like Arial, Verdana, and Impact.</li>
    <li><b>Highlight Color</b>: The color of the currently spoken word (e.g., bright yellow or red).</li>
    <li><b>Words per Chunk</b>: Controls how many words appear on screen at once (Good for pacing).</li>
</ul>
</details>

## 📂 Project Structure

```
Text2Reel Generator/
├── app.py              # Main Streamlit application
├── generator.py        # Core video generation logic (MoviePy + TTS)
├── utils.py            # Helper functions
├── requirements.txt    # Project dependencies
└── temp/               # Temporary storage for generated assets
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/SanTiwari07">SanTiwari07</a>
</p>
