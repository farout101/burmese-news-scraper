# Burmese News Scraper

This Scrapy project is designed to scrape news articles from various Burmese news websites. It includes spiders for different categories and websites, and it's configured to use Playwright for dynamic content rendering.

## Project Structure

```
burmese_news_scraper/
├── scrapy.cfg
├── burmese_news_scraper/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       ├── base/
│       │   ├── __init__.py
│       │   ├── mdngov_base.py
│       │   └── myawady_base.py
│       ├── mdngov_international_education.py
│       ├── mdngov_international_entertainment.py
│       ├── mdngov_international_political.py
│       ├── mdngov_international_sports.py
│       ├── mdngov_local_education.py
│       ├── mdngov_local_entertainment.py
│       ├── myawady_education.py
│       ├── myawady_sports.py
│       └── myawady_tech.py
├── deprecated_spiders/
│   └── mdngov_local_education.py
└── html_structures/
    ├── mdngov_international_education.html
    └── mdngov_local_education.html
```

### Key Files

- **`scrapy.cfg`**: The main configuration file for the Scrapy project.
- **`burmese_news_scraper/settings.py`**: Project settings, including middleware, pipelines, and other configurations.
- **`burmese_news_scraper/items.py`**: Defines the data structure (Scrapy Item) for the scraped data.
- **`burmese_news_scraper/spiders/`**: The directory containing the spider files.
- **`burmese_news_scraper/spiders/base/`**: This directory contains the base spiders that other spiders inherit from.
- **`deprecated_spiders/`**: Contains older versions of spiders that are no longer in use.
- **`html_structures/`**: Contains HTML files for reference and debugging.

## Architectural Approach: Base Spiders

This project employs a base spider architecture to promote code reusability and simplify the creation of new spiders. The core idea is to abstract the common scraping logic for each website into a base class. Each specific spider then inherits from the appropriate base class and only needs to define the specific `start_urls` and `category` for the section of the website it is targeting.

There are two base spiders:

- **`mdngov_base.py`**: This is the base spider for `mdn.gov.mm`. It uses Playwright to handle the dynamic JavaScript-heavy nature of the website. The `MDNGovBaseSpider` class encapsulates the logic for:
    - Initiating requests with Playwright.
    - Navigating through pagination.
    - Identifying and extracting article links.
    - Parsing the full article content.
    - Cleaning the HTML and extracting the relevant text.
    - Processing the text into individual sentences.
    - Yielding the cleaned data as `BurmeseNewsItem` objects.

- **`myawady_base.py`**: This is the base spider for `myawady.net.mm`. This website is simpler and does not require JavaScript rendering, so this spider uses standard Scrapy requests. The `MyawadyBaseSpider` class encapsulates the logic for:
    - Initiating standard Scrapy requests.
    - Navigating through pagination.
    - Identifying and extracting article links.
    - Parsing the full article content.
    - Extracting the relevant text.
    - Processing the text into individual sentences.
    - Yielding the cleaned data as `BurmeseNewsItem` objects.

By inheriting from these base spiders, we can quickly create new spiders for different sections of the same website without rewriting the core scraping logic. This makes the project more maintainable and scalable.

## Available Spiders

### MDN Gov (`mdn.gov.mm`)

- `mdngov_international_education`
- `mdngov_international_entertainment`
- `mdngov_international_political`
- `mdngov_international_sports`
- `mdngov_local_education`
- `mdngov_local_entertainment`

### Myawady (`myawady.net.mm`)

- `myawady_education`
- `myawady_sports`
- `myawady_tech`

## Scraped Data

The scraper extracts the following information from each article:

- **`text`**: The full text of the article.
- **`category`**: The category of the article (e.g., "Local Education", "Education", "Technology").
- **`source`**: The source website of the article (e.g., "mdn.gov.mm", "myawady.net.mm").
- **`url`**: The URL of the article.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd burmese_news_scraper
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**

    ```bash
    playwright install
    ```

## How to Run the Spiders

To run a spider, use the `scrapy crawl` command followed by the spider's name.

**Example:**

```bash
scrapy crawl mdngov_local_education -o output/mdngov_local_education.json
```

The scraped data will be saved in the specified output file.

## Configuration

The project's settings can be configured in the `burmese_news_scraper/settings.py` file. Some of the key settings include:

- **`DOWNLOAD_DELAY`**: The delay between requests to the same website.
- **`USER_AGENT`**: The user agent to use for requests.
- **`ITEM_PIPELINES`**: The pipelines to use for processing the scraped data.
- **`PLAYWRIGHT_BROWSER_TYPE`**: The browser to use for Playwright (e.g., "chromium", "firefox", "webkit").
- **`PLAYWRIGHT_LAUNCH_OPTIONS`**: The launch options for Playwright (e.g., `{"headless": True}` for headless mode).

## Deprecated Spiders and HTML Structures

- **`deprecated_spiders/`**: This directory contains older versions of spiders that are no longer in use. These are kept for reference purposes.
- **`html_structures/`**: This directory contains HTML files that were used for debugging and understanding the structure of the target websites.