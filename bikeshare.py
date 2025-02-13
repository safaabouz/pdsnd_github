import time
import pandas as pd
#safaa bouz
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please choose between Chicago, New York City, or Washington.")

    while True:
        month = input("Which month? January, February, ... , June, or 'all': ").strip().lower()
        if month in months or month == 'all':
            break
        print("Invalid input. Please choose a valid month or 'all'.")

    while True:
        day = input("Which day? Monday, Tuesday, ... , Sunday, or 'all': ").strip().lower()
        if day in days or day == 'all':
            break
        print("Invalid input. Please choose a valid day or 'all'.")

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_raw_data(df):
    """
    Displays raw data upon user request in increments of 5 rows.
    """
    start = 0
    while True:
        show_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no.\n").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[start:start + 5])
        start += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = months[df['month'].mode()[0] - 1].title()
    print(f"Most common month: {most_common_month}")

    most_common_day = df['day_of_week'].mode()[0].title()
    print(f"Most common day of week: {most_common_day}")

    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f"Most common start station: {df['Start Station'].mode()[0]}")

    print(f"Most common end station: {df['End Station'].mode()[0]}")

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most common trip: {most_common_trip[0]} -> {most_common_trip[1]}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print(f"Total travel time: {df['Trip Duration'].sum()} seconds")

    print(f"Mean travel time: {df['Trip Duration'].mean()} seconds")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Type Counts:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender Counts:")
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print("\nBirth Year Stats:")
        print(f"Earliest year: {int(df['Birth Year'].min())}")
        print(f"Most recent year: {int(df['Birth Year'].max())}")
        print(f"Most common year: {int(df['Birth Year'].mode()[0])}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
