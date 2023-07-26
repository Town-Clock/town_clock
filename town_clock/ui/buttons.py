"""
buttons.py

Controls the logic of the buttons.

Author: Zack Hankin

Started: 27/02/2023
"""
from __future__ import annotations

from town_clock.util.clock_exceptions import ButtonError


class Buttons:
    """
    Class for controlling the button interface from user.
    
    Button name:
        - up
        - down
        - left
        - right
        - select 
    """
    def __init__(self, button_pins: dict[str, int]) -> None:
        """Class for controlling the button interface from user.

        Button name:
        - up
        - down
        - left
        - right
        - select
        
        Args:
            button_pins (dict[str, int]): The pin number of the raspbery pi this is button is connected to.

        Raises:
            ButtonError: If button name is not one of the 5 valid options.
        """
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.select = None
        self.button_names = ['up', 'down', 'left', 'right', 'select']
        
        for button_name in self.button_names:
            try:
                self.__dict__[button_name] = button_pins[button_name]
            except KeyError as error:
                raise ButtonError( 
                                  f"Invalid button name for {button_name}. "
                                  f"Ensure all 5 button names are correctly spelt."
                                  ) from error        
    
    def is_pressed(self) -> bool:
        """Flag for any button is pressed.

        Todo: is_pressed
        
        Returns:
            bool: A button is pressed.
        """
        ...

    def __str__(self) -> str:
        return str(self.button_values)
    
    def __repr__(self) -> str:
        return f"Buttons({', '.join(self.__dict__)})"
    
    def button_value(self, button: str) -> bool:
        """Button value
        
        Returns the value of a given button.
        
        Todo: button_value
        
        Args:
            button (str): Button name.

        Returns:
            bool: Current value of button.
        """
        return bool(0)

    @property
    def button_values(self) -> dict[str, bool]:
        ret_dict: dict[str, bool] = dict()
        for button in self.button_names:
            ret_dict[button] = self.button_value(button)
        return ret_dict

if __name__ == '__main__':
    print(Buttons({
        'up': 5,
        'dwn': 6,
        'left': 7,
        'right': 8,
        'select': 9,
    }))