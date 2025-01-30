import pandas as pd
from jira import JIRA
import json
import pathlib

path = str(pathlib.Path(__file__).parent.absolute())
user = str(pathlib.Path.home())

with open(user + '\\Desktop\\Config\\jira_api.json') as f:
    jira_auth = json.load(f)

jiraOptions = {'server': jira_auth['server']}
jira = JIRA(options=jiraOptions, basic_auth=(
    jira_auth['email'], jira_auth['token']))

date = '2026-01-01'
label = '***' #censored
brand_arch = '***' #censored

db = pd.DataFrame(columns=['key','summary','reporter','assignee','created','status'])
i = 1
while int(date[:4]) > 2022:
    for singleIssue in jira.search_issues(jql_str=f'(labels = {label} or brand_arch = {brand_arch}) and created <= {date}'): 
        db.loc[len(db)] = [singleIssue.key, singleIssue.fields.summary, singleIssue.fields.reporter.displayName, 
                           singleIssue.fields.assignee.displayName, singleIssue.fields.created, singleIssue.fields.status]
    min_date = db['created'].min()[:10]
    print(f'{i}. min date {min_date}')
    i += 1
    date = min_date


db['summary'] = db['summary'].str.replace('"', '%')
db.drop_duplicates(subset=['key'], inplace=True)
print(db)

db.to_csv(path + '\\jira_tickets.csv', index=False, header=True)