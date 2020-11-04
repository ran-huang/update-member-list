import json

def get_pos_start(text, role=""):
    """ 返回特定 role 的起始行号 """
    pos_start = 0
    for line1 in text:
        pos_start += 1
        if role in line1:
            break
    pos_start += 1
    return pos_start

def get_pos_end(text, next_role=""):
    """ 返回特定 role 的结束行号 """
    pos_end = 0

    for line2 in text:
        pos_end += 1
        if next_role in line2:
            break
    pos_end -= 3
    return pos_end

def get_old_committers(filename):
    """ Read member list and generate the committers list """
    committers = []
    file_obj = open(filename, "r")
    text = file_obj.readlines()
    file_obj.close()

    pos_start = get_pos_start(text,"## Committers")  # 第一个 Committer 的行号
    pos_end = get_pos_end(text, "## Reviewers")  # 最后一个 Committer 的行号


    committers = text[pos_start:pos_end+1]
    return committers

def get_old_reviewers(filename):
    """ Read member list and generate the committers list """
    reviewers = []
    file_obj = open(filename, "r")
    text = file_obj.readlines()
    file_obj.close()

    pos_start = get_pos_start(text,"## Reviewers")  # 第一个 Reviewer 的行号
    pos_end = get_pos_end(text, "## Active Contributors")  # 最后一个 Reviewer 的行号

    reviewers = text[pos_start:pos_end+1]
    return reviewers


def cal_member_role(github_id, pr, review, committers, reviewers):
    """ Calculate the role of a github ID """
    if github_id in committers:
        role = 'Committers'
    elif github_id in reviewers:
        if review >= 20:
            role = 'Committers'
        else:
            role = 'Reviewers'
    else:
        # If a github_id doesn't belong to the two categories above
        if pr < 8:
            role = 'Contributors'
        elif pr >= 8 and pr < 20:
            role = 'Active Contributors'
        elif pr >= 20 and review < 20:
            role = 'Reviewers'
        else:
            role = 'Committers'
    return role

def generate_old_member_role():
    """Generate the old member-role dictionary"""
    file = open('member-list.md', "r")
    text = file.readlines()
    file.close()

    old_member_role = {}
    flag = 0

    for line in text:
        if "Reviewers" in line:
            break
        if "Committers" not in line and flag == 0:
            pass
        elif "Committers" in line:
            flag = 1
        elif flag == 1:
            if line == '\n':
                pass
            else:
                key = line.split('[')[1].split(']')[0]
                old_member_role[key] = "Committers"

    flag = 0
    for line in text:
        if "Active Contributors" in line:
            break
        if "Reviewers" not in line and flag == 0:
            pass
        elif "Reviewers" in line:
            flag = 1
        elif flag == 1:
            if line == '\n':
                pass
            else:
                key = line.split('[')[1].split(']')[0]
                old_member_role[key] = "Reviewers"

    flag = 0
    for line in text:
        if "## Contributors" in line:
            break
        if "Active Contributors" not in line and flag == 0:
            pass
        elif "Active Contributors" in line:
            flag = 1
        elif flag == 1:
            if line == '\n':
                pass
            else:
                key = line.split('[')[1].split(']')[0]
                old_member_role[key] = "Active Contributors"

    flag = 0
    for line in text:
        if "## Contributors" not in line and flag == 0:
            pass
        elif "## Contributors" in line:
            flag = 1
        elif flag == 1:
            if line == '\n':
                pass
            else:
                key = line.split('[')[1].split(']')[0]
                old_member_role[key] = "Contributors"

    return old_member_role

def generate_new_member_role():
    file = open('doc-pr-ranklist.json', "r")
    dict_list = json.load(file)
    file.close()

    new_member_role = {}
    for dictionary in dict_list:
        new_member_role[dictionary['user']] = ''

    return new_member_role

def get_pr_number(member):
    file = open('doc-pr-ranklist-in-recent-1-year.json', "r")
    dict_list = json.load(file)
    file.close()

    pr = 0
    for dictionary in dict_list:
        if dictionary['user'] == member:
            pr = dictionary['pr_num']

    return pr

def get_review_number(member):
    file = open('doc-review-ranklist-in-recent-1-year.json', "r")
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