from apps.telegram.telegram_models import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


class BaseKeyboard:
    pass

class ReplyKeyboardMarkupKeyboard(BaseKeyboard):

    def home_keyboard(self):
        markup = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="دکمه اول"),
                        KeyboardButton(text="دکمه دوم"),
                    ],
                    [
                        KeyboardButton(text="دکمه سوم"),
                        KeyboardButton(text="دکمه چهارم"),
                    ]
                ],
                resize_keyboard=True
            )
        return markup

    def back_keyboard(self):
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="بازگشت")
                ]
            ],
            resize_keyboard=True
        )
        return markup

    def remove_keyboard(self):
        markup = ReplyKeyboardRemove(remove_keyboard=True)
        return markup

class InlineKeyboardMarkupKeyboard(BaseKeyboard):

    def first_keyboard(self):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="دکمه اول",
                        callback_data="first_button",
                        style="success"
                    ),
                    InlineKeyboardButton(
                        text="دکمه دوم",
                        callback_data="first_button",
                        style="primary"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="دکمه سوم",
                        callback_data="first_button",
                        style="success"
                    ),
                    InlineKeyboardButton(
                        text="دکمه چهارم",
                        callback_data="first_button",
                        style="primary"
                    )
                ]
            ]
        )
        return markup

    def sponsor_channel_keyboard(self, channels):

        child = []
        for channel in channels.order_by("-other"):
            child.append(
                [
                    InlineKeyboardButton(
                        text=f"{channel.name}",
                        url=channel.link,
                        style="primary"
                    )
                ]
            )
        if child:
            child.append(
                [
                    InlineKeyboardButton(
                        text="برسی عضویت ✅",
                        callback_data="joined_to_sponsor",
                        style="success"
                    )
                ]
            )
        markup = InlineKeyboardMarkup(
            inline_keyboard=child
        )
        return markup

    def remove_keyboard(self):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[]
        )
        return markup

