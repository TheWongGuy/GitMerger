# GitMerger
I got tired of having so many repositories on my account. This script lets you merge multiple repositories into a Monorepo.

Reads a list of repositories names from `repolist.txt` in the same directory as the script.
It creates a new repo on your account, clones all of the repos from `repolist` into that repository, then deletes all the repos from `repolist`.

## Setup
* Set an environment variable `GITHUB_ACCESS_TOKEN` with an OAuth token for your account
* Set an environment variable `GITHUB_USERNAME` with your Github username
* Create a list `repolist.txt` and add all your repo names
* Run
* Disclaimer: Uses pipenv for package management
