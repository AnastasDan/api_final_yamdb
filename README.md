![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=flat&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-ff1709?style=flat&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=flat&logo=github&logoColor=white)

# Проект «YaMDb»

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь **нельзя посмотреть** фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха.

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только **администратор**.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только **один** отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только **аутентифицированные** пользователи.

## Как запустить проект:

Клонируем себе репозиторий:

```
git clone git@github.com:AnastasDan/api_final_yamdb.git
```

Переходим в директорию:

```
cd api_final_yamdb
```

Cоздаем и активируем виртуальное окружение:

* Если у вас Linux/MacOS:

    ```
    python3 -m venv venv
    ```

    ```
    source venv/bin/activate
    ```

* Если у вас Windows:

    ```
    python -m venv venv
    ```

    ```
    source venv/Scripts/activate
    ```

Устанавливаем зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создаем файл .env и заполняем его. Список данных указан в файле env.example.

Выполняем миграции:

```
python manage.py migrate
```

Запускаем проект:

```
python manage.py runserver
```

## Где посмотреть примеры запросов к API:

После запуска проекта переходим по этой ссылке:

http://127.0.0.1:8000/redoc/

## Автор проекта

[Anastas Danielian](https://github.com/AnastasDan)