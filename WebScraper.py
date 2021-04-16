# Copyright William Garrett White @ 2020 - 2021 [Educational use only]

import requests as request
from bs4 import BeautifulSoup as soup
import csv
import datetime as time

# Importing modules

class scrape():
    game_dates = []
    scores = []
    teams = []
    away_teams = []
    home_teams = []
    away_inactives_per_game = []
    home_inactives_per_game = []
    game_times_military_format = []
    did_a_major_event_occur_BOOL = []
    is_away_team_home_BOOL = []
    is_home_team_home_BOOL = []
    away_win_loss_percentage = []
    home_win_loss_percentage = []
    did_home_team_win = []

    # Declaring the class and the lists for all data collected

    ticker_dictionary = {'San Antonio': 'SAS', 'Charlotte': 'CHO', 'Philadelphia': 'PHI',
                         'Brooklyn': 'BRK', 'Milwaukee': 'MIL', 'Boston': 'BOS', 'New York': 'NYK',
                         'Toronto': 'TOR', 'Miami': 'MIA', 'Chicago': 'CHI', 'Indiana': 'IND',
                         'Atlanta': 'ATL', 'Cleveland': 'CLE', 'Washington': 'WAS', 'Orlando': 'ORL',
                         'Detroit': 'DET', 'Utah': 'UTA', 'Phoenix': 'PHO', 'LA Lakers': 'LAL',
                         'LA Clippers': 'LAC', 'Portland': 'POR', 'Denver': 'DEN', 'Golden State': 'GSW',
                         'Memphis': 'MEM', 'Dallas': 'DAL', 'New Orleans': 'NOP', 'Oklahoma City': 'OKC',
                         'Sacramento': 'SAC', 'Houston': 'HOU', 'Minnesota': 'MIN'}

    ticker_to_full_name_dictionary = {'MIL': 'Milwaukee Bucks', 'TOR': 'Toronto Raptors',
                                      'MIA': 'Miami Heat', 'BOS': 'Boston Celtics', 'IND': 'Indiana Pacers',
                                      'PHI': 'Philadelphia 76ers', 'ORL': 'Orlando Magic', 'BRK': 'Brooklyn Nets',
                                      'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons', 'WAS': 'Washington Wizards',
                                      'CHO': 'Charlotte Hornets', 'NYK': 'New York Knicks',
                                      'CLE': 'Cleveland Cavaliers', 'ATL': 'Atlanta Hawks',
                                      'LAL': 'Los Angeles Lakers', 'UTA': 'Utah Jazz',
                                      'LAC': 'Los Angeles Clippers', 'DEN': 'Denver Nuggets',
                                      'HOU': 'Houston Rockets', 'DAL': 'Dallas Mavericks',
                                      'OKC': 'Oklahoma City Thunder', 'MEM': 'Memphis Grizzlies',
                                      'SAS': 'San Antonio Spurs', 'POR': 'Portland Trail Blazers',
                                      'PHO': 'Phoenix Suns', 'NOP': 'New Orleans Pelicans',
                                      'SAC': 'Sacramento Kings', 'MIN': 'Minnesota Timberwolves',
                                      'GSW': 'Golden State Warriors'}

    # Defining a dictionary for later use to convert string names of NBA teams to their
    # 'ticker symbol'/3 character abbreviation, and converting ticker symbols back into their full team name.

    def GET_and_WRITE_data(self):
        # Declaring the main function of the entire class

        current_date = time.date.today()
        current_NBA_season_start_date = time.date(2020, 12, 22)
        # Getting the current 'datetime' to determine the scope of when data is to be collected.

        url_month = ""
        url_day = ""
        url_year = ""
        # Declaring temporary variables to use in the url from the 'request.get' function

        data_collection_days = current_date - current_NBA_season_start_date
        # Defining a range of days to collect data from

        major_events = [time.date(2020, 12, 25), time.date(2021, 1, 1), time.date(2021, 1, 6), time.date(2021, 1, 20),
                        time.date(2021, 2, 15)]
        # Major events are: Christmas, New Years, Capitol Raid, Inauguration, and Presidents day (Respectively).
        # Always able to add to this list later.

        for day in range(0, data_collection_days.days):
            loop_date = current_NBA_season_start_date + time.timedelta(days=day)
            # Defining current date to get data from

            url_month = str(loop_date.month)
            url_day = str(loop_date.day)
            url_year = str(loop_date.year)
            # Overriding the variable definitions from above with the string
            # literals of the datetime points in the for loop

            basketball_reference_2021_box_scores = "https://www.basketball-reference.com/boxscores/?month=" + url_month + \
                                                   "&day=" + url_day + "&year=" + url_year
            # Combining strings and url format from the given webpage to
            # create a final url to pull data from in the for loop

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.76 Safari/537.36',
                "Upgrade-Insecure-Requests": "1", "DNT": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
            # This may not be needed ^ but I was getting a weird error when using 'request.get' and a stackoverflow post
            # said that passing through headers would help clear any issues like I had

            raw_html = request.get(basketball_reference_2021_box_scores, headers=headers)
            html_page = raw_html.text
            # Using 'request.get' to get the html of the page as an instance of the request class and then
            # converting the hmtl to a string using 'text'

            current_games = soup(html_page, 'lxml')
            # Creating an instance of Beautiful Soup with the text of the html page and defining it as 'XML' type text

            for div in current_games.find_all('div', class_='game_summaries'):
                for table in div.find_all('table', class_='teams'):
                    for td in table.find_all('td'):
                        # Using a series of for loops that are an instance of the beautiful soup class declared above ^^
                        # to find all of the <td> element tags that is a child of the previously selected elements

                        if not (td.has_attr('class')):
                            for a in td.find_all('a'):
                                # Within the tags selected find the <td> tags that DO NOT have a 'class'
                                # attribute and finding the <a> tags beneath them

                                self.teams.append(self.ticker_dictionary[a.text])
                                # After finding the specific a tag, adding the team name after passing it
                                # through the dictionary declared earlier in the program

                                self.game_dates.append(loop_date)
                                # Additionally, adding the current date of the data collected to the 'game dates' list
                                # (again declared at the top of the program when declaring all of the lists)

                    for td in table.find_all('td', class_='right'):
                        self.scores.append(td.text)
                        # Using the same for loop above finding <table> that has attribute 'teams', then trying t
                        # find the <td> element that has the score in it and adding the text of that <td> tag
                        # to the 'scores' list declared above

        for x in range(len(self.game_dates)):
            # After the first for loop adds all of the game data along with what date they occurred on above,
            # I then use this for loop to setup comparing the dates of the 'major events' (declared above)
            # to the dates of each game. This function decides whether or not the game date occurred on
            # or around the date of a major event.
            z = 0
            for y in range(len(major_events)):
                if self.game_dates[x] == major_events[y]:
                    self.did_a_major_event_occur_BOOL.append(1)
                    z = 1
            if z != 1:
                self.did_a_major_event_occur_BOOL.append(0)
                z = 0
            # Using a nested for loop to compare values in each list 1. 'game dates' list and 2. 'major events' list

        for x in range(0, len(self.teams), 2):
            self.away_teams.append(self.teams[x])
            self.home_teams.append(self.teams[x + 1])
            # I used a 'range' for loop with a specific increment (2) because the way the data is setup in
            # the 'teams' list, there wasn't an easy way to extract just the text of the team names without
            # also grabbing the other text in the html that shared the same components.
            # The website just wasn't setup easy for that. Meaning if I run '>>print(teams)',
            # it's gonna give me a bunch of other text that also were <td> tags and had similar attributes, etc.
            # I noticed that the home and away teams were always on a specific incremental index of the list
            # so I used an incremental for loop because it was a little easier than finding
            # a different way to break up the data.

        del self.game_dates[::2]
        del self.did_a_major_event_occur_BOOL[::2]
        del self.scores[1::2]
        # Again because of the issue explained in the previous comment it made sense to delete items
        # in the list following an incremental pattern because the data was presented that way.
        # This may not be the most hardware efficient way to do this but it's what I thought would be easiest.

        for x in range(len(self.away_teams)):
            # Using a similar process to the first for loop declared in the program, I follow essentially the same steps
            # to get the data from the page only this time I'm trying to
            # get the time the game occurred (in military format) using a different URl actually.

            basketball_reference_2021_game_details = \
                "https://www.basketball-reference.com/boxscores/" + \
                str(self.game_dates[x].year) + str(self.game_dates[x].strftime('%m')) + \
                str(self.game_dates[x].strftime('%d')) + "0" + str(self.home_teams[x]) + ".html"
            # Again, declaring a new URL to pull from

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.76 Safari/537.36',
                "Upgrade-Insecure-Requests": "1", "DNT": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
            # Again using a custom url and headers to pass through 'request.get'

            specific_raw_html = request.get(basketball_reference_2021_game_details, headers=headers)
            specific_html_page = specific_raw_html.text
            specific_game = soup(specific_html_page, 'lxml').find_all('div', class_='scorebox_meta')
            # specific_game is referring to the instance of bs4 with the URL corresponding
            # to the "specific game" I'm trying to get the time from

            s = specific_html_page.index('<strong>' + self.away_teams[x])
            m = specific_html_page.index('<strong>' + self.home_teams[x])
            e = specific_html_page.index('&nbsp;</div>')
            x = specific_html_page[s:m]
            y = specific_html_page[m:e]
            self.away_inactives_per_game.append(x.count('/players'))
            self.home_inactives_per_game.append(y.count('/players'))
            # Using the same references from above ^ but because the website didn't have any attributes
            # for the tags that held the data I was trying to collect, I ended up just using the normal
            # string library to find what I needed out of the HTML instead.

            for metadata in specific_game:
                metadata_piece = str(metadata.div.text)
                times = metadata_piece[0: 8]
                correct_times = times.replace(',', '')
                formatted_times = correct_times.replace(':', '')
                if formatted_times.__contains__('PM'):
                    hours = formatted_times.replace('PM', '')
                    military_hours = int(hours) + 1200
                    self.game_times_military_format.append(military_hours)
                else:
                    hours = formatted_times.replace('AM', '')
                    military_hours = int(hours)
                    self.game_times_military_format.append(military_hours)
            # Above is a bunch of 'datetime' code to format the times correctly
            # to then add to the 'game_times_military_format' list

        for x in range(0, len(self.game_dates)):
            # This for loop is used to add data to the win percentages list. I use the last unique URL
            # and also reference things from previous lists that were created and populated above ^

            url_month = str(self.game_dates[x].month)
            url_day = str(self.game_dates[x].day)
            url_year = str(self.game_dates[x].strftime('%Y'))

            if x < 19:
                self.away_win_loss_percentage.append(0.000)
                self.home_win_loss_percentage.append(0.000)
            # It wasn't until 19 games in that each team had their own win/loss %.
            # That is the reason each team gets a null value above ^^

            if x >= 19:
                basketball_reference_historical_standings = "https://www.basketball-reference.com/friv/" + \
                                                            "standings.fcgi?month=" + url_month + "&day=" + url_day + \
                                                            "&year=" + url_year + "&lg_id=NBA"
                # Creating the URL to pull from

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1", "DNT": "1",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
                # More headers ^

                raw_html = request.get(basketball_reference_historical_standings, headers=headers)
                html_page = raw_html.text
                web_soup = soup(html_page, 'lxml')
                # Again, creating another instance of the bs4 class/module only this time I call it 'web_soup'

                away_team_name_full = self.ticker_to_full_name_dictionary[self.away_teams[x]]
                for th_tag in web_soup.find_all('th', attrs={'data-stat': 'team_name'}):
                    child_tag = th_tag.find('a')
                    if child_tag:
                        if str(child_tag.text) == str(away_team_name_full):
                            td_data = th_tag.findNext('td', attrs={'data-stat': 'win_loss_pct'})
                            self.away_win_loss_percentage.append(td_data.text)
                # Finding the win/loss % on the webpage for each away team

                home_team_name_full = self.ticker_to_full_name_dictionary[self.home_teams[x]]
                for th_tag in web_soup.find_all('th', attrs={'data-stat': 'team_name'}):
                    child_tag = th_tag.find('a')
                    if child_tag:
                        if str(child_tag.text) == str(home_team_name_full):
                            td_data = th_tag.findNext('td', attrs={'data-stat': 'win_loss_pct'})
                            self.home_win_loss_percentage.append((td_data.text))
                # Finding the win/loss % on the webpage for each home team

        for x in range(0, len(self.scores), 2):
            # Using this for loop to find out the winner of each game using the indexing of the 'scores' list,
            # to then add to the "Did the home team win?" lists

            if (int(self.scores[x + 1]) > int(self.scores[x])):
                self.did_home_team_win.append(1)
            if (int(self.scores[x + 1]) < int(self.scores[x])):
                self.did_home_team_win.append(0)
            # Code to get the labeled outcomes of each game ^

        csv_file = open('csv_basketball_reference.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ['Date of the game', 'Away Team Ticker', 'Home Team Ticker',
             'Is Away Team Home? (Home Court Advantage Stat)',
             'Is Home Team Home? (Home Court Advantage Stat)', 'Did a Major Event Occur?',
             'Military-Hours Time of the Game', 'Away team inactive players', 'Home team inactive players',
             'Away team win/loss %', 'Home Team win/loss %', 'Did Home Team Win? (Outcome)'])

        for x in range(0, len(self.away_teams)):
            csv_writer.writerow([self.game_dates[x], self.away_teams[x], self.home_teams[x], 0, 1,
                                 self.did_a_major_event_occur_BOOL[x], self.game_times_military_format[x],
                                 self.away_inactives_per_game[x], self.home_inactives_per_game[x],
                                 self.away_win_loss_percentage[x], self.home_win_loss_percentage[x],
                                 self.did_home_team_win[x]])
        csv_file.close()
        # All of the code above is from the 'csv' module and is used to write all
        # the data retrieved to the csv file for later use.
