# Payload Generator Pecha

A Python application for uploading text segments, table of contents, and commentary mappings to the WebBuddhist API. This project provides tools for processing and uploading Buddhist texts with their associated metadata and structure.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Segment Upload](#segment-upload)
  - [Table of Contents Upload](#table-of-contents-upload)
  - [Text Mapping](#text-mapping)
  - [Metadata Upload](#metadata-upload)
- [File Structure Requirements](#file-structure-requirements)
- [Testing](#testing)
- [Logging](#logging)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## 🚀 Features

- **Segment Upload**: Upload text segments to WebBuddhist API
- **Table of Contents Upload**: Upload structured TOC with segment references
- **Text Mapping**: Map commentary texts to root texts
- **Metadata Upload**: Upload text metadata and information
- **Comprehensive Testing**: Full test suite with mocking
- **Logging**: Detailed logging for all operations
- **Error Handling**: Robust error handling and validation

## 📁 Project Structure

```
payload_generator_pecha/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .venv/                             # Virtual environment
├── utils.py                           # Utility functions
├── segment_uploader_webuddhist.py     # Main segment uploader
├── toc_uploader_webuddhist.py         # Table of contents uploader
├── src/
│   └── metadata_uploader.py           # Metadata uploader
├── mapping/
│   ├── text_mapping.py                # Text mapping functionality
│   ├── mapping_models.py              # Data models for mapping
│   └── mapping_data/                  # Mapping data files
├── test/
│   ├── test_segment_uploader_webuddhist.py  # Test suite
│   └── data/                          # Test data files
│       ├── dummy_segment_upload_payload.json
│       ├── dummy_api_response.json
│       └── dummy_segment_content_with_segment_id.json
├── data/
│   └── metadata.json                  # Project metadata
├── [text_name]/                       # Text-specific directories
│   ├── [text_name]_payload/           # Payload files
│   │   ├── [text_name]_root_text_segment_payload.json
│   │   ├── [text_name]_root_text_toc_payload.json
│   │   └── [text_name]_commentary_[1-3]_text_segment_payload.json
│   └── [text_name]_api_response/      # API response files
│       └── [text_name]_segment_content_with_segment_id.json
└── pecha_segment_upload_payload/      # Pre-generated payloads
    ├── choejuk_root_text.json
    ├── choejuk_commentary_1.json
    └── ... (other text files)
```

## 🔧 Prerequisites

- Python 3.12 or higher
- Virtual environment support
- Internet connection for API calls
- WebBuddhist API credentials

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd payload_generator_pecha
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install requests pytest Levenshtein pydantic
```

### 4. Verify Installation
```bash
python -m pytest --version
python -c "import requests; print('Dependencies installed successfully')"
```

## ⚙️ Configuration

### Environment Variables Setup

The application uses environment variables for configuration to keep sensitive information secure.

#### 1. Create Environment File
```bash
# Copy the template file
cp env.template .env

# Edit the .env file with your actual values
nano .env  # or use your preferred editor
```

#### 2. Configure Your .env File
```bash
# WebBuddhist API Configuration
WEBUDDHIST_API_BASE_URL=https://your-api-domain.com
WEBUDDHIST_SEGMENTS_ENDPOINT=/api/v1/segments
WEBUDDHIST_TOC_ENDPOINT=/api/v1/texts/table-of-content
WEBUDDHIST_AUTH_ENDPOINT=/api/v1/auth/login

# Optional: Pre-configure credentials (not recommended for production)
# WEBUDDHIST_EMAIL=your-email@example.com
# WEBUDDHIST_PASSWORD=your-password

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### 3. Security Notes
- **Never commit your `.env` file** to version control
- The `.env` file is already in `.gitignore`
- For production, use proper secret management systems
- If credentials are not in `.env`, the application will prompt for them

### Authentication
You'll need WebBuddhist API credentials. You can either:
1. **Set them in `.env` file** (not recommended for production)
2. **Enter them when prompted** (recommended for security)

## 🎯 Usage

### Segment Upload

Upload text segments to the WebBuddhist API.

#### Command Line Usage:
```bash
python segment_uploader_webuddhist.py
```

#### Interactive Prompts:
1. **Text name**: Enter the name of your text (e.g., `heart_sutra`, `diamond_cutter`)
2. **Root or commentary**: Enter `root` or `commentary_1`, `commentary_2`, `commentary_3`
3. **Email/Password**: Enter your WebBuddhist API credentials

#### Required File Structure:
```
[text_name]/
├── [text_name]_payload/
│   └── [text_name]_[root_or_commentary]_text_segment_payload.json
└── [text_name]_api_response/  # Created automatically
    └── [text_name]_[root_or_commentary]_segment_content_with_segment_id.json
```

#### Example:
```bash
$ python segment_uploader_webuddhist.py
Enter the text name: heart_sutra
Enter the root or commentary_[1,2,3]: root
Enter your email: user@example.com
Enter your password: ********
```

This will:
1. Read `heart_sutra/heart_sutra_payload/heart_sutra_root_text_segment_payload.json`
2. Upload segments to the API
3. Save response to `heart_sutra/heart_sutra_api_response/heart_sutra_root_segment_content_with_segment_id.json`
4. Log activities to `segment_upload_log.txt`

### Table of Contents Upload

Upload table of contents with segment references.

#### Command Line Usage:
```bash
python toc_uploader_webuddhist.py
```

#### Prerequisites:
- Segments must be uploaded first (requires segment ID mapping file)
- TOC payload file must exist

#### Required Files:
```
[text_name]/
├── [text_name]_payload/
│   └── [text_name]_[root_or_commentary]_text_toc_payload.json
└── [text_name]_api_response/
    └── [text_name]_[root_or_commentary]_segment_content_with_segment_id.json
```

### Text Mapping

Map commentary texts to root texts.

#### Command Line Usage:
```bash
python mapping/text_mapping.py
```

### Metadata Upload

Upload text metadata.

#### Command Line Usage:
```bash
python src/metadata_uploader.py
```

## 📄 File Structure Requirements

### Segment Payload Format
```json
{
    "text_id": "uuid-string",
    "segments": [
        {
            "content": "Text content here\n",
            "type": "source",
            "mapping": []
        }
    ]
}
```

### TOC Payload Format
```json
{
    "text_id": "uuid-string",
    "sections": [
        {
            "title": "Chapter 1",
            "segments": [
                {
                    "segment_id": "segment-content-to-match"
                }
            ]
        }
    ]
}
```

## 🧪 Testing

### Run All Tests
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run tests with pytest
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest test/test_segment_uploader_webuddhist.py -v
```

### Run Tests with Coverage
```bash
python -m pytest --cov=segment_uploader_webuddhist test/
```

### Test Structure
The test suite includes:
- **16 comprehensive test cases**
- **Mock external dependencies** (API calls, file I/O, user input)
- **Error handling tests** (network errors, file permissions, invalid data)
- **Edge case testing** (empty data, malformed responses)
- **Integration tests** (full workflow testing)

### Test Data
Test data is stored in `test/data/`:
- `dummy_segment_upload_payload.json` - Sample input payload
- `dummy_api_response.json` - Mock API response
- `dummy_segment_content_with_segment_id.json` - Expected output format

## 📊 Logging

### Log Files
- `segment_upload_log.txt` - Segment upload activities
- `toc_upload_log.txt` - TOC upload activities

### Log Format
```
2024-01-01 12:00:00,000 [INFO] Uploading segments to webuddhist
2024-01-01 12:00:01,000 [INFO] Segments uploaded, 200
2024-01-01 12:00:01,100 [INFO] Segments uploaded successfully for text_id: uuid-string
```

## 🌐 API Endpoints

The application uses configurable API endpoints defined in your `.env` file:

### Segments Endpoint
- **URL**: `{WEBUDDHIST_API_BASE_URL}{WEBUDDHIST_SEGMENTS_ENDPOINT}`
- **Method**: POST
- **Headers**: `Authorization: Bearer <token>`
- **Body**: JSON payload with segments

### Table of Contents Endpoint
- **URL**: `{WEBUDDHIST_API_BASE_URL}{WEBUDDHIST_TOC_ENDPOINT}`
- **Method**: POST
- **Headers**: `Authorization: Bearer <token>`
- **Body**: JSON payload with TOC structure

### Authentication Endpoint
- **URL**: `{WEBUDDHIST_API_BASE_URL}{WEBUDDHIST_AUTH_ENDPOINT}`
- **Method**: POST
- **Body**: JSON with email and password

## 🔍 Troubleshooting

### Common Issues

#### 1. Module Import Errors
```bash
ModuleNotFoundError: No module named 'segment_uploader_webuddhist'
```
**Solution**: Make sure virtual environment is activated and you're in the project root:
```bash
source .venv/bin/activate
cd /path/to/payload_generator_pecha
python -m pytest
```

#### 2. File Not Found Errors
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'text_name/text_name_payload/...'
```
**Solution**: Ensure your file structure matches the expected format:
- Create the text directory: `mkdir [text_name]`
- Create payload directory: `mkdir [text_name]/[text_name]_payload`
- Place your JSON payload file in the correct location

#### 3. Authentication Errors
```bash
401 Unauthorized
```
**Solution**: 
- Verify your WebBuddhist API credentials
- Check if your account has the necessary permissions
- Ensure the API endpoints are correct

#### 4. Network Connection Issues
```bash
ConnectionError: Failed to establish a new connection
```
**Solution**:
- Check your internet connection
- Verify the API endpoints are accessible
- Check if there are any firewall restrictions

### Debug Mode
For detailed debugging, you can modify the logging level in the scripts:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Testing Without API Calls
Use the test suite to verify functionality without making actual API calls:
```bash
python -m pytest test/test_segment_uploader_webuddhist.py::TestSegmentUploader::test_upload_segments_to_webuddhist_success -v
```

## 📝 Example Workflow

### Complete Upload Process

1. **Prepare your text files**:
   ```bash
   mkdir heart_sutra
   mkdir heart_sutra/heart_sutra_payload
   # Place your segment payload JSON file
   ```

2. **Upload segments**:
   ```bash
   python segment_uploader_webuddhist.py
   # Enter: heart_sutra
   # Enter: root
   # Enter credentials
   ```

3. **Upload table of contents**:
   ```bash
   python toc_uploader_webuddhist.py
   # Enter: heart_sutra  
   # Enter: root
   # Enter credentials
   ```

4. **Verify uploads**:
   ```bash
   # Check log files
   tail segment_upload_log.txt
   tail toc_upload_log.txt
   
   # Check generated response files
   ls heart_sutra/heart_sutra_api_response/
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `python -m pytest`
5. Submit a pull request

## 📄 License

[Add your license information here]

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test cases for usage examples
3. Check log files for detailed error information
4. Create an issue in the repository

---

**Note**: Always test with small datasets first before uploading large collections of texts.
