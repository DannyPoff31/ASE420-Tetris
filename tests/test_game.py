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
# END-TO-END TESTS: Real components (Config, Input, Renderer) with pygame mocked
# ============================================================================
class TestRunGameE2E:
    """End-to-end tests for the run_game function with real components"""

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_initializes_with_real_config(self, mock_state_manager_class, mock_pygame):
        """E2E test: game initializes successfully with real Config object"""
        # Setup - Config will be real, only pygame and state manager mocked
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - Config should have been created with real values
        mock_pygame.init.assert_called_once()
        assert mock_state_manager_class.called

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_passes_real_components_to_state_manager(self, mock_state_manager_class, mock_pygame):
        """E2E test: state manager receives real Input and Renderer objects"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - state manager should be called with 3 args (config, input, renderer)
        assert mock_state_manager_class.call_count == 1
        call_args = mock_state_manager_class.call_args[0]
        assert len(call_args) == 3
        
        # First arg should be Config instance
        config = call_args[0]
        assert hasattr(config, 'window_width')
        assert hasattr(config, 'window_height')
        assert hasattr(config, 'counter')
        assert hasattr(config, 'level')
        
        # Second arg should be Input instance
        input_obj = call_args[1]
        assert hasattr(input_obj, 'get_actions')
        assert hasattr(input_obj, 'is_down_pressed')
        
        # Third arg should be Renderer instance
        renderer_obj = call_args[2]
        assert hasattr(renderer_obj, 'render_board')
        assert hasattr(renderer_obj, 'draw_piece')

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_renderer_created_with_real_screen(self, mock_state_manager_class, mock_pygame):
        """E2E test: Renderer is created with actual pygame screen surface"""
        # Setup
        mock_screen = Mock(name='MockScreen')
        mock_pygame.display.set_mode.return_value = mock_screen

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - Renderer should receive the exact screen object
        call_args = mock_state_manager_class.call_args[0]
        renderer = call_args[2]
        assert renderer.screen == mock_screen

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_input_created_with_real_config(self, mock_state_manager_class, mock_pygame):
        """E2E test: Input is created with real Config object"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - Input should have the config
        call_args = mock_state_manager_class.call_args[0]
        config = call_args[0]
        input_obj = call_args[1]
        assert input_obj.config == config

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_loop_with_multiple_state_updates(self, mock_state_manager_class, mock_pygame):
        """E2E test: game loop runs multiple iterations with real components"""
        # Setup
        mock_state_manager_instance = Mock()
        # Run 5 iterations
        mock_state_manager_instance.update.side_effect = [True] * 5 + [False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - state manager update should be called 6 times
        assert mock_state_manager_instance.update.call_count == 6
        assert mock_pygame.display.flip.call_count == 6
        
        # Verify config counter was updated
        call_args = mock_state_manager_class.call_args[0]
        config = call_args[0]
        # Counter should be incremented 6 times (level = 1 by default)
        assert config.counter == 6

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_config_loads_settings_from_files(self, mock_state_manager_class, mock_pygame):
        """E2E test: Config loads window dimensions and FPS from settings files"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - pygame display should be created with config dimensions
        call_args = mock_pygame.display.set_mode.call_args
        dimensions = call_args[0][0]
        
        # Should be a tuple of (width, height)
        assert isinstance(dimensions, tuple)
        assert len(dimensions) == 2
        assert isinstance(dimensions[0], int)  # width
        assert isinstance(dimensions[1], int)  # height
        assert dimensions[0] > 0
        assert dimensions[1] > 0

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_clock_created_for_frame_rate_control(self, mock_state_manager_class, mock_pygame):
        """E2E test: pygame clock is created for FPS control"""
        # Setup
        mock_clock = Mock()
        mock_pygame.time.Clock.return_value = mock_clock

        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_pygame.time.Clock.assert_called_once()
        # Clock should be ticked with a valid FPS value
        assert mock_clock.tick.call_count == 2
        tick_calls = mock_clock.tick.call_args_list
        # All tick calls should have a positive FPS value
        for call in tick_calls:
            fps_value = call[0][0]
            assert isinstance(fps_value, int)
            assert fps_value > 0

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_font_system_font_loaded(self, mock_state_manager_class, mock_pygame):
        """E2E test: pygame font system font is loaded for rendering"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - SysFont should be called with Comic Sans
        mock_pygame.font.SysFont.assert_called_once()
        call_args = mock_pygame.font.SysFont.call_args[0]
        assert call_args[0] == 'Comic Sans'
        assert call_args[1] == 25  # size
        assert call_args[2] is True  # bold
        assert call_args[3] is False  # italic

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_window_caption_set(self, mock_state_manager_class, mock_pygame):
        """E2E test: game window caption is set to Code^3 Tetris"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert
        mock_pygame.display.set_caption.assert_called_once_with("Code^3 Tetris")

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_loop_exits_gracefully(self, mock_state_manager_class, mock_pygame):
        """E2E test: game exits cleanly when state manager returns False"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False

        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - pygame.quit should be called at exit
        mock_pygame.quit.assert_called_once()
        # Only one iteration since update returns False immediately
        assert mock_state_manager_instance.update.call_count == 1

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_counter_increments_with_real_config_level(self, mock_state_manager_class, mock_pygame):
        """E2E test: counter increments based on real Config level value"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - check the config object passed to state manager
        call_args = mock_state_manager_class.call_args[0]
        config = call_args[0]
        # Default level is 1, so counter should be 3 (1+1+1)
        assert config.counter == 3
        assert config.level >= 1

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_pygame_display_flipped_each_frame(self, mock_state_manager_class, mock_pygame):
        """E2E test: pygame display is flipped (refreshed) each frame"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.side_effect = [True, True, True, False]
        mock_state_manager_class.return_value = mock_state_manager_instance

        # Execute
        run_game()

        # Assert - display.flip should be called once per loop iteration (4 times)
        assert mock_pygame.display.flip.call_count == 4

    @patch('tetris.new_code.tetris_game.main.game.pygame')
    @patch('tetris.new_code.tetris_game.main.game.EnhancedStateManager')
    def test_e2e_game_components_dependency_injection(self, mock_state_manager_class, mock_pygame):
        """E2E test: game components are properly injected with dependencies"""
        # Setup
        mock_state_manager_instance = Mock()
        mock_state_manager_instance.update.return_value = False
        mock_state_manager_class.return_value = mock_state_manager_instance

        mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = mock_screen

        # Execute
        run_game()

        # Assert - verify dependency chain
        # 1. Config is created
        call_args = mock_state_manager_class.call_args[0]
        config = call_args[0]
        assert config is not None
        
        # 2. Input is created with config
        input_obj = call_args[1]
        assert input_obj.config == config
        
        # 3. Renderer is created with screen
        renderer = call_args[2]
        assert renderer.screen == mock_screen
        
        # 4. StateManager is created with all three
        assert mock_state_manager_class.call_count == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
