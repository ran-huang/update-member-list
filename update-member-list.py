from DocsSigMember import get_old_committers, get_old_reviewers, cal_member_role

committers = get_old_committers()
reviewers = get_old_reviewers()


# generate a dictionary with github_id as keys and role as values
old_members_roles = {}
new_members_roles = {}
# To be added


# For each member in the contributor list
# Calculate their role and stores in a dictionary
for member in new_members_roles.keys():
    role = cal_member_role(member)
    new_members_roles[member] = role

# Compare the roles in two dictionaries, and show diff
for member in new_members_roles.keys():
    if old_members_roles[member] = '':
        print("New member: " + member + " (" + new_members_roles[member] + ")")
    elif old_members_roles[member] != new_members_roles[member]:
        print("Member role change: " + member +
              " ("
              old_members_roles[member] + " -> " +
              new_members_roles[member] + ")")
    else:
        pass
