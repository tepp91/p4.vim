import times
import vim
from . import util
from . import diff

# ----------------------------------------------------------------------
display_list = []


# ----------------------------------------------------------------------
def open(path):
    num_rev = 0
    with util.P4Connect() as p4:
        num_rev = __open_impl(path, p4)

    return num_rev


# ----------------------------------------------------------------------
def __open_impl(path, p4):
    global display_list
    display_list.clear()

    depot_file_list = p4.run_filelog('-l', '-i', path)
    if len(depot_file_list) == 0:
        print('Notfound depot file.')
        return

    history = ''
    last_rev = depot_file_list[-1].revisions[-1]
    for depot_file in depot_file_list:
        history += depot_file.depotFile + '\n'
        display_list.append(None)

        for rev in depot_file.revisions:
            display_list.append((depot_file.depotFile, rev.rev))
            history += __make_revision_text(rev)
            if rev != last_rev:
                history += '\n'

    # Write to buffer.
    vim.command('topleft 10new')
    vim.current.window.options['winfixheight'] = True

    with util.VimPaste():
        vim.command('normal i' + history)

    buff_options = vim.current.buffer.options
    buff_options['bufhidden'] = 'hide'
    buff_options['buftype'] = 'nofile'
    buff_options['modifiable'] = False
    buff_options['swapfile'] = False
    buff_options['filetype'] = 'p4'

    # move cursor to head.
    vim.command('normal gg')

    return len(depot_file.revisions)


# ----------------------------------------------------------------------
def __find_depot_file(path, p4):
    file_list = p4.run_filelog('-l', '-i', path)

    if len(file_list) > 0:
        return file_list[0]
    return None


# ----------------------------------------------------------------------
def __make_revision_text(rev):
    desc = rev.desc.rstrip().replace('\n', ' ')
    time_format = '%Y-%m-%d %H:%M:%S'
    time_str = times.format(rev.time, vim.eval('g:p4#timezone'), time_format)
    return '{:4}{:10d}  {}  {:<10}  {}'.format(
        rev.rev, rev.change, time_str, rev.user, desc)


# ----------------------------------------------------------------------
def open_rev(row):
    with util.P4Connect() as p4:
        __open_rev_impl(p4, row)


# ----------------------------------------------------------------------
def __open_rev_impl(p4, row):
    global display_list
    if len(display_list) <= row or display_list[row] is None:
        return

    path, rev = display_list[row]

    tmp_path = util.P4Util.export_to_tmppath(p4, path, rev)
    vim.command('tabnew  ' + tmp_path)
    vim.current.buffer.options['modifiable'] = False
    vim.current.buffer.options['swapfile'] = False


# ----------------------------------------------------------------------
def diff_prev(row):
    with util.P4Connect() as p4:
        __diff_prev_impl(p4, row)


# ----------------------------------------------------------------------
def __diff_prev_impl(p4, row1):
    global display_list
    list_len = len(display_list)
    if list_len <= row1 or display_list[row1] is None:
        return

    row2 = -1
    tmp_row = row1 + 1
    while tmp_row < len(display_list):
        if display_list[tmp_row]:
            row2 = tmp_row
            break
        tmp_row += 1

    if row2 == -1:
        return

    path1, rev1 = display_list[row1]
    path2, rev2 = display_list[row2]

    diff.open(path1, rev1, path2, rev2)
