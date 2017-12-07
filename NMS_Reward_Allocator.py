from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET

root = Tk()

__author__ = "Gmr Leon"
__credits__ = ["Gmr Leon", "localghost", "monkeyman192", "Honest Abe"]

class GUI(Frame):
    def __init__(self, leader):
        self.leader = leader
        Frame.__init__(self, self.leader)
        self.leader.title("NMS Reward Allocator")
        #Attributes set to hide repositioning of window using centerWin function.
        root.attributes('-alpha', 0.0)
        self.centerWin(root)
        root.attributes('-alpha', 1.0)
        self.grid()

        #Basic menubar settings.
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu, tearoff=False)
        menu.add_command(label="Select Exml", command=self.loadexml)
        menu.add_command(label="Help", command=self.displayhelp)

        #Listbox selection handling.
        self.selectedAlienRace = StringVar()
        self.selectedAlienRace.set("None")
        self.selectedIntType = StringVar()
        self.selectedIntType.set("None")

        #Below handles combobox custom entries.
        self.selectedRewID = StringVar()
        self.selectedRewID.set("Input Reward ID. 16 chars or less.")
        self.selectedRewID.trace("w", self.processSelection2)

        #Select exml to parse; store filename to write file in Commit function below.
        self.selexml = StringVar()
        self.selexml.set("None")
        self.savexml = StringVar()
        self.savexml.set("None")

        self.createWidgets()

    def centerWin(self, win):
        win.update_idletasks()
        width = 330
        ofrm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * ofrm_width
        height = 280
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + ofrm_width
        x = win.winfo_screenwidth() // 2 - width // 2
        y = win.winfo_screenheight() // 2 - height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def displayhelp(self):
        self.display = messagebox.showinfo("Here to help!", "1. Click Select Exml first.\n\
2. Locate NMS_DIALOG_GCALIENPUZZLETABLE.exml in METADATA\REALITY\TABLES.\n3. Pick the race & interaction type of \
the entries to modify.\n4. Write a Reward ID or select from existing Reward IDs to \
set the reward to append and/or add to the existing entries.\n5. Click Commit Settings! \
Then save the file with whatever name and wherever, and voila!\n\nP.S. If saving \
with the NMS_DIALOG name, please remember to back up the original file before overwriting!", parent=root)
        
    def createWidgets(self):
        alienrace_opts = ["None", "Atlas", "Diplomats", "Explorers", "Robots",
                          "Traders", "Warriors"]
        #Reverse set here & below with interacttype_opts to display in proper order.
        alienrace_opts.sort(reverse=True)

        Label(root, text="Alien Race").grid(sticky="NEW", row=0, column=0)
        self.alienrace = Listbox(root, selectmode=SINGLE, exportselection=0)
        self.alienrace.grid(sticky="NW", row=1, column=0, ipady=15, padx=5)

        #Populate listbox with options, set to select first in list.
        for ar in alienrace_opts:
            self.alienrace.insert(0, ar)
        self.alienrace.selection_set(first=0)

        interacttype_opts = ["None", "Shop", "NPC", "NPC_Secondary",
                             "NPC_Anomaly","NPC_Anomaly_Secondary",
                             "Ship", "Outpost", "SpaceStation",
                             "RadioTower", "Monolith", "Factory",
                             "AbandonedShip", "Harvester",
                             "Observatory", "TradingPost", "DistressBeacon",
                             "Portal", "Plaque", "AtlasStation",
                             "AbandonedBuildings", "WeaponTerminal",
                             "SuitTerminal", "SignalScanner",
                             "Teleporter_Base", "Teleporter_Station",
                             "ClaimBase", "NPC_Freighter_Captain",
                             "NPC_HIRE_Weapons", "NPC_HIRE_Weapons_Wait",
                             "NPC_HIRE_Farmer", "NPC_HIRE_Farmer_Wait",
                             "NPC_HIRE_Builder", "NPC_HIRE_Builder_Wait",
                             "NPC_HIRE_Vehicles", "NPC_HIRE_Vehicles_Wait",
                             "MessageBeacon", "NPC_HIRE_Scientist",
                             "NPC_HIRE_Scientist_Wait", "NPC_Recruit",
                             "NPC_Freighter_Captain_Secondary",
                             "NPC_Recruit_Secondary", "Vehicle",
                             "MessageModule", "TechShop", "VehicleRaseStart",
                             "BuildingShop", "MissionGiver", "HoloHub",
                             "HoloExplorer", "HoloSceptic", "HoloNoone",
                             "PortalRunEntry", "PortalActivate",
                             "CrashedFreighter", "GraveInCave",
                             "GlitchyStroyBox", "NetworkPlayer",
                             "NetworkMonument", "AnomalyComputer",
                             "AtlasPlinth", "Epilogue", "CUSTOMINTERACTION0",
                             "CUSTOMINTERACTION1", "CUSTOMINTERACTION2",
                             "CUSTOMINTERACTION3", "CUSTOMINTERACTION4"]
        interacttype_opts.sort(reverse=True)

        Label(root, text="Interaction Type").grid(sticky="NEW", row=0, column=1)
        self.interacttype = Listbox(root, width=31, selectmode=SINGLE, exportselection=0)
        self.interacttype.grid(sticky="E", row=1, column=1, ipady=15, padx=2)

        #Populate listbox with options, set to select first in list.
        for iat in interacttype_opts:
            self.interacttype.insert(0, iat)
        self.interacttype.selection_set(first=0)

        #On Listbox item selected, run processSelection function to store selection.
        self.alienrace.bind('<<ListboxSelect>>', lambda\
                            *args: self.processSelection(self.alienrace))

        self.interacttype.bind('<<ListboxSelect>>', lambda\
                               *args: self.processSelection(self.interacttype))

        rewids = ["POOPLOOT", "DAMAGESMALL", "DAMAGELARGE", "SHIELDSMALL",
                  "SHIELDLARGE", "HAZARDSMALL", "HAZARDLARGE", "HEALTHSMALL",
                  "HEALTHLARGE", "MONEY", "STANDING", "TECHWEAPON", "TECHSHIP",
                  "CAPFRT_STAND", "CAPFRT_LOOT", "FREIGHT_STAND", "FREIGHT_REWARD",
                  "PIRATELOOT", "PIRAT_LOOT_EASY", "PIRAT_LOOT_MED", "PIRAT_LOOT_HARD",
                  "POLICELOOT", "TRADERLOOT", "TRAD_LOOT_EASY", "TRAD_LOOT_MED",
                  "TRAD_LOOT_HARD", "INTERIORPLANTS", "TECHSUIT", "WORD", "PIRATE_BATTLE",
                  "PIRATE_FIGHT", "RANDOM", "NOREWARD", "HYPER", "FAKETECHSUIT",
                  "FAKEWORD", "PIRATE_BOUNTY1", "PIRATE_BOUNTY2", "PIRATE_BOUNTY3",
                  "PLANT_COMMODITY", "PLANT_TECH", "PLANT_FUEL", "PLANT_PEARL",
                  "PLANT_GRAV", "PLANT_SACVENOM", "PLANT_BARREN", "PLANT_LUSH",
                  "PLANT_CREATURE", "PLANT_POOP", "PLANT_RADIO", "PLANT_SCORCHED",
                  "PLANT_SNOW", "PLANT_TOXIC", "FREIGHTERLOOT", "PLANTER_CARBON",
                  "HEALTHFULL", "PLANT_NIP", "TECHFRAG_L", "TECHFRAG_M", "TECHFRAG_S",
                  "TIMED_RADIO", "MONEY_S", "MONEY_M", "MONEY_L", "TECHDEBRIS",
                  "KILLED_CIV", "USEFUL_PROD", "RECIPE_LIST", "R_CAVEGRAVE",
                  "R_A1S6_WAR", "R_A1S6_TRA", "R_A1S6_EXP", "TRA_WORD", "EXP_WORD",
                  "WAR_WORD", "ANOMALYTECH1", "ANOMALYTECH2", "ANOMALYTECH3",
                  "ANOMALYTECH4", "ANOMALYTECH5", "ANOMALYTECH6", "ANOMALYTECH7",
                  "ANOMALYTECH8", "ANOMALYTECH9", "ANOMALYTECH10", "ANOMALYTECH11",
                  "ANOMALYTECH12", "ANOMALYTECH13", "ANOMALYTECH14", "ANOMALYTECH15",
                  "ANOMALYTECH16", "SHIPSUIT", "STD_INC_EXP", "STD_DEC_EXP",
                  "STD_INC_TRA", "STD_DEC_TRA", "STD_INC_WAR", "STD_DEC_WAR",
                  "SUBST_COMMOD", "SUBST_TECH", "SUBST_FUEL", "PROD_COMMOD",
                  "PROD_TECH", "PROD_FUEL", "PROD_CUR", "RECIP_PROD_COMM",
                  "RECIP_PROD_TRAD", "RECIP_PROD_TECH", "RECIP_PROD_FUEL",
                  "TECH_ALL", "TECH_SUIT", "TECH_WEAPON", "TECH_SHIP",
                  "RECIP_TECH_ALL", "RECIP_TECH_SUIT", "RECIP_TECH_WEAP",
                  "RECIP_TECH_SHIP", "WEAPON", "TIMEWARP", "DISTRESSSCAN",
                  "DAMAGE_TECH", "REPAIR_TECH", "FUEL1_SM", "AMMO1_SM",
                  "HACK1_SM", "DRUGS1_SM", "FUEL1_ME", "AMMO1_ME", "HACK1_ME",
                  "DRUGS1_ME", "FUEL1_LA", "AMMO1_LA", "HACK1_LA", "DRUGS1_LA",
                  "TEACHWORD_EXP", "TEACHWORD_TRA", "TEACHWORD_WAR",
                  "GIVE_HYPERDRIVE", "GIVE_ANTI", "RECIP_ANTI",
                  "RECIP_FLUID", "ATLAS", "SCAN_A1S5", "SCAN_1",
                  "SCAN_2", "SCAN_3", "SCAN_4", "C_GEKRELIC",
                  "C_VYKEENEFFIGY", "C_KORVAXCASING", "C_NIGHTCRYSTALS",
                  "C_ATLASSTONE", "D_ATLASPASSV1", "D_ATLASPASSV2", "D_ATLASPASSV3",
                  "TEACHWORD_ATLAS", "P_HYPERFUEL1", "P_HACK1", "P_GRAVBALL",
                  "P_ALBUMENPEARL", "T_ARMOUR1", "T_ARMOUR2", "T_ARMOUR3",
                  "D_HYPERDRIVE1", "D_HYPERDRIVE2", "D_HYPERDRIVE3",
                  "FREIGHTER_TRANS", "BUILDING_VISIT", "SEC_TECHFRAG",
                  "SEC_MONEY", "SEC_CRASHEDSHIP", "SEC_STDLOW_WAR",
                  "SEC_STDLOW_TRA", "SEC_STDLOW_EXP", "SEC_STDHIGH_WAR",
                  "SEC_STDHIGH_TRA", "SEC_STDHIGH_EXP", "RECIP_NEW_COMP",
                  "RECIP_NEW_GAS", "RECIP_NEW_PROD", "RECIP_RARE_PROD",
                  "SEC_SCN_OUTPOST", "SEC_SCN_FACT", "SEC_SCN_TOWER", "SEC_SCN_OBS",
                  "SHOW_CRASHSITE", "R_TECHMISSION", "R_CURIO9", "R_CURIO7",
                  "R_CAVECUBE", "SEC_SCN_HARV", "NPC_BUILD_GOTO", "NPC_BUILD7",
                  "NPC_BUILD5", "NPC_SCI_GOTO", "NPC_SCI_GOTO1", "NPC_VEHIC_GOTO",
                  "NPC_FARM_GOTO", "NPC_WEAPON_GOTO", "NPC_WEAPON1", "NPC_WEAPON2",
                  "NPC_WEAPON3", "NPC_WEAPON4", "NPC_WEAPON5", "NPC_WEAPON6",
                  "NPC_WEAPON7", "NPC_WEAPON8", "NPC_WEAPON9", "NPC_WEAPON10",
                  "NPC_VEHICLE16S", "NPC_VEHICLE16", "NPC_VEHICLE15",
                  "NPC_VEHICLE14", "NPC_VEHICLE13", "NPC_VEHICLE12",
                  "NPC_VEHICLE11S", "NPC_VEHICLE11", "NPC_VEHICLE10",
                  "NPC_VEHICLE9", "NPC_VEHICLE8", "NPC_VEHICLE7", "NPC_VEHICLE6",
                  "NPC_VEHICLE5S", "NPC_VEHICLE5", "NPC_VEHICLE4",
                  "NPC_VEHICLE3", "NPC_VEHICLE2", "NPC_VEHICLE1",
                  "NPC_FARM1", "NPC_FARM2", "NPC_FARM3", "NPC_FARM4", "NPC_FARM5",
                  "NPC_FARM6", "NPC_FARM7", "NPC_FARM8", "NPC_FARM9", "NPC_FARM10",
                  "NPC_SCIENCE1", "NPC_SCIENCE2", "NPC_SCIENCE3", "NPC_SCIENCE4",
                  "NPC_SCIENCE5", "NPC_SCIENCE6", "NPC_SCIENCE7", "NPC_SCIENCE8",
                  "NPC_SCIENCE9", "NPC_SCIENCE10", "NPC_BUILD1", "NPC_BUILD2",
                  "NPC_BUILD3", "NPC_BUILD4", "NPC_BUILD6", "NPC_BUILD8",
                  "NPC_BUILD9", "NPC_BUILD10", "HIRE_BUILDER", "HIRE_WEAPONS",
                  "HIRE_FARMER", "HIRE_VEHICLES", "HIRE_SCIENTIST",
                  "NPC_BUILD11", "TRIGGER_ACTIVE", "R_A2S5_ARTDEAD",
                  "R_A2S5_ARTSIM", "REV_ALL_BH", "R_FACTMED_WIN", "REV_ATLAS_STA",
                  "REV_BLACK_HOLE", "FREE_EXPLORE", "RUINSCAN", "TELEPORT_BASE",
                  "TELEPORT_0", "TELEPORT_1", "TELEPORT_2", "TELEPORT_3",
                  "START_PURCHASE", "BEGIN_SALVAGE", "R_FACTHARD_WIN",
                  "INC_ATLAS_PATH", "CENTREJOURNEY1", "CENTREJOURNEY2",
                  "CENTREJOURNEY3", "CENTREJOURNEY4", "TRIG_AP_10", "PORTALRUNE1",
                  "PORTALRUNE2", "PORTALRUNE3", "PORTALRUNE4", "PORTALRUNE5",
                  "PORTALRUNE6", "PORTALRUNE7", "PORTALRUNE8", "PORTALRUNE9",
                  "PORTALRUNE10", "PORTALRUNE11", "PORTALRUNE12", "PORTALRUNE13",
                  "PORTALRUNE14", "PORTALRUNE15", "PORTALRUNE16", "C_ATLASSTONE1",
                  "C_ATLASSTONE2", "C_ATLASSTONE3", "C_ATLASSTONE4", "C_ATLASSTONE5",
                  "C_ATLASSTONE6", "C_ATLASSTONE7", "C_ATLASSTONE8", "C_ATLASSTONE9",
                  "C_ATLASSTONE10", "PIRATE_APPEASE", "PIRATE_REJECT", "PIRATE_POLICE",
                  "ADVANCE_PORTAL", "RESET_PORTAL", "CRASHCONT_M", "REVEAL_RUNES",
                  "REVEAL_PORTAL", "REPAIR_COMPLETE", "MB_STAND_HIGH", "MB_STAND_MED",
                  "MB_STAND_LOW", "MB_STAND_NEG", "R_MB_LOW", "R_MB_MED", "R_MB_HIGH",
                  "R_MB_MEGA"]
        rewids.sort()
        
        self.RewardSelect = ttk.Combobox(root, values=rewids, textvariable=self.selectedRewID,\
                                         exportselection=0)
        self.RewardSelect.grid(sticky="SEW", columnspan=2, padx=10, pady=3)
        #Same as above, on Combobox selection (if opting for preexisting reward ID)
        #store Combobox selection.
        self.RewardSelect.bind('<<ComboboxSelected>>', lambda\
                               *args: self.processSelection2(self.RewardSelect))

        #Run Commit function to parse exml for selected settings & append/add rewards in
        #entries of selected race/interaction type.
        commit = Button(root, text="Commit settings!",
                         command=lambda: self.export(self.selectedAlienRace.get(),\
                                                       self.selectedIntType.get(),\
                                                       self.selectedRewID.get()))
        commit.grid(sticky="SEW", columnspan=2, padx=10, pady=3)

    def processSelection(self, listbox):
        #Get the selected entry and assign to the appropriate variable
        selectedItem = listbox.get(listbox.curselection()[0])
        if listbox == self.alienrace:
            self.selectedAlienRace.set(selectedItem)
            print(self.selectedAlienRace.get())
        elif listbox == self.interacttype:
            self.selectedIntType.set(selectedItem)
            print(self.selectedIntType.get())

    def processSelection2(self, pick, *args):
        pick = self.RewardSelect.get()
        #Below check is debug to ensure tracer function is working properly.
        #check = self.selectedRewID.get()
        #print(check)
        if len(pick) >= 16:
            self.selectedRewID.set(pick[:16])
            print(self.selectedRewID.get())

    def loadexml(self):
        lfn = askopenfilename(title="Choose exml to parse", filetypes = (("Exml files", "*.exml"),
                                                ("All files", "*.*")))
        if lfn == '':
            return
        else:
            self.selexml.set(lfn)

    def export(self, selectedAlienRace, selectedIntType, selectedRewID):
        if self.selexml.get() == "None":
            messagebox.showwarning("Waaait a sec!", "You forgot to select an exml to parse!")
        else:
            tree = ET.parse("{0}".format(self.selexml.get()))
            root = tree.getroot()
            
            for dblfilt in root.findall('.//Property[@name="AlienRace"][@value="{0}"]/../..'\
                                    .format(self.selectedAlienRace.get())):
                #Debug lines to see what's being found & stored in dblfilt.
                #check = ET.tostring(dblfilt)
                #print(check)
                for rwrd in dblfilt.findall('.//Property[@name="InteractionType"][@value="{0}"]/../..'\
                                        .format(self.selectedIntType.get())):
                    try:
                        aha = rwrd.iterfind('.//Property[@name="Rewards"]')
                        for allopts in aha:
                            here = ET.SubElement(allopts, "Property", value='NMSString0x10.xml')
                            there = ET.SubElement(here, "Property", name='Value', value='{0}'\
                                              .format(self.selectedRewID.get()))
                            here.tail = "\n          "
                            here.text = "\n              "
                            there.tail = "\n            "
                    #Exception for entries without any rewards element whatsoever.
                    except TypeError:
                        recover = rwrd.find('.//Property[@name="Text"]')
                        identify = ET.tostring(recover)
                        print(identify)
                        print("Umm, no reward present!")
            
            sfn = asksaveasfilename(defaultextension=".exml", filetypes = (("Exml files", "*.exml"),
                                                ("All files", "*.*")))
            self.savexml.set(sfn)
            tree.write("{0}".format(self.savexml.get()), short_empty_elements=True) 

app = GUI(leader=root)
#root.iconbitmap("AddRewUtil.ico")
root.resizable(width=False, height=False)
mainloop()
