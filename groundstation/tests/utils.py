import datetime

# Default values for each datatype in fake housekeeping data
DEFAULT_INT = 42
DEFAULT_FLOAT = 13.37
DEFAULT_BYTES = b'\x4e\x65\x76\x65\x72\x20\x67\x6f\x6e\x6e\x61\x20\x67\x69\x76\x65\x20\x79\x6f\x75\x20\x75\x70\x21'


def fake_housekeeping_as_dict(timestamp, data_position):
    return {
        'timestamp': timestamp,
        'data_position': data_position,
        'tle': '1 25544U 98067A   22194.51466271  .00006028  00000+0  11379-3 0  9999\n2 25544  51.6428 206.1919 0004833   7.6129 121.4090 15.49927705349269',
    }


def fake_adcs_hk_as_dict():
    return {
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
        'CommsStat_flags_1': DEFAULT_BYTES,
        'CommsStat_flags_2': DEFAULT_BYTES,
        'CommsStat_flags_3': DEFAULT_BYTES,
        'CommsStat_flags_4': DEFAULT_BYTES,
        'CommsStat_flags_5': DEFAULT_BYTES,
        'CommsStat_flags_6': DEFAULT_BYTES,
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
        'temparray1': DEFAULT_INT,
        'temparray2': DEFAULT_INT,
        'boot_cnt': DEFAULT_INT,
        'last_reset_reason': DEFAULT_BYTES,
        'OBC_mode': DEFAULT_BYTES,
        'OBC_uptime': DEFAULT_INT,
        'OBC_software_ver': DEFAULT_BYTES,
        'solar_panel_supply_curr': DEFAULT_INT,
        'cmds_received': DEFAULT_INT,
        'pckts_incovered_by_FEC': DEFAULT_INT,
    }


def fake_eps_hk_as_dict():
    return {
        'cmd': DEFAULT_BYTES,
        'status': DEFAULT_BYTES,
        'timestamp': DEFAULT_FLOAT,
        'uptimeInS': DEFAULT_INT,
        'bootCnt': DEFAULT_INT,
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
        'outputConverterState': DEFAULT_BYTES,
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
        'outputFaultCount1': DEFAULT_BYTES,
        'outputFaultCount2': DEFAULT_BYTES,
        'outputFaultCount3': DEFAULT_BYTES,
        'outputFaultCount4': DEFAULT_BYTES,
        'outputFaultCount5': DEFAULT_BYTES,
        'outputFaultCount6': DEFAULT_BYTES,
        'outputFaultCount7': DEFAULT_BYTES,
        'outputFaultCount8': DEFAULT_BYTES,
        'outputFaultCount9': DEFAULT_BYTES,
        'outputFaultCount10': DEFAULT_BYTES,
        'outputFaultCount11': DEFAULT_BYTES,
        'outputFaultCount12': DEFAULT_BYTES,
        'outputFaultCount13': DEFAULT_BYTES,
        'outputFaultCount14': DEFAULT_BYTES,
        'outputFaultCount15': DEFAULT_BYTES,
        'outputFaultCount16': DEFAULT_BYTES,
        'outputFaultCount17': DEFAULT_BYTES,
        'outputFaultCount18': DEFAULT_BYTES,
        'temp1_c': DEFAULT_BYTES,
        'temp2_c': DEFAULT_BYTES,
        'temp3_c': DEFAULT_BYTES,
        'temp4_c': DEFAULT_BYTES,
        'temp5_c': DEFAULT_BYTES,
        'temp6_c': DEFAULT_BYTES,
        'temp7_c': DEFAULT_BYTES,
        'temp8_c': DEFAULT_BYTES,
        'temp9_c': DEFAULT_BYTES,
        'temp10_c': DEFAULT_BYTES,
        'temp11_c': DEFAULT_BYTES,
        'temp12_c': DEFAULT_BYTES,
        'temp13_c': DEFAULT_BYTES,
        'temp14_c': DEFAULT_BYTES,
        'battMode': DEFAULT_BYTES,
        'mpptMode': DEFAULT_BYTES,
        'battHeaterMode': DEFAULT_BYTES,
        'battHeaterState': DEFAULT_BYTES,
        'PingWdt_toggles': DEFAULT_INT,
        'PingWdt_turnOffs': DEFAULT_BYTES,
    }


def fake_uhf_hk_as_dict():
    return {
        'scw1': DEFAULT_BYTES,
        'scw2': DEFAULT_BYTES,
        'scw3': DEFAULT_BYTES,
        'scw4': DEFAULT_BYTES,
        'scw5': DEFAULT_BYTES,
        'scw6': DEFAULT_BYTES,
        'scw7': DEFAULT_BYTES,
        'scw8': DEFAULT_BYTES,
        'scw9': DEFAULT_BYTES,
        'scw10': DEFAULT_BYTES,
        'scw11': DEFAULT_BYTES,
        'scw12': DEFAULT_BYTES,
        'freq': DEFAULT_INT,
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
        'Output_Power': DEFAULT_FLOAT,
        'PA_Temp': DEFAULT_FLOAT,
        'Top_Temp': DEFAULT_FLOAT,
        'Bottom_Temp': DEFAULT_FLOAT,
        'Bat_Current': DEFAULT_FLOAT,
        'Bat_Voltage': DEFAULT_FLOAT,
        'PA_Current': DEFAULT_FLOAT,
        'PA_Voltage': DEFAULT_FLOAT
    }


def fake_hyperion_hk_as_dict():
    return {
        'Nadir_Temp1': DEFAULT_BYTES,
        'Nadir_Temp_Adc': DEFAULT_BYTES,
        'Port_Temp1': DEFAULT_BYTES,
        'Port_Temp2': DEFAULT_BYTES,
        'Port_Temp3': DEFAULT_BYTES,
        'Port_Temp_Adc': DEFAULT_BYTES,
        'Port_Dep_Temp1': DEFAULT_BYTES,
        'Port_Dep_Temp2': DEFAULT_BYTES,
        'Port_Dep_Temp3': DEFAULT_BYTES,
        'Port_Dep_Temp_Adc': DEFAULT_BYTES,
        'Star_Temp1': DEFAULT_BYTES,
        'Star_Temp2': DEFAULT_BYTES,
        'Star_Temp3': DEFAULT_BYTES,
        'Star_Temp_Adc': DEFAULT_BYTES,
        'Star_Dep_Temp1': DEFAULT_BYTES,
        'Star_Dep_Temp2': DEFAULT_BYTES,
        'Star_Dep_Temp3': DEFAULT_BYTES,
        'Star_Dep_Temp_Adc': DEFAULT_BYTES,
        'Zenith_Temp1': DEFAULT_BYTES,
        'Zenith_Temp2': DEFAULT_BYTES,
        'Zenith_Temp3': DEFAULT_BYTES,
        'Zenith_Temp_Adc': DEFAULT_BYTES,
        'Nadir_Pd1': DEFAULT_BYTES,
        'Port_Pd1': DEFAULT_BYTES,
        'Port_Pd2': DEFAULT_BYTES,
        'Port_Pd3': DEFAULT_BYTES,
        'Port_Dep_Pd1': DEFAULT_BYTES,
        'Port_Dep_Pd2': DEFAULT_BYTES,
        'Port_Dep_Pd3': DEFAULT_BYTES,
        'Star_Pd1': DEFAULT_BYTES,
        'Star_Pd2': DEFAULT_BYTES,
        'Star_Pd3': DEFAULT_BYTES,
        'Star_Dep_Pd1': DEFAULT_BYTES,
        'Star_Dep_Pd2': DEFAULT_BYTES,
        'Star_Dep_Pd3': DEFAULT_BYTES,
        'Zenith_Pd1': DEFAULT_BYTES,
        'Zenith_Pd2': DEFAULT_BYTES,
        'Zenith_Pd3': DEFAULT_BYTES,
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
        'charon_temp1': DEFAULT_BYTES,
        'charon_temp2': DEFAULT_BYTES,
        'charon_temp3': DEFAULT_BYTES,
        'charon_temp4': DEFAULT_BYTES,
        'charon_temp5': DEFAULT_BYTES,
        'charon_temp6': DEFAULT_BYTES,
        'charon_temp7': DEFAULT_BYTES,
        'charon_temp8': DEFAULT_BYTES
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


def fake_flight_schedule_as_dict(status=2, commands=[], execution_time=None):
    flightschedule = {
        'status': status,
        'commands': commands,
        'execution_time': execution_time
    }
    return flightschedule


def fake_passover_as_dict(timestamps):
    """Create mock passovers as a dictionary

    :param list(datetime.datetime) timestamps: The passover timestamps to use
    """
    return {
        'passovers': [{'timestamp': str(timestamp)} for timestamp in timestamps]
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
            'execution_time': str(timestamp),
            'commands': [
                {'op': 'replace',
                 'flightschedule_command_id': 1,
                 'timestamp': str(timestamp),
                 'args': [],
                 'command': {'command_id': 2}},
                {'op': 'add', 'timestamp': str(timestamp), 'args': [], 'command': {
                    'command_id': 1}}
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
