; convert rax into ASCII buffer at rdi
; destroy xmm0-xmm5
; input:	rax	number
;		rdi	16-bytes buffer
; output:	fill buffer at rdi
hexa64_rax:
	push	rax
	bswap	rax
	movdqa	xmm3,dqword [Sum1]
	movdqa	xmm4,dqword [Comp1]
	movdqa	xmm2,dqword [Mask1]
	movdqa	xmm5,dqword [Num1]
	push	rax
	movdqu	xmm0,[rsp]
	pop	rax
	movdqa	xmm1,xmm0
	psrlq	xmm0,4
	pand	xmm0,xmm2
	pand	xmm1,xmm2
	punpcklbw	xmm0,xmm1
	movdqa	xmm1,xmm0
	pcmpgtb	xmm0,xmm4
	pand	xmm0,xmm5
	paddb	xmm1,xmm3
	paddb	xmm1,xmm0
	movdqu	dqword [rdi],xmm1
	pop	rax
	ret
