#!/usr/bin/env python3
"""
从原始网站提取的数据生成完整HTML — 黑白设计风格
"""
import json

# 读取数据
with open('/Users/charlescao/Hermes/charles-english/words_data_v2.json') as f:
    data = json.load(f)

words = data['result']['data']
print(f"加载了 {len(words)} 个单词")

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Charles English · </title>
    <style>
        /* ========== CSS变量 — 黑白风格 ========== */
        :root {
            --bg-primary: #FFFFFF;
            --bg-secondary: #F5F5F5;
            --bg-card: #FFFFFF;
            --text-primary: #111111;
            --text-secondary: #444444;
            --text-muted: #888888;
            --border-color: #222222;
            --border-light: #DDDDDD;
            --accent: #000000;
            --accent-light: #333333;
            --accent-bg: #F0F0F0;
            --shadow: rgba(0, 0, 0, 0.1);
            --shadow-hover: rgba(0, 0, 0, 0.2);
            --tag-operations: #E0E0E0;
            --tag-general: #D0D0D0;
            --tag-picturable: #C0C0C0;
            --tag-qualities: #B0B0B0;
            --tag-opposites: #A0A0A0;
            --overlay: rgba(0, 0, 0, 0.8);
            --uk-color: #000000;
            --us-color: #666666;
        }

        [data-theme="dark"] {
            --bg-primary: #0A0A0A;
            --bg-secondary: #151515;
            --bg-card: #1A1A1A;
            --text-primary: #F0F0F0;
            --text-secondary: #CCCCCC;
            --text-muted: #888888;
            --border-color: #FFFFFF;
            --border-light: #333333;
            --accent: #FFFFFF;
            --accent-light: #DDDDDD;
            --accent-bg: #222222;
            --shadow: rgba(255, 255, 255, 0.05);
            --shadow-hover: rgba(255, 255, 255, 0.1);
            --tag-operations: #2A2A2A;
            --tag-general: #252525;
            --tag-picturable: #202020;
            --tag-qualities: #1A1A1A;
            --tag-opposites: #151515;
            --overlay: rgba(0, 0, 0, 0.9);
            --uk-color: #FFFFFF;
            --us-color: #999999;
        }

        /* ========== 基础样式 ========== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        /* ========== 头部 ========== */
        .header {
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .logo h1 {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        .logo .subtitle {
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }

        /* ========== 搜索框 ========== */
        .search-box {
            flex: 1;
            min-width: 200px;
            max-width: 400px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 0.6rem 1rem 0.6rem 2.5rem;
            border: 1px solid var(--border-light);
            border-radius: 8px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .search-box input:focus {
            outline: none;
            border-color: var(--accent);
        }

        .search-box::before {
            content: "⌕";
            position: absolute;
            left: 0.8rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1rem;
            color: var(--text-muted);
        }

        .search-box .shortcut {
            position: absolute;
            right: 0.5rem;
            top: 50%;
            transform: translateY(-50%);
            background: var(--bg-primary);
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 0.1rem 0.4rem;
            font-size: 0.7rem;
            color: var(--text-muted);
        }

        /* ========== 工具栏 ========== */
        .toolbar {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .toolbar-group {
            display: flex;
            align-items: center;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            overflow: hidden;
        }

        .toolbar-btn {
            padding: 0.4rem 0.8rem;
            border: none;
            background: var(--bg-primary);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.15s;
            white-space: nowrap;
        }

        .toolbar-btn:hover {
            background: var(--accent-bg);
        }

        .toolbar-btn.active {
            background: var(--accent);
            color: var(--bg-primary);
        }

        /* ========== 发音切换 ========== */
        .accent-toggle {
            display: flex;
            align-items: center;
            gap: 0;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            overflow: hidden;
        }

        .accent-btn {
            padding: 0.5rem 1rem;
            border: none;
            background: var(--bg-primary);
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.15s;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .accent-btn.uk {
            color: var(--text-muted);
        }

        .accent-btn.us {
            color: var(--text-muted);
        }

        .accent-btn.active.uk {
            background: var(--uk-color);
            color: var(--bg-primary);
        }

        .accent-btn.active.us {
            background: var(--us-color);
            color: var(--bg-primary);
        }

        .accent-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }

        .accent-dot.uk { background: #000; }
        .accent-dot.us { background: #666; }

        [data-theme="dark"] .accent-dot.uk { background: #fff; }
        [data-theme="dark"] .accent-dot.us { background: #999; }

        /* ========== 分类导航 ========== */
        .categories {
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-light);
            padding: 1rem 2rem;
        }

        .categories-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            align-items: center;
        }

        .cat-btn {
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-light);
            border-radius: 20px;
            background: var(--bg-primary);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.15s;
            white-space: nowrap;
        }

        .cat-btn:hover {
            border-color: var(--accent);
        }

        .cat-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            color: var(--bg-primary);
        }

        .cat-btn .count {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-left: 0.25rem;
        }

        /* ========== 主内容区 ========== */
        .main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .section-subtitle {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        .section-count {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        /* ========== 单词网格 ========== */
        .words-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        /* ========== 单词卡片 ========== */
        .word-card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 10px;
            padding: 1.2rem;
            transition: all 0.15s;
        }

        .word-card:hover {
            box-shadow: 0 2px 12px var(--shadow-hover);
        }

        .word-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.6rem;
        }

        .word-main {
            flex: 1;
        }

        .word-text {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        .word-phonetic {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-family: "SF Mono", "Fira Code", monospace;
            margin-top: 0.15rem;
        }

        .word-tag {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .tag-OP { background: var(--tag-operations); color: #333; }
        .tag-GT { background: var(--tag-general); color: #333; }
        .tag-PT { background: var(--tag-picturable); color: #333; }
        .tag-QG { background: var(--tag-qualities); color: #333; }
        .tag-OPP { background: var(--tag-opposites); color: #333; }

        [data-theme="dark"] .tag-OP,
        [data-theme="dark"] .tag-GT,
        [data-theme="dark"] .tag-PT,
        [data-theme="dark"] .tag-QG,
        [data-theme="dark"] .tag-OPP { color: #CCC; }

        .speak-btn {
            background: none;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.3rem 0.6rem;
            cursor: pointer;
            font-size: 0.75rem;
            color: var(--text-muted);
            transition: all 0.15s;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        .speak-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .speak-btn .accent-indicator {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }

        .speak-btn .accent-indicator.uk { background: #000; }
        .speak-btn .accent-indicator.us { background: #666; }

        [data-theme="dark"] .speak-btn .accent-indicator.uk { background: #fff; }
        [data-theme="dark"] .speak-btn .accent-indicator.us { background: #999; }

        /* ========== 中文释义 ========== */
        .word-zh {
            font-size: 1.05rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .word-explain {
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-bottom: 0.6rem;
            line-height: 1.5;
        }

        /* ========== 英文释义 ========== */
        .definition-label {
            font-size: 0.65rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.2rem;
            font-weight: 600;
        }

        .word-en {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.6rem;
            font-style: italic;
        }

        /* ========== 例句 ========== */
        .example-box {
            background: var(--accent-bg);
            border-left: 2px solid var(--accent);
            padding: 0.5rem 0.8rem;
            border-radius: 0 6px 6px 0;
            margin-bottom: 0.6rem;
        }

        .example-en {
            font-size: 0.82rem;
            color: var(--text-primary);
            margin-bottom: 0.15rem;
        }

        .example-zh {
            font-size: 0.78rem;
            color: var(--text-muted);
        }

        .example-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.3rem;
        }

        .example-label {
            font-size: 0.65rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        .example-speak-btn {
            background: none;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            padding: 0.15rem 0.4rem;
            cursor: pointer;
            font-size: 0.65rem;
            color: var(--text-muted);
            transition: all 0.15s;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        .example-speak-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* ========== 近义词 ========== */
        .synonyms {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
        }

        .synonym-tag {
            padding: 0.2rem 0.6rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            font-size: 0.72rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s;
        }

        .synonym-tag:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* ========== 卡片练习 ========== */
        .flashcard-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--overlay);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .flashcard-overlay.active {
            display: flex;
        }

        .flashcard {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 3rem;
            max-width: 500px;
            width: 90%;
            text-align: center;
            position: relative;
        }

        .flashcard-word {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .flashcard-phonetic {
            font-size: 1rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-family: "SF Mono", monospace;
        }

        .flashcard-accent {
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            margin-bottom: 1rem;
            display: inline-block;
        }

        .flashcard-accent.uk {
            background: #000;
            color: #fff;
        }

        .flashcard-accent.us {
            background: #666;
            color: #fff;
        }

        [data-theme="dark"] .flashcard-accent.uk {
            background: #fff;
            color: #000;
        }

        [data-theme="dark"] .flashcard-accent.us {
            background: #999;
            color: #000;
        }

        .flashcard-speak {
            background: none;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.4rem 1rem;
            cursor: pointer;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            transition: all 0.15s;
        }

        .flashcard-speak:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .flashcard-hint {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            cursor: pointer;
        }

        .flashcard-answer {
            display: none;
            text-align: left;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-light);
        }

        .flashcard-answer.show {
            display: block;
        }

        .flashcard-zh {
            font-size: 1.2rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .flashcard-en {
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-style: italic;
        }

        .flashcard-controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }

        .flashcard-btn {
            padding: 0.6rem 1.2rem;
            border: 1px solid var(--border-light);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.15s;
        }

        .flashcard-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .flashcard-close {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-muted);
        }

        /* ========== Toast ========== */
        .toast {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--accent);
            color: var(--bg-primary);
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-size: 0.9rem;
            z-index: 2000;
            transition: transform 0.3s ease;
            pointer-events: none;
        }

        .toast.show {
            transform: translateX(-50%) translateY(0);
        }

        /* ========== 页脚 ========== */
        .footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.75rem;
            border-top: 1px solid var(--border-light);
            margin-top: 2rem;
        }

        .shortcuts {
            margin-top: 0.5rem;
        }

        .shortcuts kbd {
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 3px;
            padding: 0.1rem 0.4rem;
            font-family: monospace;
            font-size: 0.7rem;
        }

        /* ========== 响应式 ========== */
        @media (max-width: 768px) {
            .header { padding: 1rem; }
            .header-content { gap: 1rem; }
            .search-box { max-width: 100%; order: 3; width: 100%; }
            .categories { padding: 0.8rem 1rem; }
            .main { padding: 1rem; }
            .words-grid { grid-template-columns: 1fr; }
            .flashcard { padding: 2rem; }
            .flashcard-word { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <h1>Charles English</h1>
                <div class="subtitle"></div>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索单词、释义或例句...">
                <span class="shortcut">/</span>
            </div>
            <div class="toolbar">
                <div class="accent-toggle">
                    <button class="accent-btn uk active" id="btnUK" onclick="setAccent('uk')">
                        <span class="accent-dot uk"></span> UK
                    </button>
                    <button class="accent-btn us" id="btnUS" onclick="setAccent('us')">
                        <span class="accent-dot us"></span> US
                    </button>
                </div>
                <div class="toolbar-group">
                    <button class="toolbar-btn" id="btnLight" onclick="setTheme('light')">Light</button>
                    <button class="toolbar-btn active" id="btnDark" onclick="setTheme('dark')">Dark</button>
                </div>
                <div class="toolbar-group">
                    <button class="toolbar-btn active" id="btnSimplified" onclick="setChinese('simplified')">简</button>
                    <button class="toolbar-btn" id="btnTraditional" onclick="setChinese('traditional')">繁</button>
                </div>
                <button class="toolbar-btn" onclick="openFlashcard()">卡片练习</button>
            </div>
        </div>
    </header>

    <nav class="categories">
        <div class="categories-content">
            <button class="cat-btn active" data-cat="all" onclick="filterCategory('all')">All <span class="count">850</span></button>
            <button class="cat-btn" data-cat="OP" onclick="filterCategory('OP')">Operations <span class="count">100</span></button>
            <button class="cat-btn" data-cat="GT" onclick="filterCategory('GT')">General Things <span class="count">400</span></button>
            <button class="cat-btn" data-cat="PT" onclick="filterCategory('PT')">Picturable <span class="count">200</span></button>
            <button class="cat-btn" data-cat="QG" onclick="filterCategory('QG')">Qualities <span class="count">100</span></button>
            <button class="cat-btn" data-cat="OPP" onclick="filterCategory('OPP')">Opposites <span class="count">50</span></button>
        </div>
    </nav>

    <main class="main" id="mainContent"></main>

    <div class="flashcard-overlay" id="flashcardOverlay">
        <div class="flashcard">
            <button class="flashcard-close" onclick="closeFlashcard()">×</button>
            <div class="flashcard-word" id="flashcardWord"></div>
            <div class="flashcard-phonetic" id="flashcardPhonetic"></div>
            <div class="flashcard-accent" id="flashcardAccent"></div>
            <button class="flashcard-speak" onclick="speakCurrentWord()">🔊 再听一次</button>
            <div class="flashcard-hint" onclick="toggleFlashcardAnswer()">点击翻牌</div>
            <div class="flashcard-answer" id="flashcardAnswer">
                <div class="flashcard-zh" id="flashcardZh"></div>
                <div class="flashcard-en" id="flashcardEn"></div>
            </div>
            <div class="flashcard-controls">
                <button class="flashcard-btn" onclick="prevCard()">← 上一个</button>
                <button class="flashcard-btn" onclick="randomCard()">随机</button>
                <button class="flashcard-btn" onclick="nextCard()">下一个 →</button>
            </div>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <footer class="footer">
        <p>基于 Charles English · 仅供学习使用</p>
        <div class="shortcuts">
            <kbd>/</kbd> 搜索 · <kbd>Esc</kbd> 关闭 · <kbd>Space</kbd> 翻牌
        </div>
    </footer>

    <script>
        const WORDS = ''' + json.dumps(words, ensure_ascii=False) + ''';

        const state = {
            currentCategory: 'all',
            isUKAccent: true,
            isDarkMode: true,
            isSimplified: true,
            searchQuery: '',
            flashcardIndex: 0
        };

        const categoryNames = {
            'OP': { zh: '操作词', en: 'Operations', desc: '' },
            'GT': { zh: '通用词', en: 'General Things', desc: '' },
            'PT': { zh: '图示词', en: 'Picturable', desc: '' },
            'QG': { zh: '性质词', en: 'Qualities', desc: '' },
            'OPP': { zh: '反义对', en: 'Opposites', desc: '' }
        };

        document.addEventListener('DOMContentLoaded', () => {
            loadSettings();
            renderWords();
            setupEventListeners();
        });

        function loadSettings() {
            state.isDarkMode = localStorage.getItem('theme') !== 'light';
            state.isUKAccent = localStorage.getItem('accent') !== 'us';
            state.isSimplified = localStorage.getItem('chinese') !== 'traditional';
            
            document.documentElement.setAttribute('data-theme', state.isDarkMode ? 'dark' : '');
            updateButtons();
        }

        function updateButtons() {
            document.getElementById('btnUK').classList.toggle('active', state.isUKAccent);
            document.getElementById('btnUS').classList.toggle('active', !state.isUKAccent);
            document.getElementById('btnLight').classList.toggle('active', !state.isDarkMode);
            document.getElementById('btnDark').classList.toggle('active', state.isDarkMode);
            document.getElementById('btnSimplified').classList.toggle('active', state.isSimplified);
            document.getElementById('btnTraditional').classList.toggle('active', !state.isSimplified);
        }

        function setupEventListeners() {
            document.getElementById('searchInput').addEventListener('input', (e) => {
                state.searchQuery = e.target.value.toLowerCase();
                renderWords();
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
                    e.preventDefault();
                    document.getElementById('searchInput').focus();
                }
                if (e.key === 'Escape') {
                    document.getElementById('searchInput').blur();
                    closeFlashcard();
                }
                if (e.key === ' ' && document.getElementById('flashcardOverlay').classList.contains('active')) {
                    e.preventDefault();
                    toggleFlashcardAnswer();
                }
            });
        }

        function renderWords() {
            const main = document.getElementById('mainContent');
            let filtered = getFilteredWords();
            
            const groups = {};
            filtered.forEach(w => {
                if (!groups[w.category]) groups[w.category] = [];
                groups[w.category].push(w);
            });

            let html = '';
            
            if (state.currentCategory === 'all') {
                for (const [cat, words] of Object.entries(groups)) {
                    html += renderCategorySection(cat, words);
                }
            } else {
                const words = groups[state.currentCategory] || [];
                html += renderCategorySection(state.currentCategory, words);
            }

            if (!html) {
                html = '<div style="text-align:center;padding:3rem;color:var(--text-muted);">没有找到匹配的单词</div>';
            }

            main.innerHTML = html;
        }

        function renderCategorySection(cat, words) {
            const info = categoryNames[cat] || { zh: cat, en: cat, desc: '' };
            
            let html = `
                <div class="section-header">
                    <div>
                        <div class="section-title">${info.en}</div>
                        <div class="section-subtitle">${info.zh} · ${info.desc}</div>
                    </div>
                    <div class="section-count">${words.length} WORDS</div>
                </div>
                <div class="words-grid">
            `;

            words.forEach(w => {
                html += renderWordCard(w);
            });

            html += '</div>';
            return html;
        }

        function renderWordCard(w) {
            const tagClass = w.category;
            const zh = state.isSimplified ? w.zh : (w.zhTw || w.zh);
            const explain = state.isSimplified ? w.zhExplain : (w.zhExplainTw || w.zhExplain);
            const exampleZh = state.isSimplified ? w.exampleZh : (w.exampleZhTw || w.exampleZh);
            const accentLabel = state.isUKAccent ? 'UK' : 'US';
            
            return `
                <article class="word-card">
                    <div class="word-header">
                        <div class="word-main">
                            <div class="word-text">${w.word}</div>
                            <div class="word-phonetic">${w.phonetic || ''}</div>
                        </div>
                        <span class="word-tag tag-${tagClass}">${w.category}</span>
                        <button class="speak-btn" onclick="speakWord('${w.word}')">
                            <span class="accent-indicator ${state.isUKAccent ? 'uk' : 'us'}"></span>
                            ${accentLabel}
                        </button>
                    </div>
                    <div class="word-zh">${zh}</div>
                    <div class="word-explain">${explain}</div>
                    <div class="definition-label">Definition</div>
                    <div class="word-en">${w.en}</div>
                    <div class="example-box">
                        <div class="example-header">
                            <span class="example-label">Example</span>
                            <button class="example-speak-btn" onclick="speakExample('${w.word}')">
                                <span class="accent-indicator ${state.isUKAccent ? 'uk' : 'us'}"></span>
                                朗读例句
                            </button>
                        </div>
                        <div class="example-en">${w.example}</div>
                        <div class="example-zh">${exampleZh}</div>
                    </div>
                    <div class="synonyms">
                        ${(w.synonyms || []).map(s => `<span class="synonym-tag" onclick="searchWord('${s}')">${s}</span>`).join('')}
                    </div>
                </article>
            `;
        }

        function getFilteredWords() {
            let words = [...WORDS];
            
            if (state.currentCategory !== 'all') {
                words = words.filter(w => w.category === state.currentCategory);
            }
            
            if (state.searchQuery) {
                words = words.filter(w => 
                    w.word.toLowerCase().includes(state.searchQuery) ||
                    (w.zh && w.zh.includes(state.searchQuery)) ||
                    (w.zhExplain && w.zhExplain.includes(state.searchQuery)) ||
                    (w.en && w.en.toLowerCase().includes(state.searchQuery)) ||
                    (w.example && w.example.toLowerCase().includes(state.searchQuery))
                );
            }
            
            return words;
        }

        function speakWord(word) {
            const accent = state.isUKAccent ? 'uk' : 'us';
            const audioPath = `audio/${accent}/${word}.mp3`;
            
            const audio = new Audio(audioPath);
            audio.play().catch(() => {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(word);
                    utterance.lang = state.isUKAccent ? 'en-GB' : 'en-US';
                    utterance.rate = 0.85;
                    window.speechSynthesis.speak(utterance);
                }
            });
        }

        function speakExample(word) {
            const audioPath = `audio/examples/${word}.mp3`;
            
            const audio = new Audio(audioPath);
            audio.play().catch(() => {
                showToast('例句音频不存在');
            });
        }

        function speakCurrentWord() {
            const w = WORDS[state.flashcardIndex];
            speakWord(w.word);
        }

        function filterCategory(cat) {
            state.currentCategory = cat;
            
            document.querySelectorAll('.cat-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.cat === cat);
            });
            
            renderWords();
        }

        function setAccent(accent) {
            state.isUKAccent = accent === 'uk';
            localStorage.setItem('accent', accent);
            updateButtons();
            renderWords();
            showToast(accent === 'uk' ? '🇬🇧 英式发音' : '🇺🇸 美式发音');
        }

        function setTheme(theme) {
            state.isDarkMode = theme === 'dark';
            document.documentElement.setAttribute('data-theme', state.isDarkMode ? 'dark' : '');
            localStorage.setItem('theme', theme);
            updateButtons();
        }

        function setChinese(type) {
            state.isSimplified = type === 'simplified';
            localStorage.setItem('chinese', type);
            updateButtons();
            renderWords();
        }

        function searchWord(word) {
            document.getElementById('searchInput').value = word;
            state.searchQuery = word.toLowerCase();
            renderWords();
        }

        function openFlashcard() {
            state.flashcardIndex = Math.floor(Math.random() * WORDS.length);
            updateFlashcard();
            document.getElementById('flashcardOverlay').classList.add('active');
        }

        function closeFlashcard() {
            document.getElementById('flashcardOverlay').classList.remove('active');
        }

        function toggleFlashcardAnswer() {
            document.getElementById('flashcardAnswer').classList.toggle('show');
        }

        function updateFlashcard() {
            const w = WORDS[state.flashcardIndex];
            document.getElementById('flashcardWord').textContent = w.word;
            document.getElementById('flashcardPhonetic').textContent = w.phonetic || '';
            
            const accentEl = document.getElementById('flashcardAccent');
            accentEl.textContent = state.isUKAccent ? '🇬🇧 UK' : '🇺🇸 US';
            accentEl.className = 'flashcard-accent ' + (state.isUKAccent ? 'uk' : 'us');
            
            document.getElementById('flashcardZh').textContent = w.zh;
            document.getElementById('flashcardEn').textContent = w.en;
            document.getElementById('flashcardAnswer').classList.remove('show');
            
            // 自动播放单词发音
            speakWord(w.word);
        }

        function prevCard() {
            state.flashcardIndex = (state.flashcardIndex - 1 + WORDS.length) % WORDS.length;
            updateFlashcard();
        }

        function nextCard() {
            state.flashcardIndex = (state.flashcardIndex + 1) % WORDS.length;
            updateFlashcard();
        }

        function randomCard() {
            state.flashcardIndex = Math.floor(Math.random() * WORDS.length);
            updateFlashcard();
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 1500);
        }
    </script>
</body>
</html>'''

output_path = '/Users/charlescao/Hermes/charles-english/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 已生成: {output_path}")
print(f"   单词数量: {len(words)}")
