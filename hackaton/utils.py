def write_profile(data,telegramId):
    res = ""
    res += data["name"] + " " + data["surname"] + "\n"

    res +=f'Код: "{telegramId}\n'

    return res