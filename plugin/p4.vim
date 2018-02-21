"=============================================================================
" File: p4.vim
" Author: Tepp <tepp91@outlook.com>
" License: MIT License
"=============================================================================

let s:save_cpo = &cpo
set cpo&vim

com! P4e call p4#edit()
com! P4r call p4#revert()
com! P4ra call p4#revert_all()
com! P4add call p4#add()
com! P4tl call p4#timelapse()
com! P4unchanged call p4#revert_unchanged()
com! P4h call p4#history_open()
com! P4opened call p4#open_opened()
com! P4diff call p4#diff()

let &cpo = s:save_cpo
unlet s:save_cpo

let g:p4_loaded = 1
