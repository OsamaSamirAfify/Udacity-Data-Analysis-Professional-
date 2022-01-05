import time
import pandas as pd


pd.set_option("display.max_rows", 200)
CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv',
             }
VALID_MONTH = "January,February,March,April,May,June".split(',')
SHORT_MONTH = 'Jan,Feb,Mar,Apr,May,Jun'.split(',')
MONTH_NAME = dict(zip(SHORT_MONTH, VALID_MONTH))
VALID_DAYS = "Mon,Tue,Wed,Thu,Fri,Sat,Sun".split(',')
DAY_NAME_FULL = 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday'.split(',')
DAY_NAME = dict(zip(VALID_DAYS, DAY_NAME_FULL))


def ask_for_day():
    """
    Validate and get user input for day of week ( monday, tuesday, ... sunday)
    Returns: Day Name
    """
    while True:
        day = input("Which Day - Mon, Tue, Wed, Thu, Fri, Sat, or Sun?\n").title()
        if day in VALID_DAYS:
            break
        else:
            print("Invalid Day name! please Enter 'Mon, Tus, Wed, Thr, Fri, Sat, or Sun'")
    return DAY_NAME[day]


def ask_for_month():
    """
    Validate and get user input for month (all, january, february, ... , june)
    Returns: Month Name
    """
    while True:
        month = input("Which month - Jan, Feb, Mar, Apr, May, or Jun?\n").title()
        if month in SHORT_MONTH:
            break
        else:
            print("Invalid Month name! please Enter 'Jan, Feb, Mar, Apr, May, or Jun'")
    return MONTH_NAME[month]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    not_valid_input = True
    while not_valid_input:
        in_city = input("Which City Would you like to see data for 'Chicago, New York, or Washington'?\n").lower()
        if in_city in CITY_DATA:
            not_valid_input = False
        else:  # in case of not valid input
            print('This is not a Valid input, kindly enter "Chicago, New York, or Washington" ')
    # asking user for data filtering
    while True:
        filter_selection = input("Would you like to filter the data by month, day, both, or not at all? "
                                 "Enter 'None' for no filter \n").lower()
        if filter_selection == "none":
            month = "all"
            day = "all"
            break
        elif filter_selection == "month":
            month = ask_for_month()
            day = "all"
            break
        elif filter_selection == "day":
            day = ask_for_day()
            month = "all"
            break
        elif filter_selection == 'both':
            month = ask_for_month()
            day = ask_for_day()
            break
        else:
            print("Invalid Input, Enter 'Day, Month, Both, or None")

    print('=-=' * 25)
    return in_city, month, day


# city, month, day = get_filters()


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
    # Cleaning and preparing the data
    main_data = pd.read_csv(CITY_DATA[city])
    main_data.drop(main_data.columns[0], axis=1, inplace=True)
    main_data['Start Time'] = pd.to_datetime(main_data['Start Time'])
    main_data['Month'] = main_data['Start Time'].dt.month_name()
    main_data['Day'] = main_data['Start Time'].dt.day_name()
    main_data['Hour'] = main_data['Start Time'].dt.hour
    if month != 'all':
        main_data = main_data[main_data['Month'] == month]

    if day != 'all':
        main_data = main_data[main_data['Day'] == day]
    # main_data.to_csv('filtered Data1.csv', index=False)
    return main_data


def do_calculations(data_frame: pd.DataFrame, analysis_category: str):
    """Displays statistics on the Mode and count for many categories."""

    common_category2 = data_frame[analysis_category].value_counts().head(1)
    output_form = pd.DataFrame(data=[common_category2.index, common_category2],
                               index=[analysis_category.title(), 'Count'],
                               columns=['Results'.format(analysis_category)])
    print('"Most Common {} and Total Count"\n{}\n'.format(analysis_category, output_form))


def time_stats(filtered_data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    do_calculations(filtered_data, 'Month')
    # display the most common day of week
    do_calculations(filtered_data, 'Day')
    # display the most common start hour
    do_calculations(filtered_data, 'Hour')

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-=-' * 25)


def station_stats(filtered_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    do_calculations(filtered_data, 'Start Station')
    # display most commonly used end station
    do_calculations(filtered_data, 'End Station')
    # Most Common Trip From Start to End
    combination = filtered_data.groupby(by=['Start Station', 'End Station'])['Hour'].count()
    comb_table = pd.DataFrame(combination[combination == combination.max()]). \
        rename(columns={'Hour': 'Count'}).transpose()
    print('"Most Common Trip From Start to End"\n{}\n'.format(comb_table))

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('=-=' * 25)


def trip_duration_stats(filtered_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = filtered_data['Trip Duration'].sum()
    print('Total Travel Time:   {} "In Hours"'.format(round(total_duration / (60 * 60), 2)))

    # display mean travel time
    average_duration = filtered_data['Trip Duration'].mean()
    print('Average Travel Time: {} "In Minutes"'.format(round(average_duration / 60, 2)))

    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('-=-' * 25)


def user_stats(filtered_data):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = filtered_data.groupby(by=['User Type'])['Hour'].count().sort_values(ascending=False)
    user_type_table = pd.DataFrame(user_type_count).rename(columns={'Hour': 'Count'}).transpose()
    print('Counts of User Types..\n{}\n'.format(user_type_table))
    # checking for Gender and Birth Year Columns
    if 'Gender' in filtered_data.columns:
        # Display counts of gender
        gender_count = filtered_data.groupby(by=['Gender'])['Hour'].count().sort_values(ascending=False)
        gender_table = pd.DataFrame(gender_count).rename(columns={'Hour': 'Count'}).transpose()
        print('Counts of Gender..\n{}\n'.format(gender_table))
    if 'Birth Year' in filtered_data.columns:
        # Display earliest, most recent, and most common year of birth
        common_year = filtered_data['Birth Year'].mode()[0]
        earliest_year = filtered_data['Birth Year'].min()
        recent_year = filtered_data['Birth Year'].max()
        print("Birth Year Analysis...")
        print('Most Common Year of Birth: {}'.format(int(common_year)))
        print('Earliest Year of Birth:    {}'.format(int(earliest_year)))
        print('Recent Year of Birth:      {}'.format(int(recent_year)))
    print("\nThis took %s seconds." % round((time.time() - start_time), 6))
    print('=-=' * 25)


def main():
    pd.set_option("display.max_rows", 200)
    while True:
        city, month, day = get_filters()
        file_data = load_data(city, month, day)

        time_stats(file_data)
        station_stats(file_data)
        trip_duration_stats(file_data)
        user_stats(file_data)

        start_index = 0
        end_index = start_index + 5
        invalid_input = True
        while invalid_input:  # to validate user input
            ask_raw_data = input('\nWould you like to See the Raw Data? Enter yes or no.\n').lower()
            if ask_raw_data not in ['yes', 'no']:
                print('Invalid input, please Enter "Yes or No"!')
            elif ask_raw_data == 'yes':
                while True:  # to continuously displaying the Raw data as long as user needed to
                    raw_data = file_data.iloc[start_index:end_index]
                    pd.set_option("display.max_rows", 200)
                    print(raw_data)
                    while True:  # to validate user input
                        ask_for_more = input('\nWould you like to See More Data? Enter yes or no.\n')
                        if ask_for_more not in ['yes', 'no']:
                            print('Invalid input, please Enter "Yes or No"!')
                        else:
                            break
                    if ask_for_more == 'yes':
                        start_index += 5
                        if start_index + 5 >= file_data.shape[0] - 1:  # check for the end of data
                            end_index = file_data.shape[0]
                            raw_data = file_data.iloc[start_index:end_index]
                            print(raw_data)
                            print("\nThat is the End of the file")
                            invalid_input = False
                            break
                        else:
                            end_index = start_index + 5
                    else:
                        invalid_input = False
                        break
            else:
                invalid_input = False

        restart = input('\nWould you like to restart? Enter yes or Press Enter to End.\n').lower()
        if restart != 'yes':
            print("Good Bye!")
            break


if __name__ == "__main__":
    main()
