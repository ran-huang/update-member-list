import json


def my_judgement(github_id, role):
    """Judge if a github id can be promoted"""
    print(f'Should {github_id} be promoted to {role}? (y/n)')
    answer = input()
    if answer == 'y':
        return True
    else:
        return False


def cal_member_role(github_id, pr, review):
    """ Calculate the role of a github ID """
    if pr < 8:
        role = 'contributors'
    elif pr >= 8 and pr < 20:
        role = 'activeContributors'
    elif pr >= 20 and review < 20:
        role = 'reviewers'
    else:
        role = 'committers'
    return role


def trim_format(tmp_list):
    """ 把 list 里的 dictionary 都变成 string """
    trimmed_list = []
    for each_item in tmp_list:
        trimmed_list.append(each_item['githubName'])
    return trimmed_list


def generate_old_membership(member_list_file):
    """Generate the old member-role dictionary"""
    file = open(member_list_file, "r")
    text = file.read()
    file.close()
    tmp_dict = json.loads(text)  # 把 json 文件转化为 python dictionary

    memberlist = {}
    memberlist['committers'] = trim_format(tmp_dict['committers'])
    memberlist['reviewers'] = trim_format(tmp_dict['reviewers'])
    memberlist['activeContributors'] = trim_format(
        tmp_dict['activeContributors'])

    return memberlist


def generate_new_membership(pr_1_year_file, review_1_year_file, pr_all_file):
    file = open(pr_all_file, "r")
    dict_list = json.load(file)
    file.close()

    all_members = []
    for dictionary in dict_list:
        all_members.append(dictionary['user'])

    new_membership = {'committers':[], 'reviewers':[], 'activeContributors':[], 'contributors':[]}

    for member in all_members:
        pr = get_pr_number(member, pr_1_year_file)
        review = get_review_number(member, review_1_year_file)
        role = cal_member_role(member, pr, review)
        new_membership[role].append(member)

    return new_membership


def get_pr_number(member, pr_1_year_file):
    file = open(pr_1_year_file, "r")
    dict_list = json.load(file)
    file.close()

    pr = 0
    for dictionary in dict_list:
        if dictionary['user'] == member:
            pr = dictionary['pr_num']

    return pr


def get_review_number(member, review_1_year_file):
    file = open(review_1_year_file, "r")
    dict_list = json.load(file)
    file.close()

    review = 0

    for dictionary in dict_list:
        if dictionary['user'] == member:
            review = dictionary['review_num']

    return review


def get_old_role(github_id, old_membership):
    if github_id in old_membership['committers']:
        return 'committers'
    elif github_id in old_membership['reviewers']:
        return 'reviewers'
    elif github_id in old_membership['activeContributors']:
        return 'activeContributors'
    else:
        return 'contributors'


def trim_list(role_list):
    formatted_list = []
    for item in role_list:
        item = item.split('[')[1].split(']')[0]
        formatted_list.append(item)
    return formatted_list


def diff_membership(new_membership, old_membership):
    # diff new and old committers
    if sorted(new_membership['committers']) == sorted(old_membership['committers']):
        pass
    else:
        new_committers = set(new_membership['committers']) - set(old_membership['committers'])
        if new_committers:
            print(f'new committers are: {new_committers}')

    # diff new and old reviewers
    if sorted(new_membership['reviewers']) == sorted(old_membership['reviewers']):
        pass
    else:
        new_reviewers = set(new_membership['reviewers']) - set(old_membership['reviewers'])
        if new_reviewers:
            print(f'new reviewers are: {new_reviewers}')

    # diff new and old activeContributors
    if sorted(new_membership['activeContributors']) == sorted(old_membership['activeContributors']):
        pass
    else:
        new_activeContributors = set(new_membership['activeContributors']) - set(old_membership['activeContributors'])
        demoted_activeContributors = set(old_membership['activeContributors']) - set(new_membership['activeContributors'])
        if new_activeContributors:
            print(f'new active contributors are {new_activeContributors}')
        if demoted_activeContributors:
            print(f'The following members are demoted to contributors:\n {demoted_activeContributors}')
