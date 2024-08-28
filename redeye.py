import praw
import click
import csv
import re
import os
from praw.exceptions import RedditAPIException, ClientException
from requests.exceptions import RequestException


BLUE = '\033[34m'
RED = '\033[31m'
OKGREEN = '\033[92m'
ENDC = '\033[0m'


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
)


def scanner(save, username, v):
    emails_hits = []
    urls = []
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

    try:
        user = reddit.redditor(username)
    except (RedditAPIException, ClientException, Exception) as e:
        click.echo(f"{RED}Error: Failed to fetch Reddit user: {e}{ENDC}")
        return
    try:
        comments = user.comments.new(limit=None)
        posts = user.submissions.new(limit=None)
    except RequestException as e:
        click.echo(f"{RED}Error: Failed to fetch comments/posts: {e}{ENDC}")
        return
    except Exception as e:
        click.echo(f"{RED}Unexpected error: {e}{ENDC}")
        return

    if save:
        try:
            with open(f"{username}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Type", "ID", "Content", "Subreddit", "Timestamp"])

                for comment in comments:
                    writer.writerow(["Comment", comment.id, comment.body, str(
                        comment.subreddit), comment.created_utc])

                for submission in posts:
                    writer.writerow(["Post", submission.id, submission.title, str(
                        submission.subreddit), submission.created_utc])
        except IOError as e:
            click.echo(f"{RED}Error: Failed to write CSV file: {e}{ENDC}")
        except Exception as e:
            click.echo(f"{RED}Unexpected error: {e}{ENDC}")
    else:
        for comment in comments:
            body = str(comment.body)
            comment_url = "https://www.reddit.com/" + comment.permalink
            emails = re.findall(email_regex, body)
            emails = [(x, comment_url) for x in emails]
            post_urls = re.findall(url_regex, body)
            post_urls = [(x, comment_url) for x in post_urls]

            if emails:
                emails_hits.extend(emails)
                if v:
                    for email, url in emails:
                        click.echo(f"{RED}Email found: {email} in {url}{ENDC}")
            if post_urls:
                urls.extend(post_urls)
                if v:
                    for url, comment_url in post_urls:
                        click.echo(f"{BLUE}URL found: {url} in {comment_url}{ENDC}")

        for post in posts:
            body = str(post.selftext)
            post_url = "https://www.reddit.com/" + post.permalink
            emails2 = re.findall(email_regex, body)
            emails2 = [(x, post_url) for x in emails2]
            post_urls = re.findall(url_regex, body)
            post_urls = [(x, post_url) for x in post_urls]

            if emails2:
                emails_hits.extend(emails2)
                if v:
                    for email, url in emails2:
                        click.echo(f"{RED}Email found: {email} in {url}{ENDC}")
            if post_urls:
                urls.extend(post_urls)
                if v:
                    for url, post_url in post_urls:
                        click.echo(f"{BLUE}URL found: {url} in {post_url}{ENDC}")

        click.echo(f"{OKGREEN}{username} {RED}emails{ENDC} -> {str(len(emails_hits))} | {RED}urls{ENDC} -> {str(len(urls))}\n\n")

        try:
            if emails_hits:
                with open(f"{username}_emails.csv", "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Email", "Comment URL"])
                    writer.writerows(emails_hits)
            if urls:
                with open(f"{username}_urls.csv", "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["URL", "Comment URL"])
                    writer.writerows(urls)
        except IOError as e:
            click.echo(f"{RED}Error: Failed to write CSV file: {e}{ENDC}")
        except Exception as e:
            click.echo(f"{RED}Unexpected error: {e}{ENDC}")


@click.command()
@click.option("--save", is_flag=True, help="Save user comments/posts in a CSV file")
@click.option("-r", type=click.Path(exists=True), help="Load a file of usernames")
@click.option("-v", is_flag=True, help="Enable verbose mode")
@click.argument("username", default=None, nargs=-1)
def redscan(username, save, r, v):
    if username:
        username = username[0]
    if r:
        try:
            with open(r, "r") as f:
                for line in f:
                    user = line.strip()
                    if user:  # Ensure the line is not empty
                        scanner(save=save, username=user, v=v)
        except IOError as e:
            click.echo(f"{RED}Error: Failed to read file: {e}{ENDC}")
        except Exception as e:
            click.echo(f"{RED}Unexpected error: {e}{ENDC}")
    else:
        if username:
            scanner(save=save, username=username, v=v)
        else:
            click.echo(
                "Error: You must provide a username or a file with usernames using the -r option.")


if __name__ == "__main__":
    redscan()
