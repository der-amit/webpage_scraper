import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.title("Web Content Extractor")
st.write("Enter a URL to extract the text content from any webpage")

# Input field for URL
url = st.text_input("Paste the link here:", placeholder="https://example.com")

if st.button("Extract Content") and url:
    try:
        # Show loading spinner
        with st.spinner("Fetching content..."):
            # Headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Get the webpage with headers
            response = requests.get(url, headers=headers, timeout=15)
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
            st.metric("Words", len(clean_text.split()) if clean_text else 0)
        
        # Display the content
        st.subheader("Extracted Content:")
        if clean_text:
            st.text_area("Content", clean_text, height=400)
            
            # Download button
            st.download_button(
                label="Download as Text File",
                data=clean_text,
                file_name=f"content_{url.split('//')[-1].replace('/', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("No text content found. The page might be JavaScript-heavy or protected.")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            st.error("❌ Access Forbidden (403): This website is blocking automated requests. Try a different URL or the site may have anti-bot protection.")
        elif e.response.status_code == 404:
            st.error("❌ Page Not Found (404): The URL doesn't exist or has been moved.")
        else:
            st.error(f"❌ HTTP Error {e.response.status_code}: {str(e)}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching the webpage: {str(e)}")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

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
- Browser-like headers to avoid blocking
""")

st.sidebar.title("Note")
st.sidebar.warning(
    "Some websites (like news sites) may block automated requests. "
    "If you get a 403 error, try a different URL or a simpler website like Wikipedia."
)

# Add some example URLs that usually work
st.sidebar.title("Try these URLs:")
example_urls = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://docs.python.org/3/tutorial/",
    "https://httpbin.org/html"
]

for example_url in example_urls:
    if st.sidebar.button(f"Try: {example_url.split('/')[2]}", key=example_url):
        st.text_input("Paste the link here:", value=example_url, key="example_input")