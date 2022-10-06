from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def choose_locator(locator: str, interval: int):
    locator = locator.lower()
    if locator == "day":
        return mdates.DayLocator(interval=interval)
    if locator == "week":
        return mdates.WeekdayLocator(interval=int(interval))
    elif locator == "month":
        return mdates.MonthLocator(interval=int(interval))
    elif locator == "year":
        return mdates.YearLocator()


def set_locator(ax, locator, interval):
    '''
    Locator: minute, hour, day, week, month or year
    '''
    locator = locator.lower()
    major = '%d/%m'
    minor = '%H/%d'
    if locator == 'minute':
        ax.xaxis.set_major_locator(mdates.HourLocator())
        lctr = mdates.MinuteLocator(interval=int(interval))
        major = '%H/%d'
        minor = '%M:%H'
    elif locator == 'hour':
        ax.xaxis.set_major_locator(mdates.DayLocator())
        lctr = mdates.HourLocator(interval=int(interval))
        major = '%d/%m'
        minor = '%H'
    elif locator == 'day':
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=7))
        lctr = mdates.DayLocator(interval=int(interval))
        major = '%d/%m'
        minor = '%d'
    elif locator == 'week':
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        lctr = mdates.WeekdayLocator(interval=int(interval))
        major = '%m/%y'
        minor = '%d'
    elif locator == 'month':
        ax.xaxis.set_major_locator(mdates.YearLocator())
        lctr = mdates.MonthLocator(interval=int(interval))
        major = '%y'
        minor = '%m'
    elif locator == 'year':
        lctr = mdates.YearLocator()

    ax.xaxis.set_minor_locator(lctr)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter(major))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter(minor))

def set_legend(ax, title, y, x, loc='best', framealpha=100, text_color="tab:orange"):
    ax.legend(fontsize=16, loc=loc, framealpha=framealpha)
    ax.set_title(title, color=text_color, size=25)
    ax.set_ylabel(y, color=text_color, size=23)
    ax.set_xlabel(x, color=text_color, size=23)

def create_image(fig):
    buffered = BytesIO()
    fig.savefig(buffered)
    img_str = buffered.getvalue()
    return img_str
