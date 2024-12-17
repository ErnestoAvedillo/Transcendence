# tournamentsapp/tasks.py
from __future__ import absolute_import
from celery import shared_task
from tournamentsapp.models import Matches, Tournaments
from datetime import timedelta
from django.utils import timezone
from tournaments.settings import TIME_DELTA
from tournamentsapp.status_options import StatusMatches, StatusTournaments
from tournamentsapp.tasks.actualise_tournaments import actualise_tournament
import uuid
import logging

logger = logging.getLogger('django')
@shared_task
def check_match_db_status():
	matches_passed = Matches.objects.filter(date_time__lt = timezone.now() + timedelta(minutes = TIME_DELTA), status = StatusMatches.NOT_PLAYED.value)
	tournament_ids = []
	if matches_passed.count() == 0:
		logger.debug('No matches to abort')
		return None
	for mymatch in matches_passed:
		logger.debug(f'Match to aborted: {mymatch.id}')
		mymatch.winner_id = None
		mymatch.looser_id = None
		mymatch.status = StatusMatches.ABORTED.value
		mymatch.save()
		if mymatch.tournament_id not in tournament_ids:
			tournament_ids.append(mymatch.tournament_id)
	for mytournament_id in tournament_ids:
		mytournament = Tournaments.objects.get(id=mytournament_id)
		mymatches = Matches.objects.filter(tournament_id=mytournament_id, status__in=[StatusMatches.NOT_PLAYED.value])
		if mymatches.count() == 0:
			logger.debug(f'tournament passed to create next round: {mymatch.id}')
			mytournament.status = StatusTournaments.CREATE_NEXT_ROUND.value
			actualise_tournament(mymatch.mytournament_id)



"""			##**********************************************
	mymatches = Matches.objects.filter(tournament_id=mymatch.tournament_id, status__in=[
						StatusMatches.NOT_PLAYED.value])
	if mymatches.count() == 0:
			actualise_tournament(mymatch.id)
	mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
						StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	for mymatch in mymatches: 
		logger.info(f'longitud mymatches = {mymatch.id} --- {mymatch.status}')
	while mymatches.count() > 1:
		logger.info("actualizo torneo")
		actualise_tournament(mymatches[0].id)
		mymatches = Matches.objects.filter(tournament_id__in=tournament_ids, status__in=[
				StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
		for mymatch in mymatches: 
		    logger.info(f'longitud mymatch )= {mymatch.id} --- {mymatch.status}---{nmymatch.umber_round}')
	mymatches = Matches.objects.filter(
		tournament_id__in=tournament_ids, 
		status__in=[StatusMatches.PLAYED.value, StatusMatches.WALKOVER.value])
	if mymatches.count() == 1:
		logger.info("one match left without pair")
		match (mymatches[0].round):
			case 1:
				if mymatches[0].round == Rounds.FINAL_ROUND.value and mymatches[0].status == StatusMatches.WALKOVER.value:
					mymatches[0].status = StatusMatches.PLAYED.value
					finish_tournament(tournament.id)
				if mymatches[0].round == Rounds.THIRD_PLACE_ROUND.value and mymatches[0].status == StatusMatches.WALKOVER.value:
					mymatches[0].status = StatusMatches.PLAYED.value
					actualise_tournament(mymatches[0].id)
			case 2:
				actualise_tournament(mymatches[0].id)
			case _:
				new_match = Matches.objects.create(date_time = timezone.now() + timedelta(minutes=TIME_DELTA))
				for field in mymatches[0]._meta.fields:
					if field.name != "id":  # Skip the ID field to avoid conflicts
						setattr(new_match, field.name, getattr(mymatches[0], field.name))
				new_match.round = Rounds.SEMIFINAL_ROUND.value if new_match.number_round == 3 else Rounds.QUALIFIED_ROUND.value
				new_match.number_round -=1
				new_match.save()
				

	return None
"""