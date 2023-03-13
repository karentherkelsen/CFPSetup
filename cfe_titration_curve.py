from opentrons import protocol_api
import sys

metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Cell Free expression titration curve',
    'description': '''This protocol is designed to set up a logarithmic serial 
    dilution of a single reagent for cell-free expression. A total of 7 
    concentrations of the reagent are tested in technical triplicates, including
    an internal control without DNA and the highest concentration.''',
    'author': 'Karen Therkelsen (s173684@dtu.dk)',
}

################################################################################
#                                  User inputs                                 #
################################################################################

# Define row in well-plate to load
row = "A"

################################################################################

nsamples = 8 * 3


def run(protocol):
    
    ## Load instrument, modules and labware ##

    #--------------#--------------#--------------#
    # PCR strips,  #   384-well   #    Trash     #
    # 4C   	       #   plate      #              #
    #--------------#--------------#--------------#
    #              #   P20 tips   #  P300 tips   #
    #              #              #              #
    #------------- #------------- #------------- #
    # 2mLEppendorf #              #              #
    # tubes, 4C    #              #              #
    #------------- #------------- #------------- #
    #              #              #              #
    #              #              #              #
    #------------- #------------- #------------- #


    # Pipettes and tips
    tips20 = protocol.load_labware('opentrons_96_tiprack_20ul', 8)
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    p20 = protocol.load_instrument('p20_single_gen2', mount='left', tip_racks=[tips20])
    p300 = protocol.load_instrument('p300_single', mount='right', tip_racks=[tips300])

    # 384-well plate
    plate = protocol.load_labware('corning_384_wellplate_112ul_flat', 11)

    # Temperature modules
    temp_module_pcrtubes = protocol.load_module('temperature module gen2', 10)
    pcrtubes_cool = temp_module_pcrtubes.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul')

    temp_module_eppendorftubes = protocol.load_module('temperature module gen2', 4)
    eppendorftubes_cool = temp_module_eppendorftubes.load_labware('opentrons_24_aluminumblock_nest_2ml_snapcap')
    

    ## Define start reagents
    
    # In PCR module (number refer to well)
    # A1. X: 10 uL
    # B1-H1: empty tubes
    # A2. DNA: 15 uL
    # B2. rNTP: 18 uL
    # C2. Lysate: 150 uL
    # D2. Buffer: 175 uL
    X = pcrtubes_cool.wells()[0]
    DNA = pcrtubes_cool.wells()[8]
    rNTP = pcrtubes_cool.wells()[9]
    Lysate = pcrtubes_cool.wells()[10]
    Buffer = pcrtubes_cool.wells()[11]

    # In Eppendorf module
    # A1. MQ: 1 mL
    # A2. MM: 1 mL
    MQ = eppendorftubes_cool.wells_by_name()["A1"]
    MM = eppendorftubes_cool.wells_by_name()["A2"]


    ## Functions

    def serial_dilution():
        """Prepare logaritmic serial dilution with reagent"""
        p20.distribute(9, MQ, pcrtubes_cool.wells()[1:7])
        p20.pick_up_tip()
        p20.transfer(1, pcrtubes_cool.wells()[:6], pcrtubes_cool.wells()[1:7], mix_after=(10,8), new_tip="never")
        p20.drop_tip()

    def mix_mastermix():
        """Ensure homogenous mastermix before loding"""
        p300.pick_up_tip()
        for i in range(5):
            p300.aspirate(100, MM.bottom(1))
            p300.dispense(100, MM.top(-20))
        p300.drop_tip()
     
    def cfe_mastermix_prep():
        """Prepare CFE master mix excl. reagent"""
        lysate_vol = 4 * (nsamples * 1.5) #uL
        buffer_vol = 4.5 * (nsamples * 1.5)  #uL
        rNTP_vol = 0.5 * (nsamples * 1.5)  #uL

        p300.transfer(lysate_vol, Lysate, MM, touch_tip=True)
        p300.transfer(buffer_vol, Buffer, MM, touch_tip=True)
        p20.transfer(rNTP_vol, rNTP, MM, touch_tip=True)
    
    def dispense_small_vol_to_well(well_start, well_stop, reagent):
        "Liquid handling of 0.5 uL to well-plate to a range of destination well numbers."
        p20.pick_up_tip()
        total_vol = ((well_stop - well_start) * 0.5) + 1
        p20.aspirate(total_vol, reagent.bottom(1))
        for well_no in range(well_start, well_stop):
            p20.dispense(0.5, plate.rows_by_name()[row][well_no].bottom(0.1))
        p20.drop_tip()
    
    

    ## Protocol workflow
    
    #temp_module_pcrtubes.set_temperature(4)
    #temp_module_eppendorftubes.set_temperature(4)
    
    # Prepare master mix and serial dilution
    serial_dilution()
    cfe_mastermix_prep()
    
    # Add Add mastermix
    mix_mastermix()
    p20.distribute(9.0, MM, plate.rows_by_name()[row][:nsamples], touch_tip=True, blow_out=True, blowout_location='source well')
    
    # Add reagent
    for i in range(0,nsamples-3,3):
        dil_no = int((i+1)/3)
        if dil_no == 0:
            dispense_small_vol_to_well(i, i+3, pcrtubes_cool.wells()[dil_no])
            # Load internal control
            dispense_small_vol_to_well(nsamples-3, nsamples, pcrtubes_cool.wells()[dil_no])
            dispense_small_vol_to_well(nsamples-3, nsamples, MQ) 
        else:
            dispense_small_vol_to_well(i, i+3, pcrtubes_cool.wells()[dil_no])

    # Add DNA to initate CFE
    dispense_small_vol_to_well(0, nsamples-3, DNA)
    
    #temp_module_pcrtubes.deactivate()
    #temp_module_eppendorftubes.deactivate()
