class Validator:
    def __init__(self):
        pass

    def alert_validation(self, alert: str) -> bool:
        """
        :param alert: Text for the alert.
        :return: True if alert is valid, else - False
        """

        return True if alert else False

    def user_review_validation(self, review: str) -> bool:
        """
        :param review: User review.
        :return: True if review is valid, else - False
        """

        return True if review and len(review) <= 2048 else False

    def limit_view_reviews_validation(self, limit: str, max_limit: int) -> bool:
        """
        :param limit: Limit reviews for view.
        :param max_limit: Count reviews.
        :return: True if limit is valid, else - False
        """

        try:
            limit = int(limit)

            if limit < 1 or limit > max_limit:
                return False
        except ValueError:
            return False

        return True
