from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta
import db
from admin import admin_bp
from user import user_bp #完成したら下の機能をそれぞれ持っていく。

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

# Blueprintを登録
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

#両方にある機能（index,ログアウト）
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')  
    else:
        return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


#管理者機能(ログイン,top,登録)

@app.route('/adminform')
def admin_form():
    return render_template('/admin/admin_login.html')

@app.route('/adminlogin', methods=['POST'])
def admin_login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if db.admin_login(mail,password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        return redirect(url_for('admintop'))
    else :
        error = 'ログインに失敗しました。'
        input_data = {
            'user_name': mail, 
            'password':password
            }
        return render_template('/admin/admin_login.html', error=error, data = input_data)


@app.route('/admintop', methods=['GET'])
def admin_top():
    if 'user' in session :
        return render_template('/admin/admin_top.html')
    else :
        return redirect(url_for('/admin/admin_login.html'))

    
@app.route('/newaccount')
def account_form():
    return render_template('admin_teacher_account')


@app.route('/newaccount.exe', methods=['POST'])
def account_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が未入力です'
        return render_template('/admin/teacher_new.html', error=error)
    
    if mail == '':
        error = 'メールアドレスが未入力です'
        return render_template('/admin/teacher_new.html', error=error)
    
    if password == '':
        error = 'パスワードが未入力です'
        return render_template('/admin/teacher_new.html', error=error)
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('/admin/account_new.html', error=error)  
 
 
  
#利用者機能(ログイン,top)

@app.route('/userform')
def user_form():
    return render_template('/user/user_login.html')

@app.route('/userlogin', methods=['POST'])
def user_login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if db.user_login(mail,password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        return redirect(url_for('usertop'))
    else :
        error = 'ログインに失敗しました。'
        input_data = {
            'mail': mail, 
            'password':password
            }
        return render_template('/user/user_login.html', error=error, data = input_data)


@app.route('/usertop', methods=['GET'])
def user_top():
    if 'user' in session :
        return render_template('/user/user_top.html')
    else :
        return redirect(url_for('/user/user_login.html'))


if __name__ == '__main__':
    app.run(debug=True)