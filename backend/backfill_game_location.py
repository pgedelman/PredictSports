import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    auth_plugin="caching_sha2_password"
)

season_ids = {2024: 1, 2023: 2, 2022: 3, 2021: 4, 2020: 5, 2019: 6, 2018: 7, 2017: 8, 2016: 9, 2015: 10, 2014: 11, 2013: 12, 2012: 13, 2011: 14, 2010: 15, 2009: 16, 2008: 17, 2007: 18, 2006: 19, 2005: 20, 2004: 21, 2003: 22, 2002: 23, 2001: 24, 2000: 25, 1999: 26, 1998: 27, 1997: 28, 1996: 29, 1995: 30, 1994: 31, 1993: 32, 1992: 33, 1991: 34, 1990: 35, 1989: 36, 1988: 37, 1987: 38, 1986: 39, 1985: 40, 1984: 41, 1983: 42, 1982: 43, 1981: 44, 1980: 45, 1979: 46, 1978: 47, 1977: 48, 1976: 49, 1975: 50, 1974: 51, 1973: 52, 1972: 53, 1971: 54, 1970: 55, 1969: 56, 1968: 57, 1967: 58, 1966: 59}
team_abr_ids = {'crd': 1, 'atl': 2, 'rav': 3, 'buf': 4, 'car': 5, 'chi': 6, 'cin': 7, 'cle': 8, 'dal': 9, 'den': 10, 'det': 11, 'gnb': 12, 'htx': 13, 'clt': 14, 'jax': 15, 'kan': 16, 'rai': 17, 'sdg': 18, 'ram': 19, 'mia': 20, 'min': 21, 'nwe': 22, 'nor': 23, 'nyg': 24, 'nyj': 25, 'phi': 26, 'pit': 27, 'sfo': 28, 'sea': 29, 'tam': 30, 'oti': 31, 'was': 32}
team_name_ids = {'Cardinals': 1, 'Falcons': 2, 'Ravens': 3, 'Bills': 4, 'Panthers': 5, 'Bears': 6, 'Bengals': 7, 'Browns': 8, 'Cowboys': 9, 'Broncos': 10, 'Lions': 11, 'Packers': 12, 'Texans': 13, 'Colts': 14, 'Jaguars': 15, 'Chiefs': 16, 'Raiders': 17, 'Chargers': 18, 'Rams': 19, 'Dolphins': 20, 'Vikings': 21, 'Patriots': 22, 'Saints': 23, 'Giants': 24, 'Jets': 25, 'Eagles': 26, 'Steelers': 27, '49ers': 28, 'Seahawks': 29, 'Buccaneers': 30, 'Titans': 31, 'Commanders': 32}

cursor = db.cursor()

cursor.execute("""
    SELECT * FROM game_stats WHERE game_location IS NULL;
""")

rows = cursor.fetchall()

ids = []
for row in rows:
    cursor.execute("""
                    update game_stats set game_location = 1 where id = %s;
                   """, (row[0], ))
    ids.append(row[0])

db.commit()
print(ids)

cursor.close()
db.close()