🌍 World Recipe Studio
A beginner-friendly Python desktop app for exploring recipes from Nigeria and around the world. World Recipe Studio combines a clean, food-inspired interface with recipe search, food photography, ingredient lists, and step-by-step cooking instructions.
✨ Features
- Search recipes by dish name and related recipe details.
- Explore Nigerian food with built-in recipes such as Jollof Rice and Egusi Soup.
- Discover international dishes using TheMealDB API.
- Browse by country and category, including options such as Nigerian, pasta and rice, chicken, beef and grill, and seafood.
- View recipe details, including ingredients and preparation steps.
- See food photos on the home page, recipe cards, and recipe details.
- Save favourites so selected recipes can be revisited later.
- Try a surprise dish for a random recipe idea.
- Keep browsing offline with built-in recipes when the online API is unavailable.
- Use a polished desktop interface built with CustomTkinter.
🖥️ Built With
- Python — application logic
- CustomTkinter — desktop user interface
- Requests — requests to the online recipe API
- Pillow (PIL) — loading and displaying food images
- TheMealDB API — international recipe data
📦 Requirements
- Python 3.10 or newer is recommended.
- An internet connection is needed to search for online recipes and download online food photos.
- The app attempts to install these Python packages if they are missing:
  - customtkinter
  - requests
  - Pillow
🚀 Getting Started
1. Download the project
Clone the repository:
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
Or download the repository as a ZIP file from GitHub and extract it.
2. Open the project folder
Open a terminal or Command Prompt in the folder containing recipe app.py.
3. Run the app
python "recipe app.py"
On some systems, you may need to use:
python3 "recipe app.py"
The application will attempt to install its required packages the first time it runs if they are not already installed.
🍲 How to Use
1. Launch the application.
2. Browse the featured dishes or use the search box to look for a recipe.
3. Choose a country or quick category to narrow down the recipes.
4. Select a recipe to view its ingredients and preparation instructions.
5. Open the favourites section to revisit saved recipes.
6. Use the surprise-dish option when you want an idea for something different to cook.
💾 Favourites and Local Data
The app stores saved favourites in a file named favourites.json in the same folder as the Python script. This file is created or updated when favourites are saved.
🌐 Online Recipe Data
International recipes are retrieved from TheMealDB. The app also includes built-in Nigerian recipes, allowing some recipe browsing to continue when the online service is unavailable.

Online searches and images require an internet connection. If the API cannot be reached, the app may show built-in recipes instead.
📁 Project Structure
World-Recipe-Studio/
├── recipe app.py       # Main application
└── favourites.json     # Created when favourites are saved
favourites.json may not exist until you save a favourite.
🧠 What I Learned
This project is a practical way to explore real-world Python development, including:
- Building a desktop application with a graphical user interface.
- Organising recipe information using Python dictionaries and lists.
- Searching and filtering data.
- Connecting to a REST API and handling network errors.
- Working with images using Pillow.
- Saving and loading information using JSON.
- Running network tasks in background threads to keep the interface responsive.
🔧 Troubleshooting
The app does not open
- Check that Python is installed and available from your terminal.
- Run the command from the folder containing recipe app.py.
- Read any error message shown in the terminal.
Online recipes are not appearing
- Check your internet connection.
- TheMealDB may be temporarily unavailable. Try again later; built-in recipes may still be available.
Package installation fails
- Install the packages manually:
python -m pip install customtkinter requests Pillow
📜 Credits
- Recipe API: TheMealDB
- Built with Python and open-source libraries.
📌 Future Improvements
Possible future improvements include adding recipe ratings, dietary filters, adjustable serving sizes, and the ability to add custom recipes.
Thanks for checking out World Recipe Studio! 🍽️
