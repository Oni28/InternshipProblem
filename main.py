def CTM(timeStr):
    """This function converts a time string into minutes for example: 10:00 => 600 """

    hour, minute = timeStr.split(':')
    return int(hour) * 60 + int(minute)


def createJoinedCal(rangeLimit1, rangeLimit2):
    """ This function creates a calender with all available minutes within the allowed rangeLimits if there are no meetings

        Example:
             rangeLimit1 = ['09:00', '20:00'] and rangeLimit2 = ['10:00', '18:30'] => The allowed rangeLimit is [10:00, 18:30]
        output: {600:True, 601:True,...1110:True}
    """

    # find the latest start time and convert it to minutes
    start = max(CTM(rangeLimit1[0]), CTM(rangeLimit2[0]))
    # find the earliest stop time and convert it to minutes
    end = min(CTM(rangeLimit1[1]), CTM(rangeLimit2[1]))

    # create a dict containing all minutes between start and end indicating available minutes during the day
    # this is the default without considering meetings
    available = {}
    for i in range(start, end + 1):
        available[i] = True
    return available


def delTimeSlots(cal, availableTimesDict):
    """ This function deletes all minutes from the calendar where the people have a meeting """

    # convert the start time of the meeting to minutes format
    start = CTM(cal[0])
    # convert the end time of the meeting to minutes format
    end = CTM(cal[1])
    # remove all minutes from the calender where there is a meeting exclude start and end time
    for i in range(start + 1, end):
        if i in availableTimesDict:
            del availableTimesDict[i]


def createTimeBlocks(availableTimesDict):
    """This function creates a list of sublists where each sublist is a time block

    example: [[600, 800],[900,950],[1080,1100]]
    """

    # get all keys of the dict
    availableTimesList = list(availableTimesDict.keys())
    # store first key
    firstSlot = availableTimesList[0]
    # store first key as start of first time block
    timeSlots = [[firstSlot]]

    # loop through all keys
    for i in range(len(availableTimesList) - 1):
        key = availableTimesList[i]
        # if a number(minute) has no successor which is 1 greater example: 719, 950
        # then the current number is the end of a time block and the following number
        # is the new start of a block
        # ignore all other numbers
        if (key + 1) not in availableTimesList:
            timeSlots[-1].append(key)
            timeSlots.append([availableTimesList[i + 1]])
        del availableTimesDict[key]

    # the last number left in the dict is the end of the last time block
    timeSlots[-1].append(list(availableTimesDict.keys())[0])
    return timeSlots


# given inputs
rangeLimit1 = ['09:00', '20:00']
rangeLimit2 = ['10:00', '18:30']
calender1 = [['09:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
calender2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]

meetingTime = 30

# create a calender with all available minutes within the available rangeLimit
availableTimesDict = createJoinedCal(rangeLimit1, rangeLimit2)

# delete the times where there is a meeting for calender1
for cal in calender1:
    delTimeSlots(cal, availableTimesDict)

# delete the times where there is a meeting for calender2
for cal in calender2:
    delTimeSlots(cal, availableTimesDict)

# create list with available time slots
timeSlots = createTimeBlocks(availableTimesDict)

# remove time blocks where there is not enough time for a meeting and
# convert the minutes back to military time format
availableSlots = []
for timeSlot in timeSlots:
    start, end = timeSlot
    if end - start >= meetingTime:
        hour1 = start // 60
        min1 = start - hour1 * 60
        startStr = f'{hour1:0>2}:{min1:0>2}'

        hour2 = end // 60
        min2 = end - hour2 * 60
        endStr = f'{hour2:0>2}:{min2:0>2}'
        availableSlots.append([startStr, endStr])

print(availableSlots)
