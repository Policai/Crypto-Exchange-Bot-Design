# Полная инструкция: запуск с нуля (Windows, очень подробно)

Эта инструкция написана максимально простым языком: **что скачать, куда нажать, что вставить, какие команды ввести**.

---

## 0) Что мы будем делать

Вы поднимете систему из 5 сервисов:
1. PostgreSQL (база данных)
2. Backend API (FastAPI)
3. Telegram Bot (aiogram)
4. WebApp (React)
5. Admin Panel (React)

Запуск будет через Docker, поэтому не нужно вручную ставить Python/Postgres/Node.

---

## 1) Установка программ (1 раз)

### 1.1 Установите Docker Desktop
1. Откройте сайт: https://www.docker.com/products/docker-desktop/
2. Нажмите **Download for Windows**.
3. Запустите скачанный файл.
4. Нажимайте **Next / Install**.
5. После установки перезагрузите ПК (если попросит).
6. Запустите Docker Desktop из меню Пуск.
7. Дождитесь статуса **Docker Desktop is running**.

### 1.2 Установите Git for Windows
1. Откройте сайт: https://git-scm.com/download/win
2. Скачайте установщик.
3. Установите (можно везде оставлять настройки по умолчанию).

### 1.3 (Опционально, но удобно) Установите VS Code
1. Сайт: https://code.visualstudio.com/
2. Установите стандартно.

---

## 2) Проверка, что всё установилось

1. Нажмите клавиши **Win + R**.
2. Введите `powershell` и нажмите Enter.
3. По очереди выполните команды:

```powershell
docker --version
docker compose version
git --version
```

Если команды показывают версии — всё хорошо.

---

## 3) Получить проект на компьютер

> Если проект уже у вас распакован в папке — переходите к шагу 4.

### Вариант A (через Git)
1. Откройте PowerShell.
2. Перейдите, например, на рабочий стол:

```powershell
cd $HOME\Desktop
```

3. Клонируйте репозиторий:

```powershell
git clone <ССЫЛКА_НА_РЕПО>
```

4. Откройте папку проекта:

```powershell
cd .\Crypto-Exchange-Bot-Design
```

### Вариант B (если ZIP)
1. Скачайте ZIP с проектом.
2. Нажмите по ZIP **правой кнопкой мыши**.
3. Нажмите **Извлечь все...**.
4. Выберите папку (например, Рабочий стол).
5. Откройте распакованную папку `Crypto-Exchange-Bot-Design`.

---

## 4) Как открыть нужную папку правильно

Нужно попасть в папку **`project`**.

### Способ 1 (через проводник + правая кнопка)
1. Откройте проводник и зайдите в папку `Crypto-Exchange-Bot-Design`.
2. Откройте папку `project`.
3. Внутри пустого места окна нажмите **правой кнопкой мыши**.
4. Выберите:
   - **Open in Terminal** (Windows 11), или
   - **Открыть окно PowerShell здесь** (Windows 10, если доступно).

### Способ 2 (через команду)
В PowerShell:

```powershell
cd C:\ПУТЬ\ДО\Crypto-Exchange-Bot-Design\project
```

Пример:

```powershell
cd C:\Users\Ivan\Desktop\Crypto-Exchange-Bot-Design\project
```

---

## 5) Создание Telegram-бота и токена

1. Откройте Telegram.
2. Найдите **@BotFather**.
3. Нажмите **Start**.
4. Отправьте команду:

```
/newbot
```

5. Введите имя бота (любое).
6. Введите username бота (должен заканчиваться на `bot`, например `my_exchange_super_bot`).
7. BotFather пришлёт сообщение с токеном вида:

```
123456789:AAHh....
```

8. Скопируйте этот токен — он нужен для `BOT_TOKEN`.

---

## 6) WebApp URL — как сделать (очень просто)

Telegram WebApp **не откроется** по `http://localhost...` внутри Telegram. Нужен **публичный HTTPS URL**.

Самый простой вариант для новичка — **ngrok**.

### 6.1 Установить ngrok
1. Перейдите на сайт: https://ngrok.com/
2. Зарегистрируйтесь (бесплатно).
3. Скачайте ngrok для Windows.
4. Распакуйте архив (например, в `C:\ngrok`).
5. Откройте PowerShell и выполните команду авторизации (её выдаёт сайт ngrok в личном кабинете), например:

```powershell
ngrok config add-authtoken ВАШ_NGROK_TOKEN
```

### 6.2 Запустить туннель для WebApp
После запуска проекта (шаг 9) выполните в отдельном PowerShell:

```powershell
ngrok http 5173
```

Вы увидите URL вида:

```
https://abc123.ngrok-free.app
```

Это и есть ваш `WEBAPP_URL`.

---

## 7) Где вставить свои данные (.env)

1. В папке `project` найдите файл `.env`.
2. Нажмите на него **правой кнопкой мыши**.
3. Выберите **Open with Code** (или Блокнот).
4. Замените значения на свои:

```env
BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
BACKEND_URL=http://backend:8000
WEBAPP_URL=https://ВАШ_URL_ОТ_NGROK_ИЛИ_ДОМЕНА
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/exchange
JWT_SECRET=ПРИДУМАЙТЕ_ДЛИННЫЙ_СЛОЖНЫЙ_СЕКРЕТ_МИН_32_СИМВОЛА
CRYPTOBOT_TOKEN=ВАШ_ТОКЕН_ОТ_CRYPTOBOT_ИЛИ_CHANGE_ME
```

5. Сохраните файл: **Ctrl + S**.

### Что нельзя менять без необходимости
- `BACKEND_URL` — оставьте как есть
- `DATABASE_URL` — для локального запуска оставьте как есть

---

## 8) (Важно) Настроить WebApp у BotFather

1. Снова откройте `@BotFather`.
2. Команда:

```
/mybots
```

3. Выберите вашего бота.
4. Откройте настройки Web App (пункт может называться **Bot Settings** → **Menu Button** / **Web App**).
5. Вставьте ваш `WEBAPP_URL` (например `https://abc123.ngrok-free.app`).
6. Сохраните.

> Если сменится ссылка ngrok — нужно снова обновить `WEBAPP_URL` в `.env` и в BotFather.

---

## 9) Запуск проекта

Откройте терминал в папке `project` и выполните:

```powershell
docker compose up --build -d
```

Подождите 1–5 минут (первый запуск дольше, т.к. скачиваются образы).

Проверка:

```powershell
docker compose ps
```

Должны быть сервисы: `db`, `backend`, `bot`, `webapp`, `admin-panel`.

---

## 10) Как проверить, что всё работает

### 10.1 Backend
Откройте в браузере:
- http://localhost:8000/docs

Если открылась Swagger-страница — backend работает.

### 10.2 WebApp локально
Откройте:
- http://localhost:5173

### 10.3 Admin Panel
Откройте:
- http://localhost:5174

### 10.4 Telegram бот
1. Откройте бота в Telegram.
2. Нажмите **Start**.
3. Отправьте контакт через кнопку.
4. Нажмите кнопку открытия WebApp.

---

## 11) Полезные команды (копируйте как есть)

### Посмотреть логи всех сервисов
```powershell
docker compose logs --tail=200
```

### Логи только бота
```powershell
docker compose logs bot --tail=200
```

### Логи backend
```powershell
docker compose logs backend --tail=200
```

### Перезапуск после изменений
```powershell
docker compose up --build -d
```

### Остановить всё
```powershell
docker compose down
```

---

## 12) Частые ошибки и что делать

### Ошибка: `docker: command not found`
Docker не установлен или не запущен. Установите/запустите Docker Desktop.

### Бот не отвечает
- Проверьте правильность `BOT_TOKEN` в `.env`.
- Проверьте логи:
  ```powershell
  docker compose logs bot --tail=200
  ```

### WebApp не открывается в Telegram
- `WEBAPP_URL` должен быть **https**.
- Убедитесь, что URL вставлен в BotFather.
- Если используете ngrok: возможно, ссылка изменилась — обновите её в `.env` и BotFather.

### Не запускается база
Проверьте, не занят ли порт 5432 другой программой.

---

## 13) Как менять проект под себя

### Дизайн WebApp
Файлы:
- `project/webapp/react-app/src/pages/App.jsx`
- `project/webapp/react-app/src/styles/app.css`

### Логика API
Файлы:
- `project/backend/api/*.py`
- `project/backend/services/*.py`
- `project/backend/models/*.py`

### Telegram-бот
Файлы:
- `project/bot/handlers/start.py`
- `project/bot/bot.py`

После правок:

```powershell
docker compose up --build -d
```

---

## 14) Перенос на VPS в будущем

1. Установить Docker на VPS.
2. Скопировать этот проект на сервер.
3. Заполнить `.env` прод-значениями.
4. Настроить домен + HTTPS (Nginx/Caddy + Let's Encrypt).
5. Выполнить:

```bash
docker compose up --build -d
```

Сама архитектура уже готова к переносу, потому что всё в Docker.
