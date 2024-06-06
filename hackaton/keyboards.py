from aiogram.types import (ReplyKeyboardMarkup,InlineKeyboardButton, KeyboardButton,InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Регистрация')]],resize_keyboard=True
    )
start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мои группы')],
    [KeyboardButton(text='Создать группу')]], resize_keyboard=True
    )

addComand = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мои группы')],
    [KeyboardButton(text='Создать группу')],
    [KeyboardButton(text='Расклады')]], resize_keyboard=True
    )

addUserAndTask= ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить участника в команду')],
    [KeyboardButton(text='Добавить задачу')]],
    resize_keyboard=True)

procComand=ReplyKeyboardMarkup(keyboard=[    [KeyboardButton(text='Добавить ещё')],
    [KeyboardButton(text='Сформировать группу')]],resize_keyboard=True
                )