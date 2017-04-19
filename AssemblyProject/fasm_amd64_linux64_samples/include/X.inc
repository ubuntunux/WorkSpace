; /usr/X11R6/include/X11/X.h

; error codes
;
Success			=	  0	; everything's okay
BadRequest		=	  1	; bad request code
BadValue		=	  2	; int parameter out of range
BadWindow		=	  3	; parameter not a Window
BadPixmap		=	  4	; parameter not a Pixmap
BadAtom			=	  5	; parameter not an Atom
BadCursor		=	  6	; parameter not a Cursor
BadFont			=	  7	; parameter not a Font
BadMatch		=	  8	; parameter mismatch
BadDrawable		=	  9	; parameter not a Pixmap or Window
BadAccess		=	 10	; depending on context:
					; - key/button already grabbed
					; - attempt to free an illegal cmap
					;   entry
					; - attempt to store into a read-only
					;   color map entry
					; - attempt to modify the access control
					;   list from other than the local host
BadAlloc		=	 11	; insufficient resources
BadColor		=	 12	; no such colormap
BadGC			=	 13	; parameter not a GC
BadIDChoice		=	 14	; choice not in range or already used
BadName			=	 15	; font or color name doesn't exist
BadLength		=	 16	; Request length incorrect
BadImplementation	=	 17	; server is defective
FirstExtensionError	=	128
LastExtensionError	=	255

; reserved resource and constant definitions
;
None			=	0	; universal null resource or null atom
ParentRelative		=	1	; background pixmap in CreateWindow
					; and ChangeWindowAttributes
CopyFromParent		=	0	; border pixmap in CreateWindow
					; and ChangeWindowAttributes
					; special VisualID and special window
					; class passed to CreateWindow
PointerWindow		=	0	; destination window in SendEvent
InputFocus		=	1	; destination window in SendEvent
PointerRoot		=	1	; focus window in SetInputFocus
AnyPropertyType		=	0	; special Atom, passed to GetProperty
AnyKey			=	0	; special Key Code, passed to GrabKey
AnyButton		=	0	; special Button Code, passed to GrabButton
AllTemporary		=	0	; special Resource ID passed to KillClient
CurrentTime		=	0	; special Time
NoSymbol		=	0	; special KeySym


; WINDOW DEFINITIONS
;
; Window classes used by CreateWindow
; Note that CopyFromParent is already defined as 0 above
;
InputOutput		=	1
InputOnly		=	2
;
; Window attributes for CreateWindow and ChangeWindowAttributes
;
CWBackPixmap		=	1 shl 0
CWBackPixel		=	1 shl 1
CWBorderPixmap		=	1 shl 2
CWBorderPixel           =	1 shl 3
CWBitGravity		=	1 shl 4
CWWinGravity		=	1 shl 5
CWBackingStore          =	1 shl 6
CWBackingPlanes	        =	1 shl 7
CWBackingPixel	        =	1 shl 8
CWOverrideRedirect	=	1 shl 9
CWSaveUnder		=	1 shl 10
CWEventMask		=	1 shl 11
CWDontPropagate	        =	1 shl 12
CWColormap		=	1 shl 13
CWCursor	        =	1 shl 14

; GRAPHICS DEFINITIONS
;
GXclear			=	 0		; 0
GXand			=	 1		; src AND dst
GXandReverse		=	 2		; src AND NOT dst
GXcopy			=	 3		; src
GXandInverted		=	 4		; NOT src AND dst
GXnoop			=	 5		; dst
GXxor			=	 6		; src XOR dst
GXor			=	 7		; src OR dst
GXnor			=	 8		; NOT src AND NOT dst
GXequiv			=	 9		; NOT src XOR dst
GXinvert		=	10		; NOT dst
GXorReverse		=	11		; src OR NOT dst
GXcopyInverted		=	12		; NOT src
GXorInverted		=	13		; NOT src OR dst
GXnand			=	14		; NOT src OR NOT dst
GXset			=	15		; 1
;
; LineStyle
LineSolid		=	0
LineOnOffDash		=	1
LineDoubleDash		=	2
;
; capStyle
CapNotLast		=	0
CapButt			=	1
CapRound		=	2
CapProjecting		=	3
;
; joinStyle
JoinMiter		=	0
JoinRound		=	1
JoinBevel		=	2
;
; fillStyle
FillSolid		=	0
FillTiled		=	1
FillStippled		=	2
FillOpaqueStippled	=	3
;
; fillRule
EvenOddRule		=	0
WindingRule		=	1
;
; subwindow mode
ClipByChildren		=	0
IncludeInferiors	=	1
;
; SetClipRectangles ordering
Unsorted		=	0
YSorted			=	1
YXSorted		=	2
YXBanded		=	3
;
; CoordinateMode for drawing routines
CoordModeOrigin		=	0	; relative to the origin
CoordModePrevious       =	1	; relative to previous point
;
; Polygon shapes
Complex			=	0	; paths may intersect
Nonconvex		=	1	; no paths intersect, but not convex
Convex			=	2	; wholly convex
;
; Arc modes for PolyFillArc
ArcChord		=	0	; join endpoints of arc
ArcPieSlice		=	1	; join endpoints to center of arc
;
; GC components: masks used in CreateGC, CopyGC, ChangeGC, OR'ed into GC.stateChanges
GCFunction              =	1 shl 0
GCPlaneMask             =	1 shl 1
GCForeground            =	1 shl 2
GCBackground            =	1 shl 3
GCLineWidth             =	1 shl 4
GCLineStyle             =	1 shl 5
GCCapStyle              =	1 shl 6
GCJoinStyle		=	1 shl 7
GCFillStyle		=	1 shl 8
GCFillRule		=	1 shl 9 
GCTile			=	1 shl 10
GCStipple		=	1 shl 11
GCTileStipXOrigin	=	1 shl 12
GCTileStipYOrigin	=	1 shl 13
GCFont 			=	1 shl 14
GCSubwindowMode		=	1 shl 15
GCGraphicsExposures     =	1 shl 16
GCClipXOrigin		=	1 shl 17
GCClipYOrigin		=	1 shl 18
GCClipMask		=	1 shl 19
GCDashOffset		=	1 shl 20
GCDashList		=	1 shl 21
GCArcMode		=	1 shl 22
GCLastBit		=	22


; Input Event Masks. Used as event-mask window attribute and as arguments
; to Grab requests.  Not to be confused with event names.
NoEventMask		=	0
KeyPressMask		=	1 shl 0
KeyReleaseMask		=	1 shl 1
ButtonPressMask		=	1 shl 2
ButtonReleaseMask	=	1 shl 3
EnterWindowMask		=	1 shl 4
LeaveWindowMask		=	1 shl 5
PointerMotionMask	=	1 shl 6
PointerMotionHintMask	=	1 shl 7
Button1MotionMask	=	1 shl 8
Button2MotionMask	=	1 shl 9
Button3MotionMask	=	1 shl 10
Button4MotionMask	=	1 shl 11
Button5MotionMask	=	1 shl 12
ButtonMotionMask	=	1 shl 13
KeymapStateMask		=	1 shl 14
ExposureMask		=	1 shl 15
VisibilityChangeMask	=	1 shl 16
StructureNotifyMask	=	1 shl 17
ResizeRedirectMask	=	1 shl 18
SubstructureNotifyMask	=	1 shl 19
SubstructureRedirectMask=	1 shl 20
FocusChangeMask		=	1 shl 21
PropertyChangeMask	=	1 shl 22
ColormapChangeMask	=	1 shl 23
OwnerGrabButtonMask	=	1 shl 24


; Event names.  Used in "type" field in XEvent structures. Not to be
; confused with event masks above. They start from 2 because 0 and 1
; are reserved in the protocol for errors and replies.
KeyPress		=	2
KeyRelease		=	3
ButtonPress		=	4
ButtonRelease		=	5
MotionNotify		=	6
EnterNotify		=	7
LeaveNotify		=	8
FocusIn			=	9
FocusOut		=	10
KeymapNotify		=	11
Expose			=	12
GraphicsExpose		=	13
NoExpose		=	14
VisibilityNotify	=	15
CreateNotify		=	16
DestroyNotify		=	17
UnmapNotify		=	18
MapNotify		=	19
MapRequest		=	20
ReparentNotify		=	21
ConfigureNotify		=	22
ConfigureRequest	=	23
GravityNotify		=	24
ResizeRequest		=	25
CirculateNotify		=	26
CirculateRequest	=	27
PropertyNotify		=	28
SelectionClear		=	29
SelectionRequest	=	30
SelectionNotify		=	31
ColormapNotify		=	32
ClientMessage		=	33
MappingNotify		=	34
LASTEvent		=	35	; must be bigger than any event #


; Key masks. Used as modifiers to GrabButton and GrabKey, results of
; QueryPointer, state in various key-, mouse-, and button-related events.
ShiftMask		=	0
LockMask		=	1
ControlMask		=	2
Mod1Mask		=	3
Mod2Mask		=	4
Mod3Mask		=	5
Mod4Mask		=	6
Mod5Mask		=	7

; modifier names. Used to build a SetModifierMapping request or to read
; a GetModifierMapping request. These correspond to the masks defined above.
ShiftMapIndex		=	0
LockMapIndex		=	1
ControlMapIndex		=	2
Mod1MapIndex		=	3
Mod2MapIndex		=	4
Mod3MapIndex		=	5
Mod4MapIndex		=	6
Mod5MapIndex		=	7


; button masks. Used in same manner as Key masks above. Not to be confused
; with button names below.
Button1Mask		=	1 shl 8
Button2Mask		=	1 shl 9
Button3Mask		=	1 shl 10
Button4Mask		=	1 shl 11
Button5Mask		=	1 shl 12

AnyModifier		=	1 shl 15	; used in GrabButton, GrabKey


; button names. Used as arguments to GrabButton and as detail in ButtonPress
; and ButtonRelease events.  Not to be confused with button masks above.
; Note that 0 is already defined above as "AnyButton".
Button1			=	1
Button2			=	2
Button3			=	3
Button4			=	4
Button5			=	5

; Notify modes
NotifyNormal		=	0
NotifyGrab		=	1
NotifyUngrab		=	2
NotifyWhileGrabbed	=	3

