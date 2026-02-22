```
BMO/
│
├── 📂 src/                    # Mã nguồn chính của dự án
│   ├── 📂 core/                # Các module lõi
│   │   ├── __init__.py
│   │   ├── brain.py            # Tương tác với Ollama (LLM)
│   │   ├── ears.py             # Xử lý âm thanh -> text (STT)
│   │   └── mouth.py            # Text -> âm thanh (TTS)
│   │
│   ├── 📂 orchestrator/         # Điều phối luồng hoạt động
│   │   ├── __init__.py
│   │   └── main_loop.py        # Vòng lặp chính: nghe -> suy luận -> nói
│   │
│   └── 📂 utils/                # Các tiện ích dùng chung
│       ├── __init__.py
│       ├── audio_helpers.py     # Xử lý audio (record, play)
│       ├── config_loader.py     # Đọc file cấu hình
│       └── logger.py            # Ghi log
│
├── 📂 models/                   # Chứa models đã tải về (nếu có)
│   ├── 📂 stt/                   # Whisper models
│   └── 📂 tts/                   # Piper voice models
│
├── 📂 configs/                  # File cấu hình
│   ├── config.yaml              # Cấu hình chính (model names, thresholds...)
│   └── logging.yaml             # Cấu hình ghi log
│
├── 📂 tests/                    # Unit tests
│   ├── test_brain.py
│   ├── test_ears.py
│   └── test_mouth.py
│
├── 📂 scripts/                  # Các script hỗ trợ
│   ├── download_models.py       # Script tải models tự động
│   └── test_microphone.py       # Kiểm tra mic hoạt động
│
├── 📂 data/                      # Dữ liệu tạm thời (thường được .gitignore)
│   ├── recordings/               # Ghi âm tạm
│   └── cache/                    # Cache responses
│
├── 📂 docs/                      # Tài liệu dự án
│   ├── README.md                 # Giới thiệu, cài đặt, cách dùng
│   └── architecture.md           # Mô tả kiến trúc
│
├── 📂 notebooks/                  # (Optional) Jupyter notebooks cho thử nghiệm
│   └── experiment.ipynb
│
├── .gitignore                    # Các file/thư mục không đẩy lên git
├── requirements.txt               # Dependencies cho pip
├── pyproject.toml                 # (Modern) Thay thế setup.py
├── Makefile                       # (Optional) Các lệnh tự động hóa
├── .env.example                   # Mẫu biến môi trường (API keys, paths...)
├── .pre-commit-config.yaml        # (Optional) Kiểm tra code trước commit
└── README.md                      # File giới thiệu chính
```