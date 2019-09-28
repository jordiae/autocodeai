import os, sys
from datetime import datetime
import ntpath
import random
random.seed(1)

PGA_PATH = os.path.join('..', '..', 'bin', 'pga')
SIVA_PATH = os.path.join('..', '..', 'bin', 'siva')
ENRY_PATH = os.path.join('..', '..', 'bin', 'enry')
CRAWLED_URLS_PATH = os.path.join('..', '..', 'data', 'crawled_urls')
URLS_FILE = 'urls-2019-09-24-21:07:51.txt'
SCRAPED_REPOS_PATH = os.path.join('..', '..', 'data', 'scraped_repos')
CORPUS_PATH = os.path.join('..', '..', 'data', 'corpora')


def write_set(set_files, set_name, corpus_path):
    with open(os.path.join(corpus_path, set_name +'.txt'), 'w') as corpus:
        for filepath in set_files:
            filename, file_extension = os.path.splitext(ntpath.basename(filepath))
            content = ' == ' + filename + ' ' + file_extension + ' ==\n'
            print('Writing', filepath)
            content += open(filepath, 'r').read()
            if file_extension in ['html', 'htm', 'xhtml', 'HTML', 'HTM', 'XHTML']:
                new_content = []
                for line in content.splitlines():
                    for token in line.split():
                        try:
                            if token.startswith('src="data:image/png'):
                                continue
                            else:
                                new_content.append(line+'\n')
                        except BaseException as e:
                            continue
                content = ''.join(new_content)
            content = ''.join([s for s in content.splitlines(True) if s.strip()])  # remove whitespace/tab only lines
            content = os.linesep.join([s for s in content.splitlines() if s])  # remove empty lines
            content += '\n\n'
            corpus.write(content)


def write_corpus(corpus_files, corpus_path, corpus_name, stats, ndocs, ndevtest):
    os.system('mkdir -p ' + corpus_path)
    with open(os.path.join(corpus_path, 'stats.log'), 'w') as f:
        f.writelines(stats)
    random.shuffle(corpus_files)
    train, dev, test = corpus_files[0:-ndevtest*2], corpus_files[-ndevtest*2:-ndevtest], corpus_files[-ndevtest:]
    write_set(train, 'train', corpus_path)
    write_set(dev, 'valid', corpus_path)
    write_set(test, 'test', corpus_path)


def main():
    enry = os.path.realpath(ENRY_PATH)
    urls = open(os.path.join(CRAWLED_URLS_PATH, URLS_FILE), 'r').readlines()
    corpus_path = os.path.realpath(os.path.join(CORPUS_PATH, URLS_FILE[:-4]))
    try:
        os.mkdir(SCRAPED_REPOS_PATH)
    except BaseException as e:
        print(str(e))
    os.chdir(SCRAPED_REPOS_PATH)
    try:
        os.mkdir(os.path.join(SCRAPED_REPOS_PATH, URLS_FILE[:-4]))
    except BaseException as e:
        print(str(e))
    os.chdir(os.path.join(SCRAPED_REPOS_PATH, URLS_FILE[:-4]))
    for url in urls:
        continue
        os.system('git clone ' + url)
        dir_name = []
    corpus_files = []
    stats = {}
    for dir_name, subdir_list, file_list in os.walk('.'):
        # print('Found directory: %s' % dir_name)
        for fname in file_list:
            # print('\t%s' % fname)
            output_lines = os.popen(enry + ' ' + os.path.join(dir_name, fname)).readlines()
            for line in output_lines:
                if line.split()[0] == 'language:':
                    language = None
                    try:
                        language = line.split()[1]
                        if language in ['Pickle', 'SVG', 'Text', 'INI', 'Markdown', 'CSV', 'Ignore', 'reStructuredText', 'Jupyter']:
                            break
                            #print(output_lines, dir_name)
                            #input()
                        #print('\t%s' % fname, 'is source code: ', language)
                        corpus_files.append(os.path.realpath(os.path.join(dir_name, fname)))
                        if language in stats:
                            stats[language] += 1
                        else:
                            stats[language] = 1
                    except BaseException as e:
                        pass
                        # print('\t%s' % fname, 'is NOT source code: ')
                        # print(output_lines)
                        # input()
                    break
    print(stats)
    stats_lines = []
    total = 0
    for key, value in stats.items():
        total += value
    for key, value in stats.items():
        stats_lines.append(key + ' ' + str(value) + ' ' + str(100*value/total)[:6] + '%\n')
    print(len(corpus_files), corpus_files[50])
    write_corpus(corpus_files=corpus_files, corpus_path=corpus_path, corpus_name=URLS_FILE[:-4], stats=stats_lines, ndocs=total, ndevtest=50)


if __name__ == '__main__':
    main()
