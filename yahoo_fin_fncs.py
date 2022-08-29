#some useful functions to be used with yahoo-fin

def parsedate(MonthDDYYYY): #convert yahoo-fin date format to a 3 element int-list: [month, day, year]

    t = list()

    a = MonthDDYYYY.split(" ", 1)
    b = a[1].split(",", 1)
    c = b[1].strip()

    t.append(month2num(a[0]))
    t.append(int(b[0]))
    t.append(int(c))

    return t


def month2num(month):  # convert month(string) to the corresponding nth month of the year

    match month:
        case 'January':
            return 1
        case 'February':
            return 2
        case 'March':
            return 3
        case 'April':
            return 4
        case 'May':
            return 5
        case 'June':
            return 6
        case 'July':
            return 7
        case 'August':
            return 8
        case 'September':
            return 9
        case 'October':
            return 10
        case 'November':
            return 11
        case 'December':
            return 12

        case _:
            return ''  # incase wrong input
