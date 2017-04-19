
include	'linux_def.inc'		; OS specific definitions
include	'unistd64.inc'		; syscalls' numbers list

w1ch_std:
; what it does:	writes 1 char to STDOUT (standard output)
; input:	RAX points to the char
; output:	clear carry flag if success
;		set carry flag if error
; destroy:	nothing, but maybe syscall destroy some regs ?

; prologue
	stc			; assume we fail
	pushf
	push	rax
	push	rdx
	push	rsi
	push	rdi

	mov	edx,1		; string size
	lea	rsi,[rax]	; string address
	mov	edi,STDOUT
	mov	eax,sys_write
	syscall
	or	rax,rax		; check if rax<0 (error)
	setns	al		; make AL=1 if syscall success, else AL=0
	xor	byte [rsp+8*4],al	; clear Carry Flag in stack
				; or leave it set (bit 0. of rflags)

; epilogue
	pop	rdi
	pop	rsi
	pop	rdx
	pop	rax
	popf

	ret
