# Unnatural language generation / Генератор неприродної мови

## Що це?

Це - примітивний генератор неприродної мови.
Він приймає на вхід текст та запам'ятовує зв'язки між словами, а після цього генерує речення заданої довжини на основі вхідної інформації.

## Як спробувати?

Telegram бот [@unnatural_language_bot](https://t.me/unnatural_language_bot)

## Як це працює?

Для того, щоб генерувати текст, програма має прочитати декілька вже готових.
Отриманий від користувача текст проходить декілька етапів:

1. Токенізація
2. Перетворення у граф

### Токенізація

Токенізація - процес розділення тексту на окремі частинки - слова та пунктуацію.
Пунктуація розглядається окремою частиною тексту, на тому ж рівні, що і слова.

Для токенізації використовується бібліотека [`tokenize_uk`](https://github.com/lang-uk/tokenize-uk).

### Перетворення у граф

Програма опрацьовує кожне речення окремо.
Вона по черзі бере слова з нього та записує зв'язки між ними в граф.
Вага зв'язку між двома словами у графі - це кількість випадків, коли слова зустрічалися разом у текстах.

### Приклад опрацювання тексту

Вхідний текст:

`Lorem ipsum dolor sit amet, consectetur adipiscing elit.`

Розділений на токени:

`[['lorem', 'ipsum', 'dolor', 'sit', 'amet', ',', 'consectetur', 'adipiscing', 'elit', '.']]`

Представлений у вигляді графа:

![image](https://user-images.githubusercontent.com/39884112/123977582-c9113700-d9c7-11eb-9e8b-7f9de9897f7e.png)

Кожен зв'язок має вагу 1, бо зустрічався всього один раз за весь текст. Якщо взяти цілий абзац _Lorem ipsum_, отримаємо такий граф:

![image](https://user-images.githubusercontent.com/39884112/123977950-21e0cf80-d9c8-11eb-8e16-56cd4fdede43.png)

Слів стало набагато більше, а деякі зв'язки мають вагу 2.

## Генерація тексту

Коли програма вже має граф, вона може генерувати нові тексти.
Їй потрібне перше слово речення, він якого вона може відштовхнутися.
Це має бути слово, що вже є в графі, адже інакше програма не зможе знайти наступне слово.
Кожне наступне слово випадково обирається з тих, що були пов'язані з поточним у графі, з урахуванням ваги зв'язків.
У графі можуть бути цикли і є імовірність, що програма буде вічно блукати в одному з них.

### Приклади

Завантажити тексти, використані для прикладів, можна тут: [GitHub Gist](https://gist.github.com/andrewyazura/98b612f4fe9c3075177d992495ccee12).

#### Кобзар

Після опрацювання повного тексту збірки **"Кобзар"**, програма згенерувала такий текст:

> сказилися кричать за землю він на всіх імператорів би нам , по долині - за темнії , і не наробить . мов за панною пішло . наплювали на базарі , хмара криє . під тином , скорбная , сину , козаки

#### Енеїда

**"Енеїда"** дала такі результати:

> вже дожидає і ветхого царя , вирвавшись надвір під дудку била задом , а для його щоб в другім отряді пішли к тому ж ! ти і думку пошибала к чортам ви швидче тарани . поодаль плив плив . нептун замудровав

та

> пожар залив водою чортзна де ждуть мене удруге не під буркой витягавсь . – паничу ! сількісь ! уже не захлебнувсь . – і небилиця , затрусивсь . – судьба вертить ! проклятії поганці , – не вдовольнившись , схвативши головешку

## Telegram bot

Для зручного користування програмою існує telegram бот - [@unnatural_language_bot](https://t.me/unnatural_language_bot).
Кожен користувач має свій граф і може додавати в нього нові слова, зв'язки чи очищати його.
Щоб запустити бота у себе потрібно зареєструвати свого бота через [@botfather](https://t.me/botfather) та ввести власні дані у `telegram_bot/bot_config.yml` та запустити `main_bot.py`.

### Команди

| Команда   | Значення                     |
| --------- | ---------------------------- |
| /generate | згенерувати текст            |
| /stats    | показати статистику про граф |
| /clear    | очистити свій граф           |

#### /stats

Команда `/stats` показує такі параметри:

1. Кількість слів (кількість нод у графі)
2. Кількість зв'язків між словами (кількість ребер графу)
3. Вага графу (сумма ваги кожного ребра графу)

### Адмінські команди

| Команда           | Значення                                |
| ----------------- | --------------------------------------- |
| /stats_all        | показати статистику кожного графа       |
| /clear\_user _id_ | очистити граф користувача з вказаним id |
| /clear_all        | очистити всі графи                      |

## Що не працює

Програма не розуміє контексту і не здатна відмінювати слова у реченні.

## Credits

Дякую за ідею [@danbst](https://github.com/danbst)
