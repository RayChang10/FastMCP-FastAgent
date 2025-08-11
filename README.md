# 🎯 智能面試系統 (Intelligent Interview System)

一個整合多種 AI 技術的完整智能面試解決方案，專為求職者和企業設計的專業面試平台。

## 🌟 專案特色

- **🤖 AI 驅動面試**: 整合 OpenAI、Fast Agent、MCP 等多種 AI 技術
- **🎭 虛擬面試官**: 支援語音互動和表情變化的數字人系統
- **📝 智能履歷管理**: 自動解析履歷檔案，智能技能匹配
- **🎤 語音互動**: 支援語音輸入輸出，TTS/STT 整合
- **🔍 面試分析**: AI 驅動的面試表現評估和改進建議
- **🌐 多平台支援**: Web 介面、API 服務、WebSocket 即時通訊

## 🏗️ 技術架構

### 核心技術棧
- **後端框架**: Flask + SQLAlchemy + Flask-RESTful
- **AI 引擎**: OpenAI GPT、Fast Agent、MCP (Model Context Protocol)
- **資料庫**: MongoDB + SQLite
- **語音處理**: Whisper STT、Azure TTS、自定義 TTS 引擎
- **前端技術**: Bootstrap 5、jQuery、Web Speech API
- **即時通訊**: WebSocket、HTTP API

### 系統組件
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端介面      │    │   Fast Agent    │    │   MCP Server    │
│  (Web/語音)     │◄──►│   (AI 處理)     │◄──►│   (工具整合)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Flask 後端     │    │   語音處理      │    │   資料庫層      │
│  (API 服務)     │    │  (TTS/STT)      │    │  (MongoDB/SQLite)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 安裝與設置

### 環境需求
- **Python**: 3.8.1+
- **系統**: Windows 10+ / Linux / macOS
- **記憶體**: 建議 8GB+
- **硬碟空間**: 至少 2GB

### 🚀 快速開始

#### 1. 克隆專案
```bash
git clone <repository-url>
cd ispan_project
```

#### 2. 安裝依賴
```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 Poetry (推薦)
poetry install
```

#### 3. 環境配置
```bash
# 複製環境變數範例
cp env.example .env

# 編輯 .env 檔案，填入您的 API 金鑰
OPENAI_API_KEY=your_openai_api_key_here
PYTHONPATH=.
PYTHONUNBUFFERED=1
```

#### 4. 啟動系統
```bash
# 啟動整合系統
python start_integrated_system.py

# 或分別啟動各組件
python server.py          # MCP 伺服器 (埠 8000)
python http_wrapper.py    # HTTP API 包裝器 (埠 8080)
python virtual_interviewer/app.py  # 虛擬面試系統 (埠 5000)
```

## 🎯 核心功能

### 1. 智能面試系統
- **狀態管理**: 等待 → 自我介紹 → 分析 → 問答 → 總結
- **AI 面試官**: 根據狀態智能調整回應策略
- **問題生成**: 動態生成面試問題和標準答案
- **答案分析**: AI 驅動的回答評估和改進建議
- **自動面試模式**: 支援連續問答，自動下一題功能
- **面試流程控制**: 完整的自我介紹 → 分析 → 技術問答 → 總結流程

### 2. 履歷管理系統
- **履歷建立**: 結構化履歷資料輸入
- **檔案解析**: 支援 PDF、Word 等格式自動解析
- **技能匹配**: AI 驅動的技能與職缺匹配
- **關鍵字提取**: 自動識別專業技能和經驗

### 3. 語音互動系統
- **語音識別 (STT)**: 支援多種引擎 (Whisper、Azure、Google)
- **語音合成 (TTS)**: 高品質中文語音輸出
- **唇形同步**: 數字人表情和口型同步
- **即時處理**: WebSocket 支援即時語音互動

### 4. 數字人整合
- **Fay 系統**: 完整的數字人表情和動作控制
- **虛擬面試官**: 可自定義外觀和個性
- **情感表達**: 支援多種情感狀態和強度
- **動作控制**: 說話、聆聽、待機等狀態管理

### 5. 自動化面試工具
- **簡化面試模式**: 支援命令行自動面試，無需 Web 介面
- **批量面試處理**: 可處理多個面試會話
- **面試資料管理**: MongoDB 整合，支援面試資料匯入和查詢
- **面試統計分析**: 提供詳細的面試表現統計和趨勢分析

## 🔧 API 端點

### 面試系統 API
```http
POST /api/interview          # 處理面試對話
POST /api/fast-agent         # Fast Agent 專用 API
GET  /api/users              # 取得用戶列表
POST /api/users              # 創建用戶履歷
GET  /api/users/<id>         # 取得特定用戶資料
```

### 語音處理 API
```http
POST /api/stt                # 語音轉文字
POST /api/tts/generate       # 文字轉語音
POST /api/speech             # 語音處理綜合 API
```

### 數字人控制 API
```http
POST /api/avatar/control     # 虛擬人狀態控制
POST /api/avatar/lipsync     # 唇形同步資料
POST /api/fay/integration    # Fay 系統整合
```

### 檔案處理 API
```http
POST /api/upload             # 履歷檔案上傳
```

### 面試資料管理 API
```http
POST /api/interview/import   # 匯入面試題庫
GET  /api/interview/stats    # 取得面試統計
POST /api/interview/batch    # 批量面試處理
```

## 📁 專案結構

```
ispan_project/
├── 📁 核心系統
│   ├── main.py                      # 主程式入口
│   ├── server.py                    # MCP 伺服器
│   ├── fast_agent_interview.py      # Fast Agent 面試系統
│   ├── fast_agent_bridge.py         # Fast Agent 橋接模組
│   ├── http_wrapper.py              # HTTP API 包裝器
│   ├── start_integrated_system.py   # 整合系統啟動器
│   ├── simple_auto_interview.py     # 簡化自動面試系統
│   └── interview.py                 # 面試資料匯入工具
│
├── 📁 工具模組 (tools/)
│   ├── question_manager.py          # 問題管理
│   ├── answer_analyzer.py           # 答案分析
│   ├── interview_session.py         # 面試會話管理
│   ├── database.py                  # 資料庫操作
│   └── ui_manager.py                # 介面管理
│
├── 📁 虛擬面試系統 (virtual_interviewer/)
│   ├── app.py                       # Flask 主應用
│   ├── templates/                   # HTML 模板
│   ├── static/                      # 靜態資源
│   └── run.py                       # 啟動腳本
│
├── 📁 面試題庫 (interview_csv/)
│   ├── python1.csv                  # Python 面試題
│   ├── javascripts1.csv             # JavaScript 面試題
│   ├── data_science1.csv            # 資料科學面試題
│   └── ...                          # 其他技術領域
│
├── 📁 配置檔案
│   ├── config.py                    # 統一配置管理
│   ├── fastagent.config.yaml        # Fast Agent 配置
│   ├── fastagent.jsonl              # Fast Agent 工具定義
│   ├── requirements.txt              # Python 依賴
│   ├── env.example                  # 環境變數範例
│   └── .env                         # 環境變數 (需自建)
│
└── 📁 文檔
    ├── README.md                    # 專案說明
    ├── ENV_SETUP.md                 # 環境設置指南
    ├── AI_SCORING_GUIDE.md          # AI 評分指南
    └── 流程.txt                      # 系統流程說明
```

## 🚀 使用指南

### 基本面試流程

#### 1. 開始面試
```bash
# 啟動系統
python start_integrated_system.py

# 開啟瀏覽器訪問
http://localhost:5000
```

#### 2. 面試步驟
1. **自我介紹**: 用戶進行完整的自我介紹
2. **AI 分析**: 系統分析介紹內容並給出建議
3. **技術問答**: AI 面試官提問，用戶回答
4. **答案評估**: 系統分析回答並給出評分
5. **總結建議**: 生成完整的面試表現總結

#### 3. 語音互動
```javascript
// 語音輸入
const recognition = new webkitSpeechRecognition();
recognition.start();

// 語音輸出
const utterance = new SpeechSynthesisUtterance("您好！");
speechSynthesis.speak(utterance);
```

#### 4. 命令行自動面試
```bash
# 啟動簡化自動面試系統
python simple_auto_interview.py

# 匯入面試題庫到 MongoDB
python interview.py

# 檢查用戶狀態
python check_user_state.py
```

### 進階功能使用

#### 1. Fast Agent 整合
```python
from fast_agent_bridge import call_fast_agent_function

# 調用 Fast Agent 功能
result = call_fast_agent_function(
    "analyze_answer",
    user_answer="我的回答內容",
    question="面試問題",
    standard_answer="標準答案"
)
```

#### 2. MCP 工具使用
```python
from server import get_random_question, analyze_resume

# 獲取隨機面試題
question = get_random_question()

# 分析履歷
analysis = analyze_resume("履歷內容")
```

#### 3. 數字人控制
```javascript
// 控制虛擬面試官
fetch('/api/avatar/control', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        action: 'speak',
        text: '歡迎參加面試！',
        emotion: 'friendly'
    })
});
```

## 🔧 開發指南

### 新增面試題目
1. 在 `interview_csv/` 目錄下創建新的 CSV 檔案
2. 格式：`question,standard_answer,category,difficulty`
3. 系統會自動載入新的題目

### 面試資料匯入
1. 使用 `interview.py` 將 CSV 題庫匯入 MongoDB
2. 支援批量匯入和索引建立
3. 自動處理資料格式驗證和錯誤處理

### 擴展 AI 功能
1. 在 `tools/` 目錄下創建新的工具模組
2. 在 `fast_agent_interview.py` 中註冊新工具
3. 更新配置檔案以支援新功能

### 自定義語音引擎
1. 在 `virtual_interviewer/app.py` 中擴展 TTS/STT 類別
2. 實現對應的語音處理方法
3. 更新 API 端點以支援新引擎

## 🧪 測試與偵錯

### 單元測試
```bash
# 執行所有測試
python -m pytest

# 執行特定測試
python -m pytest test_interview_flow.py
```

### API 測試
```bash
# 測試面試 API
curl -X POST http://localhost:5000/api/interview \
  -H "Content-Type: application/json" \
  -d '{"message": "開始面試", "user_id": "test_user"}'

# 測試語音 API
curl -X POST http://localhost:5000/api/stt \
  -F "audio=@test_audio.wav" \
  -F "engine=whisper"
```

### 系統監控
```bash
# 檢查服務狀態
python check_user_state.py

# 測試面試流程
python test_interview_flow.py

# 測試問題分析
python test_question_analysis.py

# 測試退出邏輯
python test_exit_logic.py
```

## 🌐 部署指南

### 開發環境
```bash
# 本地開發
python start_integrated_system.py

# 或使用 Flask 開發伺服器
export FLASK_ENV=development
python virtual_interviewer/app.py
```

### 生產環境
```bash
# 使用 Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 virtual_interviewer.app:app

# 使用 Docker (需自建 Dockerfile)
docker build -t intelligent-interview .
docker run -p 5000:5000 intelligent-interview
```

### 環境變數配置
```bash
# 生產環境配置
export FLASK_ENV=production
export OPENAI_API_KEY=your_production_key
export DATABASE_URL=your_production_db_url
```

## 🔮 未來規劃

### Phase 1 (已完成) ✅
- [x] 基本面試系統架構
- [x] AI 驅動的問題生成和答案分析
- [x] 履歷管理和技能匹配
- [x] 語音互動基礎功能
- [x] Fast Agent 橋接模組
- [x] 自動面試模式
- [x] MongoDB 資料匯入工具
- [x] 面試流程控制系統

### Phase 2 (開發中) 🚧
- [ ] 多語言支援 (英文、日文等)
- [ ] 進階情感分析
- [ ] 面試表現歷史追蹤
- [ ] 企業端管理介面

### Phase 3 (規劃中) 📋
- [ ] 視覺面試 (視訊整合)
- [ ] 群體面試支援
- [ ] 面試官培訓模式
- [ ] 企業招聘流程整合

## 🤝 貢獻指南

### 開發流程
1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 程式碼規範
- 遵循 PEP 8 Python 風格指南
- 使用有意義的變數和函數命名
- 添加適當的註解和文檔字串
- 確保所有測試通過

### 問題回報
- 使用 GitHub Issues 回報問題
- 提供詳細的錯誤訊息和重現步驟
- 包含系統環境和版本資訊

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 👥 開發團隊

- **專案架構**: 全端開發團隊
- **AI 整合**: OpenAI、Fast Agent 專家
- **語音處理**: TTS/STT 技術專家
- **UI/UX 設計**: 使用者體驗設計師

## 📞 聯絡資訊

如有任何問題或建議，請透過以下方式聯絡：

- **GitHub Issues**: [專案 Issues 頁面](https://github.com/your-repo/issues)
- **Email**: contact@intelligent-interview.com
- **文檔**: [完整 API 文檔](./docs/)

## 🙏 致謝

感謝以下開源專案和服務的支援：

- **OpenAI**: GPT 模型和 API 服務
- **Fast Agent**: 快速 AI 代理框架
- **Flask**: Python Web 框架
- **Bootstrap**: 前端 UI 框架
- **Whisper**: 語音識別技術
- **MongoDB**: 文件資料庫服務
- **SQLAlchemy**: Python ORM 框架
- **Web Speech API**: 瀏覽器語音處理

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！您的支持是我們持續改進的動力。

## 📊 專案統計

- **版本**: 2.1.0
- **最後更新**: 2024年12月
- **Python 版本**: 3.8.1+
- **授權**: MIT License
- **狀態**: 活躍開發中
- **支援的技術領域**: Python、JavaScript、Data Science、Linux、Docker、MySQL、PostgreSQL、Blockchain、CSS、Algorithm、Data Structures
- **面試題庫數量**: 12+ 個技術領域，數百道面試題
- **AI 模型整合**: OpenAI GPT、Fast Agent、MCP Protocol
