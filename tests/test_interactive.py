"""Tests for interactive CLI module"""
import unittest
from unittest.mock import patch
from pygubuai.interactive import prompt, confirm, choose, interactive_create


class TestPrompt(unittest.TestCase):
    """Test prompt function"""
    
    @patch('builtins.input', return_value='test')
    def test_prompt_with_input(self, mock_input):
        result = prompt("Enter name")
        self.assertEqual(result, 'test')
    
    @patch('builtins.input', return_value='')
    def test_prompt_with_default(self, mock_input):
        result = prompt("Enter name", default="default")
        self.assertEqual(result, 'default')
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_prompt_keyboard_interrupt(self, mock_input):
        with self.assertRaises(SystemExit):
            prompt("Enter name")


class TestConfirm(unittest.TestCase):
    """Test confirm function"""
    
    @patch('builtins.input', return_value='y')
    def test_confirm_yes(self, mock_input):
        result = confirm("Continue?")
        self.assertTrue(result)
    
    @patch('builtins.input', return_value='n')
    def test_confirm_no(self, mock_input):
        result = confirm("Continue?")
        self.assertFalse(result)
    
    @patch('builtins.input', return_value='')
    def test_confirm_default_true(self, mock_input):
        result = confirm("Continue?", default=True)
        self.assertTrue(result)
    
    @patch('builtins.input', return_value='')
    def test_confirm_default_false(self, mock_input):
        result = confirm("Continue?", default=False)
        self.assertFalse(result)


class TestChoose(unittest.TestCase):
    """Test choose function"""
    
    @patch('builtins.input', return_value='1')
    def test_choose_first_option(self, mock_input):
        result = choose("Select", ["option1", "option2"])
        self.assertEqual(result, "option1")
    
    @patch('builtins.input', return_value='2')
    def test_choose_second_option(self, mock_input):
        result = choose("Select", ["option1", "option2"])
        self.assertEqual(result, "option2")
    
    @patch('builtins.input', return_value='')
    def test_choose_default(self, mock_input):
        result = choose("Select", ["option1", "option2"], default="option1")
        self.assertEqual(result, "option1")


class TestInteractiveCreate(unittest.TestCase):
    """Test interactive_create function"""
    
    @patch('builtins.input', side_effect=['myapp', 'test app', 'n', 'y'])
    def test_interactive_create_no_template(self, mock_input):
        result = interactive_create()
        self.assertEqual(result['name'], 'myapp')
        self.assertEqual(result['description'], 'test app')
        self.assertIsNone(result['template'])
        self.assertTrue(result['git'])
    
    @patch('builtins.input', side_effect=['myapp', 'test app', 'y', '1', 'n'])
    def test_interactive_create_with_template(self, mock_input):
        result = interactive_create()
        self.assertEqual(result['name'], 'myapp')
        self.assertEqual(result['description'], 'test app')
        self.assertEqual(result['template'], 'login')
        self.assertFalse(result['git'])


if __name__ == '__main__':
    unittest.main()
