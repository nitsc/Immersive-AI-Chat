import os
from flask import Flask, render_template, request, jsonify
import ollama

# 获取当前文件的目录，确保 Flask 正确找到 templates 文件夹
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

# 初始化历史记录
history = []

# 定义页面
@app.route('/')
def index():
    return render_template('index.html', history=history)

# 处理聊天请求
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = ollama.chat(
        model="qwen2:0.5b",
        messages=[{"role": "user", "content": user_input}]
    )
    bot_response = response['message']['content']
    print(bot_response)
    history.append({'you': user_input, 'human-like': bot_response})
    return jsonify({'response': bot_response})

# 清空历史记录
@app.route('/clear', methods=['POST'])
def clear():
    global history
    history = []
    return jsonify({'status': 'cleared'})

# 获取聊天历史记录
@app.route('/chat_history', methods=['GET'])
def chat_history():
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)
