class DuplicateTeamNameError(Exception):
    pass


class TeamNotFoundError(Exception):
    pass


class MemberNotFoundError(Exception):
    pass


class MemberAlreadyInTeamError(Exception):
    pass


class MemberNotInTeamError(Exception):
    pass
