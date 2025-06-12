# YT-Downloader v2.0.0
**YouTube Video & Audio Downloader API**  
Developer: Sultan Arabi  
API Version: v1

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Server will start on:
- http://0.0.0.0:5000

## 📡 API Endpoints

### Base URL
```
https://your-repl-url.replit.dev/api
```

### 1. API Information
**GET /api/info**  
Get API version and developer information.

### 2. Available Formats
**GET /api/formats**  
Get all available video and audio quality options.

### 3. Video Information
**GET /api/video-info?url=YOUTUBE_URL**  
Get video metadata without downloading.

### 4. Download Content
**GET /api/download?url=YOUTUBE_URL&type=TYPE&quality=QUALITY**

**Parameters:**
- `url` (required): YouTube video URL
- `type` (required): "video" or "audio"
- `quality` (optional): Video/audio quality

## 🎯 Video Qualities
- `4k` - 4K (2160p)
- `1080p` - 1080p Full HD
- `720p` - 720p HD (Default)
- `480p` - 480p Standard
- `360p` - 360p Mobile
- `240p` - 240p Low

## 🎵 Audio Qualities
- `320kbps` - 320 kbps (Highest)
- `192kbps` - 192 kbps (Standard)
- `128kbps` - 128 kbps (Medium)
- `96kbps` - 96 kbps (Low)
- `64kbps` - 64 kbps (Lowest)

## 📋 Usage Examples

### Download Video
```
GET /api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=720p
```

### Download Audio
```
GET /api/download?url=https://youtu.be/VIDEO_ID&type=audio&quality=192kbps
```

### Get Video Info
```
GET /api/video-info?url=https://youtu.be/VIDEO_ID
```

## 🛠️ Programming Examples

### Python
```python
import requests

# Download video
response = requests.get('http://your-repl-url.replit.dev/api/download', 
                       params={
                           'url': 'https://youtu.be/VIDEO_ID',
                           'type': 'video',
                           'quality': '720p'
                       })

# Save file
with open('video.mp4', 'wb') as f:
    f.write(response.content)
```

### JavaScript
```javascript
// Download video
fetch('http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=720p')
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'video.mp4';
    a.click();
  });
```

### cURL
```bash
# Download video
curl -O -J "http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&type=video&quality=720p"

# Download audio
curl -O -J "http://your-repl-url.replit.dev/api/download?url=https://youtu.be/VIDEO_ID&type=audio&quality=192kbps"
```

## ⚠️ Error Responses
```json
{
  "status": "error",
  "message": "Error description"
}
```

**HTTP Status Codes:**
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## 📝 Notes
- Files are automatically named with video title
- Audio files converted to MP3 format
- Files auto-delete after 60 seconds
- Supports both youtu.be and youtube.com URLs

## 📞 Support & Contact
**Developer:** Sultan Arabi  
**Email:** sultanarabi161@gmail.com  
**Phone:** +880 1780982161  
**GitHub:** https://github.com/sultanarabi161  
**Social Media:** @sultanarabi161  

**Project:** YT-Downloader v2.0.0  
**API Version:** v1