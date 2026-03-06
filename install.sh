#!/bin/bash

apt update
apt install -y sshpass pandoc libreoffice  poppler-utils qpdf tesseract-ocr tesseract-ocr-chi-sim python3-pip fonts-noto-cjk fonts-dejavu libreoffice-calc jq xvfb jq
apt install -y chromium-browser chromium-chromedriver xvfb

npm install -g docx pptxgenjs agent-browser

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com
pip install --upgrade pip
pip install "playwright>=1.40.0"
pip install "beautifulsoup4>=4.12.0"
pip install "html2text>=2020.1.16"
pip install "requests>=2.31.0"
pip install "aiohttp>=3.9.0"
pip install "tqdm>=4.66.0"
pip install httpx
pip install rich
pip install akshare
pip install pandas
pip install numpy
pip install "selenium>=4.0.0"
pip install "webdriver-manager>=3.8.0"
pip install opencv-python
pip install openpyxl
pip install defusedxml
pip install lxml
pip install "pillow>=10.0.0"
pip install "imageio>=2.31.0"
pip install "imageio-ffmpeg>=0.4.9"
pip install pypdf
pip install pdfplumber
pip install reportlab
pip install pytesseract
pip install pdf2image
pip install python-pptx
pip install python-docx
pip install pyyaml
pip install uv
pip3 install "markitdown[pptx]"
