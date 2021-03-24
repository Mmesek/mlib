import i18n
def tr(key, language='en', **kwargs):
    return i18n.t(f'{language}.{key}', **kwargs)

def check_translation(k, l, default, **kwargs):
    _k = tr(k, l, **kwargs)
    if _k == l + '.' + k or _k == '':
        return default
    return _k

def pluralizeRussian(number, nom_sing, gen_sing, gen_pl):
    s_last_digit = str(number)[-1]

    if int(str(number)[-2:]) in range(11,20):
        #11-19
        return gen_pl
    elif s_last_digit == '1':
        #1
        return nom_sing
    elif int(s_last_digit) in range(2,5):
        #2,3,4
        return gen_sing
    else:
        #5,6,7,8,9,0
        return gen_pl

def secondsToText(secs, lang="EN"):
    weeks = secs//604800
    days = (secs - weeks*604800)//86400
    hours = (secs - weeks*604800 - days*86400)//3600
    minutes = (secs - weeks*604800 - days*86400 - hours*3600)//60
    seconds = secs - weeks*604800 - days*86400 - hours*3600 - minutes*60

    weeks_text = "w"
    if lang == 'SHORT':
        days_text = "d"
        hours_text = "h"
        minutes_text = "m"
        seconds_text = "s"
    elif lang == "ES":
        days_text = "día{}".format("s" if days!=1 else "")
        hours_text = "hora{}".format("s" if hours!=1 else "")
        minutes_text = "minuto{}".format("s" if minutes!=1 else "")
        seconds_text = "segundo{}".format("s" if seconds!=1 else "")
    elif lang == "PL":
        weeks_text = "{}".format("tydzień" if weeks==1 else ("tygodnie" if abs(weeks) % 10 in [2,3,4] else "tygodni"))
        days_text = "{}".format("dni" if days!=1 else "dzień")
        hours_text = "godzin{}".format("a" if hours==1 else ("y" if abs(hours) % 10 in [2,3,4] and hours not in [12,13,14] else ""))
        minutes_text = "minut{}".format("a" if minutes==1 else ("y" if abs(minutes) % 10 in [2,3,4] and minutes not in [12,13,14] else ""))
        seconds_text = "sekund{}".format("a" if seconds==1 else ("y" if abs(seconds) % 10 in [2,3,4] and seconds not in [12,13,14] else ""))
    elif lang == "DE":
        days_text = "Tag{}".format("e" if days!=1 else "")
        hours_text = "Stunde{}".format("n" if hours!=1 else "")
        minutes_text = "Minute{}".format("n" if minutes!=1 else "")
        seconds_text = "Sekunde{}".format("n" if seconds!=1 else "")
    elif lang == "RU":
        days_text = pluralizeRussian(days, "день", "дня", "дней")
        hours_text = pluralizeRussian(hours, "час", "часа", "часов")
        minutes_text = pluralizeRussian(minutes, "минута", "минуты", "минут")
        seconds_text = pluralizeRussian(seconds, "секунда", "секунды", "секунд")
        days_text = "день" if days == 1 else("дня" if abs(days) % 10 in [2, 3, 4] and days not in range(11, 20) else "дней")
        hours_text = "час" if hours == 1 else("часа" if abs(hours) % 10 in [2, 3, 4] and hours not in range(11, 20) else "часов")
        minutes_text = "минута" if minutes == 1 else("минуты" if abs(minutes) % 10 in [2, 3, 4] and minutes not in range(11, 20) else "минут")
        seconds_text = "секунда" if seconds == 1 else("секунды" if abs(seconds) % 10 in [2, 3, 4] and seconds not in range(11, 20) else "секунд")
    else:
        weeks_text = "week{}".format("s" if weeks != 1 else "")
        days_text = "day{}".format("s" if days!=1 else "")
        hours_text = "hour{}".format("s" if hours!=1 else "")
        minutes_text = "minute{}".format("s" if minutes!=1 else "")
        seconds_text = "second{}".format("s" if seconds!=1 else "")

    result = ", ".join(filter(lambda x: bool(x), [
    "{0} {1}".format(weeks, weeks_text) if weeks else "",
    "{0} {1}".format(days, days_text) if days else "",
    "{0} {1}".format(hours, hours_text) if hours else "",
    "{0} {1}".format(minutes, minutes_text) if minutes and not weeks else "",
    "{0} {1}".format(seconds, seconds_text) if seconds and not weeks and not days else ""
    ]))
    return result
