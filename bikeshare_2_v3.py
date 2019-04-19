import time
import pandas as pd
import numpy as np
import datetime as dt
import calendar
import timeit
# All the imports were not used for final production, but used all during the coding.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # ADD IF USER WOULD LIKE TO SEE MONTH OR DAY or all
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Enter name of the city to analyze: ").lower()
            if city in CITY_DATA.keys():
                city = city
                break
            else:
                print("That is not the city you are looking for. Check Tatooine. >_>")
        except KeyboardInterrupt:
            print("Aw...")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            timefilter = input("Would you like to filter the data by month, day, both or not at all? Type \'none\' for no time filter: ").lower()
            if timefilter in ['month']:
                month = input("Enter name of the month to filter by, or \'all\' to apply no month filter: ").lower()
                if month in ['january',
                             'february',
                             'march',
                             'april',
                             'may',
                             'june',
                             'july',
                             'august',
                             'september',
                             'october',
                             'november',
                             'december',
                             'all']:
                    month = month
                    break
            elif timefilter in ['day']:
                day = input('Enter name of the day of week to filter by, or \'all\' to apply no day filter: ').lower()
                if day in ['monday',
                           'tuesday',
                           'wednesday',
                           'thursday',
                           'friday',
                           'saturday',
                           'sunday',
                           'all']:
                    day = day
                    break
            elif timefilter in ['both']:
                month = input("Enter name of the month to filter by, or \'all\' to apply no month filter: ").lower()
                if month in ['january',
                             'february',
                             'march',
                             'april',
                             'may',
                             'june',
                             'july',
                             'august',
                             'september',
                             'october',
                             'november',
                             'december',
                             'all']:
                    month = month
                day = input('Enter name of the day of week to filter by, or \'all\' to apply no day filter: ').lower()
                if day in ['monday',
                           'tuesday',
                           'wednesday',
                           'thursday',
                           'friday',
                           'saturday',
                           'sunday',
                           'all']:
                    day = day
                    break
            elif timefilter in ['none']:
                month = 'all'
                day = 'all'
                print('Sure thing! let\'s pull all time data for the selected city, {}!'.format(city))
                break
            else:
                print("You should learn your month names and/or spelling by now... B)")
        except [KeyboardInterrupt]:
            print("It's okay... see you next time~")

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day

    My process for load_data
        1. Load files based on agent input and dictionary.
        2. Then convert the time columns to timestamp.
        3. If agent's input has other than \'all\' then filter by input. \'all\' should be as-is.
    """
    city_file = "C:/Users/fxcheon/Desktop/bikeshare/{}.csv".format(city) #Useful option B
    #city_file = "C:/Users/InfiniteKiheon/Documents/1 Intro to Programming/Python/Project/{}".format(CITY_DATA.get(city))
    city_file = pd.read_csv(city_file)

    city_file['Start Time'] = pd.to_datetime(city_file['Start Time'])
    city_file['End Time'] = pd.to_datetime(city_file['End Time'])

    # Make these into columns to visually check if filters worked
    city_file['Start Month'] = city_file['Start Time'].apply(lambda x: calendar.month_name[x.month].lower())
    city_file['Start Day'] = city_file['Start Time'].apply(lambda x: calendar.day_name[x.weekday()].lower())

    if month == 'all' and day != 'all':
        df = city_file[city_file['Start Day'] == day]
    elif day == 'all' and month != 'all':
        df = city_file[city_file['Start Month'] == month]
    elif month != 'all' and day != 'all':
        df = city_file[(city_file['Start Month'] == month) & (city_file['Start Day'] == day)]
    else:
        df = city_file
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    commonmonth = df['Start Time'].apply(lambda x: x.month_name()).value_counts().idxmax().title()
    print("The most common month for rental was in {}".format(commonmonth))
    # display the most common day of week
    commonday = df['Start Time'].apply(lambda x: x.day_name()).value_counts().idxmax().title()
    print("The most common day of week is {}".format(commonday))

    # display the most common start hour
    commonhour = df['Start Time'].apply(lambda x: x.hour).value_counts().idxmax()
    print("The most common hour usage is {}".format(commonhour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonstartstation = df['Start Station'].value_counts().idxmax()
    print("The most commonly used starting station was at {}".format(commonstartstation))

    # display most commonly used end station
    commonendstation = df['End Station'].value_counts().idxmax()
    print("The most commonly used ending station was at {}".format(commonendstation))

    # display most frequent combination of start station and end station trip
    commonstations = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is {}".format(commonstations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totaltime = (df['End Time']- df['Start Time']).sum()
    print('Current total traveled time is {}.'.format(totaltime))

    # display mean travel time
    meantime = (df['End Time']- df['Start Time']).mean()
    print('Average travel time is {}.'.format(meantime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usertypes = pd.DataFrame(df['User Type'].value_counts())
    print("Current counts of user types are: \n{} \n".format(usertypes))

    # Display counts of gender
    try:
        gendertypes = pd.DataFrame(df['Gender'].value_counts())
        print("Current counts of genders are: \n{}".format(gendertypes))
    except KeyError:
        print("No gender data for this city. Sorry! \n")
    # Display earliest, most recent, and most common year of birth
    try:
        earliestbirth = df['Birth Year'].min().astype(np.int64)
        recentbirth = df['Birth Year'].max().astype(np.int64)
        commonbirth = df['Birth Year'].value_counts().idxmax().astype(np.int64)
        print('The Oldest riders are born in {},\n while the youngest riders are born in {}. \n The most common age rider are born in {}.'.format(earliestbirth, recentbirth, commonbirth))
    except KeyError:
        print("Nope. No birth year for this city either.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data = input('\nWould you like to see the raw data? Enter yes or no: ')
        if raw_data.lower() == 'yes':
            print(df[:5])
            more_raw = input('\nWant to see more? Enter yes or no: ')
            n = 5
            nd = 10
            while more_raw == 'yes':
                if more_raw == 'yes':
                    print(df[n:nd])
                n += 5
                nd += 5
                more_raw = input('\nWant to see more? Enter yes or no: ')
        elif raw_data.lower() == 'no':
            break
        else:
            print("\nYou need to type yes or no. Would you like to see the raw data?\n")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
