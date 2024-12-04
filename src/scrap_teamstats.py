import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_team_stats(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "per_game-team"})
    if not table:
        print("Stats table not found.")
        return None

    headers = [th.text for th in table.find("thead").find_all("th")][1:]  # Skip rank
    rows = table.find("tbody").find_all("tr")
    data = [[td.text for td in row.find_all("td")] for row in rows if row.find("td")]

    df = pd.DataFrame(data, columns=headers)
    df.to_csv(f"data/team_stats_{year}.csv", index=False)
    print(f"Team stats for {year} saved.")
    return df

# Example usage
if __name__ == "__main__":
    scrape_team_stats(2023)
