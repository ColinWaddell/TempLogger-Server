from .bitchoices import BitChoices

MONDAY = "Monday"
TUESDAY = "Tuesday"
WEDNESDAY = "Wednesday"
THURSDAY = "Thursday"
FRIDAY = "Friday"
SATURDAY = "Saturday"
SUNDAY = "Sunday"

WEEKDAYS = (
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
)

# Select all days using "bitcodes"
DEFAULT = list((pow(2, index) for index in range(len(WEEKDAYS))))

CHOICES = BitChoices(
    (
        (index, day)
        for index, day in enumerate(WEEKDAYS)
    ))
