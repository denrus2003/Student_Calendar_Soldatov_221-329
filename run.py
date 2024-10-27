from app import create_app, db
from flask_migrate import Migrate

# Создаем приложение с помощью функции-фабрики
app = create_app()

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()