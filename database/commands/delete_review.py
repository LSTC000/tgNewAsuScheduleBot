from database import Reviews


async def delete_review(review_id: int) -> None:
    """delete review from the database.

        Args:
            review_id (int): Review ID to delete.
        """

    return await Reviews.delete.where(Reviews.id == review_id).gino.scalar()
