import DocsSigMember

# Import the latest membership file from community repo
member_list_file = 'membership.json'

# Import the latest pr and review raw data from pingcap metabase
pr_1_year_file = 'pr_1_year.json'
review_1_year_file = 'review_1_year.json'
pr_all_file = 'pr_all_file.json'

# Generate a dictionary of old members based on the current membership file
old_membership = DocsSigMember.generate_old_membership(member_list_file)

# Generate a dictionary of new members based on the current pr and review numbers
new_membership = DocsSigMember.generate_new_membership(pr_1_year_file, review_1_year_file, pr_all_file)

# Remove two bot id
new_membership['committers'].remove('ti-srebot')
new_membership['committers'].remove('sre-bot')
# Remove tech lead and co-lead
new_membership['committers'].remove('lilin90')
new_membership['committers'].remove('yikeke')


# Calibration 1:
# Committers are not demoted
for github_id in set(old_membership['committers'])-set(new_membership['committers']):
    new_membership['committers'].append(github_id)
    if github_id in new_membership['reviewers']:
        new_membership['reviewers'].remove(github_id)
    if github_id in new_membership['activeContributors']:
        new_membership['activeContributors'].remove(github_id)

# Reviewers are not demoted
for github_id in set(old_membership['reviewers'])-set(new_membership['reviewers']):
    if github_id not in new_membership['committers']:
        new_membership['reviewers'].append(github_id)
        if github_id in new_membership['activeContributors']:
            new_membership['activeContributors'].remove(github_id)


# Calibration 2:
# New committers need human judgement
print("Please tell whether the following members can be promoted to committers:")
tmp_committer_list = new_membership['committers'][:]
for github_id in set(tmp_committer_list)-set(old_membership['committers']):
    old_role = DocsSigMember.get_old_role(github_id, old_membership)
    # Judge if a github_id is eligible for committers
    judge1 = DocsSigMember.my_judgement(github_id, 'committers')
    if judge1 == False: # If not, demote it to reviewers
        new_membership['committers'].remove(github_id)
        new_membership['reviewers'].append(github_id)

print("\n\nPlease tell whether the following members can be promoted to reviewers:")
# New reviewers need human judgement
tmp_reviewer_list = new_membership['reviewers'][:]
for github_id in set(tmp_reviewer_list)-set(old_membership['reviewers']):
    # Judge if a github_id is eligible for reviewers
    judge = DocsSigMember.my_judgement(github_id, 'reviewers')
    # If not, restore it to the old role
    if judge == False:
        old_role = DocsSigMember.get_old_role(github_id, old_membership)
        new_membership['reviewers'].remove(github_id)
        new_membership[old_role].append(github_id)

# Output diff
DocsSigMember.diff_membership(new_membership, old_membership)
