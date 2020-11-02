class DocsSigMeber():
    def __init__(self, github_id, pr_number=0, review_number=0):
        self.github_id = github_id
        self.pr_number = pr_number
        self.review_number = review_number

    def get_pr_number_1year(self):
        # Open the csv file that stores the pr number in the past 1 year
        # with open(xx.csv) as file_obj:
        if self.github_id in


def get_old_committers():
    """ Read member list and generate the committers list """
    committers = []
    with open('member-list.md') as file_obj:
        return committers


def get_old_reviewers():
    """ Read member list and generate the committers list """
    reviewers = []
    with open('member-list.md') as file_obj:
        # Get the list of existing committers and reviewers
        return reviewers


def cal_member_role(github_id, committers=committers, reviewers=reviewers, pr, review):
    """ Calculate the role of a github ID """
    if github_id in committers:
        role = 'committer'
    elif github_id in reviewers:
        if review >= 20:
            role = 'committer'
        else:
            role = 'reviewer'
    else:
        # If a github_id doesn't belong to the two categories above
        if pr < 8:
            role = 'contributor'
        elif pr >= 8 and pr < 20:
            role = 'active contributor'
        elif pr >= 20 and review < 20:
            role = 'reviewer'
        else:
            role = 'committer'
    return role
