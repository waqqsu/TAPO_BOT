from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from g4f.client import Client

from itertools import combinations_with_replacement

from datetime import datetime

from taro_prediction.gen_predict import gen_prediction
# experts = [
#     {
#         'telegram_id':10
#         'firstname':'Денис',
#         'secondname':'Газукин',
#         'description':'Основатель Expensivematiq',
#         'psychotype':'ИХ НЕТ!',
#         'birth_date':??
#     },
#     {
#         'telegram_id':11
#         'firstname':'Дмитрий',
#         'secondname':'Лоднев',
#         'description':'Технический директор Expensivematiq',
#         'psychotype':'Сигма',
#         'birth_date':??
#     },
#     {
#         'telegram_id':12
#         'firstname':'Анна',
#         'secondname':'Жаркова',
#         'description':'Lead nokia developer',
#         'psychotype':'ДИПЛОМИРОВАННЫЙ Таролог',
#         'birth_date':??
#     },
#     {
#         'telegram_id':13
#         'firstname':'Алексей',
#         'secondname':'Воротынцев',
#         'description':'Специалист UI/UX/UY/UZ',
#         'psychotype':'Томас Шелби',
#         'birth_date':??
#     },
#     {
#         'telegram_id':14
#         'firstname':'Александр',
#         'secondname':'Комбаров',
#         'description':'СЕО, Пиротехник',
#         'psychotype':'Хлопушка по плечу',
#         'birth_date':??
#     },
#     {
#         'telegram_id':15
#         'firstname':'Роман',
#         'secondname':'Клиенко',
#         'description':'Моряк',
#         'psychotype':'Таск-хейтер',
#         'birth_date':??
#     }

# ]

def get_zodiac_sign(birthdate):
    # Словарь с диапазонами дат для каждого знака зодиака на русском языке
    zodiac_signs = {
        'Козерог': [(1, 1), (1, 19)],
        'Водолей': [(1, 20), (2, 18)],
        'Рыбы': [(2, 19), (3, 20)],
        'Овен': [(3, 21), (4, 19)],
        'Телец': [(4, 20), (5, 20)],
        'Близнецы': [(5, 21), (6, 20)],
        'Рак': [(6, 21), (7, 22)],
        'Лев': [(7, 23), (8, 22)],
        'Дева': [(8, 23), (9, 22)],
        'Весы': [(9, 23), (10, 22)],
        'Скорпион': [(10, 23), (11, 21)],
        'Стрелец': [(11, 22), (12, 21)],
        'Козерог2': [(12, 22), (12, 31)]  # Для Козерога, охватывающего конец декабря
    }

    for sign, (start, end) in zodiac_signs.items():
        start_date = datetime(birthdate.year, start[0], start[1]).date()
        end_date = datetime(birthdate.year, end[0], end[1]).date()

        if start_date <= birthdate <= end_date:
            return sign if sign != 'Козерог2' else 'Козерог'

    return None  # Если дата не попадает в известные диапазоны
import random

def random_prediction():
    predictions = [
        "На этой неделе: ковыряйте код, а не кофейную гущу.",
        "Вас ждёт: переполненная почта и куча багов.",
        "Завтра: внезапный бой с непонятной ошибкой.",
        "Сегодня: капризная машина, обновите драйверы.",
        "Ближайшие дни: терпимость, сервер упорствует в неподчинении.",
        "Пятница: встреча с кодом в стиле 'понял, но не принял'.",
        "Вперёд: расследование исчезающей ветки на GitHub.",
        "За кулисами: серверы жалуются на перегрев.",
        "Не паникуйте: крашнулась не база данных, а кофемашина.",
        "Сюрприз: начальство потребует 'ещё немного дополнений'.",
        "Завтра: битва с бесконечными коммитами на Bitbucket.",
        "Внимание: бэкапы — ваш лучший друг на выходных.",
        "Понедельник: погружение в мир 'почему не работает'.",
        "Срочно: деплой срывается, вы виновны в коде.",
        "Сегодня: баг, который вам приснился ночью возникнет на деплое.",
        "На горизонте: миграция данных и тёмные облака.",
        "Вечер: кризис идентичности — забыли пароль от сервера.",
        "Завтрашний день: апокалипсис DNS и ночь без сна.",
        "Не забудьте: дисциплина в git — ваше спасение.",
        "Успешно: код прошёл тестирование на миллион багов.",
        "Сегодня: митинг, где обсуждаются обсуждения о проекте, вы ничего не поймете.",
        "Неделя начинается: погружаемся в океан merge conflict.",
        "Будьте готовы: обновление OS на всех девайсах.",
        "Внимание: совещание с директором об отпуске IT.",
        "Срочно: кофе и новые решения для перегруженного сервера.",
        "Сегодня: кризис с контроллером версий и кривыми скриптами.",
        "Завтра: ковыряние в коде, вечная гонка с временем.",
        "Будущее: AI заменит все рутинные задачи, подготовьтесь.",
        "Пятница: намёк на пиво за успешную неделю.",
        "Сегодня: изучение нового фреймворка и куча чаепитий.",
        "Неделя начинается: смотрите внимательно в логи, там что-то есть.",
        "Важно: оттачиваем навыки управления проектом и чаем.",
        "Понедельник: гора задач и мало кофе, начнём с проблемы кофемашины.",
        "Сегодня: презентация нового продукта, держите пальцы крестиком.",
        "Не забывайте: чистый код — это не только стиль, но и уважение к коллегам.",
        "Будьте готовы: стыковка с новыми системами, адаптация — ваша вторая фамилия.",
        "Вперёд: обновление безопасности, не дайте хакерам шанса.",
        "Важно: ведём журнал изменений, чтобы не потеряться в кодовых потоках.",
        "Не забудьте: регулярные бэкапы, без них вы в полной темноте.",
        "Будущее: квантовые вычисления и сквозьневронные сети станут вашими новыми игрушками.",
        "Сегодня: тренировка скорости реакции на атаки, не дайте уснуть.",
        "Завтра: групповой код-ревью, готовьте аргументы.",
        "Внимание: планирование масштабирования, будущее — в расширении.",
        "На этой неделе: собеседование новых кандидатов, найдём аналитический мозг.",
        "Важно: обновление процессов разработки, остаться в прошлом — значит остаться позади.",
        "Сегодня: срочный фикс и запуск, у кого крепче нервы?",
        "Будьте готовы: дайджест новых технологий, времени учиться — нет.",
        "Вперёд: мониторинг новых уязвимостей, предупреждён — значит вооружён.",
        "Не забывайте: обратная связь от пользователей — ваш главный источник информации.",
        "Сегодня: релиз новой версии, ждём праздника или апокалипсиса.",
        "Завтра: внезапный скачок трафика, подготовьтесь к шторму.",
        "Сегодня: забавная опечатка в коде, смех гарантирован.",
        "Не забудьте: периодические обновления, безопасность важнее всего.",
        "Важно: дайджест последних технологических новинок, быть в тренде — значит быть впереди.",
        "На горизонте: стратегическое планирование, будущее вашей компании в ваших руках.",
        "Срочно: отчёт о прогрессе проекта, никаких мелочей, только факты.",
        "Сегодня: экстренное совещание, кто попал в исключение?",
        "Завтра: ввод новых технологий, смелость — ваше второе имя.",
        "Внимание: утечка данных, защита информации — наш приоритет.",
        "Не паникуйте: запланированное обновление, всё будет хорошо.",
        "Будьте готовы: неожиданный рост нагрузки, подготовьте серверы к бою.",
        "Важно: уточнение требований клиента, чтобы избежать недоразумений.",
        "На этой неделе: новый проект, новые вызовы, новые возможности.",
        "Сегодня: интенсивное тестирование, ошибки — ваш лучший учитель.",
        "Завтра: обновление безопасности, безопасность превыше всего.",
        "Внимание: запланированное обслуживание, подготовьтеся к небольшому перерыву.",
        "Не забудьте: регулярные резервные копии, лучше перебдеть, чем недобдеть.",
        "Срочно: поиск и устранение уязвимостей, бдительность — ваше оружие.",
        "Сегодня: встреча с заказчиком, слушайте внимательно, чтобы не пропустить детали.",
        "Завтра: анализ производительности, время выявить узкие места.",
        "На этой неделе: подготовка к выставке, демонстрация нашего технологического великолепия.",
        "Важно: обновление документации, ясность и полнота — ваш ключ к успеху.",
        "Сегодня: вдохновение, создайте что-то удивительное.",
        "Не забудьте: обучение новичков, передайте свой опыт следующему поколению.",
        "Будьте готовы: непредвиденные проблемы, главное — сохранять спокойствие.",
        "Внимание: предупреждение о возможном отключении электропитания, готовьтесь к переходу на резервные источники.",
        "Сегодня: тимбилдинг, объедините усилия, чтобы преодолеть трудности вместе.",
        "Завтра: обновление программного обеспечения, стабильность — ваш лучший друг.",
        "На этой неделе: стратегический анализ, планируйте долгосрочные цели и действия для их достижения."
    ]
    return random.choice(predictions)



def calculate_average_compatibility(zodiac_signs):
    # Словарь с процентами совместимости для каждой пары знаков зодиака
    compatibility = {
        ('Овен', 'Телец'): 70, ('Овен', 'Близнецы'): 80, ('Овен', 'Рак'): 60, 
        ('Овен', 'Лев'): 90, ('Овен', 'Дева'): 50, ('Овен', 'Весы'): 75, 
        ('Овен', 'Скорпион'): 65, ('Овен', 'Стрелец'): 85, ('Овен', 'Козерог'): 55, 
        ('Овен', 'Водолей'): 80, ('Овен', 'Рыбы'): 45, ('Овен', 'Овен'): 85,
        ('Телец', 'Близнецы'): 65, ('Телец', 'Рак'): 80, ('Телец', 'Лев'): 50, 
        ('Телец', 'Дева'): 85, ('Телец', 'Весы'): 60, ('Телец', 'Скорпион'): 75, 
        ('Телец', 'Стрелец'): 55, ('Телец', 'Козерог'): 90, ('Телец', 'Водолей'): 50, 
        ('Телец', 'Рыбы'): 70, ('Телец', 'Телец'): 80,
        ('Близнецы', 'Рак'): 55, ('Близнецы', 'Лев'): 80, ('Близнецы', 'Дева'): 60, 
        ('Близнецы', 'Весы'): 85, ('Близнецы', 'Скорпион'): 50, ('Близнецы', 'Стрелец'): 75, 
        ('Близнецы', 'Козерог'): 55, ('Близнецы', 'Водолей'): 90, ('Близнецы', 'Рыбы'): 60, 
        ('Близнецы', 'Близнецы'): 85,
        ('Рак', 'Лев'): 65, ('Рак', 'Дева'): 75, ('Рак', 'Весы'): 55, ('Рак', 'Скорпион'): 80, 
        ('Рак', 'Стрелец'): 60, ('Рак', 'Козерог'): 70, ('Рак', 'Водолей'): 50, 
        ('Рак', 'Рыбы'): 85, ('Рак', 'Рак'): 75,
        ('Лев', 'Дева'): 60, ('Лев', 'Весы'): 90, ('Лев', 'Скорпион'): 55, 
        ('Лев', 'Стрелец'): 85, ('Лев', 'Козерог'): 65, ('Лев', 'Водолей'): 75, 
        ('Лев', 'Рыбы'): 55, ('Лев', 'Лев'): 90,
        ('Дева', 'Весы'): 60, ('Дева', 'Скорпион'): 75, ('Дева', 'Стрелец'): 55, 
        ('Дева', 'Козерог'): 80, ('Дева', 'Водолей'): 65, ('Дева', 'Рыбы'): 70, 
        ('Дева', 'Дева'): 70,
        ('Весы', 'Скорпион'): 70, ('Весы', 'Стрелец'): 85, ('Весы', 'Козерог'): 55, 
        ('Весы', 'Водолей'): 80, ('Весы', 'Рыбы'): 60, ('Весы', 'Весы'): 85,
        ('Скорпион', 'Стрелец'): 60, ('Скорпион', 'Козерог'): 75, ('Скорпион', 'Водолей'): 55, 
        ('Скорпион', 'Рыбы'): 90, ('Скорпион', 'Скорпион'): 70,
        ('Стрелец', 'Козерог'): 60, ('Стрелец', 'Водолей'): 85, ('Стрелец', 'Рыбы'): 65, 
        ('Стрелец', 'Стрелец'): 85,
        ('Козерог', 'Водолей'): 55, ('Козерог', 'Рыбы'): 70, ('Козерог', 'Козерог'): 75,
        ('Водолей', 'Рыбы'): 75, ('Водолей', 'Водолей'): 80,
        ('Рыбы', 'Рыбы'): 70
    }

    # Инициализация переменных
    total_compatibility = 0
    count = 0
    min_compatibility = float('inf')
    min_pair = None

    # Получение всех возможных пар знаков зодиака, включая одинаковые
    for sign1, sign2 in combinations_with_replacement(zodiac_signs, 2):
        # Упорядочиваем пару знаков для корректного поиска в словаре
        pair = tuple(sorted((sign1, sign2)))
        if pair in compatibility:
            percent = compatibility[pair]
            total_compatibility += percent
            count += 1
            if percent < min_compatibility:
                min_compatibility = percent
                min_pair = pair

    # Проверка, чтобы избежать деления на ноль
    if count == 0:
        return 0, 0, None

    # Вычисление среднего процента совместимости
    average_compatibility = total_compatibility / count

    return average_compatibility, min_compatibility, min_pair

client = Client()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tarobot:tarobot777cards@localhost/tarobot'  # Update with your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    psychotype = db.Column(db.Text)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserProjectAssociation(db.Model):
    __tablename__ = 'user_project_association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.telegram_id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
    user = db.relationship(User, backref=db.backref("user_projects", cascade="all, delete-orphan"))
    project = db.relationship(Project, backref=db.backref("project_users", cascade="all, delete-orphan"))

with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        telegram_id=data['telegram_id'],
        firstname=data['firstname'],
        secondname=data['secondname'],
        description=data.get('description'),
        psychotype=data.get('psychotype'),
        birth_date=data['birth_date']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(telegram_id=user_id).first()
    return jsonify({
        'user_id': user.user_id,
        'telegram_id': user.telegram_id,
        'firstname': user.firstname,
        'secondname': user.secondname,
        'description': user.description,
        'psychotype': user.psychotype,
        'birth_date': user.birth_date.isoformat(),
        'created_at': user.created_at.isoformat(),
        'prediction': random_prediction(),
        "zodiac":get_zodiac_sign(user.birth_date)
    })

@app.route('/users/all', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [
        {
            'id': user.user_id,
            'telegram_id': user.telegram_id,
            'firstname': user.firstname,
            'secondname': user.secondname,
            'description': user.description,
            'psychotype': user.psychotype,
            'birth_date': str(user.birth_date),
            'created_at': str(user.created_at),
            'prediction': random_prediction(),
            'zodiac': get_zodiac_sign(user.birth_date)
        }
        for user in users
    ]
    return jsonify(user_list), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    user.telegram_id = data['telegram_id']
    user.firstname = data['firstname']
    user.secondname = data['secondname']
    user.description = data.get('description')
    user.psychotype = data.get('psychotype')
    user.birth_date = data['birth_date']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    new_project = Project(
        project_name=data['project_name'],
        description=data.get('description')
    )
    db.session.add(new_project)
    db.session.commit()
    
    if 'sender_tg_id' in data:
        user_id = data['sender_tg_id']
        
        user = User.query.filter_by(telegram_id=user_id).first()
        if user:
            association = UserProjectAssociation(user_id=user.telegram_id, project_id=new_project.project_id)
            db.session.add(association)
            db.session.commit()
            return jsonify({'message': 'Project created successfully and user added to project',"project_id":new_project.project_id}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'project_id': project.project_id,
        'project_name': project.project_name,
        'description': project.description,
        'created_at': project.created_at.isoformat()
    })

@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    project = Project.query.get_or_404(project_id)
    project.project_name = data['project_name']
    project.description = data.get('description')
    db.session.commit()
    return jsonify({'message': 'Project updated successfully'})

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'})

@app.route('/projects/<int:project_id>/add_user', methods=['POST'])
def add_user_to_project(project_id):
    data = request.json
    user_id = data['user_id']
    association = UserProjectAssociation(user_id=user_id, project_id=project_id)
    db.session.add(association)
    db.session.commit()
    return jsonify({'message': 'User added to project successfully'}), 200

@app.route('/zodiac', methods=['POST'])
def zodiac():
    data = request.json
    zodiacs = data["zodiacs"]
    proc, min_proc, min_pair = calculate_average_compatibility(zodiacs)
    d = {"procent":proc, "min_procent":min_proc, "min_pair":min_pair}
    return jsonify(d)

@app.route('/projects/user/<int:user_id>', methods=['GET'])
def get_user_projects(user_id):
    user = User.query.filter_by(telegram_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    result = []
    
    for association in user.user_projects:
        project = Project.query.get(association.project_id)
        project_users = UserProjectAssociation.query.filter_by(project_id=project.project_id).all()
        users = []
        zodiacs = []
        for project_user in project_users:
            user_info = User.query.filter_by(telegram_id=project_user.user_id).first()
            users.append({
                'user_id': user_info.user_id,
                'telegram_id': user_info.telegram_id,
                'firstname': user_info.firstname,
                'secondname': user_info.secondname,
                'description': user_info.description,
                'psychotype': user_info.psychotype,
                'birth_date': user_info.birth_date.isoformat(),
                'created_at': user_info.created_at.isoformat(),
                'prediction':random_prediction(),
                'zodiac':get_zodiac_sign(user_info.birth_date)
            })
            zodiacs.append(get_zodiac_sign(user_info.birth_date))
        proc, min_proc, min_pair = calculate_average_compatibility(zodiacs)
        result.append({
            'project_id': project.project_id,
            'project_name': project.project_name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'avg_zodiac': proc,
            'min_zodiac':min_proc,
            'min_pair_zodiac':min_pair,
            'users': users
        })
    
    return jsonify(result)

# prediction: "Общее", "Здоровье","Прошлое, настоящее, будущее", "Любовь", "Карьера, деньги"
@app.route('/prediction/<string:prediction>', methods=['GET'])
def get_prediction(prediction):
    prediction = gen_prediction(prediction)
    if prediction.choose_category() is not None:
        prediction.choose_category()
        prediction.random_cards()
        print()
        print()
        result = []
        result.append({
            'cards_msg': prediction.write_names(),
            'prediction': prediction.make_pred()
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

