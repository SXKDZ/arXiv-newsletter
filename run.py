import os
import yaml
import arxiv
import smtplib, ssl

from arxiv import SortCriterion, SortOrder
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

today = date.today()


def build_query(domains, keyword):
    query = '('
    for i, domain in enumerate(domains):
        query += f'cat:{domain}'
        if i != len(domains) - 1:
            query += ' OR '
    query += f') AND ({keyword})'
    return query


def build_content(config):
    domains = config['domains']
    keywords = config['keywords']
    query_config = config['query_config']

    messages = []

    env = Environment(
        loader=FileSystemLoader('templates/'),
        autoescape=select_autoescape()
    )
    template = env.get_template("template.html")

    total_mail = len(config['keywords'])
    subject_placeholder = 'arXiv newsletter ' + str(today) + ' {index}/' + str(total_mail)

    for i, keyword in enumerate(keywords):
        query = build_query(domains, keyword)
        results = arxiv.Search(
            query=query,
            sort_by=SortCriterion[query_config['sort_by']],
            sort_order=SortOrder[query_config['sort_order']],
            max_results=query_config['max_results'])

        newsletter = {
            'index': i + 1,
            'today': today.strftime('%B %d, %Y'),
            'query': keyword,
            'news': []
        }
        for result in results.results():
            # print(result.entry_id)
            newsletter['news'].append({
                'arxiv_id': result.entry_id[21:],
                'title': result.title,
                'authors': ', '.join([author.name for author in result.authors]),
                'published_at': result.published,
                'updated_at': result.updated,
                'categories': result.categories,
                'comments': result.comment,
                'abs': result.summary,
                'doi': f'http://dx.doi.org/{result.doi}' if result.doi else None,
                'urls': result.links[1:] if result.doi is not None else result.links,
            })
        subject = subject_placeholder.format(index=i + 1)
        content = template.render(**newsletter)
        messages.append((subject, content))

    return messages


def send_mail(config):
    mail_config = config['mail']
    smtp_server = mail_config['server']
    port = mail_config['port']
    sender = mail_config['user']
    password = mail_config['password']
    context = ssl.create_default_context()

    messages = build_content(config)
    for recipient in mail_config['recipient']:
        for i, each_message in enumerate(messages):
            subject, content = each_message

            message = MIMEMultipart('alternative')
            message['subject'] = subject
            message['To'] = recipient
            message['From'] = f'arXiv-bot <{sender}>'

            body = MIMEText(content, 'html')
            message.attach(body)

            print(subject)
            with open(f'{today}/{i + 1}.txt', 'w+') as f:
                f.write(message.as_string())
            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender, password)
                    server.sendmail(sender, recipient, message.as_string())
            except smtplib.SMTPDataError as e:
                print(e.smtp_error)
                print()


def main():
    os.chdir(Path(__file__).parent.absolute())

    try:
        os.mkdir(f'{today}')
    except OSError:
        pass

    with open('config.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    send_mail(config)


if __name__ == '__main__':
    main()
