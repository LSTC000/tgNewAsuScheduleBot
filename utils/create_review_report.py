def create_review_report(review_id: int, user_id: int, review: str, created_date: str) -> str:
    """
    Args:
        review_id (int): review_id.
        user_id (int): Telegram user id.
        review (str): User review.
        created_date (str): Date of create review.

    Returns:
        str: Review report.
    """

    report = '''
<b>ID {}</b>
    
🧑‍💻 {}
    
📅 {}
    
✏️ {}
    '''

    return report.format(review_id, user_id, created_date, review)
