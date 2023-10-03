import json
from datetime import datetime, timedelta
import pytz

class JournalEntry:
    """
    Represents a journal entry with attributes such as title, datetime, text, photos, and videos.
    """

    def __init__(self, title:str, datetime_utc:datetime, text:str="", media_content=None):
        """
        Initialize a JournalEntry instance.

        Args:
            title (str): The title of the journal entry.
            datetime_utc (datetime): The datetime in UTC.
            text (str): The text content of the journal entry (optional).
            media_contents (list): A list of photo, videos filenames or URLs (optional).
        """
        self._title = title
        self._datetime_utc = datetime_utc
        self._text = text
        self._media_content = media_content or []

    def convert_utc_to_ist(self):
        """
        Converts the UTC datetime to Indian Standard Time (IST).

        Returns:
            datetime: The datetime in IST.
        """
        ist_timezone = pytz.timezone('Asia/Kolkata')
        ist_datetime = self._datetime_utc.astimezone(ist_timezone)
        return ist_datetime


    def __str__(self):
        """
        String representation of the JournalEntry object.

        Returns:
            str: String representation.
        """
        return f"Journal Entry - Title: {self._title}, Datetime (UTC): {self._datetime_utc}, Text: {self._text}"

    def __repr__(self):
        """
        Official string representation of the JournalEntry object.

        Returns:
            str: Official string representation.
        """
        return f"JournalEntry(title='{self._title}', datetime_utc={self._datetime_utc}, text='{self._text}')"
    
    def to_dict(self):
        """
        Serialize the journal entry into a JSON representation.

        Returns:
            str: JSON representation of the journal entry.
        """
        entry_data = {
            "title": self._title,
            "datetime_utc": self._datetime_utc.isoformat(),
            "text": self._text,
            "media_content": self._media_content
        }
        return entry_data
    
    @classmethod
    def from_dict(cls, data:dict):
        """
        Create a JournalEntry object from a dictionary.

        Args:
            data (dict): Dictionary representation of a journal entry.

        Returns:
            JournalEntry: A new JournalEntry object.
        """
        title = data.get("title")
        datetime_utc = datetime.fromisoformat(data.get("datetime_utc"))
        text = data.get("text", "")
        media_content = data.get("media_content", [])
        return cls(
            title=title,
            datetime_utc=datetime_utc,
            text=text,
            media_content=media_content
        )


# Example usage:
if __name__ == "__main__":
    utc_datetime = datetime(2023, 10, 3, 12, 0, 0, tzinfo=pytz.utc)
    entry = JournalEntry("My First Entry", utc_datetime, "This is my journal entry.")

    # Printing the string and official representations
    print(str(entry))
    print(repr(entry))
