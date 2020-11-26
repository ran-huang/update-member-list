# update-member-list

This script can help you quickly calculate the membership changes of [Docs SIG](https://github.com/pingcap/community/tree/master/special-interest-groups/sig-docs).

## Usage

1. Clone this repo.

2. Download three JSON files from [PingCAP metabase collection 250](https://meta.pingcap.net/collection/250). Put the three file in the same directory of this repo, and name them as follows:

    - `pr_all_file.json`: all pull requests merged in 4 docs repos
    - `pr_1_year.json`: pull requests merged in 4 docs repos with the past 1 year
    - `review_1_year.json`: pull requests reviewed in 4 docs repos within the past 1 year

3. Download [`membership.json`](https://github.com/pingcap/community/blob/master/special-interest-groups/sig-docs/membership.json), which stores the current membership of Docs SIG.

4. Navigate to the directory, and run the following command:

    ```shell
    python3 main.py
    ```

5. The script will give prompt as to whether a member can be promoted to committers/reviewers. Answer with `y` or `n`.

    For example:

    ```
    Please tell whether the following members can be promoted to committers:
    juliezhang1112: committers? (y/n)
    n
    ```
  
   Active contributors are promoted automatically.
  
6. After you've answered all the questions, the script prints the membership changes:

    For example:

    ```
    New committers are: {'weekface'}

    New reviewers are: {'dragonly'}

    New active contributors are: {'wshwsh12'}
    ```
 
7. Update the Docs SIG [`membership.json`](https://github.com/pingcap/community/blob/master/special-interest-groups/sig-docs/membership.json) in the pingcap/community repo according to the results.
