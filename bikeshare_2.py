import time
import pandas as pd
import numpy as np
import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# 2 lists to store the correspondancy between the names and numbers of weekdays and months
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

months =['january','february','march','april','may','june','july','august','september','october','november','december']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city do you want to explore ? Choose between Chicago, New York and Washington : ').lower()
    while city not in ['chicago','new york','washington'] :
        print ("\n Oups, you must select a city among the 3 options available !")
        city = input('Which city do you want to explore ? Choose between Chicago, New York and Washington : ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month do you want to analyze ? Type the full name, or type all to keep all the data : ").lower()
    while month not in ['january','february','march','april','may','june','all'] :
        print("\n Oups, you must select a month between January and June and spell it properly, or type all. Let's try again")
        month = input("Which month do you want to analyze ? Type the full name, or type all to keep all the data : ").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day do you want to analyze ? Type the full name, or type all to keep all the data : ").lower()
    while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'] :
        print("\n Oups, you must select a day and spell it properly, or type all. Let's try again")
        day = input("Which day do you want to analyze ? Type the full name, or type all to keep all the data : ").lower()
        
    print('\n Thank you for selecting the data. We have 3 filters now : city - {} , month - {} , day - {} ' . format(city,month,day))
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
        3 columns have been added on top of the data in the csv file, to have the month nb, day nb, start hour
    """
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Day nb'] = df['Start Time'].dt.dayofweek
    df['Month nb'] = df['Start Time'].dt.month
    df['Start hour']=df['Start Time'].dt.hour
    
    if day !='all' :
        day_to_keep = days.index(day)
        df = df.loc[df['Day nb'] == day_to_keep]
        
    if month != 'all' :
        month_to_keep = months.index(month)+1
        df = df.loc[df['Month nb'] == month_to_keep]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    the input datafram should include colums containing the day nb, month nb and start hour"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month 
    most_common_month_nb = df['Month nb'].mode()[0]
    most_common_month_name = months[most_common_month_nb - 1]
    print('\n The most common month is {}'.format(most_common_month_name))

    # display the most common day of week
    most_common_day_nb = df['Day nb'].mode()[0]
    most_common_day_name = days[most_common_day_nb]
    print('\n The most common day is {}'.format(most_common_day_name))
    # display the most common start hour
    most_common_start_hour = df['Start hour'].mode()[0]
    print('\n The most common start hour is {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('\n The most common start station is {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\n The most common end station is {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Station pair'] = df['Start Station'] + ' - ' +  df['End Station']
    most_common_trip = df['Station pair'].mode()[0]
    print('\n The most common pair of start and end station is {}'.format(most_common_trip))   
    df.drop(columns=['Station pair'] , inplace = True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_seconds = int(df['Trip Duration'].sum())
    total_travel_time = str(dt.timedelta(seconds=total_travel_seconds))
    print('The total travel time was {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_seconds = int(df['Trip Duration'].mean())
    mean_travel_time = str(dt.timedelta(seconds=mean_travel_seconds))
    print('The mean travel time was {} seconds, which can also be read {}'.format(str(mean_travel_seconds) , mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count_serie = df.groupby(['User Type'])['Start Time'].count()
    user_count_dic = user_count_serie.to_dict()
    for pair in list(user_count_dic.items()) :
        print('There are {} users of type {} \n'.format(pair[1],pair[0]))
    
    # Display counts of gender
    if 'Gender' in df.columns :
        gender_count_serie = df.groupby(['Gender'])['Start Time'].count()
        gender_count_dic = gender_count_serie.to_dict()
        for pair in list(gender_count_dic.items()) :
            print('There are {} {} users \n'.format(pair[1],pair[0]))
    else :
        print('No gender information to dislay\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns :
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('In the available data, the earliest birth date is {}, the most recent is {}, and the most common is {} \n'.format(min_birth_year,max_birth_year,common_birth_year))
    else :
        print('No birth year information to display \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('\n The dimensions of the selected dataset are {}'.format(df.shape))
        print('-'*40)
        time_stats(df)
        wait = input('Press enter to continue to the next section \n')
        print('-'*40)
        station_stats(df)
        wait = input('Press enter to continue to the next section \n')
        print('-'*40)
        trip_duration_stats(df)
        wait = input('Press enter to continue to the next section \n')
        print('-'*40)
        user_stats(df)
        
        raw = input('Would you like to look at the first 5 rows of the data ? Enter yes or no\n')
        i=0
        while raw.lower() =='yes' and i<df.shape[0]-5:
            print(df[i:i+5])
            i+=5
            raw = input('Would you like to look at the next 5 rows of the data ? Enter yes or no \n')

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
