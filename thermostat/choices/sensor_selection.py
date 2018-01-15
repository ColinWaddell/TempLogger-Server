HIGHEST = "Highest monitored temperature"
LOWEST = "Lowest monitored temperature"
AVERAGE = "Average across all temperatures"

CHOICES = [
    (HIGHEST, HIGHEST),
    (LOWEST, LOWEST),
    (AVERAGE, AVERAGE)
]

ROUTINES = {
    HIGHEST: max ,
    LOWEST: min,
    AVERAGE: lambda temps: sum(temps) / float(len(temps))
}