# RDV Finder 

**CAPTCHA Extraction and Image Processing Using Selenium and Python**

## Overview

This project automates the process of navigating to web pages, capturing HTML content, extracting CAPTCHA images, and processing screenshots for targeted image cropping. Additionally, it leverages a transformer-based pre-trained model for optical character recognition (OCR) using **TrOCR** from the **Transformers** library by Hugging Face.

The notebook uses Python libraries such as `Selenium` for web scraping, `BeautifulSoup` for HTML parsing, `Pillow` for image processing, and `Transformers` for OCR.

## Workflow

### 1. Setting Up the Web Scraping Environment

The project initializes by setting up essential libraries and functions:
- **`setup_driver()`**: Configures a Selenium WebDriver with randomized user-agent strings and viewport sizes to simulate human-like browsing behavior. This setup helps avoid detection on websites with basic bot protection.

### 2. HTML Extraction and CAPTCHA Downloading

The next steps involve extracting HTML content and downloading CAPTCHA images:
- **`get_html(url)`**: Navigates to a specified URL and waits for the page to load fully. It then retrieves the page source HTML.
- **`get_captcha(html, id)`**: Parses the HTML to locate the CAPTCHA image by its `id` attribute. It then downloads the image directly from the source URL as `downloaded_image.png`.

### 3. Full-Page Screenshots and Cropping

To ensure that CAPTCHAs are accurately captured:
- **`get_captcha(url)`**: This function navigates to the specified URL, waits for loading, and scrolls to a predefined position to capture a full-page screenshot saved as `full_screenshot.png`.
- **Cropping the Screenshot**: The screenshot is cropped based on calculated dimensions around the image's center, saving the output as `element_screenshot.png`.

### 4. OCR using Transformer-Based Model

The project includes a transformer-based model, **TrOCR** (Text Recognition Optical Character Recognition), for recognizing and extracting text from images. The following model and processor are used:
   ```python
   from transformers import TrOCRProcessor, VisionEncoderDecoderModel
   from PIL import Image
   import torch

   # Load the pre-trained TrOCR model and processor
   processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
   model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

