import vim
from . import util


# ----------------------------------------------------------------------
def open(path1, rev1, path2, rev2):
    with util.P4Connect() as p4:
        __open_impl(p4, path1, rev1, path2, rev2)


# ----------------------------------------------------------------------
def __open_impl(p4, path1, rev1, path2, rev2):
    path1 = util.P4Util.export_to_tmppath(p4, path1, rev1)
    path2 = util.P4Util.export_to_tmppath(p4, path2, rev2)

    vim.command('tabnew ' + path1)
    vim.command('diffthis')
    vim.current.buffer.options['modifiable'] = False
    vim.current.buffer.options['swapfile'] = False

    vim.command('vnew ' + path2)
    vim.command('diffthis')
    vim.current.buffer.options['modifiable'] = False
    vim.current.buffer.options['swapfile'] = False

    vim.command('normal gg')


# ----------------------------------------------------------------------
def open_head(path):
    with util.P4Connect() as p4:
        __open_head_impl(p4, path)


# ----------------------------------------------------------------------
def __open_head_impl(p4, path):
    have_info_list = p4.run_have(path)
    if len(have_info_list) == 0:
        return

    have_info = have_info_list[0]
    head_rev = int(have_info['haveRev'])

    head_path = util.P4Util.export_to_tmppath(p4, path, head_rev)

    vim.command('tabnew ' + path)
    vim.command('diffthis')

    vim.command('vnew ' + head_path)
    vim.command('diffthis')
    vim.current.buffer.options['modifiable'] = False
    vim.current.buffer.options['swapfile'] = False

    vim.command('normal gg')
