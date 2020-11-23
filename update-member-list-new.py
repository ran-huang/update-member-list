import DocsSigMember

member_list_file = 'membership.json'
pr_1_year_file = 'pr_1_year.csv'
review_1_year_file = 'review_1_year.csv'
pr_all_file = 'pr_all_file.csv'

"""
Generate a dictionary of old members
based on the current json file
old_membership = {
    'committers': [],
    'reviewers': [],
    'active contributors': [],
}
"""

old_membership = DocsSigMember.generate_old_membership(member_list_file)

"""
Generate a dictionary of new members
based on the current pr and review numbers
new_membership = {
    'committers': [],
    'reviewers': [],
    'active contributors': [],
}
"""
new_membership = DocsSigMember.generate_new_membership(pr_1_year_file, review_1_year_file, pr_all_file)


# Calibration 1: committers and reviewers are not demoted
for github_id in old_membership['committers']:
    if github_id not in new_membership['committers']:
        new_membership['committers'].append(github_id)
        if github_id in new_membership['reviewers']:
            new_membership['reviewers'].remove(github_id)
        if github_id in new_membership['activeContributors']:
            new_membership['activeContributors'].remove(github_id)

for github_id in old_membership['reviewers']:
    if github_id in new_membership['committers'] or github_id in new_membership['reviewers']:
        continue
    else:
        new_membership['reviewers'].append(github_id)
        if github_id in new_membership['activeContributors']:
            new_membership['activeContributors'].remove(github_id)

# Calibration 2: committers and reviewers promotion
#                needs human judgement
for github_id in new_membership['committers']:
    if github_id not in old_membership['committers']:
        judge = DocsSigMember.my_judgement(github_id,'committers')
        if judge == False:
            # restore it to the old role
            old_role = get_old_role(github_id)

for github_id in new_membership['reviewers']:
    if github_id not in old_membership['reviewers']:
        judge = DocsSigMember.my_judgement(github_id,'reviewers')
        if judge == False:
            #restore it to the old role


# Output diff

