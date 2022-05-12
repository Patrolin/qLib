__all__ = ["DateTime"]

from qLib.math_ import floor

def isLeapYear(year):
    return ((year % 4) == 0) - ((year % 100) == 0) + ((year % 400) == 0)

def daysBeforeYear(yearMinusOne):
    return yearMinusOne * 365 + floor(yearMinusOne / 4) - floor(yearMinusOne / 100) + floor(yearMinusOne / 400)

def daysBeforeMonth(_yearMinusOne, _monthMinusOne):
    yearMinusOne = _yearMinusOne + floor(_monthMinusOne / 12)
    yearDays = daysBeforeYear(yearMinusOne)
    monthMinusOne = _monthMinusOne % 12
    k = 30 + 0.5 / 1 + 0.5 / 8
    monthDays = floor(monthMinusOne * k + 0.5) - (monthMinusOne > 1) * (2 - isLeapYear(yearMinusOne + 1))
    return yearDays + monthDays

def daysInMonth(year, month):
    return daysBeforeMonth(year, month + 1) - daysBeforeMonth(year, month)

def dateToGregorianSecond(year, month=1, day=1, hour=0, minute=0, second=0, ms=0):
    return (daysBeforeMonth(year - 1, month - 1) + (day - 1)) * 86400 + hour * 3600 + minute * 60 + second + ms / 1000

def gregorianSecondToDate(gregorianSecond):
    # TODO: fix 13/00 at the end of every year
    AVERAGE_DAYS_PER_YEAR = 365 + 1 / 4 - 1 / 100 + 1 / 400
    accSeconds = gregorianSecond
    yearMinusOneMaybe = floor(accSeconds / 86400 / AVERAGE_DAYS_PER_YEAR) + 1
    yearMinusOne = yearMinusOneMaybe - (daysBeforeYear(yearMinusOneMaybe) * 86400 > gregorianSecond)
    accSeconds -= daysBeforeYear(yearMinusOne) * 86400
    accDays = accSeconds / 86400
    monthMinusOne = (accDays >= 31) * floor((accDays + (2 - isLeapYear(yearMinusOne + 1))) / 30.5)
    accSeconds = gregorianSecond - daysBeforeMonth(yearMinusOne, monthMinusOne) * 86400
    dayMinusOne = floor(accSeconds / 86400)
    accSeconds -= dayMinusOne * 86400
    hour = floor(accSeconds / 3600)
    accSeconds -= hour * 3600
    minute = floor(accSeconds / 60)
    accSeconds -= minute * 60
    second = floor(accSeconds)
    accSeconds -= second
    ms = floor(accSeconds * 1000)
    print(accSeconds * 1000)
    return [yearMinusOne + 1, monthMinusOne + 1, dayMinusOne + 1, hour, minute, second, ms, dayMinusOne % 7]

# TODO: https://www.timeanddate.com/time/zones/
# TODO: Locale
#GREGORIAN_CALENDAR_EPOCH_YEAR = 1583 # Gregorian calendar Epoch = October 1582
#TAI_EPOCH_YEAR = 1958
# POSIX doesn't define what a second is, so people just slow down/speed up time
# whenever a leap seconds happens to make computations easier,
# therefore time is always broken past the previous leap second
POSIX_EPOCH_YEAR = 1970
UTC_EPOCH_YEAR = 1972 # UTC = TAI + (N leap seconds) + (10 unlisted leap seconds)

class DateTime:
    def __init__(self, year, month=1, day=1, hour=0, minute=0, second=0, ms=0):
        self.gregorianSecond = dateToGregorianSecond(year, month, day, hour, minute, second, ms)

    def toParts(self):
        return gregorianSecondToDate(self.gregorianSecond)

    def toUTCTimeStamp(self):
        return self.gregorianSecond - dateToGregorianSecond(POSIX_EPOCH_YEAR)

    def __repr__(self):
        [year, month, day, h, m, s, ms, weekday] = self.toParts()
        dateString = f"{year:04}-{month:02}-{day:02}"
        timeString = f"T{h:02}:{m:02}:{s:02}" if (year >= UTC_EPOCH_YEAR) else ""
        msString = f".{floor(ms):03}" if ms > 0 else ""
        timezoneString = "Z" if (year > UTC_EPOCH_YEAR) else ""
        return f"{dateString}{timeString}{msString}{timezoneString}"

    def toHistoricString(self):
        [year, *_] = self.toParts()
        return f"{year} AD" if (year > 0) else f"{1-year} BC"

if __name__ == "__main__":
    d = DateTime(2022, 5, 14, 19, 23, 59, 999)
    print(d)
    print(d.toHistoricString())
