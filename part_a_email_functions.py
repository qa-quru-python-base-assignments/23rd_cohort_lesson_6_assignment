import re
from datetime import date


def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()


def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    email_copy = email.copy()
    email_copy["short_body"] = f"{email_copy["body"][:10]}..."
    return email_copy


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return re.sub(r"[\n\t]+", " ", body)


def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    recipient = normalize_addresses(email['to'])
    sender = normalize_addresses(email['from'])
    subject = email['subject']
    # берем дату из словаря письма, если ее нет - используем сегодняшнюю
    send_date = email.get(
        "date",
        date.today().strftime("%Y-%m-%d")
    )
    clean_body = clean_body_text(email["body"])

    return (
        f"Кому: {recipient}, от {sender}\n"
        f"Тема: {subject}, дата {send_date}\n"
        f"{clean_body}"
    )


def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = not subject or not subject.strip()
    is_body_empty = not body or not body.strip()
    return is_subject_empty, is_body_empty


def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return f"{login[:2]}***@{domain}"


def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    correct_emails = []
    email_re = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|ru|net)$')
    for email in email_list:
        normalized_email = normalize_addresses(email)
        if email_re.fullmatch(normalized_email):
            correct_emails.append(email)  # добавляем в ненормализованном виде
    return correct_emails


def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body
    }


def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    email_copy = email.copy()
    email_copy["date"] = date.today().strftime("%Y-%m-%d")
    return email_copy


def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    login, domain = address.split("@")
    return login, domain
