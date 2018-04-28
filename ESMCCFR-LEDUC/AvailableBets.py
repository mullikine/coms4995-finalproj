class AvailableBets():
	def __init__(self, setup):
		self.setup = setup

	def _get_debt(self, pov, oppo):
		debt = oppo - pov
		if debt < 0:
			raise Error(
				'Debt %d < 0 for pov %d and oppo %d' %
				(debt, pov, oppo))
		return debt

	def _get_remaining(self, pov):
		remaining = self.setup.stack_size - pov
		if remaining <= 0:
			raise Error(
				'Remaining %d < 0 for pov %d and stack %d' %
				(remaining, pov, self.setup.stack_size))
		return remaining

	def _get_minimum_raise(self, debt):
		return debt + max(self.setup.big_blind, debt)

	def get_bets_as_numbers(self, pov, oppo):
		debt = self._get_debt(pov, oppo)
		remaining = self._get_remaining(pov)
		minimum_raise = self._get_minimum_raise(debt)
		# set dedupes
		return list(sorted(set([0, debt] +
			list(range(minimum_raise, remaining+1))
			+ [remaining])))

	def get_bets_by_action_type(self, pov, oppo):
		debt = self._get_debt(pov, oppo)
		remaining = self._get_remaining(pov)
		minimum_raise = self._get_minimum_raise(debt)

		bets = dict()
		if debt == 0:
			bets['check'] = [0]
		else:
			bets['fold'] = [0]
			bets['call'] = [debt]

		# all in is not considered a raise here
		if remaining > minimum_raise:
			bets['raises'] = list(range(minimum_raise, remaining))

		if debt < remaining:
			bets['allIn'] = [remaining]

		return bets

	def get_word(self, actions, bet):
		return [key for key, value in actions.items() if bet in value][0]