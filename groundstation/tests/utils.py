import datetime

# Default values for each datatype in fake housekeeping data
DEFAULT_INT = 42
DEFAULT_FLOAT = 13.37
DEFAULT_STR = 'Fake string!'


def fake_housekeeping_as_dict(timestamp, data_position):
    return {
        'timestamp': timestamp,
        'data_position': data_position,
        'tle': '1 25544U 98067A   22194.51466271  .00006028  00000+0  11379-3 0  9999\n2 25544  51.6428 206.1919 0004833   7.6129 121.4090 15.49927705349269',
    }


def fake_adcs_hk_as_dict():
    return {
        'Att_Estimate_Mode': DEFAULT_INT,
        'Att_Control_Mode': DEFAULT_INT,
        'Run_Mode': DEFAULT_INT,
        'Flags_arr': DEFAULT_INT,
        'Longitude': DEFAULT_FLOAT,
        'Latitude': DEFAULT_FLOAT,
        'Altitude': DEFAULT_FLOAT,
        'Estimated_Angular_Rate_X': DEFAULT_FLOAT,
        'Estimated_Angular_Rate_Y': DEFAULT_FLOAT,
        'Estimated_Angular_Rate_Z': DEFAULT_FLOAT,
        'Estimated_Angular_Angle_X': DEFAULT_FLOAT,
        'Estimated_Angular_Angle_Y': DEFAULT_FLOAT,
        'Estimated_Angular_Angle_Z': DEFAULT_FLOAT,
        'Sat_Position_ECI_X': DEFAULT_FLOAT,
        'Sat_Position_ECI_Y': DEFAULT_FLOAT,
        'Sat_Position_ECI_Z': DEFAULT_FLOAT,
        'Sat_Velocity_ECI_X': DEFAULT_FLOAT,
        'Sat_Velocity_ECI_Y': DEFAULT_FLOAT,
        'Sat_Velocity_ECI_Z': DEFAULT_FLOAT,
        'Sat_Position_LLH_X': DEFAULT_FLOAT,
        'Sat_Position_LLH_Y': DEFAULT_FLOAT,
        'Sat_Position_LLH_Z': DEFAULT_FLOAT,
        'ECEF_Position_X': DEFAULT_INT,
        'ECEF_Position_Y': DEFAULT_INT,
        'ECEF_Position_Z': DEFAULT_INT,
        'Coarse_Sun_Vector_X': DEFAULT_FLOAT,
        'Coarse_Sun_Vector_Y': DEFAULT_FLOAT,
        'Coarse_Sun_Vector_Z': DEFAULT_FLOAT,
        'Fine_Sun_Vector_X': DEFAULT_FLOAT,
        'Fine_Sun_Vector_Y': DEFAULT_FLOAT,
        'Fine_Sun_Vector_Z': DEFAULT_FLOAT,
        'Nadir_Vector_X': DEFAULT_FLOAT,
        'Nadir_Vector_Y': DEFAULT_FLOAT,
        'Nadir_Vector_Z': DEFAULT_FLOAT,
        'Wheel_Speed_X': DEFAULT_FLOAT,
        'Wheel_Speed_Y': DEFAULT_FLOAT,
        'Wheel_Speed_Z': DEFAULT_FLOAT,
        'Mag_Field_Vector_X': DEFAULT_FLOAT,
        'Mag_Field_Vector_Y': DEFAULT_FLOAT,
        'Mag_Field_Vector_Z': DEFAULT_FLOAT,
        'TC_num': DEFAULT_INT,
        'TM_num': DEFAULT_INT,
        'CommsStat_flags_1': DEFAULT_INT,
        'CommsStat_flags_2': DEFAULT_INT,
        'CommsStat_flags_3': DEFAULT_INT,
        'CommsStat_flags_4': DEFAULT_INT,
        'CommsStat_flags_5': DEFAULT_INT,
        'CommsStat_flags_6': DEFAULT_INT,
        'Wheel1_Current': DEFAULT_FLOAT,
        'Wheel2_Current': DEFAULT_FLOAT,
        'Wheel3_Current': DEFAULT_FLOAT,
        'CubeSense1_Current': DEFAULT_FLOAT,
        'CubeSense2_Current': DEFAULT_FLOAT,
        'CubeControl_Current3v3': DEFAULT_FLOAT,
        'CubeControl_Current5v0': DEFAULT_FLOAT,
        'CubeStar_Current': DEFAULT_FLOAT,
        'CubeStar_Temp': DEFAULT_FLOAT,
        'Magnetorquer_Current': DEFAULT_FLOAT,
        'MCU_Temp': DEFAULT_FLOAT,
        'Rate_Sensor_Temp_X': DEFAULT_INT,
        'Rate_Sensor_Temp_Y': DEFAULT_INT,
        'Rate_Sensor_Temp_Z': DEFAULT_INT
    }


def fake_athena_hk_as_dict():
    return {
        'OBC_software_ver': DEFAULT_STR,
        'MCU_core_temp': DEFAULT_INT,
        'converter_temp': DEFAULT_INT,
        'OBC_uptime': DEFAULT_INT,
        'vol0_usage_percent': DEFAULT_INT,
        'vol1_usage_percent': DEFAULT_INT,
        'boot_cnt': DEFAULT_INT,
        'boot_src': DEFAULT_INT,
        'last_reset_reason': DEFAULT_INT,
        'OBC_mode': DEFAULT_INT,
        'solar_panel_supply_curr': DEFAULT_INT,
        'cmds_received': DEFAULT_INT,
        'pckts_uncovered_by_FEC': DEFAULT_INT,
    }


def fake_eps_hk_as_dict():
    return {
        'eps_cmd_hk': DEFAULT_INT,
        'eps_status_hk': DEFAULT_INT,
        'eps_timestamp_hk': DEFAULT_FLOAT,
        'eps_uptimeInS_hk': DEFAULT_INT,
        'eps_bootCnt_hk': DEFAULT_INT,
        'wdt_gs_time_left_s': DEFAULT_INT,
        'wdt_gs_counter': DEFAULT_INT,
        'mpptConverterVoltage1_mV': DEFAULT_INT,
        'mpptConverterVoltage2_mV': DEFAULT_INT,
        'mpptConverterVoltage3_mV': DEFAULT_INT,
        'mpptConverterVoltage4_mV': DEFAULT_INT,
        'curSolarPanels1_mA': DEFAULT_INT,
        'curSolarPanels2_mA': DEFAULT_INT,
        'curSolarPanels3_mA': DEFAULT_INT,
        'curSolarPanels4_mA': DEFAULT_INT,
        'curSolarPanels5_mA': DEFAULT_INT,
        'curSolarPanels6_mA': DEFAULT_INT,
        'curSolarPanels7_mA': DEFAULT_INT,
        'curSolarPanels8_mA': DEFAULT_INT,
        'vBatt_mV': DEFAULT_INT,
        'curSolar_mA': DEFAULT_INT,
        'curBattIn_mA': DEFAULT_INT,
        'curBattOut_mA': DEFAULT_INT,
        'curOutput1_mA': DEFAULT_INT,
        'curOutput2_mA': DEFAULT_INT,
        'curOutput3_mA': DEFAULT_INT,
        'curOutput4_mA': DEFAULT_INT,
        'curOutput5_mA': DEFAULT_INT,
        'curOutput6_mA': DEFAULT_INT,
        'curOutput7_mA': DEFAULT_INT,
        'curOutput8_mA': DEFAULT_INT,
        'curOutput9_mA': DEFAULT_INT,
        'curOutput10_mA': DEFAULT_INT,
        'curOutput11_mA': DEFAULT_INT,
        'curOutput12_mA': DEFAULT_INT,
        'curOutput13_mA': DEFAULT_INT,
        'curOutput14_mA': DEFAULT_INT,
        'curOutput15_mA': DEFAULT_INT,
        'curOutput16_mA': DEFAULT_INT,
        'curOutput17_mA': DEFAULT_INT,
        'curOutput18_mA': DEFAULT_INT,
        'AOcurOutput1_mA': DEFAULT_INT,
        'AOcurOutput2_mA': DEFAULT_INT,
        'outputConverterVoltage1': DEFAULT_INT,
        'outputConverterVoltage2': DEFAULT_INT,
        'outputConverterVoltage3': DEFAULT_INT,
        'outputConverterVoltage4': DEFAULT_INT,
        'outputConverterVoltage5': DEFAULT_INT,
        'outputConverterVoltage6': DEFAULT_INT,
        'outputConverterVoltage7': DEFAULT_INT,
        'outputConverterVoltage8': DEFAULT_INT,
        'outputConverterState': DEFAULT_INT,
        'outputStatus': DEFAULT_INT,
        'outputFaultStatus': DEFAULT_INT,
        'protectedOutputAccessCnt': DEFAULT_INT,
        'outputOnDelta1': DEFAULT_INT,
        'outputOnDelta2': DEFAULT_INT,
        'outputOnDelta3': DEFAULT_INT,
        'outputOnDelta4': DEFAULT_INT,
        'outputOnDelta5': DEFAULT_INT,
        'outputOnDelta6': DEFAULT_INT,
        'outputOnDelta7': DEFAULT_INT,
        'outputOnDelta8': DEFAULT_INT,
        'outputOnDelta9': DEFAULT_INT,
        'outputOnDelta10': DEFAULT_INT,
        'outputOnDelta11': DEFAULT_INT,
        'outputOnDelta12': DEFAULT_INT,
        'outputOnDelta13': DEFAULT_INT,
        'outputOnDelta14': DEFAULT_INT,
        'outputOnDelta15': DEFAULT_INT,
        'outputOnDelta16': DEFAULT_INT,
        'outputOnDelta17': DEFAULT_INT,
        'outputOnDelta18': DEFAULT_INT,
        'outputOffDelta1': DEFAULT_INT,
        'outputOffDelta2': DEFAULT_INT,
        'outputOffDelta3': DEFAULT_INT,
        'outputOffDelta4': DEFAULT_INT,
        'outputOffDelta5': DEFAULT_INT,
        'outputOffDelta6': DEFAULT_INT,
        'outputOffDelta7': DEFAULT_INT,
        'outputOffDelta8': DEFAULT_INT,
        'outputOffDelta9': DEFAULT_INT,
        'outputOffDelta10': DEFAULT_INT,
        'outputOffDelta11': DEFAULT_INT,
        'outputOffDelta12': DEFAULT_INT,
        'outputOffDelta13': DEFAULT_INT,
        'outputOffDelta14': DEFAULT_INT,
        'outputOffDelta15': DEFAULT_INT,
        'outputOffDelta16': DEFAULT_INT,
        'outputOffDelta17': DEFAULT_INT,
        'outputOffDelta18': DEFAULT_INT,
        'outputFaultCount1': DEFAULT_INT,
        'outputFaultCount2': DEFAULT_INT,
        'outputFaultCount3': DEFAULT_INT,
        'outputFaultCount4': DEFAULT_INT,
        'outputFaultCount5': DEFAULT_INT,
        'outputFaultCount6': DEFAULT_INT,
        'outputFaultCount7': DEFAULT_INT,
        'outputFaultCount8': DEFAULT_INT,
        'outputFaultCount9': DEFAULT_INT,
        'outputFaultCount10': DEFAULT_INT,
        'outputFaultCount11': DEFAULT_INT,
        'outputFaultCount12': DEFAULT_INT,
        'outputFaultCount13': DEFAULT_INT,
        'outputFaultCount14': DEFAULT_INT,
        'outputFaultCount15': DEFAULT_INT,
        'outputFaultCount16': DEFAULT_INT,
        'outputFaultCount17': DEFAULT_INT,
        'outputFaultCount18': DEFAULT_INT,
        'temp1_c': DEFAULT_INT,
        'temp2_c': DEFAULT_INT,
        'temp3_c': DEFAULT_INT,
        'temp4_c': DEFAULT_INT,
        'temp5_c': DEFAULT_INT,
        'temp6_c': DEFAULT_INT,
        'temp7_c': DEFAULT_INT,
        'temp8_c': DEFAULT_INT,
        'temp9_c': DEFAULT_INT,
        'temp10_c': DEFAULT_INT,
        'temp11_c': DEFAULT_INT,
        'temp12_c': DEFAULT_INT,
        'temp13_c': DEFAULT_INT,
        'temp14_c': DEFAULT_INT,
        'battMode': DEFAULT_INT,
        'mpptMode': DEFAULT_INT,
        'battHeaterMode': DEFAULT_INT,
        'battHeaterState': DEFAULT_INT,
        'PingWdt_toggles': DEFAULT_INT,
        'PingWdt_turnOffs': DEFAULT_INT,
        'thermalProtTemperature_1': DEFAULT_INT,
        'thermalProtTemperature_2': DEFAULT_INT,
        'thermalProtTemperature_3': DEFAULT_INT,
        'thermalProtTemperature_4': DEFAULT_INT,
        'thermalProtTemperature_5': DEFAULT_INT,
        'thermalProtTemperature_6': DEFAULT_INT,
        'thermalProtTemperature_7': DEFAULT_INT,
        'thermalProtTemperature_8': DEFAULT_INT,
    }


def fake_eps_startup_hk_as_dict():
    return {
        'eps_cmd_startup': DEFAULT_INT,
        'eps_status_startup': DEFAULT_INT,
        'eps_timestamp_startup': DEFAULT_FLOAT,
        'last_reset_reason_reg': DEFAULT_INT,
        'eps_bootCnt_startup': DEFAULT_INT,
        'FallbackConfigUsed': DEFAULT_INT,
        'rtcInit': DEFAULT_INT,
        'rtcClkSourceLSE': DEFAULT_INT,
        'flashAppInit': DEFAULT_INT,
        'Fram4kPartitionInit': DEFAULT_INT,
        'Fram520kPartitionInit': DEFAULT_INT,
        'intFlashPartitionInit': DEFAULT_INT,
        'fwUpdInit': DEFAULT_INT,
        'FSInit': DEFAULT_INT,
        'FTInit': DEFAULT_INT,
        'supervisorInit': DEFAULT_INT,
        'uart1App': DEFAULT_INT,
        'uart2App': DEFAULT_INT,
        'tmp107Init': DEFAULT_INT,
    }


def fake_uhf_hk_as_dict():
    return {
        'scw1': DEFAULT_INT,
        'scw2': DEFAULT_INT,
        'scw3': DEFAULT_INT,
        'scw4': DEFAULT_INT,
        'scw5': DEFAULT_INT,
        'scw6': DEFAULT_INT,
        'scw7': DEFAULT_INT,
        'scw8': DEFAULT_INT,
        'scw9': DEFAULT_INT,
        'scw10': DEFAULT_INT,
        'scw11': DEFAULT_INT,
        'scw12': DEFAULT_INT,
        'U_frequency': DEFAULT_INT,
        'pipe_t': DEFAULT_INT,
        'beacon_t': DEFAULT_INT,
        'audio_t': DEFAULT_INT,
        'uptime': DEFAULT_INT,
        'pckts_out': DEFAULT_INT,
        'pckts_in': DEFAULT_INT,
        'pckts_in_crc16': DEFAULT_INT,
        'temperature': DEFAULT_FLOAT
    }


def fake_sband_hk_as_dict():
    return {
        'S_mode': DEFAULT_INT,
        'PA_status': DEFAULT_INT,
        'S_frequency_Hz': DEFAULT_INT,
        'S_scrambler': DEFAULT_INT,
        'S_filter': DEFAULT_INT,
        'S_modulation': DEFAULT_INT,
        'S_data_rate': DEFAULT_INT,
        'S_bit_order': DEFAULT_INT,
        'S_PWRGD': DEFAULT_INT,
        'S_TXL': DEFAULT_INT,
        'Output_Power': DEFAULT_INT,
        'PA_Temp': DEFAULT_INT,
        'Top_Temp': DEFAULT_INT,
        'Bottom_Temp': DEFAULT_INT,
        'Bat_Current_mA': DEFAULT_INT,
        'Bat_Voltage_mV': DEFAULT_INT,
        'PA_Current_mA': DEFAULT_INT,
        'PA_Voltage_mV': DEFAULT_INT,
    }


def fake_hyperion_hk_as_dict():
    return {
        'Nadir_Temp1': DEFAULT_INT,
        'Nadir_Temp_Adc': DEFAULT_INT,
        'Port_Temp1': DEFAULT_INT,
        'Port_Temp2': DEFAULT_INT,
        'Port_Temp3': DEFAULT_INT,
        'Port_Temp_Adc': DEFAULT_INT,
        'Port_Dep_Temp1': DEFAULT_INT,
        'Port_Dep_Temp2': DEFAULT_INT,
        'Port_Dep_Temp3': DEFAULT_INT,
        'Port_Dep_Temp_Adc': DEFAULT_INT,
        'Star_Temp1': DEFAULT_INT,
        'Star_Temp2': DEFAULT_INT,
        'Star_Temp3': DEFAULT_INT,
        'Star_Temp_Adc': DEFAULT_INT,
        'Star_Dep_Temp1': DEFAULT_INT,
        'Star_Dep_Temp2': DEFAULT_INT,
        'Star_Dep_Temp3': DEFAULT_INT,
        'Star_Dep_Temp_Adc': DEFAULT_INT,
        'Zenith_Temp1': DEFAULT_INT,
        'Zenith_Temp2': DEFAULT_INT,
        'Zenith_Temp3': DEFAULT_INT,
        'Zenith_Temp_Adc': DEFAULT_INT,
        'Nadir_Pd1': DEFAULT_INT,
        'Port_Pd1': DEFAULT_INT,
        'Port_Pd2': DEFAULT_INT,
        'Port_Pd3': DEFAULT_INT,
        'Port_Dep_Pd1': DEFAULT_INT,
        'Port_Dep_Pd2': DEFAULT_INT,
        'Port_Dep_Pd3': DEFAULT_INT,
        'Star_Pd1': DEFAULT_INT,
        'Star_Pd2': DEFAULT_INT,
        'Star_Pd3': DEFAULT_INT,
        'Star_Dep_Pd1': DEFAULT_INT,
        'Star_Dep_Pd2': DEFAULT_INT,
        'Star_Dep_Pd3': DEFAULT_INT,
        'Zenith_Pd1': DEFAULT_INT,
        'Zenith_Pd2': DEFAULT_INT,
        'Zenith_Pd3': DEFAULT_INT,
        'Port_Voltage': DEFAULT_INT,
        'Port_Dep_Voltage': DEFAULT_INT,
        'Star_Voltage': DEFAULT_INT,
        'Star_Dep_Voltage': DEFAULT_INT,
        'Zenith_Voltage': DEFAULT_INT,
        'Port_Current': DEFAULT_INT,
        'Port_Dep_Current': DEFAULT_INT,
        'Star_Current': DEFAULT_INT,
        'Star_Dep_Current': DEFAULT_INT,
        'Zenith_Current': DEFAULT_INT
    }


def fake_charon_hk_as_dict():
    return {
        'gps_crc': DEFAULT_INT,
        'charon_temp1': DEFAULT_INT,
        'charon_temp2': DEFAULT_INT,
        'charon_temp3': DEFAULT_INT,
        'charon_temp4': DEFAULT_INT,
        'charon_temp5': DEFAULT_INT,
        'charon_temp6': DEFAULT_INT,
        'charon_temp7': DEFAULT_INT,
        'charon_temp8': DEFAULT_INT
    }


def fake_dfgm_hk_as_dict():
    return {
        'Core_Voltage': DEFAULT_INT,
        'Sensor_Temperature': DEFAULT_INT,
        'Reference_Temperature': DEFAULT_INT,
        'Board_Temperature': DEFAULT_INT,
        'Positive_Rail_Voltage': DEFAULT_INT,
        'Input_Voltage': DEFAULT_INT,
        'Reference_Voltage': DEFAULT_INT,
        'Input_Current': DEFAULT_INT,
        'Reserved_1': DEFAULT_INT,
        'Reserved_2': DEFAULT_INT,
        'Reserved_3': DEFAULT_INT,
        'Reserved_4': DEFAULT_INT
    }


def fake_northern_spirit_hk_as_dict():
    return {
        'ns_temp0': DEFAULT_INT,
        'ns_temp1': DEFAULT_INT,
        'ns_temp2': DEFAULT_INT,
        'ns_temp3': DEFAULT_INT,
        'eNIM0_lux': DEFAULT_INT,
        'eNIM1_lux': DEFAULT_INT,
        'eNIM2_lux': DEFAULT_INT,
        'ram_avail': DEFAULT_INT,
        'lowest_img_num': DEFAULT_INT,
        'first_blank_img_num': DEFAULT_INT
    }


def fake_iris_hk_as_dict():
    return {
        'VIS_Temperature': DEFAULT_FLOAT,
        'NIR_Temperature': DEFAULT_FLOAT,
        'Flash_Temperature': DEFAULT_FLOAT,
        'Gate_Temperature': DEFAULT_FLOAT,
        'Image_number': DEFAULT_INT,
        'Software_Version': DEFAULT_INT,
        'Error_number': DEFAULT_INT,
        'MAX_5V_voltage': DEFAULT_INT,
        'MAX_5V_power': DEFAULT_INT,
        'MAX_3V_voltage': DEFAULT_INT,
        'MAX_3V_power': DEFAULT_INT,
        'MIN_5V_voltage': DEFAULT_INT,
        'MIN_3V_voltage': DEFAULT_INT
    }


def fake_flight_schedule_as_dict(status=2, commands=[], execution_time=None):
    flightschedule = {
        'status':status,
        'commands':commands,
        'execution_time': execution_time,
        'error': 0
    }
    return flightschedule


def fake_passover_as_dict(timestamps):
    """Create mock passovers as a dictionary

    :param list(datetime.datetime) timestamps: The passover timestamps to use
    """
    return {
        'passovers':[{'aos_timestamp':str(timestamp), 'los_timestamp':str(timestamp)} for timestamp in timestamps]
    }


def fake_message_as_dict(message='test', sender='tester', receiver='tester2'):
    fake_message = {
        'message': message,
        'sender': sender,
        'receiver': receiver,
        'timestamp': datetime.datetime.now(datetime.timezone.utc),
        'is_queued': False
    }

    return fake_message


def fake_patch_update_as_dict(timestamp):
    return {'status': 2,
            'error': 0,
            'execution_time': str(timestamp),
            'commands': [
                {
                    'op': 'replace',
                    'flightschedule_command_id': 1,
                    'timestamp': str(timestamp),
                    'args' : [],
                    'command': {'command_id': 2},
                    'repeats': {
                        'repeat_ms': False,
                        'repeat_sec': False,
                        'repeat_min': False,
                        'repeat_hr': False,
                        'repeat_day': False,
                        'repeat_month': False,
                        'repeat_year': False
                    }
                },
                {
                    'op': 'add',
                    'timestamp': str(timestamp),
                    'args' : [],
                    'command': {'command_id': 1},
                    'repeats': {
                        'repeat_ms': False,
                        'repeat_sec': False,
                        'repeat_min': False,
                        'repeat_hr': False,
                        'repeat_day': False,
                        'repeat_month': False,
                        'repeat_year': False
                    }
                }
            ]
            }


def fake_user_as_dict(username, password):
    return {
        'username': username,
        'password': password
    }


def fake_telecommand_as_dict(command_name='test', num_arguments='0', is_dangerous=False):
    return {'command_name': command_name,
            'num_arguments': num_arguments,
            'is_dangerous': is_dangerous
            }

def fake_automatedcommand_as_dict(command_id=1, priority=0, args=[]):
    return {
        'command': {
            'command_id': command_id
        },
        'priority': priority,
        'args': []
    }
