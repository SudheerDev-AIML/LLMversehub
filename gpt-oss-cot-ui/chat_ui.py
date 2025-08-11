import re
import base64
import streamlit as st
from ollama import chat
import time
import json
from datetime import datetime

# Set Streamlit page configuration
st.set_page_config(
    page_title="GPT-OSS: Open-Weight Reasoning AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
def load_custom_css():
    st.markdown("""
    <script>
        function scrollToBottom() {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Also scroll the main streamlit iframe
                window.scrollTo(0, document.body.scrollHeight);
            }
        }
        
        // Call scrollToBottom periodically to handle dynamic content
        setInterval(scrollToBottom, 1000);
    </script>
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #10a37f;
        --secondary-color: #1a73e8;
        --accent-color: #ff6b35;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-background: rgba(255, 255, 255, 0.95);
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
    }
    
    /* Header styling */
    .main-header {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .feature-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    
    .badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: var(--card-background);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Thinking process styling */
    .thinking-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid var(--accent-color);
    }
    
    .thinking-header {
        color: white;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .thinking-content {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.4;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* Stats and metrics */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 3px solid var(--primary-color);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animation for thinking */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .thinking-animation {
        animation: pulse 2s infinite;
    }
    
    /* Model info cards */
    .model-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .model-specs {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .spec-item {
        text-align: center;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .spec-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .spec-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create an attractive header with GPT-OSS branding."""
    st.markdown("""
    <div class="main-header">
        <h1>
            🧠 GPT-OSS 🤖
        </h1>
        <div class="subtitle">
            Open-Weight Reasoning AI with Chain-of-Thought Transparency
        </div>
        <div class="feature-badges">
            <span class="badge">🧠 Visible Thinking</span>
            <span class="badge">🔧 Tool Use</span>
            <span class="badge">🏠 100% Local</span>
            <span class="badge">🔒 Privacy First</span>
            <span class="badge">⚡ 20B Parameters</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create an enhanced sidebar with model information and controls."""
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Model Selection and Info
        st.markdown("### 🤖 Model Configuration")
        
        # Fixed to 20B model only
        model_choice = "gpt-oss:20b"
        st.info("🚀 Using GPT-OSS 20B Model")
        
        reasoning_effort = st.selectbox(
            "Reasoning Effort",
            ["low", "medium", "high"],
            index=1,
            help="Higher effort = better reasoning but slower response"
        )
        
        # Model specifications for 20B - compact version
        st.markdown("### 📊 Model Info")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Parameters", "21B")
            st.metric("Experts", "32")
        with col2:
            st.metric("Active", "3.6B")
            st.metric("Context", "128K")
        
        # Session stats
        if "session_stats" in st.session_state:
            st.markdown("### 📈 Session Statistics")
            stats = st.session_state.session_stats
            st.metric("Messages", stats.get("messages", 0))
            st.metric("Thinking Steps", stats.get("thinking_steps", 0))
            st.metric("Avg Response Time", f"{stats.get('avg_response_time', 0):.1f}s")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.messages = [
                {"role": "system", "content": f"You are GPT-OSS, an advanced open-weight reasoning model. Use {reasoning_effort} reasoning effort. Show your thinking process clearly."}
            ]
            st.session_state.session_stats = {
                "messages": 0,
                "thinking_steps": 0,
                "avg_response_time": 0,
                "total_response_time": 0
            }
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return model_choice, reasoning_effort

def process_thinking_stream(stream, model_choice):
    """Process streaming response with enhanced thinking visualization."""
    thinking_content = ""
    response_content = ""
    start_time = time.time()
    
    # Initialize session state for processing status
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    
    # Create containers for real-time updates
    thinking_container = st.empty()
    response_container = st.empty()
    stop_button = st.empty()
    
    # Add stop button
    if stop_button.button("🛑 Stop Response", key="stop_generation"):
        st.session_state.stop_generation = True
        return thinking_content, response_content, time.time() - start_time
    
    # Initialize stop flag if not exists
    if 'stop_generation' not in st.session_state:
        st.session_state.stop_generation = False
    
    with st.status("🧠 GPT-OSS is thinking...", expanded=True) as status:
        thinking_steps = 0
        
        for chunk in stream:
            # Check if stop button was clicked
            if st.session_state.stop_generation:
                st.session_state.stop_generation = False  # Reset for next time
                break
                
            # Handle thinking content
            if chunk["message"].get("thinking"):
                thinking_content += chunk["message"]["thinking"]
                thinking_steps += 1
                
                # Update thinking display in real-time
                thinking_container.markdown(f"""
                <div class="thinking-container">
                    <div class="thinking-header thinking-animation">
                        🧠 Chain-of-Thought Reasoning (Step {thinking_steps})
                    </div>
                    <div class="thinking-content">
                        {thinking_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Handle response content
            if chunk["message"].get("content"):
                response_content += chunk["message"]["content"]
                
                # Update response display in real-time
                response_container.markdown(response_content)
        
        # Final status update
        response_time = time.time() - start_time
        status.update(
            label=f"✅ Reasoning complete! ({response_time:.1f}s, {thinking_steps} thinking steps)", 
            state="complete", 
            expanded=False
        )
        
        # Add auto-scroll after response is complete
        st.markdown("""
            <script>
                function scrollToChatInput() {
                    const chatInput = document.querySelector('.stChatInputContainer');
                    if (chatInput) {
                        chatInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
                setTimeout(scrollToChatInput, 1000);
            </script>
        """, unsafe_allow_html=True)
    
    # Update session statistics
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "messages": 0,
            "thinking_steps": 0,
            "avg_response_time": 0,
            "total_response_time": 0
        }
    
    stats = st.session_state.session_stats
    stats["messages"] += 1
    stats["thinking_steps"] += thinking_steps
    stats["total_response_time"] += response_time
    stats["avg_response_time"] = stats["total_response_time"] / stats["messages"]
    
    return thinking_content, response_content, response_time

def display_message(message):
    """Display a message with enhanced formatting."""
    role = "user" if message["role"] == "user" else "assistant"
    
    with st.chat_message(role):
        if role == "assistant":
            thinking_content = message.get("thinking", "")
            display_assistant_message(message["content"], thinking_content)
        else:
            st.markdown(message["content"])

def display_assistant_message(content, thinking_content=None):
    """Display assistant message with enhanced thinking visualization."""
    # Display thinking content if present
    if thinking_content and thinking_content.strip():
        with st.expander("🧠 View Chain-of-Thought Reasoning", expanded=False):
            st.markdown(f"""
            <div class="thinking-content">
                {thinking_content}
            </div>
            """, unsafe_allow_html=True)
    
    # Display main response
    if content:
        st.markdown(content)
        
    # Add auto-scroll script
    st.markdown("""
        <script>
            function scroll_to_bottom() {
                var chatHistory = document.querySelector('.stChatFloating');
                if (chatHistory) {
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }
            }
            window.addEventListener('load', scroll_to_bottom);
            scroll_to_bottom();
        </script>
        """, unsafe_allow_html=True)

def display_chat_history():
    """Display chat history with enhanced formatting."""
    for message in st.session_state["messages"]:
        if message["role"] != "system":
            display_message(message)

def create_example_prompts():
    """Create example prompts to showcase GPT-OSS capabilities."""
    st.markdown("### 💡 Try These Examples")
    
    # Create tabs for different categories
    tab1, tab2 = st.tabs(["🧠 Reasoning", "🔧 Tool Use"])
    
    with tab1:
        reasoning_examples = [
            {
                "title": "🧮 Advanced Math",
                "prompt": "Solve this step by step: If a train travels 120 miles in 2 hours, then speeds up by 25% for the next 3 hours, how far does it travel in total?",
                "icon": "🚂"
            },
            {
                "title": "💻 Code Generation", 
                "prompt": "Write a Python function that finds the longest palindromic substring in a given string. Include time complexity analysis.",
                "icon": "🐍"
            },
            {
                "title": "🔬 Scientific Reasoning",
                "prompt": "Explain the process of photosynthesis and how it relates to climate change mitigation. Include the chemical equations.",
                "icon": "🌱"
            },
            {
                "title": "🧩 Logic Puzzle",
                "prompt": "Three friends Alice, Bob, and Charlie have different colored shirts (red, blue, green). Alice doesn't wear red, Bob doesn't wear blue, and the person in green is taller than Alice. If Charlie is the shortest, what color shirt does each person wear?",
                "icon": "🎯"
            }
        ]
        
        for i, example in enumerate(reasoning_examples):
            if st.button(f"{example['icon']} {example['title']}", key=f"reasoning_{i}"):
                st.session_state.example_prompt = example['prompt']
                st.rerun()
    
    with tab2:
        tool_examples = [
            {
                "title": "🔍 Web Search",
                "prompt": "Search for the latest news about artificial intelligence breakthroughs in 2025. Summarize the top 3 most important developments.",
                "icon": "🌐"
            },
            {
                "title": "🐍 Code Execution",
                "prompt": "Write and execute Python code to calculate the first 10 Fibonacci numbers, then create a simple visualization showing their growth pattern.",
                "icon": "⚡"
            },
            {
                "title": "📊 Data Analysis",
                "prompt": "Generate sample sales data for a fictional company and perform basic statistical analysis including mean, median, and trend analysis.",
                "icon": "📈"
            },
            {
                "title": "🔧 Multi-Tool Task",
                "prompt": "Research the current weather in San Francisco, then write Python code to convert the temperature to different units and explain the weather patterns.",
                "icon": "🛠️"
            },
            {
                "title": "📝 File Operations",
                "prompt": "Create a simple text file with a poem about AI, then read it back and analyze the literary devices used.",
                "icon": "📄"
            },
            {
                "title": "🧮 Calculator Tool",
                "prompt": "Use calculation tools to solve this complex problem: What's the compound interest on $10,000 invested at 7% annually for 15 years, compounded monthly?",
                "icon": "🔢"
            }
        ]
        
        for i, example in enumerate(tool_examples):
            if st.button(f"{example['icon']} {example['title']}", key=f"tool_{i}"):
                st.session_state.example_prompt = example['prompt']
                st.rerun()
    
    # Add instructions for tool use
    st.markdown("""
    ### 🔧 Tool Use Instructions
    
    To test tool capabilities, try prompts that ask GPT-OSS to:
    - **Search the web** for current information
    - **Execute code** in Python or other languages  
    - **Perform calculations** with specific tools
    - **Create and manipulate files**
    - **Combine multiple tools** for complex tasks
    
    **Example prompts:**
    - "Search for recent AI news and summarize it"
    - "Write Python code to solve [problem] and run it"
    - "Calculate [complex math] using appropriate tools"
    - "Create a file with [content] and then analyze it"
    """)

@st.cache_resource
def get_chat_model(model_name):
    """Get a cached instance of the chat model."""
    return lambda messages: chat(
        model=model_name,
        messages=messages,
        stream=True,
        think=True,
    )

def handle_user_input(model_choice, reasoning_effort):
    """Handle user input with enhanced processing."""
    # Check for example prompt
    user_input = None
    if hasattr(st.session_state, 'example_prompt'):
        user_input = st.session_state.example_prompt
        delattr(st.session_state, 'example_prompt')
    
    # Regular chat input with auto-scroll script
    if not user_input:
        st.markdown("""
            <script>
                function scrollToBottom() {
                    window.scrollTo(0, document.body.scrollHeight);
                }
                setTimeout(scrollToBottom, 500);
            </script>
        """, unsafe_allow_html=True)
        user_input = st.chat_input("Ask GPT-OSS anything... 🚀")
    
    if user_input:
        # Add reasoning effort instruction to system message
        system_msg = f"You are GPT-OSS, an advanced open-weight reasoning model. Use {reasoning_effort} reasoning effort. Show your thinking process clearly and be thorough in your analysis."
        
        # Update system message if it exists
        if st.session_state["messages"] and st.session_state["messages"][0]["role"] == "system":
            st.session_state["messages"][0]["content"] = system_msg
        
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            chat_model = get_chat_model(model_choice)
            stream = chat_model(st.session_state["messages"])
            
            thinking_content, response_content, response_time = process_thinking_stream(stream, model_choice)
            
            # Save the complete response
            st.session_state["messages"].append({
                "role": "assistant", 
                "content": response_content, 
                "thinking": thinking_content,
                "response_time": response_time
            })

def main():
    """Main application function."""
    load_custom_css()
    create_header()
    
    # Sidebar configuration
    model_choice, reasoning_effort = create_sidebar()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    # Initialize chat input state if not exists
    if 'chat_input_disabled' not in st.session_state:
        st.session_state.chat_input_disabled = False
    
    with col1:
        # Put chat input in a container at the bottom
        chat_input_container = st.container()
        
        # First, show chat history
        display_chat_history()
        
        # Then, show the chat input below history
        with chat_input_container:
            if not st.session_state.chat_input_disabled:
                user_input = st.chat_input("Ask GPT-OSS anything... 🚀")
                if user_input:
                    st.session_state.chat_input_disabled = True
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.markdown(user_input)
                    
                    # Generate and display assistant response
                    with st.chat_message("assistant"):
                        chat_model = get_chat_model(model_choice)
                        stream = chat_model(st.session_state["messages"])
                        thinking_content, response_content, response_time = process_thinking_stream(stream, model_choice)
                        st.session_state["messages"].append({
                            "role": "assistant", 
                            "content": response_content, 
                            "thinking": thinking_content,
                            "response_time": response_time
                        })
                    st.session_state.chat_input_disabled = False
                    st.rerun()
    
    with col2:
        st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
        # Example prompts
        create_example_prompts()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model information
        st.markdown("""
        ### 🎯 About GPT-OSS
        
        GPT-OSS is OpenAI's first open-weight language model since GPT-2, featuring:
        
        - **Mixture-of-Experts**: Efficient parameter usage
        - **Chain-of-Thought**: Transparent reasoning process  
        - **Tool Use**: Web search, code execution, and more
        - **Safety Trained**: Robust safety measures
        - **Apache 2.0**: Fully open license
        
        **Performance Highlights:**
        - Matches GPT-4o-mini on many benchmarks
        - Outperforms proprietary models on health tasks
        - Excellent at competition mathematics
        - Strong coding capabilities
        """)

if __name__ == "__main__":
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are GPT-OSS, an advanced open-weight reasoning model. Use medium reasoning effort. Show your thinking process clearly."}
        ]
    
    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "messages": 0,
            "thinking_steps": 0,
            "avg_response_time": 0,
            "total_response_time": 0
        }
    
    main()
