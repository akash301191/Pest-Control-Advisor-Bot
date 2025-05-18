# Pest Control Advisor Bot

Pest Control Advisor Bot is a smart Streamlit application that helps you identify insects based on uploaded images and location context, then provides safe, natural pest control solutions tailored to your environment. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, this tool generates a structured, actionable report you can trust.

## Folder Structure

```
Pest-Control-Advisor-Bot/
├── pest-control-advisor-bot.py
├── README.md
└── requirements.txt
```

* **pest-control-advisor-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Insect Image & Location Input**  
  Upload a photo of an insect and describe the location and context in which it was found (e.g., garden, kitchen, wardrobe).

* **AI-Powered Insect Identification**  
  The `Insect Identifier` agent analyzes the image to detect the most likely species, its scientific name, key traits, and risk assessment.

* **Eco-Friendly Pest Research**  
  The `Insect Control Researcher` agent uses SerpAPI to find reliable, natural pest control strategies based on your inputs.

* **Personalized Pest Control Report**  
  The `Pest Control Advisor` agent synthesizes findings into a clean Markdown report with practical remedies, safety tips, and embedded resource links.

* **Structured Markdown Output**  
  Reports are organized with clear section headers, bullet points, and clickable hyperlinks.

* **Download Option**  
  Download your full pest control report as a `.md` file for offline use or sharing.

* **Streamlit UI**  
  Intuitive, responsive, and clean interface for a smooth experience.

## Prerequisites

* Python 3.11 or higher  
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

    ```bash
   git clone https://github.com/akash301191/Pest-Control-Advisor-Bot.git
   cd Pest-Control-Advisor-Bot
    ```

2. **(Optional) Create and activate a virtual environment**:

    ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
    ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run pest-control-advisor-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI and SerpAPI keys in the sidebar.
   * Upload an insect image and fill out the location/context fields.
   * Click **🐞 Generate Insect Report**.
   * View your AI-generated pest control report.

3. **Download Option**
   Use the **📥 Download Pest Control Report** button to save the generated Markdown report.

## Code Overview

* **`render_sidebar()`**: Captures and stores OpenAI and SerpAPI keys securely in Streamlit session state.
* **`render_insect_input()`**: Handles file uploads and contextual user inputs like location and notes.
* **`generate_insect_report()`**:

  * Calls the `Insect Identifier` agent to analyze the uploaded image.
  * Uses the `Insect Control Researcher` to retrieve real-time remedies from the web.
  * Combines all information into a report via the `Pest Control Advisor` agent.
* **`main()`**: Manages layout, integrates inputs, handles validation, and controls the app flow.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your changes are clean, well-tested, and aligned with the purpose of the application.