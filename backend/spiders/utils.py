from datetime import datetime

from money import Money


def convert_price_to_money(price: str, currency: str) -> Money:
    return Money(amount=float(price), currency=currency)


def combine_date_and_time(date: datetime, time: str, format="%H:%M") -> datetime:
    time = datetime.strptime(time, format).time()
    return datetime.combine(date, time)
