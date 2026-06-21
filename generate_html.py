#!/usr/bin/env python3
"""
从原始网站提取的数据生成完整HTML
"""
import json

# 读取数据
with open('/Users/charlescao/Hermes/english-vocab/words_data_v2.json') as f:
    data = json.load(f)

words = data['result']['data']
print(f"加载了 {len(words)} 个单词")

# 分类统计
categories = {}
for w in words:
    cat = w['category']
    categories[cat] = categories.get(cat, 0) + 1

print("分类统计:")
for cat, count in categories.items():
    print(f"  {cat}: {count}")

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ogden's Basic English · 850 词学习手册</title>
    <style>
        /* ========== CSS变量 ========== */
        :root {
            --bg-primary: #FFFEF5;
            --bg-secondary: #F5F0E6;
            --bg-card: #FFFEF5;
            --text-primary: #3D3226;
            --text-secondary: #6B5B4B;
            --text-muted: #9B8B7B;
            --border-color: #8B7355;
            --border-light: #C4B5A0;
            --accent: #B8860B;
            --accent-light: #DAA520;
            --accent-bg: #FFF8DC;
            --shadow: rgba(139, 115, 85, 0.15);
            --shadow-hover: rgba(139, 115, 85, 0.3);
            --tag-operations: #E8D5B7;
            --tag-general: #D4E6B5;
            --tag-picturable: #B5D4E6;
            --tag-qualities: #E6B5D4;
            --tag-opposites: #E6D4B5;
            --overlay: rgba(61, 50, 38, 0.6);
            --success: #5B8C5A;
            --info: #5A7C8C;
        }

        [data-theme="dark"] {
            --bg-primary: #1A1610;
            --bg-secondary: #2A2418;
            --bg-card: #2A2418;
            --text-primary: #E8DCC8;
            --text-secondary: #C4B5A0;
            --text-muted: #8B7B6B;
            --border-color: #6B5B4B;
            --border-light: #4A3D30;
            --accent: #DAA520;
            --accent-light: #FFD700;
            --accent-bg: #3D3226;
            --shadow: rgba(0, 0, 0, 0.3);
            --shadow-hover: rgba(0, 0, 0, 0.5);
            --tag-operations: #4A3D2E;
            --tag-general: #2E4A2E;
            --tag-picturable: #2E3D4A;
            --tag-qualities: #4A2E3D;
            --tag-opposites: #4A4A2E;
            --overlay: rgba(0, 0, 0, 0.7);
        }

        /* ========== 基础样式 ========== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        /* ========== 头部 ========== */
        .header {
            background: var(--bg-secondary);
            border-bottom: 2px solid var(--border-color);
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

        .logo {
            flex-shrink: 0;
        }

        .logo h1 {
            font-size: 1.5rem;
            color: var(--accent);
            font-weight: 700;
        }

        .logo .subtitle {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
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
            border: 2px solid var(--border-light);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-primary);
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .search-box input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-bg);
        }

        .search-box::before {
            content: "🔍";
            position: absolute;
            left: 0.8rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.9rem;
        }

        .search-box .shortcut {
            position: absolute;
            right: 0.5rem;
            top: 50%;
            transform: translateY(-50%);
            background: var(--bg-secondary);
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
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .toolbar-group {
            display: flex;
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 6px;
            overflow: hidden;
        }

        .toolbar-btn {
            padding: 0.4rem 0.8rem;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .toolbar-btn:hover {
            background: var(--accent-bg);
            color: var(--accent);
        }

        .toolbar-btn.active {
            background: var(--accent);
            color: white;
        }

        .toolbar-divider {
            width: 1px;
            height: 24px;
            background: var(--border-light);
            margin: 0 0.25rem;
        }

        /* ========== 分类导航 ========== */
        .categories {
            background: var(--bg-secondary);
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
            border: 2px solid var(--border-light);
            border-radius: 20px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .cat-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        .cat-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }

        .cat-btn .count {
            font-size: 0.75rem;
            opacity: 0.8;
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
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-color);
        }

        .section-title {
            font-size: 1.3rem;
            color: var(--text-primary);
            font-weight: 700;
        }

        .section-subtitle {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .section-count {
            font-size: 0.85rem;
            color: var(--text-muted);
            background: var(--bg-secondary);
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
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
            padding: 1rem;
            transition: all 0.2s;
            position: relative;
        }

        .word-card:hover {
            box-shadow: 0 4px 12px var(--shadow-hover);
            transform: translateY(-2px);
        }

        .word-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .word-main {
            flex: 1;
        }

        .word-text {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.2;
        }

        .word-phonetic {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-family: "Lucida Console", "Courier New", monospace;
            margin-top: 0.2rem;
        }

        .word-tag {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .tag-OP { background: var(--tag-operations); color: #8B6914; }
        .tag-GT { background: var(--tag-general); color: #2E7D32; }
        .tag-PT { background: var(--tag-picturable); color: #1565C0; }
        .tag-QG { background: var(--tag-qualities); color: #7B1FA2; }
        .tag-OPP { background: var(--tag-opposites); color: #E65100; }

        .speak-btn {
            background: none;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            padding: 0.3rem 0.5rem;
            cursor: pointer;
            font-size: 0.8rem;
            color: var(--text-muted);
            transition: all 0.2s;
            flex-shrink: 0;
        }

        .speak-btn:hover {
            background: var(--accent-bg);
            color: var(--accent);
            border-color: var(--accent);
        }

        /* ========== 中文释义 ========== */
        .word-zh {
            font-size: 1rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 0.3rem;
        }

        .word-explain {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }

        /* ========== 英文释义 ========== */
        .definition-label {
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.2rem;
        }

        .word-en {
            font-size: 0.85rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            font-style: italic;
        }

        /* ========== 例句 ========== */
        .example-box {
            background: var(--accent-bg);
            border-left: 3px solid var(--accent);
            padding: 0.5rem 0.8rem;
            border-radius: 0 6px 6px 0;
            margin-bottom: 0.5rem;
        }

        .example-en {
            font-size: 0.85rem;
            color: var(--text-primary);
            margin-bottom: 0.2rem;
        }

        .example-zh {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        /* ========== 近义词 ========== */
        .synonyms {
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }

        .synonym-tag {
            padding: 0.2rem 0.6rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }

        .synonym-tag:hover {
            background: var(--accent-bg);
            color: var(--accent);
            border-color: var(--accent);
        }

        /* ========== 分页 ========== */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            padding: 2rem 0;
        }

        .page-btn {
            padding: 0.5rem 1rem;
            border: 1px solid var(--border-light);
            border-radius: 6px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }

        .page-btn:hover:not(:disabled) {
            background: var(--accent-bg);
            color: var(--accent);
            border-color: var(--accent);
        }

        .page-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        .page-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* ========== 统计信息 ========== */
        .stats-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.5rem 0;
        }

        .stats-info {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        .sort-btn {
            padding: 0.3rem 0.8rem;
            border: 1px solid var(--border-light);
            border-radius: 4px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.8rem;
        }

        /* ========== 卡片练习模式 ========== */
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
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 3rem;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .flashcard-word {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .flashcard-phonetic {
            font-size: 1.1rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }

        .flashcard-hint {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
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
            font-size: 1.3rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .flashcard-en {
            font-size: 0.95rem;
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
            padding: 0.6rem 1.5rem;
            border: 2px solid var(--border-light);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .flashcard-btn:hover {
            background: var(--accent-bg);
            color: var(--accent);
            border-color: var(--accent);
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

        /* ========== Toast提示 ========== */
        .toast {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--text-primary);
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
            font-size: 0.8rem;
            border-top: 1px solid var(--border-light);
            margin-top: 2rem;
        }

        .footer a {
            color: var(--accent);
            text-decoration: none;
        }

        .shortcuts {
            margin-top: 0.5rem;
            font-size: 0.75rem;
        }

        .shortcuts kbd {
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 3px;
            padding: 0.1rem 0.4rem;
            font-family: monospace;
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

        @media (max-width: 480px) {
            .toolbar { gap: 0.3rem; }
            .toolbar-btn { padding: 0.3rem 0.6rem; font-size: 0.75rem; }
            .cat-btn { padding: 0.4rem 0.8rem; font-size: 0.8rem; }
        }
    </style>
</head>
<body>
    <!-- 头部 -->
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <h1>Ogden's Basic English</h1>
                <div class="subtitle">850 词学习手册</div>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索单词、释义或例句...">
                <span class="shortcut">/</span>
            </div>
            <div class="toolbar">
                <div class="toolbar-group">
                    <button class="toolbar-btn active" id="btnUK" onclick="setAccent('uk')">英式发音</button>
                    <button class="toolbar-btn" id="btnUS" onclick="setAccent('us')">美式发音</button>
                </div>
                <div class="toolbar-group">
                    <button class="toolbar-btn" id="btnLight" onclick="setTheme('light')">浅色模式</button>
                    <button class="toolbar-btn active" id="btnDark" onclick="setTheme('dark')">深色模式</button>
                </div>
                <div class="toolbar-group">
                    <button class="toolbar-btn active" id="btnSimplified" onclick="setChinese('simplified')">简</button>
                    <button class="toolbar-btn" id="btnTraditional" onclick="setChinese('traditional')">繁</button>
                </div>
                <button class="toolbar-btn" onclick="openFlashcard()">打开卡片练习</button>
            </div>
        </div>
    </header>

    <!-- 分类导航 -->
    <nav class="categories">
        <div class="categories-content">
            <button class="cat-btn active" data-cat="all" onclick="filterCategory('all')">All · 全部 <span class="count">850</span></button>
            <button class="cat-btn" data-cat="OP" onclick="filterCategory('OP')">Operations · 操作词 <span class="count">100</span></button>
            <button class="cat-btn" data-cat="GT" onclick="filterCategory('GT')">General Things · 通用词 <span class="count">400</span></button>
            <button class="cat-btn" data-cat="PT" onclick="filterCategory('PT')">Picturable · 图示词 <span class="count">200</span></button>
            <button class="cat-btn" data-cat="QG" onclick="filterCategory('QG')">Qualities · 性质词 <span class="count">100</span></button>
            <button class="cat-btn" data-cat="OPP" onclick="filterCategory('OPP')">Opposites · 反义对 <span class="count">50</span></button>
        </div>
    </nav>

    <!-- 主内容 -->
    <main class="main" id="mainContent">
        <!-- 动态生成 -->
    </main>

    <!-- 卡片练习 -->
    <div class="flashcard-overlay" id="flashcardOverlay">
        <div class="flashcard">
            <button class="flashcard-close" onclick="closeFlashcard()">×</button>
            <div class="flashcard-word" id="flashcardWord"></div>
            <div class="flashcard-phonetic" id="flashcardPhonetic"></div>
            <div class="flashcard-hint">点击翻牌查看释义</div>
            <div class="flashcard-answer" id="flashcardAnswer">
                <div class="flashcard-zh" id="flashcardZh"></div>
                <div class="flashcard-en" id="flashcardEn"></div>
            </div>
            <div class="flashcard-controls">
                <button class="flashcard-btn" onclick="prevCard()">◀ 上一个</button>
                <button class="flashcard-btn" onclick="randomCard()">🎲 随机</button>
                <button class="flashcard-btn" onclick="nextCard()">下一个 ▶</button>
            </div>
        </div>
    </div>

    <!-- Toast -->
    <div class="toast" id="toast"></div>

    <!-- 页脚 -->
    <footer class="footer">
        <p>基于 Ogden's Basic English · 仅供学习使用</p>
        <div class="shortcuts">
            快捷键: <kbd>/</kbd> 搜索 · <kbd>Esc</kbd> 关闭 · <kbd>Space</kbd> 翻牌
        </div>
    </footer>

    <script>
        // ========== 数据 ==========
        const WORDS = ''' + json.dumps(words, ensure_ascii=False) + ''';

        // ========== 状态 ==========
        const state = {
            currentCategory: 'all',
            currentPage: 1,
            pageSize: 43,
            isUKAccent: true,
            isDarkMode: false,
            isSimplified: true,
            searchQuery: '',
            flashcardIndex: 0,
            sortOrder: 'default'
        };

        // ========== 分类映射 ==========
        const categoryNames = {
            'OP': { zh: '操作词', zhTw: '操作詞', en: 'Operations', desc: '动词、介词、代词、连词等', descTw: '動詞、介詞、代詞、連詞等' },
            'GT': { zh: '通用词', zhTw: '通用詞', en: 'General Things', desc: '日常事物、概念、抽象名词等', descTw: '日常事物、概念、抽象名詞等' },
            'PT': { zh: '图示词', zhTw: '圖示詞', en: 'Picturable', desc: '可以用图像表示的具体事物', descTw: '可以用圖像表示的具體事物' },
            'QG': { zh: '性质词', zhTw: '性質詞', en: 'Qualities', desc: '形容词、描述性词语', descTw: '形容詞、描述性詞語' },
            'OPP': { zh: '反义对', zhTw: '反義對', en: 'Opposites', desc: '成对的反义词', descTw: '成對的反義詞' }
        };

        // ========== 初始化 ==========
        document.addEventListener('DOMContentLoaded', () => {
            loadSettings();
            renderWords();
            setupEventListeners();
        });

        function loadSettings() {
            state.isDarkMode = localStorage.getItem('theme') === 'dark';
            state.isUKAccent = localStorage.getItem('accent') !== 'us';
            state.isSimplified = localStorage.getItem('chinese') !== 'traditional';
            
            document.documentElement.setAttribute('data-theme', state.isDarkMode ? 'dark' : '');
            updateAccentButtons();
            updateThemeButtons();
            updateChineseButtons();
        }

        function setupEventListeners() {
            document.getElementById('searchInput').addEventListener('input', (e) => {
                state.searchQuery = e.target.value.toLowerCase();
                state.currentPage = 1;
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

        // ========== 渲染单词 ==========
        function renderWords() {
            const main = document.getElementById('mainContent');
            let filtered = getFilteredWords();
            
            // 分组
            const groups = {};
            filtered.forEach(w => {
                if (!groups[w.category]) groups[w.category] = [];
                groups[w.category].push(w);
            });

            let html = '';
            
            if (state.currentCategory === 'all') {
                // 显示所有分类
                for (const [cat, words] of Object.entries(groups)) {
                    html += renderCategorySection(cat, words);
                }
            } else {
                // 只显示当前分类
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
            const desc = state.isSimplified ? info.desc : (info.descTw || info.desc);
            
            let html = `
                <div class="section-header">
                    <div>
                        <div class="section-title">${info.en}</div>
                        <div class="section-subtitle">${info.zh} · ${desc}</div>
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
            const tagClass = w.category.toLowerCase().replace('pp', 'pp');
            const zh = state.isSimplified ? w.zh : (w.zhTw || w.zh);
            const explain = state.isSimplified ? w.zhExplain : (w.zhExplainTw || w.zhExplain);
            const exampleZh = state.isSimplified ? w.exampleZh : (w.exampleZhTw || w.exampleZh);
            
            return `
                <article class="word-card">
                    <div class="word-header">
                        <div class="word-main">
                            <div class="word-text">${w.word}</div>
                            <div class="word-phonetic">${w.phonetic || ''}</div>
                        </div>
                        <span class="word-tag tag-${tagClass}">${w.category}</span>
                        <button class="speak-btn" onclick="speakWord('${w.word}')">🔊 读单词</button>
                    </div>
                    <div class="word-zh">${zh}</div>
                    <div class="word-explain">${explain}</div>
                    <div class="definition-label">Definition</div>
                    <div class="word-en">${w.en}</div>
                    <div class="example-box">
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
            
            // 分类过滤
            if (state.currentCategory !== 'all') {
                words = words.filter(w => w.category === state.currentCategory);
            }
            
            // 搜索过滤
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

        // ========== 语音朗读 ==========
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

        // ========== 分类过滤 ==========
        function filterCategory(cat) {
            state.currentCategory = cat;
            state.currentPage = 1;
            
            document.querySelectorAll('.cat-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.cat === cat);
            });
            
            renderWords();
        }

        // ========== 口音切换 ==========
        function setAccent(accent) {
            state.isUKAccent = accent === 'uk';
            localStorage.setItem('accent', accent);
            updateAccentButtons();
            showToast(accent === 'uk' ? '已切换到英式发音' : '已切换到美式发音');
        }

        function updateAccentButtons() {
            document.getElementById('btnUK').classList.toggle('active', state.isUKAccent);
            document.getElementById('btnUS').classList.toggle('active', !state.isUKAccent);
        }

        // ========== 主题切换 ==========
        function setTheme(theme) {
            state.isDarkMode = theme === 'dark';
            document.documentElement.setAttribute('data-theme', state.isDarkMode ? 'dark' : '');
            localStorage.setItem('theme', theme);
            updateThemeButtons();
            showToast(state.isDarkMode ? '已切换到深色模式' : '已切换到浅色模式');
        }

        function updateThemeButtons() {
            document.getElementById('btnLight').classList.toggle('active', !state.isDarkMode);
            document.getElementById('btnDark').classList.toggle('active', state.isDarkMode);
        }

        // ========== 中文切换 ==========
        function setChinese(type) {
            state.isSimplified = type === 'simplified';
            localStorage.setItem('chinese', type);
            updateChineseButtons();
            renderWords();
            showToast(state.isSimplified ? '已切换到简体中文' : '已切换到繁體中文');
        }

        function updateChineseButtons() {
            document.getElementById('btnSimplified').classList.toggle('active', state.isSimplified);
            document.getElementById('btnTraditional').classList.toggle('active', !state.isSimplified);
        }

        // ========== 搜索 ==========
        function searchWord(word) {
            document.getElementById('searchInput').value = word;
            state.searchQuery = word.toLowerCase();
            state.currentPage = 1;
            renderWords();
        }

        // ========== 卡片练习 ==========
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
            document.getElementById('flashcardZh').textContent = w.zh;
            document.getElementById('flashcardEn').textContent = w.en;
            document.getElementById('flashcardAnswer').classList.remove('show');
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

        // ========== Toast ==========
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }
    </script>
</body>
</html>'''

# 保存HTML
output_path = '/Users/charlescao/Hermes/english-vocab/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ 已生成: {output_path}")
print(f"   单词数量: {len(words)}")
