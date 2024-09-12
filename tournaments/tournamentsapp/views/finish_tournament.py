from tournamentsapp.status_options import StatusTournaments, Rounds
from tournamentsapp.models import Tournaments, Matches

try: 
	from usermodel.models import User
except:
	from ..models import User

def finish_tournament(tournament_id):
	tournament = Tournaments.objects.get(id=tournament_id)
	list_of_matches = Matches.objects.filter(tournament_id=tournament.id)
	for match in list_of_matches:
		if match.round == Rounds.FINAL_ROUND.value:
			tournament.id_winner = match.winner_id
			tournament.id_second = match.looser_id
			user = User.objects.get(id = tournament.id_winner)
			user.puntos += tournament.price_1
			user.save()
			user = User.objects.get(id = tournament.id_second)
			user.puntos += tournament.price_2
			user.save()
		elif match.round == Rounds.THIRD_PLACE_ROUND.value:
			tournament.id_third = match.winner_id
			user = User.objects.get(id=tournament.id_third)
			user.puntos += tournament.price_3
			user.save()
	tournament.status = StatusTournaments.FINISHED_TOURNAMENT.value
	tournament.save()
