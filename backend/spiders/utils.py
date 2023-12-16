from datetime import datetime

from money import Money


def convert_price_to_money(price: str, currency: str) -> Money:
    return Money(amount=float(price[1:]), currency=currency)


def combine_date_and_time(date: datetime, time: str) -> datetime:
    time = datetime.strptime(time, "%H:%M").time()
    return datetime.combine(date, time)
