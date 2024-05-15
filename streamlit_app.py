import streamlit as st
import fitz
import spacy
from spacy.pipeline import EntityRuler
import json

# Loading pretrained model
nlp = spacy.load("en_core_web_lg")
# jsonl file
skills_pattern_file = "jz_skill_patterns.jsonl"

# Create an EntityRuler instance with a unique name
ruler = nlp.add_pipe("entity_ruler", name="my_entity_ruler")

# Load patterns from disk
ruler.from_disk(skills_pattern_file)

# Function to extract skills
def extract_skills(text):
    try:
        # Check if "dotnet" or ".net" is present in the text
        dotnet_present = "dotnet" in text.lower()
        dot_net_present = ".net" in text.lower()

        # Process text to extract skills
        doc = nlp(text)
        skills = set()
        for ent in doc.ents:
            if ent.label_ == 'SKILL':
                skills.add(ent.text.lower().capitalize())

        # Include "dotnet" and ".net" in the extracted skills if present
        if dotnet_present:
            skills.add("Dotnet")
        if dot_net_present:
            skills.add(".Net")

        return list(skills)
    except Exception as e:
        return str(e)

# Streamlit app
def main():
    st.title("Skill Extractor from PDF")

    # File upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

    if uploaded_file is not None:
        # Read PDF file
        pdf_contents = uploaded_file.read()
        
        # Extract text from PDF
        text = ""
        with fitz.open(stream=pdf_contents, filetype="pdf") as pdf_doc:
            for page in pdf_doc:
                text += page.get_text()

        # Extract skills
        skills = extract_skills(text)

        # Return skills in JSON format
        skills_json = json.dumps({"skills": skills})
        st.json(skills_json)

if __name__ == '__main__':
    main()
