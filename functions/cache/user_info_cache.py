from loader import user_info_cache

from database import (
    get_user_info, 
    add_user_info, 
    update_student_data, 
    update_lecturer_data, 
    update_user_alert
)


class UserInfoCache:
    def __init__(self, user_id: int) -> None:
        """
        Args:
            user_id (int): Telegram user id.
        """

        self.user_id = user_id

    async def get_user_info_cache(self) -> dict:
        """get user info

        Returns:
            dict: Dict with user info.
        """

        if self.user_id in user_info_cache:
            user_info = user_info_cache[self.user_id]
        else:
            user_info = await get_user_info(self.user_id)

            if user_info:
                user_info = {
                    'student_name': user_info[0][0],
                    'student_url': user_info[0][1],
                    'lecturer_name': user_info[0][2],
                    'lecturer_url': user_info[0][3],
                    'alert': user_info[0][4]
                }
            else:
                await add_user_info(self.user_id)
                user_info = {
                    'student_name': None,
                    'student_url': None,
                    'lecturer_name': None,
                    'lecturer_url': None,
                    'alert': True
                }

            user_info_cache[self.user_id] = user_info

        return user_info

    async def get_student_name_cache(self) -> str:
        """get last user student name.

        Returns:
            str: Last user student name.
        """

        user_info = await self.get_user_info_cache()
        return user_info['student_name']
    
    async def get_student_url_cache(self) -> str:
        """get last user student schedule url.

        Returns:
            str: Last user student schedule url.
        """

        user_info = await self.get_user_info_cache()
        return user_info['student_url']
    
    async def get_lecturer_name_cache(self) -> str:
        """get last user lecturer name.

        Returns:
            str: Last user lecturer name.
        """

        user_info = await self.get_user_info_cache()
        return user_info['lecturer_name']

    async def get_lecturer_url_cache(self) -> str:
        """get last lecturer student schedule url.

        Returns:
            str: Last user lecturer schedule url.
        """

        user_info = await self.get_user_info_cache()
        return user_info['lecturer_url']
    
    async def get_user_alert_cache(self) -> bool:
        """get user alert.

        Returns:
            bool: True - alert is on, False - alert is off.
        """

        user_info = await self.get_user_info_cache()
        return user_info['alert']

    async def update_student_data_cache(self, student_name: str, student_url: str) -> None:
        """update last user student data. 

        Args:
            student_name (str): New last user student name.
            student_url (str): New last user student schedule url.
        """

        await update_student_data(
            user_id=self.user_id, 
            student_name=student_name, 
            student_url=student_url
        )

        if self.user_id in user_info_cache:
            user_info_cache[self.user_id]['student_name'] = student_name
            user_info_cache[self.user_id]['student_url'] = student_url

    async def update_lecturer_data_cache(self, lecturer_name: str, lecturer_url: str) -> None:
        """update last user lecturer data. 

        Args:
            lecturer_name (str): New last user lecturer name.
            lecturer_url (str): New last user lecturer schedule url.
        """

        await update_lecturer_data(
            user_id=self.user_id, 
            lecturer_name=lecturer_name, 
            lecturer_url=lecturer_url
        )

        if self.user_id in user_info_cache:
            user_info_cache[self.user_id]['lecturer_name'] = lecturer_name
            user_info_cache[self.user_id]['lecturer_url'] = lecturer_url

    async def update_user_alert_cache(self, alert: bool) -> None:
        """update user alert. 

        Args:
            alert (bool): True - alert is on, False - alert is off.
        """

        await update_user_alert(user_id=self.user_id, alert=alert)

        if self.user_id in user_info_cache:
            user_info_cache[self.user_id]['alert'] = alert
