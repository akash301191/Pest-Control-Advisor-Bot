import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_insect_input():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Image Upload
    with col1:
        st.subheader("📸 Upload Insect Image")
        uploaded_image = st.file_uploader(
            "Upload a photo of the insect you've found",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Location + Additional Input
    with col2:
        st.subheader("📍 Location & Context")

        location = st.text_input(
            "Where did you find the insect?",
            placeholder="e.g., kitchen garden, Delhi or backyard, Austin"
        )

        context = st.text_input(
            "Additional notes (optional)",
            placeholder="e.g., found under a leaf, near stored food, inside wardrobe"
        )

    return {
        "uploaded_image": uploaded_image,
        "location": location,
        "context": context if context else "Not Specified",
    }

def generate_insect_report(insect_profile):
    uploaded_image = insect_profile["uploaded_image"]
    location = insect_profile["location"]
    context = insect_profile["context"]

    # Save the uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Insect Identification Agent
    insect_identifier = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Insect Identifier",
        role="Identifies insects from images and describes key traits and risks.",
        description=(
            "You are an expert entomologist. When given an image of an insect, "
            "your job is to identify the insect species, describe its appearance, and estimate a confidence level."
        ),
        instructions=[
            "Analyze the uploaded image and identify the insect species or best match.",
            "Provide the common name and scientific name.",
            "Estimate a confidence level (percentage).",
            "List key visual features (e.g., size, color, number of legs, wings, antennae).",
            "Mention any known risk the insect poses (e.g., crop damage, harmless, bites).",
            "Output in this markdown format:\n\n"
            "**Common Name**: <Insect Name>\n"
            "**Scientific Name**: *<Botanical Name>*\n"
            "**Confidence**: <e.g., 88%>\n"
            "**Visual Traits**:\n- ...\n- ...\n"
            "**Potential Risk**: <Short sentence>",
            "If unsure, list the top 2–3 likely species and clearly note uncertainty."
        ],
        markdown=True
    )

    identifier_response = insect_identifier.run(
        "Identify this insect and assess its traits.",
        images=[Image(filepath=image_path)]
    )
    insect_identification = identifier_response.content

    # Step 2: Research Agent
    insect_researcher = Agent(
        name="Insect Control Researcher",
        role="Finds safe pest control strategies based on insect identification and context.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a pest control researcher. Given the insect name, location, and context,
            your job is to find safe and natural pest control measures using web search.
        """),
        instructions=[
            "Read the insect name, region, and context provided.",
            "Generate ONE focused Google search query, e.g., 'natural pest control for red flour beetle indoor India'.",
            "Use `search_google` with that query.",
            "Return a clean, curated list of 10 helpful URLs offering pest control solutions.",
            "Avoid listing product ads or irrelevant pages. Prioritize natural or safe methods.",
            "Do NOT summarize results—just output URLs clearly in markdown list format."
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
        markdown=True
    )

    research_input = f"Insect identified in: {location}\nContext: {context}\n\n{insect_identification}"
    research_response = insect_researcher.run(research_input)
    research_results = research_response.content

    # Step 3: Report Generator Agent
    insect_advisor = Agent(
        name="Pest Control Advisor",
        role="Generates a full insect identification and pest control report.",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a pest control advisor. Given:
            1. A structured insect identification summary
            2. A list of curated pest control resources
            3. The user's region and context

            Your task is to create a helpful Markdown report with two main sections:
            - ## 🐞 Insect Identification
            - ## 🧪 Safe Pest Control Guide
        """),
        instructions=[
            "Begin with ## 🐞 Insect Identification section.",
            "Include the following details clearly:\n- **Common Name**\n- **Scientific Name** (italicized)\n- **Confidence** (e.g., 87%)\n- **Visual Traits** (use bullet points)\n- **Potential Risk** (one-line explanation)",
            "",
            "Then, add ## 🧪 Safe Pest Control Guide with these subheadings (use ###):",
            "### 🌱 Natural Remedies",
            "### 🏡 Indoor/Outdoor Safety Tips",
            "### 🚫 What to Avoid",
            "### 🔗 Trusted Resources",
            "",
            "Summarize care strategies using information from the provided URLs only.",
            "Use proper Markdown to embed links directly into the report — do **not** paste raw URLs.",
            "Example: Instead of 'https://example.com', write: [How to handle aphids](https://example.com)",
            "Only include hyperlinks that relate to specific strategies or facts discussed in the guide.",
            "Under 'Trusted Resources', format the links as a clean bulleted list with descriptive link text.",
            "",
            "Do not add extra commentary or meta instructions. Output only the formatted Markdown report."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )


    advisor_prompt = f"""
Insect Identification:
{insect_identification}

Location: {location}
Context: {context}

Research Results:
{research_results}

Generate a comprehensive pest control report based on these.
"""
    advisor_response = insect_advisor.run(advisor_prompt)
    final_insect_report = advisor_response.content

    return final_insect_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Pest Control Advisor Bot", page_icon="🐞", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🐞 Pest Control Advisor Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Pest Control Advisor Bot — your smart assistant for identifying insects using images and location, and getting safe, eco-friendly pest control tips tailored to your surroundings.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_insect_profile = render_insect_input()
    
    st.markdown("---")

    if st.button("🐞 Generate Insect Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in user_insect_profile or not user_insect_profile["uploaded_image"]:
            st.error("Please upload an insect image before generating the report.")
        else:
            with st.spinner("Identifying the insect and generating a tailored pest control guide..."):
                insect_report = generate_insect_report(user_insect_profile)

                st.session_state.insect_report = insect_report
                st.session_state.image = user_insect_profile["uploaded_image"]

    # Display and download
    if "insect_report" in st.session_state:
        st.markdown("## 📸 Uploaded Insect Image")
        st.image(st.session_state.image, use_container_width=False)

        st.markdown(st.session_state.insect_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Pest Control Report",
            data=st.session_state.insect_report,
            file_name="insect_pest_control_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
