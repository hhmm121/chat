// DOM元素
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// 示例问题
const exampleQuestions = [
    "什么是人工智能？",
    "Python如何连接数据库？",
    "解释量子计算的基本概念",
    "如何学习编程？",
    "写一首关于春天的短诗"
];

// 初始化应用
function initializeApp() {
    // 设置输入框高度自适应
    messageInput.addEventListener('input', adjustTextareaHeight);

    // 绑定发送按钮事件
    sendButton.addEventListener('click', sendMessage);

    // 绑定回车键发送事件
    messageInput.addEventListener('keydown', handleKeyDown);

    // 添加示例问题按钮
    createExampleButtons();
}

// 调整输入框高度
function adjustTextareaHeight() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight > 60 ? this.scrollHeight : 60) + 'px';
}

// 处理键盘事件
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 发送消息
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // 添加用户消息
    addMessage(message, 'user');

    // 显示"正在输入"指示器
    showTypingIndicator();

    // 清空输入框
    clearInput();

    // 发送到FastAPI后端
    sendToBackend(message);
}

// 添加消息到聊天框
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender + '-message');

    const now = new Date();
    const timeString = formatTime(now);

    messageDiv.innerHTML = createMessageHTML(content, sender, timeString);

    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 创建消息HTML
function createMessageHTML(content, sender, timeString) {
    const userInfo = {
        user: {
            name: "您",
            avatar: "https://ui-avatars.com/api/?name=用户&background=1976d2&color=fff",
            color: "#1976d2"
        },
        assistant: {
            name: "AI助手",
            avatar: "https://ui-avatars.com/api/?name=AI&background=f57c00&color=fff",
            color: "#f57c00"
        }
    };

    const info = userInfo[sender];

    return `
        <div class="message-header">
            <img src="${info.avatar}" alt="${info.name}">
            <span>${info.name}</span>
        </div>
        <div class="message-content">${content}</div>
        <div class="timestamp">${timeString}</div>
    `;
}

// 格式化时间
function formatTime(date) {
    return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
}

// 显示"正在输入"指示器
function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

// 隐藏"正在输入"指示器
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// 清空输入框
function clearInput() {
    messageInput.value = '';
    messageInput.style.height = '60px';
}

// 滚动到底部
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 发送请求到后端（流式处理）
function sendToBackend(message) {
    // 先添加一个空的AI助手消息div，后续流式填充内容
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.classList.add('message', 'assistant-message');
    const now = new Date();
    const timeString = formatTime(now);
    aiMessageDiv.innerHTML = createMessageHTML('', 'assistant', timeString);
    chatContainer.appendChild(aiMessageDiv);
    scrollToBottom();

    fetch('http://192.168.51.2:8002/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(async response => {
        if (!response.ok) {
            throw new Error('网络响应错误');
        }
        // 流式读取
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let result = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            result += chunk;
            // 实时更新AI助手消息内容
            const contentDiv = aiMessageDiv.querySelector('.message-content');
            if (contentDiv) {
                contentDiv.textContent = result;
            }
            scrollToBottom();
        }
        hideTypingIndicator();
    })
    .catch(handleError);
}

// 处理错误
function handleError(error) {
    hideTypingIndicator();
    addMessage(`抱歉，处理您的请求时出错: ${error.message}`, 'assistant');
}

// 创建示例问题按钮
function createExampleButtons() {
    const welcomeDiv = document.querySelector('.welcome-message');
    const examplesDiv = document.createElement('div');

    examplesDiv.classList.add('examples-container');

    exampleQuestions.forEach(question => {
        const btn = document.createElement('button');
        btn.classList.add('example-btn');
        btn.textContent = question;
        btn.addEventListener('click', () => {
            messageInput.value = question;
            sendMessage();
        });
        examplesDiv.appendChild(btn);
    });

    welcomeDiv.appendChild(examplesDiv);
}

// 当文档加载完成后初始化应用
document.addEventListener('DOMContentLoaded', initializeApp);