# Developer's Guide to This Project
This guide will serve as a how-to for the basic process of contributing to SpellIt

## Starting Up

**If you prefer to read the detailed GitHub guide on forks, see [here](https://help.github.com/articles/working-with-forks/)**

#### Pre-Requisite

1. Install [Git](https://git-scm.com/)

#### Forking the Project

1. Navigate to the main repository (repo): <https://github.com/Hun-Spell-It/SpellIt>
2. Click the "Fork" button in the upper right hand corner of the screen.
3. Once the repo has been forked, you will be taken to your local copy at <https://github.com/YOURUSERNAME/SpellIt>

#### Cloning Your Fork

1. Open a Terminal/ Command Line / Bash Shell and navigate to the desired directory for storing the project.
2. Clone using the following command:

```shell
$ git clone https://github.com/YOURUSERNAME/SpellIt.git
```

You will then have a local copy of the project

#### Setting Upstream

1. Change into the new directory ('cd SpellIt')
2. Add a remote to the original repo:

```shell
$ git remote add upstream https://github.com/Hun-Spell-It/SpellIt.git
```

## Starting Work

#### Getting Updates

Before creating a new branch, do the following:

1. Make sure you are on the `develop` branch

```shell
$ git status
On branch develop
Your branch is up-to-date with 'origin/develop'
```

If not currently on develop, make any necessary commits and then checkout the `develop` branch

```shell
$ git checkout develop
```

2. Do a pull with rebase against `upstream`
```shell
$ git pull --rebase upstream develop
```

This pulls in the most recent changes on the official develop branch, without a commit to your local repo.

3. Pusn the updated develop branch to your GitHub fork
```shell
$git push origin develop
```

#### Create a Branch

Before beginning work, you need to create a new branch specific to the issue or feature you are addressing. To keep naming consistent, pick from one of the following:

`feature/xxx`
`fix/xxx`
`release/xxx`
`hotfix/xxx`

where xxx is a short descriptor of the issue the branch addresses.

1. Create and switch to your new branch

```shell
$ git checkout -b [new_branch_name]
```

2. Push new branch to GitHub

```shell
$ git push origin [new_branch_name]
```

**For more info on the strategy for branch management please refer to [this](https://nvie.com/posts/a-successful-git-branching-model/).**


#### Make Your Changes

1. Make the desired changes, always making sure to work only on the branch you have created, and never directly on the `develop` branch. 

2. Use `git status` to see unstaged files.

3. Add the files you wish to update using `git add path/to/desiredfile.txt` or use `git add .` to add all unstaged files

4. Commit your edits using `git commit -m "Your short message here"`. 

5. If needed, squash your commits: 

```shell
$ git log					//to show all recent commits
$ git rebase -i HEAD~3		//to combine the previous 3 commits
```

Use `pick` for the desired commit, squash for the rest. Then modify the commit description.

6. Push your changes to GitHub

```shell
$ git push origin [branch_name]
```

## Creating a Pull Request

**If you prefer to read the detailed GitHub guide on Pull Requests, see:**

**[Creating Pull Requests](https://help.github.com/articles/proposing-changes-to-your-work-with-pull-requests/)
[Reviewing Pull Requests](https://help.github.com/articles/reviewing-changes-in-pull-requests/)
[Incorporating a Pull Request](https://help.github.com/articles/incorporating-changes-from-a-pull-request/)**

#### Initiating the Process

1. Once you have pushed commits to your local fork, navigate to that page, located at <https://github.com/YOURUSERNAME/SpellIt>

2. You will be prompted to create a pull request. If you are ready to add your code to the organization repo, click the button to start the pull request.

3. Make the pull request against SpellIt's main repo, on the `develop` branch. (The one exception to this rule is if a `release` branch is ready to be merged into the master branch. In this case, the pull request should be made to both `develop` and `master`)

4. Submit the pull request from your branch to SpellIt's `develop` branch.

5. In the body of the PR, include a detailed summary of the changes you made, and why. Also include who you expect to review your code, by using `@USERNAME` of the requrired reviewer. Only one review is required for merging to `develop`, while three are required for `master`. If you wish to tag the whole team, you may also use the command `@Hun-Spell-It/csci5030`.

#### Performing Code Reviews

1. If you have been tagged in a pull request, you should then review the changes requested. You can access the page using the search qualifier `review-requested:[USERNAME]` or `team-review-requested:[TEAMNAME]`.

2. On the main Hun-Spell-It/SpellIt page, click **Pull requests** and then select the pull request you'd like to review. 

3. Click **Files Changed**. Hover over the line where you want to make a comment and click the blue comment icon. Type your comment.

4. Click either **Start a review** or **Add review comment**

5. Click **Review changes** and then type a comment summarizing your feedback. 

6. Select whether the reivew is a **Comment**, **Approve**, or **Request Changes** and then submit the review.

#### Adjusting Your Pull Request

1. When changes to your pull request are requested, you will need to modify your code. You can simply make the changes on your local repo, and commit with `git commit --amend`. This will add the changes to your existing commit.

2. Force push to your fork to overwrite the old commit `git push --force`

3. Comment in the Pull Request conversation that you have made the requested changes. 


