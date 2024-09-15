from aiogram import types
from loader import dp, db
from states.state import Register, MainMenu
from keyboards.default.markups import lang, uz, ru, eng, menu


@dp.message_handler(commands=['start'])
async def cm_start(message: types.Message):
    products_user_id = [i[0] for i in db.execute('select chat_id from products_user', fetchall=True)]
    if message.from_user.id in products_user_id:
        user_lang = db.execute('select lang from products_user where chat_id = ?',
                               parameters=(message.from_user.id,), fetchone=True)[0]
        if user_lang == uz:
            await message.answer(text='Bosh menyu', reply_markup=menu['uz'])
            await MainMenu.step_one_uz.set()
        elif user_lang == ru:
            await message.answer(text='Главное меню', reply_markup=menu['ru'])
            await MainMenu.step_one_ru.set()
        else:
            await message.answer(text='Main menu', reply_markup=menu['eng'])
            await MainMenu.step_one_eng.set()

    else:
        await message.answer(text="""
    Здравствуйте! Давайте для начала выберем язык обслуживания!
    
    Keling, avvaliga xizmat ko’rsatish tilini tanlab olaylik.
    
    Hi! Let's first we choose language of serving!""", reply_markup=lang)
        await Register.lang.set()
