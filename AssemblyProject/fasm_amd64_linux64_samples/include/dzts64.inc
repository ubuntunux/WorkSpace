
include	'linux_def.inc'		; OS specific definitions
include	'unistd64.inc'		; syscalls' numbers list

wzts_std:
; what it does:	writes zero-terminated string to STDOUT (standard output)
; input:	RAX points to the 0-terminated string
; output:	clear carry flag if success
;		set carry flag if error
; destroy:	nothing, but maybe syscall destroy some regs ?

; prologue
	stc			; assume we fail
	pushf
	push	rax
	push	rcx
	push	rdx
	push	rsi
	push	rdi

; find size of string without 0-terminator
	lea	rdi,[rax]	; get string address
	lea	rsi,[rax]
	or	ecx,-1		; ecx=-1
	xor	eax,eax
	lea	edx,[ecx-1]	; edx=-2
	cld
	repnz scasb
	sub	edx,ecx		; string size
	jz	wzts_std_done	; string has size=0, begins with 0
; rsi offset of string, rdx string size
; write string to STDOUT
	mov	edi,STDOUT
	mov	eax,sys_write
	syscall
wzts_std_done:
	or	rax,rax		; check if rax<0 (error)
	setns	al		; make AL=1 if syscall success, else AL=0
	xor	byte [rsp+8*5],al	; clear Carry Flag in stack
				; or leave it set (bit 0. of rflags)

; epilogue
	pop	rdi
	pop	rsi
	pop	rdx
	pop	rcx
	pop	rax
	popf

	ret
