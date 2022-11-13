from datetime import datetime


def get_release_date(release_str):
    words = release_str.split()
    return datetime.strptime('{}/{}/{}'.format(words[3].zfill(2), words[4], words[5].zfill(4)), "%d/%B/%Y")

