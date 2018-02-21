import vim
from . import util


# ----------------------------------------------------------------------
def open_opened_list():
    opened_list = []
    with util.P4Connect() as p4:
        opened_list = open_opened_list_impl(p4)
    return opened_list


# ----------------------------------------------------------------------
def open_opened_list_impl(p4):
    opened_depot_file_list = p4.run_opened()

    client_root = p4.run_info()[0]['clientRoot']

    opened = ''
    opened_file_list = []
    for file in opened_depot_file_list:
        file_path = file['depotFile'].replace('//depot', client_root)
        opened_file_list.append(file_path)
        opened += file_path + '[' + file['action'] + ']'
        if file != opened_depot_file_list[-1]:
            opened += '\n'

    # Write to buffer.
    vim.command('enew')

    with util.VimPaste():
        vim.command('normal i' + opened)

    buff_options = vim.current.buffer.options
    buff_options['bufhidden'] = 'hide'
    buff_options['buftype'] = 'nofile'
    buff_options['modifiable'] = False
    buff_options['swapfile'] = False
    buff_options['filetype'] = 'p4'

    # move cursor to head.
    vim.command('normal gg')

    return opened_file_list
