import sys
import os
from github import Github
from git import Repo

class RepoMerger:
    def __init__(self):
        token = os.environ.get("GITHUB_ACCESS_TOKEN")
        self.user = os.environ.get("GITHUB_USERNAME")
        self.reponames = self.loadRepos()
        self.git = self.authGithub()
        self.confirmRepositories()
        self.createNewRepo()
        self.cloneRepos()
        self.cleanPulledRepos()
        self.pushRepo()

    def appendUser(self, repo):
        repo = repo.strip()
        return "{user}/{repo}".format(user=self.user, repo=repo)

    def loadRepos(self):
        file = open('repolist.txt', 'r+')
        reponames = file.readlines()
        if len(reponames) == 0:
            print("No repos provided", file=sys.stderr)
            sys.exit(1)
        reponames = list(map(self.appendUser, reponames))
        print("Loaded repository list...")
        return reponames

    def authGithub(self, token):
        g = Github(token)
        print("Authenticated to github...")
        return g
    
    def confirmRepositories(self):
        self.repos = list()
        for repo in self.reponames:
            print("Confirming repo: \"{repo}\"... ".format(repo=repo), end='\t')
            try:
                r = self.git.get_repo(repo)
                self.repos.append(r)
                print("\tconfirmed")
            except:
                print("\tfailed")
                sys.exit(1)
        print("All repositories confirmed")

    def createNewRepo(self):
        r = None
        self.newrepo = input("Enter new repository name: ")
        if os.path.exists(self.newrepo):
            print("Directory already exists")
            sys.exit(1)
        try:
            r = self.git.get_repo(self.newrepo)
            "Repo already exists... cloning"
        except:
            user = self.git.get_user()
            r = user.create_repo(self.newrepo, description = "{repo} created from MergeRepos".format(repo=self.newrepo))
            "Repo created... cloning"
        Repo.clone_from(r.ssh_url, self.newrepo)
        print("Cloned Repo")
        os.chdir(self.newrepo)


    def cloneRepos(self):
        print("Cloning all repos from list")
        for repo in self.repos:
            print("Cloning repo {repo}...".format(repo=repo.name), end="\t")
            try:
                Repo.clone_from(repo.ssh_url, repo.name)
                print("success")
            except Exception as e:
                print("failed")
                print(e)
                sys.exit(1)
        print("All repositories cloned.")

    def cleanPulledRepos(self):
        print("Cleaning repos")
        for repo in self.repos:
            print("Cleaning repo {repo}...".format(repo=repo.name), end="\t")
            try:
                os.system("rm -rf {repodir}/.git".format(repodir=repo.name))
                print("success")
            except:
                print("failed")
        print("All repos cleaned")

    def pushRepo(self):
        print("Pushing to remote")
        os.system("git add * && git commit -m \"Commited from GitMerger\" && git push")
        confirmation = input("Please confirm the push to upstream was successful (Y/N): ")
        if(confirmation == "Y"):
            for repo in self.repos:
                print("Deleting repo {repo}...".format(repo=repo.name), end="\t")
                try:
                    repo.delete()
                    print("success")
                except:
                    print("failed")
            
        print("Done")

r = RepoMerger()
