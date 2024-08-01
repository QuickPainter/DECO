import os
import aiohttp
import asyncio
from aiofiles import open as aio_open
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm.asyncio import tqdm

# Configurations
base_url = 'https://bulk.cv.nrao.edu/deco/users/cjlaw/IMAGING/Images_v2/ROph/Images/'  # URL of the directory listing
keyword = '_CO_'                        # Keyword to filter filenames
exclude_substrings = ['Sz68',
 'Sz90',
 'Sz95',
 'Sz96',
 'J162738.3-243658',
 'J162739.0-235818',
 'J162618.9-242820',
 'J162730.2-242743',
 'J162733.1-244115',
 'J162649.0-243825',
 'J162616.8-242223',
 'J162636.8-241552',
 'J162536.7-241542',
 'J162656.8-241351',
 'J162624.1-241613',
 'J162854.1-244744',
 'J162755.6-242618',
 'J162713.7-241817',
 'J11095407-7629253',
 'J10590108-7722407',
 'J11100369-7633291',
 'J11100704-7629376',
 'J11085367-7521359',
 'J11095340-7634255',
 'J11075792-7738449',
 'J11173700-7704381',
 'J11080148-7742288',
 'J11092379-7623207',
 'J11105333-7634319',
 'J10555973-7724399',
 'DS_Tau',
 'DG_Tau',
 'HP_Tau',
 'J162755.6-242618',
 'J11092379-7623207',
 'J162755.6-242618',
 'J162713.7-241817',
 'J11100704-7629376',
 'pbcor',
 'J10581677-7717170',
 'mask'] # List of substrings to exclude

download_directory = '/Users/calebpainter/Downloads/DECO/fits_files/ROph'    # Local directory to save files
# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

async def get_file_links(session, url):
    """Fetches and parses the HTML to extract file links."""
    async with session.get(url) as response:
        html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not href.endswith('/'):  # Skip directories
            links.append(urljoin(url, href))
    return links

async def download_file(session, url, save_path):
    """Downloads a file from a given URL and saves it to the specified path with a progress bar."""
    async with session.get(url) as response:
        total_size = int(response.headers.get('content-length', 0))
        async with aio_open(save_path, 'wb') as file:
            async for chunk in response.content.iter_any(8192):
                if chunk:
                    await file.write(chunk)
                    # Update the progress bar (will be more complex in async context)
                    tqdm.write(f"Downloading {save_path}")

async def main():
    async with aiohttp.ClientSession() as session:
        file_links = await get_file_links(session, base_url)
        
        filtered_links = [
            (url, os.path.join(download_directory, os.path.basename(url)))
            for url in file_links
            if keyword in os.path.basename(url) and not any(substring in os.path.basename(url) for substring in exclude_substrings)
        ]
        
        tasks = [download_file(session, url, path) for url, path in filtered_links]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())