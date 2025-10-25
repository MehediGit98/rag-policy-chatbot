"""
Gradio Interface for RAG Policy Assistant
Optimized for Hugging Face Spaces deployment
"""

import gradio as gr
import os
import time
from pathlib import Path

# Set environment variable to disable telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from src.retrieval import RAGRetriever
from src.config import Config
from src.ingestion import DocumentIngestion

# Initialize configuration
config = Config()
config.print_config()

# Global retriever instance
rag_retriever = None


def initialize_system():
    """Initialize or load the RAG system."""
    global rag_retriever
    
    status_messages = []
    
    try:
        # Check if vector store exists
        chroma_path = Path(config.CHROMA_DIR)
        
        if not chroma_path.exists() or not any(chroma_path.iterdir()):
            status_messages.append("📦 Vector store not found. Building from scratch...")
            status_messages.append("⏳ This will take 2-3 minutes on first run...")
            
            # Build vector store
            ingestion = DocumentIngestion()
            ingestion.ingest_all()
            
            status_messages.append("✅ Vector store created successfully!")
        else:
            status_messages.append("✅ Found existing vector store")
        
        # Initialize retriever
        status_messages.append("🔧 Initializing RAG system...")
        rag_retriever = RAGRetriever()
        status_messages.append("✅ RAG system ready!")
        
        return True, "\n".join(status_messages)
        
    except Exception as e:
        error_msg = f"❌ Initialization failed: {str(e)}"
        status_messages.append(error_msg)
        return False, "\n".join(status_messages)


def format_response(result):
    """Format the response with citations."""
    answer = result.get('answer', 'No answer generated')
    citations = result.get('citations', [])
    
    # Build formatted response
    formatted = f"**Answer:**\n\n{answer}\n\n"
    
    if citations:
        formatted += "**📚 Sources:**\n\n"
        for citation in citations:
            source = citation.get('source', 'Unknown')
            snippet = citation.get('snippet', '')
            formatted += f"- **{source}**\n"
            formatted += f"  _{snippet}_\n\n"
    
    return formatted


def chat_interface(message, history):
    """Main chat interface function."""
    global rag_retriever
    
    if not rag_retriever:
        return "❌ System not initialized. Please refresh the page."
    
    if not message or not message.strip():
        return "⚠️ Please enter a question."
    
    try:
        # Get response from RAG system
        start_time = time.time()
        result = rag_retriever.query(message)
        latency = time.time() - start_time
        
        # Format response
        response = format_response(result)
        response += f"\n\n⏱️ _Response time: {latency:.2f}s_"
        
        return response
        
    except Exception as e:
        return f"❌ Error processing question: {str(e)}"


def create_interface():
    """Create the Gradio interface."""
    
    # Initialize system on startup
    print("🚀 Initializing RAG system...")
    success, init_message = initialize_system()
    print(init_message)
    
    if not success:
        print("⚠️ System initialization failed!")
    
    # Custom CSS for better styling
    custom_css = """
    .container {
        max-width: 900px;
        margin: auto;
    }
    .gradio-container {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    """
    
    # Create interface
    with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🤖 Company Policy Assistant
            
            Ask me anything about company policies! I can help you with:
            - 🏖️ PTO and vacation policies
            - 🏡 Remote work guidelines  
            - 💰 Expense reimbursement
            - 🔒 Security policies
            - 📅 Holiday schedules
            
            **Powered by:** Groq (Llama 3.1) + RAG
            """
        )
        
        # Chatbot interface
        chatbot = gr.Chatbot(
            label="Policy Assistant",
            height=500,
            show_label=False,
            avatar_images=(None, "🤖")
        )
        
        msg = gr.Textbox(
            label="Ask a question",
            placeholder="e.g., How many PTO days do employees get?",
            lines=2
        )
        
        with gr.Row():
            submit = gr.Button("Submit", variant="primary")
            clear = gr.Button("Clear")
        
        # Example questions
        gr.Examples(
            examples=[
                "How many PTO days do employees get?",
                "What is the remote work policy?",
                "How do I submit expense reports?",
                "What are the security requirements for passwords?",
                "When are the company holidays?"
            ],
            inputs=msg,
            label="Example Questions"
        )
        
        # System info in accordion
        with gr.Accordion("ℹ️ System Information", open=False):
            gr.Markdown(
                f"""
                **Configuration:**
                - LLM Model: {config.GROQ_MODEL}
                - Embedding Model: {config.EMBEDDING_MODEL}
                - Chunk Size: {config.CHUNK_SIZE}
                - Top-K Retrieval: {config.TOP_K}
                
                **Status:** {'✅ Ready' if success else '❌ Not Ready'}
                
                {init_message}
                """
            )
        
        # Event handlers
        def user_message(message, history):
            return "", history + [[message, None]]
        
        def bot_response(history):
            user_msg = history[-1][0]
            bot_msg = chat_interface(user_msg, history)
            history[-1][1] = bot_msg
            return history
        
        msg.submit(
            user_message, 
            [msg, chatbot], 
            [msg, chatbot], 
            queue=False
        ).then(
            bot_response,
            chatbot,
            chatbot
        )
        
        submit.click(
            user_message,
            [msg, chatbot],
            [msg, chatbot],
            queue=False
        ).then(
            bot_response,
            chatbot,
            chatbot
        )
        
        clear.click(lambda: None, None, chatbot, queue=False)
    
    return demo


if __name__ == "__main__":
    # Create and launch interface
    demo = create_interface()
    
    # Launch with appropriate settings for HF Spaces
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )