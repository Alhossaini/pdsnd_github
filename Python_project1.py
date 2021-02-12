import time
import pandas as pd
import numpy as np

#welcome to my python script!
print('Hello! Let\'s explore some US Bikeshare data!')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_input(input_str,input_type):
    """
    in order to check if user input is valid or not
    input_str is the user input, and input_type is the type of the input (1: city, 2: month, 3: day)
    """
    while True:
        #users input should be string
        input_read = input(input_str).lower()
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print('wrong entry, please enter a city from the three mentioned below')
                if input_type == 2:
                    print('Wrong entry, please enter a valid gregorian month from January to june or "all" for all months')
                if input_type == 3:
                    print('wrong entry, please enter a correct week day or enter "all" for all days of the week')
        except ValueError:
            print('sorry, wrong input, please enter correct input')
    return input_read

def get_filters():
    '''
    Asks the user to specify a city, month, and a week day to analyze

    '''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input('Would you like to see the data for chicago, new york city or washington?\n',1)
    # get user input for month (all, january, february, ... , june)
    month = check_input('please enter a Month (january, ... june) or "all" for all months:\n',2)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input('please enter a day (sunday, monday, ... saturday) or "all" for all days of the week:\n',3)
    print('-'*40)
    return city, month, day

def load_data(city,month,day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays results for part1 on the most popular times of travel."""

    print('\nCalculating The Most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most popular Month: ',df['month'].mode()[0])

    # display the most common day of the week
    print('Most Popular day of the week: ',df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most pupolar hour: ',df['hour'].mode()[0])

    #display how much time the process took in seconds
    print('Elapsed Time in seconds: ',(time.time()-start_time))
    print('-'*40)

def station_stats(df):
    """Displays results for part2 on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and most common trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most frequent Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most frequent End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent trip combination of Start Station and End Station :\n', popular_combination_station)

    print('Elapsed Time in seconds: ', (time.time() - start_time))
    print('-'*40)

def trip_stats(df):
    """Displays results for part3 on total and average trip duration."""

    print('\nCalculating Trip duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time: ',df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Travel Time: ',df['Trip Duration'].mean())

    print('Elapsed Time in seconds: ',(time.time()-start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays results for part4 Bikeshare users info."""

    print('\nCalculating User stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        print(df['Gender'].value_counts())

        # Display earliest, most recent, most common year of birth
        print('Earliest Year: ',df['Birth Year'].min())
        print('Most recent year: ',df['Birth Year'].max())
        print('Most common year: ',df['Birth Year'].mode()[0])

    print('Elapsed Time in seconds: ',(time.time()-start_time))
    print('_'*40)

def view_data(df):

    '''
     display the data used to calculate statistics
    '''
    # Removing added lines in order to present the unmodified form of data used
    df = df.drop(['month', 'day_of_week','hour'], axis = 1)
    row_index = 0

    # asking if the user wanted to see rows of file used to calulate the results
    see_data = input('\nWould you like to view 5 rows of the raw data used to calculate the results? please enter "yes" or "no"\n').lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input('\nWould you like to view 5 more rows of the data used to calculate the results? please enter "yes" or "no" \n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_stats(df)
        user_stats(df,city)
        view_data(df)

        restart = input('Would you like to check for more information? please enter "yes" or "no":\n').lower()
        if restart != 'yes':
           print('Thank you for checking Bikeshare data, have a wonderful day :) ')
           break

if __name__=="__main__":
    main()
