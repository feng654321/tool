# git squash 
git checkout master  
git pull origin master  
git checkout -b branchName  
git pull --rebase origin branchName  
git rebase -i master  
`Fix conflicts`  
git add <conflicts file>  
git rebase --continue  
```
It will open an interactive vi, and then only keep one pick, change other pick to squash.

pick 01d1124 Adding license    #only keep one first pick
squash 6340aaa Moving license into its own file
squash ebfd367 Jekyll has become self-aware.
squash 30e0ccb Changed the tagline in the binary, too.
...
```
Save with `wq!`, then will open anther interactive `vi`, you should keep one commit log you want.  
git push --force origin branchName  
## option 2
git pull --rebase origin <branch name>  
git checkout master  
git pull  
git checkout <branch name>  
git rebase -i master  
#verify conflicts  
git add .  
git rebase --continue  
git push --set-upstream origin <branch name> -f  
