from django.core.management import BaseCommand
from sportstracker_app.models import Team

NFL = {
    "Arizona Cardinals": ("ARI", "img/nfl/ARI.svg"),
    "Atlanta Falcons": ("ATL", "img/nfl/ATL.svg"),
    "Baltimore Ravens": ("BAL", "img/nfl/BAL.svg"),
    "Buffalo Bills": ("BUF", "img/nfl/BUF.svg"),
    "Carolina Panthers": ("CAR", "img/nfl/CAR.svg"),
    "Chicago Bears": ("CHI", "img/nfl/CHI.svg"),
    "Cincinnati Bengals": ("CIN", "img/nfl/CIN.svg"),
    "Cleveland Browns": ("CLE", "img/nfl/CLE.svg"),
    "Dallas Cowboys": ("DAL", "img/nfl/DAL.svg"),
    "Denver Broncos": ("DEN", "img/nfl/DEN.svg"),
    "Detroit Lions": ("DET", "img/nfl/DET.svg"),
    "Green Bay Packers": ("GB",  "img/nfl/GB.svg"),
    "Houston Texans": ("HOU", "img/nfl/HOU.svg"),
    "Indianapolis Colts": ("IND", "img/nfl/IND.svg"),
    "Jacksonville Jaguars": ("JAX", "img/nfl/JAX.svg"),
    "Kansas City Chiefs": ("KC", "img/nfl/KC.svg"),
    "Las Vegas Raiders": ("LV", "img/nfl/LV.svg"),
    "Los Angeles Chargers": ("LAC", "img/nfl/LAC.svg"),
    "Los Angeles Rams": ("LAR", "img/nfl/LAR.svg"),
    "Miami Dolphins": ("MIA", "img/nfl/MIA.svg"),
    "Minnesota Vikings": ("MIN", "img/nfl/MIN.svg"),
    "New England Patriots": ("NE", "img/nfl/NE.svg"),
    "New Orleans Saints": ("NO", "img/nfl/NO.svg"),
    "New York Giants": ("NYG", "img/nfl/NYG.svg"),
    "New York Jets": ("NYJ", "img/nfl/NYJ.svg"),
    "Philadelphia Eagles": ("PHI", "img/nfl/PHI.svg"),
    "Pittsburgh Steelers": ("PIT", "img/nfl/PIT.svg"),
    "San Francisco 49ers": ("SF", "img/nfl/SF.svg"),
    "Seattle Seahawks": ("SEA", "img/nfl/SEA.svg"),
    "Tampa Bay Buccaneers": ("TB", "img/nfl/TB.svg"),
    "Tennessee Titans": ("TEN", "img/nfl/TEN.svg"),
    "Washington Commanders": ("WAS", "img/nfl/WAS.svg"),
}

class Command(BaseCommand):
    help = "Create or update NFL Team rows with abbr and logo_path."

    def handle(self, *args, **kwargs):
        created = 0
        updated = 0

        # Detect optional fields
        team_fields = {f.name for f in Team._meta.get_fields()}
        has_league = "league" in team_fields
        has_slug = "slug" in team_fields

        for name, (abbr, logo) in NFL.items():
            defaults = {"abbr": abbr, "logo_path": logo}
            if has_league:
                defaults["league"] = "nfl"
            if has_slug:
                defaults["slug"] = abbr.lower()

            obj, was_created = Team.objects.update_or_create(
                name=name, defaults=defaults
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created}, updated {updated}."
        ))
