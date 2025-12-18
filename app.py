import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from models import db, User, Workbench, Workspace, AppIcon

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    from config import ProductionConfig as ConfigClass
elif config_name == 'development':
    from config import DevelopmentConfig as ConfigClass
else:
    from config import DevelopmentConfig as ConfigClass

app = Flask(__name__)
app.config.from_object(ConfigClass)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global DEV_MODE for backward compatibility
DEV_MODE = app.config['DEV_MODE'] 

db.init_app(app)

with app.app_context():
    db.create_all()
    if DEV_MODE:
        if not User.query.filter_by(userid='dev_user').first():
            dev_user = User(userid='dev_user', name='Walter Dev', avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=Walter')
            db.session.add(dev_user)
            db.session.commit()

# --- Helpers ---

def get_current_user():
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def fetch_page_metadata(url):
    """Fetches title, description and icon from a URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ''
        if not title:
            # Try og:title
            og_title = soup.find("meta", property="og:title")
            title = og_title["content"] if og_title else urlparse(url).netloc

        description = ''
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc:
            description = meta_desc.get("content", "")

        # Try to find favicon
        icon_url = ''
        # 1. Check for link rel icon
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link:
            icon_url = urljoin(url, icon_link.get('href'))
        else:
            # 2. Fallback to /favicon.ico
            parsed_uri = urlparse(url)
            base_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            icon_url = urljoin(base_url, '/favicon.ico')
            
        return {'title': title.strip(), 'description': description.strip(), 'icon_url': icon_url}
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return {'title': '', 'description': '', 'icon_url': ''}

# --- Routes ---

@app.route('/login')
def login():
    if DEV_MODE:
        user = User.query.filter_by(userid='dev_user').first()
        session['user_id'] = user.id
        return redirect(url_for('index'))

    # Real WeCom OAuth2 Authorization
    redirect_uri = url_for('auth_callback', _external=True)
    appid = app.config['WECOM_CORPID']
    url = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    return redirect(url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    if not code:
        return "Authorization code not found", 400

    # Exchange code for access token
    token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={app.config['WECOM_CORPID']}&corpsecret={app.config['WECOM_SECRET']}"
    r_token = requests.get(token_url).json()

    if 'access_token' not in r_token:
        return f"Failed to get access token: {r_token}", 500

    access_token = r_token['access_token']

    # Get user info
    user_info_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={access_token}&code={code}"
    r_user = requests.get(user_info_url).json()

    if 'UserId' not in r_user:
        return f"Failed to get UserID: {r_user}", 500

    userid = r_user['UserId']

    # Get detailed user info
    detail_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={userid}"
    r_detail = requests.get(detail_url).json()

    if 'errcode' in r_detail and r_detail['errcode'] != 0:
        return f"Failed to get user details: {r_detail}", 500

    # Create or update user
    user = User.query.filter_by(userid=userid).first()
    if not user:
        user = User(userid=userid)
        db.session.add(user)

    user.name = r_detail.get('name', 'Unknown')
    user.avatar = r_detail.get('avatar', '')
    db.session.commit()

    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user = get_current_user()
    workbenches = Workbench.query.all()
    
    active_wb_id = request.args.get('active_wb_id', type=int)
    active_workbench = None
    
    if workbenches:
        if active_wb_id:
            active_workbench = Workbench.query.get(active_wb_id)
        if not active_workbench:
            active_workbench = workbenches[0]
            
    return render_template('index.html', user=user, workbenches=workbenches, active_workbench=active_workbench)

# --- API for Metadata ---
@app.route('/api/fetch-meta', methods=['POST'])
@login_required
def api_fetch_meta():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    data = fetch_page_metadata(url)
    return jsonify(data)

# --- CRUD Actions ---

@app.route('/workbench/new', methods=['POST'])
@login_required
def create_workbench():
    user = get_current_user()
    name = request.form.get('name')
    if name:
        wb = Workbench(name=name, owner=user)
        db.session.add(wb)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/workbench/<int:wb_id>/workspace/new', methods=['POST'])
@login_required
def create_workspace(wb_id):
    name = request.form.get('name')
    is_public = request.form.get('is_public') == 'on'
    if name:
        ws = Workspace(name=name, is_public=is_public, workbench_id=wb_id)
        db.session.add(ws)
        db.session.commit()
    return redirect(url_for('index', active_wb_id=Workbench.query.get(wb_id).id))

@app.route('/workspace/<int:ws_id>/app/new', methods=['POST'])
@login_required
def add_app(ws_id):
    name = request.form.get('name')
    description = request.form.get('description')
    url = request.form.get('url')
    icon_type = request.form.get('icon_type', 'url') # 'url' or 'upload'
    
    final_icon_url = ''
    
    # Handle File Upload
    if icon_type == 'upload' and 'icon_file' in request.files:
        file = request.files['icon_file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            # Add timestamp to prevent collision
            import time
            filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final_icon_url = url_for('static', filename=f"uploads/{filename}")
    else:
        # Handle URL
        final_icon_url = request.form.get('icon_url')
    
    if name and url:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        app_icon = AppIcon(
            name=name, 
            description=description,
            url=url, 
            icon_url=final_icon_url, 
            icon_type=icon_type,
            workspace_id=ws_id
        )
        db.session.add(app_icon)
        db.session.commit()
        
    # Redirect back to the workbench that owns this workspace
    ws = Workspace.query.get(ws_id)
    return redirect(url_for('index', active_wb_id=ws.workbench_id))

@app.route('/app/visit/<int:app_id>')
@login_required
def visit_app(app_id):
    app_icon = AppIcon.query.get_or_404(app_id)
    app_icon.visits += 1
    db.session.commit()
    return redirect(app_icon.url)

@app.route('/app/update/<int:app_id>', methods=['POST'])
@login_required
def update_app(app_id):
    app_icon = AppIcon.query.get_or_404(app_id)
    ws = Workspace.query.get(app_icon.workspace_id)
    
    # Simple permission check (in real app, should be more robust)
    # Allow if user is owner of workbench OR user created it (if we tracked creator)
    # For now, we allow workbench owner or any member of workspace (if we had that logic fully)
    # Let's stick to: Workbench Owner can edit everything. 
    if ws.workbench.owner_id != get_current_user().id:
         abort(403) 

    name = request.form.get('name')
    description = request.form.get('description')
    url = request.form.get('url')
    icon_type = request.form.get('icon_type', 'url')

    if name and url:
        app_icon.name = name
        app_icon.description = description
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        app_icon.url = url
        app_icon.icon_type = icon_type

        # Handle File Upload
        if icon_type == 'upload' and 'icon_file' in request.files:
            file = request.files['icon_file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                app_icon.icon_url = url_for('static', filename=f"uploads/{filename}")
        elif icon_type == 'url':
             new_icon_url = request.form.get('icon_url')
             # Update if provided (even if empty, to allow clearing) or keep old?
             # Let's say if user switches to URL type, they should provide URL or we keep old if it looks like a URL
             if new_icon_url is not None:
                 app_icon.icon_url = new_icon_url

        db.session.commit()
    
    return redirect(url_for('index', active_wb_id=ws.workbench_id))

@app.route('/app/delete/<int:app_id>')
@login_required
def delete_app(app_id):
    app_icon = AppIcon.query.get_or_404(app_id)
    ws_id = app_icon.workspace_id
    ws = Workspace.query.get(ws_id)
    db.session.delete(app_icon)
    db.session.commit()
    return redirect(url_for('index', active_wb_id=ws.workbench_id))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
