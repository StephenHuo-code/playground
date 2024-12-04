import gradio as gr
import openai
import os
from pathlib import Path
import tempfile
import whisper
from moviepy.editor import VideoFileClip



# 初始化Whisper模型
whisper_model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """转录音频文件"""
    result = whisper_model.transcribe(audio_path)
    return result["text"]

def extract_audio_from_video(video_path):
    """从视频中提取音频"""
    video = VideoFileClip(video_path)
    audio = video.audio
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        audio.write_audiofile(temp_audio.name)
        audio_path = temp_audio.name
    
    video.close()
    audio.close()
    return audio_path

def process_message(message, history, audio=None, video=None):
    """处理不同类型的输入并返回GPT-4回复"""
    
    # 处理音频输入
    if audio is not None:
        message = transcribe_audio(audio)
    
    # 处理视频输入
    if video is not None:
        audio_path = extract_audio_from_video(video)
        message = transcribe_audio(audio_path)
        os.unlink(audio_path)  # 删除临时音频文件
    
    # 准备对话历史
    messages = []
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})
    
    # 调用GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    return response.choices[0].message.content

# 创建Gradio界面
with gr.Blocks() as demo:
    # 从环境变量获取OpenAI API密钥
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("请设置环境变量 'OPENAI_API_KEY'")

    chatbot = gr.Chatbot(height=400)
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(placeholder="输入文本消息...", label="文本输入")
            audio_input = gr.Audio(source="microphone", type="filepath", label="语音输入")
            video_input = gr.Video(label="视频输入")
    
    def respond(message, audio, video, history):
        bot_message = process_message(message, history, audio, video)
        history.append((message, bot_message))
        return "", None, None, history
    
    submit_btn = gr.Button("发送")
    submit_btn.click(
        respond,
        inputs=[text_input, audio_input, video_input, chatbot],
        outputs=[text_input, audio_input, video_input, chatbot]
    )

# 启动应用
if __name__ == "__main__":
    demo.launch() 