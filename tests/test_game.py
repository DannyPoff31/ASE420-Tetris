"""
Comprehensive test suite for game.py

Includes:
- Unit tests: testing run_game with full mocking
- Integration tests: testing with minimal mocking
- End-to-end (E2E) tests: testing with real components (Config, Input, Renderer)

Author: Test Suite
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Add the tetris module to the path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tetris.new_code.tetris_game.main.game import run_game


# ============================================================================
# UNIT TESTS: Full mocking of all dependencies
# ============================================================================
class TestRunGameUnit:
    """Unit tests for the run_game function with full mocking"""

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_initializes_pygame(self, mock_state_manager, mock_config_class, 
                                      mock_input_class, mock_renderer_class, mock_pygame):
        """Test that pygame is initialized when game runs"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False  # Exit on first iteration
        mock_state_manager.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_pygame.init.assert_called_once()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_creates_display(self, mock_state_manager, mock_config_class, 
                                   mock_input_class, mock_renderer_class, mock_pygame):
        """Test that pygame display is created with correct dimensions"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_pygame.display.set_mode.assert_called_once_with((800, 600))
        mock_pygame.display.set_caption.assert_called_once_with("Code^3 Tetris")

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_creates_renderer_with_screen(self, mock_state_manager, mock_config_class, 
                                                mock_input_class, mock_renderer_class, mock_pygame):
        """Test that Renderer is created with the screen object"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_renderer_class.assert_called_once_with(screen=mock_screen)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_creates_input_with_config(self, mock_state_manager, mock_config_class, 
                                             mock_input_class, mock_renderer_class, mock_pygame):
        """Test that Input is created with the config object"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_input_class.assert_called_once_with(mock_config)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_creates_state_manager(self, mock_state_manager_class, mock_config_class, 
                                         mock_input_class, mock_renderer_class, mock_pygame):
        """Test that EnhancedStateManager is created with correct dependencies"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_input = Mock()
        mock_input_class.return_value = mock_input

        mock_renderer = Mock()
        mock_renderer_class.return_value = mock_renderer

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_state_manager_class.assert_called_once_with(mock_config, mock_input, mock_renderer)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_loop_updates_state_manager(self, mock_state_manager_class, mock_config_class, 
                                              mock_input_class, mock_renderer_class, mock_pygame):
        """Test that state manager is updated in the main loop"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # Return True twice, then False to exit loop
        mock_state_manager_instance.update.side_effect = [True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - update should be called 3 times (True, True, False)
        assert mock_state_manager_instance.update.call_count == 3

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_loop_refreshes_display(self, mock_state_manager_class, mock_config_class, 
                                          mock_input_class, mock_renderer_class, mock_pygame):
        """Test that display is flipped each iteration"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # Run loop twice
        mock_state_manager_instance.update.side_effect = [True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - display.flip should be called twice (once per loop iteration)
        assert mock_pygame.display.flip.call_count == 2

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_loop_ticks_clock(self, mock_state_manager_class, mock_config_class, 
                                    mock_input_class, mock_renderer_class, mock_pygame):
        """Test that clock is ticked with correct FPS"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        assert mock_clock.tick.call_count == 2
        mock_clock.tick.assert_called_with(60)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_quits_pygame(self, mock_state_manager_class, mock_config_class, 
                                mock_input_class, mock_renderer_class, mock_pygame):
        """Test that pygame.quit() is called when game ends"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_pygame.quit.assert_called_once()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_counter_increments_by_level(self, mock_state_manager_class, mock_config_class, 
                                               mock_input_class, mock_renderer_class, mock_pygame):
        """Test that counter increments by level each iteration"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 5
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - counter should be incremented twice (5 + 5 = 10)
        assert mock_config.counter == 10

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_counter_resets_on_overflow(self, mock_state_manager_class, mock_config_class, 
                                              mock_input_class, mock_renderer_class, mock_pygame):
        """Test that counter resets to 0 when it exceeds 100000"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 99999
        mock_config.level = 5
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - counter should be reset to 0 (99999 + 5 = 100004, which is > 100000)
        assert mock_config.counter == 0

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_exits_on_state_manager_false(self, mock_state_manager_class, mock_config_class, 
                                                mock_input_class, mock_renderer_class, mock_pygame):
        """Test that game loop exits when state manager returns False"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - update should be called only once
        assert mock_state_manager_instance.update.call_count == 1
        mock_pygame.quit.assert_called_once()


# ============================================================================
# INTEGRATION TESTS: Minimal mocking, test component interactions
# ============================================================================
class TestRunGameIntegration:
    """Integration tests for the run_game function with minimal mocking"""

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_full_initialization_sequence(self, mock_state_manager_class, 
                                                mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify full initialization sequence with minimal mocks"""
        # Setup - keep Config real, mock only pygame and state manager
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - verify all initialization steps occurred
        mock_pygame.init.assert_called_once()
        mock_pygame.display.set_mode.assert_called_once()
        mock_pygame.display.set_caption.assert_called_with("Code^3 Tetris")
        mock_pygame.time.Clock.assert_called_once()
        mock_pygame.font.SysFont.assert_called_once()
        mock_renderer_class.assert_called_once()
        mock_input_class.assert_called_once()
        mock_state_manager_class.assert_called_once()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_multiple_loop_iterations(self, mock_state_manager_class, 
                                            mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: run multiple game loop iterations"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1

        mock_state_manager_instance = Mock()
        # Simulate 5 successful iterations then exit
        mock_state_manager_instance.update.side_effect = [True] * 5 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        assert mock_state_manager_instance.update.call_count == 6  # 5 True + 1 False
        assert mock_pygame.display.flip.call_count == 6
        clock_mock = mock_pygame.time.Clock()
        assert clock_mock.tick.call_count == 6

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_state_manager_receives_all_dependencies(self, mock_state_manager_class, 
                                                           mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify state manager receives correct dependencies"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1

        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_input = Mock()
        mock_input_class.return_value = mock_input

        mock_renderer = Mock()
        mock_renderer_class.return_value = mock_renderer

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - state manager should receive config, input, and renderer
        call_args = mock_state_manager_class.call_args
        assert call_args[0][0] == mock_config  # config
        assert call_args[0][1] == mock_input    # input
        assert call_args[0][2] == mock_renderer # renderer

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_renderer_uses_correct_screen(self, mock_state_manager_class, 
                                                 mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify renderer receives the correct screen object"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 1024
        mock_config.window_height = 768
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1

        mock_screen = Mock(name='MockScreen')
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - renderer should be created with the exact screen object
        mock_renderer_class.assert_called_once_with(screen=mock_screen)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_clock_fps_matches_config(self, mock_state_manager_class, 
                                            mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify clock is ticked with config FPS"""
        # Setup
        fps_values = [30, 60, 120, 144]
        
        for fps in fps_values:
            mock_config = Mock()
            mock_config.window_width = 800
            mock_config.window_height = 600
            mock_config.fps = fps
            mock_config.counter = 0
            mock_config.level = 1

            mock_clock = Mock()
            mock_pygame.time.Clock.return_value = mock_clock

            mock_state_manager_instance = Mock()
            mock_state_manager_instance.update.side_effect = [True, False]
            mock_state_manager_class.return_value = mock_state_manager_instance

            # Execute
            run_game()

            # Assert
            mock_clock.tick.assert_called_with(fps)
            mock_pygame.reset_mock()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_window_dimensions_from_config(self, mock_state_manager_class, 
                                                 mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify window is created with config dimensions"""
        # Setup
        dimensions = [(640, 480), (800, 600), (1024, 768), (1920, 1080)]

        for width, height in dimensions:
            mock_config = Mock()
            mock_config.window_width = width
            mock_config.window_height = height
            mock_config.fps = 60
            mock_config.counter = 0
            mock_config.level = 1

            mock_state_manager_instance = Mock()
            mock_state_manager_instance.update.return_value = False
            mock_state_manager_class.return_value = mock_state_manager_instance

            # Execute
            run_game()

            # Assert
            mock_pygame.display.set_mode.assert_called_with((width, height))
            mock_pygame.reset_mock()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_counter_progression_over_iterations(self, mock_state_manager_class, 
                                                       mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify counter increments correctly over multiple iterations"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 50000
        mock_config.level = 10000

        mock_state_manager_instance = Mock()
        # 3 iterations: 50000 -> 60000 -> 70000 -> 80000
        mock_state_manager_instance.update.side_effect = [True, True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - final counter should be 80000 (50000 + 3*10000)
        assert mock_config.counter == 80000

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_game_counter_overflow_multiple_times(self, mock_state_manager_class, 
                                                    mock_input_class, mock_renderer_class, mock_pygame):
        """Integration test: verify counter resets multiple times if needed"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 99000
        mock_config.level = 500  # Will overflow multiple times

        mock_state_manager_instance = Mock()
        # After first iteration: 99000 + 500 = 99500 (no reset)
        # After second: 99500 + 500 = 100000 (reset to 0)
        # After third: 0 + 500 = 500 (no reset)
        mock_state_manager_instance.update.side_effect = [True, True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        assert mock_config.counter == 500


# ============================================================================
# REGRESSION TESTS: Ensure previously fixed bugs don't reoccur
# ============================================================================
class TestRunGameRegression:
    """Regression tests to prevent previously fixed bugs from reoccurring"""

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_pygame_not_quit_before_loop_ends(self, mock_state_manager_class, 
                                                          mock_config_class, mock_input_class, 
                                                          mock_renderer_class, mock_pygame):
        """Regression test: pygame.quit is called only after loop exits, not before"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        call_order = []
        
        def track_flip():
            call_order.append('flip')
        
        def track_quit():
            call_order.append('quit')
            
        mock_pygame.display.flip.side_effect = track_flip
        mock_pygame.quit.side_effect = track_quit

        # Execute
        run_game()

        # Assert - flip should come before quit in call order
        flip_index = call_order.index('flip')
        quit_index = call_order.index('quit')
        assert flip_index < quit_index, "pygame.display.flip should be called before pygame.quit"

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_counter_exact_threshold(self, mock_state_manager_class, 
                                                 mock_config_class, mock_input_class, 
                                                 mock_renderer_class, mock_pygame):
        """Regression test: counter resets at exactly 100000, not before or after"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 99999
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - counter should be exactly 0 (99999 + 1 = 100000 which triggers reset)
        assert mock_config.counter == 0, "Counter should reset at > 100000"

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_screen_initialized_before_renderer(self, mock_state_manager_class, 
                                                            mock_config_class, mock_input_class, 
                                                            mock_renderer_class, mock_pygame):
        """Regression test: screen is created before Renderer initialization"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        call_order = []
        
        def track_set_mode():
            call_order.append('set_mode')
            return Mock()
        
        def track_renderer_init(*args, **kwargs):
            call_order.append('renderer_init')
            return Mock()

        mock_pygame.display.set_mode.side_effect = track_set_mode
        mock_renderer_class.side_effect = track_renderer_init

        # Execute
        run_game()

        # Assert
        set_mode_index = call_order.index('set_mode')
        renderer_init_index = call_order.index('renderer_init')
        assert set_mode_index < renderer_init_index, "Screen must be set before Renderer init"

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_loop_continues_when_state_manager_true(self, mock_state_manager_class, 
                                                                mock_config_class, mock_input_class, 
                                                                mock_renderer_class, mock_pygame):
        """Regression test: loop continues when state_manager.update() returns True"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # Return True 10 times to verify loop continues
        mock_state_manager_instance.update.side_effect = [True] * 10 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - update should be called 11 times (10 True + 1 False)
        assert mock_state_manager_instance.update.call_count == 11

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_config_created_before_pygame_init(self, mock_state_manager_class, 
                                                           mock_config_class, mock_input_class, 
                                                           mock_renderer_class, mock_pygame):
        """Regression test: Config is created before pygame.init is called"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        call_order = []
        
        def track_config_create():
            call_order.append('config_create')
            return mock_config
        
        def track_pygame_init():
            call_order.append('pygame_init')

        mock_config_class.side_effect = track_config_create
        mock_pygame.init.side_effect = track_pygame_init

        # Execute
        run_game()

        # Assert
        config_index = call_order.index('config_create')
        pygame_init_index = call_order.index('pygame_init')
        assert config_index < pygame_init_index, "Config must be created before pygame.init"

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_regression_clock_tick_prevents_cpu_spin(self, mock_state_manager_class, 
                                                      mock_config_class, mock_input_class, 
                                                      mock_renderer_class, mock_pygame):
        """Regression test: clock.tick is called to prevent CPU spinning"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - clock.tick should be called same number of times as loop iterations
        assert mock_clock.tick.call_count == 4
        # Verify it's called with the FPS value from config
        for call_obj in mock_clock.tick.call_args_list:
            assert call_obj[0][0] == 60


# ============================================================================
# ACCEPTANCE TESTS: High-level user scenarios and requirements
# ============================================================================
class TestRunGameAcceptance:
    """Acceptance tests for user-facing requirements and scenarios"""

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_can_start_and_stop(self, mock_state_manager_class, 
                                                 mock_config_class, mock_input_class, 
                                                 mock_renderer_class, mock_pygame):
        """Acceptance: Player can start the game and it initializes without errors"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False  # Game exits immediately
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute - should not raise any exceptions
        try:
            run_game()
            success = True
        except Exception as e:
            success = False

        # Assert
        assert success, "Game should start and stop without errors"
        mock_pygame.init.assert_called_once()
        mock_pygame.quit.assert_called_once()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_window_displays_correctly(self, mock_state_manager_class, 
                                                        mock_config_class, mock_input_class, 
                                                        mock_renderer_class, mock_pygame):
        """Acceptance: Game window is displayed with correct title"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - window should be created with correct title
        mock_pygame.display.set_mode.assert_called_once()
        mock_pygame.display.set_caption.assert_called_once_with("Code^3 Tetris")

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_runs_at_configured_fps(self, mock_state_manager_class, 
                                                     mock_config_class, mock_input_class, 
                                                     mock_renderer_class, mock_pygame):
        """Acceptance: Game runs at the FPS specified in configuration"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60  # User configures 60 FPS
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - clock.tick should be called with the configured FPS
        for call_obj in mock_clock.tick.call_args_list:
            assert call_obj[0][0] == 60

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_loop_runs_continuously(self, mock_state_manager_class, 
                                                     mock_config_class, mock_input_class, 
                                                     mock_renderer_class, mock_pygame):
        """Acceptance: Game loop continues running until state manager indicates exit"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # Simulate 100 frames of gameplay
        mock_state_manager_instance.update.side_effect = [True] * 100 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - game should run for 101 iterations (100 True + 1 False)
        assert mock_state_manager_instance.update.call_count == 101

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_receives_user_input(self, mock_state_manager_class, 
                                                  mock_config_class, mock_input_class, 
                                                  mock_renderer_class, mock_pygame):
        """Acceptance: Game creates Input component to handle user input"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_input = Mock()
        mock_input_class.return_value = mock_input

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - Input should be created to handle player input
        mock_input_class.assert_called_once_with(mock_config)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_renders_output(self, mock_state_manager_class, 
                                             mock_config_class, mock_input_class, 
                                             mock_renderer_class, mock_pygame):
        """Acceptance: Game creates Renderer to display game visuals"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_renderer = Mock()
        mock_renderer_class.return_value = mock_renderer

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - Renderer should be created with screen to display visuals
        mock_renderer_class.assert_called_once_with(screen=mock_screen)

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_frame_is_updated_every_iteration(self, mock_state_manager_class, 
                                                               mock_config_class, mock_input_class, 
                                                               mock_renderer_class, mock_pygame):
        """Acceptance: Game display is refreshed (flipped) every frame"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # 50 frames of gameplay
        mock_state_manager_instance.update.side_effect = [True] * 50 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - display should be flipped once per frame (51 times)
        assert mock_pygame.display.flip.call_count == 51

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_graceful_shutdown(self, mock_state_manager_class, 
                                                mock_config_class, mock_input_class, 
                                                mock_renderer_class, mock_pygame):
        """Acceptance: Game shuts down gracefully when requested"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 1
        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # Simulate player requesting exit after a few frames
        mock_state_manager_instance.update.side_effect = [True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute - should not raise exceptions
        try:
            run_game()
            shutdown_clean = True
        except Exception as e:
            shutdown_clean = False

        # Assert
        assert shutdown_clean, "Game should shut down gracefully"
        mock_pygame.quit.assert_called_once()

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.Renderer')
    @patch('tetris.new_code.tetris_game.main.game.Input')
    @patch('tetris.new_code.tetris_game.main.game.Config')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_acceptance_game_tracks_score_progression(self, mock_state_manager_class, 
                                                       mock_config_class, mock_input_class, 
                                                       mock_renderer_class, mock_pygame):
        """Acceptance: Game tracks player score/counter throughout gameplay"""
        # Setup
        mock_config = Mock()
        mock_config.window_width = 800
        mock_config.window_height = 600
        mock_config.fps = 60
        mock_config.counter = 0
        mock_config.level = 10  # Player is at level 10

        mock_config_class.return_value = mock_config

        mock_state_manager_instance = Mock()
        # 5 frames of gameplay
        mock_state_manager_instance.update.side_effect = [True] * 5 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - counter should increment based on level (5 frames * level 10 = 50)
        assert mock_config.counter == 50
