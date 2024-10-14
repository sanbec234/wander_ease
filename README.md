# Travel Planner with Google Maps API

This project is a travel planning web application that generates optimal itineraries for a chosen destination. The app integrates the Google Maps API to calculate distances, travel times, and hotel recommendations while scraping attraction information from Holidify.

## Features
- **Place Autocomplete**: Uses Google Maps API to auto-complete place names for attractions and hotels.
- **Distance Calculation**: Fetches distance and travel time between attractions.
- **Itinerary Planning**: Plans optimal travel routes based on ratings and proximity.
- **Hotel Recommendation**: Scrapes hotel data from Holidify and ranks them by rating.
- **Optimized Waypoints**: Uses Google Maps API to optimize the order of waypoints for a more efficient itinerary.
- **Custom Budget Options**: Allows users to choose hotel options based on their budget (Luxurious, Premium, Affordable).

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Flask templates)
- **APIs**: 
  - Google Maps API (Distance Matrix, Places, Directions)
  - Holidify (for scraping attraction and hotel data)
- **Data Parsing**: BeautifulSoup (for scraping HTML content)

## Setup Instructions

### Prerequisites
- Python 3.x
- Flask
- `requests` library
- `googlemaps` library
- `beautifulsoup4` library

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/travel-planner.git
    cd travel-planner
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Google Maps API Key**:
    - Obtain a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/).
    - Replace the placeholder API key (`'abcdefghijksadiq'`) in the code with your actual API key.

4. **Run the Flask Application**:
    ```bash
    python app.py
    ```

5. **Access the Application**:
    - Open your browser and navigate to `http://localhost:8884`.

## API Endpoints

- **GET /**: Renders the home page.
- **GET /startPlan**: Renders the form to enter destination details.
- **POST /handle_data**: Accepts user input and processes the travel plan.
- **GET /spots**: Returns the optimized travel itinerary.

## Usage

1. Open the homepage.
2. Enter the destination, budget type (Luxurious, Premium, or Affordable), and the number of days for the trip.
3. The app will generate an optimal itinerary based on the attractions and hotels in the destination.
4. View the final itinerary on the `spots` page.

## Example Workflow

1. **Start Planning**: 
   - Visit `/startPlan` and enter:
     - Destination: e.g., "Paris"
     - Tour Budget: e.g., "Premium"
     - Number of Days: e.g., "3"
   
2. **View Itinerary**: 
   - The app will generate an itinerary that includes attractions grouped by proximity and hotel recommendations. 
   - The optimized plan will be displayed on the `/spots` page.

## Screenshots

_Include screenshots of your app here, showing the homepage, itinerary plan, etc._

## Contributing

If you would like to contribute to this project, please create a fork, make your changes, and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
