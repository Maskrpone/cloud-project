import datetime


def get_phase_menstruelle(jour_debut: datetime.date, duree_cycle: int) -> str:
    """
    This method should help targeting the phase which the user is currently in.
    """
    jour_actuel = datetime.date.today()
    jour_cycle = (jour_actuel - jour_debut).days + 1

    jour_ovulation = duree_cycle - 14

    if jour_cycle <= 5:
        return "menstruelle"
    elif jour_cycle < jour_ovulation:
        return "folliculaire"
    elif jour_cycle == jour_ovulation:
        return "ovulation"
    else:
        return "lutéale"


