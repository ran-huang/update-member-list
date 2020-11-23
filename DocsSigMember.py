import json


def my_judgement(github_id, role):
    """Judge if a github id can be promoted"""
    print("Should %s be promoted to %s? (y/n)" % github_id, role)
    answer = input()
    if answer == 'y':
        return True
    else:
        return False


def cal_member_role(github_id, pr, review):
    """ Calculate the role of a github ID """
    if pr < 8:
        role = 'Contributors'
    elif pr >= 8 and pr < 20:
        role = 'Active Contributors'
    elif pr >= 20 and review < 20:
        role = 'Reviewers'
    else:
        role = 'Committers'
    return role


def trim_format(tmp_list):
    """ 把 list 里的 dictionary 都变成 string """
    trimmed_list = []
    for i in (0, len(tmp_list)):
        trimmed_list[i] = tmp_list[i]['githubName']
    return trimmed_list


def generate_old_membership(memberlist):
    """Generate the old member-role dictionary"""
    file = open(memberlist, "r")
    text = file.read()
    file.close()
    tmp_dict = json.loads(text)  # 把 json 文件转化为 python dictionary

    memberlist['committers'] = trim_format(tmp_dict['committers'])
    memberlist['reviewers'] = trim_format(tmp_dict['reviewers'])
    memberlist['activeContributors'] = trim_format(
        tmp_dict['activeContributors'])

    return memberlist


def generate_new_membership(pr_1_year_file, review_1_year_file, pr_all_file):
    file = open(pr_all_file, "r")
    dict_list = json.load(file)
    file.close()

    new_membership = {}
    for dictionary in dict_list:
        new_membership[dictionary['user']] = ''

    for member in new_membership.keys():
        pr = get_pr_number(member, pr_1_year_file)
        review = get_review_number(member, review_1_year_file)
        new_membership[member] = cal_member_role(member, pr, review)

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


def trim_list(role_list):
    formatted_list = []
    for item in role_list:
        item = item.split('[')[1].split(']')[0]
        formatted_list.append(item)
    return formatted_list
