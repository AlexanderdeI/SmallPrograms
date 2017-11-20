import notify2
from . import rates


def notify():
    ICON_PATH = '/home/alexdei/PycharmProjects/SmallPrograms/Crypto_Notifier/icons/bitcoin.png'

    # Получаем текущий курс
    bitcoin = rates.fetch_bitcoin()

    # Инициализируем d-bus соединение
    notify2.init("Cryptocurrency rates notifier")

    # Создаем Notification-объект
    n = notify2.Notification("Crypto Notifier", icon=ICON_PATH)

    # Устанавливаем скорость срочности
    n.set_urgency(notify2.URGENCY_NORMAL)

    # Устанавливаем задержку
    n.set_timeout(1000)

    result = '{0} - {1}'.format(*bitcoin)

    # Обновляем содержимое
    n.update("Current rate", result)

    # Показываем уведомление
    n.show()


if __name__ == '__main__':
    notify()