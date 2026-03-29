import re
import pandas as pd

def chat(data):

    # Step 1: extract date + full message
    pattern = r"\[(.*?)\]\s(.*)"
    matches = re.findall(pattern, data)

    dates = []
    users = []
    messages = []

    for date, msg in matches:

        # Step 2: split user & message
        if ": " in msg:
            user, message = msg.split(": ", 1)
        else:
            user = "group_notification"
            message = msg

        dates.append(date)
        users.append(user)
        messages.append(message)

    # Step 3: create dataframe
    df = pd.DataFrame({
        'date': dates,
        'user': users,
        'message': messages
    })

    # Step 4: convert date
    df['date'] = df['date'].str.replace('\u202f', ' ')
    df['date'] = pd.to_datetime(
        df['date'],
        format='%d/%m/%y, %I:%M:%S %p',
        errors='coerce'
    )

    # Step 5: feature extraction
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Step 6: period column
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df