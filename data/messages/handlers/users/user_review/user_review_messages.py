from data.config import MAX_REVIEW_LENGTH


ENTER_USER_REVIEW_MESSAGE = (f'✏ Введите отзыв о нашем боте...\n\n❗ Длина отзыва не должна превышать '
                             f'<b>{MAX_REVIEW_LENGTH}</b> символов.')
CONFIRM_USER_REVIEW_MESSAGE = '❓ Вы действительно хотите отправить этот отзыв:\n\n{}'
ERROR_ENTER_USER_REVIEW_MESSAGE = (f'❗ Отзыв введён некорректно.\n\nПожалуйста, убедитесь, что ваш отзыв не превышает '
                                   f'<b>{MAX_REVIEW_LENGTH}</b> символов!')
SUCCESSFUL_ENTER_USER_REVIEW_MESSAGE = '✅ Ваш отзыв был успешно сохранён'
