import asyncio
from playwright.sync_api import sync_playwright
from time import sleep
import os
from dotenv import load_dotenv
import requests
import traceback
from bs4 import BeautifulSoup
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    auth_plugin="caching_sha2_password"
)
cursor = db.cursor()

super_bowl_years = [year for year in range(1991, 1966 - 1, -1)]
teams = {'crd': 'Cardinals', 'atl': 'Falcons', 'rav': 'Ravens', 'buf': 'Bills', 'car': 'Panthers', 'chi': 'Bears', 'cin': 'Bengals', 'cle': 'Browns', 'dal': 'Cowboys', 'den': 'Broncos', 'det': 'Lions', 'gnb': 'Packers', 'htx': 'Texans', 'clt': 'Colts', 'jax': 'Jaguars', 'kan': 'Chiefs', 'rai': 'Raiders', 'sdg': 'Chargers', 'ram': 'Rams', 'mia': 'Dolphins', 'min': 'Vikings', 'nwe': 'Patriots', 'nor': 'Saints', 'nyg': 'Giants', 'nyj': 'Jets', 'phi': 'Eagles', 'pit': 'Steelers', 'sfo': '49ers', 'sea': 'Seahawks', 'tam': 'Buccaneers', 'oti': 'Titans', 'was': 'Commanders'}
season_ids = {2024: 1, 2023: 2, 2022: 3, 2021: 4, 2020: 5, 2019: 6, 2018: 7, 2017: 8, 2016: 9, 2015: 10, 2014: 11, 2013: 12, 2012: 13, 2011: 14, 2010: 15, 2009: 16, 2008: 17, 2007: 18, 2006: 19, 2005: 20, 2004: 21, 2003: 22, 2002: 23, 2001: 24, 2000: 25, 1999: 26, 1998: 27, 1997: 28, 1996: 29, 1995: 30, 1994: 31, 1993: 32, 1992: 33, 1991: 34, 1990: 35, 1989: 36, 1988: 37, 1987: 38, 1986: 39, 1985: 40, 1984: 41, 1983: 42, 1982: 43, 1981: 44, 1980: 45, 1979: 46, 1978: 47, 1977: 48, 1976: 49, 1975: 50, 1974: 51, 1973: 52, 1972: 53, 1971: 54, 1970: 55, 1969: 56, 1968: 57, 1967: 58, 1966: 59}
team_abr_ids = {'crd': 1, 'atl': 2, 'rav': 3, 'buf': 4, 'car': 5, 'chi': 6, 'cin': 7, 'cle': 8, 'dal': 9, 'den': 10, 'det': 11, 'gnb': 12, 'htx': 13, 'clt': 14, 'jax': 15, 'kan': 16, 'rai': 17, 'sdg': 18, 'ram': 19, 'mia': 20, 'min': 21, 'nwe': 22, 'nor': 23, 'nyg': 24, 'nyj': 25, 'phi': 26, 'pit': 27, 'sfo': 28, 'sea': 29, 'tam': 30, 'oti': 31, 'was': 32}
team_name_ids = {'Cardinals': 1, 'Falcons': 2, 'Ravens': 3, 'Bills': 4, 'Panthers': 5, 'Bears': 6, 'Bengals': 7, 'Browns': 8, 'Cowboys': 9, 'Broncos': 10, 'Lions': 11, 'Packers': 12, 'Texans': 13, 'Colts': 14, 'Jaguars': 15, 'Chiefs': 16, 'Raiders': 17, 'Chargers': 18, 'Rams': 19, 'Dolphins': 20, 'Vikings': 21, 'Patriots': 22, 'Saints': 23, 'Giants': 24, 'Jets': 25, 'Eagles': 26, 'Steelers': 27, '49ers': 28, 'Seahawks': 29, 'Buccaneers': 30, 'Titans': 31, 'Commanders': 32}

insert_game = "INSERT INTO games (week, season_id, home_team_id, away_team_id, home_team_stats, away_team_stats) VALUES (%s, %s, %s, %s, %s, %s)"
insert_game_stats = """INSERT INTO game_stats (game_id, team_id, overtime, outcome, win_percentage,
    game_location, opponent_id, points_scored, points_allowed,
    passes_completed, passes_attempted, passing_yards, passing_td,
    interceptions, times_sacked, yards_sacked, yards_per_attempt,
    net_yards_per_attempt, completion_rate, passer_rating,
    rushing_attempts, rushing_yards, rushing_yards_per_attempt,
    rushing_td, field_goals_made, field_goals_attempted,
    extra_points_made, extra_points_attempted, punts, punting_yards,
    third_down_conversions, third_down_attempts,
    fourth_down_conversions, fourth_down_attempts, time_in_possession
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"""

search_previous_game = """SELECT * FROM games WHERE week = %s and season_id = %s and home_team_id = %s and away_team_id = %s"""
update_game_home_stats = """UPDATE games SET home_team_stats = %s WHERE id = %s"""
update_game_away_stats = """UPDATE games SET away_team_stats = %s WHERE id = %s"""

BASE_URL = "https://www.pro-football-reference.com/"

unused = {2001: [], 2000: [], 1999: [], 1998: [], 1997: [], 1996: [], 1995: [], 1994: [], 1993: [], 1992: [], 1991: [], 1990: [], 1989: [], 1988: [], 1987: [], 1986: [], 1985: [], 1984: [], 1983: [], 1982: [], 1981: [], 1980: [], 1979: [], 1978: [], 1977: [], 1976: [], 1975: [], 1974: [], 1973: [], 1972: [], 1971: [], 1970: [], 1969: [], 1968: [], 1967: [], 1966: []}

def minutes_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def get_season_stats(team, season_year):
    url = f"{BASE_URL}teams/{team}/{season_year}/gamelog/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(15000)

        try:
            print(url)
            page.goto(url)
            page.wait_for_selector(f"#gamelog{season_year}")

            # Get page content
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')

            tables = [soup.find('table', id=f"gamelog{season_year}"), soup.find('table', id=f"playoff_gamelog{season_year}")]
            stats = []
            win_percentage = 0
            tot_games = 0

            for table in tables:
                if not table:
                    print("Game-by-game table not found.")
                    continue

                # Process rows
                rows = table.find('tbody').find_all('tr')
                if not rows:
                    print("No rows found in the table.")
                    continue

                for row in rows:
                    # Skip empty rows (e.g., placeholders for playoff games not yet played)
                    if row.find('td', {'data-stat': 'boxscore_word'}).text == "preview" or row.find('td', {'data-stat': 'opp'}).text == "Bye Week":
                        continue
                    if row.get('class') and 'thead' in row['class']:
                        continue
                    # Extract basic stats
                    tot_games += 1
                    game_week = row.find('th', {'data-stat': 'week_num'})
                    game_week = game_week.text if game_week else None

                    overtime = row.find('td', {'data-stat': 'overtime'})
                    overtime = overtime.text if overtime else None

                    outcome = row.find('td', {'data-stat': 'game_outcome'})
                    outcome = outcome.text if outcome else None

                    if outcome == 'W':
                        win_percentage += 1

                    game_location = row.find('td', {'data-stat': 'game_location'})
                    game_location = game_location.text if game_location else None

                    opponent = row.find('td', {'data-stat': 'opp'})
                    opponent = opponent.text if opponent else None

                    opponent_abbreviation = row.find('td', {'data-stat': 'opp'})
                    opponent_abbreviation = (
                        opponent_abbreviation.find('a')['href'].split('/')[2]
                        if opponent_abbreviation and opponent_abbreviation.find('a') else None
                    )

                    points_scored = row.find('td', {'data-stat': 'pts_off'})
                    points_scored = points_scored.text if points_scored else None

                    points_allowed = row.find('td', {'data-stat': 'pts_def'})
                    points_allowed = points_allowed.text if points_allowed else None

                    passes_completed = row.find('td', {'data-stat': 'pass_cmp'})
                    passes_completed = passes_completed.text if passes_completed else None

                    passes_attempted = row.find('td', {'data-stat': 'pass_att'})
                    passes_attempted = passes_attempted.text if passes_attempted else None

                    passing_yards = row.find('td', {'data-stat': 'pass_yds'})
                    passing_yards = passing_yards.text if passing_yards else None

                    passing_td = row.find('td', {'data-stat': 'pass_td'})
                    passing_td = passing_td.text if passing_td else None

                    interceptions = row.find('td', {'data-stat': 'pass_int'})
                    interceptions = interceptions.text if interceptions else None

                    times_sacked = row.find('td', {'data-stat': 'pass_sacked'})
                    times_sacked = times_sacked.text if times_sacked else None

                    yards_sacked = row.find('td', {'data-stat': 'pass_sacked_yds'})
                    yards_sacked = yards_sacked.text if yards_sacked else None

                    yards_per_attempt = row.find('td', {'data-stat': 'pass_yds_per_att'})
                    yards_per_attempt = yards_per_attempt.text if yards_per_attempt else None

                    net_yards_per_attempt = row.find('td', {'data-stat': 'pass_net_yds_per_att'})
                    net_yards_per_attempt = net_yards_per_attempt.text if net_yards_per_attempt else None

                    completion_rate = row.find('td', {'data-stat': 'pass_cmp_perc'})
                    completion_rate = completion_rate.text if completion_rate else None

                    passer_rating = row.find('td', {'data-stat': 'pass_rating'})
                    passer_rating = passer_rating.text if passer_rating else None

                    rushing_attempts = row.find('td', {'data-stat': 'rush_att'})
                    rushing_attempts = rushing_attempts.text if rushing_attempts else None

                    rushing_yards = row.find('td', {'data-stat': 'rush_yds'})
                    rushing_yards = rushing_yards.text if rushing_yards else None

                    rushing_yards_per_attempt = row.find('td', {'data-stat': 'rush_yds_per_att'})
                    rushing_yards_per_attempt = rushing_yards_per_attempt.text if rushing_yards_per_attempt else None

                    rushing_td = row.find('td', {'data-stat': 'rush_td'})
                    rushing_td = rushing_td.text if rushing_td else None

                    field_goals_made = row.find('td', {'data-stat': 'fgm'})
                    field_goals_made = field_goals_made.text if field_goals_made else None

                    field_goals_attempted = row.find('td', {'data-stat': 'fga'})
                    field_goals_attempted = field_goals_attempted.text if field_goals_attempted else None

                    extra_points_made = row.find('td', {'data-stat': 'xpm'})
                    extra_points_made = extra_points_made.text if extra_points_made else None

                    extra_points_attempted = row.find('td', {'data-stat': 'xpa'})
                    extra_points_attempted = extra_points_attempted.text if extra_points_attempted else None

                    punts = row.find('td', {'data-stat': 'punt'})
                    punts = punts.text if punts else None

                    punting_yards = row.find('td', {'data-stat': 'punt_yds'})
                    punting_yards = punting_yards.text if punting_yards else None

                    third_down_conversions = row.find('td', {'data-stat': 'third_down_success'})
                    third_down_conversions = third_down_conversions.text if third_down_conversions else None

                    third_down_attempts = row.find('td', {'data-stat': 'third_down_att'})
                    third_down_attempts = third_down_attempts.text if third_down_attempts else None

                    fourth_down_conversions = row.find('td', {'data-stat': 'fourth_down_success'})
                    fourth_down_conversions = fourth_down_conversions.text if fourth_down_conversions else None

                    fourth_down_attempts = row.find('td', {'data-stat': 'fourth_down_att'})
                    fourth_down_attempts = fourth_down_attempts.text if fourth_down_attempts else None

                    time_in_possession = row.find('td', {'data-stat': 'time_of_poss'})
                    time_in_possession = time_in_possession.text if time_in_possession else None

                    if game_week and points_scored:
                        stats.append({
                            "Game Week": int(game_week) if game_week and game_week.strip() else None,
                            "Win Percentage": win_percentage / tot_games,
                            "Overtime": 1 if overtime and overtime.strip() else (0 if overtime else None),
                            "Outcome": 1 if outcome and outcome.strip() == "W" else (0 if outcome and outcome.strip() else None),
                            "Home Game": 0 if game_location and game_location.strip() == "@" else (1 if game_location and game_location.strip() else None),
                            "Opponent": opponent.split(" ")[-1] if opponent else None,
                            "Opponent Abbreviation": opponent_abbreviation if opponent and opponent.find('a') else None,
                            "Points Scored": int(points_scored) if points_scored and points_scored.strip() else None,
                            "Points Allowed": int(points_allowed) if points_allowed and points_allowed.strip() else None,
                            "Passes Completed": int(passes_completed) if passes_completed and passes_completed.strip() else None,
                            "Passes Attempted": int(passes_attempted) if passes_attempted and passes_attempted.strip() else None,
                            "Passing Yards": int(passing_yards) if passing_yards and passing_yards.strip() else None,
                            "Passing TD": int(passing_td) if passing_td and passing_td.strip() else None,
                            "Interceptions": int(interceptions) if interceptions and interceptions.strip() else None,
                            "Times Sacked": int(times_sacked) if times_sacked and times_sacked.strip() else None,
                            "Yards Sacked": int(yards_sacked) if yards_sacked and yards_sacked.strip() else None,
                            "Yards per Attempt": float(yards_per_attempt) if yards_per_attempt and yards_per_attempt.strip() else None,
                            "Net Yards per Attempt": float(net_yards_per_attempt) if net_yards_per_attempt and net_yards_per_attempt.strip() else None,
                            "Completion Rate": float(completion_rate) if completion_rate and completion_rate.strip() else None,
                            "Passer Rating": float(passer_rating) if passer_rating and passer_rating.strip() else None,
                            "Rushing Attempts": int(rushing_attempts) if rushing_attempts and rushing_attempts.strip() else None,
                            "Rushing Yards": int(rushing_yards) if rushing_yards and rushing_yards.strip() else None,
                            "Rushing Yards per Attempt": float(rushing_yards_per_attempt) if rushing_yards_per_attempt and rushing_yards_per_attempt.strip() else None,
                            "Rushing TD": int(rushing_td) if rushing_td and rushing_td.strip() else None,
                            "Field Goals Made": int(field_goals_made) if field_goals_made and field_goals_made.strip() else None,
                            "Field Goals Attempted": int(field_goals_attempted) if field_goals_attempted and field_goals_attempted.strip() else None,
                            "Extra Points Made": int(extra_points_made) if extra_points_made and extra_points_made.strip() else None,
                            "Extra Points Attempted": int(extra_points_attempted) if extra_points_attempted and extra_points_attempted.strip() else None,
                            "Punts": int(punts) if punts and punts.strip() else None,
                            "Punting Yards": int(punting_yards) if punting_yards and punting_yards.strip() else None,
                            "Third Down Conversions": int(third_down_conversions) if third_down_conversions and third_down_conversions.strip() else None,
                            "Third Down Attempts": int(third_down_attempts) if third_down_attempts and third_down_attempts.strip() else None,
                            "Fourth Down Conversions": int(fourth_down_conversions) if fourth_down_conversions and fourth_down_conversions.strip() else None,
                            "Fourth Down Attempts": int(fourth_down_attempts) if fourth_down_attempts and fourth_down_attempts.strip() else None,
                            "Time of Possession in Seconds": minutes_to_seconds(time_in_possession) if time_in_possession and time_in_possession.strip() else None,
                        })
            browser.close()
            print(f"Team {team} completed")
            return stats

        except Exception as e:
            traceback.print_exc()
            browser.close()
            print(e) 


faulty_teams = {24: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 25: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 26: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 27: {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 28: {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 29: {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 30: {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 31: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 32: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 33: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 34: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 35: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 36: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 37: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 38: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 39: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 40: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 41: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 42: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 43: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 44: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 45: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 46: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 47: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 48: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 49: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}, 50: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 51: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 52: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 53: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 54: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 55: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 56: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 57: {1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 58: {1, 2, 4, 6, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32}, 59: {1, 2, 4, 6, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 31, 32}}
id_to_team_abr = {value: key for key, value in team_abr_ids.items()}
id_to_season = {value: key for key, value in season_ids.items()}
print(id_to_team_abr)
for year_id in faulty_teams:
    year = id_to_season[year_id]
    season_id = year_id
    for team_id in faulty_teams[season_id]:
        team = id_to_team_abr[team_id]
        url = BASE_URL.format(team=team, year=year)
        team_id = team_abr_ids[team]
        sleep(7)
        print(year, team)
        try:
            stats = get_season_stats(team, year)
            try:
                for game in stats:
                    opp_id = team_abr_ids[game['Opponent Abbreviation']]
                    update_game_stats = update_game_home_stats

                    search_previous_game_values = (game['Game Week'], season_id, team_id, opp_id)
                    cursor.execute(search_previous_game, search_previous_game_values)
                    game_inserted = cursor.fetchall()
                    if not game_inserted:
                        print("PROBLEM")
                    else:
                        game_id = game_inserted[0][0]
                        home_stats_id = game_inserted[0][4]
                        away_stats_id = game_inserted[0][5]

                        cursor.execute("""UPDATE game_stats SET overtime = %s, set game_location = %s WHERE id = %s
                                       """, (game['Overtime'], game['Home Game'], home_stats_id))
                        cursor.execute("""UPDATE game_stats SET overtime = %s, set game_location = %s WHERE id = %s
                                       """, (game['Overtime'], not game['Home Game'], away_stats_id))
                        
                        
            except Exception as e:
                print(f"Problem with games: {e}", f"Exiting on season: {year}")
                unused[year].append(team)
        except Exception as e:
            print(f"Problem getting stats: {e}", f"Exiting on season: {year}")
            unused[year].append(team)

db.commit()




"""
for year in super_bowl_years:
    season_id = season_ids[int(year)]
    for team in teams:
        url = BASE_URL.format(team=team, year=year)
        team_id = team_abr_ids[team]
        sleep(10)
        print(year, team)
        try:
            stats = get_season_stats(team, year)
            try:
                for game in stats:
                    opp_id = team_abr_ids[game['Opponent Abbreviation']]
                    update_game_stats = update_game_home_stats

                    search_previous_game_values = (game['Game Week'], season_id, opp_id, team_id)
                    cursor.execute(search_previous_game, search_previous_game_values)
                    game_inserted = cursor.fetchall()
                    if game_inserted:
                        game_id = game_inserted[0][0]
                        update_game_stats = update_game_away_stats
                    else:
                        game_data = (game['Game Week'], season_id, team_id, opp_id, None, None)
                        cursor.execute(insert_game, game_data)
                        db.commit()
                        game_id = cursor.lastrowid

                    game_stats_data = (game_id, team_id, game['Overtime'], game['Outcome'], game['Win Percentage'], 
                        game['Home Game'], opp_id, game['Points Scored'], game['Points Allowed'], 
                        game['Passes Completed'], game['Passes Attempted'], game['Passing Yards'], game['Passing TD'], 
                        game['Interceptions'], game['Times Sacked'], game['Yards Sacked'], game['Yards per Attempt'], 
                        game['Net Yards per Attempt'], game['Completion Rate'], game['Passer Rating'], game['Rushing Attempts'], 
                        game['Rushing Yards'], game['Rushing Yards per Attempt'], game['Rushing TD'], game['Field Goals Made'], 
                        game['Field Goals Attempted'], game['Extra Points Made'], game['Extra Points Attempted'], game['Punts'], 
                        game['Punting Yards'], game['Third Down Conversions'], game['Third Down Attempts'], 
                        game['Fourth Down Conversions'], game['Fourth Down Attempts'], game['Time of Possession in Seconds'])
                        
                    cursor.execute(insert_game_stats, game_stats_data)
                    db.commit()

                    game_stats_id = cursor.lastrowid
                    update_values = (game_stats_id, game_id)            
                    
                    cursor.execute(update_game_stats, update_values)
                    db.commit()
            except Exception as e:
                print(f"Problem with games: {e}", f"Exiting on season: {year}")
                unused[year].append(team)
        except Exception as e:
            print(f"Problem getting stats: {e}", f"Exiting on season: {year}")
            unused[year].append(team)
"""
print(unused)