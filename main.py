import logging
import asyncio
import aiohttp
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OPEN_LIBRARY_API_URL = "https://openlibrary.org/api/books"

async def fetch_book_data(session, isbn):
    params = {
        "bibkeys": f"ISBN:{isbn}",
        "format": "json",
        "jscmd": "data"
    }
    try:
        async with session.get(OPEN_LIBRARY_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get(f"ISBN:{isbn}")
            else:
                logger.error(f"Error fetching data for ISBN {isbn}: HTTP {response.status}")
                return None
    except Exception as e:
        logger.error(f"Error fetching data for ISBN {isbn}: {str(e)}")
        return None

async def scrape_books():
    # Sample ISBNs for demonstration
    isbns = ["9780451524935", "9780061120084", "9780141439518", "9780743273565", "9780141182704"]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_book_data(session, isbn) for isbn in isbns]
        results = await asyncio.gather(*tasks)
    
    return [result for result in results if result]

def main():
    logger.info("Starting book data fetching process")

    try:
        results = asyncio.run(scrape_books())
        
        for book in results:
            if book:
                logger.info(f"Successfully fetched data for '{book.get('title', 'Unknown Title')}'")
                # Here you can process the book data as needed
                # For example, save it to a file or database
                with open(f"{book.get('title', 'Unknown')}.json", 'w') as f:
                    json.dump(book, f, indent=2)
            else:
                logger.warning(f"Failed to fetch data for a book")
        
        logger.info("Book data fetching process completed")
    except Exception as e:
        logger.error(f"An error occurred during the fetching process: {str(e)}")

if __name__ == "__main__":
    main()
