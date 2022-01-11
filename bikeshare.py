import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!\nEnter a city name to get started...')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nEnter one of the following cities:\n[ Chicago, New York City or Washington ] : ").lower()
    city_filter = ['chicago', 'new york city', 'washington']
    while city not in city_filter:
        print('Ohh, it seems you entered the wrong city, kindly enter any of the following cities: chicago, new york city, washington')
        city = input("\nEnter one of the following cities:\n[ Chicago, New York or Washington ] : ").lower()
    # get user input for month (all, january, february, ... , june)
    month = input("\nEnter a month from january to june,\n or type 'all' to select all the months  : ").lower()
    month_filter = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in month_filter:
        print('You entered the wrong month')
        month = input("\nKindly enter a month from january to june,\n or type 'all' to select all the months  : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nEnter a week day from\n[sunday' to 'saturday' or 'all'] : ").lower()
    day_filter = [ 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    while day not in day_filter:

        print('You entered the wrong day')
        day = input("\nselect the day of the week from\n['sunday' to 'saturday', 'all'] : ").lower()

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

    # To load the data
    df = pd.read_csv(CITY_DATA[city])

    #To convert start time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #To extract month and weekday from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.day_name()

    #To xtract the hour from Start Time
    df['Start Hour'] = df['Start Time'].dt.hour

    # Month filtering condition
    if month != 'all':
        # month index to create month list
        month_filter = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_filter.index(month) + 1

        
        df = df[df['month'] == month]

    # place a condition to filter by weekday if applicable
    if day != 'all':
        # dataframe created by week day filtering
        df = df[df['weekday'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    month_filter = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Based on the selected filter, the month with most travels is: \t{}'.format(month_filter[most_common_month]))

    # display the most common day of week
    most_common_day = df['weekday'].mode()[0]
    print('Based on the selected filter, the weekday with most travels is: \t{}'.format(most_common_day))

    # display the most common start hour
    popular_hour = df['Start Hour'].mode()[0]
    print('Based on the selected filter, the most common start hour is: \t{}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station is {}".format(most_start_station))

    # display most commonly used end station
    most_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station is {} ".format(most_end_station))


    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' and ' + df['End Station'] # this will add both stations
    most_used_route = df['route'].mode()[0] # this will select the mode of both stations
    print ("The most used route is {} ".format(most_used_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # trip duration statistics
    print(' Trip Duration statistics '.center(80, '-'))
    # display total travel time
    print('Total Travel Time '.ljust(40, '.'), df['Trip Duration'].sum())
    # display the mean travel time
    print('Mean Travel Time '.ljust(40, '.'), df['Trip Duration'].mean())
    # display the most travel time
    print('Most Travel Time '.ljust(40, '.'), df['Trip Duration'].mode()[0])
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df.groupby(["User Type"])["User Type"].count())
    print(' User type statistics '.center(80, '-'))
    print("User Type \t\t\t Total ")
    for user_type in user_types.keys():
        print("{}: \t\t\t {}".format(user_type, user_types[user_type]))
    # Display counts of gender
    try:    # this will handle any potential exception as not all dataset have a gender column
        gender = dict(df.groupby(["Gender"])["Gender"].count())
        print(' Gender statistics '.center(80, '-'))
        print("Gender \t\t\t Total ")
        for user_gender in gender.keys():
            print("{}: \t\t\t {}".format(user_gender, gender[user_gender]))
    except: 
        print("Oh!, the chosen data set has no data for gender \n")

    # Display earliest, most recent, and most common year of birth
    print(' Age statistics '.center(80, '-'))
    try:
        earliest_birth_year = list(df["Birth Year"].dropna().sort_values(ascending=True).head(1))
        print("The oldest bikers for the selected filter was born in {} ".format(int(earliest_birth_year[0])))

        latest_birth_year = list(df["Birth Year"].dropna().sort_values(ascending=False).head(1))
        print("The youngest bikers for the selected filter was born in {}".format(int(latest_birth_year[0])))

        most_common_year_of_birth = int(df["Birth Year"].mode()[0])
        print("The most common year of birth for the selected filter is {}".format(most_common_year_of_birth))
    except:
        print("Sorry, there is no birth year for the selected dataset \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """
        Display the data set used for the analysis in steps of 5 rows based on user interest.

        Args:
            (dataframe) df - dataframe used for the analysis
        """

    # remove the combined column created earlier
    df = df.drop(columns=['Start Station','End Station','Start Time', 'End Time'], axis=1)
    #request if user is interested in seeing the raw data
    request= input("Do you want to see the first 5 lines of raw data? (yes or no): ").lower() #requsting user consent to display the dataset

    #To deplay the raw data in batches of 5s
    start_index = 0
    end_index = 5

    # request if user want to see the next 5 lines of raw data
    while request == "yes" and end_index <= df.size:
        print(df[start_index: end_index])
        start_index = end_index
        end_index += 5
        request = input("Do you want to see the next 5 lines of raw data? (yes or no) : ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
