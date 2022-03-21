from datetime import datetime

from src.api.resources.energy_history import db_get_data


def format_data():
    yesterday = [None for _ in range(1440)]
    average = [[] for _ in range(1440)]

    now = datetime.now()
    for date, value in db_get_data():
        minute = int((date - date.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) // 60
        day = int((date.replace(hour=0, minute=0, second=0, microsecond=0) - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) // 86400
        average[minute].append(value)
        if day == -1:
            yesterday[minute] = value

    for i in range(len(average)):
        average[i] = sum(average[i]) / len(average[i]) if len(average[i]) > 0 else None

    for i in range(len(average)):
        if yesterday[i] is None:
            j = i
            while yesterday[j] is None:
                if j == len(yesterday) - 1:
                    yesterday[j] = 0
                    break
                j += 1
            yesterday[i] = (yesterday[i-1] + (yesterday[i-1] - yesterday[j]) / (i - 1 - j)) if yesterday[i-1] is not None else 0
        if average[i] is None:
            j = i
            while average[j] is None:
                if j == len(average) - 1:
                    average[j] = 0
                    break
                j += 1
            average[i] = (average[i-1] + (average[i-1] - average[j]) / (i - 1 - j)) if average[i-1] is not None else 0

    return yesterday, average


def profitability(yesterday, average):
    def find_previous_day_extrema(values: list):
        maximum = None
        minimum = None
        # values.append(first_value_of_today)

        for idx in range(len(values) - 2, 0, -1):
            if values[idx] > values[idx - 1] and values[idx] > values[idx + 1] and maximum is None:
                maximum = values[idx]
            elif values[idx] < values[idx - 1] and values[idx] < values[idx + 1] and minimum is None:
                minimum = values[idx]

            if maximum is not None and minimum is not None:
                break

        # in case the plot is a non-decreasing or non-increasing function
        if minimum is None:
            minimum = min(values[0], values[-2])
        if maximum is None:
            maximum = max(values[0], values[-2])

        # values.pop()

        return minimum, maximum

    def find_todays_extrema(values: list):
        maxima = []
        minima = []
        # values.insert(0, last_value_of_yesterday)
        # Nie chcemy sprawdzać, czy pierwszy pomiar danego dnia jest ekstremum
        # bo przez to czasem estymacje świrują. To wynika bezpośrednio z tego,
        # że mamy niestety nieciągłe połączenie pomiędzy estymacjami na kolejne dni...

        for idx in range(1, len(values) - 2):
            if values[idx] > values[idx - 1] and values[idx] > values[idx + 1]:
                maxima.append(idx)
            elif values[idx] < values[idx - 1] and values[idx] < values[idx + 1]:
                minima.append(idx)

        if values[-1] > values[-2]:
            maxima.append(len(values) - 1)
        else:
            minima.append(len(values) - 1)

        # values.pop(0) # connected with values.insert(0, ...)

        return minima, maxima

    last_minimum, last_maximum = find_previous_day_extrema(yesterday)
    incoming_minima, incoming_maxima = find_todays_extrema(average)

    # last_value_of_yesterday: float
    # for value in reversed(yesterday):
    #     last_value_of_yesterday = value
    #     if average[0] != last_value_of_yesterday:
    #         break
    #     else:
    #         print("same? weird...")

    isDerivativePositive = True if average[1] > average[0] else False

    if isDerivativePositive and average[0] < average[1] and average[0] < yesterday[-1]:
        last_minimum = average[0]

    # this is working, but for our chart shapes the algotithm just works better without checking this
    # if not isDerivativePositive and average[0] > average[1] and average[0] > yesterday[-1]:
    #     last_maximum = average[0]

    incoming_maximum = average[incoming_maxima[0]]
    incoming_minimum = average[incoming_minima[0]]
    charging = []
    discharging = []

    for i in range(1440):
        if isDerivativePositive:
            discharging.append((average[i] - last_minimum) / (incoming_maximum - last_minimum))
        elif not isDerivativePositive:
            discharging.append((average[i] - incoming_minimum) / (last_maximum - incoming_minimum))
        charging.append(1.0 - discharging[-1])  # nie ma sensu liczyć wzorem, bo i tak wyjdzie 1-discharging

        if len(incoming_maxima) > 0 and incoming_maxima[0] == i:
            last_maximum = average[incoming_maxima.pop(0)]
            incoming_maximum = average[incoming_maxima[0]] if len(incoming_maxima) > 0 else incoming_maximum
            isDerivativePositive = False
        if len(incoming_minima) > 0 and incoming_minima[0] == i:
            last_minimum = average[incoming_minima.pop(0)]
            incoming_minimum = average[incoming_minima[0]] if len(incoming_minima) > 0 else incoming_minimum
            isDerivativePositive = True

    return charging, discharging
