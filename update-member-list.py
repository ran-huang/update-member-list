import DocsSigMember

member_list_file = 'membership.md'
committers = DocsSigMember.get_old_committers(member_list_file)
reviewers = DocsSigMember.get_old_reviewers(member_list_file)


# Generate a dictionary with github_id as keys and role as values
old_members_roles = DocsSigMember.generate_old_member_role(member_list_file)
new_members_roles = DocsSigMember.generate_new_member_role()


# For each member in the csv file,
# Calculate their role and stores in a dictionary
for member in new_members_roles.keys():
    pr = DocsSigMember.get_pr_number(member)
    review = DocsSigMember.get_review_number(member)
    role = DocsSigMember.cal_member_role(member,pr,review,committers,reviewers)
    new_members_roles[member] = role

# Compare the roles in two dictionaries, and show diff
for member in new_members_roles.keys():
    if old_members_roles.get(member) == None:
        print("New member: " + member + " (" + new_members_roles[member] + ")")
    elif old_members_roles[member] != new_members_roles[member]:
        print("Member role change: " + member +
              " ("+
              old_members_roles[member] + " -> " +
              new_members_roles[member] + ")")
    else:
        pass
