# UPDATE (2/25/26) There are two separate branches!
1. Top Left should indicate the current branch (in git, you can check the current branch with `git branch --show`)

## If it is showing `main`, perform these commands:
1. `git branch -m main prototype`
2. `git fetch origin`
3. `git branch -u origin/prototype prototype`
4. `git remote set-head origin -a`
5. `git switch prototype`
Now, the branch should be pointing to `prototype`.

## To switch over to the `final` branch:
1. `git switch final`
2. `git branch --show` (to check the current branch)

-----

# How to add github repository to your computer:
1. Open Terminal (MacOS)/Git Bash (Windows)
2. Change directory to preferred folder where you want the files to go
(ie. `cd username/PycharmProjects/IMT561`)
3. `git clone https://github.com/nessa-c/Airline_Delay_Analysis.git`
4. `cd Airline_Delay_Analysis`

Now you can work on the project, make new files, change existing ones, etc.

# Anytime you have a change you want to push to the repository, you should do the following:
1. `git add .`
2. `git commit -m "INSERT SUMMARY OF CHANGES HERE"`
3. `git push origin main`

# Before making any changes when reopening the project, make sure you do:
1. `git pull origin main`

# Note About merge conflicts:
If two people edit the same file (or the same lines in a file) at the same time, git may produce a merge conflict.
When this happens, you’ll need to manually review the file, choose which changes to keep, and then commit the resolved version.
1. `git add .`
2. `git commit -m "SUMMARY OF WHAT WAS CHANGED"`
3. `git push origin main`