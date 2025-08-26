import json


class BaseKeyboard:

    def to_json(self, data: dict):
        return json.dumps(data)


class ReplyKeyboardMarkup(BaseKeyboard):

    def home_keyboard(self):
        markup = {
            "keyboard": [
                ["دکمه اول", "دکمه دوم"],
                ["دکمه سوم", "دکمه چهارم"]
            ],
            "resize_keyboard":True
        }
        return self.to_json(
            data=markup
        )

    def back_keyboard(self):
        markup = {
            "keyboard": [
                ["بازگشت"]
            ],
            "resize_keyboard":True
        }
        return self.to_json(
            data=markup
        )

    def remove_keyboard(self):
        markup = {"keyboard": []}
        return self.to_json(
            data=markup
        )

class InlineKeyboardMarkup(BaseKeyboard):

    def first_keyboard(self):
        markup = {
            "inline_keyboard": [
                [
                    {"text": "دکمه اول", "callback_data": "first_button"},
                    {"text": "دکمه دوم", "callback_data": "second_button"}
                ],
                [
                    {"text": "دکمه سوم", "callback_data": "third_button"},
                    {"text": "دکمه چهارم", "callback_data": "fourth_button"}
                ]
            ]
        }
        return self.to_json(
            data=markup
        )

    def remove_keyboard(self):
        markup = {"inline_keyboard": []}
        return self.to_json(
            data=markup
        )

    def sponsor_channel_keyboard(self, channels):

        child = []
        for channel in channels.order_by("-other"):
            child.append(
                [{"text": f"{channel.name}", "url": channel.link}]
            )
        if child:
            child.append(
                [
                    {"text": "تایید عضویت ✅", "callback_data": "joined_to_sponsor"}  # noqa: F541
                ]
            )
        markup = {
            "inline_keyboard": child
        }
        return self.to_json(data=markup)

    def remove_keyboard(self):
        markup = {"inline_keyboard": []}
        return self.to_json(data=markup)

