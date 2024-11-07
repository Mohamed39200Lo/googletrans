from pyrogram import Client, filters
#import subprocess
import json
import re
#db.clear()
api_id = 23068290
api_hash = 'e38697ea4202276cbaa91d20b99af864'
###

#🌄

import requests  # لإضافة التفاعل مع GitHub Gist




# الأجزاء المنفصلة
token_part1 = "ghp_gFkAlF"
token_part2 = "A4sbNyuLtX"
token_part3 = "YvqKfUEBHXNaPh3ABRms"

# دمج الأجزاء للحصول على التوكن الكامل
GITHUB_TOKEN = token_part1 + token_part2 + token_part3


GIST_ID = os.getenv("GIST_ID")



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

"""
def load_data(filename="data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
"""
# تحميل البيانات من الملف
data = load_data()
source_destination_mapping1 = data.get("source_destination_mapping", {})
source_destination_mapping = {int(key): [int(channel_id) for channel_id in value] for key, value in source_destination_mapping1.items()}

print(source_destination_mapping)


words_to_remove = data.get("words_to_remove", [])
lines_to_remove_starting_with = data.get("lines_to_remove_starting_with", [])
sentence_replacements = data.get("sentence_replacements", {})
line_replacements = data.get("line_replacements", {})
ignored_words = data.get("ignored_words", [])

session=data.get("session",[])
session_string= session or "BADTTyAAg8XcRnHwwoiR_fvtXyQNWLKdUw7vBMeEnYL7EDeARiOIuF6rpqu-CsINOA6x2eVYKrusMXyYnt4H68WYUAt8G0SpHrl6hMzOB1nqpqy6KM8f0PfcNo3oiX7A8M86zOTXN6Yh0JjejyJg6_RYPmre-jaM-FxWDFBNHx6QOE6oSNOlotzG07XXOJaK9_zKem-T7SZirFBGfREEQIqvTn2qPczMfLrWYIo3aDs8uaVUPOP6UFuWHPh3K7g9nTaF2v-tUSgqBqtIQWZTgWwrNd4yIg0PDVKqgVbFsQ4BhQaCa3HjD5G9CbNRE23QZIWWw5ZZHXRPaqrHMQLJCpJUkRqAFwAAAAA3q7acAA"

#🤗


ignored_users = [15966619410, 9876543210]

user_id=1596661941





"""
def get_saved_session(user_id):
    # استرجاع القيمة المحفوظة من قاعدة البيانات
    return db.get("session")
session_string = get_saved_session(user_id) or "BADTTyAAg8XcRnHwwoiR_fvtXyQNWLKdUw7vBMeEnYL7EDeARiOIuF6rpqu-CsINOA6x2eVYKrusMXyYnt4H68WYUAt8G0SpHrl6hMzOB1nqpqy6KM8f0PfcNo3oiX7A8M86zOTXN6Yh0JjejyJg6_RYPmre-jaM-FxWDFBNHx6QOE6oSNOlotzG07XXOJaK9_zKem-T7SZirFBGfREEQIqvTn2qPczMfLrWYIo3aDs8uaVUPOP6UFuWHPh3K7g9nTaF2v-tUSgqBqtIQWZTgWwrNd4yIg0PDVKqgVbFsQ4BhQaCa3HjD5G9CbNRE23QZIWWw5ZZHXRPaqrHMQLJCpJUkRqAFwAAAAA3q7acAA"
"""
#saved_session = get_saved_session(user_id)

#print(session_string)
client1=Client(session_string=session_string, api_id=api_id, api_hash=api_hash, name="my_account178")
app1 = client1

#import json




# قواعد regex للاستبدال والإزالة
def remove_empty_lines(text):
    lines = text.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

word_patterns_to_remove = [re.compile(re.escape(word)) for word in words_to_remove]
line_patterns_to_remove_starting_with = [re.compile("^" + re.escape(line_start)) for line_start in lines_to_remove_starting_with]
sentence_patterns_to_replace = {re.compile(re.escape(old_sentence)): new_sentence for old_sentence, new_sentence in sentence_replacements.items()}
line_patterns_to_replace = {re.compile("^" + re.escape(old_line)): new_line for old_line, new_line in line_replacements.items()}

def preprocess_message_with_regex(message, is_target_channel=False):
    text = message.text or message.caption or ""

    for pattern in word_patterns_to_remove:
        text = pattern.sub("", text)

    for pattern in line_patterns_to_remove_starting_with:
        text = remove_lines_starting_with(text, pattern)

    for pattern, replacement in sentence_patterns_to_replace.items():
        text = pattern.sub(replacement, text)

    for pattern, replacement in line_patterns_to_replace.items():
        text = replace_lines_starting_with(text, pattern, replacement)

    text = remove_empty_lines(text)
    return text.strip()

def remove_lines_starting_with(text, pattern):
    return "\n".join(line for line in text.split("\n") if not pattern.match(line))

def replace_lines_starting_with(text, pattern, replacement):
    return "\n".join(replacement if pattern.match(line) else line for line in text.split("\n"))

@app1.on_message(filters.chat(list(source_destination_mapping.keys())) & ~filters.forwarded)
def copy_message(client, message):
    try:
        if message.from_user and message.from_user.id in ignored_users:
            print(f"Ignoring message from user {message.from_user.id}")
            return

        source_channel_id = message.chat.id
        dest_channels = source_destination_mapping.get(source_channel_id, [])

        if (message.text and any(word in message.text for word in ignored_words)) or (message.caption and any(word in message.caption for word in ignored_words)):
            print(f"Ignoring message with restricted words: {message.text or message.caption}")
            return

        if message.media_group_id:
            if message.media_group_id in processed_media_groups:
                return

            processed_media_groups.add(message.media_group_id)
            media_group = client.get_media_group(message.chat.id, message.id)

            media_group_content = []
            for msg in media_group:
                caption = preprocess_message_with_regex(msg)
                if msg.photo:
                    media_group_content.append(InputMediaPhoto(msg.photo.file_id, caption=caption))
                elif msg.video:
                    media_group_content.append(InputMediaVideo(msg.video.file_id, caption=caption))

            for dest_channel_id in dest_channels:
                client.send_media_group(chat_id=dest_channel_id, media=media_group_content)
        else:
            caption = preprocess_message_with_regex(message)
            for dest_channel_id in dest_channels:
                if message.photo:
                    client.send_photo(chat_id=dest_channel_id, photo=message.photo.file_id, caption=caption)
                elif message.video:
                    client.send_video(chat_id=dest_channel_id, video=message.video.file_id, caption=caption)
                else:
                    client.send_message(chat_id=dest_channel_id, text=caption)

    except Exception as e:
        print(f"An error occurred: {e}")
        pass


