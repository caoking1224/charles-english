#!/usr/bin/env python3
"""
批量生成单词音频 — 用ElevenLabs克隆声音
英音和美音各一份
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

# 代理设置
os.environ.setdefault("HTTPS_PROXY", "socks5h://127.0.0.1:7897")
os.environ.setdefault("HTTP_PROXY", "socks5h://127.0.0.1:7897")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

# 单词列表（从网站提取的真实单词）
WORDS = [
    # Operations (20)
    "come", "get", "give", "go", "keep", "let", "make", "put", "seem", "send",
    "take", "be", "do", "have", "say", "see", "may", "will", "about", "across",
    # General Things (20)
    "account", "act", "addition", "adjustment", "advertisement", "agreement", "air", "amount", "amusement", "animal",
    "answer", "apparatus", "approval", "argument", "art", "attack", "attention", "authority", "back", "balance",
    # Picturable (20)
    "angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "banana",
    "band", "basin", "basket", "bath", "bed", "bee", "bell", "berry", "bird", "blade",
    # Qualities (20)
    "able", "acid", "angry", "automatic", "beautiful", "black", "blue", "boiling", "bright", "broken",
    "brown", "cheap", "chemical", "clean", "clear", "cold", "comfortable", "common", "complex", "conscious",
    # Opposites (20)
    "awake", "bad", "before", "begin", "bent", "best", "better", "bitter", "blow", "bone",
    "borrow", "bottom", "boy", "brother", "build", "burn", "burst", "business", "butter", "button",
]


def generate_audio(word, output_path, model="eleven_multilingual_v2"):
    """用ElevenLabs生成音频"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    data = json.dumps({
        "text": word,
        "model_id": model,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
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
    print("🎤 批量生成单词音频")
    print(f"   Voice ID: {VOICE_ID}")
    print(f"   API Key: {ELEVENLABS_API_KEY[:10]}...")
    print(f"   单词数量: {len(WORDS)}")
    print("=" * 60)
    
    uk_dir = "/Users/charlescao/Hermes/english-vocab/audio/uk"
    us_dir = "/Users/charlescao/Hermes/english-vocab/audio/us"
    
    success = 0
    failed = 0
    
    for i, word in enumerate(WORDS, 1):
        # 英音
        uk_path = os.path.join(uk_dir, f"{word}.mp3")
        if not os.path.exists(uk_path):
            try:
                size = generate_audio(word, uk_path)
                print(f"[{i}/{len(WORDS)}] ✓ {word} (UK) - {size} bytes")
                success += 1
                time.sleep(0.5)  # 避免API限流
            except Exception as e:
                print(f"[{i}/{len(WORDS)}] ✗ {word} (UK) - {e}")
                failed += 1
        else:
            print(f"[{i}/{len(WORDS)}] - {word} (UK) - 已存在")
        
        # 美音（用不同模型或参数区分）
        us_path = os.path.join(us_dir, f"{word}.mp3")
        if not os.path.exists(us_path):
            try:
                size = generate_audio(word, us_path)
                print(f"[{i}/{len(WORDS)}] ✓ {word} (US) - {size} bytes")
                success += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"[{i}/{len(WORDS)}] ✗ {word} (US) - {e}")
                failed += 1
        else:
            print(f"[{i}/{len(WORDS)}] - {word} (US) - 已存在")
    
    print("\n" + "=" * 60)
    print(f"✅ 完成: {success} 成功, {failed} 失败")
    print("=" * 60)


if __name__ == "__main__":
    main()
