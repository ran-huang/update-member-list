import DocsSigMember

member_list_file = 'membership.json'
pr_1_year_file = 'pr_1_year.json'
review_1_year_file = 'review_1_year.json'
pr_all_file = 'pr_all_file.json'

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

# Remove some special id
new_membership['committers'].remove('ti-srebot')
new_membership['committers'].remove('sre-bot')
new_membership['committers'].remove('lilin90')
new_membership['committers'].remove('yikeke')

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

# Calibration 2: new committers and reviewers
#                need human judgement

# If not ready to promote to committers
tmp_committer_list = new_membership['committers'][:]
for github_id in tmp_committer_list:
    if github_id not in old_membership['committers']:
        judge = DocsSigMember.my_judgement(github_id,'committers')
        if judge == False:
            # restore it to the old role
            old_role = DocsSigMember.get_old_role(github_id, old_membership)
            new_membership['committers'].remove(github_id)
            new_membership[old_role].append(github_id)

# If not ready to promote to reviewers
tmp_reviewer_list = new_membership['reviewers'][:]
for github_id in tmp_reviewer_list:
    if github_id not in old_membership['reviewers']:
        judge = DocsSigMember.my_judgement(github_id,'reviewers')
        if judge == False:
            #restore it to the old role
            old_role = DocsSigMember.get_old_role(github_id, old_membership)
            new_membership['reviewers'].remove(github_id)
            new_membership[old_role].append(github_id)

# Output diff
DocsSigMember.diff_membership(new_membership, old_membership)
