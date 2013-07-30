import unittest
import logging
from mock import patch, MagicMock

import soklog


class SoklogTest(unittest.TestCase):

    @patch('soklog.logging.getLogger')
    def test_init(self, mock):
        soklog.init(1, 2)

        mock.assert_called_with(2)
        self.assertEqual(1, soklog.data['module'])
        self.assertEqual(mock.return_value, soklog.data['log'])

    def test__get_args_as_string(self):
        self.assertEqual('1 2 3', soklog._get_args_as_string([1, 2, '3']))

    @patch.dict(soklog.data, {'log': MagicMock()})
    def test_info(self):
        soklog.info(1, 2, 3, something=4)
        soklog.data['log'].info.assert_called_with("1 2 3", something=4)

    @patch.dict(soklog.data, {'log': MagicMock()})
    def test_warning(self):
        soklog.warning(1, 2, 3, something=4)
        soklog.data['log'].warning.assert_called_with("1 2 3", something=4)

    @patch.dict(soklog.data, {'log': MagicMock(), 'module': soklog})
    def test_debug(self):
        soklog.debug(1, 2, 3, something=4)
        soklog.data['log'].debug.assert_called_with(
            './tests.py:33 1 2 3', something=4)

    @patch.dict(soklog.data, {'log': MagicMock()})
    def test_error(self):
        soklog.error(1, 2, 3, something=4)
        soklog.data['log'].error.assert_called_with(1, 2, 3, something=4)

    @patch('soklog.logging.basicConfig')
    def test_start_stdout_logging(self, mock):
        soklog.start_stdout_logging()
        mock.assert_called_with(
            level=logging.DEBUG,
            format="%(asctime)-10s %(message)s",
            datefmt="%H:%M:%S"
        )

    @patch.dict(soklog.data, {'log': MagicMock()})
    @patch('soklog.logging')
    def test_start_file_logging(self, mock):
        soklog.start_file_logging('somewhere')
        mock.FileHandler.assert_called_with('somewhere')
        mock.Formatter.assert_called_with("%(asctime)-10s %(message)s")

        hdlr = mock.FileHandler.return_value
        hdlr.setFormatter.assert_called_with(mock.Formatter.return_value)

        soklog.data['log'].addHandler.assert_called_with(hdlr)
        soklog.data['log'].setLevel.assert_called_with(mock.DEBUG)
