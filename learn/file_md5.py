import hashlib

def diff_md5(file1,file2):
    def chick_md5(file):
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                content = f.read(8192)
                if content:
                    md5.update(content)
                else:
                    break
        return md5.hexdigest()
    return chick_md5(file1) == chick_md5(file2)



print(diff_md5('/Users/xxxx1/Desktop/1/ui/Settings.class','/Users/xxxx1/Desktop/com/ui/Settings.class'))