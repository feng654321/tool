# git command

## git config
```
git config --global core.autocrlf input  # This will set the default ending character to LF.
git config --get core.autocrlf # Get the value of this setting.
```
## git basic command
```
git clone "ssh://xhe@gerrite1.ext.net.nokia.com:8282/netact/radio3" && (cd "radio3" && gitdir=$(git rev-parse --git-dir); curl -o ${gitdir}/hooks/commit-msg https://gerrite1.ext.net.nokia.com/static/commit-msg ; chmod +x ${gitdir}/hooks/commit-msg)

git branch <branch name>                   # Create branch
git checkout <branch name>                 # Switch branch
git checkout -b <branch name>              # Create branch and switch to it
git checkout --track origin/na18_a         # Create local branch with the same name as remote branch and track it
git branch na17_8 origin/na17_8            # Create local na17_8 branch and set upstream branch to remote na17_8
git branch --set-upstream-to=origin/master # Set current branch to track remote master

git status                       # List latest file status
git add <file>                   # Stage
git reset HEAD <file>            # Unstage
git checkout -- <file>           # Discard changes in working directory
git commit -m "test"             # Commit comment template: https://confluence.ext.net.nokia.com/display/MPP/GIT+commit+template
git commit --amend               # Commit and merge contents with previous commit
git reset HEAD^                  # Undo latest commit and keep the changes back to workspace
git reset --hard HEAD^           # Remove latest commit completely. Latest committed changes lost.
git review                       # Push the changes to gerrit for review

git checkout filename            # revert untracked changes for one file, this will checkout the file from HEAD, overwriting the change
git reset --hard                 # revert/resets all uncommitted changes
git clean -fd                    # revert all uncommitted changes including files and folders

git pull                         # Pull the latest changes from remote master branch. You need to checkout to master first
git rebase master                # Update branch code based on master
git branch -d <branch name>      # Delete branch
git branch -v                    # List the latest change of every branch
git branch -vv                   # List the latest change of every branch and also show the upstream branch
git cherry -v                    # Show unmerged changes of current branch

git stash                        # Save the changes in your working directory temporarily.
git stash list                   # List your saved working copies.
git stash pop                    # Retrieve the very first save copy of your working directory and delete the save copy.
git stash drop <stash_id>        # Delete the specific saved copy.

git update-index --assume-unchanged com.nsn.oss.nwi3/implementation/robot/remote-test/taHelpers/editable.runTA.properties      # Tell Git to ignore tracked file
git update-index --no-assume-unchanged com.nsn.oss.nwi3/implementation/robot/remote-test/taHelpers/editable.runTA.properties   # Undo Git to ignore tracked file

git config --global core.autocrlf input          # This will set the default ending character to LF.
git config --get core.autocrlf                   # Get the value of this setting.
git config user.email "evan.he@nokia-sbell.com"  # Set the email used by gerrit review
git config --get user.email                      # Get the email used by gerrit review
```

## Git alias configure
```
C:\Users\<LoginName>\.gitconfig
[alias]
co = checkout
rb = rebase
ci = commit
st = status
br = branch
hist = log --pretty=format:\"%h %ad | %s%d [%an]\" --graph --date=short
```

## gitignore
```
  .gitignore文件，用于忽略不需要提交的文件。有了".gitignore"文件，用户可以不用指定每一个需要提交的文件，帮助提高代码提交的效率。
```
1. 在repo下，新建 ".gitignore"文件
2. 在".gitignore"文件中，添加要过滤的文件，如下：
   ![image](https://github.com/user-attachments/assets/4168f61b-7d2c-427c-8373-6da2c4a8947c)

