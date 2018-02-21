import os
import vim
from P4 import P4


def get_tmp_path(path, rev_number):
    tmp_dir = os.path.dirname(vim.eval('tempname()'))
    tmp_dir = os.path.join(tmp_dir, 'p4vim')
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    file_name, ext = os.path.splitext(os.path.basename(path))
    tmp_name = file_name + '@' + str(rev_number) + ext

    return os.path.join(tmp_dir, tmp_name)


class P4Connect:
    def __enter__(self):
        self.p4 = P4()
        self.p4.connect()
        return self.p4

    def __exit__(self, exp_type, value, traceback):
        self.p4.disconnect()
        return True


class VimPaste:
    def __enter__(self):
        vim.options['paste'] = True

    def __exit__(self, type, value, traceback):
        vim.options['paste'] = False


class P4Util:
    @staticmethod
    def get_rev_content(p4, path, rev_number):
        content_info = p4.run_print(path + '#' + str(rev_number))

        if not content_info:
            return ''

        return content_info[1]

    @staticmethod
    def export_to_tmppath(p4, path, rev_number):
        tmp_path = get_tmp_path(path, rev_number)
        return P4Util.export(p4, path, rev_number, tmp_path)

    @staticmethod
    def export(p4, path, rev_number, output_path):
        content = P4Util.get_rev_content(p4, path, rev_number)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return output_path
