
; 6690 is new instruction WAIT instead of 90 NOP
macro padnum [params]
{   times params-1 db "f" ;66h
    db 90h
}
macro AMDPad16
{	virtual
		align 16
		a = $-$$
	end virtual
			;  a+3
	c=(a+3) shr 2	;  ---
			;   4
	repeat c
		padnum (a-%+c)/c
	end repeat
}

macro padnum16zero
{	virtual
		align 16
		a = $ - $$
	end virtual
		db	a dup 0
}

macro padnum16dummy
{	virtual
		align 16
		a = $ - $$
	end virtual
		rb	a
}
