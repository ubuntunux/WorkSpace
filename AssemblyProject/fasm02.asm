format ELF64 executable 3

segment readable executable

entry main

include 'io.inc'

main:
    lea rdi, [msg]
    call print
    lea rdi, [msg2]
    call print
    xor rdi, rdi
    mov rax, 60
    syscall
    
segment readable writable

msg db 'Hello World!', 10, 0
msg2 db 'This is my other string.', 10, 0
