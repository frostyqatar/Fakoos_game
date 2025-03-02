from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import time

def automate_game_setup():
    print("🎮 Starting Fakoos Trivia automation with Selenium...")
    
    # Initialize the WebDriver (Chrome in this example)
    driver = webdriver.Chrome()
    
    try:
        # Open the game HTML file (adjust path as needed)
        driver.get("C:\\Users\\provo\\Documents\\Fakoos_game\\fakoos-trivia-game-code.html")
        
        # Wait longer for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "setup-screen"))
        )
        
        print("Initial screen loaded successfully")
        
        # 1. Select 3 random categories
        print("📋 Selecting categories...")
        # Wait for categories to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "category-item"))
        )
        
        categories = driver.find_elements(By.CLASS_NAME, "category-item")
        print(f"Found {len(categories)} categories")
        
        if len(categories) < 3:
            print("Not enough categories found!")
            return
        
        # Select 3 random categories
        selected_indices = random.sample(range(len(categories)), 3)
        for index in selected_indices:
            categories[index].click()
            time.sleep(0.5)  # Give time for the click to register
            try:
                category_text = categories[index].text.strip()
                print(f"Selected category: {category_text}")
            except:
                print(f"Selected category at index {index}")
        
        # 2. Process Team 1 setup
        print("👥 Setting up Team 1...")
        
        # Find Team 1 container
        team1_container = driver.find_elements(By.CSS_SELECTOR, ".team-setup-container")[0]
        
        # Set team name (first input in the container)
        team1_name_input = team1_container.find_element(By.CSS_SELECTOR, ".team-name-input")
        team1_name_input.clear()
        team1_name_input.send_keys("Super Stars")
        print("Set team 1 name")
        
        # Add players to Team 1
        team1_players = ["Ahmed", "Fatima", "Mohammed", "Aisha", "Omar", "Layla", "Youssef", "Noor"]
        
        # First, fill in the existing player inputs (container starts with 2)
        player_inputs = team1_container.find_elements(By.CSS_SELECTOR, ".player-input")
        for i, input_field in enumerate(player_inputs):
            if i < len(team1_players):
                input_field.clear()
                input_field.send_keys(team1_players[i])
                print(f"Added initial player {team1_players[i]} to team 1")
        
        # Then add remaining players by clicking the add button
        add_player_button = team1_container.find_element(By.XPATH, ".//button[contains(text(), 'إضافة لاعب')]")
        
        # Start from where we left off with the existing inputs
        for i in range(len(player_inputs), len(team1_players)):
            # Click add player button
            add_player_button.click()
            time.sleep(0.5)  # Wait for new input to appear
            
            # Find the newly added input (it will be the last one)
            new_inputs = team1_container.find_elements(By.CSS_SELECTOR, ".player-input")
            if len(new_inputs) > i:
                new_input = new_inputs[-1]  # Get the last input
                new_input.clear()
                new_input.send_keys(team1_players[i])
                print(f"Added new player {team1_players[i]} to team 1")
            else:
                print(f"❌ Failed to add player {team1_players[i]} - no input field found")
        
        # 3. Process Team 2 setup
        print("👥 Setting up Team 2...")
        
        # Find Team 2 container
        try:
            team2_container = driver.find_elements(By.CSS_SELECTOR, ".team-setup-container")[1]
            
            # Set team name (first input in the container)
            team2_name_input = team2_container.find_element(By.CSS_SELECTOR, ".team-name-input")
            team2_name_input.clear()
            team2_name_input.send_keys("Mega Minds")
            print("Set team 2 name")
            
            # Add players to Team 2
            team2_players = ["Ali", "Sara", "Hassan", "Mariam", "Khalid", "Zainab", "Ibrahim", "Hala"]
            
            # First, fill in the existing player inputs (container starts with 2)
            player_inputs = team2_container.find_elements(By.CSS_SELECTOR, ".player-input")
            for i, input_field in enumerate(player_inputs):
                if i < len(team2_players):
                    input_field.clear()
                    input_field.send_keys(team2_players[i])
                    print(f"Added initial player {team2_players[i]} to team 2")
            
            # Then add remaining players by clicking the add button
            add_player_button = team2_container.find_element(By.XPATH, ".//button[contains(text(), 'إضافة لاعب')]")
            
            # Start from where we left off with the existing inputs
            for i in range(len(player_inputs), len(team2_players)):
                # Click add player button
                add_player_button.click()
                time.sleep(0.5)  # Wait for new input to appear
                
                # Find the newly added input (it will be the last one)
                new_inputs = team2_container.find_elements(By.CSS_SELECTOR, ".player-input")
                if len(new_inputs) > i:
                    new_input = new_inputs[-1]  # Get the last input
                    new_input.clear()
                    new_input.send_keys(team2_players[i])
                    print(f"Added new player {team2_players[i]} to team 2")
                else:
                    print(f"❌ Failed to add player {team2_players[i]} - no input field found")
                    
        except Exception as e:
            print(f"⚠️ Error setting up team 2: {e}")
        
        # 4. Start the game
        print("🎲 Starting the game...")
        time.sleep(2)  # Longer delay before clicking
        
        # Try to find and click the start game button
        try:
            # Try by class and text
            start_button = driver.find_element(By.CSS_SELECTOR, ".button.submit-btn")
            start_button.click()
            print("✅ Clicked start game button")
        except NoSuchElementException:
            try:
                # Try by text content
                start_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'ابدأ اللعبة')]")
                if start_buttons:
                    start_buttons[0].click()
                    print(f"✅ Clicked start game button by text: '{start_buttons[0].text}'")
                else:
                    print("❌ Could not find start game button by text")
                    setup_screen = driver.find_element(By.CLASS_NAME, "setup-screen")
                    all_buttons = setup_screen.find_elements(By.TAG_NAME, "button")
                    print(f"Found {len(all_buttons)} buttons in setup screen")
                    for i, btn in enumerate(all_buttons):
                        print(f"Button {i}: '{btn.text}'")
                        if i == len(all_buttons) - 1:  # Last button in setup screen
                            btn.click()
                            print("Clicked last button in setup screen")
            except Exception as inner_e:
                print(f"⚠️ Error finding start button: {inner_e}")
        
        # Wait to see the game board
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "game-board"))
        )
        print("✅ Game board loaded successfully")
        
        # Login complete - leave the browser open
        print("✅ Setup complete! Browser will remain open.")
        input("Press Enter to close the browser window...")
        
    except Exception as e:
        print(f"⚠️ Error: {e}")
        
    finally:
        # Close the browser when user hits Enter
        driver.quit()

if __name__ == "__main__":
    automate_game_setup()
