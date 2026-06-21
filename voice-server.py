#!/usr/bin/env python3
"""
本地语音服务器 — 用ElevenLabs克隆声音朗读英语单词
端口: 8765
"""
import os
import json
import http.server
import urllib.request

# 加载 .env
def load_env(path):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:]
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env(os.path.expanduser("~/Hermes/voice-translator/.env"))

# 代理设置
os.environ.setdefault("HTTPS_PROXY", "socks5h://127.0.0.1:7897")
os.environ.setdefault("HTTP_PROXY", "socks5h://127.0.0.1:7897")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")


class SpeechHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 健康检查
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "voice_id": VOICE_ID}).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        if self.path == "/speak":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            text = data.get("text", "")
            
            if not text:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "no text"}')
                return
            
            try:
                # 调用ElevenLabs API
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
                req_data = json.dumps({
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }).encode()
                
                req = urllib.request.Request(url, data=req_data, headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                })
                
                with urllib.request.urlopen(req, timeout=30) as resp:
                    audio_data = resp.read()
                
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(audio_data)))
                self.end_headers()
                self.wfile.write(audio_data)
                
            except Exception as e:
                print(f"ElevenLabs error: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        # CORS预检
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[语音服务器] {args[0]}")


def main():
    server = http.server.HTTPServer(("127.0.0.1", 8765), SpeechHandler)
    print("=" * 50)
    print("🎤 语音服务器启动")
    print(f"   地址: http://127.0.0.1:8765")
    print(f"   Voice ID: {VOICE_ID}")
    print(f"   API Key: {ELEVENLABS_API_KEY[:10]}...")
    print("=" * 50)
    server.serve_forever()


if __name__ == "__main__":
    main()
