def get_phase_menstruelle(jour_debut: datetime.date, duree_cycle: int):
    """
    This method should help targeting the phase which the user is currently in.
    """
    print(f"Jour début : {jour_debut}, durée : {duree_cycle}")
    jour_actuel = datetime.date.today()
    jour_cycle = (jour_actuel - jour_debut).days + 1 

    jour_ovulation = duree_cycle - 14

    if jour_cycle <= 5:
        return "menstruelle"
    elif jour_cycle <= jour_ovulation:
        return "folliculaire"
    elif jour_cycle == jour_ovulation:
        return "ovulation"
    else: 
        return "lutéale"
