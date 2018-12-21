set tabstop=8                   "A tab is 8 spaces
set expandtab                   "Always uses spaces instead of tabs
set softtabstop=4               "Insert 4 spaces when tab is pressed
set shiftwidth=4                "An indent is 4 spaces
set shiftround                  "Round indent to nearest shiftwidth multiple
set autoindent    "turns it on
set smartindent   "does the right thing (mostly) in programs
set cindent       "stricter rules for C programs
set tenc=utf-8
set incsearch 		"키워드 입력시 점진적 검색
syntax on 		"구문강조 사용
filetype indent on 	"파일 종류에 따른 구문강조
set nowrapscan 		"검색할 때 문서의 끝에서 처음으로 안돌아감
set ruler 		"화면 우측 하단에 현재 커서의 위치(줄,칸) 표
set number 		"행번호 표시, set nu 도 가능
set hlsearch 		"검색어 강조, set hls 도 가능
set ignorecase 		"검색시 대소문자 무시, set ic 도 가능
set backspace=eol,start,indent "줄의 끝, 시작, 들여쓰기에서 백스페이스시 이전줄로
set history=1000 		"vi 편집기록 기억갯수 .viminfo에 기록
