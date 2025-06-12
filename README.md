# YT-Downloader v2.0.0
**YouTube Video & Audio Downloader API**  
Developer: Sultan Arabi  
API Version: v1

## 🚀 Quick Start

### Installation Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Or using uv (recommended)
uv sync

# Run the application
python main.py
```

### Server will start on:
- Local: http://127.0.0.1:5000
- Network: http://0.0.0.0:5000

## 📡 API Documentation

### Base URL
```
https://your-repl-url.replit.dev/api
```

### 1. API Information
**Endpoint:** `GET /api/info`  
**Description:** Get API version, developer info, and available endpoints

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "yt-downloader",
    "version": "2.0.0",
    "developer": "Sultan Arabi",
    "api_version": "v1",
    "description": "YouTube Video & Audio Downloader API",
    "last_updated": "2025-01-12"
  },
  "endpoints": {
    "info": "/api/info",
    "download": "/api/download",
    "video_info": "/api/video-info",
    "formats": "/api/formats"
  }
}
```

### 2. Available Formats
**Endpoint:** `GET /api/formats`  
**Description:** Get all available video and audio quality options

**Response:**
```json
{
  "status": "success",
  "data": {
    "video_qualities": {
      "best[height<=2160]/best": "4K (2160p)",
      "best[height<=1080]/best": "1080p Full HD",
      "best[height<=720]/best": "720p HD",
      "best[height<=480]/best": "480p Standard",
      "best[height<=360]/best": "360p Mobile",
      "best[height<=240]/best": "240p Low",
      "worst": "Lowest Available"
    },
    "audio_qualities": {
      "320": "320 kbps (Highest)",
      "256": "256 kbps (High)",
      "192": "192 kbps (Standard)",
      "128": "128 kbps (Medium)",
      "96": "96 kbps (Low)",
      "64": "64 kbps (Lowest)"
    },
    "types": ["video", "audio"]
  }
}
```

### 3. Video Information
**Endpoint:** `GET /api/video-info`  
**Parameters:**
- `url` (required): YouTube video URL

**Example:**
```
GET /api/video-info?url=https://youtu.be/VIDEO_ID
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "title": "Video Title",
    "uploader": "Channel Name",
    "duration": 180,
    "view_count": 1000000,
    "upload_date": "20240101",
    "description": "Video description...",
    "thumbnail": "https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg",
    "webpage_url": "https://www.youtube.com/watch?v=VIDEO_ID"
  }
}
```

### 4. Download Video
**Endpoint:** `GET /api/download`  
**Parameters:**
- `url` (required): YouTube video URL
- `type` (required): "video" or "audio"
- `quality` (optional): Video quality (default: "best[height<=720]/best")
- `audio_quality` (optional): Audio quality in kbps (default: "192")

**Video Download Examples:**
```bash
# 720p HD Video
GET /api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=best[height<=720]/best

# 1080p Full HD Video
GET /api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=best[height<=1080]/best

# 4K Video
GET /api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=best[height<=2160]/best
```

**Audio Download Examples:**
```bash
# Standard Quality Audio (192 kbps)
GET /api/download?url=https://youtu.be/VIDEO_ID&type=audio&audio_quality=192

# High Quality Audio (320 kbps)
GET /api/download?url=https://youtu.be/VIDEO_ID&type=audio&audio_quality=320

# Low Quality Audio (128 kbps)
GET /api/download?url=https://youtu.be/VIDEO_ID&type=audio&audio_quality=128
```

### 5. Download Information
**Endpoint:** `GET /api/download-info`  
**Description:** Get download information without actually downloading
**Parameters:**
- `url` (required): YouTube video URL
- `type` (required): "video" or "audio"
- `quality` (optional): Video/audio quality

**Example:**
```
GET /api/download-info?url=https://youtu.be/VIDEO_ID&type=video&quality=best[height<=720]/best
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "title": "Video Title",
    "uploader": "Channel Name",
    "duration": 180,
    "thumbnail": "https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg",
    "requested_quality": "best[height<=720]/best",
    "requested_type": "video",
    "estimated_filename": "Video_Title_video.mp4"
  }
}
```

## 🛠️ Usage Examples

### Python Example
```python
import requests

# Get video info
response = requests.get('http://your-repl-url.replit.dev/api/video-info', 
                       params={'url': 'https://youtu.be/VIDEO_ID'})
print(response.json())

# Download video
response = requests.get('http://your-repl-url.replit.dev/api/download', 
                       params={
                           'url': 'https://youtu.be/VIDEO_ID',
                           'type': 'video',
                           'quality': 'best[height<=720]/best'
                       })

# Save file
with open('downloaded_video.mp4', 'wb') as f:
    f.write(response.content)
```

### JavaScript Example
```javascript
// Get video info
fetch('http://your-repl-url.replit.dev/api/video-info?url=https://youtu.be/VIDEO_ID')
  .then(response => response.json())
  .then(data => console.log(data));

// Download video
fetch('http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&format=video&quality=720p')
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'video.mp4';
    a.click();
  });
```

### cURL Examples
```bash
# Get API info
curl "http://your-repl-url.replit.dev/api/info"

# Get video info
curl "http://your-repl-url.replit.dev/api/video-info?url=https://youtu.be/VIDEO_ID"

# Download video
curl -O -J "http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=best[height<=720]/best"

# Download audio
curl -O -J "http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&type=audio&audio_quality=192"
```

## ⚙️ Available Video Qualities
- `best[height<=2160]/best` - 4K (2160p)
- `best[height<=1080]/best` - 1080p Full HD
- `best[height<=720]/best` - 720p HD (Recommended)
- `best[height<=480]/best` - 480p Standard
- `best[height<=360]/best` - 360p Mobile
- `best[height<=240]/best` - 240p Low
- `worst` - Lowest Available

## 🎵 Available Audio Qualities
- `320` - 320 kbps (Highest)
- `256` - 256 kbps (High)
- `192` - 192 kbps (Standard)
- `128` - 128 kbps (Medium)
- `96` - 96 kbps (Low)
- `64` - 64 kbps (Lowest)

## 🚨 Error Responses
All error responses follow this format:
```json
{
  "status": "error",
  "message": "Error description"
}
```

**Common HTTP Status Codes:**
- `400` - Bad Request (Invalid URL or parameters)
- `404` - Endpoint not found
- `500` - Internal server error

## 📝 Notes
- All downloads are temporary and automatically deleted after 30-60 seconds
- Audio files are converted to MP3 format
- Video files maintain their original format (usually MP4)
- Large files may take longer to process
- The API supports both short (youtu.be) and long (youtube.com) URL formats

## 🔧 Development Commands
```bash
# Start development server
python main.py

# Install new dependencies
pip install package_name
uv add package_name

# Update dependencies
pip install -r requirements.txt --upgrade
uv sync --upgrade
```

## 📞 Support
For any issues or questions, please contact:
- Developer: Sultan Arabi
- Project: YT-Downloader v2.0.0
- API Version: v1