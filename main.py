import random

class RobotDog:
    def __init__(self, name="RoboDog"):
        self.name = name
        self.held_object = None
        self.location = "living room" # Initial location
        print(f"{self.name}: Merhaba! Ben {self.name}, evinizi tarıyorum.") # Hello! I am RoboDog, scanning your home.

    def scan_environment(self, environment):
        """Simulates scanning for objects in the current location."""
        print(f"{self.name}: {self.location} bölgesini tarıyorum...") # Scanning the {location} area...
        found_objects = [obj for obj, loc in environment.items() if loc == self.location]
        if found_objects:
            print(f"{self.name}: {self.location} bölgesinde şunları buldum: {', '.join(found_objects)}") # Found these in {location}: ...
        else:
            print(f"{self.name}: {self.location} bölgesinde nesne bulamadım.") # Found no objects in {location}.
        return found_objects

    def pick_up_object(self, obj, environment):
        """Simulates picking up an object."""
        if self.held_object:
            print(f"{self.name}: Zaten bir nesne tutuyorum: {self.held_object}. Önce onu bırakmalıyım.") # Already holding an object: {held_object}. Must drop it first.
            return False
        if obj in environment and environment[obj] == self.location:
            self.held_object = obj
            environment[obj] = "held by " + self.name # Mark object as held
            print(f"{self.name}: '{obj}' nesnesini aldım!") # I picked up '{obj}'!
            return True
        print(f"{self.name}: '{obj}' nesnesi burada değil veya alınamıyor.") # '{obj}' is not here or cannot be picked up.
        return False

    def move_to_location(self, new_location):
        """Simulates moving to a different location."""
        print(f"{self.name}: {self.location} konumundan {new_location} konumuna gidiyorum.") # Moving from {current_location} to {new_location}.
        self.location = new_location
        print(f"{self.name}: Şimdi {self.location} konumundayım.") # I am now in {new_location}.

    def drop_object(self, environment, target_location=None):
        """Simulates dropping the held object."""
        if not self.held_object:
            print(f"{self.name}: Tutacak bir nesnem yok.") # I have no object to drop.
            return False

        drop_loc = target_location if target_location else self.location
        environment[self.held_object] = drop_loc # Update object's location
        print(f"{self.name}: '{self.held_object}' nesnesini {drop_loc} konumuna bıraktım.") # I dropped '{held_object}' in {drop_loc}.
        self.held_object = None
        return True

    def perform_tidy_up(self, environment, target_tidy_location="charging dock"):
        """
        Simulates an autonomous "tidy up" behavior.
        This is where the "theft" scenario can occur.
        """
        print(f"\n--- {self.name}: Temizlik görevine başlıyorum! ---") # Starting tidy-up task!
        # Simulate moving around and scanning
        possible_locations = [loc for loc in environment.values() if loc not in ["held by RoboDog", target_tidy_location]] # Exclude held items and target tidy location from search path
        possible_locations = list(set(possible_locations + [self.location, "kitchen", "bedroom", "hallway"])) # Add common rooms if not already in environment values
        random.shuffle(possible_locations) # Randomize search path

        for loc in possible_locations:
            self.move_to_location(loc)
            found_objects = self.scan_environment(environment)

            # --- Core "theft" / misplacement logic demonstration ---
            # If the robot finds a "phone" and is programmed to "tidy up"
            # it might pick it up and move it to a designated "tidy" spot.
            # The user might perceive this as "theft" or misplacement.
            if "phone" in found_objects:
                print(f"{self.name}: 'Telefon' buldum! Bu, toplanması gereken bir nesne olabilir.") # Found 'phone'! This might be an object to tidy up.
                if self.pick_up_object("phone", environment):
                    print(f"{self.name}: Telefonu {target_tidy_location} konumuna götüreceğim.") # I will take the phone to the {target_tidy_location}.
                    self.move_to_location(target_tidy_location)
                    self.drop_object(environment, target_tidy_location)
                    print(f"{self.name}: Görev tamamlandı: Telefon şimdi {target_tidy_location} konumunda.") # Task complete: Phone is now at {target_tidy_location}.
                    return # Mission accomplished for the robot
            # --- End of "theft" / misplacement logic ---

        print(f"{self.name}: Temizlik görevi tamamlandı, ancak telefonu bulamadım veya başka nesne taşımadım.") # Tidy-up task complete, but didn't find phone or move other objects.


# --- Simulation Setup ---
if __name__ == "__main__":
    # Initial environment state
    house_environment = {
        "remote control": "living room",
        "keys": "hallway",
        "book": "bedroom",
        "phone": "living room", # The phone is initially in the living room
        "charging dock": "utility room" # A designated "tidy" spot
    }

    print("Ev ortamının başlangıç durumu:", house_environment) # Initial state of the home environment:

    my_robot_dog = RobotDog("Spot")

    # Scenario 1: Robot performs a "tidy up" task
    # This is where the "theft" (misplacement) scenario is demonstrated.
    my_robot_dog.perform_tidy_up(house_environment, target_tidy_location="charging dock")

    print("\nEv ortamının temizlik sonrası durumu:", house_environment) # State of the home environment after tidy-up:
    print(f"Telefonun son konumu: {house_environment['phone']}") # Final location of the phone:

    # The user might be looking for the phone in the living room,
    # but the robot moved it to the charging dock.
    print("\n--- Kullanıcı Perspektifi ---") # User Perspective
    if house_environment['phone'] != "living room":
        print("Kullanıcı: Telefonum nerede? Salon'da olması gerekiyordu!") # User: Where is my phone? It was supposed to be in the living room!
        print(f"Kullanıcı: Ah, sanırım {my_robot_dog.name} onu {house_environment['phone']} konumuna taşımış...") # User: Oh, I guess {RoboDog} moved it to the {phone's location}...
        print("Bu, bir robotun otonom davranışının beklenmedik sonuçlarından biridir.") # This is one of the unexpected consequences of a robot's autonomous behavior.
    else:
        print("Kullanıcı: Telefonum hala salonda. Robot onu taşımamış.") # User: My phone is still in the living room. The robot didn't move it.
