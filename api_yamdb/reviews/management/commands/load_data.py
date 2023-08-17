import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class Command(BaseCommand):
    help = "Загрузка данных из CSV-файлов"

    def create_category(self, model, row):
        Category.objects.create(
            id=row["id"], name=row["name"], slug=row["slug"]
        )

    def create_genre(self, model, row):
        Genre.objects.create(id=row["id"], name=row["name"], slug=row["slug"])

    def create_title(self, model, row):
        category = Category.objects.get(pk=row["category"])
        model.objects.create(
            id=row["id"],
            name=row["name"],
            year=row["year"],
            category=category,
        )

    def create_user(self, model, row):
        User.objects.create(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            role=row["role"],
            bio=row["bio"],
            first_name=row["first_name"],
            last_name=row["last_name"],
        )

    def create_review(self, model, row):
        title = Title.objects.get(pk=row["title_id"])
        author = User.objects.get(pk=row["author"])
        model.objects.create(
            id=row["id"],
            text=row["text"],
            score=row["score"],
            title=title,
            author=author,
            pub_date=row["pub_date"],
        )

    def create_comment(self, model, row):
        review = Review.objects.get(pk=row["review_id"])
        author = User.objects.get(pk=row["author"])
        model.objects.create(
            id=row["id"],
            text=row["text"],
            review=review,
            author=author,
            pub_date=row["pub_date"],
        )

    def add_genre_to_title(self, model, row):
        title = Title.objects.get(pk=row["title_id"])
        genre = Genre.objects.get(pk=row["genre_id"])
        title.genre.add(genre)

    def handle(self, *args, **kwargs):
        if any(
            model.objects.exists()
            for model in [Category, Genre, Title, Review, Comment, User]
        ):
            return "В базе данных уже есть данные, загрузка невозможна"

        models_data = [
            (Category, "category.csv", self.create_category),
            (Genre, "genre.csv", self.create_genre),
            (Title, "titles.csv", self.create_title),
            (User, "users.csv", self.create_user),
            (Review, "review.csv", self.create_review),
            (Comment, "comments.csv", self.create_comment),
            (None, "genre_title.csv", self.add_genre_to_title),
        ]

        for model, filename, handler in models_data:
            with open(f"static/data/{filename}", encoding="utf8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    handler(model, row)

        self.stdout.write(
            self.style.SUCCESS("Импорт данных завершился успешно!")
        )
