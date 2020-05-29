import sys
import os


def traverse(f):
    oldgit = 'http://gitlab.mogujie.org'
    newgit = 'http://wxgitlab.mogujie.org'

    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if not os.path.isdir(tmp_path):
            if f1 == 'config' and tmp_path.index('.git/config') > 0:
                file_data = ""
                with open(tmp_path, "r", encoding="utf-8") as f1:
                    for line in f1:
                        if oldgit in line:
                            line = line.replace(oldgit,newgit)
                        file_data += line
                with open(tmp_path,"w",encoding="utf-8") as f1:
                    f1.write(file_data)
                print('文件: %s'%tmp_path)
        else:
            # print('文件夹：%s'%tmp_path)
            traverse(tmp_path)

# path = '/Users/xxxx1/IdeaProjects/wx1'
# traverse(path)

if __name__ == '__main__':
    traverse(sys.argv[1])