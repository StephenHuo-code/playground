
import gradio as gr

def welcome(name):
    return f"Welcome to Gradio, {name}!"

js_video_player = """
function createVideoPlayerJS() {

    var head = document.head;
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '//sf-unpkg.bytepluscdn.com/obj/byteplusfe-sg/sdk/@byteplus/veplayer/1.9.3/index.min.css';
    head.appendChild(link);

    var script = document.createElement('script');
    script.src = '//sf-unpkg.bytepluscdn.com/obj/byteplusfe-sg/sdk/@byteplus/veplayer/1.9.3/index.min.js';
    head.appendChild(script);

    // 创建一个容器来包含按钮和视频播放器
    var mainContainer = document.createElement('div');
    mainContainer.style.display = 'flex';
    mainContainer.style.flexDirection = 'column';
    mainContainer.style.alignItems = 'center';
    mainContainer.style.gap = '20px';
    mainContainer.style.marginBottom = '20px';

    // 创建按钮容器
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';

    // 创建按钮
    var button = document.createElement('button');
    button.innerText = 'Click Me';
    button.style.padding = '10px 20px';
    container.appendChild(button);

    // 使用事件监听器来响应按钮点击事件
    button.addEventListener('click', function() {
        alert('Hello World');
    });


    document.addEventListener('DOMContentLoaded', function() {
        var gradioButton = document.getElementById('gradio_button');
        if (gradioButton) {
            gradioButton.addEventListener('click', function() {
                window.gradio_btn_click_func();
            });
        }
    });

    // 创建视频容器
    var videoContainer = document.createElement('div');
    videoContainer.id = 'video';

    // 将按钮容器和视频容器添加到主容器
    mainContainer.appendChild(container);
    mainContainer.appendChild(videoContainer);

    // 将主容器添加到gradio容器中
    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(mainContainer, gradioContainer.firstChild);

    function createPlayer() {
        var playerSdk = new VePlayer({
            lang: 'en', 
            id: 'video',
            url: "https://veplayer-vod-cdn.bytepluscdn.com/8b4843dcb4ab445b1d6e2d45d398d50f/79748ff1/video/tos/sgcomm1/tos-sgcomm1-v-0ebc06aace7614ac-sg/oU6aVALegGFUtMus1hBAR4f9ierza8E7M782Ee/?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=9a5fba0195f54553a78f0b8d1d87b435%2F20240730%2F%2F%2Faws4_request&X-Amz-Date=20240730T064921Z&X-Amz-Expires=315360600&X-Amz-Signature=499aaabeeeb01a225cdee9633a085e848ac045756443f2347afe39551149eccc&X-Amz-SignedHeaders=host&X-Amz-SignedQueries=X-Amz-Algorithm%3BX-Amz-Credential%3BX-Amz-Date%3BX-Amz-Expires%3BX-Amz-SignedHeaders%3BX-Amz-SignedQueries%3BX-Amz-UriRange%3Bsgw-endpoint&X-Amz-UriRange=0%2C+92&sgw-endpoint=veplayer-vod-cdn.bytepluscdn.com",
            poster: "https://veplayer-cdn.bytepluscdn.com/tos-sgcomm1-v-0ebc06aace7614ac-sg/fedd3b2df3884fe6bf0f49f5e6579c44~tplv-vod-noop.image",
            width: 600,
            height: 400,
            vodLogOpts: {
                line_app_id: 562771,
                tag: 'normal'
            }
        });
        window.playerSdk = playerSdk;
    }
    script.onload = createPlayer;

    // 创建一个全局函数，可以从外部调用
    window.gradio_btn_click_func = function() {
        console.log('clicked');
        const currentTime = window.playerSdk.player.currentTime;
        console.log(currentTime);
        // 在这里添加你想要执行的其他操作
        return true; // 返回true表示事件处理成功
    };


    return 'VideoPlayer created';
}
"""

with gr.Blocks(title="额外播放器", js=js_video_player) as additional_player:
    with gr.Group():
        # 创建按钮
        button = gr.Button("点击我", elem_id="gradio_button")
        
        # 定义按钮点击事件的响应函数
        def on_button_click():
            print("按钮被点击了")
            return None
        
        # 将按钮点击事件绑定到响应函数，并添加 JavaScript 处理
        button.click(
            fn=None,
            inputs=None,
            outputs=None,
            js="() => {window.gradio_btn_click_func(); return []}"
        )
        
additional_player.launch()