css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}
.chat-message:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}
.chat-message.user {
    background: linear-gradient(135deg, #1d3557, #457b9d);
    color: #f1faee;
}
.chat-message.bot {
    background: linear-gradient(135deg, #264653, #2a9d8f);
    color: #f1faee;
}
.chat-message .avatar {
    width: 60px;
    height: 60px;
    flex-shrink: 0;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
}
.chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.chat-message .message {
    flex: 1;
    font-size: 1rem;
    line-height: 1.5;
}
</style>
'''

bot_template = '''
<!-- Bot Message Template -->
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://scx2.b-cdn.net/gfx/news/hires/2019/3-robot.jpg" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<!-- User Message Template -->
<div class="chat-message user">
    <div class="avatar">
        <img src="https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
