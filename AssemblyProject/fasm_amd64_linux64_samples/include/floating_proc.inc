; convert rax into decimal ASCII buffer at rdi
; destroy ??
; input:	rax	number, must be < 10000000000000000
;		rdi	33-bytes buffer (32 digits + 1 zero-terminator)
; output:	fill buffer at rdi
; need to include hexa_data.inc

max_digits_to_display	=	16

a=1
c=max_digits_to_display
while c<>0
a=a*10
c=c-1
end while
max_rax			=	a

rax_hex2decimalascii:
	emms
	push	rax
	push	rcx
	mov	rcx,max_rax-1
	cmp	rcx,rax
	jc	rax_dec2ascii_end	; Carry flag is set
	push	rdi
	push	rax
	push	rax
	fild	qword [rsp]
	fbstp	tbyte [rsp]
	movdqu	xmm0,dqword [rsp]
	movdqa	xmm2,dqword [Mask1]
	movdqa	xmm3,dqword [Sum1]
	movdqa	xmm1,xmm0
	psrlq	xmm1,4
	pand	xmm0,xmm2
	pand	xmm1,xmm2
	punpcklbw	xmm0,xmm1
	paddb	xmm0,xmm3
	movdqu	dqword [rsp],xmm0

	mov	al,'0'
	mov	ecx,max_digits_to_display
	lea	rdi,[rsp + max_digits_to_display - 1]
	pushf
	std
	repz scasb
	inc	ecx
;	popf
;	mov	rdi,qword [rsp + 8*2]
;	pushf
	mov	rdi,qword [rsp + 8*3]
	cld
AMDPad16
rax_dec2ascii_L0:
	mov	al,byte [rsp+8 + rcx-1]		; +8 because pushf
	stosb
	loop	rax_dec2ascii_L0
	popf
	mov	byte [rdi],cl	; make 0-terminated string
	add	rsp,8*3		; this clear carry flag
rax_dec2ascii_end:
	pop	rcx
	pop	rax

	ret
