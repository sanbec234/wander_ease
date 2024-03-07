import googlemaps
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

global_optimal_plan = None

def tem(place,max_price,no_of_days):
  def check_get_travel_time(origin, destination):
      url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
      response = requests.get(url)
      data = response.json()
      if data['status'] == 'OK':
          return "OK"
      else:
          # print("Error:", data['status'])
          # print(f"{origin}->{destination}")
          return "ZERO_RESULTS"

  def get_distance(origin, destination, api_key):
      url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origin}&destinations={destination}&key={api_key}"
      response = requests.get(url)
      data = response.json()
      # Check if response status is OK
      if  data["rows"][0]["elements"][0]["status"] == "OK":
          # distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
          distance_value = data["rows"][0]["elements"][0]["distance"]["value"]
          return distance_value
      # distance_text, 
      else:
          return None

  # print("enter 1 for city \n 2 for state\n")
  search_type = 1


  if search_type==1:
    url = "https://www.holidify.com/places/"+place+"/sightseeing-and-things-to-do.html"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    rarr=[]
    for ob in soup.find_all(attrs={"class":'card-heading'}):
        rarr.append(ob.text)
        # print(ob.text)
    # print(rarr)
  if search_type==2:
    
    url = "https://www.holidify.com/country/"+place+"/places-to-visit.html"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    rarr=[]
    for ob in soup.find_all(attrs={"class":'card-heading'}):
        rarr.append(ob.text)
        # print(ob.text)
    # print(rarr)
  # Initialize Google Maps API client
  locations_cleaned = [location.split('. ')[1] for location in rarr]

  # Add ',tuticorin' to each location
  locations_with_place = [location + ',' + place for location in locations_cleaned]
  api_key = 'abcdefghijksadiq'
  gmaps = googlemaps.Client(key=api_key)

  # List of location names
  location_names = locations_with_place
  # print("\n\n\n orginal location")
  # print(location_names)

  place_loc=[]

  place_loc.append(place)

  def rm (location):
    
      url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={place}&destinations={location}&key={api_key}"
      response = requests.get(url)
      data = response.json()
      if(data['destination_addresses']==data['origin_addresses']):
          return location.split(',')[0]
      return location

  def autocomplete_location(keyword):
      try:
          # Perform a place autocomplete request
          autocomplete_result = gmaps.places_autocomplete(input_text=keyword)

          # Extract location suggestions
          predictions = [result['description'] for result in autocomplete_result]
          url = f"https://maps.googleapis.com/maps/api/directions/json?origin={predictions[0]}&destination={place}&key={api_key}"
          response = requests.get(url)
          data = response.json()
          if data['status'] == 'OK':
              return predictions[0]
          return "ZERO_RESULTS"
      except Exception as e:
          return None


  for i,loc in enumerate(location_names):
      location_names[i] = autocomplete_location(loc)
      if location_names[i] == None:
          location_names[i] = rm (loc)
  # print(location_names)


  def get_place_rating(place_name):
      # Perform Places API request to get place details
      place = gmaps.places(query=place_name)['results']
      if place:
          return place[0].get('rating', 0)
      return 0

  # Sort places by rating
  sorted_places = sorted(location_names, key=lambda x: get_place_rating(x), reverse=True)

  location_names = sorted_places
  # print("location names \n\n")
  # print(sorted_places)

  # Group locations within a specified radius
  def group_locations_within_radius(locations, radius):
      grouped_locations = {}
      visited = set()
      
      # Helper function to find nearby locations
      def find_nearby_locations(location_index):
          nearby_locations = []
          location = locations[location_index]
          for idx, other_location in enumerate(locations):
              if idx != location_index and idx not in visited:
                  distance = get_distance(location, other_location, 'abcdefghijksadiq')
                  # distance = gmaps.distance_matrix(location, other_location)['rows'][0]['elements'][0]['distance']['value']  # Distance in meters
                  # # print(location + "->" + other_location +" "+str(distance))
                  if(distance==None):
                      continue
                  if distance <= radius * 1000:  # Convert radius from km to meters
                      nearby_locations.append(idx)
                      visited.add(idx)
          return nearby_locations
      
      # Loop over all locations
      for i, _ in enumerate(locations):
          if i not in visited:
              nearby_locations = find_nearby_locations(i)
              grouped_locations[i] = [i] + nearby_locations
      
      return grouped_locations

  # Specify the radius in kilometers
  radius = 10

  # Group locations within the specified radius
  grouped_locations = group_locations_within_radius(location_names, radius)
  # print(grouped_locations)
  # Output the grouped locations
  # for parent_index, group in grouped_locations.items():
  #     # print(f"Parent location: {location_names[parent_index]}")
  #     # print(f"Nearby locations within {radius} km radius:")
  #     for idx in group[1:]:
  #         # print(f"\t{location_names[idx]}  : {get_distance(location_names[parent_index], location_names[idx], 'abcdefghijksadiq')}")

  #     # print()


  # hotels.py






  def get_sorted_hotels(max_price):
    if search_type == 1:
        
        url = "https://www.holidify.com/places/" + place + "/hotels-where-to-stay.html"
    elif search_type == 2:
        
        url = "https://www.holidify.com/country/" + place + "/hotels-where-to-stay.html"
    else:
        # print("Invalid choice!")
        exit()

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    def get_place_rating(place_name, api_key):
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=name,rating&key={api_key}'
        response = requests.get(url)
        data = response.json()
        if 'candidates' in data and len(data['candidates']) > 0 and 'rating' in data['candidates'][0]:
            return data['candidates'][0]['rating']
        return None



    def get_distance(origin, destination):
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data["status"] == "OK":
            distance = data["routes"][0]["legs"][0]["distance"]["value"]  # Distance in meters
            return distance
        else:
            # print("Error:", data["status"])
            return None


    def sort_places_by_rating(places, api_key):
        ratings = {}
        for place_name in places:
            place_name_str=place_name['place']+','+place
            rating = get_place_rating(place_name_str, api_key)
            if rating is not None:
                ratings[place_name_str] = rating
        sorted_places = sorted(ratings.keys(), key=lambda x: ratings[x], reverse=True)

        return sorted_places



    # Your Google API key


    # Extract hotel names1
    rarr = [ob.text.strip() for ob in soup.find_all(attrs={"class": "card-heading"})]

    # Extract prices
    # parr = [int(ob.text.strip().replace('₹', '').replace(',', '')) for ob in soup.find_all(attrs={"class": "price default"})]

    parr = []
    for ob in soup.find_all(attrs={"class": "price default"}):
        price_text = ob.text.strip().replace(',', '')
        if '₹' in price_text:
            price = int(price_text.replace('₹', ''))/82
        elif '$' in price_text:
            price = int(price_text.replace('$', ''))
        else:
            continue
        parr.append(price)
        

    # Combine hotel names and prices into a dictionary
    hotel_prices = [{'place': place, 'price': price} for place, price in zip(rarr, parr)]

    # Get the maximum price from the user
    

    # Filter hotels based on maximum price
    filtered_hotels = [{'place': hotel['place'], 'price': hotel['price']} for hotel in hotel_prices if hotel['price'] <= max_price]
    place_to_price_dict = {hotel['place']: hotel['price'] for hotel in filtered_hotels}
    # Print the filtered hotels
    # # print(filtered_hotels)
    sorted_hotels_fin=[]

    if filtered_hotels:
        sorted_hotels = sort_places_by_rating(filtered_hotels, api_key)
        # # print(sorted_hotels)
        for hotel in sorted_hotels:

            name=hotel.split(',')[0]
            print_name = name.split('.', 1)[-1]
            sorted_hotels_fin.append(print_name)

    return sorted_hotels_fin


  def get_distance_hotel(origin, destination):
      url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
      response = requests.get(url)
      data = response.json()
      
      if data["status"] == "OK":
          distance = data["routes"][0]["legs"][0]["distance"]["value"]  # Distance in meters
          return distance
      else:
          # print("Error:", data["status"])
          return None
  sorted_hotels_fin = get_sorted_hotels(max_price)

  for index,i in enumerate(sorted_hotels_fin):
    sorted_hotels_fin[index] = autocomplete_location(i)

  if "ZERO_RESULTS" in sorted_hotels_fin:
    sorted_hotels_fin.remove("ZERO_RESULTS")

  def get_hotel(location):
      for threshold in range(10,20,5):
          for hotel in sorted_hotels_fin:
              dis =get_distance_hotel(hotel,location)
              # print(dis)
              if(dis==None):
                continue
              if dis<threshold*1000:
                  return hotel
      return "NULL"













  #cas.py
  def get_place_rating(place_name):
      # Perform Places API request to get place detailsp
      place = gmaps.places(query=place_name)['results']
      if place:
          return place[0].get('rating', 0)
      return 0


  extracted_locations = [location_names[index] for index in grouped_locations.keys()]

  # print(extracted_locations)

  node_order = sorted(extracted_locations, key=lambda x: get_place_rating(x), reverse=True)

  # print(node_order)


  node_val=[]

  for parent_index, group in grouped_locations.items():
      tem = []
      for idx in group:
          tem.append(location_names[idx])
      node_val.append(tem)

  # print(node_val)
  hotel = "Hôtel Geetha Internation,Tuticorin"

  def get_travel_time(origin, destination):
      url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
      response = requests.get(url)
      data = response.json()
      if data['status'] == 'OK':
          # Extract travel time in seconds
          travel_time_seconds = data['routes'][0]['legs'][0]['duration']['value']
          # Convert travel time to minutes
          travel_time_minutes = travel_time_seconds / 60
          return travel_time_minutes
      else:
          # print("Error:", data['status'])
          # print(f"{origin}->{destination}")
          return 1


  def flatten_2d_to_1d(arr_2d):
      arr_1d = []
      for row in arr_2d:
          arr_1d.extend(row)
      return arr_1d

  # Example 2D array

  # Convert to 1D array
  arr_1d = flatten_2d_to_1d(node_val)

  # print(arr_1d)
  if "ZERO_RESULTS" in arr_1d:
    arr_1d.remove("ZERO_RESULTS")
  hotel = get_hotel(arr_1d[0])



  def doplan(all_day,hotel):
    days=0
    plan=[]
    end_place=0
    while True:
      tem_distance =get_distance(arr_1d[end_place],hotel,api_key)
      if tem_distance!=None:
        if tem_distance>20:
          tem_hotel = get_hotel(arr_1d[end_place])
        if tem_hotel!="NULL":
          hotel=get_hotel(arr_1d[end_place])
      day_time_spent=0
      curr=end_place
      if days==all_day:
        return plan
      day_plan=[]
      day_plan.append(hotel)
      while True:
        day_plan.append(arr_1d[curr])
        day_time_spent+=2
        if day_time_spent>=10:
          end_place=curr+1
          days+=1
          plan.append(day_plan)
          ## print(day_plan)
          break
        if curr>=len(arr_1d)-1:
          return plan
        day_time_spent+=get_travel_time(arr_1d[curr],arr_1d[curr+1])/60
        # print('day:',days,'from ',arr_1d[curr],' to',arr_1d[curr+1],' time ',get_travel_time(arr_1d[curr],arr_1d[curr+1]))
        curr=curr+1
        

  try:
      full_plan=doplan(no_of_days,hotel)
  except IndexError:
              pass
              # print(f"Index out of bounds exception occurred. not enough places to plan for {no_of_days} days ")
              
  # for plan in full_plan:
    # print(plan)
  def get_opt_plan(way,orgin,dest):
    directions = gmaps.directions(origin=orgin,
                                  destination=dest,
                                  waypoints=way,
                                  optimize_waypoints=True,  # Optimize the order of waypoints
                                  mode="driving")

    # Extract the optimized order of waypoints
    optimized_waypoint_order = directions[0]['waypoint_order']

    # Create a list of places in the optimized order
    ordered_places = [way[i] for i in optimized_waypoint_order]
    ordered_places.append(dest)
    return ordered_places

  optimal_plan = []


  for index,plan in enumerate(full_plan):
    if index+1<len(full_plan):
      optimal_plan.append(get_opt_plan(plan,plan[0],full_plan[index+1][0]))
    else:
      optimal_plan.append(get_opt_plan(plan,plan[0],full_plan[index][0]))

  global global_optimal_plan
  global_optimal_plan = optimal_plan
  
#   for plan in optimal_plan:
#     # print(plan)
  return optimal_plan


# print(global_optimal_plan)

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("home_page.html")

@app.route("/startPlan")
def startPlan():
    return render_template("enter_details.html")

@app.route("/handle_data", methods=["POST"])
def handle_data():
    place = request.json['destination'].lower()
    tour_budget = request.json['tourBudget']
    no_of_days = int(request.json["numDays"])
    switcher = {
        "Luxurious": "500",  # Define the maximum price for Luxurious option
        "Premium": "250",    # Define the maximum price for Premium option
        "Affordable": "100", # Define the maximum price for Affordable option
    }
    max_price = switcher[tour_budget]
    return tem(place, int(max_price), no_of_days)

def get_spots():
    # Assuming global_optimal_plan is defined somewhere in your code
    return global_optimal_plan

@app.route('/spots')
def spots():
    spots_data = get_spots()
    return render_template('secpage.html', itinerary_data=spots_data)

if __name__ == "__main__":
    app.run(debug=True, port=8884)