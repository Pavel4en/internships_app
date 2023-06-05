from app import app, mail
from flask import render_template, request, redirect, session, jsonify, flash
import smtplib
from email.mime.text import MIMEText
import sqlite3
from datetime import datetime
from flask_mail import Message

def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)

def get_db_connection():
    conn = sqlite3.connect('inter.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    if session.get('user_id'):
        return render_template('index.html')
    else:
        return render_template('index.html')

#Карточки с заказчиками 
@app.route('/clients')
def clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    clients = cursor.fetchall()
    conn.close()
    return render_template('clients_card.html', clients=clients)
#Карточки со стажерами
@app.route('/trainees')
def trainees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trainee")
    trainees = cursor.fetchall()
    conn.close()
    return render_template('trainees_card.html', trainees=trainees)

@app.route('/logout')
def logout():
    session.clear()  
    return redirect('/')  


@app.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверка, существует ли уже пользователь с таким логином
        query = "SELECT * FROM Client WHERE Client_login = ?"
        cursor.execute(query, (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Пользователь с таким логином уже существует"
            return render_template('client.html', error_message=error_message)

        # Добавление нового пользователя в таблицу Client
        query = "INSERT INTO Client (Client_login, Client_pas, Client_name, Client_surname, Client_patronymic) " \
                "VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (login, password, name, surname, patronymic))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template('client.html')

@app.route('/register/intern', methods=['GET', 'POST'])
def register_intern():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверка, существует ли уже пользователь с таким логином
        query = "SELECT * FROM Trainee WHERE Trainee_login = ?"
        cursor.execute(query, (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Пользователь с таким логином уже существует"
            return render_template('Trainee.html', error_message=error_message)

        # Добавление нового пользователя в таблицу Trainee
        query = "INSERT INTO Trainee (Trainee_login, Trainee_pas, Trainee_name, Trainee_surname, Trainee_patronymic) " \
                "VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (login, password, name, surname, patronymic))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template('Trainee.html')

# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user_type = request.form['user_type']  # "customer" для заказчика, "intern" для стажера

        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверка логина и пароля в соответствующей таблице
        if user_type == "customer":
            query = "SELECT * FROM Client WHERE Client_login = ? AND Client_pas = ?"
        elif user_type == "intern":
            query = "SELECT * FROM Trainee WHERE Trainee_login = ? AND Trainee_pas = ?"

        cursor.execute(query, (login, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Успешная авторизация, сохранение данных в сессии
            session['user_id'] = user[0]
            session['user_type'] = user_type
            return redirect('/dashboard')  # Перенаправление на страницу с данными пользователя
        else:
            error_message = "Неверный логин или пароль"
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

# Страница с данными пользователя
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']

        conn = get_db_connection()
        cursor = conn.cursor()

        if user_type == "customer":
            query = "SELECT * FROM Client WHERE Client_id = ?"
        elif user_type == "intern":
            query = "SELECT * FROM Trainee WHERE Trainee_id = ?"

        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return render_template('dashboard.html', user=user)

    return redirect('/login')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']

        conn = get_db_connection()
        cursor = conn.cursor()

        if user_type == "customer":
            if request.method == 'POST':
                surname = request.form['surname']
                name = request.form['name']
                patronymic = request.form['patronymic']
                organization = request.form['organization']
                about_organization = request.form['about_organization']

                query = "UPDATE Client SET Client_surname = ?, Client_name = ?, Client_patronymic = ?, " \
                        "Client_organization = ?, Client_aboutOrganisation = ? WHERE Client_id = ?"
                cursor.execute(query, (surname, name, patronymic, organization, about_organization, user_id))
                conn.commit()

                return redirect('/dashboard')

            query = "SELECT * FROM Client WHERE Client_id = ?"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return render_template('edit_dashboard.html', user=user)

        elif user_type == "intern":
            if request.method == 'POST':
                surname = request.form['surname']
                name = request.form['name']
                patronymic = request.form['patronymic']
                age = request.form['age']
                phone = request.form['phone']
                speciality = request.form['speciality']
                competencies = request.form['competencies']
                wishes = request.form['wishes']
                experience = request.form['experience']
                position = request.form['position']
                about_me = request.form['about_me']

                query = "UPDATE Trainee SET Trainee_surname = ?, Trainee_name = ?, Trainee_patronymic = ?, " \
                        "Trainee_age = ?, Trainee_phone = ?, Trainee_speciality = ?, Trainee_competencies = ?, " \
                        "Trainee_wishes = ?, Trainee_experience = ?, Trainee_position = ?, Trainee_aboutMe = ? " \
                        "WHERE Trainee_id = ?"
                cursor.execute(query, (surname, name, patronymic, age, phone, speciality, competencies, wishes,
                                       experience, position, about_me, user_id))
                conn.commit()

                return redirect('/dashboard')

            query = "SELECT * FROM Trainee WHERE Trainee_id = ?"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return render_template('edit_dashboard.html', user=user)

    return redirect('/login')

#Фильтр заказчиков для стажеров
@app.route('/get_customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)

@app.route('/filter_customers', methods=['GET'])
def filter_customers():
    name = request.args.get('name')
    organization = request.args.get('organization')
    rating = request.args.get('rating')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Client WHERE 1=1"

    if name:
        query += " AND (Client_surname LIKE ? OR Client_name LIKE ? OR Client_patronymic LIKE ?)"
    if organization:
        query += " AND Client_organization LIKE ?"
    if rating:
        query += " AND Client_rate = ?"

    values = ['%' + name + '%' if name else None,
              '%' + name + '%' if name else None,
              '%' + name + '%' if name else None,
              '%' + organization + '%' if organization else None,
              rating if rating else None]

    cursor.execute(query, values)
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)

#Полная инфа по стажировке из карточки
@app.route('/internship/<int:internship_id>')
def internship(internship_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Получение информации о стажировке по идентификатору
    query = "SELECT * FROM Traineeship WHERE Traineeship_id = ?"
    cursor.execute(query, (internship_id,))
    internship = cursor.fetchone()

    # Получение информации о заказчике
    query = """
        SELECT C.*
        FROM Client C
        INNER JOIN ClientTraineeship CT ON C.Client_id = CT.Client_id
        WHERE CT.Traineeship_id = ?
    """
    cursor.execute(query, (internship_id,))
    client = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('internship.html', internship=internship, client=client)






    




@app.route('/internships')
def internships():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Получение списка стажировок
    query = "SELECT * FROM Traineeship"
    cursor.execute(query)
    internships = cursor.fetchall()

    cursor.close()
    conn.close()

    # Проверка типа пользователя
    user_type = session.get('user_type')

    return render_template('board.html', internships=internships, user_type=user_type)

@app.route('/create_internship', methods=['GET', 'POST'])
def create_internship():
    if request.method == 'POST':
        # Получение данных формы создания стажировки
        name = request.form['name']
        description = request.form['description']
        # Дополнительные поля и данные формы
        internship_type = request.form['type']
        pasport = request.form['pasport']
        level = request.form['level']
        
        # Получение ID заказчика из сессии
        client_id = session.get('user_id')

        # Создание новой стажировки в базе данных
        conn = get_db_connection()
        cursor = conn.cursor()

        # Вставка стажировки
        query = "INSERT INTO Traineeship (Traineeship_name, Traineeship_type, Traineeship_pasport, Traineeship_description, Traineeship_level) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (name, internship_type, pasport, description, level))
        
        # Получение ID стажировки
        internship_id = cursor.lastrowid
        
        # Вставка связи заказчика и стажировки
        query = "INSERT INTO ClientTraineeship (Traineeship_id, Client_id) VALUES (?, ?)"
        cursor.execute(query, (internship_id, client_id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/internships')

    return render_template('create_card.html')




@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # Получение данных из формы
        sender_id = session['user_id']
        recipient_id = int(request.form['recipient_id'])
        message_text = request.form['message_text']

        # Сохранение сообщения в базе данных
        db = get_db_connection()
        db.execute('INSERT INTO Message (Sender_id, Recipient_id, Text) VALUES (?, ?, ?)',
                   (sender_id, recipient_id, message_text))
        db.commit()
        db.close()

        return redirect('/chat')

    else:
        # Получение списка пользователей для выбора получателя сообщения
        db = get_db_connection()
        users = db.execute('SELECT * FROM Client').fetchall()
        db.close()

        # Получение списка отправленных и принятых сообщений из базы данных
        db = get_db_connection()
        sent_messages = db.execute('SELECT * FROM Message WHERE Sender_id = ?', (session['user_id'],)).fetchall()
        received_messages = db.execute('SELECT * FROM Message WHERE Recipient_id = ?', (session['user_id'],)).fetchall()
        db.close()

        return render_template('chat.html', users=users, sent_messages=sent_messages, received_messages=received_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender_id = session['user_id']
    recipient_id = int(request.form['recipient_id'])
    message_text = request.form['message_text']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Сохранение сообщения в базе данных
    db = get_db_connection()
    db.execute('INSERT INTO Message (Sender_id, Recipient_id, Timestamp ,Text_message) VALUES (?, ?, ?, ?)',
               (sender_id, recipient_id, timestamp, message_text))
    db.commit()
    db.close()

    return redirect('/chat')

@app.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        db = get_db_connection()
        sent_messages = db.execute('SELECT * FROM Message WHERE Sender_id = ?', (session['user_id'],)).fetchall()
        received_messages = db.execute('SELECT * FROM Message WHERE Recipient_id = ?', (session['user_id'],)).fetchall()
        db.close()

        data = {
            'sent_messages': [dict(message) for message in sent_messages],
            'received_messages': [dict(message) for message in received_messages]
        }

        return jsonify(data)

    except Exception as e:
        print(str(e))
        return 'Error', 500

@app.route('/get_chat', methods=['GET'])
def get_chat():
    recipient_id = request.args.get('recipient_id')
    db = get_db_connection()

    # Выполняем запрос к базе данных
    messages = db.execute('SELECT * FROM Message WHERE Recipient_id = ?', (recipient_id,)).fetchall()
    
    # Преобразуем результат запроса в список словарей
    messages_list = []
    for message in messages:
        message_dict = {
            'Sender_id': message['Sender_id'],
            'Recipient_id': message['Recipient_id'],
            'Text_message': message['Text_message'],
            'Timestamp': message['Timestamp']
        }
        messages_list.append(message_dict)

    # Возвращаем сообщения в формате JSON
    return jsonify(messages=messages_list)


def get_internship_and_client_info(client_traineeship_id):
    conn = sqlite3.connect('inter.sqlite3')  # Замените 'your_database.db' на имя вашей базы данных SQLite
    cursor = conn.cursor()

    query = '''
    SELECT Traineeship.Traineeship_name, Traineeship.Traineeship_description, Client.Client_name, Client.Client_email
    FROM ClientTraineeship
    JOIN Traineeship ON ClientTraineeship.Traineeship_id = Traineeship.Traineeship_id
    JOIN Client ON ClientTraineeship.Client_id = Client.Client_id
    WHERE ClientTraineeship.ClientTraineeship_id = ?
    '''

    cursor.execute(query, (client_traineeship_id,))
    result = cursor.fetchone()

    conn.close()

    return result

@app.route('/submit_application', methods=['POST'])
def submit_application():
    internship_id = request.form['internship_id']
    client_id = request.form['client_id']
    
    # Получите информацию о стажировке и заказчике на основе идентификаторов
    internship_info = get_internship_and_client_info(client_id)
    internship_name = internship_info[0]
    internship_description = internship_info[1]
    client_name = internship_info[2]
    client_email = internship_info[3]
    
    # Отправка письма
    sender_email = 'birzha.stazher@yandex.ru'
    recipient_email = client_email
    message = f"Subject: Заявка на стажировку\n\nСтажер желает пройти стажировку.\n\nНазвание стажировки: {internship_name}\nОписание стажировки: {internship_description}\nЗаказчик: {client_name}"
    
    with smtplib.SMTP('imap.yandex.ru', 465) as smtp:
        smtp.starttls()
        smtp.login(sender_email, '123456789birzha')  
        smtp.sendmail(sender_email, recipient_email, message)
    
    return 'Заявка отправлена'


# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.pop('user_type', None)
#     return redirect('/login')


