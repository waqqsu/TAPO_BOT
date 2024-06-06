from aiogram.types import Message,CallbackQuery,ContentType
from aiogram.filters import CommandStart, Command
from aiogram import Router,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton, UNSET_PARSE_MODE
import hackaton.keyboards as kb
import requests, json
from aiogram import types
from hackaton.utils import *

router = Router()

class Register(StatesGroup):
    name = State()
    surname = State()
    birth_date = State()
    psychotype = State()
    about = State()

from aiogram import types

@router.message(F.text == "Мои группы")
async def get_user_project(message: types.Message):
    user_id = message.from_user.id
    response = requests.get(f'http://127.0.0.1:5000/projects/user/{user_id}')
    
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Пересобрать группу", callback_data=f"add_user_{project['project_id']}")]
            ])
            users = ""
            for i in project["users"]:
                users += f"👤 {i['firstname']} {i['secondname']}\n"+\
                f"🔹описание: {i['description']}\n" +\
                f"🔹психотип {i['psychotype']}\n" +\
                f"🔹знак зодиака {i['zodiac']}\n" +\
                f"⭐️Расклад:{i['prediction']}" +\
                "\n\n\n"
            await message.answer(
                f"Проект: {project['project_name']}\n" +
                f"Описание: {project['description']}\n"+
                f"Средняя совместимость знаков: {project['avg_zodiac']}%\n" +
                f"Минимальная совместимость знаков: {project['min_zodiac']}%\n" +
                f"Наименее совместимая пара знаков: {project['min_pair_zodiac']}\n" +
                f"Участники:" +
                users,

                reply_markup=keyboard
            )
    else:
        await message.answer("Ошибка при получении списка групп.")

@router.callback_query(F.data.startswith("add_user_"))
async def show_group_details(callback_query: types.CallbackQuery, state: FSMContext):
    user_tg_id = callback_query.data.split("_")[2]
    storage = await state.get_data()
    print(storage)
    response = requests.post(f"http://localhost:5000/projects/{int(storage['current_project_id'])}/add_user", json={"user_id":user_tg_id})
    print(response.json)
    if response.status_code == 200:
        await callback_query.message.answer(
            "Пользователь успешно добавлен",
            reply_markup=kb.procComand
        )
        print(f"user_tg_id {user_tg_id} 63 строка")
        storage['current_user_ids'].append(user_tg_id)
        await state.update_data(current_users_id=storage['current_user_ids'])
    else:
        await callback_query.message.answer("Ошибка при добавлении юзера.")
    await callback_query.answer()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    response = requests.get('http://localhost:5000/users/'+ str(message.from_user.id))
    print(response.json)
    tg_id = message.from_user.id
    print(tg_id)
    print(type(tg_id))
    # if str(tg_id) in ['1026910141']:
    if(response.status_code == 200 or response.status_code==201):
        await message.answer('Привет, какие планы на сегодня?', reply_markup=kb.addComand)
    else:
        await state.set_state(Register.name)
        await message.answer("Привет! 👋\n\n"
            "Я твой новый помощник в формировании идеальных команд для работы над проектами! 🚀\n\n"
            "Здесь ты можешь:\n"
            "🔍 Найти подходящих специалистов по навыкам и опыту\n"
            "🤝 Создать эффективные команды, готовые к любым вызовам\n"
            "📈 Улучшить координацию и производительность проектов\n\n")
        await message.answer('Пожалуйста пройдите регистрацию.\n\nВведите ваше имя:')
    # else:

    #     youtube_button = InlineKeyboardButton(text="Открыть", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    #     # Create the markup
    #     inline_kb = InlineKeyboardMarkup(inline_keyboard=[[youtube_button]])

    #     # Send the message with the inline keyboard
    #     await message.answer('Звезды сегодня неблагоспокойны, бот открыт только достойнымы', reply_markup=inline_kb)

@router.message(F.text == 'Регистрация')
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.surname)
    await message.answer('Введите вашу фамилию')

@router.message(Register.surname)
async def register_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Register.birth_date)
    await message.answer('Введите вашу дату рождения')

    
@router.message(Register.birth_date)
async def register_birthdate(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await state.set_state(Register.about)
    await message.answer('Расскажите пару слов о себе')

@router.message(Register.about)
async def register_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(Register.psychotype)
    await message.answer('Введите ваш психотип')

@router.message(Register.psychotype)
async def register_psychotype(message: Message, state: FSMContext):
    await state.update_data(psychotype=message.text)
    telegramId=message.from_user.id
    data = await state.get_data()

    comandList={'telegram_id':telegramId, 'firstname':data["name"], "description":data["about"],
                'secondname':data["surname"], 'psychotype':data["psychotype"],
                "birth_date": data["birth_date"]}
    
    url='http://127.0.0.1:5000/users'
    response = requests.post(url,json=comandList)
    if (response.status_code == 200 or response.status_code == 201):  # Успешное создание ресурса
        response = requests.get(f"http://localhost:5000/users/{telegramId}")
        user = response.json()
        user_str = f"👤 {user['firstname']} {user['secondname']}\n"+\
                f"🔹описание: {user['description']}\n" +\
                f"🔹психотип {user['psychotype']}\n" +\
                f"🔹знак зодиака {user['zodiac']}\n" +\
                f"⭐️Расклад: {user['prediction']}"
        await message.answer(user_str,reply_markup=kb.addComand)
    else:
        await message.answer(f'Ошибка при добавлении юзера: {response.status_code}')

    await state.clear()


class Comand(StatesGroup):
    comand_name=State()
    description=State()
    current_group=State()
    
@router.message(F.text == 'Создать группу')
async def register(message: Message, state: FSMContext):
    await state.set_state(Comand.comand_name)
    await message.answer('Введите название команды')


@router.message(Comand.comand_name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(comand_name=message.text)
    await state.set_state(Comand.description)
    await message.answer('Введите примечания')

@router.message(Comand.description)
async def register_group(message: Message, state: FSMContext):
    tg_id=message.from_user.id
    
    await state.update_data(description=message.text)
    data = await state.get_data()
    comandList={'project_name':data["comand_name"], 'description':data["description"],'sender_tg_id':tg_id}
    await state.clear()
    await state.update_data(current_user_ids=[tg_id])
    
    
    
    url='http://localhost:5000/projects'
    response =requests.post(url,json=comandList)
    data = response.json()
    project_id = data['project_id']
    await state.update_data(current_project_id=project_id)
    storage = await state.get_data()
    if (response.status_code == 200 or response.status_code == 201):  # Успешное создание ресурса
        response = requests.get("http://127.0.0.1:5000/users/all")
        data = response.json()
        print(data)
        print(tg_id)
        for user in data:
            if user['telegram_id'] != str(tg_id):
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Добавить участника", callback_data=f"add_user_{user['telegram_id']}")]
                ])

                await message.answer(
                    f"👤 {user['firstname']} {user['secondname']}\n"+
                    f"🔹описание: {user['description']}\n" +
                    f"🔹психотип {user['psychotype']}\n" +
                    f"🔹знак зодиака {user['zodiac']}\n" +
                    f"⭐️Расклад: {user['prediction']}",

                    reply_markup=keyboard
                )
        await message.answer("Добавьте участников к вашей группе"
                             , reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Сформировать группу')]],resize_keyboard=True
                )
                )
        

    else:
        await message.answer(f'Ошибка при добавлении проекта: {response.status_code}\n{response.json()}')
    

@router.message(F.text == "Сформировать группу")
async def sf_group(message: Message, state: FSMContext):
    print("ok")
    tg_id=message.from_user.id
    storage = await state.get_data()
    response = requests.get(f"http://localhost:5000/projects/user/{tg_id}")
    data = response.json()
    project = [d for d in data if d['project_id'] == storage['current_project_id']][0]
    print(project)
    users = ""
    for i in project["users"]:
        users += f"👤 {i['firstname']} {i['secondname']}\n"+ \
            f"🔹описание: {i['description']}\n" + \
            f"🔹психотип {i['psychotype']}\n" + \
            f"🔹знак зодиака {i['zodiac']}\n"+\
            f"⭐️Расклад: {i['prediction']}\n\n\n" 
    await message.answer(
        f"📋Проект: {project['project_name']}\n" +
        f"📝Описание: {project['description']}\n"+
        f"🔮Средняя совместимость знаков: {project['avg_zodiac']}%\n" +
        f"⚠️Минимальная совместимость знаков: {project['min_zodiac']}%\n" +
        f"⚡️Наименее совместимая пара знаков: {project['min_pair_zodiac']}\n" +
        f"👥Участники:" +
        users,

        reply_markup=kb.addComand
    )
@router.message(F.text == "Добавить ещё")
async def current_group(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    tg_id=message.from_user.id
    storage = await state.get_data()

    response = requests.get("http://127.0.0.1:5000/users/all")
    data = response.json()

    for user in data:
        if user['telegram_id'] != str(tg_id):
            if user['telegram_id'] in storage['current_user_ids']:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Убрать участника", callback_data=f"remove_user_{user['telegram_id']}")]
            ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Добавить участника", callback_data=f"add_user_{user['telegram_id']}")]
                ])

            await message.answer(
                f"👤 {user['firstname']}{user['secondname']}\n"+ \
                f"🔹описание: {user['description']}\n" + \
                f"🔹психотип {user['psychotype']}\n" + \
                f"🔹знак зодиака {user['zodiac']}\n"+\
                f"⭐️Расклад: {user['prediction']}",

                reply_markup=keyboard
            )
    await message.answer("Добавьте участников к вашей группе", reply_markup=kb.procComand)

@router.message(F.text == 'Расклады')
async def prediction(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Общее", callback_data="prediction_Общее")],
                    [InlineKeyboardButton(text="Здоровье", callback_data="prediction_Здоровье")],
                    [InlineKeyboardButton(text="Прошлое, настоящее, будущее", callback_data="prediction_Прошлое, настоящее, будущее")],
                    [InlineKeyboardButton(text="Любовь", callback_data="prediction_Любовь")],
                    [InlineKeyboardButton(text="Карьера, деньги", callback_data="prediction_Карьера, деньги")]
                ])
    await message.answer("Выберите расклад:", reply_markup= keyboard)

@router.callback_query(F.data.startswith("prediction_"))
async def show_group_details(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        prediction = callback_query.data.split("_")[1]
    except(IndexError, ValueError):
        await callback_query.message.answer("Неверный формат данных." + callback_query.data)
        return
    response = requests.get(f"http://localhost:5000/prediction/{prediction}")
    if response.status_code == 200:
        data = response.json()
        print(data[0])
        await callback_query.message.answer(f"{data[0]['cards_msg']}\n\n{data[0]['prediction']}")
    else:
        await callback_query.message.answer("Ошибка при тусовки колоды.")
    await callback_query.answer()