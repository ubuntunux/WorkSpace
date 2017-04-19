; /usr/X11R6/include/X11/Xlib.h

; Display datatype maintaining display specific data.
; The contents of this structure are implementation dependent.
; A Display should be treated as opaque by application code.
;
struc XPrivDisplay
{
.ext_data		rq	1	; hook for extension to hang data
.private1		rq	1
.fd			rd	1	; Network socket.
.private2		rd	1
.proto_major_version	rd	1	; major version of server's X protocol
.proto_minor_version	rd	1	; minor version of servers X protocol
.vendor			rq	1	; vendor of the server hardware
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
			rq	1
.display_name		rq	1	; "host:display" string used on this connect, typical like :0.0
.default_screen		rd	1	; default screen for operations
.nscreens		rd	1	; number of screens on this server
.screens		rq	1	; pointer to list of screens
;... other params
; there is more to this structure, but it is private to Xlib
}
XDisplay	XPrivDisplay


; Information about the screen. The contents of this structure are
; implementation dependent. A Screen should be treated as opaque
; by application code.
;
struc Screen
{
.ext_data		rq	1	; hook for extension to hang data
.display		rq	1	; back pointer to display strucure
.root			rq	1	; Root window id.
.width			rd	1
.height			rd	1	; width and height of screen
.mwidth			rd	1
.mheight		rd	1	; width and height of  in millimeters
.ndepths		rd	1	; number of depths possible
			rd	1	; dummy, keep align 8 for next pointer
.depths			rq	1	; list of allowable depths on the screen
.root_depth		rd	1	; bits per pixel
			rd	1
.root_visual		rq	1	; root visual
.default_gc		rq	1	; GC for the root root visual
.cmap			rq	1	; default color map
.white_pixel		rq	1
.black_pixel		rq	1	; White and Black pixel values
.max_maps		rd	1
.min_maps		rd	1	; max and min color maps
.backing_store		rd	1	; Never, WhenMapped, Always
.save_unders		rd	1
.root_input_mask	rq	1	; initial root input mask
}


; Data structure for setting window attributes.
;
struc XSetWindowAttributes
{
.background_pixmap	rq	1	; background or None or ParentRelative
.background_pixel	rq	1	; background pixel
.border_pixmap		rq	1	; border of the window
.border_pixel		rq	1	; border pixel value
.bit_gravity		rd	1	; one of bit gravity values
.win_gravity		rd	1	; one of the window gravity values
.backing_store		rd	1	; NotUseful, WhenMapped, Always
			rd	1
.backing_planes		rq	1	; planes to be preseved if possible
.backing_pixel		rq	1	; value to use in restoring planes
.save_under		rd	1	; should bits under be saved? (popups)
			rd	1
.event_mask		rq	1	; set of events that should be saved
.do_not_propagate_mask	rq	1	; set of events that should not propagate
.override_redirect	rd	1	; boolean value for override-redirect
			rd	1
.colormap		rq	1	; color map to be associated with window
.cursor			rq	1	; cursor to be displayed (or None)
}


; Data structure for setting graphics context.
;
struc XGCValues
{
.function		rd	1	; logical operation
			rd	1
.plane_mask		rq	1	; plane mask
.foreground		rq	1	; foreground pixel
.background		rq	1	; background pixel
.line_width		rd	1	; line width
.line_style		rd	1 	; LineSolid, LineOnOffDash, LineDoubleDash
.cap_style		rd	1  	; CapNotLast, CapButt, CapRound, CapProjecting
.join_style		rd	1 	; JoinMiter, JoinRound, JoinBevel
.fill_style		rd	1	; FillSolid, FillTiled, FillStippled. FillOpaqueStippled
.fill_rule		rd	1  	; EvenOddRule, WindingRule
.arc_mode		rd	1	; ArcChord, ArcPieSlice
			rd	1
.tile			rq	1	; tile pixmap for tiling operations
.stipple		rq	1	; stipple 1 plane pixmap for stipping
.ts_x_origin		rd	1	; offset for tile or stipple operations
.ts_y_origin		rd	1
.font			rq	1	; default text font for text operations
.subwindow_mode		rd	1	; ClipByChildren, IncludeInferiors
.graphics_exposures	rd	1	; boolean, should exposures be generated
.clip_x_origin		rd	1	; origin for clipping
.clip_y_origin		rd	1
.clip_mask		rq	1	; bitmap clipping; other calls for rects
.dash_offset		rd	1	; patterned/dashed line information
			rd	1
.dashes			rq	1
}


struc XFontStruct
{
.ext_data		rq	1	; hook for extension to hang data
.fid			rq	1	; Font id for this font
.direction		rd	1	; hint about direction the font is painted
.min_char_or_byte2	rd	1	; first character
.max_char_or_byte2	rd	1	; last character
.min_byte1		rd	1	; first row that exists
.max_byte1		rd	1	; last row that exists
.all_chars_exist	rd	1	; flag if all characters have non-zero size
.default_char		rd	1	; char to print for undefined character
.n_properties		rd	1	; how many properties there are
.properties		rq	1	; pointer to array of additional properties
.min_bounds		rq	1	; minimum bounds over all existing char
.max_bounds		rq	1	; maximum bounds over all existing char
.per_char		rq	1	; first_char to last_char information
.ascent			rd	1	; log. extent above baseline for spacing
.descent		rd	1	; log. descent below baseline for spacing
}


; Data structure used by color operations
struc XColor
{
.pixel			rq	1
.red			rw	1
.green			rw	1
.blue			rw	1
			rw	1	; padding for keep align 8
.flags			rq	1	; do_red, do_green, do_blue
.pad			rq	1
}


; Definitions of specific events.
;
struc XKeyEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.window			rq	1	; "event" window it is reported relative to
.root			rq	1	; root window that the event occurred on
.subwindow		rq	1	; child window
.time			rq	1	; milliseconds
.x			rd	1
.y			rd	1	; pointer x, y coordinates in event window
.x_root			rd	1
.y_root			rd	1	; coordinates relative to root
.state			rd	1	; key or button mask
.keycode		rd	1	; detail
.same_screen		rd	1	; same screen flag
			rd	1
}
XKeyPressedEvent	XKeyEvent
XKeyReleasedEvent	XKeyEvent


struc XButtonEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.window			rq	1	; "event" window it is reported relative to
.root			rq	1	; root window that the event occurred on
.subwindow		rq	1	; child window
.time			rq	1	; milliseconds
.x			rd	1
.y			rd	1	; pointer x, y coordinates in event window
.x_root			rd	1
.y_root			rd	1	; coordinates relative to root
.state			rd	1	; key or button mask
.button			rd	1	; detail
.same_screen		rd	1	; same screen flag
			rd	1
}
XButtonPressedEvent	XButtonEvent
XButtonReleasedEvent	XButtonEvent


struc XMotionEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.window			rq	1	; "event" window it is reported relative to
.root			rq	1	; root window that the event occurred on
.subwindow		rq	1	; child window
.time			rq	1	; milliseconds
.x			rd	1
.y			rd	1	; pointer x, y coordinates in event window
.x_root			rd	1
.y_root			rd	1	; coordinates relative to root
.state			rd	1	; key or button mask
.is_hint		rd	1	; detail
.same_screen		rd	1	; same screen flag
			rd	1
}
XPointerMovedEvent	XMotionEvent


struc XExposeEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.window			rq	1	; "event" window it is reported relative to
.x			rd	1
.y			rd	1	; pointer x, y coordinates in event window
.width			rd	1
.height			rd	1	; coordinates relative to root
.count			rd	1	; if non-zero, at least this many more
			rd	1
}


struc XGraphicsExposeEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.drawable		rq	1
.x			rd	1
.y			rd	1	; pointer x, y coordinates in event window
.width			rd	1
.height			rd	1	; coordinates relative to root
.count			rd	1	; if non-zero, at least this many more
.major_code		rd	1	; core is CopyArea or CopyPlane
.minor_code		rd	1	; not defined in the core
			rd	1
}


struc XNoExposeEvent
{
.type			rd	1	; of event
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.drawable		rq	1
.major_code		rd	1	; core is CopyArea or CopyPlane
.minor_code		rd	1	; not defined in the core
}


struc XAnyEvent
{
.type			rd	1
			rd	1
.serial			rq	1	; # of last request processed by server
.send_event		rd	1	; true if this came from a SendEvent request
			rd	1
.display		rq	1	; Display the event was read from
.window			rq	1	; window on which event was requested in event mask
}

