__all__ = ['register_admins_commands']


from .admin_cmd import admin_cmd

from aiogram import Dispatcher


def register_admins_commands(dp: Dispatcher):
    dp.register_message_handler(admin_cmd)
