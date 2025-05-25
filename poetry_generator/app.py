import streamlit as st
import requests
import random

# Hugging Face API Setup
# Define the API endpoint for the Mistral language model
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
# API key for authentication with Hugging Face
HUGGINGFACE_API_KEY = "HUGGING FACE API KEY"  # Your API key here

def generate_poem(theme, style=None, mood=None):
    """
    Advanced poem generation with multiple customization options.
    
    Args:
        theme (str): The central theme of the poem
        style (str, optional): Poetic style
        mood (str, optional): Emotional tone of the poem
    
    Returns:
        str: Generated poem or error message
    """
    # Construct the base prompt with the given theme
    prompt_parts = [f"Write a poem about: {theme}"]
    
    # Add style specification to the prompt if provided
    if style:
        prompt_parts.append(f"Style: {style}")
    
    # Add mood specification to the prompt if provided
    if mood:
        prompt_parts.append(f"Mood: {mood}")
    
    # Prepare the payload for API request with detailed generation parameters
    payload = {
        # Combine prompt parts and add instructions for poem generation
        "inputs": ". ".join(prompt_parts) + ". Create a structured poem with vivid imagery and emotional depth. Use line breaks and proper formatting.",
        # Fine-tune text generation parameters
        "parameters": {
            "max_length": 300,  # Maximum length of generated text
            "temperature": 0.85,  # Creativity level (higher = more random)
            "top_p": 0.92,  # Nucleus sampling threshold
            "top_k": 50,  # Top-k tokens to consider
            "do_sample": True,  # Enable sampling for more diverse output
            "no_repeat_ngram_size": 2  # Prevent repetitive n-grams
        }
    }

    # Prepare headers with API authentication
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    try:
        # Send POST request to Hugging Face API with timeout
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        # Raise an exception for unsuccessful HTTP requests
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        generated_text = data[0]['generated_text']
        
        # Clean and format the generated poem lines
        poem_lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
        
        # Use fallback poem generation if no lines are generated
        if not poem_lines:
            poem_lines = _generate_fallback_poem(theme)
        
        # Join poem lines and return as a string
        return "\n".join(poem_lines)
    
    except requests.exceptions.RequestException as e:
        # Handle and return any API request errors
        return f"🚫 Poem Generation Error: {str(e)}"

def _generate_fallback_poem(theme):
    """
    Fallback poem generation method in case of API failure.
    
    Args:
        theme (str): Theme for the fallback poem
    
    Returns:
        list: Lines of a simple poem
    """
    # Predefined poem templates with the given theme
    fallback_templates = [
        [
            f"In the realm of {theme}, whispers rise,",
            "Echoing thoughts beneath silent skies,",
            "A melody of dreams, soft and light,",
            "Dancing through the edges of insight."
        ],
        [
            f"Oh {theme}, vast and deep and wide,",
            "Where imagination's currents ride,",
            "Your essence sparks a burning flame,",
            "A poetry beyond a simple name."
        ]
    ]
    # Randomly select and return a fallback poem template
    return random.choice(fallback_templates)

def main():
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="Poem Crafting Studio", 
        page_icon="✍", 
        layout="wide"
    )

    # Add custom CSS styling to enhance UI
    st.markdown("""
    <style>
    .main {
        background-color: #f0f0f8;
        font-family: 'Georgia', serif;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #6A1B9A;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    .stButton button {
        background-color: #8A2BE2;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #6A1B9A;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Display main title and subtitle
    st.title("✍ Poem Crafting Studio")
    st.subheader("Create Unique Poems with AI Magic")

    # Create three columns for input fields
    col1, col2, col3 = st.columns(3)

    # Theme input
    with col1:
        theme = st.text_input("🎨 Poem Theme", placeholder="Love, Nature, Hope...")
    
    # Style selection dropdown
    with col2:
        style = st.selectbox("📝 Poem Style", [
            "Free Verse", "Sonnet", "Haiku", 
            "Limerick", "Ode", "Ballad"
        ])
    
    # Mood selection dropdown
    with col3:
        mood = st.selectbox("🌈 Emotional Tone", [
            "Joyful", "Melancholic", "Mysterious", 
            "Romantic", "Contemplative", "Inspirational"
        ])

    # Poem generation button
    if st.button("✨ Craft My Poem", use_container_width=True):
        # Check if theme is provided
        if theme.strip():
            # Show loading spinner during poem generation
            with st.spinner("Weaving poetic magic..."):
                poem = generate_poem(theme, style, mood)
            
            # Display generated poem
            st.subheader("🌟 Your Generated Poem:")
            st.code(poem, language="")

            # Additional interaction buttons
            col_copy, col_save = st.columns(2)
            
            # Copy poem button
            with col_copy:
                if st.button("📋 Copy Poem"):
                    st.code(poem)
                    st.success("Poem copied to clipboard!")
            
            # Save poem button (placeholder for future functionality)
            with col_save:
                if st.button("💾 Save Poem"):
                    # Future: Implement save functionality
                    st.info("Save feature coming soon!")

        else:
            # Show warning if no theme is entered
            st.warning("Please enter a theme for your poem!")

    # Footer with feature description
    st.markdown("---")
    st.markdown("#### 🚀 Features")
    st.markdown("""
    - Custom theme-based poem generation
    - Multiple poetic styles
    - Emotional tone selection
    - Instant poem crafting
    """)


# Entry point of the script
if __name__ == "__main__":
    main()