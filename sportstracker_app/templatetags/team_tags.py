from django import template
from types import SimpleNamespace
import re

register = template.Library()

CODES = [
    "ARI","ATL","BAL","BUF","CAR","CHI","CIN","CLE","DAL","DEN","DET","GB","HOU","IND",
    "JAX","KC","LAC","LAR","LV","MIA","MIN","NE","NO","NYG","NYJ","PHI","PIT","SEA",
    "SF","TB","TEN","WAS"
]

ALIASES = {
    # NFC West
    "ARIZONA": "ARI", "CARDINALS": "ARI", "ARIZONA CARDINALS": "ARI",
    "LOS ANGELES RAMS": "LAR", "LA RAMS": "LAR", "RAMS": "LAR",
    "SAN FRANCISCO": "SF", "49ERS": "SF", "SAN FRANCISCO 49ERS": "SF",
    "SEATTLE": "SEA", "SEAHAWKS": "SEA", "SEATTLE SEAHAWKS": "SEA",

    # NFC South
    "ATLANTA": "ATL", "FALCONS": "ATL", "ATLANTA FALCONS": "ATL",
    "CAROLINA": "CAR", "PANTHERS": "CAR", "CAROLINA PANTHERS": "CAR",
    "NEW ORLEANS": "NO", "SAINTS": "NO", "NEW ORLEANS SAINTS": "NO",
    "TAMPA BAY": "TB", "BUCCANEERS": "TB", "TAMPA BAY BUCCANEERS": "TB",

    # NFC North
    "CHICAGO": "CHI", "BEARS": "CHI", "CHICAGO BEARS": "CHI",
    "DETROIT": "DET", "LIONS": "DET", "DETROIT LIONS": "DET",
    "GREEN BAY": "GB", "PACKERS": "GB", "GREEN BAY PACKERS": "GB",
    "MINNESOTA": "MIN", "VIKINGS": "MIN", "MINNESOTA VIKINGS": "MIN",

    # NFC East
    "DALLAS": "DAL", "COWBOYS": "DAL", "DALLAS COWBOYS": "DAL",
    "NEW YORK GIANTS": "NYG", "GIANTS": "NYG",
    "NEW YORK JETS": "NYJ", "JETS": "NYJ",
    "PHILADELPHIA": "PHI", "EAGLES": "PHI", "PHILADELPHIA EAGLES": "PHI",
    "WASHINGTON": "WAS", "COMMANDERS": "WAS", "WASHINGTON COMMANDERS": "WAS", "WSH": "WAS",

    # AFC West
    "DENVER": "DEN", "BRONCOS": "DEN", "DENVER BRONCOS": "DEN",
    "KANSAS CITY": "KC", "CHIEFS": "KC", "KANSAS CITY CHIEFS": "KC",
    "LAS VEGAS": "LV", "RAIDERS": "LV", "LAS VEGAS RAIDERS": "LV", "OAKLAND RAIDERS": "LV",
    "LOS ANGELES CHARGERS": "LAC", "LA CHARGERS": "LAC", "CHARGERS": "LAC",

    # AFC South
    "HOUSTON": "HOU", "TEXANS": "HOU", "HOUSTON TEXANS": "HOU",
    "INDIANAPOLIS": "IND", "COLTS": "IND", "INDIANAPOLIS COLTS": "IND",
    "JACKSONVILLE": "JAX", "JAGUARS": "JAX", "JACKSONVILLE JAGUARS": "JAX", "JAC": "JAX",
    "TENNESSEE": "TEN", "TITANS": "TEN", "TENNESSEE TITANS": "TEN",

    # AFC North
    "BALTIMORE": "BAL", "RAVENS": "BAL", "BALTIMORE RAVENS": "BAL",
    "CINCINNATI": "CIN", "BENGALS": "CIN", "CINCINNATI BENGALS": "CIN",
    "CLEVELAND": "CLE", "BROWNS": "CLE", "CLEVELAND BROWNS": "CLE",
    "PITTSBURGH": "PIT", "STEELERS": "PIT", "PITTSBURGH STEELERS": "PIT",

    # AFC East
    "BUFFALO": "BUF", "BILLS": "BUF", "BUFFALO BILLS": "BUF",
    "MIAMI": "MIA", "DOLPHINS": "MIA", "MIAMI DOLPHINS": "MIA",
    "NEW ENGLAND": "NE", "PATRIOTS": "NE", "NEW ENGLAND PATRIOTS": "NE",
    "BOSTON PATRIOTS": "NE",
}

INDEX = {code: code for code in CODES}
INDEX.update(ALIASES)

def normalize_key(value) -> str:
    s = str(value or "").strip().upper()
    # remove punctuation; keep letters, numbers, space
    s = re.sub(r"[^A-Z0-9 ]+", "", s)
    return s

def resolve_code(value) -> str | None:
    key = normalize_key(value)
    if key in INDEX:
        return INDEX[key]
    # Try two-word joins like "INDIANAPOLIS COLTS"
    parts = key.split()
    if len(parts) >= 2:
        joined = " ".join(parts)
        if joined in INDEX:
            return INDEX[joined]
    return None

def make_team(value) -> SimpleNamespace:
    code = resolve_code(value)
    if not code:
        # Return safe defaults (what you saw as UNK)
        return SimpleNamespace(
            abbr="UNK",
            logo_path="sportstracker_app/img/nfl/placeholder.svg",
        )
    return SimpleNamespace(
        abbr=code,
        logo_path=f"sportstracker_app/img/nfl/{code}.svg",
    )

@register.simple_tag
def team_by_name(value):
    """
    Map a variety of inputs (abbr, city, nickname, full name) to a team object:
      - .abbr       (e.g., 'IND')
      - .logo_path  (e.g., 'sportstracker_app/img/nfl/IND.svg')
    Never raises; returns placeholder if unknown.
    """
    return make_team(value)
