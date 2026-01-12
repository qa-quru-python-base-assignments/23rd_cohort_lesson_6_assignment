from part_a_email_functions import *


def sender_email(recipient_list: list[str],
                 subject: str,
                 body: str,
                 sender: str) -> list[str]:
    # 1. Проверить, что список получателей не пустой
    if not recipient_list:
        return []

    # 2. Проверить корректность email адресов
    validated_sender = get_correct_email([sender])
    validated_recipient_list = get_correct_email(recipient_list)
    if not validated_sender or not validated_recipient_list:
        return []
    sender = validated_sender[0]
    recipient_list = validated_recipient_list

    # 3. Проверить заполненность темы и тела письма
    is_subject_empty, is_body_empty = check_empty_fields(subject, body)
    if is_subject_empty or is_body_empty:
        return []

    # 4. Исключить отправку самому себе
    recipient_list = [
        recipient for recipient in recipient_list if normalize_address(recipient) != normalize_address(sender)
    ]
    if not recipient_list:  # проверка, что после удаления в списке остались элементы
        return []

    # 5. Нормализовать все текстовые данные
    subject = clean_body_text(subject)
    body = clean_body_text(body)
    sender = normalize_address(sender)
    recipient_list = [normalize_address(recipient) for recipient in recipient_list]

    # 6. Создать письмо для каждого получателя
    email_list = [create_email(sender, recipient, subject, body) for recipient in recipient_list]

    # 7. Добавить дату отправки
    email_list = [add_send_date(email) for email in email_list]

    # 8. Замаскировать email отправителя
    login, domain = extract_login_domain(sender)
    masked_sender = mask_sender_email(login, domain)
    for email in email_list:
        email['sender'] = masked_sender

    # 9. Создать короткую версию тела письма
    email_list = [add_short_body(email) for email in email_list]

    # 10. Сформировать итоговый текст письма
    return [build_sent_text(email) for email in email_list]


if __name__ == "__main__":
    # Список email для проверки из задания
    test_emails = [
        "default@study.com",  # Совпадает с дефолтным отправителем
        " hello@corp.ru   ",
        "user@site.NET",
        "user@domain.coM",
        "user.name@domain.ru",
        "usergmail.com",  # Invalid
        "user@domain",  # Invalid
        "user@domain.org",  # Invalid (.org нет в условии)
        "@mail.ru",  # Формально валиден по @ и .ru, но без логина
        "name@.com",  # Формально валиден по @ и .com
        "name@domain.comm",  # Invalid
        "",  # Invalid
        "   ",  # Invalid
    ]

    # Параметры письма
    sender = "default@study.com"
    subj = "Hello!\tFriend"
    msg = "Привет,\nдруг!   Как дела?"

    # Запуск функции
    sent_letters = sender_email(
        test_emails,
        subj,
        msg,
        sender
    )

    # Вывод результатов
    print(f"Всего отправлено писем: {len(sent_letters)}\n")

    for letter in sent_letters:
        print("-" * 40)
        print(letter)
