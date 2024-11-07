
from newbot2 import *
from newbot1 import *
from app import server
import asyncio
import os
import sys
import time
from pyrogram.errors import AuthKeyDuplicated
import subprocess
import gunicorn

@app2.on_message(filters.command("reload"))
async def reload_bots(_: Client, message: Message):
    await message.reply("جاري إعادة تشغيل البرنامج...")
    os.execl(sys.executable, sys.executable, *sys.argv)

def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)


async def run_bot1():
    global Tests
    try:
        await app1.start()
        sent_alert = False  # متغير لتتبع ما إذا تم إرسال التنبيه بالفعل أم لا
        while True:
            try:
                await app1.get_me()
                await asyncio.sleep(15)
            except AuthKeyUnregistered:
                if not sent_alert:  # إذا لم يتم إرسال التنبيه بعد
                    print("Bot 1 session is unregistered. Sending alert to Bot 2.")
                    await app2.send_message(1596661941, "هناك مشكله في جلسة تليجرام جرب التسجيل مرة أخرى واعد تشغيل البوت")
                    sent_alert = True  # قم بتعيين المتغير إلى True بعد إرسال التنبيه
            except AuthKeyDuplicated:
                if not sent_alert:
                    print("Bot 1 session is duplicated. Sending alert to Bot 2.")
                    await app2.send_message(1596661941, "يرجى التسجيل من جديد باستخدام حساب تليجرام واعد تشغيل البوت ")
                    sent_alert = True
            except Exception as e:
                await app2.send_message(1596661941, "حدث خطأ أثناء عمل البوت")
                Tests += 1
                if Tests >= 3:
                    Tests = 0
                    await restart_program()
                    time.sleep(350)
                time.sleep(45)
                print(f"An error occurred in bot1: {e}")
    except Exception as e:
        print(f"An error occurred in bot1: {e}")
        pass

async def run_bot2():
    session_file1 = "SessionsExcutor.session"  # 
    session_file2 = "path_to_bot2_session_file_2"  # 
    try:
        if app1.is_connected:
            print(55)
            await app2.stop()
        await app2.start()
        while True:
            await asyncio.sleep(50)
    except AuthKeyDuplicated:
        print("Bot 2 session is duplicated. Deleting session files and restarting.")
        time.sleep(20)

        if os.path.exists(session_file1):
            os.remove(session_file1)
        if os.path.exists(session_file2):
            os.remove(session_file2)
        restart_program()
    except Exception as e:
        print(f"An error occurred in bot2: {e}")
        pass

# تشغيل البوتين في وضع دائم
def main():
    subprocess.Popen(["gunicorn", "app:app", "-b", "0.0.0.0:8080"])
    loop = asyncio.get_event_loop()
    # تشغيل بوت الأول
    task1 = asyncio.ensure_future(run_bot1())
    # تشغيل بوت الثاني
    task2 = asyncio.ensure_future(run_bot2())

    try:
        loop.run_until_complete(asyncio.gather(task1, task2))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred in one of the bots: {e}")
    finally:
        loop.stop()

if __name__ == "__main__":
    main()
