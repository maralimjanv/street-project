from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

product_cb = CallbackData('product', 'id', 'count', 'action')
order_cb = CallbackData('order', 'id', 'count', 'action')


def order_menu(price=0):
    manu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"📥 Корзина ({price} som)", callback_data='_')],
        [
            InlineKeyboardButton(text="🎉AKSIYA", switch_inline_query_current_chat="🎉AKSIYA"),

            InlineKeyboardButton(text="🥤🌯Summer Set", switch_inline_query_current_chat="🥤🌯Summer Set")],
        [
            InlineKeyboardButton(text="🍕 Pizza", switch_inline_query_current_chat="🍕 Pizza"),

            InlineKeyboardButton(text="🌯 Rollar", switch_inline_query_current_chat="🌯 Rollar")],
        [
            InlineKeyboardButton(text="🍟 Snacks", switch_inline_query_current_chat="🍟 Snacks"),

            InlineKeyboardButton(text="🍔 BURGERS", switch_inline_query_current_chat="🍔 BURGERS")],
        [
            InlineKeyboardButton(text="🥗 Salatlar", switch_inline_query_current_chat="🥗 Salatlar"),

            InlineKeyboardButton(text="🍭 Bolalar uchun", switch_inline_query_current_chat="🍭 Bolalar uchun")],
        [
            InlineKeyboardButton(text="🥤Sovuq ichimliklar", switch_inline_query_current_chat="🥤Sovuq ichimliklar"),

            InlineKeyboardButton(text="🥫Souslar", switch_inline_query_current_chat="🥫Souslar")],
        [
            InlineKeyboardButton(text="🍹Kokteyllar", switch_inline_query_current_chat="🍹Kokteyllar")]

    ], resize_keyboard=True)
    return manu


def product_markup(items_id, count):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕', callback_data=product_cb.new(id=items_id, count=count, action='plus')),
         InlineKeyboardButton(text=f'{count}', callback_data=product_cb.new(id=items_id, count=count, action='count')),
         InlineKeyboardButton(text='➖', callback_data=product_cb.new(id=items_id, count=count, action='minus'))],
        [InlineKeyboardButton(text='istayman', callback_data=product_cb.new(id=items_id, count=count, action='add'))]
    ])
    return markup


def basket_markup(products):
    markup = InlineKeyboardMarkup()
    index = 1
    for id, name, price, count in products:
        markup.add(
            InlineKeyboardButton(text='➕', callback_data=order_cb.new(id=id, count=count, action='plus')),
            InlineKeyboardButton(text=f'{count}', callback_data=order_cb.new(id=id, count=count, action='count')),
            InlineKeyboardButton(text='➖', callback_data=order_cb.new(id=id, count=count, action='minus'))
        )
        markup.add(InlineKeyboardButton(text=f'❌{index}. {name}',
                                        callback_data=order_cb.new(id=id, count=count, action='delete')))
        index += 1
    return markup
