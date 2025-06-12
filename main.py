from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import yt_dlp
import os
import time
import random
import re
import tempfile
from werkzeug.utils import secure_filename
import threading
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sultan-arabi-yt-downloader-secret-key'

# Project Information
PROJECT_INFO = {
    "name": "yt-downloader",
    "version": "2.0.0",
    "developer": "Sultan Arabi",
    "api_version": "v1",
    "description": "YouTube Video & Audio Downloader API",
    "last_updated": "2025-01-12",
    "contact": {
        "email": "sultanarabi161@gmail.com",
        "phone": "+880 1780982161",
        "github": "https://github.com/sultanarabi161",
        "social": "@sultanarabi161"
    }
}

# Global variable to store download progress
download_progress = {}

def is_valid_youtube_url(url):
    """Validate YouTube URL"""
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/',
        r'(https?://)?(www\.)?youtube\.com/watch\?v=',
        r'(https?://)?(www\.)?youtu\.be/',
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

def progress_hook(d):
    """Progress hook for yt-dlp"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
        elif 'total_bytes_estimate' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
        else:
            percent = 0
        
        download_progress[d.get('filename', 'unknown')] = {
            'percent': percent,
            'status': 'downloading'
        }
    elif d['status'] == 'finished':
        download_progress[d.get('filename', 'unknown')] = {
            'percent': 100,
            'status': 'finished'
        }

def get_safe_filename(title):
    """Create a safe filename from video title"""
    # Remove invalid characters and limit length
    safe_chars = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_chars = re.sub(r'\s+', '_', safe_chars.strip())
    return safe_chars[:100] if len(safe_chars) > 100 else safe_chars

def download_youtube_content(url, quality, format_type, audio_quality='192'):
    """Core download function"""
    try:
        # Create temporary directory for downloads
        temp_dir = tempfile.mkdtemp()
        timestamp = str(int(time.time())) + "_" + str(random.randint(1000, 9999))
        
        # Get video info first
        info_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = get_safe_filename(info.get('title', 'Unknown'))
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
        
        # Configure yt-dlp options based on format type
        if format_type == 'audio':
            # For audio, create a specific filename
            safe_title = get_safe_filename(info.get('title', 'Unknown'))
            output_template = os.path.join(temp_dir, f'{safe_title}_audio.%(ext)s')
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best[acodec!=none]',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': str(audio_quality),
                }],
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True,
                'restrictfilenames': True,
                'prefer_ffmpeg': True,
                'keepvideo': False,
            }
        else:
            # For video, create a specific filename with quality info
            safe_title = get_safe_filename(info.get('title', 'Unknown'))
            quality_suffix = quality.split('[')[1].split(']')[0] if '[' in quality and ']' in quality else 'video'
            output_template = os.path.join(temp_dir, f'{safe_title}_{quality_suffix}.%(ext)s')
            ydl_opts = {
                'format': quality,
                'outtmpl': output_template,
                'progress_hooks': [progress_hook],
                'quiet': True,
                'restrictfilenames': True,
                'merge_output_format': 'mp4',
                'prefer_ffmpeg': True,
            }
        
        # Set ffmpeg path if available
        try:
            import subprocess
            ffmpeg_path = subprocess.check_output(['which', 'ffmpeg'], text=True).strip()
            ydl_opts['ffmpeg_location'] = ffmpeg_path
        except:
            # Try common paths
            for path in ['/usr/bin/ffmpeg', '/usr/local/bin/ffmpeg', '/nix/store/*/bin/ffmpeg']:
                import glob
                matches = glob.glob(path)
                if matches:
                    ydl_opts['ffmpeg_location'] = matches[0]
                    break
        
        # Download the content
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # Find the downloaded file
            downloaded_files = []
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if os.path.isfile(file_path):
                    downloaded_files.append(file_path)
            
            if downloaded_files:
                file_path = downloaded_files[0]
                file_size = os.path.getsize(file_path)
                original_filename = os.path.basename(file_path)
                
                return {
                    'success': True,
                    'file_path': file_path,
                    'filename': original_filename,
                    'title': info.get('title', 'Unknown'),  # Use original title
                    'duration': duration,
                    'uploader': uploader,
                    'file_size': file_size,
                    'temp_dir': temp_dir
                }
            else:
                return {
                    'success': False,
                    'error': 'Download completed but file not found'
                }
                
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Web Interface Routes
@app.route('/')
def index():
    return render_template('index.html', project_info=PROJECT_INFO)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.form.get('url', '').strip()
        quality_param = request.form.get('quality', 'best[height<=720]/best')
        format_type = request.form.get('format_type', 'video')
        audio_quality = request.form.get('audio_quality', '192')
        
        # Map quality for web interface
        web_quality_mapping = {
            'best[height<=720]/best': 'best[height<=720]/bestvideo[height<=720]+bestaudio/best',
            'best[height<=1080]/best': 'best[height<=1080]/bestvideo[height<=1080]+bestaudio/best',
            'best[height<=480]/best': 'best[height<=480]/bestvideo[height<=480]+bestaudio/best',
            'best[height<=360]/best': 'best[height<=360]/bestvideo[height<=360]+bestaudio/best',
            'worst': 'worst/bestvideo+bestaudio'
        }
        
        quality = web_quality_mapping.get(quality_param, quality_param)
        
        # Validate YouTube URL
        if not url or not is_valid_youtube_url(url):
            return jsonify({'error': 'Please enter a valid YouTube URL!'}), 400
        
        # Download content
        result = download_youtube_content(url, quality, format_type, audio_quality)
        
        if result['success']:
            file_path = result['file_path']
            temp_dir = result['temp_dir']
            
            # Send file for download
            def cleanup_file():
                time.sleep(30)  # Wait 30 seconds before cleanup
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    os.rmdir(temp_dir)
                except:
                    pass
            
            # Start cleanup in background
            cleanup_thread = threading.Thread(target=cleanup_file)
            cleanup_thread.daemon = True
            cleanup_thread.start()
            
            return send_file(
                file_path,
                as_attachment=True,
                download_name=result['filename']
            )
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# API Routes
@app.route('/api/info', methods=['GET'])
def api_info():
    """API Information endpoint"""
    return jsonify({
        'status': 'success',
        'data': PROJECT_INFO,
        'endpoints': {
            'info': '/api/info',
            'download': '/api/download',
            'video_info': '/api/video-info',
            'formats': '/api/formats'
        },
        'usage': {
            'download_video': '/api/download?url=<youtube_url>&format=video&quality=<quality>',
            'download_audio': '/api/download?url=<youtube_url>&format=audio&quality=<audio_quality>',
            'examples': {
                'video_720p': '/api/download?url=https://youtu.be/VIDEO_ID&format=video&quality=720p',
                'video_1080p': '/api/download?url=https://youtu.be/VIDEO_ID&format=video&quality=1080p',
                'audio_320': '/api/download?url=https://youtu.be/VIDEO_ID&format=audio&quality=320kbps',
                'audio_192': '/api/download?url=https://youtu.be/VIDEO_ID&format=audio&quality=192kbps'
            }
        }
    })

@app.route('/api/formats', methods=['GET'])
def api_formats():
    """Available formats and qualities"""
    return jsonify({
        'status': 'success',
        'data': {
            'video_qualities': {
                '4k': '4K (2160p)',
                '2160p': '4K (2160p)', 
                '1080p': '1080p Full HD',
                '720p': '720p HD (Recommended)',
                '480p': '480p Standard',
                '360p': '360p Mobile',
                '240p': '240p Low',
                'best': 'Best Available',
                'worst': 'Lowest Available'
            },
            'audio_qualities': {
                '320kbps': '320 kbps (Highest)',
                '256kbps': '256 kbps (High)', 
                '192kbps': '192 kbps (Standard)',
                '128kbps': '128 kbps (Medium)',
                '96kbps': '96 kbps (Low)',
                '64kbps': '64 kbps (Lowest)'
            },
            'formats': ['video', 'audio'],
            'parameters': {
                'url': 'YouTube video URL (required)',
                'format': 'video or audio (required)',
                'quality': 'Video: 4k, 1080p, 720p, 480p, 360p, 240p | Audio: 320kbps, 256kbps, 192kbps, 128kbps, 96kbps, 64kbps'
            }
        }
    })

@app.route('/api/video-info', methods=['GET'])
def api_video_info():
    """Get YouTube video information"""
    try:
        url = request.args.get('url', '').strip()
        
        if not url or not is_valid_youtube_url(url):
            return jsonify({
                'status': 'error',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        # Get video info
        info_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_info = {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'description': info.get('description', '')[:500] + '...' if info.get('description', '') else '',
                'thumbnail': info.get('thumbnail', ''),
                'webpage_url': info.get('webpage_url', url)
            }
            
            return jsonify({
                'status': 'success',
                'data': video_info
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get video info: {str(e)}'
        }), 500

@app.route('/api/download', methods=['GET'])
def api_download():
    """API Download endpoint"""
    try:
        url = request.args.get('url', '').strip()
        
        # Support both 'format' and 'type' parameters for backward compatibility
        download_format = request.args.get('format', request.args.get('type', 'video')).lower()
        
        # Handle quality parameter - support both simplified and detailed formats
        quality_param = request.args.get('quality', '720p')
        audio_quality = request.args.get('audio_quality', '192')
        
        # Map simplified quality names to yt-dlp format strings
        quality_mapping = {
            # Video qualities
            '4k': 'best[height<=2160]/best',
            '2160p': 'best[height<=2160]/best',
            '1080p': 'best[height<=1080]/best',
            '720p': 'best[height<=720]/best',
            '480p': 'best[height<=480]/best',
            '360p': 'best[height<=360]/best',
            '240p': 'best[height<=240]/best',
            'worst': 'worst/bestvideo+bestaudio',
            'best': 'best/bestvideo+bestaudio'
        }
        
        # Audio quality mapping - extract just the number
        audio_quality_mapping = {
            '320kbps': '320',
            '256kbps': '256', 
            '192kbps': '192',
            '128kbps': '128',
            '96kbps': '96',
            '64kbps': '64',
            '320': '320',
            '256': '256',
            '192': '192', 
            '128': '128',
            '96': '96',
            '64': '64'
        }
        
        # Convert quality parameter
        if download_format == 'video':
            quality = quality_mapping.get(quality_param, quality_param)
            # Fallback to a working format if invalid
            if not any(x in quality for x in ['best', 'worst', 'height', 'bestvideo']):
                quality = 'best[height<=720]/bestvideo+bestaudio/best'
        else:
            # For audio, extract number from quality string and validate
            if quality_param.endswith('kbps'):
                audio_quality = audio_quality_mapping.get(quality_param, '192')
            else:
                audio_quality = audio_quality_mapping.get(quality_param, quality_param)
            
            # Ensure audio_quality is just a number
            if not audio_quality.isdigit():
                audio_quality = '192'  # Default fallback
            
            quality = 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best[acodec!=none]'
        
        # Validate parameters
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'URL parameter is required'
            }), 400
            
        if not is_valid_youtube_url(url):
            return jsonify({
                'status': 'error',
                'message': 'Please provide a valid YouTube URL'
            }), 400
            
        if download_format not in ['video', 'audio']:
            return jsonify({
                'status': 'error',
                'message': 'Format must be either "video" or "audio"'
            }), 400
        
        # Download content
        result = download_youtube_content(url, quality, download_format, audio_quality)
        
        if result['success']:
            file_path = result['file_path']
            temp_dir = result['temp_dir']
            
            # Send file for download
            def cleanup_file():
                time.sleep(60)  # Wait 60 seconds for API downloads
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    os.rmdir(temp_dir)
                except:
                    pass
            
            # Start cleanup in background
            cleanup_thread = threading.Thread(target=cleanup_file)
            cleanup_thread.daemon = True
            cleanup_thread.start()
            
            return send_file(
                file_path,
                as_attachment=True,
                download_name=result['filename']
            )
        else:
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/download-info', methods=['GET'])
def api_download_info():
    """Get download information without actually downloading"""
    try:
        url = request.args.get('url', '').strip()
        download_format = request.args.get('format', request.args.get('type', 'video')).lower()
        quality_param = request.args.get('quality', '720p')
        
        # Map quality for display
        quality_mapping = {
            '4k': '4K (2160p)', '2160p': '4K (2160p)',
            '1080p': '1080p Full HD', '720p': '720p HD',
            '480p': '480p Standard', '360p': '360p Mobile',
            '240p': '240p Low', 'best': 'Best Available', 'worst': 'Lowest Available'
        }
        
        audio_quality_mapping = {
            '320kbps': '320 kbps', '256kbps': '256 kbps', '192kbps': '192 kbps',
            '128kbps': '128 kbps', '96kbps': '96 kbps', '64kbps': '64 kbps'
        }
        
        if download_format == 'video':
            quality_display = quality_mapping.get(quality_param, quality_param)
        else:
            quality_display = audio_quality_mapping.get(quality_param, quality_param)
        
        if not url or not is_valid_youtube_url(url):
            return jsonify({
                'status': 'error',
                'message': 'Please provide a valid YouTube URL'
            }), 400
        
        # Get video info and available formats
        info_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            response_data = {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'requested_quality': quality_display,
                'requested_format': download_format,
                'estimated_filename': get_safe_filename(info.get('title', 'Unknown')) + ('_audio.mp3' if download_format == 'audio' else '_video.mp4')
            }
            
            return jsonify({
                'status': 'success',
                'data': response_data
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get download info: {str(e)}'
        }), 500

@app.route('/progress/<filename>')
def get_progress(filename):
    """Get download progress"""
    progress = download_progress.get(filename, {'percent': 0, 'status': 'waiting'})
    return jsonify(progress)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': ['/api/info', '/api/download', '/api/video-info', '/api/formats']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print(f"\n🚀 {PROJECT_INFO['name']} v{PROJECT_INFO['version']}")
    print(f"👨‍💻 Developer: {PROJECT_INFO['developer']}")
    print(f"📡 API Version: {PROJECT_INFO['api_version']}")
    print("🌐 Server starting on http://0.0.0.0:5000")
    print("\n📋 API Endpoints:")
    print("   • GET  /api/info - API information")
    print("   • GET  /api/formats - Available formats")
    print("   • GET  /api/video-info?url=<youtube_url> - Video information")
    print("   • GET  /api/download?url=<url>&type=<video|audio>&quality=<quality> - Download")
    print("   • GET  /api/download-info?url=<url>&type=<type>&quality=<quality> - Download info")
    print("\n💡 Example API Usage:")
    print("   Video: /api/download?url=https://youtu.be/VIDEO_ID&format=video&quality=720p")
    print("   Audio: /api/download?url=https://youtu.be/VIDEO_ID&format=audio&quality=192kbps")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
