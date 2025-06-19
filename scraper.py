import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Web Content Extractor")
st.write("Enter a URL to extract the text content from any webpage")

# Input field for URL
url = st.text_input("Paste the link here:", placeholder="https://example.com")

if st.button("Extract Content") and url:
    try:
        # Show loading spinner
        with st.spinner("Fetching content..."):
            # Get the webpage
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text_content = soup.get_text()
            
            # Clean up the text (remove extra whitespace)
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
        # Display results
        st.success("Content extracted successfully!")
        
        # Show webpage title
        if soup.title:
            st.subheader(f"Title: {soup.title.string}")
        
        # Show character and word count
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Characters", len(clean_text))
        with col2:
            st.metric("Words", len(clean_text.split()))
        
        # Display the content
        st.subheader("Extracted Content:")
        st.text_area("Content", clean_text, height=400)
        
        # Download button
        st.download_button(
            label="Download as Text File",
            data=clean_text,
            file_name=f"content_{url.split('//')[-1].replace('/', '_')}.txt",
            mime="text/plain"
        )
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the webpage: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add some info in the sidebar
st.sidebar.title("About")
st.sidebar.info(
    "This tool extracts clean text content from any webpage. "
    "Simply paste a URL and click 'Extract Content' to get the text without HTML tags, scripts, or styling."
)

st.sidebar.title("Features")
st.sidebar.markdown("""
- Clean text extraction
- Word and character count
- Download extracted content
- Error handling for invalid URLs
""")