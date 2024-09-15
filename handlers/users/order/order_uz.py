from aiogram import types
from states.state import MainMenu, OrderState
from keyboards.default.markups import get_branches, back_uz, delivery
from keyboards.inline.inline import order_menu, product_markup, product_cb, basket_markup, order_cb
from aiogram.dispatcher import FSMContext
from loader import dp, db


@dp.message_handler(text='🏃 Olib ketish', state=MainMenu.step_two_uz)
async def order(message: types.Message):
    await message.answer(text="""
Qayerdasiz 👀?Agar lokatsiyangizni📍 yuborsangiz, sizga eng yaqin filialni aniqlaymiz""",
                         reply_markup=get_branches('uz', message.from_user.id, 'yes'))
    await OrderState.step_one_uz.set()


@dp.message_handler(lambda x: x.text in db.get_branches(x.from_user.id, 'uz'), state=OrderState.step_one_uz)
async def get_menu(message: types.Message, state: FSMContext):
    await state.update_data(branches=message.text)
    await message.answer(text=f'Tanlangan filial: {message.text}')
    await message.answer(text='Nimadan boshlaymiz?', reply_markup=order_menu())
    await OrderState.step_two_uz.set()


@dp.message_handler(lambda x: x.text not in db.get_branches(x.from_user.id,
                                                            'uz') and x.text != back_uz and x.text != '📍 Eng yaqin fillialni aniqlash',
                    state=OrderState.step_one_uz)
async def err(message: types.Message):
    await message.answer(text="""
    Qayerdasiz 👀?Agar lokatsiyangizni📍 yuborsangiz, sizga eng yaqin filialni aniqlaymiz""",
                         reply_markup=get_branches('uz', message.from_user.id, 'yes'))


@dp.message_handler(content_types='location', state=OrderState.step_one_uz)
async def location(message: types.Message):
    await message.answer(text='raxmat')


@dp.inline_handler(lambda x: x.query in db.get_category(), state=OrderState.step_two_uz)
async def inline_mode(inline: types.InlineQuery):
    msg = []
    sql = '''
select i.id, i.name, i.price, i.caption, i.photo from products_items as i
join products_category as c on i.category_id = c.id
where c.name = ?   
    '''
    for id, name, price, caption, photo in db.execute(sql=sql, parameters=(inline.query,), fetchall=True):
        msg.append(
            types.InlineQueryResultArticle(
                id=id,
                title=name,
                input_message_content=types.InputMessageContent(
                    message_text=name
                ),
                thumb_url=photo,
                description=caption
            )

        )
    msg.append(
        types.InlineQueryResultArticle(
            id=str('back'),
            title=back_uz,
            input_message_content=types.InputMessageContent(
                message_text="⬅️ Kategoriyaga"
            ),
            thumb_url='https://cdn.pixabay.com/photo/2017/06/20/14/55/icon-2423347_1280.png',
            description="Ortga qaytish uchun tugmani bosing"

        )

    )
    await inline.answer(results=msg, cache_time=0)
    await OrderState.step_three_uz.set()


@dp.message_handler(state=OrderState.step_three_uz)
async def get_items(message: types.Message):
    sql = '''
select id, name, photo, price, caption from products_items
where name = ?
    '''
    id, name, photo, price, caption = db.execute(sql=sql, parameters=(message.text,), fetchone=True)
    await message.answer_photo(photo=photo,
                               caption=f'{name}\n\n{caption}\n\nNarxi: {price}',
                               reply_markup=product_markup(id, 1))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.delete()


@dp.callback_query_handler(product_cb.filter(action='plus'), state=OrderState.step_three_uz)
@dp.callback_query_handler(product_cb.filter(action='minus'), state=OrderState.step_three_uz)
@dp.callback_query_handler(product_cb.filter(action='add'), state=OrderState.step_three_uz)
@dp.callback_query_handler(product_cb.filter(action='count'), state=OrderState.step_three_uz)
async def product(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    items_id = callback_data['id']
    count = int(callback_data['count'])
    action = callback_data['action']
    data = await state.get_data()
    print(data)
    if action == 'plus':
        count += 1
        sql = '''
        select  name,  price, caption from products_items
        where id = ?
            '''
        name, price, caption = db.execute(sql=sql, parameters=(items_id,), fetchone=True)

        mes = f'{name}\n\n{caption}\n\nNarxi: {price * count}'
        await call.message.edit_caption(mes, reply_markup=product_markup(items_id, count))

    elif action == 'minus':
        if count > 1:
            count -= 1
            sql = '''
                    select  name,  price, caption from products_items
                    where id = ?
                        '''
            name, price, caption = db.execute(sql=sql, parameters=(items_id,), fetchone=True)

            mes = f'{name}\n\n{caption}\n\nNarxi: {price * count}'
            await call.message.edit_caption(mes, reply_markup=product_markup(items_id, count))
        else:
            await call.answer(text='minum 1')

    elif action == 'count':
        await call.answer(text=f'{count}')

    else:
        sql = """
insert into products_basket(user_id, item_id, count)
values(?, ?, ?) 
        """
        db.execute(sql=sql, parameters=(call.from_user.id, items_id, count), commit=True)
        sql = 'select name from products_items where id = ?'
        items_name = db.execute(sql, parameters=(items_id,), fetchone=True)[0]
        sql = """
select sum(i.price * b.count)  from products_basket as b
join products_items as i on i.id = b.item_id
where b.user_id = ?
        
        """
        total_price = db.execute(sql=sql, parameters=(call.from_user.id,), fetchone=True)[0]
        await call.message.answer(text=f"Mahsulot: {items_name} savatga muvaffaqiyatli qo'shildi ✅")
        await call.message.answer(text=f"Tanlangan filial: {data['branches']}")
        await call.message.answer(text='Davom etamizmi? 😉', reply_markup=order_menu(total_price))
        await call.message.delete()
        await OrderState.step_two_uz.set()


@dp.message_handler(text=back_uz, state=OrderState.step_one_uz)
async def back_order(message: types.Message):
    await message.answer(text='Harakat tanlang', reply_markup=delivery['uz'])
    await MainMenu.step_two_uz.set()


async def basket(call: types.CallbackQuery, helper=False):
    sql = '''
    select b.id, i.name, i.price, b.count from products_basket as b
    join products_items as i on b.item_id = i.id where b.user_id = ?
        '''
    products = db.execute(sql=sql, parameters=(call.from_user.id,), fetchall=True)
    mes = '📥 Savat:\n\n'
    index = 1
    total_price = 0
    for id, name, price, count in products:
        total_price += count * price
        mes += f'{index}. {name}\n{count} x {price} = {count * price} som\n\n'
        index += 1

    mes += f'Umumiy: {total_price} som'
    if helper:
        await call.message.answer(text=mes, reply_markup=basket_markup(products))
    else:
        await call.message.edit_text(text=mes, reply_markup=basket_markup(products))


@dp.callback_query_handler(text='_', state='*')
async def _(call: types.CallbackQuery):
    await basket(call, True)
    await call.answer()


@dp.callback_query_handler(order_cb.filter(action='plus'), state='*')
@dp.callback_query_handler(order_cb.filter(action='minus'), state='*')
@dp.callback_query_handler(order_cb.filter(action='count'), state='*')
@dp.callback_query_handler(order_cb.filter(action='delete'), state='*')
async def order_update(call: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    basket_id = callback_data['id']
    count = int(callback_data['count'])

    if action == 'plus':
        count += 1
        sql = '''
update products_basket set count = ?
where id = ?
        '''
        db.execute(sql=sql, parameters=(count, basket_id), commit=True)

    elif action == 'minus':
        if count > 1:
            count -= 1
            sql = '''
            update products_basket set count = ?
            where id = ?
                    '''
            db.execute(sql=sql, parameters=(count, basket_id), commit=True)

        else:
            sql = 'delete from products_basket where id = ?'
            db.execute(sql=sql, parameters=(basket_id,), commit=True)

    elif action == 'delete':
        sql = 'delete from products_basket where id = ?'
        db.execute(sql=sql, parameters=(basket_id,), commit=True)
    else:
        await call.answer(f'{count}')

    await basket(call)
