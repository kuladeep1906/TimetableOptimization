from deap import tools # type: ignore

def select_best(individuals, k=3):
    """
    Tournament selection to pick the best individuals.
    """
    return tools.selTournament(individuals, k, tournsize=3)
