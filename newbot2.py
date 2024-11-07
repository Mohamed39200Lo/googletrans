from pyrogram import Client, filters
from pyrogram.errors.exceptions.unauthorized_401 import AuthKeyUnregistered
from pyrogram.types import Message, CallbackQuery, ForceReply
from pyrogram.types import InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button
from pyrogram.errors import (ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid)
from pyrolistener import Listener, exceptions
from typing import Union
import asyncio
import threading
import os
import sys
import json



"""
# دوال حفظ واسترجاع البيانات من ملف JSON
def save_data(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
"""

#بديل
import requests  # لإضافة التفاعل مع GitHub Gist

Momo="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"
GITHUB_TOKEN = Momo  # ضع هنا الـ GitHub Token
GIST_ID = '1050e1f10d7f5591f4f26ca53f2189e9'  



# الدالة لتحميل البيانات من Gist
def load_data():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
    if response.status_code == 200:
        files = response.json().get('files', {})
        content = files.get('data22.json', {}).get('content', '{}')
        return json.loads(content)
    else:
        return {}

# الدالة لحفظ البيانات إلى Gist
def save_data(data):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    payload = {
        "files": {
            "data22.json": {
                "content": json.dumps(data, indent=4, default=str)
            }
        }
    }
    response = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to update Gist: {response.status_code}, {response.text}")



# تحميل البيانات من الملف
data = load_data()
source_destination_mapping = data.get("source_destination_mapping", {})


# إزالة علامات الاقتباس عند الطباعة

words_to_remove = data.get("words_to_remove", [])
lines_to_remove_starting_with = data.get("lines_to_remove_starting_with", [])
sentence_replacements = data.get("sentence_replacements", {})
line_replacements = data.get("line_replacements", {})
ignored_words = data.get("ignored_words", [])



def save_session(user_id, session_string):
    # 2. تحديد مفتاح فريد لكل جلسة

    data[f"session_{user_id}"] = session_string
    save_data(data)
    #print(session_string)

# تهيئة البوت
app2 = Client(
    "SessionsExcutor2",
    api_id=13848352,
    api_hash="99172839e8a8d950529aebfe46528cd0",
    bot_token="6474944481:AAFyN3tlQ-fibMMbW8RgR4FiA-T8xuhxuJs"
)

listener = Listener(client=app2)
# دالة لحذف جميع الخرائط
def delete_mappings():
    if "source_destination_mapping" in data:
        del data["source_destination_mapping"]
        save_data(data)

@app2.on_message(filters.command("deletemap"))
async def delete_mapping(_: Client, message: Message):
    delete_mappings()
    await message.reply("تم حذف القوائم المحفوظة بنجاح.")




# دوال حذف العناصر الأخرى
@app2.on_message(filters.command("deletewords"))
async def delete_words(_: Client, message: Message):
    global words_to_remove
    words_to_remove = []
    data["words_to_remove"] = words_to_remove
    save_data(data)
    await message.reply("تم حذف الكلمات المحفوظة بنجاح.")

@app2.on_message(filters.command("deletelines"))
async def delete_lines(_: Client, message: Message):
    global lines_to_remove_starting_with
    lines_to_remove_starting_with = []
    data["lines_to_remove_starting_with"] = lines_to_remove_starting_with
    save_data(data)
    await message.reply("تم حذف السطور المحفوظة بنجاح.")

@app2.on_message(filters.command("deletesentences_replace"))
async def delete_sentences(_: Client, message: Message):
    global sentence_replacements
    sentence_replacements = {}
    data["sentence_replacements"] = sentence_replacements
    save_data(data)
    await message.reply("تم حذف استبدالات الجمل المحفوظة بنجاح.")

@app2.on_message(filters.command("deleteline_replacements"))
async def delete_line_replacements(_: Client, message: Message):
    global line_replacements
    line_replacements = {}
    data["line_replacements"] = line_replacements
    save_data(data)
    await message.reply("تم حذف استبدالات السطور المحفوظة بنجاح.")

@app2.on_message(filters.command("deleteignoredwords"))
async def delete_ignored_words(_: Client, message: Message):
    global ignored_words
    ignored_words = []
    data["ignored_words"] = ignored_words
    save_data(data)
    await message.reply("تم حذف الكلمات المتجاهلة المحفوظة بنجاح.")

# دالة عرض البيانات المحفوظة
@app2.on_message(filters.command("showdata"))
async def show_data(_: Client, message: Message):
    data_message = (
        f"**القنوات:**\n{data.get('source_destination_mapping', {})}\n\n"
        f"**الكلمات التي يتم حذفها:**\n{data.get('words_to_remove', [])}\n\n"
        f"**الاسطر التي يتم حذفها:**\n{data.get('lines_to_remove_starting_with', [])}\n\n"
        f"**جمل يتم استبدالها:**\n{data.get('sentence_replacements', {})}\n\n"
        f"**اسطر يتم استبدالها:**\n{data.get('line_replacements', {})}\n\n"
        f"**كلمات الفلترة :**\n{data.get('ignored_words', [])}\n\n"
    )
    await message.reply(data_message)



# إضافة معالجة زر "عرض البيانات"
@app2.on_callback_query(filters.regex(r"^showdata$"))
async def show_data_callback(_: Client, callback: CallbackQuery):
    await show_data(_, callback.message)




@app2.on_callback_query(filters.regex(r"^control$"))
async def control_options(_: Client, callback: CallbackQuery):
    control_markup = Keyboard([

            [Button("إضافة كلمة للحذف", callback_data="add_word_to_remove")],
            [Button("إضافة سطر للحذف", callback_data="add_line_to_remove")],
            [Button("إضافة استبدال جملة", callback_data="add_sentence_replacement")],
            [Button("إضافة استبدال سطر", callback_data="add_line_replacement")],
            [Button("إضافة كلمة للتجاهل", callback_data="add_ignored_word")],  


            [Button("إلغاء", callback_data="cancel_control")]
    ])
    await callback.edit_message_text("اختر الإجراء الذي ترغب في القيام به:", reply_markup=control_markup)


@app2.on_callback_query(filters.regex(r"^add_word_to_remove$"))
async def add_word_to_remove(_: Client, callback: CallbackQuery):
    await callback.edit_message_text("أدخل كلمة ترغب في إضافتها للحذف:", reply_markup=ForceReply(selective=True))

@app2.on_callback_query(filters.regex(r"^add_line_to_remove$"))
async def add_line_to_remove(_: Client, callback: CallbackQuery):
    await callback.edit_message_text("أدخل السطر الذي ترغب في إضافته للحذف:", reply_markup=ForceReply(selective=True))

@app2.on_callback_query(filters.regex(r"^add_sentence_replacement$"))
async def add_sentence_replacement(_: Client, callback: CallbackQuery):
    await callback.edit_message_text("أدخل الجملة التي ترغب في استبدالها:", reply_markup=ForceReply(selective=True))

@app2.on_callback_query(filters.regex(r"^add_line_replacement$"))
async def add_line_replacement(_: Client, callback: CallbackQuery):
    await callback.edit_message_text("أدخل السطر الذي ترغب في استبداله:", reply_markup=ForceReply(selective=True))


@app2.on_callback_query(filters.regex(r"^add_ignored_word$"))
async def add_ignored_word_callback(_: Client, callback: CallbackQuery):
    await callback.edit_message_text("أدخل الكلمة التي ترغب في تجاهلها:", reply_markup=ForceReply(selective=True))

# دالة لإضافة خريطة جديدة بين القنوات
@app2.on_message(filters.command("add_mapping"))
async def add_mapping(_: Client, message: Message):
    user_id = message.from_user.id
    await message.reply("أدخل معرّف القناة المصدر:")
    source_channel_id = await get_user_input(user_id)
    if source_channel_id is None:
        return await message.reply("تم إلغاء الأمر.")

    await message.reply("أدخل معرّف القناة الهدف (يمكنك إدخال أكثر من واحد مفصولة بفاصلة):")
    destination_channel_ids = await get_user_input(user_id)
    if destination_channel_ids is None:
        return await message.reply("تم إلغاء الأمر.")

    destination_channel_ids = [int(channel_id) for channel_id in destination_channel_ids.split(",")]
    source_destination_mapping[int(source_channel_id)] = destination_channel_ids
    data["source_destination_mapping"] = source_destination_mapping
    save_data(data)
    await message.reply("تم حفظ البيانات بنجاح.")

# دوال لمعالجة الإدخال من المستخدم وإضافة عناصر جديدة للحذف أو الاستبدال
@app2.on_message(filters.reply & filters.text)
async def process_user_input(_: Client, message: Message):
    if "أدخل كلمة ترغب في إضافتها للحذف:" in message.reply_to_message.text:
        word = message.text.lower()
        words_to_remove.append(word)
        data["words_to_remove"] = words_to_remove
        save_data(data)
        await message.reply(f"تمت إضافة كلمة '{word}' للحذف.")
    elif "أدخل الجملة التي ترغب في استبدالها:" in message.reply_to_message.text:
        replacement_data = message.text.split("#")
        if len(replacement_data) == 2:
            old_sentence, new_sentence = replacement_data[0].strip(), replacement_data[1].strip()
            sentence_replacements[old_sentence] = new_sentence
            data["sentence_replacements"] = sentence_replacements
            save_data(data)
            await message.reply(f"تمت إضافة استبدال: '{old_sentence}' => '{new_sentence}'.")
    elif "أدخل السطر الذي ترغب في إضافته للحذف:" in message.reply_to_message.text:
        line = message.text.strip()
        lines_to_remove_starting_with.append(line)
        data["lines_to_remove_starting_with"] = lines_to_remove_starting_with
        save_data(data)
        await message.reply(f"تمت إضافة سطر '{line}' للحذف.")
    elif "أدخل السطر الذي ترغب في استبداله:" in message.reply_to_message.text:
        replacement_data = message.text.split("#")
        if len(replacement_data) == 2:
            old_line, new_line = replacement_data[0].strip(), replacement_data[1].strip()
            line_replacements[old_line] = new_line
            data["line_replacements"] = line_replacements
            save_data(data)
            await message.reply(f"تمت إضافة استبدال: '{old_line}' => '{new_line}'.")
    elif "أدخل الكلمة التي ترغب في تجاهلها:" in message.reply_to_message.text:
        new_word = message.text.strip()
        ignored_words.append(new_word)
        data["ignored_words"] = ignored_words
        save_data(data)
        await message.reply(f"تمت إضافة الكلمة '{new_word}' إلى قائمة التجاهل.")

async def get_user_input(user_id: int) -> Union[str, None]:
    try:
        user_input = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            timeout=120
        )
        return user_input.text.strip()
    except exceptions.TimeOut:
        return None









@app2.on_message(filters.command("start"))
@app2.on_message(filters.command("generate"))
async def s_type(_: Client, message: Message):
    caption = "مرحبا بك عزيزي في بوت النقل التلقائي "
    await message.reply(caption, reply_markup=markup, reply_to_message_id=message.id)


@app2.on_callback_query(filters.regex(r"^(pyrogram )"))
async def gen(_: Client, callback: CallbackQuery):
    cd: str = callback.data
    is_bot: Union[None, bool] = None
    if cd.endswith("bot"):
        await callback.answer("سيتم تنشيط الجلسة للبوت V2.", show_alert=True)
        is_bot = True
    await callback.edit_message_text("الجلسة البرنامجية بدأت.")
    s_vars = await getter(callback, is_bot)
    if not s_vars: return
    await registration(s_vars[0], s_vars[1], s_vars[2], is_bot, callback)


async def getter(callback: CallbackQuery, is_bot: bool):
    user_id: int = callback.from_user.id
    try: s_api_id: Message = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text="أدخل معرّف API الخاص بك. \nأرسل /default لاستخدام API الافتراضي\nأرسل /cancel لإلغاء الأمر.",
        reply_markup=ForceReply(selective=True, placeholder="معرّف API الخاص بك: "),
        reply_to_message_id=callback.message.id,
        timeout=60,
    )
    except exceptions.TimeOut: return await callback.message.reply("انتهى الوقت. يرجى إعادة الإرسال.", reply_markup=markup)
    if s_api_id.text == "/default": 
        _id: int = app2.api_id
        _hash: str = app2.api_hash
    elif s_api_id.text == "/cancel":
        await s_api_id.reply("تم إلغاء الجلسة.", reply_markup=markup, reply_to_message_id=s_api_id.id)
        return False
    else:
        try: int(s_api_id.text)
        except ValueError: return await s_api_id.reply("يجب أن يكون معرّف الـ API من نوع رقمي. حاول مرة أخرى.", reply_to_message_id=s_api_id.id,  reply_markup=markup)
        try: s_api_hash: Message = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="أدخل مفتاح API الخاص بك. \nأرسل /cancel لإلغاء الأمر.",
            reply_markup=ForceReply(selective=True, placeholder="مفتاح API الخاص بك: "),
            reply_to_message_id=s_api_id.id,
            timeout=60
        )
        except exceptions.TimeOut: await callback.message.reply("انتهى الوقت. يرجى إعادة الإرسال.", reply_markup=markup)
        if s_api_hash.text == "/cancel":
            await s_api_hash.reply("تم إلغاء الجلسة.", reply_markup=markup, reply_to_message_id=s_api_hash.id)
            return False
        _id, _hash = int(s_api_id.text), s_api_hash.text
    try: tp: Message = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text=f"أدخل رقم هاتفك {'أو رقم الهاتف الذي تريد تفعيله -> +128372'}\nأرسل /cancel لإلغاء الأمر.",
        reply_markup=ForceReply(selective=True, placeholder=f"{'رقم الهاتف الخاص بك' if not is_bot else 'رقم الهاتف -> +128372'}: "),
        timeout=60
    )
    except exceptions.TimeOut: await callback.message.reply("انتهى الوقت. يرجى إعادة الإرسال.", reply_markup=markup)
    if tp.text == "/cancel":
        await tp.reply("تم إلغاء الجلسة.", reply_to_message_id=tp.id, reply_markup=markup)
        return False
    elif is_bot:
        _token = tp.text
        return _id, _hash, _token
    else :
        _number = tp.text
        return _id, _hash, _number


markup: Keyboard = Keyboard([

        [
            Button("التسجيل على البوت", "pyrogram 2")
        ],
        [Button("إضافة تعديلات للرسائل", callback_data="control")
        ],
        [Button("عرض البيانات المحفوظة", callback_data="showdata")]


    ])


async def registration(_id: int, _hash: str, tp: str, is_bot: bool, callback: CallbackQuery):
    user_id = callback.from_user.id
    _token = tp if is_bot else None
    _number = tp if not is_bot else None
    await callback.message.reply("بدأ تسجيل الجلسة.")
    if is_bot:
        client = Client("bot", api_id=_id, api_hash=_hash, bot_token=_token, in_memory=True)
        await client.connect()
        try:await client.sign_in_bot(_token)
        except: return await callback.message.reply("فشل في تنشيط الجلسة للبوت.\nحاول مرة أخرى.", reply_markup=markup)
        session = await client.export_session_string()
        #await save_session(user_id, session)
        data["session"] = session
        save_data(data)
        return await callback.message.reply(
            f"تم تنشيط الجلسة الخاصة بك بنجاح.\n\n`{session}`",
            reply_to_message_id = callback.message.id
        )
    client: Client = Client("acc", in_memory=True)
    client.api_id = _id
    client.api_hash = _hash
    await client.connect()
    try: p_code_hash = await client.send_code(_number)
    except (ApiIdInvalid): return await callback.message.reply("خطأ في معرّف API الخاص بك أو مفتاح الوصول.\nحاول مرة أخرى.", reply_markup=markup)
    except (PhoneNumberInvalid): return await callback.message.reply("خطأ في رقم الهاتف الخاص بك.\nحاول مرة أخرى.", reply_markup=markup)
    try: code = await listener.listen(
        from_id=user_id,
        chat_id=user_id,
        text="أدخل رمز التحقق المكون من 6 أرقام الذي تم إرساله إلى هاتفك.\nاستخدم الأرقام فقط. لا تستخدم أي أحرف.",
        timeout=120,
        reply_markup=ForceReply(selective=True, placeholder="رمز التحقق: ")
    )
    except exceptions.TimeOut: return await callback.message.reply("انتهى الوقت. يرجى إعادة الإرسال.",  reply_markup=markup)
    try: await client.sign_in(_number, p_code_hash.phone_code_hash, code.text.replace(" ", ""))
    except (PhoneCodeInvalid): return await callback.message.reply("رمز التحقق غير صحيح.\nحاول مرة أخرى.", reply_markup=markup, reply_to_message_id=code.id)
    except (PhoneCodeExpired): return await callback.message.reply("انتهت صلاحية رمز التحقق.\nحاول مرة أخرى.", reply_markup=markup, reply_to_message_id=code.id)
    except (SessionPasswordNeeded):
        try:password = await listener.listen(
            from_id=user_id,
            chat_id=user_id,
            text="أدخل كلمة المرور الثانية (إذا كانت مطلوبة).",
            reply_markup=ForceReply(selective=True, placeholder="كلمة المرور: "),
            timeout=180,
            reply_to_message_id=code.id
        )
        except exceptions.TimeOut:return await callback.message.reply("انتهى الوقت. يرجى إعادة الإرسال.",  reply_markup=markup)
        try: await client.check_password(password.text)
        except (PasswordHashInvalid): return await callback.message.reply("كلمة المرور غير صحيحة.\nحاول مرة أخرى.", reply_markup=markup)
    session = await client.export_session_string()
    data["session"] = session
    save_data(data)
    await client.send_message(
        "me",
        f"تم تنشيط الجلسة الخاصة بك بنجاح.\n\n`{session}`",
        reply_to_message_id = callback.message.id
    )
    await client.disconnect()
    await app2.send_message(user_id, "تم تنشيط جلسة البرنامج الخاصة بك بنجاح. تحقق من الرسائل الخاصة.", reply_markup=Keyboard([[Button("اختر نوع الجلسة #1", user_id=1596661941)]]))

