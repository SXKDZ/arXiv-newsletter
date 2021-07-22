import os
import yaml
import arxiv
import smtplib, ssl

from pathlib import Path
from datetime import date


today = date.today()


def build_query(domains, keyword):
    query = '('
    for i, domain in enumerate(domains):
        query += f'cat:{domain}'
        if i != len(domains) - 1:
            query += ' OR '
    query += f') AND ({keyword})'
    return query


def build_content(query, query_config):
    domains = query['domains']
    keywords = query['keywords']
    total_mail = len(query['keywords'])

    subject_placeholder = 'arXiv newsletter ' + str(today) + ' {index}/' + str(total_mail)
    content_placeholder = '\n' + '*' * 35 + '\n ' + subject_placeholder + ' \n' + '*' * 35 + '\n'
    entry_placeholder = '{index}. {title}\n{authors}\nPublished at: {publish}\nUpdated at: {update}\nPrimary Category: {primary_category}\nCategories: {categories}\n{notes}\n{link}\n\nAbstract:\n{abstract}\n'

    messages = []

    for i, keyword in enumerate(keywords):
        query = build_query(domains, keyword)
        print(query)
        while True:
            try:
                results = arxiv.Search(query=query, **query_config)
                break
            except:
                pass
        entries = ''
        for j, result in enumerate(results.results()):
            entry = entry_placeholder.format(
                index=j + 1,
                title=result.title,
                authors=', '.join([author.name for author in result.authors]),
                publish=result.published,
                update=result.updated,
                primary_category=result.primary_category,
                categories=', '.join(result.categories),
                link='\n'.join([link.href for link in result.links]),
                abstract=result.summary,
                notes=f'Comments: {result.comment}\n' if result.comment is not None else ''
            )
            entries += entry + '\n'
        subject = subject_placeholder.format(index=i + 1)
        content = content_placeholder.format(index=i + 1)
        content += '\nQuery: ' + keyword + '\n\n' + entries
        # content = textwrap.wrap(content, width=80, replace_whitespace=False)
        # content = '\n'.join(content)
        messages.append((subject, content))

    return messages


def send_mail(config):
    mail_config = config['mail']
    smtp_server = mail_config['server']
    port = mail_config['port']
    sender = mail_config['user']
    password = mail_config['password']

    query_config = config['query_config']
    query_config['sort_by'] = arxiv.SortCriterion._member_map_[query_config['sort_by']]
    query_config['sort_order'] = arxiv.SortOrder._member_map_[query_config['sort_order']]

    context = ssl.create_default_context()
    comments = '\nPowered by arXiv-newsletter \nhttps://github.com/SXKDZ/arXiv-newsletter\n'
    
    for recipient in config['recipients']:
        messages = build_content(query=recipient, query_config=query_config)
        for i, each_message in enumerate(messages):
            subject, content = each_message

            header = f'To: {recipient["recipient"]}\nFrom: arXiv-bot <{sender}>\nSubject: {subject}\n'
            message = header + content + comments
            print(header)
            with open(f'{today}/{recipient["recipient"]}_{i + 1}.txt', 'w+') as f:
                f.write(message)
            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender, password)
                    server.sendmail(sender, recipient['recipient'], message.encode('ascii', 'ignore').decode('ascii'))
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
