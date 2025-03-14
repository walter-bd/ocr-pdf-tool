# PDF Processing Service with OCR

A Sanic-based web service for processing PDF files with OCR text detection and insertion. It allows users to upload PDF files, which are processed asynchronously using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR), and return the modified PDF with detected text embedded at the detected positions. The UI is built using Vue.js for simplicity.

---

### Table of Contents
- [PDF Processing Service with OCR](#pdf-processing-service-with-ocr)
    - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Server](#running-the-server)
    - [Uploading PDF via Web UI:](#uploading-pdf-via-web-ui)
    - [Command-Line Usage (cURL):](#command-line-usage-curl)
  - [Dependencies](#dependencies)
  - [License](#license)
  - [This project is licensed under the Apache License 2.0. See LICENSE for details.](#this-project-is-licensed-under-the-apache-license-20-see-license-for-details)
  - [Contributions](#contributions)

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/[your-repo]/pdf-ocr-service.git
   cd pdf-ocr-service
   ```

2. **Install dependencies** (create a virtual environment first if preferred):
   ```bash
   pip install -r requirements.txt  # Ensure requirements.txt includes:
   # sanic sanic-jinja2 sanic-session paddleocr numpy pypdfium2
   ```

3. **Install PaddleOCR models**:
   ```bash
   # The Latin language model is required (ensure your environment meets PaddleOCR's prerequisites)
   pip install paddleocr[extra]
   ```

---

## Usage

### Running the Server
1. Start the Sanic application:
   ```bash
   sanic app --port 5000
   ```
   The server runs on `http://localhost:5000`.

### Running the Server on docker

```bash
docker build -t ocr-pdf-tool .
docker run -it --rm -p 5000:5000 -v .paddleocr:/root/.paddleocr ocr-pdf-tool
```

### Uploading PDF via Web UI:
1. Open the browser and go to `http://localhost:5000`.

2. Select a PDF file from your computer and click "Process PDF". The output PDF will be downloaded automatically.

### Command-Line Usage (cURL):
```bash
curl -X POST -F 'file=@path/to/your/file.pdf' http://localhost:5000/process-pdf -o output.pdf
```

---

## Dependencies

| Package                | Description                          |
|------------------------|--------------------------------------|
| **Sanic**              | Fast Python web server               |
| **PaddleOCR**          | OCR engine from PaddlePaddle         |
| **pypdfium2**          | PDF rendering/pdf modification library |
| **numpy**              | Array processing                     |
| **Vue.js (template)**  | Lightweight frontend framework       |

---

## License
This project is licensed under the Apache License 2.0. See LICENSE for details.

## Contributions
Contributions are welcome! For issues or feature requests, please open an [issue](https://github.com/[your-repo]/issues).