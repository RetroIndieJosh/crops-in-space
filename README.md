# CROPS IN SPACE
(c)2018 Joshua McLean

# Notes

Fuel consumption: 1/hr

Engine 0: idle, grow 100%
Engine 1: 1x speed, 2x fuel, grow 100%
Engine 2: 3x speed, 2x fuel, grow 50% 
Engine 3: 6x speed, 2x fuel, grow 0%, requires crew

Wait for X hours interrupted when event occurs
        Approaching planet
        Fuel low
        Fuel empty
        Entering conflict
        Arrived at Earth

# Version History

## Version 0.1.0 (June 2018)

Rewrite:
+ Bridge menu
+ Crops menu
+ Power room menu
+ Combat
+ Planet landing

Bug fixes:
- Fix exception when asking why we can't sell seeds
+ Fix running out of fuel doesn't stop engine (negative fuel)
+ Fix passed planet still in range (negative distance)
+ Fix crew appearing in tutorial and ending when not on ship

Improvements:
+ Improve UI for selecting numbers (no more typing)
+ Rebalance engine fuel consumption 
+ Improve crew and background graphics
+ Improve combat graphics
+ Streamline event system to be less intrusive
+ Update all music tracks
+ Simplify shields to 1 - 3 instead of %
+ Ship UI overhaul with more visual cues
+ New music for crop room
+ New music for power room

Game changes:
+ Interactive introduction/tutorial
+ Combat: negotiate for safe passage
+ Combat: wait for help (and help actually comes)
+ Crew: more mood messages/interaction
+ Crew: hire additional crew on planet
+ Crops: place seeds in grid
+ When out of fuel in space, can now piggyback to previous planet
+ New room: crew quarters where the crew go to rest
+ New room: lounge where the crew hang out if not working
- Crew affinity for all other crewmembers
- Remove realtime clock, crew feeding, food conversion/purchasing

## [Version 0.0.7 (23 April 2018)]

Ludum Dare 41 release (first public version)

# License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

(c)2019 Joshua McLean
