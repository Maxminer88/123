import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import math
import random

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Состояние пользователей (для викторины)
user_states = {}

# Система оценивания пользователей
user_scores = {}

# Вопросы для викторины
quiz_questions = [
    {
        "question": "Что такое ВВП?",
        "options": ["А) Валовой внутренний продукт", "Б) Валовой внешний продукт", "В) Внутренний валовой процент"],
        "answer": "А"
    },
    {
        "question": "Что такое флотирование валюты?",
        "options": ["А) Установленный курс", "Б) Свободное установление курса", "В) Поддержка курса"],
        "answer": "Б"
    },
    {
        "question": "Какой из следующих показателей является опережающим индикатором?",
        "options": ["А) Уровень безработицы", "Б) Индекс производственной активности", "В) Инфляция"],
        "answer": "Б"
    },
    {
        "question": "Что такое валютный курс?",
        "options": ["А) Цена одной валюты в терминах другой", "Б) Уровень инфляции в стране", "В) Рейтинг финансовых институтов"],
        "answer": "А"
    },
    {
        "question": "Какое влияние оказывает снижение процентной ставки?",
        "options": ["А) Увеличивает инвестиции", "Б) Увеличивает инфляцию", "В) Снижает спрос на кредит"],
        "answer": "А"
    },
    {
        "question": "Что такое экономический цикл?",
        "options": ["А) Периоды роста и спада экономики", "Б) Устойчивое экономическое развитие", "В) Нестабильность цен"],
        "answer": "А"
    },
    {
        "question": "Что такое динамика цен?",
        "options": ["А) Изменение общего уровня цен", "Б) Колебание валютного курса", "В) Темп роста экономики"],
        "answer": "А"
    },
    {
        "question": "Что такое экономическая загрязнённость?",
        "options": ["А) Рост производства", "Б) Увеличение экологии", "В) Влияние производства на природу"],
        "answer": "В"
    },
    {
        "question": "Какой стимул используется для повышения инвестиций?",
        "options": ["А) Снижение налогов", "Б) Увеличение государственных расходов", "В) Увеличение процентных ставок"],
        "answer": "А"
    },
    {
        "question": "Что измеряет ставки рефинансирования?",
        "options": ["А) Условия кредитования", "Б) Стоимость денег для банков", "В) Уровень заимствований"],
        "answer": "Б"
    },
    {
        "question": "Какое из утверждений верно для монетарной политики?",
        "options": ["А) Ориентирована на налоги", "Б) Ориентирована на денежную массу", "В) Ориентирована на социальные программы"],
        "answer": "Б"
    },
    {
        "question": "Какая организация устанавливает ключевую ставку в России?",
        "options": ["А) Минфин", "Б) Центральный банк", "В) Правительство"],
        "answer": "Б"
    },
    {
        "question": "Что означает рост инфляции?",
        "options": ["А) Снижение цен", "Б) Рост цен", "В) Стабильность цен"],
        "answer": "Б"
    },
    {
        "question": "Что такое дефляция?",
        "options": ["А) Рост цен", "Б) Снижение цен", "В) Стабильность цен"],
        "answer": "Б"
    },
    {
        "question": "Какой показатель характеризует безработицу?",
        "options": ["А) Уровень безработицы", "Б) Индекс цен", "В) Валютный курс"],
        "answer": "А"
    },
    {
        "question": "Что такое девальвация рубля?",
        "options": ["А) Укрепление рубля", "Б) Ослабление рубля", "В) Стабильность курса"],
        "answer": "Б"
    },
    {
        "question": "Как называется общая стоимость всех товаров и услуг в стране?",
        "options": ["А) ВНП", "Б) ВВП", "В) НД"],
        "answer": "Б"
    },
    {
        "question": "Что показывает индекс потребительских цен?",
        "options": ["А) Динамику цен на товары и услуги", "Б) Уровень безработицы", "В) Объём экспорта"],
        "answer": "А"
    },
    {
        "question": "Какая валюта является резервной в мире?",
        "options": ["А) Евро", "Б) Доллар США", "В) Британский фунт"],
        "answer": "Б"
    },
    {
        "question": "Что такое рецессия?",
        "options": ["А) Экономический рост", "Б) Экономический спад", "В) Стабильная экономика"],
        "answer": "Б"
    },
    {
        "question": "Кто является главой Центрального банка России?",
        "options": ["А) Министр финансов", "Б) Председатель ЦБ РФ", "В) Премьер-министр"],
        "answer": "Б"
    },
    {
        "question": "Что такое фискальная политика?",
        "options": ["А) Политика в области налогов и расходов", "Б) Денежная политика", "В) Торговая политика"],
        "answer": "А"
    },
    {
        "question": "Какой налог является прямым?",
        "options": ["А) НДС", "Б) Подоходный налог", "В) Акциз"],
        "answer": "Б"
    },
    {
        "question": "Что показывает коэффициент Джини?",
        "options": ["А) Уровень инфляции", "Б) Неравенство доходов", "В) Экономический рост"],
        "answer": "Б"
    },
    {
        "question": "Какая организация публикует данные о ВВП России?",
        "options": ["А) Росстат", "Б) ЦБ РФ", "В) Минэкономразвития"],
        "answer": "А"
    },
    {
        "question": "Что такое мультипликатор в экономике?",
        "options": ["А) Коэффициент роста инвестиций", "Б) Коэффициент увеличения ВВП", "В) Коэффициент инфляции"],
        "answer": "Б"
    },
    {
        "question": "Какой показатель характеризует покупательную способность валюты?",
        "options": ["А) Номинальный курс", "Б) Реальный курс", "В) Официальный курс"],
        "answer": "Б"
    },
    {
        "question": "Что такое стагфляция?",
        "options": ["А) Рост + инфляция", "Б) Спад + дефляция", "В) Стагнация + инфляция"],
        "answer": "В"
    },
    {
        "question": "Какой вид безработицы связан с поиском новой работы?",
        "options": ["А) Структурная", "Б) Фрикционная", "В) Циклическая"],
        "answer": "Б"
    },
    {
        "question": "Что такое ликвидность?",
        "options": ["А) Способность активов превращаться в деньги", "Б) Доходность инвестиций", "В) Уровень риска"],
        "answer": "А"
    },
    {
        "question": "Что такое торговый баланс?",
        "options": ["А) Разность между экспортом и импортом", "Б) Общий объем торговли", "В) Курс национальной валюты"],
        "answer": "А"
    },
    {
        "question": "Какую функцию выполняют центральные банки?",
        "options": ["А) Регулирование денежного обращения", "Б) Налогообложение", "В) Социальная поддержка"],
        "answer": "А"
    },
    {
        "question": "Что такое эмиссия денег?",
        "options": ["А) Изъятие денег из обращения", "Б) Выпуск новых денег", "В) Обмен валют"],
        "answer": "Б"
    },
    {
        "question": "Какой показатель измеряет общий уровень цен в экономике?",
        "options": ["А) ИПЦ (Индекс потребительских цен)", "Б) ВВП", "В) Уровень безработицы"],
        "answer": "А"
    },
    {
        "question": "Что означает профицит бюджета?",
        "options": ["А) Превышение расходов над доходами", "Б) Превышение доходов над расходами", "В) Равенство доходов и расходов"],
        "answer": "Б"
    }
]

# Словарь экономических терминов
economics_dictionary = {
    "ВВП": "Валовой внутренний продукт - общая рыночная стоимость всех товаров и услуг, произведенных в стране за определенный период.",
    "Инфляция": "Устойчивое повышение общего уровня цен на товары и услуги в экономике.",
    "Дефляция": "Снижение общего уровня цен в экономике, противоположность инфляции.",
    "Рецессия": "Период экономического спада, характеризующийся сокращением ВВП в течение двух или более кварталов подряд.",
    "Ключевая ставка": "Процентная ставка, по которой центральный банк предоставляет кредиты коммерческим банкам.",
    "Девальвация": "Снижение курса национальной валюты по отношению к другим валютам.",
    "Фискальная политика": "Государственная политика в области налогообложения и государственных расходов.",
    "Монетарная политика": "Политика центрального банка по управлению денежной массой и процентными ставками.",
    "Безработица": "Состояние экономики, при котором часть трудоспособного населения не может найти работу.",
    "Ликвидность": "Способность актива быстро превращаться в наличные деньги без существенной потери стоимости."
}

# Полезные ссылки
useful_links = {
    "📈 Центральный банк РФ": "https://cbr.ru - Официальный сайт ЦБ РФ с данными о ключевой ставке, курсах валют",
    "📊 Росстат": "https://rosstat.gov.ru - Федеральная служба государственной статистики",
    "💼 Минэкономразвития": "https://economy.gov.ru - Министерство экономического развития РФ",
    "🌍 МВФ": "https://imf.org - Международный валютный фонд",
    "📰 РБК Экономика": "https://rbc.ru/economics - Экономические новости",
    "📈 Investing.com": "https://ru.investing.com - Финансовые рынки и аналитика",
    "📚 Экономикс": "https://economicus.ru - Образовательный ресурс по экономике"
}

# Экономические формулы
economic_formulas = {
    "Темп инфляции": "((ИПЦ_текущий - ИПЦ_базовый) / ИПЦ_базовый) × 100%",
    "Реальный ВВП": "Номинальный ВВП / Дефлятор ВВП",
    "Уровень безработицы": "(Количество безработных / Рабочая сила) × 100%",
    "Реальная процентная ставка": "Номинальная ставка - Темп инфляции",
    "Мультипликатор расходов": "1 / (1 - Предельная склонность к потреблению)",
    "Эластичность спроса": "% изменения количества / % изменения цены",
    "Производительность труда": "Выпуск продукции / Количество рабочих часов"
}

# Темы для докладов
presentation_topics = [
    "🏦 Роль Центрального банка в экономике России",
    "💱 Влияние курса рубля на российскую экономику",
    "📈 Анализ динамики ВВП России за последние 10 лет",
    "🏭 Структурные проблемы российской экономики",
    "🌍 Влияние санкций на экономику России",
    "⚡ Энергетический сектор как драйвер экономики",
    "🌾 Роль аграрного сектора в экономике России",
    "💼 Малый и средний бизнес: проблемы и перспективы",
    "🏗️ Инфраструктурные проекты и их экономический эффект",
    "📊 Цифровая экономика в России: состояние и развитие",
    "🏛️ Бюджетная политика и государственный долг",
    "🎯 Инновационная экономика и стартап-экосистема",
    "🌐 Международная торговля и экспортная политика",
    "👥 Демографические вызовы для экономики",
    "🏢 Банковская система России: современное состояние"
]

# Функция для создания главной клавиатуры
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🖋️ Проверь себя"), KeyboardButton("📊 Моя статистика")],
        [KeyboardButton("🏆 Рейтинг"), KeyboardButton("📚 Словарь терминов")],
        [KeyboardButton("📈 Полезные ссылки"), KeyboardButton("📒 Курс лекций")],
        [KeyboardButton("📽️ Темы докладов"), KeyboardButton("📐 Формулы")],
        [KeyboardButton("📰 Новости"), KeyboardButton("❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция викторины
async def quiz_question(update: Update):
    user_id = update.effective_user.id
    question = random.choice(quiz_questions)
    
    # Сохраняем состояние пользователя
    user_states[user_id] = {
        'mode': 'quiz',
        'current_question': question
    }
    
    text = f"🧠 Вопрос:\n{question['question']}\n\n"
    for option in question['options']:
        text += f"{option}\n"
    text += f"\nОтветьте буквой (А, Б или В)"
    await update.message.reply_text(text)

# Функция проверки ответа
async def check_quiz_answer(update: Update, user_answer: str):
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "Аноним"
    
    if user_id not in user_states or user_states[user_id]['mode'] != 'quiz':
        return False
    
    # Инициализация счета пользователя если его нет
    if user_id not in user_scores:
        user_scores[user_id] = {
            'name': username,
            'correct': 0,
            'incorrect': 0,
            'total': 0
        }
    
    correct_answer = user_states[user_id]['current_question']['answer']
    user_answer = user_answer.upper().strip()
    
    # Обновляем статистику
    user_scores[user_id]['total'] += 1
    
    if user_answer == correct_answer:
        user_scores[user_id]['correct'] += 1
        score = user_scores[user_id]
        percentage = round((score['correct'] / score['total']) * 100, 1)
        await update.message.reply_text(
            f"✅ Правильно! Отличная работа! 🎉\n\n"
            f"📊 Ваша статистика:\n"
            f"Правильных ответов: {score['correct']}\n"
            f"Всего вопросов: {score['total']}\n"
            f"Процент правильных: {percentage}%",
            reply_markup=get_main_keyboard()
        )
    else:
        user_scores[user_id]['incorrect'] += 1
        score = user_scores[user_id]
        percentage = round((score['correct'] / score['total']) * 100, 1)
        await update.message.reply_text(
            f"❌ Неверно. Правильный ответ: {correct_answer}\n\n"
            f"📊 Ваша статистика:\n"
            f"Правильных ответов: {score['correct']}\n"
            f"Всего вопросов: {score['total']}\n"
            f"Процент правильных: {percentage}%",
            reply_markup=get_main_keyboard()
        )
    
    # Очищаем состояние пользователя
    del user_states[user_id]
    return True

# Функция показа словаря терминов
async def show_dictionary(update: Update):
    text = "📚 Словарь экономических терминов:\n\n"
    for term, definition in economics_dictionary.items():
        text += f"🔹 <b>{term}</b>\n{definition}\n\n"
    
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=get_main_keyboard())

# Функция показа полезных ссылок
async def show_useful_links(update: Update):
    text = "📈 Полезные ресурсы по экономике:\n\n"
    for name, link in useful_links.items():
        text += f"{name}\n{link}\n\n"
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# Функция показа курса лекций
async def show_course(update: Update):
    course_text = (
        "📒 Курс лекций по экономике:\n\n"
        "📖 <b>Модуль 1: Основы экономической теории</b>\n"
        "• Предмет и методы экономической науки\n"
        "• Базовые экономические понятия\n"
        "• Типы экономических систем\n\n"
        "📖 <b>Модуль 2: Микроэкономика</b>\n"
        "• Спрос и предложение\n"
        "• Эластичность\n"
        "• Поведение потребителя\n"
        "• Теория фирмы\n\n"
        "📖 <b>Модуль 3: Макроэкономика</b>\n"
        "• ВВП и национальные счета\n"
        "• Инфляция и безработица\n"
        "• Денежно-кредитная политика\n"
        "• Фискальная политика\n\n"
        "📖 <b>Модуль 4: Международная экономика</b>\n"
        "• Международная торговля\n"
        "• Валютные отношения\n"
        "• Платежный баланс\n\n"
        "💡 Для углубленного изучения рекомендуем использовать раздел 'Полезные ссылки'"
    )
    await update.message.reply_text(course_text, parse_mode='HTML', reply_markup=get_main_keyboard())

# Функция показа тем докладов
async def show_presentation_topics(update: Update):
    text = "📽️ Темы для докладов и исследований:\n\n"
    for i, topic in enumerate(presentation_topics, 1):
        text += f"{i}. {topic}\n"
    
    text += f"\n💡 Выберите тему, которая вас интересует, и проведите собственное исследование!"
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# Функция показа формул
async def show_formulas(update: Update):
    text = "📐 Основные экономические формулы:\n\n"
    for formula_name, formula in economic_formulas.items():
        text += f"🔹 <b>{formula_name}</b>\n{formula}\n\n"
    
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=get_main_keyboard())

# Функция показа новостей
async def show_news(update: Update):
    news_text = (
        "📰 Источники экономических новостей:\n\n"
        "🔸 <b>Российские источники:</b>\n"
        "• РБК Экономика - rbc.ru/economics\n"
        "• Ведомости - vedomosti.ru\n"
        "• Коммерсантъ - kommersant.ru\n"
        "• Экономика РИА Новости - ria.ru/economy\n\n"
        "🔸 <b>Международные источники:</b>\n"
        "• Bloomberg - bloomberg.com\n"
        "• Financial Times - ft.com\n"
        "• The Economist - economist.com\n"
        "• Reuters Economics - reuters.com\n\n"
        "🔸 <b>Аналитические ресурсы:</b>\n"
        "• Центр развития НИУ ВШЭ\n"
        "• Институт экономической политики им. Гайдара\n"
        "• Аналитический центр при Правительстве РФ\n\n"
        "📊 Регулярно следите за экономическими новостями для понимания текущих трендов!"
    )
    await update.message.reply_text(news_text, parse_mode='HTML', reply_markup=get_main_keyboard())

# Функция показа рейтинга
async def show_leaderboard(update: Update):
    if not user_scores:
        await update.message.reply_text(
            "🏆 Рейтинг пуст. Начните викторину, чтобы попасть в топ!",
            reply_markup=get_main_keyboard()
        )
        return
    
    # Сортируем по проценту правильных ответов, затем по количеству правильных
    sorted_users = sorted(
        user_scores.items(),
        key=lambda x: (x[1]['correct'] / max(x[1]['total'], 1), x[1]['correct']),
        reverse=True
    )
    
    text = "🏆 Топ-10 участников:\n\n"
    for i, (user_id, score) in enumerate(sorted_users[:10], 1):
        percentage = round((score['correct'] / max(score['total'], 1)) * 100, 1)
        text += f"{i}. {score['name']} - {percentage}% ({score['correct']}/{score['total']})\n"
    
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "друг"
    welcome_text = (
        f"👋 Привет, {user_name}! Добро пожаловать в образовательный центр по экономике!\n\n"
        f"📚 Доступные разделы:\n"
        f"🖋️ Проверь себя - викторина с оценками\n"
        f"📊 Моя статистика - ваши результаты\n"
        f"🏆 Рейтинг - топ участников викторины\n"
        f"📚 Словарь терминов - основные понятия\n"
        f"📈 Полезные ссылки - важные ресурсы\n"
        f"📒 Курс лекций - учебные материалы\n"
        f"📽️ Темы докладов - идеи для работ\n"
        f"📐 Формулы - экономические формулы\n"
        f"📰 Новости - экономические новости\n\n"
        f"Используйте кнопки меню для навигации!"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# Команда /quiz
async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await quiz_question(update)

# Команда /stats
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_scores:
        await update.message.reply_text(
            "📊 У вас пока нет статистики. Начните викторину!",
            reply_markup=get_main_keyboard()
        )
        return
    
    score = user_scores[user_id]
    percentage = round((score['correct'] / max(score['total'], 1)) * 100, 1)
    
    stats_text = (
        f"📊 Ваша статистика:\n\n"
        f"👤 Имя: {score['name']}\n"
        f"✅ Правильных ответов: {score['correct']}\n"
        f"❌ Неправильных ответов: {score['incorrect']}\n"
        f"📝 Всего вопросов: {score['total']}\n"
        f"📈 Процент правильных: {percentage}%\n\n"
    )
    
    # Определяем уровень знаний
    if percentage >= 90:
        stats_text += "🏆 Уровень: Эксперт по экономике!"
    elif percentage >= 75:
        stats_text += "🥇 Уровень: Продвинутый"
    elif percentage >= 60:
        stats_text += "🥈 Уровень: Хороший"
    elif percentage >= 40:
        stats_text += "🥉 Уровень: Базовый"
    else:
        stats_text += "📚 Уровень: Начинающий"
    
    await update.message.reply_text(stats_text, reply_markup=get_main_keyboard())

# Команда /leaderboard
async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_leaderboard(update)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "❓ Помощь по образовательному центру:\n\n"
        "🖋️ <b>Проверь себя</b>:\n"
        "• Викторина с вопросами по экономике\n"
        "• Отвечайте буквами А, Б или В\n"
        "• Результаты сохраняются в статистике\n\n"
        "📊 <b>Моя статистика</b>:\n"
        "• Ваши результаты викторины\n"
        "• Процент правильных ответов\n"
        "• Уровень знаний\n\n"
        "🏆 <b>Рейтинг</b>:\n"
        "• Топ-10 лучших участников\n"
        "• Сравнение с другими пользователями\n\n"
        "📚 <b>Словарь терминов</b>:\n"
        "• Основные экономические понятия\n"
        "• Определения и объяснения\n\n"
        "📈 <b>Полезные ссылки</b>:\n"
        "• Важные экономические ресурсы\n"
        "• Официальные источники данных\n\n"
        "📒 <b>Курс лекций</b>:\n"
        "• Структурированные учебные материалы\n"
        "• От основ до продвинутых тем\n\n"
        "📽️ <b>Темы докладов</b>:\n"
        "• Идеи для исследований\n"
        "• Актуальные экономические вопросы\n\n"
        "📐 <b>Формулы</b>:\n"
        "• Основные экономические расчеты\n"
        "• Формулы с объяснениями\n\n"
        "📰 <b>Новости</b>:\n"
        "• Источники экономических новостей\n"
        "• Российские и международные ресурсы"
    )
    await update.message.reply_text(help_text, parse_mode='HTML', reply_markup=get_main_keyboard())

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Проверяем, находится ли пользователь в режиме викторины
    if await check_quiz_answer(update, text):
        return
    
    # Обработка кнопок клавиатуры
    if text == "🖋️ Проверь себя":
        await quiz_question(update)
    elif text == "📊 Моя статистика":
        await stats_command(update, context)
    elif text == "🏆 Рейтинг":
        await leaderboard_command(update, context)
    elif text == "📚 Словарь терминов":
        await show_dictionary(update)
    elif text == "📈 Полезные ссылки":
        await show_useful_links(update)
    elif text == "📒 Курс лекций":
        await show_course(update)
    elif text == "📽️ Темы докладов":
        await show_presentation_topics(update)
    elif text == "📐 Формулы":
        await show_formulas(update)
    elif text == "📰 Новости":
        await show_news(update)
    elif text == "❓ Помощь":
        await help_command(update, context)
    else:
        # Если сообщение не распознано
        await update.message.reply_text(
            "🤔 Не понимаю команду. Используйте кнопки меню или команду /help для получения помощи.",
            reply_markup=get_main_keyboard()
        )

# Функция для обработки ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Exception while handling an update: {context.error}")

# Основная функция
def main():
    if not TOKEN:
        print("❌ Ошибка: Не найден токен бота. Проверьте переменную окружения TELEGRAM_BOT_TOKEN")
        return
    
    print("🤖 Запуск экономического викторина-бота...")
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
