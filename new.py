import re
import pandas as pd

def chat(data):

    pattern = r"\[(.*?)\]\s(.*)"
    matches = re.findall(pattern, data)

    dates = []
    users = []
    messages = []

    for date, msg in matches:

        if ": " in msg:
            user, message = msg.split(": ", 1)
        else:
            user = "group_notification"
            message = msg

        dates.append(date)
        users.append(user)
        messages.append(message)   # ✅ correct

    df = pd.DataFrame({
        "message_date": dates,
        "user": users,
        "message": messages
    })

    df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M:%S %p',
        errors='coerce'
    )

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour

    return df