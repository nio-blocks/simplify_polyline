from nio.block.terminals import DEFAULT_TERMINAL
from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..simplify_polyline_block import SimplifyPolyline
from .test_values import test_points, test_results


class TestSimplifyPolyline(NIOBlockTestCase):
    """
    source: https://github.com/mourner/simplify-js/blob/master/test/test.js
    """

    signal_list = [Signal(point) for point in test_points]

    def _get_result_signals(self, group=None):
        result_signals = []
        for result in test_results:
            result['group'] = group
            result_signals.append(Signal(result))
        return result_signals

    def test_simplify(self):
        """Simplifies points correctly with the given tolerance."""
        blk = SimplifyPolyline()
        self.configure_block(blk, {'tolerance': 5})
        blk.start()
        blk.process_signals(self.signal_list)
        blk.stop()
        self.assert_last_signal_list_notified(self._get_result_signals())

    def test_one_point(self):
        """Just return the points if it has only one point."""
        blk = SimplifyPolyline()
        self.configure_block(blk, {'tolerance': 5})
        blk.start()
        blk.process_signals([self.signal_list[0]])
        blk.stop()
        self.assert_last_signal_list_notified([self._get_result_signals()[0]])
