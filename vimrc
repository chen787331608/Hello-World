"vim插件
execute pathogen#infect()
syntax on
filetype plugin indent on

" 新建文件 信息补全
autocmd BufNewFile *.py exec ":call StrictWarn()"

func StrictWarn()
    call setline(1, "#!/usr/bin/env python")
    call append(1, "# -*- coding: utf-8 -*-")
    call append(2, "# Author: chen787331608")
endfunc

" 自动缩进
set autoindent
set cindent
" Tab键的宽度
set tabstop=4
" 统一缩进为4
set softtabstop=4
set shiftwidth=4
" 使用空格代替制表符
set expandtab
" 在行和段开始处使用制表符
set smarttab
" 显示行号
set number
" 高亮显示匹配的括号
set showmatch
" 匹配括号高亮的时间（单位是十分之一秒）
set matchtime=1
"代码补全 
set completeopt=preview,menu
