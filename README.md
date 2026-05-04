# AI-SERVICE - Medical Assistant API

## 📋 Mô tả Project

AI-SERVICE là một hệ thống API dựa trên FastAPI, kết hợp **BioBERT** và **Mistral LLM** để xây dựng một trợ lý y tế thông minh. Hệ thống có khả năng:

- **Trích xuất entities**: Sử dụng BioBERT để nhận diện các bệnh lý (symptoms) và thuốc (drugs) từ đầu vào của người dùng
- **Phân tích ý định**: Dùng Mistral LLM để hiểu ý định của người dùng
- **Đánh giá mức độ khẩn cấp**: Xác định mức độ ưu tiên của yêu cầu (LOW, MEDIUM, HIGH)
- **Đề xuất hành động**: Cung cấp các hành động/lời khuyên thích hợp
- **Tạo phản hồi**: Trả lời người dùng một cách thân thiện và hữu ích

## 🔧 Công nghệ Sử dụng

- **Python 3.8+**
- **FastAPI** - Framework web hiện đại, hiệu suất cao
- **Transformers** - Thư viện cho BioBERT model
- **Ollama** - Runtime cho chạy Mistral LLM
- **Pydantic** - Validation dữ liệu
- **Requests** - HTTP client

## 📦 Cài Đặt

### 1. Clone Repository
```bash
git clone https://github.com/VoTrucSonBKiter/AI-SERVICE.git
cd AI-SERVICE
```

### 2. Tạo Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

Hoặc cài từng package:
```bash
pip install fastapi uvicorn transformers torch requests pydantic
```

### 4. Cài Đặt Ollama và Mistral Model

**Cài Ollama:**
- Tải từ: https://ollama.ai
- Cài đặt theo hướng dẫn

**Pull Mistral model:**
```bash
ollama pull mistral
ollama serve
```

Ollama sẽ chạy trên `http://localhost:11434`

## 🚀 Chạy Project

### 1. Đảm bảo Ollama đang chạy
```bash
# Terminal 1
ollama serve
```

### 2. Chạy FastAPI Server (Terminal khác)
```bash
# Kích hoạt virtual environment
venv\Scripts\activate

# Chạy server
uvicorn main:app --reload --port 8000
```

Server sẽ khởi động tại `http://localhost:8000`

### 3. Kiểm Tra API

**Xem tài liệu Swagger:**
```
http://localhost:8000/docs
```

**Test endpoint /analyze:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tôi bị đau đầu và sốt, nên uống gì?"}'
```

**Response mẫu:**
```json
{
  "intent": "medical_advice",
  "entities": {
    "symptoms": ["đau đầu", "sốt"],
    "drugs": []
  },
  "urgency": "MEDIUM",
  "actions": ["Uống thuốc hạ sốt", "Ngủ đủ", "Uống nước ấm"],
  "response_text": "Bạn nên nghỉ ngơi, uống thuốc hạ sốt và liên hệ bác sĩ nếu tình trạng không cải thiện."
}
```

## 📁 Cấu Trúc Thư Mục

```
AI-SERVICE/
├── main.py           # FastAPI app chính
├── biobert.py        # Module trích xuất entities với BioBERT
├── llm.py            # Module gọi Mistral LLM
├── schema.py         # Prompt template cho LLM
├── requirements.txt  # Danh sách dependencies
└── README.md         # File này
```

## 🛠️ Troubleshooting

**Lỗi: Ollama connection refused**
- Đảm bảo Ollama đang chạy: `ollama serve`
- Kiểm tra cổng 11434 không bị block

**Lỗi: BioBERT model không tải**
- Kiểm tra kết nối internet
- Model sẽ tải từ Hugging Face lần đầu (cần ~600MB)

**Lỗi: Port 8000 đã được sử dụng**
```bash
uvicorn main:app --reload --port 8001
```

## 📝 Ghi Chú

- BioBERT model tải tự động lần đầu tiên chạy
- API chỉ hỗ trợ POST request đến endpoint `/analyze`
- Response luôn là JSON format

## 👨‍💻 Author

Phát triển cho SmartHospital Project

---

**Hãy tạo issue nếu bạn gặp vấn đề! 😊**
