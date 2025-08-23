from apps.bot.models import Message


class MessageManager:
    """
    Manages retrieval and formatting of messages from the database.
    """

    MESSAGES = {}

    @staticmethod
    def get_message(name: str, **kwargs) -> str:
        """
        Retrieves a message from the database and formats it if needed.

        Parameters:
            name (str): The name of the message stored in the database.
            lang (str): The language of the user stored in the database.
            **kwargs: Key-value pairs for formatting the message.

        Returns:
            str: The message text. If `kwargs` are provided, the message will be formatted accordingly.

        Example:
            >>> MessageManager.fetch("welcome", username="Ali")
            "Hello Ali! Welcome."
        """
        message = Message.objects.get(name=name.strip())
        text = message.text
        return text.format(**kwargs) if kwargs else text
