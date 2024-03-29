"""This module contains Validators which can be used to validated JSON payloads or dicts to make sure they follow
the expected format and contain the required information needed by the backend_api endpoints. Refer to backend_api endpoints
for examples, eg.) backend_api.housekeeping.HousekeepingLogList.post. Note: You can nest validators using the Nested field.
"""

from marshmallow import Schema, fields, validate, \
    validates_schema, ValidationError


class ArgumentValidator(Schema):
    """Validator for arguments to flight schedule or automated commands
    """
    index = fields.Integer(required=True)
    argument = fields.Integer(required=True)


class CommandValidator(Schema):
    """Validator for a single flight schedule or automated command
    """
    command_id = fields.Integer(required=True)
    num_arguments = fields.Integer(required=False)
    is_dangerous = fields.Boolean(required=False)
    command_name = fields.String(required=False)
    about_info = fields.String(required=False, allow_none=True)


class FlightScheduleCommandRepeatValidator(Schema):
    """Validator for the repeat settings for a single flight schedule command
    """
    repeat_ms = fields.Boolean(required=True)
    repeat_sec = fields.Boolean(required=True)
    repeat_min = fields.Boolean(required=True)
    repeat_hr = fields.Boolean(required=True)
    repeat_day = fields.Boolean(required=True)
    repeat_month = fields.Boolean(required=True)
    repeat_year = fields.Boolean(required=True)

    @validates_schema
    def validate_min_hr_repeat(self, data, **kwargs):
        if data['repeat_min'] and not data['repeat_hr']:
            raise ValidationError(
                'repeat_hr MUST be checked if repeat_min is also checked!')


class AutomatedCommandValidator(Schema):
    """Validator for automated commands
    """
    priority = fields.Integer(required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)


class AutomatedCommandPatchValidator(Schema):
    """Validator for patching (editing) an automated command
    """
    priority = fields.Integer(required=False)
    command = fields.Nested(CommandValidator, required=False)
    args = fields.Nested(ArgumentValidator, required=False, many=True)
    automatedcommand_id = fields.Integer(required=False)


class FlightScheduleCommandValidator(Schema):
    """Validator for flighschedule commands
    """
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    repeats = fields.Nested(
        FlightScheduleCommandRepeatValidator, required=True)


class FlightScheduleValidator(Schema):
    """Validator for flight schedules
    """
    status = fields.Integer(
        required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(
        FlightScheduleCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)
    # Prevents posting a flight schedule with an error
    error = fields.Integer(required=True, validate=validate.Equal(0))


class FlightSchedulePatchCommandValidator(Schema):
    """Validator for patching (editing) a flightschedule's commands
    """
    op = fields.String(required=True)
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    flightschedule_command_id = fields.Integer(required=False)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    repeats = fields.Nested(
        FlightScheduleCommandRepeatValidator, required=True)


class FlightSchedulePatchValidator(Schema):
    """Validator for patching (editing) a flightschedule
    """
    status = fields.Integer(
        required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(
        FlightSchedulePatchCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)
    error = fields.Integer(required=True)


class PassoverValidator(Schema):
    """Validator for passovers
    """
    aos_timestamp = fields.DateTime(format='iso', required=True)
    los_timestamp = fields.DateTime(format='iso', required=True)


class PassoverListValidator(Schema):
    """Validator list of passovers
    """
    passovers = fields.Nested(
        PassoverValidator, many=True, required=True, validate=validate.Length(min=1))


class UserValidator(Schema):
    """Validator for creating new users
    """
    username = fields.String(required=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=False)
    creator_id = fields.Integer(required=False)


class UserPatchValidator(Schema):
    """Validator for patching existing users
    """
    username = fields.String(required=False)
    password = fields.String(required=False)
    is_admin = fields.Boolean(required=False)
    slack_id = fields.String(required=False)
    id = fields.Integer(required=False)
    subscribed_to_slack = fields.Boolean(required=False)


class AuthLoginValidator(Schema):
    """Validator for checking login information is present
    """
    username = fields.String(required=True)
    password = fields.String(required=True)


class TelecommandListValidator(Schema):
    """Validator for new telecommands
    """
    command_name = fields.String(required=True)
    num_arguments = fields.Integer(required=True)
    is_dangerous = fields.Boolean(required=True)

############################
# HOUSEKEEPING VALIDATION
############################


class AdcsHKValidator(Schema):
    """Validator for ADCS housekeeping data
    """
    Att_Estimate_Mode = fields.Integer(required=False)
    Att_Control_Mode = fields.Integer(required=False)
    Run_Mode = fields.Integer(required=False)
    Flags_arr = fields.Integer(required=False)
    Longitude = fields.Float(required=False)
    Latitude = fields.Float(required=False)
    Altitude = fields.Float(required=False)
    Estimated_Angular_Rate_X = fields.Float(required=False)
    Estimated_Angular_Rate_Y = fields.Float(required=False)
    Estimated_Angular_Rate_Z = fields.Float(required=False)
    Estimated_Angular_Angle_X = fields.Float(required=False)
    Estimated_Angular_Angle_Y = fields.Float(required=False)
    Estimated_Angular_Angle_Z = fields.Float(required=False)
    Sat_Position_ECI_X = fields.Float(required=False)
    Sat_Position_ECI_Y = fields.Float(required=False)
    Sat_Position_ECI_Z = fields.Float(required=False)
    Sat_Velocity_ECI_X = fields.Float(required=False)
    Sat_Velocity_ECI_Y = fields.Float(required=False)
    Sat_Velocity_ECI_Z = fields.Float(required=False)
    Sat_Position_LLH_X = fields.Float(required=False)
    Sat_Position_LLH_Y = fields.Float(required=False)
    Sat_Position_LLH_Z = fields.Float(required=False)
    ECEF_Position_X = fields.Integer(required=False)
    ECEF_Position_Y = fields.Integer(required=False)
    ECEF_Position_Z = fields.Integer(required=False)
    Coarse_Sun_Vector_X = fields.Float(required=False)
    Coarse_Sun_Vector_Y = fields.Float(required=False)
    Coarse_Sun_Vector_Z = fields.Float(required=False)
    Fine_Sun_Vector_X = fields.Float(required=False)
    Fine_Sun_Vector_Y = fields.Float(required=False)
    Fine_Sun_Vector_Z = fields.Float(required=False)
    Nadir_Vector_X = fields.Float(required=False)
    Nadir_Vector_Y = fields.Float(required=False)
    Nadir_Vector_Z = fields.Float(required=False)
    Wheel_Speed_X = fields.Float(required=False)
    Wheel_Speed_Y = fields.Float(required=False)
    Wheel_Speed_Z = fields.Float(required=False)
    Mag_Field_Vector_X = fields.Float(required=False)
    Mag_Field_Vector_Y = fields.Float(required=False)
    Mag_Field_Vector_Z = fields.Float(required=False)
    TC_num = fields.Integer(required=False)
    TM_num = fields.Integer(required=False)
    CommsStat_flags_1 = fields.Integer(required=False)
    CommsStat_flags_2 = fields.Integer(required=False)
    CommsStat_flags_3 = fields.Integer(required=False)
    CommsStat_flags_4 = fields.Integer(required=False)
    CommsStat_flags_5 = fields.Integer(required=False)
    CommsStat_flags_6 = fields.Integer(required=False)
    Wheel1_Current = fields.Float(required=False)
    Wheel2_Current = fields.Float(required=False)
    Wheel3_Current = fields.Float(required=False)
    CubeSense1_Current = fields.Float(required=False)
    CubeSense2_Current = fields.Float(required=False)
    CubeControl_Current3v3 = fields.Float(required=False)
    CubeControl_Current5v0 = fields.Float(required=False)
    CubeStar_Current = fields.Float(required=False)
    CubeStar_Temp = fields.Float(required=False)
    Magnetorquer_Current = fields.Float(required=False)
    MCU_Temp = fields.Float(required=False)
    Rate_Sensor_Temp_X = fields.Integer(required=False)
    Rate_Sensor_Temp_Y = fields.Integer(required=False)
    Rate_Sensor_Temp_Z = fields.Integer(required=False)


class AthenaHKValidator(Schema):
    """Validator for Athena housekeeping data
    """
    software_ver_major = fields.Integer(required=False)
    software_ver_minor = fields.Integer(required=False)
    software_ver_patch = fields.Integer(required=False)
    MCU_core_temp = fields.Integer(required=False)
    converter_temp = fields.Integer(required=False)
    OBC_uptime = fields.Integer(required=False)
    vol0_usage_percent = fields.Integer(required=False)
    vol1_usage_percent = fields.Integer(required=False)
    boot_cnt = fields.Integer(required=False)
    boot_src = fields.Integer(required=False)
    last_reset_reason = fields.Integer(required=False)
    OBC_mode = fields.Integer(required=False)
    solar_panel_supply_curr = fields.Integer(required=False)
    cmds_received = fields.Integer(required=False)
    pckts_uncovered_by_FEC = fields.Integer(required=False)
    heap_free = fields.Integer(required=False)
    lowest_heap_free = fields.Integer(required=False)


class EpsHKValidator(Schema):
    """Validator for EPS housekeeping data
    """
    eps_cmd_hk = fields.Integer(required=False)
    eps_status_hk = fields.Integer(required=False)
    eps_timestamp_hk = fields.Float(required=False)
    eps_uptimeInS_hk = fields.Integer(required=False)
    eps_bootCnt_hk = fields.Integer(required=False)
    wdt_gs_time_left_s = fields.Integer(required=False)
    wdt_gs_counter = fields.Integer(required=False)
    mpptConverterVoltage1_mV = fields.Integer(required=False)
    mpptConverterVoltage2_mV = fields.Integer(required=False)
    mpptConverterVoltage3_mV = fields.Integer(required=False)
    mpptConverterVoltage4_mV = fields.Integer(required=False)
    curSolarPanels1_mA = fields.Integer(required=False)
    curSolarPanels2_mA = fields.Integer(required=False)
    curSolarPanels3_mA = fields.Integer(required=False)
    curSolarPanels4_mA = fields.Integer(required=False)
    curSolarPanels5_mA = fields.Integer(required=False)
    curSolarPanels6_mA = fields.Integer(required=False)
    curSolarPanels7_mA = fields.Integer(required=False)
    curSolarPanels8_mA = fields.Integer(required=False)
    vBatt_mV = fields.Integer(required=False)
    curSolar_mA = fields.Integer(required=False)
    curBattIn_mA = fields.Integer(required=False)
    curBattOut_mA = fields.Integer(required=False)
    curOutput1_mA = fields.Integer(required=False)
    curOutput2_mA = fields.Integer(required=False)
    curOutput3_mA = fields.Integer(required=False)
    curOutput4_mA = fields.Integer(required=False)
    curOutput5_mA = fields.Integer(required=False)
    curOutput6_mA = fields.Integer(required=False)
    curOutput7_mA = fields.Integer(required=False)
    curOutput8_mA = fields.Integer(required=False)
    curOutput9_mA = fields.Integer(required=False)
    curOutput10_mA = fields.Integer(required=False)
    curOutput11_mA = fields.Integer(required=False)
    curOutput12_mA = fields.Integer(required=False)
    curOutput13_mA = fields.Integer(required=False)
    curOutput14_mA = fields.Integer(required=False)
    curOutput15_mA = fields.Integer(required=False)
    curOutput16_mA = fields.Integer(required=False)
    curOutput17_mA = fields.Integer(required=False)
    curOutput18_mA = fields.Integer(required=False)
    AOcurOutput1_mA = fields.Integer(required=False)
    AOcurOutput2_mA = fields.Integer(required=False)
    outputConverterVoltage1 = fields.Integer(required=False)
    outputConverterVoltage2 = fields.Integer(required=False)
    outputConverterVoltage3 = fields.Integer(required=False)
    outputConverterVoltage4 = fields.Integer(required=False)
    outputConverterVoltage5 = fields.Integer(required=False)
    outputConverterVoltage6 = fields.Integer(required=False)
    outputConverterVoltage7 = fields.Integer(required=False)
    outputConverterVoltage8 = fields.Integer(required=False)
    outputConverterState = fields.Integer(required=False)
    outputStatus = fields.Integer(required=False)
    outputFaultStatus = fields.Integer(required=False)
    protectedOutputAccessCnt = fields.Integer(required=False)
    outputOnDelta1 = fields.Integer(required=False)
    outputOnDelta2 = fields.Integer(required=False)
    outputOnDelta3 = fields.Integer(required=False)
    outputOnDelta4 = fields.Integer(required=False)
    outputOnDelta5 = fields.Integer(required=False)
    outputOnDelta6 = fields.Integer(required=False)
    outputOnDelta7 = fields.Integer(required=False)
    outputOnDelta8 = fields.Integer(required=False)
    outputOnDelta9 = fields.Integer(required=False)
    outputOnDelta10 = fields.Integer(required=False)
    outputOnDelta11 = fields.Integer(required=False)
    outputOnDelta12 = fields.Integer(required=False)
    outputOnDelta13 = fields.Integer(required=False)
    outputOnDelta14 = fields.Integer(required=False)
    outputOnDelta15 = fields.Integer(required=False)
    outputOnDelta16 = fields.Integer(required=False)
    outputOnDelta17 = fields.Integer(required=False)
    outputOnDelta18 = fields.Integer(required=False)
    outputOffDelta1 = fields.Integer(required=False)
    outputOffDelta2 = fields.Integer(required=False)
    outputOffDelta3 = fields.Integer(required=False)
    outputOffDelta4 = fields.Integer(required=False)
    outputOffDelta5 = fields.Integer(required=False)
    outputOffDelta6 = fields.Integer(required=False)
    outputOffDelta7 = fields.Integer(required=False)
    outputOffDelta8 = fields.Integer(required=False)
    outputOffDelta9 = fields.Integer(required=False)
    outputOffDelta10 = fields.Integer(required=False)
    outputOffDelta11 = fields.Integer(required=False)
    outputOffDelta12 = fields.Integer(required=False)
    outputOffDelta13 = fields.Integer(required=False)
    outputOffDelta14 = fields.Integer(required=False)
    outputOffDelta15 = fields.Integer(required=False)
    outputOffDelta16 = fields.Integer(required=False)
    outputOffDelta17 = fields.Integer(required=False)
    outputOffDelta18 = fields.Integer(required=False)
    outputFaultCount1 = fields.Integer(required=False)
    outputFaultCount2 = fields.Integer(required=False)
    outputFaultCount3 = fields.Integer(required=False)
    outputFaultCount4 = fields.Integer(required=False)
    outputFaultCount5 = fields.Integer(required=False)
    outputFaultCount6 = fields.Integer(required=False)
    outputFaultCount7 = fields.Integer(required=False)
    outputFaultCount8 = fields.Integer(required=False)
    outputFaultCount9 = fields.Integer(required=False)
    outputFaultCount10 = fields.Integer(required=False)
    outputFaultCount11 = fields.Integer(required=False)
    outputFaultCount12 = fields.Integer(required=False)
    outputFaultCount13 = fields.Integer(required=False)
    outputFaultCount14 = fields.Integer(required=False)
    outputFaultCount15 = fields.Integer(required=False)
    outputFaultCount16 = fields.Integer(required=False)
    outputFaultCount17 = fields.Integer(required=False)
    outputFaultCount18 = fields.Integer(required=False)
    temp1_c = fields.Integer(required=False)
    temp2_c = fields.Integer(required=False)
    temp3_c = fields.Integer(required=False)
    temp4_c = fields.Integer(required=False)
    temp5_c = fields.Integer(required=False)
    temp6_c = fields.Integer(required=False)
    temp7_c = fields.Integer(required=False)
    temp8_c = fields.Integer(required=False)
    temp9_c = fields.Integer(required=False)
    temp10_c = fields.Integer(required=False)
    temp11_c = fields.Integer(required=False)
    temp12_c = fields.Integer(required=False)
    temp13_c = fields.Integer(required=False)
    temp14_c = fields.Integer(required=False)
    battMode = fields.Integer(required=False)
    mpptMode = fields.Integer(required=False)
    battHeaterMode = fields.Integer(required=False)
    battHeaterState = fields.Integer(required=False)
    PingWdt_toggles = fields.Integer(required=False)
    PingWdt_turnOffs = fields.Integer(required=False)
    thermalProtTemperature_1 = fields.Integer(required=False)
    thermalProtTemperature_2 = fields.Integer(required=False)
    thermalProtTemperature_3 = fields.Integer(required=False)
    thermalProtTemperature_4 = fields.Integer(required=False)
    thermalProtTemperature_5 = fields.Integer(required=False)
    thermalProtTemperature_6 = fields.Integer(required=False)
    thermalProtTemperature_7 = fields.Integer(required=False)
    thermalProtTemperature_8 = fields.Integer(required=False)


class EpsStartupHKValidator(Schema):
    """Validator for EPS Startup housekeeping data
    """
    eps_cmd_startup = fields.Integer(required=False)
    eps_status_startup = fields.Integer(required=False)
    eps_timestamp_startup = fields.Float(required=False)
    last_reset_reason_reg = fields.Integer(required=False)
    eps_bootCnt_startup = fields.Integer(required=False)
    FallbackConfigUsed = fields.Integer(required=False)
    rtcInit = fields.Integer(required=False)
    rtcClkSourceLSE = fields.Integer(required=False)
    flashAppInit = fields.Integer(required=False)
    Fram4kPartitionInit = fields.Integer(required=False)
    Fram520kPartitionInit = fields.Integer(required=False)
    intFlashPartitionInit = fields.Integer(required=False)
    fwUpdInit = fields.Integer(required=False)
    FSInit = fields.Integer(required=False)
    FTInit = fields.Integer(required=False)
    supervisorInit = fields.Integer(required=False)
    uart1App = fields.Integer(required=False)
    uart2App = fields.Integer(required=False)
    tmp107Init = fields.Integer(required=False)


class UhfHKValidator(Schema):
    """Validator for UHK housekeeping data
    """
    scw1 = fields.Integer(required=False)
    scw2 = fields.Integer(required=False)
    scw3 = fields.Integer(required=False)
    scw4 = fields.Integer(required=False)
    scw5 = fields.Integer(required=False)
    scw6 = fields.Integer(required=False)
    scw7 = fields.Integer(required=False)
    scw8 = fields.Integer(required=False)
    scw9 = fields.Integer(required=False)
    scw10 = fields.Integer(required=False)
    scw11 = fields.Integer(required=False)
    scw12 = fields.Integer(required=False)
    U_frequency = fields.Integer(required=False)
    pipe_t = fields.Integer(required=False)
    beacon_t = fields.Integer(required=False)
    audio_t = fields.Integer(required=False)
    uptime = fields.Integer(required=False)
    pckts_out = fields.Integer(required=False)
    pckts_in = fields.Integer(required=False)
    pckts_in_crc16 = fields.Integer(required=False)
    temperature = fields.Float(required=False)


class SbandHKValidator(Schema):
    """Validator for S-Band housekeeping data
    """
    S_mode = fields.Integer(required=False)
    PA_status = fields.Integer(required=False)
    S_frequency_Hz = fields.Integer(required=False)
    S_scrambler = fields.Integer(required=False)
    S_filter = fields.Integer(required=False)
    S_modulation = fields.Integer(required=False)
    S_data_rate = fields.Integer(required=False)
    S_bit_order = fields.Integer(required=False)
    S_PWRGD = fields.Integer(required=False)
    S_TXL = fields.Integer(required=False)
    Output_Power = fields.Integer(required=False)
    PA_Temp = fields.Integer(required=False)
    Top_Temp = fields.Integer(required=False)
    Bottom_Temp = fields.Integer(required=False)
    Bat_Current_mA = fields.Integer(required=False)
    Bat_Voltage_mV = fields.Integer(required=False)
    PA_Current_mA = fields.Integer(required=False)
    PA_Voltage_mV = fields.Integer(required=False)


class HyperionHKValidator(Schema):
    """Validator for Hyperion housekeeping data
    """
    Nadir_Temp1 = fields.Integer(required=False)
    Nadir_Temp_Adc = fields.Integer(required=False)
    Port_Temp1 = fields.Integer(required=False)
    Port_Temp2 = fields.Integer(required=False)
    Port_Temp3 = fields.Integer(required=False)
    Port_Temp_Adc = fields.Integer(required=False)
    Port_Dep_Temp1 = fields.Integer(required=False)
    Port_Dep_Temp2 = fields.Integer(required=False)
    Port_Dep_Temp3 = fields.Integer(required=False)
    Port_Dep_Temp_Adc = fields.Integer(required=False)
    Star_Temp1 = fields.Integer(required=False)
    Star_Temp2 = fields.Integer(required=False)
    Star_Temp3 = fields.Integer(required=False)
    Star_Temp_Adc = fields.Integer(required=False)
    Star_Dep_Temp1 = fields.Integer(required=False)
    Star_Dep_Temp2 = fields.Integer(required=False)
    Star_Dep_Temp3 = fields.Integer(required=False)
    Star_Dep_Temp_Adc = fields.Integer(required=False)
    Zenith_Temp1 = fields.Integer(required=False)
    Zenith_Temp2 = fields.Integer(required=False)
    Zenith_Temp3 = fields.Integer(required=False)
    Zenith_Temp_Adc = fields.Integer(required=False)
    Nadir_Pd1 = fields.Integer(required=False)
    Port_Pd1 = fields.Integer(required=False)
    Port_Pd2 = fields.Integer(required=False)
    Port_Pd3 = fields.Integer(required=False)
    Port_Dep_Pd1 = fields.Integer(required=False)
    Port_Dep_Pd2 = fields.Integer(required=False)
    Port_Dep_Pd3 = fields.Integer(required=False)
    Star_Pd1 = fields.Integer(required=False)
    Star_Pd2 = fields.Integer(required=False)
    Star_Pd3 = fields.Integer(required=False)
    Star_Dep_Pd1 = fields.Integer(required=False)
    Star_Dep_Pd2 = fields.Integer(required=False)
    Star_Dep_Pd3 = fields.Integer(required=False)
    Zenith_Pd1 = fields.Integer(required=False)
    Zenith_Pd2 = fields.Integer(required=False)
    Zenith_Pd3 = fields.Integer(required=False)
    Port_Voltage = fields.Integer(required=False)
    Port_Dep_Voltage = fields.Integer(required=False)
    Star_Voltage = fields.Integer(required=False)
    Star_Dep_Voltage = fields.Integer(required=False)
    Zenith_Voltage = fields.Integer(required=False)
    Port_Current = fields.Integer(required=False)
    Port_Dep_Current = fields.Integer(required=False)
    Star_Current = fields.Integer(required=False)
    Star_Dep_Current = fields.Integer(required=False)
    Zenith_Current = fields.Integer(required=False)


class CharonHKValidator(Schema):
    """Validator for Charon housekeeping data
    """
    gps_crc = fields.Integer(required=False)
    charon_temp1 = fields.Integer(required=False)
    charon_temp2 = fields.Integer(required=False)
    charon_temp3 = fields.Integer(required=False)
    charon_temp4 = fields.Integer(required=False)
    charon_temp5 = fields.Integer(required=False)
    charon_temp6 = fields.Integer(required=False)
    charon_temp7 = fields.Integer(required=False)
    charon_temp8 = fields.Integer(required=False)


class DfgmHKValidator(Schema):
    """Validator for DFGM housekeeping data
    """
    Core_Voltage = fields.Integer(required=False)
    Sensor_Temperature = fields.Integer(required=False)
    Reference_Temperature = fields.Integer(required=False)
    Board_Temperature = fields.Integer(required=False)
    Positive_Rail_Voltage = fields.Integer(required=False)
    Input_Voltage = fields.Integer(required=False)
    Reference_Voltage = fields.Integer(required=False)
    Input_Current = fields.Integer(required=False)
    Reserved_1 = fields.Integer(required=False)
    Reserved_2 = fields.Integer(required=False)
    Reserved_3 = fields.Integer(required=False)
    Reserved_4 = fields.Integer(required=False)


class NorthernSpiritHKValidator(Schema):
    """Validator for Northern Spirit payload housekeeping data
    """
    ns_temp0 = fields.Integer(required=False)
    ns_temp1 = fields.Integer(required=False)
    ns_temp2 = fields.Integer(required=False)
    ns_temp3 = fields.Integer(required=False)
    eNIM0_lux = fields.Integer(required=False)
    eNIM1_lux = fields.Integer(required=False)
    eNIM2_lux = fields.Integer(required=False)
    ram_avail = fields.Integer(required=False)
    lowest_img_num = fields.Integer(required=False)
    first_blank_img_num = fields.Integer(required=False)


class IrisHKValidator(Schema):
    """Validator for IRIS housekeeping data
    """
    VIS_Temperature = fields.Float(required=False)
    NIR_Temperature = fields.Float(required=False)
    Flash_Temperature = fields.Float(required=False)
    Gate_Temperature = fields.Float(required=False)
    Image_number = fields.Integer(required=False)
    Software_Version = fields.Integer(required=False)
    Error_number = fields.Integer(required=False)
    MAX_5V_voltage = fields.Integer(required=False)
    MAX_5V_power = fields.Integer(required=False)
    MAX_3V_voltage = fields.Integer(required=False)
    MAX_3V_power = fields.Integer(required=False)
    MIN_5V_voltage = fields.Integer(required=False)
    MIN_3V_voltage = fields.Integer(required=False)


class HousekeepingValidator(Schema):
    """Validator for a housekeeping entry
    """
    timestamp = fields.DateTime(format='iso', required=True)
    data_position = fields.Integer(required=True)
    tle = fields.String(required=False)

    # Subsystem validation
    adcs = fields.Nested(AdcsHKValidator, many=False, required=True)
    athena = fields.Nested(AthenaHKValidator, many=False, required=True)
    eps = fields.Nested(EpsHKValidator, many=False, required=True)
    eps_startup = fields.Nested(EpsStartupHKValidator, many=False, required=True)
    uhf = fields.Nested(UhfHKValidator, many=False, required=True)
    sband = fields.Nested(SbandHKValidator, many=False, required=True)
    hyperion = fields.Nested(HyperionHKValidator, many=False, required=True)
    charon = fields.Nested(CharonHKValidator, many=False, required=True)
    dfgm = fields.Nested(DfgmHKValidator, many=False, required=True)
    northern_spirit = fields.Nested(
        NorthernSpiritHKValidator, many=False, required=True)
    iris = fields.Nested(IrisHKValidator, many=False, required=True)
