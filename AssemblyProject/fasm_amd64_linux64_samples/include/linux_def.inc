
NULL			=	0

TRUE			=	1
FALSE			=	0

STDIN			=	0
STDOUT			=	1
STDERR			=	2

EOL			=	0

SEEK_SET		=	0
SEEK_CUR		=	1
SEEK_END		=	2

O_RDONLY		=	0
O_WRONLY		=	1
O_RDWR			=	2

O_CREAT			=	0100o	; octal, = 40h
O_EXCL			=	0200o
O_NOCTTY		=	0400o
O_TRUNC			=	1000o
O_APPEND		=	2000o
O_NONBLOCK		=	4000o
O_NONDELAY		=	O_NONBLOCK
O_SYNC			=	10000o
O_ASYNC			=	20000o
O_DIRECT		=	40000o
O_LARGEFILE		=	100000o
O_DIRECTORY		=	200000o
O_NOFOLLOW		=	400000o

PROT_READ		=	1
PROT_WRITE		=	2
PROT_EXEC		=	4
PROT_NONE		=	0		; page can not be accessed
PROT_SEM		=	8
PROT_GROWSDOWN		=	01000000h	; mprotect flag: extend change to start of growsdown vma
PROT_GROWSUP		=	02000000h	; mprotect flag: extend change to end of growsup vma

MAP_SHARED		=	01h		; Share changes
MAP_PRIVATE		=	02h		; Changes are private
MAP_TYPE		=	0Fh		; Mask for type of mapping
MAP_FIXED		=	10h		; Interpret addr exactly
MAP_ANONYMOUS		=	20h		; don't use a file
MAP_32BIT		=	40h		; only give out 32bit addresses

MAP_GROWSDOWN		=	0100h		; stack-like segment
MAP_DENYWRITE		=	0800h		; ETXTBSY
MAP_EXECUTABLE		=	1000h		; mark it as an executable
MAP_LOCKED		=	2000h		; pages are locked
MAP_NORESERVE		=	4000h		; don't check for reservations
MAP_POPULATE		=	8000h		; populate (prefault) pagetables
MAP_NONBLOCK		=	10000h		; do not block on IO

MS_ASYNC		=	1		; sync memory asynchronously
MS_INVALIDATE		=	2		; invalidate the caches
MS_SYNC			=	4		; synchronous memory sync

MCL_CURRENT		=	1		; lock all current mappings
MCL_FUTURE		=	2		; lock all future mappings

MADV_NORMAL		=	0		; default page-in behavior
MADV_RANDOM		=	1		; page-in minimum required
MADV_SEQUENTIAL		=	2		; read-ahead aggressively
MADV_WILLNEED		=	3		; pre-fault pages
MADV_DONTNEED		=	4		; discard these pages

MAP_ANON		=	MAP_ANONYMOUS
MAP_FILE		=	0


; /usr/src/linux/include/linux/ptrace.h
PTRACE_TRACEME		=	0
PTRACE_PEEKTEXT		=	1
PTRACE_PEEKDATA		=	2
PTRACE_PEEKUSR		=	3
PTRACE_POKETEXT		=	4
PTRACE_POKEDATA		=	5
PTRACE_POKEUSR		=	6
PTRACE_CONT		=	7
PTRACE_KILL		=	8
PTRACE_SINGLESTEP	=	9
PTRACE_ATTACH		=	10h
PTRACE_DETACH		=	11h
PTRACE_SYSCALL		=	24

; /usr/src/linux/include/asm-x86_64/ptrace.h
;FRAME_OFFSETS
;R15 0
;R14 8
;R13 16
;R12 24
;RBP 32
;RBX 40
; arguments: interrupts/non tracing syscalls only save upto here
;R11 48
;R10 56	
;R9 64
;R8 72
;RAX 80
;RCX 88
;RDX 96
;RSI 104
;RDI 112
;ORIG_RAX 120	; = ERROR
; cpu exception frame or undefined in case of fast syscall.
;RIP 128
;CS 136
;EFLAGS 144
;RSP 152
;SS 160
;ARGOFFSET R11
; top of stack page
;FRAME_SIZE 168
;struct pt_regs {
;	unsigned long r15;
;	unsigned long r14;
;	unsigned long r13;
;	unsigned long r12;
;	unsigned long rbp;
;	unsigned long rbx;
; arguments: non interrupts/non tracing syscalls only save upto here
; 	unsigned long r11;
;	unsigned long r10;	
;	unsigned long r9;
;	unsigned long r8;
;	unsigned long rax;
;	unsigned long rcx;
;	unsigned long rdx;
;	unsigned long rsi;
;	unsigned long rdi;
;	unsigned long orig_rax;
; end of arguments
; cpu exception frame or undefined
;	unsigned long rip;
;	unsigned long cs;
;	unsigned long eflags; 
;	unsigned long rsp; 
;	unsigned long ss;
; top of stack page

PTRACE_GETREGS		=	12
PTRACE_SETREGS		=	13
PTRACE_GETFPREGS	=	14
PTRACE_SETFPREGS	=	15
PTRACE_GETFPXREGS	=	18
PTRACE_SETFPXREGS	=	19
PTRACE_OLDSETOPTIONS	=	21

; only useful for access 32bit programs
PTRACE_GET_THREAD_AREA	=	25
PTRACE_SET_THREAD_AREA	=	26

PTRACE_ARCH_PRCTL	=	30	; arch_prctl for child

EF_CF			= 00000001h
EF_PF			= 00000004h
EF_AF			= 00000010h
EF_ZF			= 00000040h
EF_SF			= 00000080h
EF_TF			= 00000100h
EF_IE			= 00000200h
EF_DF			= 00000400h
EF_OF			= 00000800h
EF_IOPL			= 00003000h
EF_IOPL_RING0		= 00000000h
EF_IOPL_RING1		= 00001000h
EF_IOPL_RING2		= 00002000h
EF_NT			= 00004000h	; nested task
EF_RF			= 00010000h	; resume
EF_VM			= 00020000h	; virtual mode
EF_AC			= 00040000h	; alignment
EF_VIF			= 00080000h	; virtual interrupt
EF_VIP			= 00100000h	; virtual interrupt pending
EF_ID			= 00200000h	; id


; /usr/src/linux/include/asm-x86_64/signal.h
SIGHUP			=	 1
SIGINT			=	 2
SIGQUIT			=	 3
SIGILL			=	 4
SIGTRAP			=	 5
SIGABRT			=	 6
SIGIOT			=	 6
SIGBUS			=	 7
SIGFPE			=	 8
SIGKILL			=	 9
SIGUSR1			=	10
SIGSEGV			=	11
SIGUSR2			=	12
SIGPIPE			=	13
SIGALRM			=	14
SIGTERM			=	15
SIGSTKFLT		=	16
SIGCHLD			=	17
SIGCONT			=	18
SIGSTOP			=	19
SIGTSTP			=	20
SIGTTIN			=	21
SIGTTOU			=	22
SIGURG			=	23
SIGXCPU			=	24
SIGXFSZ			=	25
SIGVTALRM		=	26
SIGPROF			=	27
SIGWINCH		=	28
SIGIO			=	29
SIGPOLL			=	SIGIO
SIGLOST			=	29
SIGPWR			=	30
SIGSYS			=	31
SIGUNUSED		=	31
SIGRTMIN		=	32

; /usr/src/linux/include/linux/wait.h
WNOHANG			=	00000001h
WUNTRACED		=	00000002h
WSTOPPED		=	WUNTRACED
WEXITED			=	00000004h
WCONTINUED		=	00000008h
WNOWAIT			=	01000000h	; Don't reap, just poll status.
__WNOTHREAD		=	20000000h	; Don't wait on children of other threads in this group
__WALL			=	40000000h	; Wait on all children, regardless of type
__WCLONE		=	80000000h	; Wait only on non-SIGCHLD children

; /usr/include/bits/waitstatus.h
;
;# error "Never include <bits/waitstatus.h> directly; use <sys/wait.h> instead."
; If WIFEXITED(STATUS), the low-order 8 bits of the status.
; #define	__WEXITSTATUS(status)	(((status) & 0xff00) >> 8)
;
; If WIFSIGNALED(STATUS), the terminating signal.
; #define	__WTERMSIG(status)	((status) & 0x7f)
;
; If WIFSTOPPED(STATUS), the signal that stopped the child.
; #define	__WSTOPSIG(status)	__WEXITSTATUS(status)
;
; Nonzero if STATUS indicates normal termination.
; #define	__WIFEXITED(status)	(__WTERMSIG(status) == 0)
;
; Nonzero if STATUS indicates termination by a signal.
; #define __WIFSIGNALED(status) \
;   (((signed char) (((status) & 0x7f) + 1) >> 1) > 0)
;
; Nonzero if STATUS indicates the child is stopped.
; #define	__WIFSTOPPED(status)	(((status) & 0xff) == 0x7f)
WIFSTOPPED		=	7Fh
; Nonzero if STATUS indicates the child continued after a stop.  We only
;   define this if <bits/waitflags.h> provides the WCONTINUED flag bit.
; # define __WIFCONTINUED(status)	((status) == __W_CONTINUED)
;
; Nonzero if STATUS indicates the child dumped core.
; #define	__WCOREDUMP(status)	((status) & __WCOREFLAG)
;
; Macros for constructing status values.
; #define	__W_EXITCODE(ret, sig)	((ret) << 8 | (sig))
; #define	__W_STOPCODE(sig)	((sig) << 8 | 0x7f)
; #define __W_CONTINUED		0xffff
; #define	__WCOREFLAG		0x80

; /usr/include/asm-x68_64/user.h
; This matches the 64bit FXSAVE format as defined by AMD. It is the same
; as the 32bit format defined by Intel, except that the selector:offset pairs
; for data and eip are replaced with flat 64bit pointers.
; struct user_i387_struct {
;	unsigned short	cwd;
;	unsigned short	swd;
;	unsigned short	twd; Note this is not the same as the 32bit/x87/FSAVE twd - Tag "Byte" - It is first byte only, second byte is dummy.
;	unsigned short	fop;
;	u64	rip;
;	u64	rdp;
;	u32	mxcsr;
;	u32	mxcsr_mask;
;	u32	st_space[32]; 8*16 bytes for each FP-reg = 128 bytes
;	u32	xmm_space[64]; 16*16 bytes for each XMM-reg = 256 bytes
;	u32	padding[24];
;
;struct user_regs_struct {
;	unsigned long r15,r14,r13,r12,rbp,rbx,r11,r10;
;	unsigned long r9,r8,rax,rcx,rdx,rsi,rdi,orig_rax;
;	unsigned long rip,cs,eflags;
;	unsigned long rsp,ss;
;	unsigned long fs_base, gs_base;
;	unsigned long ds,es,fs,gs; 
;
; When the kernel dumps core, it starts by dumping the user struct -
; this will be used by gdb to figure out where the data and stack segments
; are within the file, and what virtual addresses to use. */
; struct user{
; We start with the registers, to mimic the way that "memory" is returned
; from the ptrace(3,...) function.
; struct user_regs_struct regs	; Where the registers are actually stored
; ptrace does not yet supply these.  Someday....
; int u_fpvalid			;True if math co-processor being used.
;				; for this mess. Not yet used.
; struct user_i387_struct i387	; Math Co-processor registers.
; The rest of this junk is to help gdb figure out what goes where
; unsigned long int u_tsize	; Text segment size (pages).
; unsigned long int u_dsize	; Data segment size (pages).
; unsigned long int u_ssize	; Stack segment size (pages).
; unsigned long start_code;     ; Starting virtual address of text.
; unsigned long start_stack;	; Starting virtual address of stack area.
;				; This is actually the bottom of the stack,
;				; the top of the stack is always found in the
;				; esp register.
; long int signal;     		; Signal that caused the core dump.
; int reserved;			; No longer used
; struct user_pt_regs * u_ar0;	; Used by gdb to help find the values for
;				; the registers.
; struct user_i387_struct* u_fpstate	; Math Co-processor pointer.
; unsigned long magic;		; To uniquely identify a core file
; char u_comm[32];		; User command that was responsible
; unsigned long u_debugreg[8]
