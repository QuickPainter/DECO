import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from tqdm import tqdm

# Configurations
base_url = 'https://bulk.cv.nrao.edu/deco/users/cjlaw/IMAGING/Images_v2/ChaI/Images/'  # URL of the directory listing
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

download_directory = '/Users/calebpainter/Downloads/DECO/fits_files/ChamI'    # Local directory to save files

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

def get_file_links(url):
    """Fetches and parses the HTML to extract file links."""
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in tqdm(soup.find_all('a', href=True)):
        href = a_tag['href']
        if not href.endswith('/'):  # Skip directories
            links.append(urljoin(url, href))
    return links

def download_file(url, save_path):
    """Downloads a file from a given URL and saves it to the specified path."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as file, tqdm(
        desc=save_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
            
def main():
    file_links = get_file_links(base_url)
    print('file links', file_links)
    for file_url in file_links:
        filename = os.path.basename(file_url)
        if keyword in filename and not any(substring in filename for substring in exclude_substrings):
            save_path = os.path.join(download_directory, filename)
            print(f"Downloading {file_url} to {save_path}")
            download_file(file_url, save_path)

if __name__ == '__main__':
    main()
