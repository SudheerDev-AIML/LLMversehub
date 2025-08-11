# GPT-OSS: Open-Weight Reasoning AI 🧠

Experience the power of GPT-OSS reasoning locally with an enhanced UI that showcases the model's advanced capabilities and transparent thinking process.

## 🌟 What Makes This Special

- 🧠 **Visible Chain-of-Thought**: Watch GPT-OSS think through problems step-by-step
- 🏠 **100% Local**: Run on your own hardware using Ollama - complete privacy
- ⚡ **Advanced Reasoning**: GPT-OSS 20B/120B with mixture-of-experts architecture
- 🎯 **Multiple Reasoning Efforts**: Choose between low, medium, and high reasoning intensity
- 🔧 **Tool Use Ready**: Built for web search, code execution, and agentic workflows
- 💰 **Zero Cost**: No API fees or usage limits
- 🔒 **Apache 2.0**: Fully open license for commercial use

## 🚀 Key Features

### Enhanced UI Experience
- **Professional Design**: Modern gradient themes with responsive layout
- **Real-time Thinking**: See the model's reasoning process unfold live
- **Interactive Examples**: One-click prompts showcasing different capabilities
- **Session Statistics**: Track messages, thinking steps, and response times

### GPT-OSS Capabilities Showcase
- **🧮 Advanced Mathematics**: Competition-level problem solving
- **💻 Code Generation**: Python, algorithms, and complexity analysis
- **🔬 Scientific Reasoning**: Chemistry, biology, physics explanations
- **🧩 Logic Puzzles**: Multi-step reasoning and deduction
- **🩺 Health & Medical**: Outperforms many proprietary models
- **🎯 Competition Tasks**: AIME, Codeforces, and more

### Technical Excellence
- **Mixture-of-Experts**: 32/128 experts with 4 active per token
- **128K Context**: Long conversation and document support
- **Streaming Responses**: Real-time generation with thinking visualization
- **Safety Trained**: Robust safety measures and alignment

## 📊 Performance Highlights

GPT-OSS delivers state-of-the-art performance:

- **Matches GPT-4o-mini** on core reasoning benchmarks
- **Outperforms GPT-4o** on health-related queries (HealthBench)
- **Exceeds proprietary models** on competition mathematics
- **Strong tool use** capabilities for agentic workflows
- **Efficient deployment** - 20B runs on 16GB, 120B on 80GB

## 🛠 Installation and Setup

### Prerequisites
- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- 16GB RAM minimum (20B model) or 80GB (120B model)

### 1. Setup Ollama

```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the GPT-OSS models
ollama pull gpt-oss:20b
```

### 2. Install Dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install streamlit ollama
```

### 3. Run the Enhanced App

```bash
uv run streamlit run chat_ui.py
# or with pip: streamlit run app.py
```

The app will be available at `look for url in your terminal`

## 🎯 Usage Examples

### Try These Prompts to See GPT-OSS in Action:

**🧮 Advanced Mathematics:**
```
Solve this step by step: If a train travels 120 miles in 2 hours, then speeds up by 25% for the next 3 hours, how far does it travel in total?
```

**💻 Code Generation:**
```
Write a Python function that finds the longest palindromic substring in a given string. Include time complexity analysis.
```

**🔬 Scientific Reasoning:**
```
Explain the process of photosynthesis and how it relates to climate change mitigation. Include the chemical equations.
```

**🧩 Logic Puzzle:**
```
Three friends Alice, Bob, and Charlie have different colored shirts (red, blue, green). Alice doesn't wear red, Bob doesn't wear blue, and the person in green is taller than Alice. If Charlie is the shortest, what color shirt does each person wear?
```

## 🎛 Configuration Options

### Reasoning Effort
- **Low** - Quick responses, basic reasoning
- **Medium** - Balanced performance and speed
- **High** - Deep analysis, slower but thorough

## 🔍 What You'll See

### Chain-of-Thought Transparency
Unlike black-box models, GPT-OSS shows you exactly how it thinks:
- Step-by-step reasoning process
- Problem decomposition
- Solution verification
- Real-time thinking visualization

### Session Analytics
Track your interaction patterns:
- Total messages exchanged
- Thinking steps taken
- Average response times
- Model performance metrics

## 🏗 Architecture Details

### GPT-OSS 20B Specifications
- **Total Parameters**: 21B
- **Active Parameters**: 3.6B per token
- **Experts**: 32 total, 4 active
- **Context Length**: 128K tokens
- **Memory Requirement**: 16GB


## 🔒 Privacy & Safety

- **Local Processing**: All conversations stay on your machine
- **No Data Collection**: Zero telemetry or usage tracking
- **Safety Trained**: Robust alignment and safety measures
- **Open Source**: Full transparency and auditability

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional example prompts
- UI/UX enhancements
- Performance optimizations
- New visualization features
- Documentation improvements

Please fork the repository and submit a pull request with your improvements.

## 📚 Learn More

- [GPT-OSS Announcement](https://openai.com/index/introducing-gpt-oss/)
- [Model Card](https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf)
- [Safety Research](https://cdn.openai.com/pdf/231bf018-659a-494d-976c-2efdfc72b652/oai_gpt-oss_Model_Safety.pdf)
- [Ollama Documentation](https://ollama.com/docs)

---

## 🙏 Acknowledgments

- OpenAI for releasing GPT-OSS as open-weight models
- Ollama team for excellent local inference support
- Streamlit for the amazing web app framework
