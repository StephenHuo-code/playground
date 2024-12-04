# This is a Gradio app that integrates with OpenAI to create a chatbot.
import gradio as gr
from openai import OpenAI
import os


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the chat function
def chat_with_openai(message, history):
    # Convert history to the format OpenAI expects
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    print(history)
    print(message)
    # Add conversation history
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    
    # Add the new message
    messages.append({"role": "user", "content": message})

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",  # 使用 GPT-4 模型
        messages=messages,
        temperature=0.7,
        max_tokens=150,
    )
    # Extract the response text
    reply = response.choices[0].text.strip()
    # Return the response as a message
    return {"role": "assistant", "content": reply}

contents_chatbot = gr.Chatbot(
        placeholder="输入你的主题内容或上传音频文件",
        height=800,
        type="messages",
    )
# Create a Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chat_with_openai,
    chatbot=contents_chatbot, 
    type="messages",
    title="OpenAI Chatbot",
    multimodal=True,
)
demo.launch(show_error=True)

# Launch the interface