" plugin for control perforce
" Maintainer: Tepp <tepp91@outlook.com>
" License: MIT License

let s:save_cpo = &cpo
set cpo&vim

" Global options {{{

let g:p4#timezone
    \ = get(g:, 'p4#timezone', 'Asia/Tokyo')

let g:p4#history_format
    \ = get(g:, 'p4#history_format', '{rev:4}{cl:10d}  {time}  {user:<10} {desc}')

" }}}

" Command line wrapper {{{

func! p4#edit()
	echo system('p4 edit '.expand('%:p'))
	if v:shell_error == 0
		set noreadonly
	endif
endfunc

func! p4#revert()
	echo system('p4 revert '.expand('%:p'))
	e!
endfunc

func! p4#revert_all()
	echo system('p4 revert //...')
	e!
endfunc

func! p4#revert_unchanged()
	echo system('p4 revert -a '.expand('%:p'))
endfunc

func! p4#add()
	echo system('p4 add '.expand('%:p'))
endfunc

func! p4#timelapse()
	execute  '!start p4v -cmd "annotate ' . expand('%:p') . '"'
endfunc

" }}}

" Import python code {{{
py3 << PY3END
import sys
import vim
this_path = vim.eval('expand("<sfile>:p:h")')
if not(this_path in sys.path):
	sys.path.insert(0, this_path)

from p4 import history
from p4 import diff
from p4 import workspace
PY3END
" }}}

" Function {{{

func! p4#history_open()
	py3 history.open(vim.eval('expand("%:p")'))

	nnoremap <silent><buffer> q <C-W>c
	nnoremap <silent><buffer> <CR> :call p4#history_open_rev(line('.')-1)<CR>
	nnoremap <silent><buffer> dp :call p4#history_diff_prev(line('.')-1)<CR>
endfunc

func! p4#history_open_rev(row)
	quit
	py3 history.open_rev(int(vim.eval('a:row')))
endfunc

func! p4#history_diff_prev(row)
	quit
	py3 history.diff_prev(int(vim.eval('a:row')))
endfunc

func! p4#open_opened()
	let b:p4_opened_file = py3eval("workspace.open_opened_list()")

	nnoremap <silent><buffer> q <C-W>c
	nnoremap <silent><buffer> <CR> :call p4#open_file(b:p4_opened_file[line('.')-1])<CR>
endfunc

func! p4#open_file(filepath)
	execute 'e '.a:filepath
endfunc

func! p4#diff()
	py3 diff.open_head(vim.eval('expand("%:p")'))
endfunc

func! p4#enable_auto_edit()
	augroup p4_auto_edit
		autocmd!
		autocmd FileChangedRO * call p4#edit()
	augroup END
endfunc


" }}}


let &cpo = s:save_cpo
unlet s:save_cpo

" vim: foldmethod=marker
