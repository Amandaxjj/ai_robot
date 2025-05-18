import asyncio
from pyppeteer import launch
from readability import Document
from markdownify import markdownify as md
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# User agent list for randomization
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]

async def _launch_browser():
    """Launch a headless browser instance with Puppeteer."""
    return await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    )

async def _fetch_page_content(url, max_retries=3, retry_delay=2):
    """
    Fetch the HTML content of a webpage using Puppeteer.
    
    Args:
        url (str): The URL of the webpage to fetch
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        str: The HTML content of the webpage
    """
    browser = None
    try:
        browser = await _launch_browser()
        page = await browser.newPage()
        
        # Set a random user agent
        user_agent = random.choice(USER_AGENTS)
        await page.setUserAgent(user_agent)
        
        # Add random delays to appear more human-like
        await page.setExtraHTTPHeaders({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })
        
        for attempt in range(max_retries):
            try:
                # Navigate to the URL with a timeout
                response = await page.goto(url, {
                    'waitUntil': 'networkidle0',
                    'timeout': 30000
                })
                
                if response.status == 200:
                    # Wait a bit for any JavaScript to run
                    await asyncio.sleep(random.uniform(1, 3))
                    
                    # Get the page content
                    content = await page.content()
                    return content
                else:
                    logger.warning(f"Received status code {response.status} for {url}")
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        logger.info(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Error fetching URL (attempt {attempt+1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
        
        raise Exception(f"Failed to fetch {url} after {max_retries} attempts")
    
    finally:
        if browser:
            await browser.close()

def _html_to_markdown(html_content):
    """
    Convert HTML content to markdown using markdownify.
    
    Args:
        html_content (str): HTML content to convert
        
    Returns:
        str: The markdown representation of the HTML content
    """
    return md(html_content, heading_style="ATX", strip=["script", "style"])

def _extract_article_content(html_content):
    """
    Extract the main article content from HTML using Mozilla's Readability.
    
    Args:
        html_content (str): The full HTML content of the webpage
        
    Returns:
        str: The extracted article content in HTML format
    """
    try:
        doc = Document(html_content)
        article = doc.summary()
        title = doc.title()
        return {"title": title, "content": article}
    except Exception as e:
        logger.error(f"Error extracting article content: {str(e)}")
        return {"title": "Unknown", "content": html_content}

async def fetch_article_as_markdown(url):
    """
    Fetch an article from a URL and convert it to markdown format.
    
    Args:
        url (str): The URL of the article to fetch
        
    Returns:
        str: The article content in markdown format
    """
    try:
        logger.info(f"Fetching article from {url}")
        html_content = await _fetch_page_content(url)
        
        logger.info("Extracting article content using Readability")
        article_data = _extract_article_content(html_content)
        
        logger.info("Converting article to markdown")
        markdown_content = _html_to_markdown(article_data["content"])
        
        # Add the title at the top of the markdown
        full_markdown = f"# {article_data['title']}\n\n{markdown_content}"
        
        return full_markdown
    except Exception as e:
        logger.error(f"Error fetching article as markdown: {str(e)}")
        raise

<<<<<<< HEAD
def fetch_article(url):
    """
    Synchronous wrapper for fetch_article_as_markdown.
    
    Args:
        url (str): The URL of the article to fetch
        
    Returns:
        str: The article content in markdown format
    """
    try:
        # Use asyncio.run instead of get_event_loop().run_until_complete
        return asyncio.run(fetch_article_as_markdown(url))
    except RuntimeError as e:
        # Handle case where there's already a running event loop
        if "There is already a running event loop" in str(e):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(fetch_article_as_markdown(url))
        raise
=======
import trafilatura

def fetch_article(url):
    """
    Fetch readable article text from a URL using trafilatura.
    
    Args:
        url (str): The URL of the article to fetch
    
    Returns:
        str: Clean extracted article text
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""

    article = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    return article or ""
>>>>>>> 9cde1b5 (初始化项目，添加 sentiment_analysis 等代码)

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter article URL: ")
    
    try:
        markdown = fetch_article(url)
        print("\n--- Article in Markdown ---\n")
        print(markdown)
    except Exception as e:
        print(f"Failed to fetch article: {str(e)}") 