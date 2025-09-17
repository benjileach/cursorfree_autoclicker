import pyautogui
import time
import keyboard
import os
from pathlib import Path

# Configure pyautogui for safety adnd change stuff 
pyautogui.FAILSAFE = True  # Move mouse to corner to stop
pyautogui.PAUSE = 0.1

class SimpleDesktopClicker:
    def __init__(self):
        self.button_image = None
        self.clicking = False
    
    def capture_button(self):
        """Step-by-step button capture"""
        print("=== BUTTON CAPTURE ===")
        print("1. Open your desktop application")
        print("2. Make sure the button you want to click is visible")
        print("3. Position your mouse EXACTLY over the button")
        print("4. Press SPACE to capture the button")
        print("5. Press ESC to cancel")
        print("\nWaiting for you to position mouse...")
        
        while True:
            if keyboard.is_pressed('space'):
                # Get mouse position
                x, y = pyautogui.position()
                print(f"Capturing button at position: ({x}, {y})")
                
                # Take screenshot of button area (larger area for better recognition)
                try:
                    # Capture 100x50 pixel area around mouse
                    screenshot = pyautogui.screenshot(region=(x-50, y-25, 100, 50))
                    
                    # Save the button image
                    button_path = "desktop_button.png"
                    screenshot.save(button_path)
                    self.button_image = button_path
                    
                    print(f"✓ Button captured and saved as: {button_path}")
                    print("You can now test clicking this button!")
                    return True
                    
                except Exception as e:
                    print(f"Error capturing button: {e}")
                    return False
                    
            elif keyboard.is_pressed('esc'):
                print("Capture cancelled")
                return False
                
            time.sleep(0.1)
    
    def test_single_click(self):
        """Test clicking the button once"""
        if not self.button_image or not Path(self.button_image).exists():
            print("❌ No button image found. Please capture a button first!")
            return False
        
        print("Testing single click...")
        
        # Store current mouse position
        original_pos = pyautogui.position()
        
        try:
            # Find button on screen
            button_location = pyautogui.locateOnScreen(self.button_image, confidence=0.8)
            
            if button_location:
                # Get center of button
                button_center = pyautogui.center(button_location)
                print(f"✓ Button found at: {button_center}")
                
                # Click the button
                pyautogui.click(button_center)
                
                # Restore mouse position
                pyautogui.moveTo(original_pos)
                
                print("✓ Button clicked successfully!")
                return True
            else:
                print("❌ Button not found on screen")
                print("Troubleshooting tips:")
                print("- Make sure your application is visible")
                print("- Try capturing the button again")
                print("- Check if the button appearance has changed")
                return False
                
        except Exception as e:
            print(f"❌ Error during click: {e}")
            return False
    
    def start_auto_clicking(self, interval=2.0):
        """Start automatic clicking"""
        if not self.button_image or not Path(self.button_image).exists():
            print("❌ No button image found. Please capture a button first!")
            return
        
        print(f"🔄 Starting auto-click every {interval} seconds...")
        print("🛑 Press 'Q' to stop, or move mouse to top-left corner")
        print("📱 Make sure your desktop application stays visible!")
        
        self.clicking = True
        click_count = 0
        
        while self.clicking:
            # Check for stop conditions
            if keyboard.is_pressed('q'):
                print("\n🛑 Stopped by user (Q pressed)")
                break
            
            # Store current mouse position
            original_pos = pyautogui.position()
            
            try:
                # Find and click button
                button_location = pyautogui.locateOnScreen(self.button_image, confidence=0.8)
                
                if button_location:
                    button_center = pyautogui.center(button_location)
                    pyautogui.click(button_center)
                    click_count += 1
                    print(f"✓ Click #{click_count} at {button_center}")
                else:
                    print("⚠️ Button not found, skipping click")
                
                # Restore mouse position
                pyautogui.moveTo(original_pos)
                
            except pyautogui.FailSafeException:
                print("\n🛑 Stopped by failsafe (mouse moved to corner)")
                break
            except Exception as e:
                print(f"❌ Error during auto-click: {e}")
            
            # Wait before next click
            time.sleep(interval)
        
        self.clicking = False
        print(f"\n✅ Auto-clicking stopped. Total clicks: {click_count}")

def main():
    """Main menu for desktop app clicking"""
    clicker = SimpleDesktopClicker()
    
    print("🖱️  DESKTOP APPLICATION AUTO CLICKER")
    print("=" * 40)
    
    while True:
        print(f"\nCurrent button: {'✓ Ready' if clicker.button_image else '❌ Not set'}")
        print("\nOptions:")
        print("1. 📸 Capture Button")
        print("2. 🎯 Test Single Click") 
        print("3. 🔄 Start Auto-Clicking")
        print("4. 🛑 Stop Auto-Clicking")
        print("5. ❓ Help & Tips")
        print("6. 🚪 Exit")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == '1':
            print("\n" + "="*50)
            clicker.capture_button()
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            print("\n" + "="*50)
            clicker.test_single_click()
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            print("\n" + "="*50)
            try:
                interval = float(input("Click interval in seconds (default 2.0): ") or "2.0")
                if interval < 0.1:
                    print("Minimum interval is 0.1 seconds")
                    interval = 0.1
            except ValueError:
                interval = 2.0
                print("Using default interval: 2.0 seconds")
            
            clicker.start_auto_clicking(interval)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            clicker.clicking = False
            print("🛑 Auto-clicking will stop after current click")
            
        elif choice == '5':
            print("\n" + "="*50)
            print("💡 HELP & TIPS:")
            print("• Make sure your desktop app is always visible")
            print("• Capture a clear, unique part of the button") 
            print("• If clicks fail, try capturing the button again")
            print("• Test single click before starting auto-click")
            print("• Use reasonable intervals (1+ seconds) to avoid issues")
            print("• Move mouse to top-left corner for emergency stop")
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            clicker.clicking = False
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    print("Checking requirements...")
    
    try:
        import pyautogui
        import keyboard
        from PIL import Image
        print("✓ All requirements satisfied")
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please install: pip install pyautogui keyboard pillow")
        exit(1)
    

    main()
