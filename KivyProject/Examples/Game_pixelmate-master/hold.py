from copy import copy

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.vector import Vector


class TapAndHoldWidget(Widget):
    ''' A tap and hold mixIn for widgets '''
    _point = None  # Contains point after trigger
    _sensitivity = 4  # Sensitivity (pixels)
    _hold_length = 1.4  # Seconds
    _event = None  # Outstanding event or none
    triggered = False  # Whether or not the event was triggered

    def _distance(self, touch):
        ''' Calculate distance moved from start '''
        if self._point is not None:
            return Vector(touch.pos).distance(self._point.pos)
        return 0

    def _release_event(self):
        ''' Free up and cancel any outstanding event '''
        if self._event is not None:
            self._event.release()  # stop any outstanding events
        self._event = None

    def _long_hold(self, _dt):
        ''' Comes here after a tap and hold '''
        if self._event is not None:
            self.triggered = True
            self.on_hold(self._point)  # Generate event
            self._release_event()

    def on_touch_down(self, touch):
        super(TapAndHoldWidget, self).on_touch_down(touch)
        ''' touch down event '''
        if self.collide_point(touch.x, touch.y):  # filter touch events
            self.triggered = False
            self._release_event()
            self._point = copy(touch)  # Touch events share an instance
            self._event = Clock.schedule_once(self._long_hold, self._hold_length)

    def on_touch_move(self, touch):
        ''' If there was movement, invalidate the tap+hold '''
        dxy = self._distance(touch)
        if dxy > self._sensitivity:
            self._point = None  # No event triggered
            self._release_event()

    def on_touch_up(self, touch):
        ''' Tap+hold is finished if it was effective '''
        self._point = None
        self._release_event()

    def on_hold(self, touch):
        ''' To be implemented by concrete class '''

