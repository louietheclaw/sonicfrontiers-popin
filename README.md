# sonicfrontiers-popin
Skip to "Usage Instructions" if you want to get right to the good stuff.

## The script:
Using Adubbz's Pop-In multiplier script as a base I found all of the entities in the game and created corresponding multipliers for each of them.  As of Sonic Frontiers v1.20 there are 317 entities, a manageable number to work with. Instead of asking the user for a one-size-fits-all multiplier we feed my version of the script the ini file after tuning it to our liking.

## The ini file:
My goal with this ini file was to maximize range for environmental features and collectibles while minimizing range for behavior objects. In particular I was looking for entities that sound like they shouldn't spawn, though admittedly this has been all guesswork. I don't know who "BossBitManager" is but I might not want to see him.  As a bonus I kept the Titans high because they look cool in the distance.

As I was adjusting distances I did my best to eliminate 3 things:
1. Crashes during or shortly after Starfall
2. Sound glitches on Ares Island
3. Enemies engage from too far away

I'm happy to say that as far as I can tell, 1 and 2 are eliminated. There is one enemy that seems to be a little too sticky. The weak one hit Soldier type that is used as a footstool in platforming challenges. I don't know his internal name so I may have left him at x2 or x3.5, you can still disengage by running a bit away from him.  That brings me to my final remarks.

If you tweak this ini and find additional improvements please pay it forward! You may find bugs that I missed and improve the stability, further push the boundaries, or find a better compromise by tuning these entities individually. I hope this tool is able to increase others' enjoyment of the game as it has mine.

## Usage Instructions:
1. Download and install Python 3.1.1.
2. Download and unpack the latest dev build of HedgeLib from here: https://ci.appveyor.com/project/Radfordhound/hedgelib
3. Download and unpack this script
4. (See 4a for alternate step) BACKUP your \SonicFrontiers\image\x64\raw\gedit folder. If anything goes wrong or you want to make tweaks you can replace the original files. Note: You'll want to wipe any changes manually before re-running the script otherwise it will keep multiplying modified values! Results will not be good.
4a. It's better to plug our modified gedit files into the IncludeDir of another mod. I've been using SousTitré's Higher Object Pop-In Mod. In "\SonicFrontiers\Mods\high pop in value\10x\raw" delete the existing gedit folder and copy the game's vanilla gedit folder here ("\SonicFrontiers\image\x64\raw\gedit"). This will guarantee you're never touching game files. Then configure the mod to x10 to load our modified files.
5. Finally, run the script.
Usage: python .\bubbler_mod.py C:\Path\To\HedgeArcPack.exe "C:\Path\To\gedit" .\frontiers_all_objects_release_8x_max.ini
6. Tune the ini file to your liking and repeat from step 3. If you build a nice ini, share it!
