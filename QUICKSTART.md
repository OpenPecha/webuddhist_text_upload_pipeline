# Quick Start Guide

Get up and running with Payload Generator Pecha in 5 minutes!

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m pytest test/test_segment_uploader_webuddhist.py -v
```

## 🔧 Configure Environment

Set up your API configuration:

```bash
# Copy the environment template
cp env.template .env

# Edit with your actual API details
nano .env
```

Your `.env` file should look like:
```bash
WEBUDDHIST_API_BASE_URL=https://your-api-domain.com
WEBUDDHIST_SEGMENTS_ENDPOINT=/api/v1/segments
WEBUDDHIST_TOC_ENDPOINT=/api/v1/texts/table-of-content
WEBUDDHIST_AUTH_ENDPOINT=/api/v1/auth/login
ENVIRONMENT=development
```

## 📁 Prepare Your Files

Create the directory structure for your text:

```bash
# Example for "heart_sutra" text
mkdir -p heart_sutra/heart_sutra_payload
mkdir -p heart_sutra/heart_sutra_api_response
```

Place your segment payload file:
```bash
# Your JSON file should be named:
heart_sutra/heart_sutra_payload/heart_sutra_root_text_segment_payload.json
```

## 🎯 Upload Segments

```bash
# Activate virtual environment
source .venv/bin/activate

# Run segment uploader
python segment_uploader_webuddhist.py
```

When prompted:
- **Text name**: `heart_sutra`
- **Root or commentary**: `root`
- **Email**: Your WebBuddhist API email
- **Password**: Your WebBuddhist API password

## ✅ Verify Upload

Check the logs:
```bash
tail segment_upload_log.txt
```

Check the generated response file:
```bash
ls heart_sutra/heart_sutra_api_response/
cat heart_sutra/heart_sutra_api_response/heart_sutra_root_segment_content_with_segment_id.json
```

## 🧪 Run Tests

```bash
# Run all tests
python -m pytest

# Run specific test with verbose output
python -m pytest test/test_segment_uploader_webuddhist.py -v

# Run single test
python -m pytest test/test_segment_uploader_webuddhist.py::TestSegmentUploader::test_segment_uploader_initialization -v
```

## 📋 Example Payload File

Create `heart_sutra/heart_sutra_payload/heart_sutra_root_text_segment_payload.json`:

```json
{
    "text_id": "your-uuid-here",
    "segments": [
        {
            "content": "འཇམ་དཔལ་གཞོན་ནུར་གྱུར་པ་ལ་ཕྱག་འཚལ་ལོ། །\n",
            "type": "source",
            "mapping": []
        },
        {
            "content": "བཅོམ་ལྡན་འདས་མ་ཤེས་རབ་ཀྱི་ཕ་རོལ་ཏུ་ཕྱིན་པ་ཧྲཱིཿ\n",
            "type": "source", 
            "mapping": []
        }
    ]
}
```

## 🔧 Troubleshooting

### Import Error
```bash
ModuleNotFoundError: No module named 'segment_uploader_webuddhist'
```
**Solution**: Make sure you're in the project root and virtual environment is activated:
```bash
source .venv/bin/activate
pwd  # Should show: .../payload_generator_pecha
```

### File Not Found
```bash
FileNotFoundError: No such file or directory
```
**Solution**: Check your file structure matches the expected format:
```bash
ls -la heart_sutra/heart_sutra_payload/
# Should contain: heart_sutra_root_text_segment_payload.json
```

### Test Failures
```bash
# Run tests to identify issues
python -m pytest -v

# Check if all dependencies are installed
python -c "import requests, Levenshtein, pydantic, pytest; print('All good!')"
```

## 📞 Need Help?

1. Check the full [README.md](README.md) for detailed documentation
2. Look at test files in `test/data/` for example formats
3. Check log files for detailed error messages
4. Ensure your virtual environment is activated: `source .venv/bin/activate`

## 🎉 Success!

If everything works, you should see:
- ✅ Tests passing
- ✅ Log entries in `segment_upload_log.txt`
- ✅ Response file created in `[text_name]_api_response/` directory

Ready to upload more texts? Just repeat the process with different text names!
