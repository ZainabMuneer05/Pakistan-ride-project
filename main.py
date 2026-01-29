import random
import time
from linked_list import LinkedList
from rollback import RollbackManager
from city_graph import City
from driver import Driver
from rider import Rider

class RideApp:
    def __init__(self):
        self.city = City()
        self.drivers = LinkedList()
        self.rollback = RollbackManager()
        self.helpline_number = "15"
        # Driver names list for realism
        self.driver_names = ["Ali", "Ahmed", "Usman", "Hamza", "Bilal", "Zubair", "Omar", "Hassan", "Zaid"]
        self.pak_cities_data = {
            "Karachi": 0, "Hyderabad": 160, "Sukkur": 460, "Larkana": 520, 
            "Rohri": 470, "Multan": 820, "Bahawalpur": 900, "RahimYarKhan": 760, 
            "DGKhan": 880, "Faisalabad": 1050, "Sahiwal": 980, "Okara": 1010, 
            "Lahore": 1150, "Gujranwala": 1200, "Sialkot": 1230, "Gujrat": 1210, 
            "Jhelum": 1260, "Islamabad": 1350, "Rawalpindi": 1360, "Attock": 1400, 
            "Peshawar": 1500, "Mardan": 1470, "Swabi": 1440, "Abbottabad": 1460, 
            "Mansehra": 1500, "Swat": 1550, "Dir": 1600, "Chitral": 1700, 
            "Gilgit": 1850, "Skardu": 1950, "Hunza": 2000, "Muzaffarabad": 1450, 
            "Mirpur": 1420, "Kotli": 1400, "Bhimber": 1380, "Quetta": 1300, 
            "Zhob": 1150, "Loralai": 1180, "Khuzdar": 900, "Turbat": 600, 
            "Gwadar": 450, "Panjgur": 700, "Thatta": 100, "Badin": 140, 
            "Umerkot": 260, "Tharparkar": 300, "Jacobabad": 480, "Kashmore": 500, 
            "Chaman": 1200
        }
        self._setup_map()

    def _setup_map(self):
        city_list = list(self.pak_cities_data.keys())
        for i in range(len(city_list) - 1):
            u, v = city_list[i], city_list[i+1]
            dist = abs(self.pak_cities_data[v] - self.pak_cities_data[u])
            self.city.add_road(u, v, dist)
        
        # Adding drivers with names instead of just IDs
        for i in range(len(self.driver_names)):
            d = Driver(i+1, random.choice(city_list), random.choice(["Bike", "Mini", "AC_Car"]))
            d.name = self.driver_names[i] # Assigning name to driver object
            self.drivers.add(d)

    def display_available_cities(self):
        print("\n" + "="*80)
        print("                      AVAILABLE CITIES IN PAKISTAN")
        print("="*80)
        cities = sorted(list(self.pak_cities_data.keys()))
        for i in range(0, len(cities), 4):
            row = cities[i:i+4]
            line = "".join(["{:<20}".format(city) for city in row])
            print(line)
        print("="*80)

    def run(self):
        print("\n--- PAKISTAN RIDE APP ---")
        name = input("Enter Name: ")
        while True:
            try:
                bal = float(input("Enter Balance: "))
                break
            except ValueError:
                print("❌ Invalid balance!")
        rider = Rider(name, bal)
        
        while True:
            print(f"\n[ USER: {rider.name} | WALLET: {rider.wallet:.2f} PKR ]")
            print("1. Book Ride")
            print("2. Call Helpline ")
            print("3. File Complaint")
            print("4. Driver Rankings")
            print("5. Rollback Last Trip")
            print("6. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                self.display_available_cities()
                p = input("\nEnter Pickup City: ").strip().title()
                d = input("Enter Dropoff City: ").strip().title()
                
                if p in self.city.locations and d in self.city.locations:
                    path, dist = self.city.get_shortest_path(p, d)
                    print("\n--- Select Your Vehicle Type ---")
                    print("Total Distance: ", dist)
                    print(f"1. Bike    (Rate: 10 PKR/km) (Expected: {10*dist})")
                    print(f"2. Mini    (Rate: 20 PKR/km) (Expected: {20*dist})")
                    print(f"3. AC_Car  (Rate: 40 PKR/km) (Expected: {40*dist})")
                    v_choice = input("Enter Choice (1/2/3): ")
                    
                    rate, v_name, speed = (10, "Bike", 40) if v_choice == "1" else (40, "AC_Car", 60) if v_choice == "3" else (20, "Mini", 50)
                    
                    available_drivers = [dr for dr in self.drivers.traverse() if dr.vehicle == v_name]
                    selected_driver = random.choice(available_drivers) if available_drivers else random.choice(list(self.drivers.traverse()))
                    
                    print(f"\n✅ Your Nearest Driver: {selected_driver.name} is available!")
                    
                    fare = dist * rate
                    eta_minutes = int((dist / speed) * 60)
                    
                    print(f"Distance: {dist} km | ETA: {eta_minutes} mins | Total Fare: {fare} PKR")
                    
                    if rider.wallet >= fare:
                        confirm = input("Confirm booking? (y/n): ")
                        if confirm.lower() == 'y':
                            print("\n⏳ Finding your driver...")
                            time.sleep(1)
                            print(f"🚗 {v_name} assigned! {selected_driver.name} is arriving in 2 minutes...")
                            time.sleep(3.5)
                            print(f"📍 {selected_driver.name} has arrived at your location.")
                            time.sleep(2)
                            print(f"🚀 Your ride has started...")
                            time.sleep(2)
                            
                            print("\n✅ You have reached your destination!")
                            
                            # --- Payment Selection & Summary ---
                            print("\n--- Payment Method ---")
                            print("1. Cash")
                            print("2. Online Pay (JazzCash/EasyPaisa)")
                            p_choice = input("Select Option (1/2): ")
                            
                            # Billing and Route Summary
                            print("\n" + "*"*40)
                            print("           RIDE BILL SUMMARY")
                            print("*"*40)
                            print(f"Driver Name   : {selected_driver.name}")
                            print(f"Pickup        : {p}")
                            print(f"Dropoff       : {d}")
                            print(f"Route Taken   : {' -> '.join(path)}")
                            print(f"Total Fare    : {fare} PKR")
                            
                            if p_choice == "2":
                                rider.wallet -= fare
                                print(f"Payment Mode  : Online")
                                print("JazzCash/EP   : 03012345678")
                            else:
                                print(f"Payment Mode  : Cash")
                            
                            print(f"New Wallet Bal: {rider.wallet:.2f} PKR")
                            print("*"*40)
                            
                            self.rollback.push({"rider": rider, "fare": fare if p_choice == "2" else 0})
                            
                            print("\n" + "-"*30)
                            rating = input("Please rate our service out of 5 stars: ")
                            print(f"Thank you for giving {rating} stars!")
                            
                            time.sleep(2)
                            print("\n✨ BEST WISHES FROM PAKISTAN RIDE SERVICE! ✨")
                            print("Have a wonderful day and stay safe! 😊")
                            print("-" * 30)
                    else:
                        print("❌ Insufficient Balance!")
                else:
                    print("❌ Error: City name not found.")

            elif choice == "2":
                print(f"\n📞 Calling Helpline: {self.helpline_number}...")
            elif choice == "3":
                input("\nEnter complaint: ")
                print(f"✅ Registered. ID: {random.randint(100,999)}")
            elif choice == "4":
                print("\n--- Rankings ---")
                for dr in self.drivers.traverse():
                    print(f"Driver {dr.name}: {dr.rating:.1f} ⭐")
            elif choice == "5":
                last = self.rollback.undo()
                if last:
                    if last['fare'] > 0: last['rider'].wallet += last['fare']
                    print(f"✅ Rollback Successful! {last['fare']} PKR Refunded.")
                else: 
                    print("❌ No trips found.")
            elif choice == "6":
                print("\n" + "="*40)
                print("🌟 Thank you for using Pakistan Ride App! 🌟")
                print("🙏 Allah Hafiz! See you again soon.")
                print("="*40)
                break

if __name__ == "__main__":
    RideApp().run()