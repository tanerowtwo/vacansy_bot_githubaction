import os
import json
import urllib.parse
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession


# ============================================================
# ENV
# ============================================================

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
string_session = os.environ["STRING_SESSION"]

target_chat = int(
    os.environ.get("TARGET_CHAT", "-4734945370")
)


# ============================================================
# НАСТРОЙКИ
# ============================================================

STATE_FILE = "state.json"


include_words = [
    "монтаж",
    "монтажер",
    "#ищу_монтаж",
    "монтажера",
    "смонтировать",
    "екатеринбург",
    "екб",
    "колорист",
    "покрасить",
    "цветокоррекция",
    "магнитогорск",
    "челябинск"
]


# Чаты, которые полностью игнорируем
blacklist_chats = [
    -1002392926279,
    1126831003
]


# Добавляем target_chat автоматически,
# чтобы бот не начал анализировать собственные пересланные сообщения.
if target_chat not in blacklist_chats:
    blacklist_chats.append(target_chat)


exclude_words = ["#ищу_работу", "#ищуработу", "я видеомонтажёр", "занимаюсь монтажом", "#резюме", "нахожусь в поисках проектов", "я монтажёр", "я видеомонтажер", "я монтажер", "#портфолио", "#помогу", "#рилсмейкер", "предлагаю свою кандидатуру", "делаю монтаж", "мое портфолио", "я #видеомонтажёр", "работаю с блогерами", "reels / shorts / tiktok", "добро пожаловать в группу шапка чат.", "я занимаюсь монтажом", "создам красивую картинку", "я монтирую", "я помогу тебе", "мой монтаж", "предлагаю услуги", "почему вам стоит выбрать меня", "ищу новые проекты", "я оператор-постановщик", "почему стоит выбрать меня", "reels", "я - монтажер", "занимаюсь монтажом", "я начинающий монтажёр", "я начинающий специалист", "я монтирую", "я видеооператор-монтажер", "я колорист", "я занимаюсь монтажем", "создаю ролики", "мы делаем ролики", "тогда тебе — ко мне", "чем я конкретно занимаюсь", "я оператор-видеомонтажер", "вот что я умею", "я full-time колорист", "сделаю качественный моушен", "я сведу ваши лучшие кадры", "хочешь такой же монтаж", "свободен для проектов", "свободен для новых проектов", "летаю на дронах", "я начинающий монтажер", "я fulltime колорист", "я являюсь видеомонтажером", "я знаю толк в монтаже", "ваше сообщение удалено", "улетит в @ru_montage_pins", "ищу смм-менеджера.", "делаю волшебство в сфере монтажа", "clarity design", "@winerooo", "@kartinsky", "смонтирую бесплатно парочку", "https://t.me/andrews_hurricane", "превращу ваши исходники", "пишите — обсудим ваш проект!", "@lykiardtg", "emalzp", "монтаж который приносит людям результаты", "@frutell04ka", "мои работы", "у тебя нет времени на монтаж", "@the13tn", "@anwazzup", "я занимаюсь видеомонтажом.", "@karinakraskj", "ищу заказы", "я олег — видеомонтажер", "@ragestrike", "@minec0mmand", "https://t.me/prtflconsence", "@terpkiy56", "https://t.me/eprikyanedit", "@kanexlz", "я дипломированный опытный", "занимаюсь созданием роликов", "смонтирую любой ваш контент", "@tamedghost", "@iamyownmuse", "я — видеомонтажёр,", "я — видеомонтажёр", "кастинг актеров", "предоставляю услуги", "работаю в видеомонтаже", "@abramov_prod", "почему твои видео не работают.", "предлагаю свои услуги", "@moshpitedit", "буду рад выйти на ваш проект", "@simon_rotkiv", "я специализируюсь на монтаже видео.", "я специализируюсь на монтаже видео", "я fulltime колорист", "монтаж для потребителя", "@daniilvfx", "@cgtesto", "свободен, ищу проекты", "монтирую круто", "я видео монтажёр", "@zinckprod", "ищу работу", "ищу начинающего", "@osukhovskiyfilms", "@sabo_tg", "нужен качественный монтаж?", "буду рада выйти", "готова выйти", "@film_post_production", "стану вашим монтажером", "@leifu", "@tati_lead_manager", "@kugukanton", "@emifilm", "монтаж который даст тебе результаты", "@tsujiss", "@aladdin_videomaker", "могу выйти на ваш проект", "я специализируюсь на монтаже", "я — профессиональный монтажёр", "традиционная акция уже близко!", "1 - h.264/265", "@vladin98", "ищу смм", "список основных триггеров:", "я профессиональный колорист", "ищите ответственного монтажёра?", "@asens410", "ищу девушку монтажерку для отношений", "делаю бесплатный монтаж", "https://t.me/jump_cut/773", "ищу проекты в портфолио", "бесплатный монтаж видео", "https://t.me/portgromov", "@smaryd1", "telegram:@smaryd1", "готов бесплатно смонтировать", "я режиссер монтажа.", "открыт к проектам", "@pslnnn", "@radicalsubject", "@logovosrg", "я профессиональный колорист.", "работаю в davinci resolve", "ищите ответственного монтажёра?", "я видеограф", "делаю ролики, которые приносят прибыль", "готов выполнить ваши задачи", "сделаю ебейший монтаж", "ищу проекты", "готова к новым проектам", "@slavik13evg", "монтаж, который дарит эмоции", "@kabadvd", "нужен качественный видеомонтаж?", "я занимаюсь монтажём", "сделаю сочнейший монтаж", "делаю уникальный монтаж", "ищу интересные заказы", "я занимаюсь цветокоррекцией", "худший монтаж - это когда моушн бессилен", "увеличил(а) репутацию", "монтаж на результат", "@alexei1v", "я-монтажёр", "@samnexer", "возьму проекты на цветокоррекцию", "выступаю в роли оператора", "выйду на ваши проекты", "готов выйти на смену", "открыт для новых проектов", "готов взять в работу", "я режиссёр-монтажа", "я занимаюсь видеомонтажом", "dreamreel production", "@nikitamontagx", "@satorussia", "работаю удаленно", "вот моё портфолио", "@crsupportcr"]



# ============================================================
# STATE
# ============================================================

def load_state():
    """
    Загружает последний обработанный message_id
    для каждого чата.
    """

    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            return data

        return {}

    except Exception as e:
        print(f"⚠️ Не удалось прочитать state.json: {e}")
        return {}


def save_state(state):
    """
    Сохраняет состояние.
    """

    temp_file = STATE_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(
            state,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temp_file, STATE_FILE)


# ============================================================
# TELEGRAM CLIENT
# ============================================================

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)


# ============================================================
# ОБРАБОТКА ОДНОГО СООБЩЕНИЯ
# ============================================================

async def process_message(message):
    """
    Возвращает:
        True  — сообщение успешно обработано
        False — сообщение не подошло под фильтры

    Если возникает настоящая ошибка отправки,
    функция выбрасывает исключение.
    """

    if not message.message:
        return False

    raw_msg = message.message
    msg = raw_msg.lower()

    print(
        f"📩 [{message.chat_id}:{message.id}] "
        f"{msg[:100]}"
    )

    # --------------------------------------------------------
    # INCLUDE
    # --------------------------------------------------------

    if not any(
        word.lower() in msg
        for word in include_words
    ):
        return False

    # --------------------------------------------------------
    # EXCLUDE
    # --------------------------------------------------------

    if any(
        word.lower() in msg
        for word in exclude_words
    ):
        print("⛔ Отфильтровано")
        return False

    # --------------------------------------------------------
    # BLACKLIST
    # --------------------------------------------------------

    chat_id = message.chat_id

    if chat_id in blacklist_chats:
        print(
            f"⛔ Игнорирую чат {chat_id}"
        )
        return False

    # --------------------------------------------------------
    # CHAT / SENDER
    # --------------------------------------------------------

    chat = await message.get_chat()
    sender = await message.get_sender()

    chat_name = (
        getattr(chat, "title", None)
        or getattr(chat, "username", None)
        or "Чат"
    )

    username = getattr(
        sender,
        "username",
        None
    )

    user_id = sender.id

    if username:

        sender_display = (
            f'<a href="https://t.me/{username}">'
            f'@{username}'
            f'</a>'
        )

    else:

        sender_display = (
            f'<a href="tg://user?id={user_id}">'
            f'Пользователь'
            f'</a>'
        )

    # --------------------------------------------------------
    # ОТКЛИКИ
    # --------------------------------------------------------

    msg1 = (
        "Здравствуйте! Пишу по поводу монтажа.\n\n"
        "Мои работы: "
        "danilkaltashev.ru"
    )

    msg2 = (
        "Добрый день! Пишу по поводу монтажа.\n\n"
        "Мои работы: "
        "danilkaltashev.ru"
    )

    msg3 = (
        "Приветствую! Пишу по поводу монтажа.\n\n"
        "Мои работы: "
        "danilkaltashev.ru"
    )

    links = ""

    if username:

        msg1_enc = urllib.parse.quote(msg1)
        msg2_enc = urllib.parse.quote(msg2)
        msg3_enc = urllib.parse.quote(msg3)

        links = (
            "\n\n💬 Отклики:\n"
            f"— <a href='https://t.me/{username}"
            f"?text={msg1_enc}'>Отклик 1</a>\n"
            f"— <a href='https://t.me/{username}"
            f"?text={msg2_enc}'>Отклик 2</a>\n"
            f"— <a href='https://t.me/{username}"
            f"?text={msg3_enc}'>Отклик 3</a>\n"
        )

    # --------------------------------------------------------
    # ИТОГОВОЕ СООБЩЕНИЕ
    # --------------------------------------------------------

    text = (
        f"📢 Из чата: {chat_name}\n"
        f"👤 От: {sender_display}\n\n"
        f"{raw_msg}"
        f"{links}"
    )

    # --------------------------------------------------------
    # ОТПРАВКА
    # --------------------------------------------------------

    await client.send_message(
        target_chat,
        text,
        parse_mode="html"
    )

    print(
        f"✅ Отправлено из {chat_name} "
        f"(message_id={message.id})"
    )

    return True


# ============================================================
# ОБРАБОТКА ОДНОГО ЧАТА
# ============================================================

async def process_chat(dialog, state):
    """
    Обрабатывает только сообщения после last_message_id.

    Возвращает обновлённый last_message_id.
    """

    chat_id = str(dialog.id)

    # --------------------------------------------------------
    # ПЕРВЫЙ ЗАПУСК ДЛЯ ЭТОГО ЧАТА
    # --------------------------------------------------------

    if chat_id not in state:

        print(
            f"🆕 Новый чат в state: "
            f"{dialog.name}"
        )

        try:

            latest_messages = []

            async for message in client.iter_messages(
                dialog.entity,
                limit=1
            ):
                latest_messages.append(message)

            if latest_messages:

                latest_id = latest_messages[0].id

                state[chat_id] = latest_id

                print(
                    f"📌 Начальная точка "
                    f"{dialog.name}: {latest_id}"
                )

            else:

                state[chat_id] = 0

                print(
                    f"📌 В чате {dialog.name} "
                    f"нет сообщений"
                )

        except Exception as e:

            print(
                f"⚠️ Ошибка инициализации "
                f"{dialog.name}: {e}"
            )

        return state.get(chat_id, 0)

    # --------------------------------------------------------
    # ПОСЛЕДНИЙ ОБРАБОТАННЫЙ MESSAGE ID
    # --------------------------------------------------------

    last_id = int(state[chat_id])

    print(
        f"🔎 {dialog.name} | "
        f"последний ID: {last_id}"
    )

    newest_successful_id = last_id

    # --------------------------------------------------------
    # ПОЛУЧАЕМ НОВЫЕ СООБЩЕНИЯ
    # --------------------------------------------------------

    try:

        async for message in client.iter_messages(
            dialog.entity,
            min_id=last_id,
            reverse=True
        ):

            print(
                f"➡️ Новое сообщение "
                f"{dialog.name}: {message.id}"
            )

            try:

                await process_message(message)

                # Сообщение либо отправлено,
                # либо отфильтровано.
                #
                # В обоих случаях его можно считать
                # обработанным.

                newest_successful_id = message.id

            except Exception as e:

                # Очень важно:
                #
                # если отправка подходящего сообщения
                # реально упала, НЕ двигаем checkpoint.
                #
                # Следующий запуск попробует это сообщение
                # снова.

                print(
                    f"❌ Ошибка обработки "
                    f"{dialog.name} / "
                    f"{message.id}: {e}"
                )

                break

    except Exception as e:

        print(
            f"⚠️ Ошибка чтения "
            f"{dialog.name}: {e}"
        )

        return last_id

    # --------------------------------------------------------
    # ОБНОВЛЯЕМ STATE
    # --------------------------------------------------------

    if newest_successful_id > last_id:

        state[chat_id] = newest_successful_id

        print(
            f"💾 {dialog.name}: "
            f"{last_id} → "
            f"{newest_successful_id}"
        )

    return state[chat_id]


# ============================================================
# MAIN
# ============================================================

async def main():

    print("=" * 60)
    print("🚀 Запуск Telegram scanner")
    print("=" * 60)

    state = load_state()

    print(
        f"📂 В state.json записано чатов: "
        f"{len(state)}"
    )

    # --------------------------------------------------------
    # CONNECT
    # --------------------------------------------------------

    await client.start()

    me = await client.get_me()

    print(
        f"👤 Авторизован как: "
        f"@{getattr(me, 'username', None)} "
        f"(ID {me.id})"
    )

    # --------------------------------------------------------
    # ПОЛУЧАЕМ ВСЕ ДИАЛОГИ
    # --------------------------------------------------------

    dialogs = []

    print("📚 Получаю список диалогов...")

    async for dialog in client.iter_dialogs():

        # Только группы и каналы.
        #
        # Личные переписки здесь не сканируем.
        # Для вакансий это правильнее и экономнее.

        if not dialog.is_group and not dialog.is_channel:
            continue

        chat_id = dialog.id

        # blacklist

        if chat_id in blacklist_chats:
            print(
                f"⛔ Blacklist: {dialog.name}"
            )
            continue

        dialogs.append(dialog)

    print(
        f"📚 Будет проверено чатов: "
        f"{len(dialogs)}"
    )

    # --------------------------------------------------------
    # ПРОХОД ПО ЧАТАМ
    # --------------------------------------------------------

    for index, dialog in enumerate(dialogs, start=1):

        print()
        print(
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

        print(
            f"💬 Чат {index}/{len(dialogs)}: "
            f"{dialog.name}"
        )

        try:

            await process_chat(
                dialog,
                state
            )

        except Exception as e:

            print(
                f"❌ Критическая ошибка "
                f"чата {dialog.name}: {e}"
            )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_state(state)

    print()
    print("=" * 60)
    print("💾 State сохранён")
    print(
        f"📊 Всего чатов в state: "
        f"{len(state)}"
    )
    print("🏁 Проверка завершена")
    print("=" * 60)

    await client.disconnect()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())
