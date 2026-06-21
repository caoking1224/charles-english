#!/usr/bin/env python3
"""
重新生成单词音频 — 高音量、清晰发音
区分英音/美音
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

# 单词列表
WORDS = [
    "come", "get", "give", "go", "keep", "let", "make", "put", "seem", "send",
    "take", "be", "do", "have", "say", "see", "may", "will", "about", "across",
    "account", "act", "addition", "adjustment", "advertisement", "agreement", "air", "amount", "amusement", "animal",
    "answer", "apparatus", "approval", "argument", "art", "attack", "attention", "authority", "back", "balance",
    "angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "banana",
    "band", "basin", "basket", "bath", "bed", "bee", "bell", "berry", "bird", "blade",
    "able", "acid", "angry", "automatic", "beautiful", "black", "blue", "boiling", "bright", "broken",
    "brown", "cheap", "chemical", "clean", "clear", "cold", "comfortable", "common", "complex", "conscious",
    "awake", "bad", "before", "begin", "bent", "best", "better", "bitter", "blow", "bone",
    "borrow", "bottom", "boy", "brother", "build", "burn", "burst", "business", "butter", "button",
]


def generate_audio(word, output_path, stability=0.4, similarity_boost=0.8):
    """用ElevenLabs生成音频，提高音量和清晰度"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    data = json.dumps({
        "text": word,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": 0.3,  # 增加表现力
            "use_speaker_boost": True  # 增加音量
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
    print("🎤 重新生成单词音频（高音量版）")
    print(f"   Voice ID: {VOICE_ID}")
    print(f"   单词数量: {len(WORDS)}")
    print("=" * 60)
    
    uk_dir = "/Users/charlescao/Hermes/english-vocab/audio/uk"
    us_dir = "/Users/charlescao/Hermes/english-vocab/audio/us"
    
    # 清除旧文件
    for f in os.listdir(uk_dir):
        os.remove(os.path.join(uk_dir, f))
    for f in os.listdir(us_dir):
        os.remove(os.path.join(us_dir, f))
    
    print("已清除旧音频文件")
    
    success = 0
    failed = 0
    
    for i, word in enumerate(WORDS, 1):
        # 英音（更正式、清晰）
        uk_path = os.path.join(uk_dir, f"{word}.mp3")
        try:
            size = generate_audio(word, uk_path, stability=0.5, similarity_boost=0.75)
            print(f"[{i}/{len(WORDS)}] ✓ {word} (UK) - {size} bytes")
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"[{i}/{len(WORDS)}] ✗ {word} (UK) - {e}")
            failed += 1
        
        # 美音（更自然、卷舌）
        us_path = os.path.join(us_dir, f"{word}.mp3")
        try:
            size = generate_audio(word, us_path, stability=0.4, similarity_boost=0.85)
            print(f"[{i}/{len(WORDS)}] ✓ {word} (US) - {size} bytes")
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"[{i}/{len(WORDS)}] ✗ {word} (US) - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成: {success} 成功, {failed} 失败")
    
    # 检查新文件大小
    uk_sizes = [os.path.getsize(os.path.join(uk_dir, f)) for f in os.listdir(uk_dir)[:5]]
    us_sizes = [os.path.getsize(os.path.join(us_dir, f)) for f in os.listdir(us_dir)[:5]]
    print(f"\\n新UK文件大小(前5): {uk_sizes}")
    print(f"新US文件大小(前5): {us_sizes}")
    print("=" * 60)


if __name__ == "__main__":
    main()
