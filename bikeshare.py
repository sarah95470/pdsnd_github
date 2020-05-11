import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def get_filters():
    """
    We ensure that the user is welcomed
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Welcome dear user.')
    print('Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please input city name: ").lower()

    while city not in ['chicago', 'New york city', 'washington']:
        city = input(
        "City is name is invalid! Name must contain: chicago,new york city,washington : ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please input month name:\n Select from: all,january,february,march,april,may,june:    ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please input day of week:\n ").lower()

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
    """
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['start_end_combo'] = "starting at" + df['Start Station'] + ' and ending at ' + df['End Station']

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['week_day'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

# A filter has been added this is to ensure that when the user selects a particular month and day the user expects to selects
# only what he has asked for and not a general over view of the day;
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        # Note the use of iloc so as to pick rows and columns
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # Note the use of iloc so as to pick rows and columns
        df = df.loc[df['week_day'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The Most Common Month is ',common_month)


    # TO DO: display the most common day of week
    common_day = df['week_day'].mode().values[0]
    print('The Most Common Day is ',common_day)


    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_hour = df['start_hour'].mode().values[0]
    print('The Most Common Hour is ',common_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station is ', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station is ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_combo = df['start_end_combo'].mode()[0]
    print('The Most Popular Start/End Combination is ', popular_start_end_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total Trip Duration is ', total_trip_duration)

    # TO DO: display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print('Average Trip Duration is ', avg_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    try:
        user_genders = df['Gender'].value_counts()
    except: user_genders = 'Washington does not have user gender data'
    print(user_genders)

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        oldest_rider_birth = 'The oldest rider was born in ' + str(df['Birth Year'].min())
    except: oldest_rider_birth = 'Washington does not have rider year of birth data'

    print(oldest_rider_birth)

    try:
        youngest_rider_birth = 'The youngest ride was born in ' + str(df['Birth Year'].max())
    except: youngest_rider_birth = 'Washington does not have rider year of birth data'

    print(youngest_rider_birth)

    try:
        most_common_rider_birth = 'The year in which the most riders were born in is ' + str(df['Birth Year'].mode()[0])
    except: most_common_rider_birth = 'Washington does not have rider year of birth data'

    print(most_common_rider_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):

#used a while loop to keep iterating as long as user continues to answer "yes" or exit and move on when they don't.
    i = 0
    data = input("\nwould you like to view the first 5 lines of raw bikeshare data?\n").lower()
    if data != 'yes':
        print("skipping raw data display.")
    else:
        while True:
            window = df[(i * 5):5 +(i * 5)]
            print(window)
            i += 1
            five_raw = input("\nWould you like to see the next 5 rows of raw data?\n")
            if five_raw.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
