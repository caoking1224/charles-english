#!/usr/bin/env python3
"""
生成例句音频 — 用ElevenLabs克隆声音
"""
import os
import sys
import json
import time
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

os.environ.setdefault("HTTPS_PROXY", "socks5h://127.0.0.1:7897")
os.environ.setdefault("HTTP_PROXY", "socks5h://127.0.0.1:7897")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

# 读取单词数据
with open('/Users/charlescao/Hermes/english-vocab/words_data_v2.json') as f:
    data = json.load(f)
words = data['result']['data']


def generate_audio(text, output_path):
    """用ElevenLabs生成音频"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    data = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    })
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        audio_data = resp.read()
    
    with open(output_path, "wb") as f:
        f.write(audio_data)
    
    return len(audio_data)


def main():
    print("=" * 60)
    print("🎤 生成例句音频")
    print(f"   Voice ID: {VOICE_ID}")
    print(f"   例句数量: {len(words)}")
    print("=" * 60)
    
    # 创建目录
    examples_dir = "/Users/charlescao/Hermes/english-vocab/audio/examples"
    os.makedirs(examples_dir, exist_ok=True)
    
    success = 0
    failed = 0
    
    for i, w in enumerate(words, 1):
        word = w['word']
        example = w.get('example', '')
        
        if not example:
            print(f"[{i}/{len(words)}] - {word} - 无例句")
            continue
        
        # 文件名用单词名
        output_path = os.path.join(examples_dir, f"{word}.mp3")
        
        # 跳过已存在的文件
        if os.path.exists(output_path):
            print(f"[{i}/{len(words)}] - {word} - 已存在")
            continue
        
        try:
            size = generate_audio(example, output_path)
            print(f"[{i}/{len(words)}] ✓ {word} - {size} bytes")
            print(f"   例句: {example}")
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"[{i}/{len(words)}] ✗ {word} - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成: {success} 成功, {failed} 失败")
    print(f"   目录: {examples_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
